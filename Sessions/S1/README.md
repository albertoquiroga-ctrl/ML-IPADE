# Bob's Conundrum — Store 10 Performance Analysis

Deep-dive analysis for IPADE case **AD 23 eC 02: *Bob's Conundrum — Too Much Sales Data***.

> *Bob Garza, an MBA graduate interviewing with a consulting firm, has three days to evaluate Store 10's performance from an anonymous supermarket dataset. After hours of Excel averaging he concludes Store 10 is "above average" — but fears the analysis is too simplistic. He's right to worry.*

This repo answers the question *properly* — not just "is Store 10 good?" but "**where** is the decline, **when** did it start, **against whom** should Store 10 be measured, and **what's signal vs noise?**"

Analysis runs on the real [Walmart Sales Forecast dataset on Kaggle](https://www.kaggle.com/datasets/aslanahmedov/walmart-salesforecast) (421,570 rows, 45 stores, 81 departments, 143 weeks).

---

## Key findings

| Finding | Detail |
|---|---|
| Decline is **concentrated**, not broad | 5 departments drive 52% of the $1.5M net loss. Depts 72 (−$607K), 5 (−$366K), 95 (−$338K) lead. |
| Dept 95 is **store-specific** | Chain-wide Dept 95 grew +1.2%; Store 10 fell −11%. A 12pp gap that can't be explained away as a category trend. |
| **Step-change, not gradual slide** | Quandt-Andrews break detected at 2011-11-25 (Black Friday, F=9.97). Pre-break slope not statistically significant (p=0.41). Post-break: −52pp/year (p=0.003). |
| **Not a promo-starvation story** | Store 10 ranks 4/17 in MarkDown $/sqft among Type-B stores. More promo spend isn't the lever. |
| **Type-B was the wrong peer group** | K-means clustering on size + regional vars puts Store 10 with [12, 28, 33, 38, 42] — only Store 12 overlaps with the naive Type-B comparison. |
| **Store 12 is the true benchmark** | Same type, same demographic cluster. Grew +4.93% vs Store 10's −2.14%. Outperforms Store 10 in all 3 worst-hit departments. |
| **Holiday gap is *larger* than non-holiday gap** | Strong holiday lift was masking weakness, not revealing strength. |
| **Share drain to Type-A stores** | Store 10 lost 0.6 share points (4.37% → 3.77%) — redistributed predominantly to large-format stores. |

## The headline

Store 10 is not gradually declining. It experienced a sharp Q4 2011 inflection that survives controls for promotional spending, concentrated in three specific departments, against a demographic peer group that has navigated the period better. The naive Type-B comparison understated the problem by 2.5pp of growth; the right diagnostic action is to benchmark Store 10 against Store 12 in Depts 72, 5, and 95.

---

## What this analysis does that the first take didn't

| | First take | This version |
|---|---|---|
| Department-level decomposition | Skipped ("next steps") | Waterfall of 5 worst, isolate store-specific vs category |
| Statistical rigor on residual erosion | Asserted "~8-9pp/year" | Tested — full sample p=0.08 (fails 5%), break detection finds real inflection |
| Peer group construction | Assumed Type-B is correct | K-means clustering, matched-pair with Store 12 |
| MarkDown (promo) analysis | Noted but not used | Regressed as control variable + peer ranking |
| Structural break detection | Absent | Quandt-Andrews scan identifies Nov 25, 2011 endogenously |
| Market share | Absent | Quarterly trajectory + identification of share gainers |
| Recommendation specificity | "Defend, don't celebrate" | "Send a team to Store 12; focus on Depts 72, 5, 95" |

---

## Repo contents

| File | Purpose |
|------|---------|
| `store10_analysis.ipynb` | The full analysis with embedded outputs and dashboard. |
| `requirements.txt` | Python dependencies. |
| `.gitignore` | Excludes the raw CSVs (available on Kaggle). |

---

## Running locally

1. Download the three CSVs from Kaggle into this folder: `stores.csv`, `features.csv`, `sales.csv`  
   → https://www.kaggle.com/datasets/aslanahmedov/walmart-salesforecast

2. Install dependencies and run:

```bash
pip install -r requirements.txt
jupyter lab store10_analysis.ipynb
```

The notebook has an `assert` statement at the start that reproduces Bob's Exhibit B numbers exactly — if the data loads correctly, it proceeds; if not, it fails fast with a clear error.

---

## The meta-lesson

The case is a trap about **judgment**, not tooling. The teaching point is *what questions to ask before writing any code*:

- Against whom? (peer group matters — a lot)
- On what metric? (level vs growth vs share vs residual)
- Over what horizon? (levels vs trends vs structural breaks)
- How much is signal and how much is noise? (test, don't assert)
- Where is the effect concentrated? (aggregate numbers hide everything)

Bob's own Table 3 already contained the teaching twist. Python, Excel, or a notebook — any tool can produce the correct analysis once the question is framed properly. The recruiter is grading the question, not the regression.

---

## Case source

Ibarra Garza, A., Herrera Martínez, R., Pensamiento Calderón, G. A., & Rodas Aguilar, E. J. (2023). *Bob's Conundrum: Too Much Sales Data* (AD 23 eC 02). Instituto Panamericano de Alta Dirección de Empresa (IPADE).

Public dataset: [Walmart Sales Forecast on Kaggle](https://www.kaggle.com/datasets/aslanahmedov/walmart-salesforecast).
