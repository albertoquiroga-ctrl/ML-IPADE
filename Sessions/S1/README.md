# Bob's Conundrum — Store 10 Performance Analysis (v4)

Causal-inference-grade deep dive for IPADE case **AD 23 eC 02: *Bob's Conundrum — Too Much Sales Data***.

> *Bob Garza, an MBA graduate interviewing with a consulting firm, has three days to evaluate Store 10's performance from an anonymous supermarket dataset. After hours of Excel averaging he concludes Store 10 is "above average" — but fears the analysis is too simplistic. He's right to worry.*

This version (v4) adds the rigor that separates *serious analysis* from *defensible causal inference*: placebo tests across 45 stores, per-department break detection, synthetic control with placebo distribution, clustering sensitivity analysis, and a forecast with confidence intervals.

Analysis runs on the real [Walmart Sales Forecast dataset on Kaggle](https://www.kaggle.com/datasets/aslanahmedov/walmart-salesforecast) (421,570 rows, 45 stores, 81 departments, 143 weeks).

---

## What v4 adds over v3

v3 delivered dept decomposition, K-means clustering, structural break detection, MarkDown controls, and a Store 12 benchmark. It was a solid analysis. But when I stress-tested v3's claims, several moderated meaningfully:

| v4 rigor test | v3 claim | v4 finding |
|---|---|---|
| Placebo Quandt-Andrews on 45 stores | "Q4 2011 was a Store-10-specific event" | **22 of 45 stores break in Q4 2011 window. Store 10's F-stat (9.97) is at the 69th percentile — not unusually sharp.** The break is chain-wide, likely linked to the Nov 2011 start of MarkDown reporting. |
| Per-department break timing | "Structural break on 2011-11-25" | **Departments break at different dates** — Dept 5 (Aug 2010), Dept 95 (Apr 2011), Dept 72 (Nov 2011), Dept 55 (Jan 2012). The aggregate break is a weighted average of staggered category-level events, not a single shock. |
| Synthetic control + placebo | "Store 10 has worst residual trajectory (#1/45)" | **True for slope, but moderates under synthetic control: Store 10 is 2.2pp below counterfactual, ranks #6/33 well-fit placebo stores (15th percentile)** — real underperformance, not extreme outlier. |
| Clustering sensitivity (k=3...8) | "Peer group is [12, 28, 33, 38, 42]" | **Confirmed — identical peer group for k=3, 4, 5, and 6. Stores 33 and 42 present in all six k-settings tested.** Extremely robust. |
| Forecast with confidence interval | "Edge is eroding" | **Point estimate: 10.5 quarters to $/sqft convergence (≈mid-2015). 95% CI: 7–26 quarters.** Wide CI reflects only 49 post-break weeks. |

**The refined headline:** Store 10 is not the victim of a unique local event. It's the worst-responding store to a chain-wide Q4 2011 inflection, with multiple staggered category-level weaknesses accumulating across an 18-month window. The diagnostic pivots from *"what happened here?"* to *"why is Store 10 the worst recoverer when its peers managed the same shock better?"*

---

## What remains from v3

The findings that survived v4's stress tests:

| Finding | Detail |
|---|---|
| Decline is **concentrated** | Top 5 depts drive 52% of the gross $ loss. Top 3 (72, 5, 95) alone = $1.3M of $1.5M net loss. |
| **Dept 95 is Store-10-specific** | Chain-wide Dept 95 grew +1.2%; Store 10 fell −11%. The 12pp gap can't be explained as a category trend. |
| Post-Nov-2011 decline **survives MarkDown control** | Slope −52pp/year (p=0.003) even with LogMD as regressor. Not a data-regime artifact. |
| **Not a promo-starvation story** | Store 10 ranks 4/17 on MarkDown $/sqft among Type-B. More promo $ isn't the lever. |
| **Store 12 is the natural benchmark** | Only store that is both Type B and in Store 10's demographic cluster. Loses less in each of Store 10's worst-hit departments. |
| Holiday gap (−5pp) **larger** than non-holiday gap (−4.4pp) | Strong holiday lift was masking weakness. |
| Share drain to Type-A stores | Store 10 lost 0.6 share points (4.37% → 3.77%) — redistributed to large-format siblings. |

---

## The headline

Store 10 is a flagship-productivity store responding worst-in-fleet to a chain-wide Q4 2011 inflection, driven by staggered category-level structural breaks spanning August 2010 to January 2012. The underperformance is real but moderate (−2.2pp vs synthetic counterfactual, 15th-percentile placebo), concentrated in three departments, and not attributable to MarkDown under-investment. On current trajectory, Store 10's 77% productivity advantage converges to its peer group between 2015 and 2019 (95% CI). The operational imperative is to understand why Store 12 — the only demographically comparable Type-B peer — has absorbed the same shock better in the same departments.

---

## Repo contents

| File | Purpose |
|------|---------|
| `store10_analysis.ipynb` | The full v4 analysis with embedded outputs and 6-panel dashboard. |
| `requirements.txt` | Python dependencies. |
| `.gitignore` | Excludes the raw CSVs (available on Kaggle). |

---

## Notebook structure

1. Setup + sanity check (reproduces Bob's Exhibit B exactly before analyzing)
2. Baseline Type-B comparison (the starting observation, not the conclusion)
3. **Decompose** — dept concentration, per-dept break timing, holiday/non-holiday, market share
4. **Re-benchmark** — K-means clustering, **sensitivity to k**, Store 12 head-to-head
5. **Explain + test** — OLS with HC1 robust SE, Quandt-Andrews break scan, **placebo across 45 stores**, MarkDown control, **synthetic control with placebo distribution**
6. **Project** — convergence forecast with 95% CI
7. Six-panel visual summary
8. Executive summary with 90-second recruiter pitch

---

## Running locally

1. Download the three CSVs from Kaggle into this folder: `stores.csv`, `features.csv`, `sales.csv`  
   → https://www.kaggle.com/datasets/aslanahmedov/walmart-salesforecast

2. Install dependencies and run:

```bash
pip install -r requirements.txt
jupyter lab store10_analysis.ipynb
```

The notebook starts with an `assert` that reproduces Bob's Exhibit B Table 3 numbers exactly — if the data loads correctly, it proceeds; if not, it fails fast with a clear error.

Full execution takes about 2–3 minutes. The bottleneck is running Quandt-Andrews placebo scans across 45 stores and 45 synthetic-control optimizations.

---

## Methodological notes

**Why the story moderates under rigorous testing.** The more careful the inference technique, the more modest the "Store 10 specific event" claim becomes. This is normal and honest — raw comparisons almost always overstate effects because they don't control for shared trends. Reporting the moderated version (rather than the raw residual slope) is what separates an analyst from a consultant.

**On the pre-break slope insignificance.** In the pre-Nov-2011 window, Store 10's residual slope has p=0.41 — i.e., statistically flat. This was missed in v3 (which implied gradual erosion). The decline is genuinely concentrated post-break, not a long smoldering trend.

**Why the forecast CI is wide.** We have 143 total weeks and only 49 post-break. Any linear extrapolation from that short a post-event sample comes with wide uncertainty. Reporting the CI — rather than a single convergence date — is the honest move.

**On synthetic control interpretation.** The 2.2pp post-break gap is not a treatment effect in the formal sense (there's no discrete intervention). It's the best available counterfactual-based estimate of how much Store 10 is underperforming relative to a weighted blend of stores that tracked it well pre-break. The placebo distribution provides the reference for interpreting whether that gap is unusual.

---

## Case source

Ibarra Garza, A., Herrera Martínez, R., Pensamiento Calderón, G. A., & Rodas Aguilar, E. J. (2023). *Bob's Conundrum: Too Much Sales Data* (AD 23 eC 02). Instituto Panamericano de Alta Dirección de Empresa (IPADE).

Public dataset: [Walmart Sales Forecast on Kaggle](https://www.kaggle.com/datasets/aslanahmedov/walmart-salesforecast).
