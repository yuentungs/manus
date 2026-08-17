"""Create a transparent APAC jewellery market-entry signal framework.

The outputs are prioritisation hypotheses based on macro proxies. They are not
jewellery-market forecasts, investment advice, or recommendations to enter a market.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "world_bank_wdi_observations.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
OUTPUT_DIR = ROOT / "outputs"
FIGURE_DIR = ROOT / "figures"

for directory in (PROCESSED_DIR, OUTPUT_DIR, FIGURE_DIR):
    directory.mkdir(parents=True, exist_ok=True)

INDICATORS = [
    "gdp_per_capita_current_usd",
    "internet_users_pct",
    "gdp_current_usd",
    "urban_population_pct",
]

SCENARIOS = {
    "balanced": {
        "purchasing_power": 0.25,
        "digital_readiness": 0.25,
        "urban_retail_context": 0.25,
        "economic_scale": 0.25,
    },
    "digital_first": {
        "purchasing_power": 0.35,
        "digital_readiness": 0.35,
        "urban_retail_context": 0.20,
        "economic_scale": 0.10,
    },
    "scale_led": {
        "purchasing_power": 0.20,
        "digital_readiness": 0.15,
        "urban_retail_context": 0.20,
        "economic_scale": 0.45,
    },
}


def latest_series(data: pd.DataFrame, indicator: str) -> pd.DataFrame:
    """Select the latest available value by country for an indicator."""
    subset = data.loc[data["indicator"] == indicator].copy()
    subset = subset.sort_values(["country_code", "year"], ascending=[True, False])
    return subset.drop_duplicates("country_code", keep="first").set_index("country_code")


def min_max(series: pd.Series) -> pd.Series:
    span = series.max() - series.min()
    if span == 0:
        return pd.Series(0.5, index=series.index)
    return (series - series.min()) / span


def main() -> None:
    raw = pd.read_csv(RAW_FILE)
    pivot = pd.DataFrame()
    display_names = latest_series(raw, "gdp_per_capita_current_usd")[["country"]].copy()

    for indicator in INDICATORS:
        selected = latest_series(raw, indicator)
        pivot[indicator] = selected["value"]
        pivot[f"{indicator}_year"] = selected["year"]

    pivot = display_names.join(pivot, how="left")
    missing = pivot[INDICATORS].isna().any(axis=1)
    if missing.any():
        missing_markets = ", ".join(pivot.index[missing])
        raise RuntimeError(f"Missing required indicator coverage for: {missing_markets}")

    pivot["purchasing_power"] = min_max(pivot["gdp_per_capita_current_usd"])
    pivot["digital_readiness"] = min_max(pivot["internet_users_pct"])
    pivot["urban_retail_context"] = min_max(pivot["urban_population_pct"])
    # Log-transform economic scale so the largest market does not mechanically dominate.
    pivot["economic_scale"] = min_max(np.log1p(pivot["gdp_current_usd"]))

    score_columns = []
    for scenario, weights in SCENARIOS.items():
        score_name = f"score_{scenario}"
        pivot[score_name] = sum(pivot[metric] * weight for metric, weight in weights.items())
        pivot[f"rank_{scenario}"] = pivot[score_name].rank(ascending=False, method="min").astype(int)
        score_columns.append(score_name)

    pivot["rank_range"] = (
        pivot[[f"rank_{scenario}" for scenario in SCENARIOS]].max(axis=1)
        - pivot[[f"rank_{scenario}" for scenario in SCENARIOS]].min(axis=1)
    )
    pivot["rank_stability"] = np.where(pivot["rank_range"] == 0, "stable", "scenario-sensitive")

    output = pivot.reset_index().rename(columns={"index": "country_code"})
    output = output.sort_values("rank_balanced")
    output.to_csv(OUTPUT_DIR / "market_priority_scores.csv", index=False)
    output.to_csv(PROCESSED_DIR / "market_signal_panel.csv", index=False)

    coverage_columns = [
        "country",
        "gdp_per_capita_current_usd_year",
        "internet_users_pct_year",
        "gdp_current_usd_year",
        "urban_population_pct_year",
    ]
    output[coverage_columns].to_csv(OUTPUT_DIR / "data_coverage.csv", index=False)

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(11, 7))
    scatter = ax.scatter(
        output["digital_readiness"],
        output["economic_scale"],
        s=300 + output["purchasing_power"] * 1600,
        c=output["score_balanced"],
        cmap="viridis",
        alpha=0.85,
        edgecolors="white",
        linewidth=1.2,
    )
    label_offsets = {
        "Hong Kong SAR, China": (8, -14),
        "Malaysia": (8, 12),
        "Indonesia": (8, -15),
    }
    for _, row in output.iterrows():
        ax.annotate(
            row["country"],
            (row["digital_readiness"], row["economic_scale"]),
            xytext=label_offsets.get(row["country"], (7, 7)),
            textcoords="offset points",
            fontsize=9,
        )
    ax.set_title("APAC Jewellery Market Prioritisation — Balanced Scenario", fontweight="bold")
    ax.set_xlabel("Digital readiness (min–max normalised internet use)")
    ax.set_ylabel("Economic-scale context (min–max normalised log GDP)")
    ax.text(
        0.02,
        0.04,
        "Bubble size: purchasing-power context",
        transform=ax.transAxes,
        va="bottom",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.8, "edgecolor": "none"},
    )
    colourbar = fig.colorbar(scatter, ax=ax)
    colourbar.set_label("Balanced signal score")
    fig.text(
        0.01,
        0.01,
        "Macro-demand framework only; not a jewellery sales forecast or market-entry recommendation.",
        fontsize=8,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(FIGURE_DIR / "market_entry_signals.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    readme = [
        "# APAC Jewellery Market Entry Signal Results",
        "",
        "The balanced scenario gives each 2024 macro signal equal weight: purchasing-power context, digital readiness, urban retail context and economic scale.",
        "",
        "| Market | Balanced rank | Balanced score | Rank stability |",
        "|---|---:|---:|---|",
    ]
    for _, row in output.iterrows():
        readme.append(
            f"| {row['country']} | {row['rank_balanced']} | {row['score_balanced']:.3f} | {row['rank_stability']} |"
        )
    readme.extend(
        [
            "",
            "## Interpretation discipline",
            "",
            "A higher score is a research-prioritisation signal under the stated weights—not a claim of market size, product-market fit, jewellery demand, margin, regulatory readiness, or a recommendation to enter a market. The `data_coverage.csv` file shows the year used for each input and should be reviewed before drawing a conclusion.",
            "",
            "## Sensitivity scenarios",
            "",
            "The model also tests a digital-first scenario and a scale-led scenario. Markets whose ranking changes across scenarios are flagged as scenario-sensitive, signalling the need for qualitative validation before resource allocation.",
        ]
    )
    (OUTPUT_DIR / "results_summary.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    print(f"Saved results to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
