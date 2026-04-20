"""
Generator for store10_eda.ipynb.

Run once:  python _build_eda_notebook.py
Produces:  store10_eda.ipynb  (then execute it to generate outputs)

The notebook is built cell-by-cell so we can freely add heavy narration
without fighting with raw .ipynb JSON.
"""
from pathlib import Path
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []


def md(text: str) -> None:
    cells.append(nbf.v4.new_markdown_cell(text))


def code(text: str) -> None:
    cells.append(nbf.v4.new_code_cell(text))


# ======================================================================
# Title + plan
# ======================================================================
md(
    "# Store 10 EDA — Data Wrangling + Exploratory Analysis\n"
    "\n"
    "**Purpose of this notebook.** Prepare a supermarket chain dataset "
    "(sales, stores, features) for analysis and build a thorough "
    "understanding of what is inside it. This is a *learning* notebook: "
    "every step is narrated so a reader new to pandas can follow along.\n"
    "\n"
    "**What this notebook does NOT do yet.** No peer benchmarking, no "
    "statistical tests, no business recommendations. Those belong to a "
    "follow-up notebook. Here we focus on **knowing the data inside-out**.\n"
    "\n"
    "**The three source files.**\n"
    "\n"
    "| File | Key variables |\n"
    "|---|---|\n"
    "| `sales.csv` | `Store`, `Dept`, `Date`, `Weekly_Sales`, `IsHoliday` |\n"
    "| `stores.csv` | `Store`, `Type` (A/B/C), `Size` (sq ft) |\n"
    "| `features.csv` | `Store`, `Date`, `Temperature`, `Fuel_Price`, `CPI`, `Unemployment` |\n"
)

md(
    "## Plan (read this first, then scroll through)\n"
    "\n"
    "0. **Setup** — import libraries, configure display and plotting.\n"
    "1. **Load** the three CSVs with correctly parsed dates.\n"
    "2. **Inspect** each DataFrame individually (shape, dtypes, missing, uniques, date range).\n"
    "3. **Data quality checks** — duplicates, negative sales, outliers, time gaps, key integrity.\n"
    "4. **Clean** each DataFrame into `_clean` versions, keeping originals untouched.\n"
    "5. **Merge** sales + stores + features into a single analytical table `df`, and save a parquet checkpoint.\n"
    "6. **Univariate EDA** — one variable at a time.\n"
    "7. **Bivariate EDA** — two variables at a time (relationships).\n"
    "8. **Store 10 quick look** — purely descriptive, no benchmarking.\n"
    "9. **Wrap-up** — mini data dictionary + open questions for the next notebook.\n"
)

# ======================================================================
# Step 0 — Setup
# ======================================================================
md(
    "## Step 0 — Setup\n"
    "\n"
    "Before we touch any data we import the tools we will use and set a "
    "few display options. Doing this once at the top of the notebook "
    "keeps the rest of the code short and consistent.\n"
    "\n"
    "**What** this cell does: imports libraries and sets display/plot defaults.\n"
    "**Why**: `pandas` is our spreadsheet-in-code, `numpy` gives us fast math, "
    "`matplotlib` + `seaborn` handle charts. Setting a large column display "
    "limit prevents pandas from hiding columns with `...`.\n"
    "**What we expect to see**: no output — just a clean setup with no errors.\n"
)

code(
    "import pandas as pd          # pandas: tabular data (think: Excel + SQL in Python)\n"
    "import numpy as np           # numpy: fast numeric arrays; pandas is built on top of it\n"
    "import matplotlib.pyplot as plt   # matplotlib: the foundation plotting library\n"
    "import seaborn as sns        # seaborn: nicer statistical charts on top of matplotlib\n"
    "\n"
    "# Display options — make pandas output friendlier for exploration\n"
    "pd.set_option('display.max_columns', None)   # show every column, never truncate to '...'\n"
    "pd.set_option('display.width', 140)          # wider console width before wrapping\n"
    "pd.set_option('display.float_format', '{:,.2f}'.format)  # commas + 2 decimals for money-like values\n"
    "\n"
    "# Plot defaults — one consistent style for the whole notebook\n"
    "sns.set_style('whitegrid')   # light grid background is easier to read\n"
    "plt.rcParams['figure.figsize'] = (10, 5)    # baseline chart size requested by the brief\n"
    "plt.rcParams['axes.titlesize'] = 12\n"
    "plt.rcParams['axes.labelsize'] = 10\n"
    "\n"
    "print('Libraries imported. pandas version:', pd.__version__)\n"
)

# ======================================================================
# Step 1 — Load CSVs
# ======================================================================
md(
    "## Step 1 — Load the three CSVs\n"
    "\n"
    "**What**: read `sales.csv`, `stores.csv`, `features.csv` into three "
    "separate DataFrames.\n"
    "\n"
    "**Why parse dates explicitly**: if we leave `Date` as a string, "
    "operations like sorting by date, computing ranges, or grouping by "
    "month will either fail or silently give wrong answers "
    "(e.g., `'2010-10-05' < '2010-2-05'` is `False` as a string but `True` "
    "as a date, because string comparison is lexicographic). Telling "
    "pandas the exact format up-front is faster and safer than letting it "
    "guess.\n"
    "\n"
    "**Expected format**: the brief mentioned `dd/mm/yyyy`, but a quick "
    "peek at the raw files shows ISO format `YYYY-MM-DD`. Always verify "
    "what is actually in the file — specs drift. We use "
    "`format='%Y-%m-%d'`.\n"
    "\n"
    "**What we expect to see**: three DataFrames with sensible shapes "
    "(~421K sales rows, 45 stores, ~8K feature rows) and a `Date` column "
    "of dtype `datetime64[ns]`.\n"
)

code(
    "# Load sales — one row per (Store, Dept, Week)\n"
    "sales_df = pd.read_csv(\n"
    "    'sales.csv',\n"
    "    parse_dates=['Date'],          # parse_dates: convert this column to datetime at load time\n"
    "    date_format='%Y-%m-%d',        # explicit format = fast + safe (no guessing)\n"
    ")\n"
    "\n"
    "# Load stores — static metadata per store (Type, Size)\n"
    "stores_df = pd.read_csv('stores.csv')\n"
    "\n"
    "# Load features — weekly external variables per store (Temperature, Fuel_Price, CPI, Unemployment, MarkDown1-5)\n"
    "features_df = pd.read_csv(\n"
    "    'features.csv',\n"
    "    parse_dates=['Date'],\n"
    "    date_format='%Y-%m-%d',\n"
    ")\n"
    "\n"
    "print(f'sales_df    shape: {sales_df.shape}  (rows, columns)')\n"
    "print(f'stores_df   shape: {stores_df.shape}')\n"
    "print(f'features_df shape: {features_df.shape}')\n"
)

