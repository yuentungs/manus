"""Generate a transparent candidate-fit report from official job-posting requirements.

This project intentionally uses explicit, reviewable rules. It is not an automated
recruiting system and does not make hiring recommendations.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pandas as pd

SCRIPT_PATH = Path(__file__).resolve()
ROOT = SCRIPT_PATH.parent.parent if SCRIPT_PATH.parent.name == "src" else SCRIPT_PATH.parent
DATA_FILE = ROOT / "data" / "auction_house_roles.csv"
REPORT_FILE = ROOT / "reports" / "role_fit_report.md"

# Flat-file fallback for browser-based GitHub uploads.
if not DATA_FILE.exists():
    DATA_FILE = ROOT / "auction_house_roles.csv"
if not REPORT_FILE.parent.exists():
    REPORT_FILE = ROOT / "role_fit_report.md"

# Evidence deliberately limited to the information provided for the portfolio.
# In particular, no GIA/FGA, French, collector network, or direct auction-house
# specialist credentials are inferred.
EVIDENCE = {
    "operations": (
        "Direct evidence",
        "Ten years in jewellery product management, including product development and production-process optimisation.",
    ),
    "client_service": (
        "Transferable evidence",
        "Senior product-management work requires cross-functional stakeholder coordination; direct private-sales client-service experience is not claimed.",
    ),
    "compliance": (
        "Transferable evidence",
        "Production-process and supply-chain optimisation indicate documentation discipline; auction compliance experience is not claimed.",
    ),
    "data": (
        "Direct evidence",
        "Python/SQL data-analysis capability, with a public reproducible role-intelligence project.",
    ),
    "experience": (
        "Direct evidence",
        "Approximately ten years of senior jewellery-industry experience.",
    ),
    "languages": (
        "Development gap",
        "Language fluency must be confirmed by the candidate; this project does not infer language proficiency.",
    ),
    "jewellery_market": (
        "Transferable evidence",
        "Long-term jewellery product experience and Mainland China/Southeast Asia market familiarity; specialist knowledge of gemstones and signed jewels is not claimed.",
    ),
    "valuation": (
        "Development gap",
        "No direct auction-house valuation or appraisal record is represented.",
    ),
    "network": (
        "Development gap",
        "No established European collector or dealer network is represented.",
    ),
    "qualification": (
        "Development gap",
        "No GIA/FGA or equivalent qualification is represented.",
    ),
    "business_development": (
        "Transferable evidence",
        "Regional market knowledge may support commercial development; property sourcing and auction-consignment results are not claimed.",
    ),
    "leadership": (
        "Direct evidence",
        "Senior product-management background supports team and project leadership evidence, subject to CV substantiation.",
    ),
    "presentation": (
        "Transferable evidence",
        "Product-management experience supports presentation and stakeholder communication; auction-client negotiation results are not claimed.",
    ),
}


def evidence_for(row: pd.Series) -> tuple[str, str]:
    """Return requirement-specific evidence while avoiding inflated seniority claims."""
    if row["requirement_id"] == "PHI-04":
        return (
            "Transferable evidence",
            "Approximately ten years in a recognised jewellery business; this is not presented as five years in an auction-house specialist role.",
        )
    return EVIDENCE.get(
        row["requirement_area"],
        ("Development gap", "No evidence rule is available for this requirement."),
    )


def add_role_summary(lines: list[str], role: pd.DataFrame) -> None:
    first = role.iloc[0]
    title = first["job_title"]
    company = first["company"]
    location = first["location"]
    source = first["source_url"]

    lines.append(f"## {company} — {title}")
    lines.append("")
    lines.append(f"**Location:** {location}  ")
    lines.append(f"**Official source:** {source}")
    lines.append("")
    lines.append("| Requirement area | Official requirement summary | Evidence status | Interpretation |")
    lines.append("|---|---|---|---|")

    for _, row in role.iterrows():
        status, interpretation = evidence_for(row)
        lines.append(
            "| {area} | {summary} | **{status}** | {interpretation} |".format(
                area=row["requirement_area"].replace("_", " ").title(),
                summary=row["requirement_summary"],
                status=status,
                interpretation=interpretation,
            )
        )

    counts = Counter(evidence_for(row)[0] for _, row in role.iterrows())
    lines.append("")
    lines.append(
        "**Evidence summary:** "
        f"{counts['Direct evidence']} direct, "
        f"{counts['Transferable evidence']} transferable, and "
        f"{counts['Development gap']} development-gap requirements."
    )
    lines.append("")


def main() -> None:
    roles = pd.read_csv(DATA_FILE)
    lines = [
        "# Jewellery & Auction Role Intelligence — Role Fit Report",
        "",
        "**Generated:** 2026-08-17  ",
        "**Method:** Explicit rule-based mapping of public role requirements against disclosed candidate evidence.",
        "",
        "> This report is a preparation aid, not a hiring recommendation. It distinguishes direct evidence, transferable evidence, and development gaps so that application materials remain accurate.",
        "",
    ]

    for _, role in roles.groupby("role_id", sort=False):
        add_role_summary(lines, role)

    lines.extend(
        [
            "## Application positioning",
            "",
            "For the Sotheby’s role, the strongest truthful narrative is operational control across a complex product lifecycle: documentation, supplier/process coordination, quality discipline, market awareness, and data literacy. The application should not imply that the role is a formal valuation position.",
            "",
            "For the Phillips role, the analysis identifies material senior-specialist gaps: direct auction valuation, GIA/FGA (if not held), French fluency, European collector network, and a record of European consignment sourcing. The responsible strategy is an honest expression of interest that signals value in Asian market intelligence and data-led research while requesting consideration for adjacent roles such as Cataloguing, Jewellery Operations, Client Development, or Junior Specialist pathways.",
            "",
            "## Reproducibility",
            "",
            "Run `python3 src/analyse_roles.py` from the project root. The script reads `data/auction_house_roles.csv` and recreates this report.",
            "",
            "## Sources",
            "",
            "1. https://job-boards.greenhouse.io/sothebys/jobs/6092229004",
            "2. https://www.phillips.com/careers/326/zh",
        ]
    )

    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT_FILE}")


if __name__ == "__main__":
    main()
