# Quantitative Asset Management Projects (MGMTMFE 431)

**Author:** Vikalp Thukral
**Program:** UCLA Anderson MFE III — Quantitative Asset Management
**Course Instructor:** Prof. Bernard Herskovic
**Term:** Spring 2025

---

## Overview

This repository consolidates five major projects completed as part of the **Quantitative Asset Management** course (MGMTMFE 431).
Each problem set replicates a canonical empirical asset-pricing factor or model — from the **market and risk-free components** through **size, value, momentum**, and finally **betting against correlation (BAC)**.

The sequence reflects both theoretical depth and technical rigor: beginning with data handling and portfolio formation using WRDS/CRSP/Compustat data, progressing to multi-factor replication, and culminating in an original factor-engineering project.

---

## Repository Structure

| Folder            | Factor / Theme                                      | Core Objective                                                                                                                                                                                                                                  |
| ----------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **PS1/**          | **Market and Risk-Free Factor Construction**        | Construct market (MKT-RF) and risk-free (RF) series from CRSP monthly returns; replicate CAPM components used in Fama–French factor models.                                                                                                     |
| **PS2/**          | **Profitability and Investment Factors (RMW, CMA)** | Recreate the Fama–French 5-Factor extensions (2015). Compute **RMW** (robust-minus-weak) and **CMA** (conservative-minus-aggressive) factors using Compustat accounting data and CRSP linkages.                                                 |
| **PS3/**          | **Momentum Factor Replication**                     | Reproduce the **momentum anomaly** as in *Daniel & Moskowitz (2016)* and *Kenneth French*. Define ranking returns, form decile portfolios, and validate the **WML (winners-minus-losers)** factor versus published benchmarks.                  |
| **PS4/**          | **Size and Value Factor Replication (SMB & HML)**   | Integrate CRSP and Compustat to replicate **SMB (small-minus-big)** and **HML (high-minus-low)** factors from *Fama & French (1992, 1993)*. Build decile portfolios on market equity and book-to-market, test against Ken French library data.  |
| **FinalProject/** | **Betting Against Correlation (BAC)**               | Design and backtest the **BAC factor**, going long low-correlation stocks and short high-correlation stocks. Implement rolling correlation estimation, beta-neutral portfolio formation, and performance attribution vs. standard risk factors. |

---

## Project Summaries

### PS1 — Market Factor Construction

* Derived the **market excess return (MKT-RF)** by aggregating CRSP equity data.
* Constructed a consistent **risk-free rate** series aligned with Fama–French inputs.
* Verified that the computed market portfolio tracks the official Fama–French series closely.

### PS2 — Profitability and Investment Factors

* Replicated **RMW (robust minus weak)** and **CMA (conservative minus aggressive)** factors using firm-level operating profitability and total asset growth.
* Created cross-sectional deciles on profitability and investment, value-weighted monthly.
* Compared replication statistics (mean, volatility, Sharpe, correlation) to the French 5-factor library.

### PS3 — Momentum Factor (Daniel & Moskowitz 2016)

* Constructed rolling ranking returns based on 12-month past performance, skipping the most recent month.
* Formed decile portfolios both under **Daniel–Moskowitz** and **Kenneth French** definitions.
* Calculated long–short WML returns and validated performance vs. benchmark data (correlations >0.99 across deciles).
* Discussed **momentum crashes** and implementation limits in recent years.

### PS4 — Size and Value Factor (Fama–French 1992/1993)

* Merged **CRSP and Compustat** via the CCM link table to compute **market equity (ME)** and **book equity (BE)**.
* Formed decile portfolios by **NYSE breakpoints** for ME and BE/ME ratios.
* Constructed **SMB** and **HML** factors and evaluated replication accuracy vs. Ken French portfolios (correlations ≈0.99).
* Analyzed factor consistency over time — confirming persistence of size and value premia but attenuation in the post-2010 period.

### Final Project — Betting Against Correlation (BAC)

* Implemented a **novel factor isolating the correlation component of beta**, as in Frazzini–Pedersen-style decompositions.
* BAC goes long **low-correlation**, short **high-correlation** stocks; scaled to maintain dollar- and beta-neutrality.
* Computed rolling market correlations, formed monthly BAC portfolios, and backtested performance.
* Demonstrated that **BAC captures the correlation-risk premium** independent of volatility, with low market beta and moderate positive alpha over 2010–2024.
* Benchmarked BAC against standard Fama–French factors and observed low correlation, indicating orthogonal return drivers.

---

## Methodology Highlights

* **Data Sources:** WRDS (CRSP, Compustat North America), Kenneth French Data Library.
* **Portfolio Construction:** Decile-based, value-weighted, NYSE breakpoints, July–June rebalancing.
* **Evaluation Metrics:** Annualized mean, volatility, Sharpe ratio, skewness, and correlations with official Fama–French series.
* **Factor Validation:** Replication correlations >0.95 across all factors (MKT, SMB, HML, RMW, CMA, WML).
* **Codebase:** Modular Python notebooks for data ingestion, cleaning, portfolio formation, and result visualization.

---

## References

* Fama, Eugene F., and Kenneth R. French (1992, 1993, 2015) — *Common Risk Factors in the Returns on Stocks and Bonds*.
* Daniel, Kent, and Tobias Moskowitz (2016) — *Momentum Crashes*, *Journal of Financial Economics*.
* Kenneth R. French Data Library (U.S. Factor Portfolios).
* WRDS (CRSP, Compustat, CCM Link Tables).
* Frazzini, A., and Pedersen, L. H. (2014) — *Betting Against Beta* and correlation-based decompositions.