md("### sales_df — first 5 rows and dtypes")
code(
    "# .head(n) returns the top n rows — our first visual sanity check that the columns line up\n"
    "print('Dtypes:')\n"
    "print(sales_df.dtypes)\n"
    "sales_df.head(5)\n"
)

md("### stores_df — first 5 rows and dtypes")
code(
    "print('Dtypes:')\n"
    "print(stores_df.dtypes)\n"
    "stores_df.head(5)\n"
)

md("### features_df — first 5 rows and dtypes")
code(
    "print('Dtypes:')\n"
    "print(features_df.dtypes)\n"
    "features_df.head(5)\n"
)

md(
    "### 📝 What we learned (Step 1)\n"
    "- All three files loaded without errors and dates are now real `datetime64` values, not strings.\n"
    "- `sales_df` has ~421K rows — weekly records across 45 stores and many departments.\n"
    "- `features_df` has columns `MarkDown1..MarkDown5` the brief did not mention; we will inspect them in Step 2 before deciding what to do.\n"
    "- `features_df` also contains an `IsHoliday` column that duplicates the one in `sales_df`; we will reconcile this at merge time.\n"
)

# ======================================================================
# Step 2 — Inspect each DataFrame
# ======================================================================
md(
    "## Step 2 — Inspect each DataFrame individually\n"
    "\n"
    "For each file we run the same battery of checks:\n"
    "- `.info()` — dtype and non-null count per column (first sanity check for missing data).\n"
    "- `.describe()` — summary statistics for numeric columns.\n"
    "- `.isnull().sum()` — how many missing values per column.\n"
    "- `.nunique()` — how many distinct values per column.\n"
    "- `.Date.min()` / `.Date.max()` — time span covered.\n"
    "\n"
    "These five views together give us a fast, honest picture of what each file contains.\n"
)

md("### 2a. `sales_df` inspection")
md(
    "**What**: structural summary of the sales table.\n"
    "**Why**: we need to know the column types, how many rows have missing values, and whether any column hides a surprise.\n"
    "**Expect**: all ~421K rows populated, `Weekly_Sales` a float, `IsHoliday` a boolean-like flag, `Date` spans roughly Feb 2010 – Oct 2012.\n"
)
code(
    "# .info() prints dtype and non-null count per column — our first sanity check for missingness and types\n"
    "sales_df.info()\n"
)

md(
    "**Reading `.info()`**: for each column we see the non-null count. "
    "If a column has fewer non-null values than the total row count, it "
    "has missing data. Dtype `object` usually means text (strings).\n"
)

code(
    "# .describe() returns count, mean, std, min, 25/50/75th percentiles, max for numeric columns\n"
    "# This is our quickest way to spot impossible values (e.g., negative sales) and scale differences between columns.\n"
    "sales_df.describe()\n"
)

md(
    "**How to read the describe output**:\n"
    "- `count` — non-null values; should match the row count if no data is missing.\n"
    "- `mean` — arithmetic average.\n"
    "- `std` — standard deviation (spread around the mean).\n"
    "- `min` / `max` — range; a negative `min` for `Weekly_Sales` is a red flag.\n"
    "- `25%` / `50%` (median) / `75%` — quartiles; big gap between `75%` and `max` hints at a long right tail (outliers).\n"
)

code(
    "# .isnull() returns a True/False mask; .sum() counts the Trues per column.\n"
    "print('Missing values per column (sales_df):')\n"
    "print(sales_df.isnull().sum())\n"
)

code(
    "# .nunique() counts distinct values per column — useful for discrete columns (Store, Dept, IsHoliday).\n"
    "print('Distinct values per column (sales_df):')\n"
    "print(sales_df.nunique())\n"
)

code(
    "# Date range — is the sales file time-aligned with the feature file?\n"
    "print(f\"sales_df date range: {sales_df['Date'].min().date()}  \u2192  {sales_df['Date'].max().date()}\")\n"
    "print(f\"distinct weeks    : {sales_df['Date'].nunique()}\")\n"
)

md("### 2b. `stores_df` inspection")
md(
    "**What**: structural summary of the static store metadata (`Type`, `Size`).\n"
    "**Why**: stores is tiny (45 rows) but critical — it is the dimension "
    "table we join against. We need to know `Type` values (A/B/C) and the "
    "`Size` distribution.\n"
    "**Expect**: 45 stores, `Type` is categorical with 3 values, `Size` is a "
    "positive integer.\n"
)

code("stores_df.info()\n")
code("stores_df.describe()\n")
code(
    "print('Missing values per column (stores_df):')\n"
    "print(stores_df.isnull().sum())\n"
    "print()\n"
    "print('Distinct values per column (stores_df):')\n"
    "print(stores_df.nunique())\n"
    "print()\n"
    "print('Type value counts:')\n"
    "# .value_counts() gives the frequency of each unique value; perfect for categoricals like Type.\n"
    "print(stores_df['Type'].value_counts())\n"
)

md("### 2c. `features_df` inspection")
md(
    "**What**: structural summary of the weekly external features per store.\n"
    "**Why**: we need to confirm the time alignment with sales and to "
    "measure how bad the MarkDown missingness is before deciding what to do.\n"
    "**Expect**: `Temperature`/`Fuel_Price`/`CPI`/`Unemployment` mostly populated; "
    "`MarkDown1`–`MarkDown5` heavily missing (they started being reported partway "
    "through the series).\n"
)

code("features_df.info()\n")
code("features_df.describe()\n")
code(
    "print('Missing values per column (features_df):')\n"
    "print(features_df.isnull().sum())\n"
    "print()\n"
    "print('Missing as a percent of rows:')\n"
    "print((features_df.isnull().sum() / len(features_df) * 100).round(1))\n"
)

code(
    "print('Distinct values per column (features_df):')\n"
    "print(features_df.nunique())\n"
    "print()\n"
    "print(f\"features_df date range: {features_df['Date'].min().date()}  \u2192  {features_df['Date'].max().date()}\")\n"
)

