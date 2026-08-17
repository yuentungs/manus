"""Download public World Bank indicators for APAC jewellery market-entry analysis.

The script saves raw observation records and deliberately preserves each indicator's
latest available year, because data coverage can vary across markets and series.
"""

from __future__ import annotations

import json
import time
from datetime import date
from pathlib import Path

import pandas as pd
import requests

SCRIPT_PATH = Path(__file__).resolve()
ROOT = SCRIPT_PATH.parent.parent if SCRIPT_PATH.parent.name == "src" else SCRIPT_PATH.parent
RAW_DIR = ROOT / "data" / "raw" if (ROOT / "data").exists() else ROOT
RAW_DIR.mkdir(parents=True, exist_ok=True)

COUNTRIES = {
    "HKG": "Hong Kong SAR, China",
    "SGP": "Singapore",
    "THA": "Thailand",
    "MYS": "Malaysia",
    "VNM": "Vietnam",
    "IDN": "Indonesia",
}

INDICATORS = {
    "NY.GDP.PCAP.CD": "gdp_per_capita_current_usd",
    "IT.NET.USER.ZS": "internet_users_pct",
    "NY.GDP.MKTP.CD": "gdp_current_usd",
    "SP.URB.TOTL.IN.ZS": "urban_population_pct",
}

API_ROOT = "https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}"


def get_series(indicator: str) -> list[dict]:
    """Return non-null World Bank observations for all selected markets.

    A single batched request per indicator reduces network calls; a bounded retry
    loop handles intermittent upstream timeouts without obscuring the source URL.
    """
    countries = ";".join(COUNTRIES)
    endpoint = API_ROOT.format(countries=countries, indicator=indicator)
    response = None
    for attempt in range(1, 4):
        try:
            response = requests.get(
                endpoint,
                params={"format": "json", "per_page": 1000, "date": "2024:2024"},
                timeout=60,
            )
            response.raise_for_status()
            break
        except requests.RequestException:
            if attempt == 3:
                raise
            time.sleep(attempt * 2)
    assert response is not None
    payload = response.json()
    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        return []

    records = []
    for observation in payload[1]:
        value = observation.get("value")
        country = observation.get("countryiso3code")
        if value is None or country not in COUNTRIES:
            continue
        records.append(
            {
                "country_code": country,
                "country": COUNTRIES[country],
                "indicator_code": indicator,
                "indicator": INDICATORS[indicator],
                "year": int(observation["date"]),
                "value": float(value),
                "source": "World Development Indicators via World Bank API",
                "api_url": response.url,
            }
        )
    return records


def main() -> None:
    records: list[dict] = []
    for indicator in INDICATORS:
        records.extend(get_series(indicator))

    data = pd.DataFrame(records)
    if data.empty:
        raise RuntimeError("No World Bank observations were returned.")

    data.to_csv(RAW_DIR / "world_bank_wdi_observations.csv", index=False)
    (RAW_DIR / "download_metadata.json").write_text(
        json.dumps(
            {
                "download_date": date.today().isoformat(),
                "countries": COUNTRIES,
                "indicators": INDICATORS,
                "period_requested": "2024",
                "source_note": "Values are retrieved from World Bank API endpoints recorded in the CSV.",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Saved {len(data):,} observations to {RAW_DIR / 'world_bank_wdi_observations.csv'}")


if __name__ == "__main__":
    main()
