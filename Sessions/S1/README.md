# Bob's Conundrum — Store 10 Performance Analysis

Companion analysis for IPADE case **AD 23 eC 02: *Bob's Conundrum — Too Much Sales Data***.

> *Bob Garza, an MBA graduate interviewing with a consulting firm, has three days to evaluate Store 10's weekly sales performance from an anonymous supermarket dataset. After hours of Excel averaging he concludes Store 10 is "above average" — but fears the analysis is too simplistic. He's right to worry.*

This repo demonstrates the **5-layer consulting analysis** Bob *should* have delivered, answering the real question: *is Store 10 a good performer, compared to what, on which metric, over what horizon?*

---

## The reframe

Bob's mistake wasn't tools — it was skipping the question. "Is Store 10 good?" is unanswerable without defining (a) peer group, (b) metric, (c) horizon. His own Table 3 already contained the teaching twist:

| | 2010 | 2011 | 2012 | Growth |
|---|---:|---:|---:|---:|
| Store 10 avg weekly sales | 26,984 | 26,399 | 25,507 | **−5.5%** |
| All-stores avg weekly sales | 16,270 | 15,954 | 15,695 | −3.5% |

Store 10 is *above the system in levels* but *declining faster than the system*. The level-1 read ("good store") flips when you look at trajectory.

---

## The 5-layer framework

| Layer | Question | Technique |
|-------|----------|-----------|
| 1. Define | Peer group? Metric? Horizon? | Framework only |
| 2. Describe | Normalize & trend | Sales/sqft, YoY growth, seasonality, volatility |
| 3. Benchmark | Percentile rank | Compare Store 10 across 3 peer groups |
| 4. Explain | Does context explain the level? | OLS regression + residual analysis |
| 5. Recommend | Headline + evidence | Executive summary |

---

## Repo contents

| File | Purpose |
|------|---------|
| `generate_synthetic_data.ipynb` | Generates Walmart-style CSVs (`stores.csv`, `features.csv`, `sales.csv`) calibrated to match the case's Exhibit B numbers. Use this if you don't have Kaggle access. |
| `store10_analysis.ipynb` | The full 5-layer analysis. Runs unchanged against synthetic or real Kaggle data. |
| `requirements.txt` | Python dependencies. |

Both notebooks are committed with executed outputs, so you can browse the analysis and dashboard directly on GitHub without running anything.

---

## Running locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2a. Generate calibrated synthetic data (fastest path)
jupyter nbconvert --to notebook --execute generate_synthetic_data.ipynb

# 2b. OR drop real Kaggle CSVs into this folder:
#     https://www.kaggle.com/datasets/aslanahmedov/walmart-salesforecast
#     Files needed: stores.csv, features.csv, sales.csv

# 3. Run the analysis
jupyter nbconvert --to notebook --execute store10_analysis.ipynb
```

Or just open either notebook in Jupyter / VS Code and run cells interactively.

---

## Key findings

**Headline:** Store 10 is the best Type-B store in the fleet on level and productivity but is *structurally deteriorating* — one of the worst stores on growth momentum.

- 100th percentile among Type-B peers on absolute weekly sales and sales/sqft
- ~6th percentile among Type-B peers on 2010→2012 growth
- OLS residual (context-adjusted outperformance) erodes from +26.8% in 2010 to +22.6% in 2012

This is a *store to defend, not to celebrate* — the opposite conclusion to Bob's initial read.

---

## The meta-lesson

The case is a trap about *judgment*, not *tooling*. The teaching point is that asking the right analytical question ("compared to what, on which metric, over what horizon?") matters more than the tool used to answer it. Python, Excel, or R — any of them can produce the correct analysis once the question is framed properly.

---

## Case source

Ibarra Garza, A., Herrera Martínez, R., Pensamiento Calderón, G. A., & Rodas Aguilar, E. J. (2023). *Bob's Conundrum: Too Much Sales Data* (AD 23 eC 02). Instituto Panamericano de Alta Dirección de Empresa (IPADE).

Public dataset: [Walmart Sales Forecast on Kaggle](https://www.kaggle.com/datasets/aslanahmedov/walmart-salesforecast).