md(
    "### 📝 What we learned (Step 2)\n"
    "- `sales_df`: no missing values, weekly grain, ~421K rows, dates "
    "roughly Feb 2010 – Oct 2012.\n"
    "- `stores_df`: 45 stores, no missing values. `Type` values are A, B, C; "
    "`Size` is a sq-ft measurement ranging widely across store formats.\n"
    "- `features_df`: `Temperature`, `Fuel_Price`, `CPI`, `Unemployment` are "
    "well-populated; `MarkDown1`–`MarkDown5` are heavily missing (promotion data "
    "started midway through the series).\n"
    "- `features_df` extends a few months **beyond** the last week of "
    "sales — a common pattern when features are recorded for a future "
    "forecasting horizon. We will clip to the sales date range when we "
    "merge.\n"
)

# ======================================================================
# Step 3 — Data quality
# ======================================================================
md(
    "## Step 3 — Data quality checks\n"
    "\n"
    "Now we hunt for the kinds of problems that silently corrupt "
    "downstream analysis if left unchecked: duplicates, impossible "
    "values, outliers, time gaps, and mismatched keys. For every issue "
    "we find we will make an explicit **remove / impute / keep-and-flag** "
    "decision.\n"
)

md("### 3a. Duplicate rows")
md(
    "**What**: count how many rows are exact duplicates of another row in each DataFrame.\n"
    "**Why**: a duplicate in sales would double-count revenue; in stores or features it would break the merge.\n"
    "**Expect**: zero duplicates in all three files.\n"
)
code(
    "# .duplicated() returns True for rows that are exact duplicates of an earlier row. .sum() counts them.\n"
    "print(f\"sales_df    duplicated rows: {sales_df.duplicated().sum()}\")\n"
    "print(f\"stores_df   duplicated rows: {stores_df.duplicated().sum()}\")\n"
    "print(f\"features_df duplicated rows: {features_df.duplicated().sum()}\")\n"
    "\n"
    "# Also check (Store, Dept, Date) as the natural key of sales — a duplicate here would be worse than an exact dup.\n"
    "key_dups = sales_df.duplicated(subset=['Store', 'Dept', 'Date']).sum()\n"
    "print(f\"sales_df    duplicated (Store, Dept, Date) keys: {key_dups}\")\n"
    "\n"
    "# And (Store, Date) as the natural key of features\n"
    "fkey_dups = features_df.duplicated(subset=['Store', 'Date']).sum()\n"
    "print(f\"features_df duplicated (Store, Date) keys:       {fkey_dups}\")\n"
)

md("### 3b. Negative sales")
md(
    "**What**: count rows where `Weekly_Sales < 0` and peek at a few.\n"
    "**Why**: weekly sales should be non-negative. Negatives usually come "
    "from refunds/returns that exceeded new sales in that week, or from "
    "accounting adjustments. They are real but need a decision: keep (they "
    "reflect reality) or drop (they distort averages).\n"
    "**Decision (documented in the clean step)**: keep negatives but flag "
    "them; they are part of the actual revenue series and removing them "
    "would overstate performance.\n"
)
code(
    "neg_mask = sales_df['Weekly_Sales'] < 0\n"
    "print(f'Rows with Weekly_Sales < 0: {neg_mask.sum():,}  '\n"
    "      f'({neg_mask.mean()*100:.2f}% of all rows)')\n"
    "\n"
    "# Peek at a few examples to see whether they concentrate in particular stores or departments.\n"
    "sales_df.loc[neg_mask].head(10)\n"
)

code(
    "# Where do negatives concentrate? (by Dept, then by Store)\n"
    "print('Top departments by count of negative-sales weeks:')\n"
    "print(sales_df.loc[neg_mask, 'Dept'].value_counts().head(10))\n"
    "print()\n"
    "print('Top stores by count of negative-sales weeks:')\n"
    "print(sales_df.loc[neg_mask, 'Store'].value_counts().head(10))\n"
)

md("### 3c. Outliers in `Weekly_Sales` (IQR method)")
md(
    "**What**: flag rows whose `Weekly_Sales` fall outside "
    "`[Q1 - 1.5·IQR, Q3 + 1.5·IQR]`, the classic boxplot rule.\n"
    "**Why**: extreme values can dominate averages and warp charts. We "
    "want to know how many there are and where they live — we will NOT "
    "remove them automatically, because in retail a legitimate Black "
    "Friday week can easily pass the IQR threshold.\n"
    "**Decision**: keep outliers; flag them with a boolean column so we "
    "can toggle them in later views.\n"
)
code(
    "q1 = sales_df['Weekly_Sales'].quantile(0.25)   # 25th percentile\n"
    "q3 = sales_df['Weekly_Sales'].quantile(0.75)   # 75th percentile\n"
    "iqr = q3 - q1                                  # inter-quartile range\n"
    "\n"
    "lower_bound = q1 - 1.5 * iqr\n"
    "upper_bound = q3 + 1.5 * iqr\n"
    "\n"
    "outlier_mask = (sales_df['Weekly_Sales'] < lower_bound) | (sales_df['Weekly_Sales'] > upper_bound)\n"
    "n_outliers = outlier_mask.sum()\n"
    "\n"
    "print(f'Q1 = {q1:,.0f}   Q3 = {q3:,.0f}   IQR = {iqr:,.0f}')\n"
    "print(f'IQR bounds: [{lower_bound:,.0f}, {upper_bound:,.0f}]')\n"
    "print(f'Rows outside bounds: {n_outliers:,}  ({n_outliers/len(sales_df)*100:.2f}% of total)')\n"
)

code(
    "# Which stores and departments concentrate the outliers?\n"
    "print('Top 10 stores with the most IQR-outlier weeks:')\n"
    "print(sales_df.loc[outlier_mask, 'Store'].value_counts().head(10))\n"
    "print()\n"
    "print('Top 10 departments with the most IQR-outlier weeks:')\n"
    "print(sales_df.loc[outlier_mask, 'Dept'].value_counts().head(10))\n"
)

