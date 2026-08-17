# Executive Findings — APAC Jewellery Market Prioritisation

> **Decision statement:** Allocate the next market-research cycle in three waves: establish a reference pilot in Singapore; validate premium/digital propositions in Hong Kong and Malaysia; and test Indonesia only through a scale-led, affordability-and-channel hypothesis. Thailand and Vietnam remain targeted discovery or watchlist markets under this macro framework.

## What the model finds

Singapore ranks **first in the balanced, digital-first and scale-led scenarios**, making it the framework’s only stable lead market. Hong Kong and Malaysia perform more strongly when digital readiness and purchasing-power context are emphasised than when economic scale dominates, so they should be treated as proposition-validation markets rather than automatic scale plays. Indonesia moves from **sixth in the digital-first scenario to second in the scale-led scenario**; that dispersion makes it an important but conditional scale hypothesis, not an immediate conclusion. Thailand has no stable cross-scenario advantage, while Vietnam remains lower-ranked under all three stated scenarios.

## Research sequencing and actions

| Market | Research wave | Evidence-based finding | Next validation action |
|---|---|---|---|
| Singapore | **Wave 1 — Reference market** | The only consistently top-ranked market across all stated scenarios. | Prioritise detailed category research and a small measurable pilot; use the outcome to define regional operating benchmarks. |
| Hong Kong SAR, China | **Wave 2 — Premium/digital validation** | Performs relatively better when purchasing-power and digital-readiness signals are weighted more heavily than economic scale. | Validate price architecture, online conversion, local content and assortment relevance before committing broader resources. |
| Malaysia | **Wave 2 — Premium/digital validation** | Performs relatively better when purchasing-power and digital-readiness signals are weighted more heavily than economic scale. | Validate price architecture, online conversion, local content and assortment relevance before committing broader resources. |
| Thailand | **Targeted opportunity scan** | Middle-ranked under the balanced baseline without a stable cross-scenario advantage. | Use a focused local research sprint to identify occasions, categories or channels that could justify a more specific pilot. |
| Indonesia | **Wave 3 — Scale-led hypothesis** | Performs strongly when economic scale is emphasised but materially weaker in a digital-first scenario. | Validate target-customer segmentation, affordability, channel economics and fulfilment before treating scale as an opportunity. |
| Vietnam | **Watchlist / evidence-gathering** | Ranks in the lower tier across the current macro-demand framework. | Monitor market and category evidence; prioritise lightweight discovery rather than resource-intensive pilots. |

## Managerial implication

The analysis is useful because it converts a broad regional ambition into a staged research allocation. It **does not** advise entering, investing in, or ranking the profitability of any market. Before a pilot decision, the next evidence set must include jewellery-category demand, ticket-size and price-band data, local customer segmentation, channel conversion, competitor assortment, regulatory constraints, cost-to-serve and expected margin.

## Rule transparency

The waves are generated with explicit rules in `generate_executive_findings.py`. A stable leader is ranked first with no rank change across scenarios. Premium/digital validation markets rank within the top three in the digital-first scenario but decline when economic scale is prioritised. Scale-led hypotheses rank within the top three when economic scale is prioritised but rank fifth or lower in the digital-first scenario. These rules ensure that the narrative can be independently checked against `market_priority_scores.csv`.
