# Jewellery & Auction Role Intelligence

A reproducible Python portfolio project that transforms **official auction-house job descriptions** into a structured role-requirements dataset and a transparent candidate-fit analysis. It is designed to demonstrate how data thinking can support career research in the jewellery and auction sector.

> **Scope.** This project is a career-research and requirements-analysis prototype. It does **not** estimate jewellery values, predict auction prices, or use private client or transaction data.

## Why this project

Auction houses increasingly combine connoisseurship, client service, operations, compliance, and commercial judgement. This project demonstrates a practical way to convert unstructured job descriptions into an auditable decision-support workflow: source evidence is retained, requirements are categorised, and the scoring rules are explicit rather than opaque.

The initial analysis examines two official vacancies published by Sotheby’s and Phillips. The first is a Hong Kong private-sales operations role that requires process control, client service, compliance and multilingual communication. The second is a Geneva jewellery-specialist role that requires deep valuation expertise, sourcing capability, an established network and formal gemmological qualifications.[1][2]

## Project structure

| Path | Purpose |
|---|---|
| `data/auction_house_roles.csv` | Manually structured facts and requirement summaries from official public role pages. |
| `src/analyse_roles.py` | Reproducible Python script that categorises requirements and produces a role-fit report. |
| `reports/role_fit_report.md` | Generated report comparing observable evidence against stated criteria. |
| `requirements.txt` | Minimal runtime dependency list. |

## Method

The script assigns a tag to each stated requirement: `operations`, `client_service`, `compliance`, `data`, `jewellery_market`, `valuation`, `qualification`, `network`, `languages`, or `leadership`. It then compares the tags with a candidate-evidence profile that contains only information deliberately supplied for the exercise. Each match is labelled as one of three statuses:

| Status | Meaning |
|---|---|
| **Direct evidence** | The candidate profile contains evidence that clearly maps to the requirement. |
| **Transferable evidence** | The profile offers a relevant adjacent skill, but not the exact stated experience or qualification. |
| **Development gap** | The requirement is not evidenced and must not be claimed in an application. |

This makes the analysis suitable as a portfolio example: the reasoning is visible, the limitations are stated, and no fabricated credentials are introduced.

## Quick start

```bash
python3 -m pip install -r requirements.txt
python3 src/analyse_roles.py
```

The command creates or refreshes `reports/role_fit_report.md`.

## Candidate evidence used in the example

The example profile represents an experienced jewellery product-management professional with approximately ten years of experience across product development, production-process optimisation, Southeast Asian market analysis, Mainland China market familiarity, and Python/SQL data analysis. It does **not** assume GIA/FGA certification, French proficiency, an established European collector network, or direct auction-house valuation experience.

## Responsible use

The output is a structured preparation aid—not an automated hiring decision. A job applicant should verify every vacancy directly on the issuer’s official careers site before applying, adapt their CV to the role, and never represent transferable skills as regulated qualifications or specialist experience.

## Sources

[1] [Sotheby’s — Seller Operations Coordinator, Private Sales, Hong Kong](https://job-boards.greenhouse.io/sothebys/jobs/6092229004)

[2] [Phillips — Specialist, Jewellery, Geneva](https://www.phillips.com/careers/326/zh)

## Author

Yuen Tung Sze  
[LinkedIn](https://www.linkedin.com/in/yuen-tung-sze-81488275)

---

*This portfolio was created as a transparent skills demonstration using public job-posting data current as of 17 August 2026.*