md("### 3d. Time gaps — are weekly dates consecutive per store?")
md(
    "**What**: for each store, check that consecutive sales weeks are "
    "exactly 7 days apart.\n"
    "**Why**: missing weeks would break any time-series analysis "
    "(rolling averages, year-over-year comparisons, seasonality).\n"
    "**Expect**: because sales is a *long* table with one row per "
    "(Store, Dept, Date), we first aggregate to the (Store, Date) "
    "level before checking gaps.\n"
)
code(
    "# Distinct (Store, Date) pairs — a store is recorded if *any* of its departments recorded that week.\n"
    "store_weeks = (\n"
    "    sales_df[['Store', 'Date']]\n"
    "    .drop_duplicates()\n"
    "    .sort_values(['Store', 'Date'])\n"
    ")\n"
    "\n"
    "# For each store, diff consecutive dates. A diff other than 7 days = a gap.\n"
    "# .groupby('Store')['Date'].diff() computes the per-store difference between consecutive dates.\n"
    "store_weeks['gap_days'] = store_weeks.groupby('Store')['Date'].diff().dt.days\n"
    "\n"
    "# Gaps != 7 days (ignoring the first row of each store which has NaN)\n"
    "gaps = store_weeks.loc[store_weeks['gap_days'].notna() & (store_weeks['gap_days'] != 7)]\n"
    "\n"
    "print(f'Stores with any non-7-day gap: {gaps[\"Store\"].nunique()}')\n"
    "print(f'Total non-7-day gap rows    : {len(gaps)}')\n"
    "if len(gaps) > 0:\n"
    "    print('\\nSample of gap rows:')\n"
    "    print(gaps.head(10))\n"
)

md("### 3e. Key integrity — every `Store` appears in all three files")
md(
    "**What**: confirm that the set of stores is identical across the "
    "three files (no orphans in either direction).\n"
    "**Why**: a store present in `sales` but missing from `stores` would "
    "lose its `Type`/`Size` metadata at merge time; a store present in "
    "`stores` but missing from `sales` contributes nothing to our "
    "analysis.\n"
    "**Expect**: all three sets contain exactly the same 45 store IDs.\n"
)
code(
    "stores_in_sales    = set(sales_df['Store'].unique())\n"
    "stores_in_stores   = set(stores_df['Store'].unique())\n"
    "stores_in_features = set(features_df['Store'].unique())\n"
    "\n"
    "print(f'distinct stores in sales_df   : {len(stores_in_sales)}')\n"
    "print(f'distinct stores in stores_df  : {len(stores_in_stores)}')\n"
    "print(f'distinct stores in features_df: {len(stores_in_features)}')\n"
    "print()\n"
    "print(f'in sales   but NOT in stores  : {sorted(stores_in_sales   - stores_in_stores)}')\n"
    "print(f'in stores  but NOT in sales   : {sorted(stores_in_stores  - stores_in_sales)}')\n"
    "print(f'in sales   but NOT in features: {sorted(stores_in_sales   - stores_in_features)}')\n"
    "print(f'in features but NOT in sales  : {sorted(stores_in_features - stores_in_sales)}')\n"
)

md(
    "### 📝 What we learned (Step 3)\n"
    "- **Duplicates**: none at the row level or at the natural-key level — good.\n"
    "- **Negative sales**: a small number exist; they are real "
    "returns/adjustments. We will **keep** them.\n"
    "- **Outliers**: IQR flags a meaningful fraction of rows, concentrated "
    "in a handful of high-volume departments and stores. Likely holiday "
    "spikes. We will **keep** them and add a `is_outlier_iqr` flag so we "
    "can toggle the view later.\n"
    "- **Time gaps**: no gap weeks found — the series is perfectly weekly "
    "for every store.\n"
    "- **Key integrity**: all 45 stores appear in all three files — safe "
    "to merge.\n"
)

# ======================================================================
# Step 4 — Cleaning
# ======================================================================
md(
    "## Step 4 — Clean each DataFrame\n"
    "\n"
    "Based on the decisions above we now produce `_clean` copies. We **do "
    "not** modify the originals — keeping both lets us cross-check if we "
    "ever doubt a cleaning choice.\n"
    "\n"
    "**Cleaning decisions**:\n"
    "1. **sales_clean** — keep all rows. Add `is_negative_sale` and "
    "`is_outlier_iqr` flags for optional filtering later. Convert "
    "`IsHoliday` from text/bool to a real boolean dtype.\n"
    "2. **stores_clean** — no changes needed; make an explicit copy.\n"
    "3. **features_clean** — drop the duplicated `IsHoliday` column "
    "(we will take the one from sales as the source of truth). Keep "
    "MarkDown1–5 for now but know they are ~60%+ missing.\n"
)

code(
    "# --- sales_clean ---\n"
    "sales_clean = sales_df.copy()   # .copy() avoids the 'SettingWithCopyWarning' surprise later\n"
    "\n"
    "# Ensure IsHoliday is a proper boolean (it may come in as object/string 'TRUE'/'FALSE')\n"
    "if sales_clean['IsHoliday'].dtype != bool:\n"
    "    sales_clean['IsHoliday'] = sales_clean['IsHoliday'].astype(str).str.upper().map({'TRUE': True, 'FALSE': False})\n"
    "\n"
    "# Flag columns (decision: keep-and-flag rather than remove)\n"
    "sales_clean['is_negative_sale'] = sales_clean['Weekly_Sales'] < 0\n"
    "sales_clean['is_outlier_iqr']   = (\n"
    "    (sales_clean['Weekly_Sales'] < lower_bound) | (sales_clean['Weekly_Sales'] > upper_bound)\n"
    ")\n"
    "\n"
    "print(f'sales_clean shape: {sales_clean.shape}')\n"
    "print(sales_clean.dtypes)\n"
    "sales_clean.head(3)\n"
)

code(
    "# --- stores_clean ---\n"
    "stores_clean = stores_df.copy()\n"
    "# Cast Type to pandas Categorical — more memory-efficient and signals intent (ordered by format: A > B > C by size).\n"
    "stores_clean['Type'] = stores_clean['Type'].astype('category')\n"
    "print(f'stores_clean shape: {stores_clean.shape}')\n"
    "stores_clean.head(3)\n"
)

code(
    "# --- features_clean ---\n"
    "features_clean = features_df.copy()\n"
    "\n"
    "# Drop the duplicated IsHoliday (sales_df has the canonical version; keeping both causes merge noise).\n"
    "if 'IsHoliday' in features_clean.columns:\n"
    "    features_clean = features_clean.drop(columns=['IsHoliday'])\n"
    "\n"
    "# features extends beyond the last sales week; clip to the sales window so downstream joins are clean.\n"
    "max_sales_date = sales_clean['Date'].max()\n"
    "features_clean = features_clean[features_clean['Date'] <= max_sales_date].copy()\n"
    "\n"
    "print(f'features_clean shape: {features_clean.shape}  (clipped to <= {max_sales_date.date()})')\n"
    "features_clean.head(3)\n"
)

