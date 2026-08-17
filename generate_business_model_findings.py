"""Generate a decision brief for three jewellery business-model assumptions.

The script intentionally frames outputs as research-prioritisation hypotheses. It
never treats macro proxies as direct estimates of jewellery demand or profitability.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

SCRIPT_PATH = Path(__file__).resolve()
ROOT = SCRIPT_PATH.parent.parent if SCRIPT_PATH.parent.name == "src" else SCRIPT_PATH.parent
SCORES = ROOT / "outputs" / "business_model_priority_scores.csv"
ASSUMPTIONS = ROOT / "outputs" / "business_model_assumptions.csv"
OUT = ROOT / "outputs" / "business_model_findings.md"
if not SCORES.exists():
    SCORES = ROOT / "business_model_priority_scores.csv"
    ASSUMPTIONS = ROOT / "business_model_assumptions.csv"
    OUT = ROOT / "business_model_findings.md"

MODEL_ACTIONS = {
    "international_brand": {
        "question": "Where should a higher-control international jewellery brand prioritise premium proposition and brand-experience validation?",
        "action": "Validate premium price architecture, high-touch client experience, retail-format economics and local brand storytelling.",
        "conditional_note": "A strong rank is not evidence of sufficient luxury-category demand, partner access or store economics.",
    },
    "small_independent": {
        "question": "Where can a smaller jewellery business test demand with lower fixed commitment and stronger digital reach?",
        "action": "Validate customer acquisition cost, social/content conversion, ticket-size fit, fulfilment and a narrow assortment test before physical expansion.",
        "conditional_note": "A digital-reach signal does not establish affordable acquisition cost or repeat purchase.",
    },
    "ecommerce_cross_border": {
        "question": "Where should an e-commerce or cross-border jeweller test scalable online demand and operational feasibility?",
        "action": "Validate logistics, duties/returns, payments, trust signals, conversion, local fulfilment and contribution margin by price band.",
        "conditional_note": "Scale and internet use do not prove cross-border profitability, fulfilment feasibility or customer trust.",
    },
}


def main() -> None:
    scores = pd.read_csv(SCORES)
    assumptions = pd.read_csv(ASSUMPTIONS).set_index("model")

    lines = [
        "# Business-Model Findings — APAC Jewellery Market Prioritisation",
        "",
        "> **Core conclusion:** The same regional data does not imply one universal market sequence. Singapore and Hong Kong remain the top two under all three stated business models; the material strategic divergence is in how Malaysia and Indonesia should be prioritised. Malaysia is more compelling for premium/digital validation, while Indonesia moves up only for the scale-weighted e-commerce model and therefore needs a stricter operational proof point.",
        "",
        "## Transparent assumptions",
        "",
        "The weightings below are deliberate business-model assumptions, not statistically estimated elasticities or sales forecasts. They use the same four 2024 public macro inputs in every model so the rank differences are traceable to strategic priorities.",
        "",
        "| Business model | Purchasing power | Digital readiness | Urban retail context | Economic scale | Strategic assumption |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for model, row in assumptions.iterrows():
        lines.append(
            f"| **{row['label']}** | {row['purchasing_power']:.0%} | {row['digital_readiness']:.0%} | {row['urban_retail_context']:.0%} | {row['economic_scale']:.0%} | {row['strategy_assumption']} |"
        )

    lines.extend(
        [
            "",
            "## Findings by business model",
            "",
        ]
    )
    for model, configuration in MODEL_ACTIONS.items():
        label = assumptions.loc[model, "label"]
        ranked = scores.sort_values(f"rank_{model}")
        top_three = ranked.head(3)["country"].tolist()
        lines.extend(
            [
                f"### {label}",
                "",
                f"> **Decision question:** {configuration['question']}",
                "",
                "| Priority | Market | Rank | Strategic interpretation | Next validation action |",
                "|---|---|---:|---|---|",
            ]
        )
        for _, row in ranked.iterrows():
            rank = int(row[f"rank_{model}"])
            priority = "Primary research priority" if rank <= 2 else "Conditional / later-wave research"
            interpretation = (
                "Lead research candidate under this model's stated assumptions."
                if rank <= 2
                else "Requires model-specific validation; the rank is not a go/no-go decision."
            )
            lines.append(
                f"| {priority} | {row['country']} | #{rank} | {interpretation} | {configuration['action']} |"
            )
        lines.extend(["", f"**Interpretation guardrail:** {configuration['conditional_note']}", ""])

    lines.extend(
        [
            "## Cross-model decision rule",
            "",
            "1. Treat **Singapore** as the cross-model reference market: it ranks #1 for international brand, small/independent and e-commerce/cross-border assumptions. This supports sequencing research there first, not an automatic market launch.",
            "2. Treat **Hong Kong** as the cross-model premium and digital validation market: it ranks #2 in all three models, but its modest economic-scale signal means category economics still require direct validation.",
            "3. Treat **Malaysia** as a proposition-validation market: it ranks #3 for international-brand and small/independent models but #4 for e-commerce/cross-border, so digital reach should be tested against monetisation and scale constraints.",
            "4. Treat **Indonesia** as a scale-led exception: it is #3 for e-commerce/cross-border but #4 for international brand and #6 for small/independent. Its strategy should begin with affordability, logistics, payments and contribution-margin evidence—not a generic regional launch plan.",
            "",
            "## What is still needed before a market decision",
            "",
            "This framework is a first-screen allocation tool. A decision to enter, invest, open stores, appoint distributors or launch an e-commerce market requires category-specific jewellery spend, price-band demand, customer segments, competitor assortment, customer acquisition cost, conversion, returns, duties, service levels, cost-to-serve and expected margin.",
        ]
    )
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
