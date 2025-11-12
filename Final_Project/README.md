

# BAC Factor — Replication Project

**Author:** Vikalp Thukral
**Program:** UCLA Anderson MFE III — Quantitative Asset Management
**Date:** May 2025

## Purpose

Replicate the **Betting Against Correlation (BAC)** factor and evaluate its performance, construction robustness, and relation to standard equity factors. The BAC factor goes **long low-correlation stocks** and **short high-correlation stocks**, scaling legs to be beta-neutral and dollar-neutral. The rationale follows the decomposition of market beta:
[
\beta_i=\rho_{i,m}\frac{\sigma_i}{\sigma_m},
]
so isolating and betting against **correlation** targets the portion of beta unrelated to idiosyncratic volatility.

## Contents

| File                            | Role                                                                                                                                                                            |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bac-daily-download-dump.ipynb` | Data ingestion. Downloads daily prices (BAC universe = broad US equities), market index, risk-free rates; constructs clean return series with consistent trading calendars.     |
| `bac-datacleaning-052925.ipynb` | Cleaning and feature engineering. Computes rolling volatilities, market volatility, and **pairwise correlation with the market**; creates the BAC signal and portfolio weights. |
| `bac-053025-v2.ipynb`           | Core replication and analysis. Forms the BAC factor, runs time-series/CS diagnostics, regression attribution vs. FF3/FF5/MOM, and produces performance plots/tables.            |

> If you only want the final factor and results, open `bac-053025-v2.ipynb`.

## Data

* **Prices:** Daily total-return series for US common stocks; survivorship-aware panel (CRSP/WRDS or equivalent).
* **Market proxy:** Value-weighted market index (CRSP VW or S&P 500 total return).
* **Risk-free rate:** Daily T-bill proxy.
* **Sample:** 2010–2024 (extendable).
* **Universe filters:** Common shares only; basic liquidity and price screens; delisting returns handled.

## Methodology

### 1) Rolling statistics

* **Estimation window:** 252 trading days (default).
* **Per stock (i):**

  * ( \sigma_i ): stock volatility (stdev of daily returns).
  * ( \sigma_m ): market volatility.
  * ( \rho_{i,m} ): correlation with the market (rolling Pearson).
  * ( \beta_i=\rho_{i,m}\sigma_i/\sigma_m ) (for diagnostics only).

### 2) BAC signal

* **Primary signal:** negative of the market correlation, ( s_i = -\rho_{i,m} ).
  Lower correlation → higher weight in the **long** leg; higher correlation → weight in the **short** leg.
* **Neutralizations/constraints:**

  * Dollar-neutral: long and short legs sum to zero.
  * **Beta-neutral:** scale long/short legs so portfolio beta to the market is ~0 each rebalance.
  * Optional volatility targeting: scale to constant ex-ante volatility.

### 3) Portfolio construction

* **Sorting:** Cross-sectional on ( \rho_{i,m} ) each month.
* **Buckets:** Quintiles or deciles; BAC factor = Long(low-ρ) − Short(high-ρ).
* **Weights:** Value-weight or risk-weight within each bucket; winsorize outliers; apply turnover control.
* **Rebalance:** Monthly; trade on first trading day using previous window estimates.

### 4) Backtest & evaluation

* **Performance:** Cumulative and annualized return, volatility, Sharpe, drawdown, turnover, hit rate.
* **Exposures:** Rolling betas to MKT, SMB, HML, RMW, CMA, MOM; maintain near-zero market beta by construction.
* **Attribution:** Time-series regressions of BAC returns on standard factors to estimate alpha and residual risk.
* **Robustness:** Vary window (126/504 days), alternative weighting, liquidity screens, and transaction-cost haircuts.

## What to Expect

* BAC should exhibit **low market beta** by design and a return stream driven by cross-sectional correlation dispersion.
* Ex-post correlations with HML/SMB/MOM are typically modest; alpha depends on period and trading frictions.
* Performance is sensitive to correlation-window choice, microcap handling, and turnover controls.

## Reproduction

1. **Run ingestion:** `bac-daily-download-dump.ipynb`
   Configure paths/credentials; verify calendar alignment and absence of NaNs after merges.
2. **Build features:** `bac-datacleaning-052925.ipynb`
   Generates rolling ( \rho_{i,m} ), ( \sigma_i ), ( \sigma_m ), and cleaned panel for portfolio formation.
3. **Form factor & analyze:** `bac-053025-v2.ipynb`
   Creates BAC long/short, applies beta-neutral scaling, outputs return series, figures, and tables.

## Outputs (from `bac-053025-v2.ipynb`)

* `bac_factor_returns.csv` — daily BAC factor return series.
* `fig_bac_cumulative.png` — cumulative returns of BAC vs. market.
* `fig_bac_rolling_beta.png` — rolling market beta (should hover near zero).
* `table_bac_perf.md` — summary stats; `table_bac_ffreg.md` — factor regressions.

## Notes and Caveats

* Use robust correlation estimates if microstructure noise is material (e.g., shrinkage, Spearman, or EWMA).
* Enforce liquidity and price floors to control turnover and outliers.
* Transaction costs materially affect BAC; include slippage/fees when reporting out-of-sample results.

## References

* Decomposition ( \beta_i=\rho_{i,m}\sigma_i/\sigma_m ) and correlation-based tilts widely discussed in the factor literature; BAC isolates the **correlation** channel of beta rather than volatility.
* Standard equity factors: Fama–French (1993, 2015), Carhart (1997).