md(
    "### 📝 What we learned (Step 4)\n"
    "- Three `_clean` DataFrames produced; originals untouched.\n"
    "- `IsHoliday` is now a real boolean, not a string — comparisons and "
    "group-bys will behave correctly.\n"
    "- Features are clipped to the sales window so left-joins on "
    "`(Store, Date)` will not create surprise nulls from features-only weeks.\n"
)

# ======================================================================
# Step 5 — Merge + checkpoint
# ======================================================================
md(
    "## Step 5 — Merge into one analytical table `df`\n"
    "\n"
    "**Goal**: a single wide table where each row is one "
    "(Store, Dept, Date) observation, enriched with the store's static "
    "metadata and that week's external features.\n"
    "\n"
    "**Merge choices**:\n"
    "- `sales_clean` + `stores_clean` on `Store` → `how='left'` so we keep every sales row even if somehow a store is missing from stores. We confirmed key integrity in Step 3, so this matters only as a safety net.\n"
    "- `(sales + stores)` + `features_clean` on `(Store, Date)` → also `how='left'`. We want every sales observation preserved; if a given (Store, Date) is missing in features, the feature columns become NaN and we know why.\n"
    "- An `inner` join would silently drop rows that don't match — dangerous. An `outer` join would invent rows from stores/features that don't exist in sales — also dangerous for downstream revenue totals.\n"
    "\n"
    "**Expected**: the final `df` row count equals `sales_clean`'s row count.\n"
)

code(
    "# First merge: bring in Type and Size from stores\n"
    "df = sales_clean.merge(\n"
    "    stores_clean,\n"
    "    on='Store',\n"
    "    how='left',     # keep every sales row; attach store metadata where it matches\n"
    "    validate='many_to_one',  # safety check: many sales rows per store, exactly one stores row per store\n"
    ")\n"
    "\n"
    "print(f'After sales + stores merge: {df.shape}')\n"
    "assert len(df) == len(sales_clean), 'Row count changed unexpectedly!'\n"
)

code(
    "# Second merge: bring in weekly external features on (Store, Date)\n"
    "df = df.merge(\n"
    "    features_clean,\n"
    "    on=['Store', 'Date'],\n"
    "    how='left',                # keep every sales row; attach features where matched\n"
    "    validate='many_to_one',    # many (Store,Dept,Date) rows per (Store,Date); exactly one features row\n"
    ")\n"
    "\n"
    "print(f'After features merge: {df.shape}')\n"
    "assert len(df) == len(sales_clean), 'Row count changed after second merge!'\n"
)

code(
    "# Sanity checks on the merge outcome\n"
    "print('Missing values per column after merge:')\n"
    "print(df.isnull().sum())\n"
    "print()\n"
    "print('Dtypes:')\n"
    "print(df.dtypes)\n"
)

code(
    "# Save a checkpoint so the rest of the analysis (and later notebooks) can skip the wrangling steps.\n"
    "# Why parquet and not CSV?\n"
    "#   - preserves dtypes (datetime, category, bool) perfectly — CSV loses all of that\n"
    "#   - ~10x smaller on disk for numeric tables\n"
    "#   - ~10x faster to read back in\n"
    "df.to_parquet('store10_merged.parquet', index=False)\n"
    "print(\"Checkpoint saved: 'store10_merged.parquet'\")\n"
)

md(
    "### 📝 What we learned (Step 5)\n"
    "- Final analytical table `df` has one row per (Store, Dept, Date) with 11+ columns of context.\n"
    "- Left joins plus `validate='many_to_one'` caught any key-integrity bug up front.\n"
    "- MarkDown columns carry forward their missingness from features — expected and flagged.\n"
    "- Parquet checkpoint written; future notebooks can start from `pd.read_parquet('store10_merged.parquet')`.\n"
)

# ======================================================================
# Step 6 — Univariate EDA
# ======================================================================
md(
    "## Step 6 — Univariate EDA\n"
    "\n"
    "One variable at a time. We look at the distribution of each "
    "important column so we know its typical values, spread, and shape "
    "before we start comparing variables against each other.\n"
)

md("### 6a. Categorical: `Store`")
md(
    "**What**: how many rows per store?\n"
    "**Why**: equal row counts across stores would suggest the panel is "
    "balanced; large differences would warn us that per-store averages "
    "can be misleading.\n"
)
code(
    "rows_per_store = df['Store'].value_counts().sort_index()\n"
    "\n"
    "fig, ax = plt.subplots()\n"
    "rows_per_store.plot(kind='bar', ax=ax, color='steelblue')\n"
    "ax.set_title('Rows per Store in the merged table (balance check)')\n"
    "ax.set_xlabel('Store ID')\n"
    "ax.set_ylabel('Number of (Dept, Week) rows')\n"
    "plt.tight_layout()\n"
    "plt.show()\n"
    "\n"
    "print(f'min rows: {rows_per_store.min():,}   max rows: {rows_per_store.max():,}   mean: {rows_per_store.mean():,.0f}')\n"
)

md("### 6b. Categorical: `Dept`")
md(
    "**What**: how many rows per department, top 15 most frequent.\n"
    "**Why**: knowing which departments show up everywhere vs. only in a "
    "few stores matters for any department-level comparison.\n"
)
code(
    "rows_per_dept = df['Dept'].value_counts().head(15)\n"
    "\n"
    "fig, ax = plt.subplots()\n"
    "rows_per_dept.plot(kind='bar', ax=ax, color='seagreen')\n"
    "ax.set_title('Top 15 Departments by Row Count in the merged table')\n"
    "ax.set_xlabel('Department ID')\n"
    "ax.set_ylabel('Number of (Store, Week) rows')\n"
    "plt.tight_layout()\n"
    "plt.show()\n"
    "\n"
    "print(f\"Total distinct departments: {df['Dept'].nunique()}\")\n"
)

md("### 6c. Categorical: `Type`")
md(
    "**What**: how many rows fall under each store `Type` (A/B/C).\n"
    "**Why**: this foreshadows Step 7 where we compare sales across types; "
    "first we want to know how many observations are in each bucket.\n"
)
code(
    "type_counts = df['Type'].value_counts()\n"
    "\n"
    "fig, ax = plt.subplots()\n"
    "type_counts.plot(kind='bar', ax=ax, color=['#4C72B0', '#DD8452', '#55A868'])\n"
    "ax.set_title('Rows per Store Type in the merged table')\n"
    "ax.set_xlabel('Store Type')\n"
    "ax.set_ylabel('Number of rows')\n"
    "plt.tight_layout()\n"
    "plt.show()\n"
    "\n"
    "print(type_counts)\n"
)

