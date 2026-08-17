# APAC Jewellery Market Prioritisation

## A reproducible macro-demand framework for product-planning research

This portfolio demonstrates a disciplined approach to **regional market prioritisation** for a jewellery business. It converts public, consistently dated macroeconomic and digital-access indicators into a transparent research framework for deciding **where to prioritise further market validation and digital-localisation work**.

> **Scope and discipline.** This is not a jewellery sales forecast, market-size estimate, investment recommendation, or a claim that any market should be entered. It does not measure category demand, price elasticity, consumer willingness to pay, margin, regulations, competitor intensity or store economics. It is an evidence-led first screen designed to structure the next research question.

## Business question

> Across selected APAC markets, which markets should be prioritised for the next stage of jewellery market research and digital-localisation validation, when assessed through a transparent set of 2024 macro-demand proxies?

The selected markets are Hong Kong SAR, China; Singapore; Thailand; Malaysia; Vietnam; and Indonesia. Mainland China is strategically important but is not included in the comparable panel: a robust China analysis would require a separate city-tier and domestic-consumption dataset rather than being folded into a cross-country proxy model.

## Why this shows product-planning capability

A senior product-planning decision is rarely based on a single metric. The framework demonstrates five practical capabilities:

| Capability | Evidence in this project |
|---|---|
| Problem formulation | Defines a limited, decision-relevant question rather than presenting a generic dashboard. |
| Data governance | Uses one source family, retains download metadata and restricts the baseline to consistently dated 2024 values. |
| Metric design | Distinguishes purchasing-power context, digital readiness, urban retail context and economic scale. |
| Analytical rigour | Applies reproducible transformations, min–max normalisation, log scaling and sensitivity scenarios. |
| Decision communication | Separates a research-priority signal from a commercial decision, and clearly identifies validation steps. |

## Data and transformations

All baseline inputs are publicly available **2024** World Development Indicators, downloaded through the World Bank API. The raw CSV includes the exact API URL used for every observation.

| Signal | Indicator | Transformation | Interpretation discipline |
|---|---|---|---|
| Purchasing-power context | GDP per capita, current US$ (`NY.GDP.PCAP.CD`) | Min–max normalisation | Context for broad spending capacity; **not** a luxury-jewellery demand measure. |
| Digital readiness | Individuals using the internet, % of population (`IT.NET.USER.ZS`) | Min–max normalisation | Context for digital reach; **not** an e-commerce conversion measure. |
| Urban retail context | Urban population, % of total (`SP.URB.TOTL.IN.ZS`) | Min–max normalisation | Context for concentrated retail access; **not** a store-network feasibility measure. |
| Economic scale | GDP, current US$ (`NY.GDP.MKTP.CD`) | `log(1 + GDP)`, then min–max normalisation | Context for market scale; **not** category expenditure or profit potential. |

The balanced baseline assigns equal 25% weights to the four signals. Two sensitivity cases are also calculated: **digital-first** and **scale-led**. Any market whose rank changes between scenarios is flagged as **scenario-sensitive**, signalling that qualitative validation is needed before allocating resources.

## Output

![APAC macro-demand priority signals](market_entry_signals.png)

The output is deliberately a **prioritisation hypothesis**, not a verdict. It allows a product manager to move from broad regional intuition to a clear next-stage workplan:

| Stage | Recommended validation activity |
|---|---|
| 1. Category demand | Obtain jewellery-category spend, price-band, purchase-frequency and competitor data. |
| 2. Customer proposition | Test localised assortment, gifting occasions, design preferences and material/collection preferences. |
| 3. Channel economics | Validate e-commerce conversion, store productivity, fulfilment constraints, marketing costs and margin. |
| 4. Pilot design | Define a small, measurable assortment or digital experiment with success thresholds. |

## Reproduce the analysis

```bash
python3 -m pip install -r requirements.txt
python3 fetch_world_bank_data.py
python3 analyse_market_priority.py
```

The scripts refresh the raw observations, data coverage table, market-signal panel, sensitivity scores, results summary and the visualisation.

| Path | Content |
|---|---|
| `fetch_world_bank_data.py` | Downloads 2024 public World Bank observations and retains endpoint metadata. |
| `analyse_market_priority.py` | Calculates the explicit scenarios and produces analysis outputs. |
| `world_bank_wdi_observations.csv` | Raw source observations and API URLs. |
| `market_priority_scores.csv` | Scenario scores, ranks and stability flags. |
| `data_coverage.csv` | Confirms 2024 coverage for all markets and input indicators. |
| `market_entry_signals.png` | Market-signal visualisation. |

## Sources and limitations

The World Bank identifies GDP per capita as national-accounts data assembled from country official statistics and other sources; it should not be read as a proxy for jewellery expenditure.[1] The internet-use indicator is sourced from the International Telecommunication Union and measures use, not retail conversion.[2] All data use the World Bank’s CC BY 4.0 public licence.[1] [2]

This project explicitly avoids a direct cross-country tourism comparison because the World Bank notes that national collection methods and coverage differ, which can undermine comparability.[3]

## Author

**Yuen Tung Sze**  
Senior Manager, Product Planning | Jewellery Industry  
[LinkedIn](https://www.linkedin.com/in/yuen-tung-sze-81488275)

## References

[1] [World Bank — GDP per capita (current US$)](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD)

[2] [World Bank — Individuals using the Internet (% of population)](https://data.worldbank.org/indicator/IT.NET.USER.ZS)

[3] [World Bank DataBank — International tourism arrivals metadata and comparability limitations](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/ST.INT.ARVL)
