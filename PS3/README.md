# PS3 — Momentum Portfolio Construction and Analysis

## Overview

This project replicates and analyzes the construction and performance of **momentum-based portfolios**, following the methodology of **Daniel and Moskowitz (2016)**. The assignment is part of the **Quantitative Asset Management (QAM)** course in the **UCLA Anderson MFE Program (Spring 2025)**.

The problem statement is provided in `MFE_PS3.pdf`.
The implementation, analysis, and results are contained in:

* `PS3.ipynb` — full Python notebook implementation
* `PS3_notebook.pdf` — rendered notebook in PDF format
* `PS3_VikalpThukral_406534669.pdf` — formal written report
* Supporting datasets, including CRSP monthly equity data and factor files

The project reconstructs key aspects of the **momentum anomaly**, evaluates its robustness, and examines its historical performance and risk characteristics.

---

## Problem Statement

Momentum investing involves buying stocks that have performed well in the recent past (“winners”) and selling those that have performed poorly (“losers”). The goal is to replicate and validate the Daniel-Moskowitz (2016) findings on momentum portfolios using CRSP stock data from **1927–2024**.

Specifically, the assignment asks us to:

1. Construct stock-level momentum signals based on lagged 12-month returns (with a one-month skip).
2. Sort stocks into deciles using two methodologies:

   * **DM (Daniel-Moskowitz)**: NYSE breakpoints only.
   * **KRF (Kenneth R. French)**: all-exchange breakpoints.
3. Compute value-weighted decile returns and excess returns using Fama-French factors.
4. Compare empirical outcomes against published benchmarks.
5. Analyze the performance and stability of the **Winner-Minus-Loser (WML)** portfolio.
6. Evaluate the recent decade (2015–2024) to assess whether the momentum effect persists.

---

## Implementation Summary

### Q1 — Data Preparation

* Loaded and filtered **CRSP monthly equity data (1926–2024)**.
* Included delisting returns to avoid survivorship bias:
  [
  \text{RET_FULL} = (1 + \text{RET}) (1 + \text{DLRET}) - 1
  ]
* Computed lagged market capitalization and 12-month cumulative ranking returns (skipping the last month).

### Q2 — Decile Formation

* Sorted stocks monthly into **10 deciles** using both DM and KRF breakpoints.
* DM uses **NYSE-only** stocks for threshold computation; KRF uses **all exchanges**.
* Output includes `DM_decile` and `KRF_decile` assignments for every stock-month observation.

### Q3 — Value-Weighted Portfolio Returns

* Calculated monthly **value-weighted returns** for each decile and both methodologies.
* Merged with **Fama-French factor data** to compute excess returns (`R - Rf`).
* Output: 11,760 monthly decile observations (1176 months × 10 deciles).

### Q4 — Daniel–Moskowitz Benchmark Replication

* Computed summary statistics:

  * Mean excess return, volatility, Sharpe ratio, skewness, correlation with DM benchmark.
* Achieved **>99% correlation** with Daniel–Moskowitz (2016) benchmark portfolios.
* Constructed and evaluated the **Winner-Minus-Loser (WML)** portfolio.

### Q5 — Kenneth French Benchmark Comparison

* Replicated the same analysis using KRF deciles and compared with official **Kenneth French momentum returns**.
* Verified near-perfect replication accuracy (correlations >0.99 for all deciles).

### Q6 — Recent Momentum Performance (2015–2024)

* Computed recent-period WML statistics:

  * Annualized mean return: **20.54%**
  * Volatility: **35.46%**
  * Sharpe ratio: **0.58**
  * Skewness: **–0.84**
* The cumulative return plot shows a strong but volatile uptrend in WML over the decade.

### Q7 — Interpretation and Implementation

* Discussed **risks of momentum investing**, including momentum crashes and regime dependency.
* Proposed **risk-management extensions**, such as volatility scaling and crash-hedging.
* Described a **hybrid rotation-hedge strategy** combining momentum with bond rotation and inverse ETF hedging for robustness.

---

## Key Results

| Statistic              | WML (2015–2024) |
| ---------------------- | --------------- |
| Annualized Mean Return | **20.54%**      |
| Annualized Volatility  | **35.46%**      |
| Sharpe Ratio           | **0.58**        |
| Skewness               | **–0.84**       |

The replicated results confirm that the momentum effect remains strong on average but highly volatile and prone to large drawdowns during reversals.

---

## Files and Structure

```
PS3/
│
├── MFE_PS3.pdf                        # Problem statement
├── PS3.ipynb                          # Main Jupyter notebook
├── PS3_notebook.pdf                   # PDF export of notebook
├── PS3_VikalpThukral_406534669.pdf    # Final report
├── CRSP_monthly_equity_1926_2024.csv  # Main dataset (LFS)
├── DM_data_2017_03/                   # Daniel–Moskowitz benchmark data
└── FF_Factors/                        # Fama–French macro factors
```

---

## References

1. Daniel, K., & Moskowitz, T. J. (2016). *Momentum Crashes*. Journal of Financial Economics, 122(2), 221–247.
2. Kenneth R. French Data Library — Momentum Portfolios and Fama–French Factors.
3. UCLA Anderson MFE Program, QAM Course Materials (2025).
4. Thukral, V. (2025). *Dynamic Equity-Bond Rotation Strategy with Option-Enhanced Risk Management*.