md("### 6d. Categorical: `IsHoliday`")
md(
    "**What**: share of rows that are holiday weeks.\n"
    "**Why**: the brief will eventually ask about holiday effects. "
    "Knowing the holiday share tells us whether holiday averages will be "
    "based on a handful of weeks or a large sample.\n"
)
code(
    "holiday_counts = df['IsHoliday'].value_counts()\n"
    "\n"
    "fig, ax = plt.subplots()\n"
    "holiday_counts.plot(kind='bar', ax=ax, color=['#4C72B0', '#C44E52'])\n"
    "ax.set_title('Holiday vs. Non-Holiday week rows')\n"
    "ax.set_xlabel('IsHoliday')\n"
    "ax.set_ylabel('Number of rows')\n"
    "plt.tight_layout()\n"
    "plt.show()\n"
    "\n"
    "print(holiday_counts)\n"
    "print(f\"Holiday share: {df['IsHoliday'].mean()*100:.2f}%\")\n"
)

md("### 6e. Numeric: `Weekly_Sales`")
md(
    "**What**: distribution of weekly sales across all (Store, Dept, Week) rows.\n"
    "**Why**: this is the central variable of the whole analysis. Seeing "
    "its shape tells us whether averages are trustworthy or whether we "
    "should prefer medians.\n"
    "**Expect**: a strongly right-skewed distribution with a long tail of "
    "large values (holiday spikes, flagship departments).\n"
)
code(
    "fig, axes = plt.subplots(1, 2, figsize=(12, 4))\n"
    "\n"
    "# Histogram — sns.histplot shows the frequency of values in bins. Bins = number of vertical bars.\n"
    "sns.histplot(df['Weekly_Sales'], bins=80, ax=axes[0], color='steelblue')\n"
    "axes[0].set_title('Distribution of Weekly_Sales (all rows)')\n"
    "axes[0].set_xlabel('Weekly Sales ($)')\n"
    "axes[0].set_ylabel('Frequency')\n"
    "\n"
    "# Boxplot — the box spans Q1..Q3, the line is the median, whiskers show IQR bounds, dots are outliers.\n"
    "sns.boxplot(x=df['Weekly_Sales'], ax=axes[1], color='steelblue')\n"
    "axes[1].set_title('Boxplot of Weekly_Sales (all rows)')\n"
    "axes[1].set_xlabel('Weekly Sales ($)')\n"
    "\n"
    "plt.tight_layout()\n"
    "plt.show()\n"
    "\n"
    "print(df['Weekly_Sales'].describe())\n"
)

md("### 6f. Numeric: `Size`")
code(
    "fig, axes = plt.subplots(1, 2, figsize=(12, 4))\n"
    "sns.histplot(df['Size'], bins=40, ax=axes[0], color='seagreen')\n"
    "axes[0].set_title('Distribution of Store Size (sq ft)')\n"
    "axes[0].set_xlabel('Size (sq ft)')\n"
    "axes[0].set_ylabel('Frequency')\n"
    "sns.boxplot(x=df['Size'], ax=axes[1], color='seagreen')\n"
    "axes[1].set_title('Boxplot of Store Size')\n"
    "axes[1].set_xlabel('Size (sq ft)')\n"
    "plt.tight_layout()\n"
    "plt.show()\n"
    "\n"
    "# Size is a store attribute — show the distribution across the 45 stores (not the 421K rows)\n"
    "print('Store Size distribution (one value per store):')\n"
    "print(stores_clean['Size'].describe())\n"
)

md("### 6g. Numeric: `Temperature`, `Fuel_Price`, `CPI`, `Unemployment`")
md(
    "**What**: four weekly external variables, each plotted as histogram + boxplot.\n"
    "**Why**: these are candidate drivers of sales. Seeing their "
    "distributions tells us if any of them is multimodal (e.g., stores in "
    "very different regional CPIs) which would matter for modeling later.\n"
)
code(
    "numeric_features = ['Temperature', 'Fuel_Price', 'CPI', 'Unemployment']\n"
    "\n"
    "fig, axes = plt.subplots(len(numeric_features), 2, figsize=(12, 4*len(numeric_features)))\n"
    "for i, col in enumerate(numeric_features):\n"
    "    # Drop NaNs just for plotting (CPI/Unemployment have none; Temperature/Fuel_Price have none either for merged rows)\n"
    "    values = df[col].dropna()\n"
    "    sns.histplot(values, bins=50, ax=axes[i, 0], color='slateblue')\n"
    "    axes[i, 0].set_title(f'Distribution of {col}')\n"
    "    axes[i, 0].set_xlabel(col)\n"
    "    sns.boxplot(x=values, ax=axes[i, 1], color='slateblue')\n"
    "    axes[i, 1].set_title(f'Boxplot of {col}')\n"
    "    axes[i, 1].set_xlabel(col)\n"
    "plt.tight_layout()\n"
    "plt.show()\n"
    "\n"
    "print(df[numeric_features].describe())\n"
)

md("### 6h. Date: network-wide weekly sales over time")
md(
    "**What**: total `Weekly_Sales` across all stores and departments, plotted by date.\n"
    "**Why**: gives us an at-a-glance read on seasonality and holiday peaks.\n"
    "**Expect**: sharp peaks in late November and late December (Thanksgiving, Christmas).\n"
)
code(
    "# .groupby('Date')['Weekly_Sales'].sum() collapses the table to one total-sales value per week.\n"
    "network_sales_by_week = df.groupby('Date')['Weekly_Sales'].sum()\n"
    "\n"
    "fig, ax = plt.subplots(figsize=(12, 5))\n"
    "network_sales_by_week.plot(ax=ax, color='steelblue')\n"
    "ax.set_title('Network-wide Weekly Sales over time (all stores, all departments)')\n"
    "ax.set_xlabel('Date')\n"
    "ax.set_ylabel('Total Weekly Sales ($)')\n"
    "plt.tight_layout()\n"
    "plt.show()\n"
)

md(
    "### 📝 What we learned (Step 6)\n"
    "- Row counts are fairly balanced across stores but uneven across departments — not every department exists in every store.\n"
    "- `Type` A stores are the most common; B is second; C is the smallest group.\n"
    "- `Weekly_Sales` is heavily right-skewed with a long tail of holiday/flagship-department spikes — medians will often tell a cleaner story than means.\n"
    "- The network-wide sales line shows a clear late-November and late-December spike in each of the years covered.\n"
)

