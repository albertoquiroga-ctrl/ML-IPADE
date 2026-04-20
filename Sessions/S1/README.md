# Bob's Conundrum — Store 10 Performance Analysis

Companion analysis for IPADE case **AD 23 eC 02: *Bob's Conundrum — Too Much Sales Data***.

> *Bob Garza, an MBA graduate interviewing with a consulting firm, has three days to evaluate Store 10's weekly sales performance from an anonymous supermarket dataset. After hours of Excel averaging he concludes Store 10 is "above average" — but fears the analysis is too simplistic. He's right to worry.*

This repo demonstrates the **5-layer consulting analysis** Bob *should* have delivered, answering the real question: *is Store 10 a good performer, compared to what, on which metric, over what horizon?*

The analysis runs against the real [Walmart Sales Forecast dataset on Kaggle](https://www.kaggle.com/datasets/aslanahmedov/walmart-salesforecast) (421,570 rows).

---

## The reframe

Bob's mistake wasn't tools — it was skipping the question. "Is Store 10 good?" is unanswerable without defining (a) peer group, (b) metric, (c) horizon. His own Table 3 already contained the teaching twist:

| | 2010 | 2011 | 2012 | Growth |
|---|---:|---:|---:|---:|
| Store 10 avg weekly sales (per row) | 26,984 | 26,399 | 25,507 | **−5.5%** |
| All-stores avg weekly sales (per row) | 16,270 | 15,954 | 15,695 | −3.5% |

Store 10 is *above the system in levels* but *declining faster than the system*. The level-1 read ("good store") flips entirely when you aggregate to the store level and measure growth on comparable periods.

---

## The 5-layer framework

| Layer | Question | Technique |
|-------|----------|-----------|
| 1. Define | Peer group? Metric? Horizon? | Framework only |
| 2. Describe | Normalize & trend | Sales/sqft, growth (comparable periods), seasonality, volatility, holiday lift |
| 3. Benchmark | Percentile rank | Compare Store 10 across 3 peer groups |
| 4. Explain | Does context explain the level? | OLS regression + residual analysis over time |
| 5. Recommend | Headline + evidence | Executive summary |

---

## Key findings (real data)

**Headline:** Store 10 is a category-leading Type-B store on level and productivity, executes holidays better than its peers — but it is the *only* Type-B store actually declining while its peer group grows. Its context-adjusted edge is eroding by ~8–9 pp/year.

| Dimension | Store 10 | Type-B peers | Read |
|---|---:|---:|---|
| Avg weekly sales rank (Type-B) | **100th pct** | — | Best Type-B store |
| Sales/sqft rank (Type-B) | **100th pct** | — | Best Type-B productivity |
| Feb–Oct 2010→2012 growth | **−2.14%** | **+2.32%** (median) | Only store declining |
| Growth rank (Type-B) | **~29th pct** | — | Bottom third |
| Holiday lift | **+12.2%** | +10.9% (mean) | Executes events well |
| OLS residual 2010 | **+114%** | 0 (by construction) | Far above model |
| OLS residual 2012 | **+97%** | 0 | Edge eroding ~8 pp/yr |

**Reframed conclusion:** Store 10 is the single most important store to *diagnose and defend*, not to celebrate. If the current slope holds, it converges with its peer group within 5–10 years.

---

## Repo contents

| File | Purpose |
|------|---------|
| `store10_analysis.ipynb` | The full 5-layer analysis. Pre-executed with outputs and dashboard embedded. |
| `requirements.txt` | Python dependencies. |
| `.gitignore` | Excludes the raw CSVs (large files) and generated outputs. |

---

## Running locally

1. Download the three CSVs from Kaggle into this folder: `stores.csv`, `features.csv`, `sales.csv`  
   → https://www.kaggle.com/datasets/aslanahmedov/walmart-salesforecast

2. Install dependencies and run:

```bash
pip install -r requirements.txt
jupyter lab store10_analysis.ipynb
```

Or execute headless:

```bash
jupyter nbconvert --to notebook --execute store10_analysis.ipynb
```

The notebook validates its load by reproducing Bob's Exhibit B numbers exactly before running any analysis — so if the CSVs aren't loaded correctly, you'll see the mismatch right away.

---

## The meta-lesson

The case is a trap about **judgment**, not tooling. The teaching point is that asking the right analytical question ("compared to what, on which metric, over what horizon?") matters more than the tool used to answer it. Python, Excel, or R — any of them can produce the correct analysis once the question is framed properly.

---

## Case source

Ibarra Garza, A., Herrera Martínez, R., Pensamiento Calderón, G. A., & Rodas Aguilar, E. J. (2023). *Bob's Conundrum: Too Much Sales Data* (AD 23 eC 02). Instituto Panamericano de Alta Dirección de Empresa (IPADE).

Public dataset: [Walmart Sales Forecast on Kaggle](https://www.kaggle.com/datasets/aslanahmedov/walmart-salesforecast).