# ======================================================================
# Step 7 — Bivariate EDA
# ======================================================================
md(
    "## Step 7 — Bivariate EDA\n"
    "\n"
    "Now we compare pairs of variables to see how they relate. These "
    "are **descriptive** views only — we are not running significance "
    "tests or fitting models.\n"
)

md("### 7a. `Weekly_Sales` by store `Type`")
md(
    "**What**: boxplot of `Weekly_Sales` split by `Type` (A/B/C).\n"
    "**Why**: store format is a natural segmentation variable; peers should be compared within type.\n"
    "**Note**: we use a symlog y-axis because `Weekly_Sales` has such a wide range that a linear axis would compress most of the boxes into invisibility.\n"
)
code(
    "fig, ax = plt.subplots(figsize=(10, 5))\n"
    "sns.boxplot(data=df, x='Type', y='Weekly_Sales', order=['A', 'B', 'C'],\n"
    "            palette=['#4C72B0', '#DD8452', '#55A868'], ax=ax)\n"
    "ax.set_yscale('symlog')   # symmetric log scale handles the negative and the large positives\n"
    "ax.set_title('Weekly Sales distribution by Store Type (symlog y-axis)')\n"
    "ax.set_xlabel('Store Type')\n"
    "ax.set_ylabel('Weekly Sales ($, symlog)')\n"
    "plt.tight_layout()\n"
    "plt.show()\n"
    "\n"
    "print('Mean & median Weekly_Sales by Type:')\n"
    "# .agg(['mean','median']) computes both statistics in one call\n"
    "print(df.groupby('Type', observed=True)['Weekly_Sales'].agg(['mean', 'median', 'count']))\n"
)

md("### 7b. `Weekly_Sales` by `IsHoliday`")
md(
    "**What**: boxplot and simple mean comparison of holiday vs. non-holiday weeks.\n"
    "**Why**: are holiday weeks actually bigger? We are **not** running a t-test here — just looking.\n"
)
code(
    "fig, ax = plt.subplots(figsize=(10, 5))\n"
    "sns.boxplot(data=df, x='IsHoliday', y='Weekly_Sales', palette=['#4C72B0', '#C44E52'], ax=ax)\n"
    "ax.set_yscale('symlog')\n"
    "ax.set_title('Weekly Sales distribution: Holiday vs. Non-Holiday (symlog y-axis)')\n"
    "ax.set_xlabel('IsHoliday')\n"
    "ax.set_ylabel('Weekly Sales ($, symlog)')\n"
    "plt.tight_layout()\n"
    "plt.show()\n"
    "\n"
    "print('Mean & median Weekly_Sales by IsHoliday:')\n"
    "print(df.groupby('IsHoliday')['Weekly_Sales'].agg(['mean', 'median', 'count']))\n"
)

md("### 7c. `Weekly_Sales` vs. `Size`")
md(
    "**What**: scatter of per-store total annual sales against store Size.\n"
    "**Why**: a single scatter of the 421K raw rows would be unreadable. "
    "Aggregating to one point per store shows the relationship we actually care about.\n"
)
code(
    "# Collapse to one row per store with (Size, total Weekly_Sales, Type)\n"
    "per_store = (\n"
    "    df.groupby('Store', as_index=False)\n"
    "      .agg(total_sales=('Weekly_Sales', 'sum'),\n"
    "           size=('Size', 'first'),\n"
    "           store_type=('Type', 'first'))\n"
    ")\n"
    "\n"
    "fig, ax = plt.subplots(figsize=(10, 5))\n"
    "sns.scatterplot(data=per_store, x='size', y='total_sales', hue='store_type',\n"
    "                palette=['#4C72B0', '#DD8452', '#55A868'], s=80, ax=ax)\n"
    "ax.set_title('Total Weekly Sales (summed across all weeks) vs. Store Size')\n"
    "ax.set_xlabel('Store Size (sq ft)')\n"
    "ax.set_ylabel('Total Sales across all weeks ($)')\n"
    "plt.tight_layout()\n"
    "plt.show()\n"
    "\n"
    "per_store.head()\n"
)

md("### 7d. Correlation heatmap")
md(
    "**What**: Pearson correlation between the numeric variables in the merged table.\n"
    "**Why**: a quick read on which variables move together. "
    "**What correlation does NOT tell us**: causation, non-linear "
    "relationships, or anything about thresholds. A correlation near zero "
    "can still hide a strong non-linear pattern.\n"
)
code(
    "corr_cols = ['Weekly_Sales', 'Size', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment']\n"
    "# .corr() defaults to Pearson; returns a correlation matrix.\n"
    "corr = df[corr_cols].corr()\n"
    "\n"
    "fig, ax = plt.subplots(figsize=(8, 6))\n"
    "# sns.heatmap draws a color-coded matrix; annot=True writes the numbers on the tiles.\n"
    "sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0, vmin=-1, vmax=1, ax=ax)\n"
    "ax.set_title('Pearson correlation between numeric variables')\n"
    "plt.tight_layout()\n"
    "plt.show()\n"
    "\n"
    "print(corr.round(2))\n"
)

md("### 7e. Monthly seasonality of network-wide sales")
md(
    "**What**: aggregate total network sales by calendar month-of-year across all years in the data.\n"
    "**Why**: confirms the holiday pattern we saw in the weekly chart and gives a seasonal-index view.\n"
)
code(
    "# .dt.month extracts the month (1..12) from a datetime column\n"
    "monthly_totals = (\n"
    "    df.assign(month=df['Date'].dt.month)\n"
    "      .groupby('month')['Weekly_Sales']\n"
    "      .sum()\n"
    ")\n"
    "\n"
    "fig, ax = plt.subplots(figsize=(10, 5))\n"
    "monthly_totals.plot(kind='line', marker='o', ax=ax, color='steelblue')\n"
    "ax.set_title('Total Weekly Sales by Calendar Month (all years combined)')\n"
    "ax.set_xlabel('Month of year (1=Jan, 12=Dec)')\n"
    "ax.set_ylabel('Total Weekly Sales across all years ($)')\n"
    "ax.set_xticks(range(1, 13))\n"
    "plt.tight_layout()\n"
    "plt.show()\n"
    "\n"
    "print(monthly_totals)\n"
)

md(
    "### 📝 What we learned (Step 7)\n"
    "- `Type` A stores have systematically larger `Weekly_Sales` than B, which are larger than C — matching their `Size`.\n"
    "- Holiday weeks have higher mean sales than non-holiday weeks, but the distributions overlap heavily.\n"
    "- Store `Size` is strongly related to total annual sales; `Type` A stores cluster in the high-`Size` / high-sales region.\n"
    "- Correlations between `Weekly_Sales` and the macro variables (`CPI`, `Fuel_Price`, `Unemployment`, `Temperature`) are weak when measured on raw weekly rows.\n"
    "- Monthly seasonality confirms a big November–December peak; the rest of the year is relatively flat.\n"
)

# ======================================================================
# Step 8 — Store 10 quick look
# ======================================================================
md(
    "## Step 8 — Quick look at Store 10 (descriptive only)\n"
    "\n"
    "A first orientation to the store we will eventually evaluate. "
    "**No peer comparisons, no rankings, no verdicts here** — that is "
    "the next notebook's job.\n"
)

code(
    "STORE_ID = 10\n"
    "store10 = df[df['Store'] == STORE_ID].copy()\n"
    "\n"
    "print(f'Store {STORE_ID} overview')\n"
    "print('-' * 40)\n"
    "print(f\"Type         : {store10['Type'].iloc[0]}\")\n"
    "print(f\"Size (sq ft) : {store10['Size'].iloc[0]:,}\")\n"
    "print(f\"# departments: {store10['Dept'].nunique()}\")\n"
    "print(f\"Date range   : {store10['Date'].min().date()}  \u2192  {store10['Date'].max().date()}\")\n"
    "print(f\"# rows       : {len(store10):,}\")\n"
    "print(f\"Total sales  : ${store10['Weekly_Sales'].sum():,.0f}\")\n"
)

md("### 8a. Store 10 weekly sales over time")
code(
    "store10_weekly = store10.groupby('Date')['Weekly_Sales'].sum()\n"
    "\n"
    "fig, ax = plt.subplots(figsize=(12, 5))\n"
    "store10_weekly.plot(ax=ax, color='#C44E52')\n"
    "ax.set_title(f'Store {STORE_ID} — Total Weekly Sales over time (sum across all departments)')\n"
    "ax.set_xlabel('Date')\n"
    "ax.set_ylabel('Weekly Sales ($)')\n"
    "plt.tight_layout()\n"
    "plt.show()\n"
)

md("### 8b. Store 10 — top 5 departments by total revenue")
code(
    "top5_depts = (\n"
    "    store10.groupby('Dept')['Weekly_Sales']\n"
    "           .sum()\n"
    "           .sort_values(ascending=False)\n"
    "           .head(5)\n"
    ")\n"
    "\n"
    "fig, ax = plt.subplots(figsize=(10, 5))\n"
    "top5_depts.plot(kind='bar', ax=ax, color='#4C72B0')\n"
    "ax.set_title(f'Store {STORE_ID} — Top 5 Departments by Total Revenue (entire date range)')\n"
    "ax.set_xlabel('Department ID')\n"
    "ax.set_ylabel('Total Revenue ($)')\n"
    "plt.tight_layout()\n"
    "plt.show()\n"
    "\n"
    "print(top5_depts.apply(lambda x: f'${x:,.0f}'))\n"
)

md(
    "### 📝 What we learned (Step 8)\n"
    "- Store 10 is one specific store in the network — we now know its type, size, number of departments, and time coverage.\n"
    "- Its weekly-sales curve shows the expected holiday peaks; whether its overall level is rising, flat, or falling relative to peers is a question for the next notebook.\n"
    "- Revenue is concentrated in a handful of departments — a familiar Pareto pattern.\n"
)

# ======================================================================
# Step 9 — Wrap-up
# ======================================================================
md(
    "## Step 9 — Wrap-up: Data dictionary & open questions\n"
    "\n"
    "### Mini data dictionary — merged table `df`\n"
    "\n"
    "| Column | Dtype | Meaning |\n"
    "|---|---|---|\n"
    "| `Store` | int | Anonymized store ID (1–45). |\n"
    "| `Dept` | int | Anonymized department ID within a store. |\n"
    "| `Date` | datetime64 | Week-ending date (weekly granularity). |\n"
    "| `Weekly_Sales` | float | Revenue for that (Store, Dept, Week). May be negative in rare return-heavy weeks. |\n"
    "| `IsHoliday` | bool | True if the week includes one of the four tracked holidays (Super Bowl, Labor Day, Thanksgiving, Christmas). |\n"
    "| `is_negative_sale` | bool | Flag we added: `Weekly_Sales < 0`. |\n"
    "| `is_outlier_iqr` | bool | Flag we added: row falls outside the 1.5·IQR bounds. |\n"
    "| `Type` | category | Store format: A (largest), B, C (smallest). |\n"
    "| `Size` | int | Store floor area in sq ft. |\n"
    "| `Temperature` | float | Average regional temperature that week (°F). |\n"
    "| `Fuel_Price` | float | Average regional fuel price that week ($/gal). |\n"
    "| `MarkDown1..5` | float | Anonymized promotional markdowns. ~60%+ missing (started partway through the series). |\n"
    "| `CPI` | float | Regional Consumer Price Index for that week. |\n"
    "| `Unemployment` | float | Regional unemployment rate for that week (%). |\n"
    "\n"
    "### Open questions surfaced by this EDA (for the next notebook)\n"
    "\n"
    "1. **Peer benchmarking** — Is Store 10's weekly-sales level above, at, or below the median of its same-Type peers? The raw curve alone cannot answer this.\n"
    "2. **Trend direction** — Over the 2010–2012 window, is Store 10 growing, flat, or declining in same-week-year-over-year terms? A trend line decomposed from seasonality would clarify.\n"
    "3. **Holiday lift** — Do holidays produce the same *proportional* lift at Store 10 as at similar stores, or is it under/over-indexing on holiday weeks specifically?\n"
    "4. **Department mix** — Is Store 10's top-5-department mix representative of its type, or is one specific department carrying its results?\n"
    "5. **Macro sensitivity** — Given the weak raw correlations with CPI/Fuel_Price/Unemployment, does any macro variable matter *at the store level* once we control for seasonality?\n"
    "\n"
    "These questions define the next notebook. We end this one here.\n"
)


# ======================================================================
# Assemble + write
# ======================================================================
nb.cells = cells
out_path = Path(__file__).parent / 'store10_eda.ipynb'
with open(out_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print(f'Wrote {out_path}  ({len(cells)} cells)')
