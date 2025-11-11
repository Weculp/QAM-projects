# Quantitative Asset Management – Problem Set 2 (Risk Parity)

**Course:** MGMTMFE 431 – Quantitative Asset Management
**University:** UCLA Anderson School of Management
**Instructor:** Professor Bernard Herskovic
**Term:** Spring 2025
**Student:** Vikalp Thukral (UID: 406534669)

---

## Project Overview

This repository contains the full implementation, analysis, and report for **Problem Set 2 (PS2): Risk Parity**, based on the paper:

**“Leverage Aversion and Risk Parity”**
*Clifford S. Asness, Andrea Frazzini, and Lasse H. Pedersen (2012, Financial Analysts Journal, Vol. 68, No. 1)*.

The goal of this project is to replicate and analyze the performance of **risk-parity portfolios** using U.S. stock, bond, and Treasury data from **January 1926 to December 2024**, following the methodology described in Asness et al. (2012).

---

## Repository Structure

| File                                                       | Description                                                                 |
| ---------------------------------------------------------- | --------------------------------------------------------------------------- |
| `MFE_PS2.pdf`                                              | Original problem statement and instructions provided by Professor Herskovic |
| `PS2_406534669.ipynb`                                      | Main Jupyter Notebook containing the Python implementation and workflow     |
| `PS2_406534669.pdf`                                        | Exported PDF version of the Jupyter Notebook                                |
| `PS2_406534669_writeup_full.pdf`                           | Full written report and analytical discussion                               |
| `PS2_406534669.py`                                         | Standalone Python script used for submission                                |
| `bonds_data.csv`, `rf_data.csv`, `Monthly_CRSP_Stocks.csv` | Processed CRSP datasets for bonds, T-bills, and stocks                      |
| `git_lfs/crsp_raw_PS2.csv`                                 | Large raw dataset stored via Git LFS (approx. 320 MB)                       |

---

## Problem Statement Summary

The assignment, titled **“Risk Parity”**, asked students to replicate empirical results from Asness et al. (2012) using CRSP data accessed through WRDS.
The exercise was divided into four main components, each implemented as a Python function:

1. **PS2_Q1 – Construct Bond Market Returns**

   * Compute equal-weighted and value-weighted bond market returns.
   * Calculate lagged total bond market capitalization using CRSP bond data (1926–2024).

2. **PS2_Q2 – Combine Stocks, Bonds, and Risk-Free Data**

   * Merge CRSP stock, bond, and Treasury (riskless) datasets.
   * Compute excess value-weighted returns and lagged market values for stocks and bonds.

3. **PS2_Q3 – Build Risk-Parity Portfolios**

   * Compute unlevered and levered risk-parity (RP) portfolio returns using inverse volatility weighting.
   * Leverage the unlevered RP portfolio to match the volatility of the value-weighted market portfolio.

4. **PS2_Q4 – Replicate Table 2 (Panel A) from Asness et al. (2012)**

   * Replicate the performance table reporting annualized mean returns, volatility, Sharpe ratios, skewness, and excess kurtosis for:

     * CRSP Stocks
     * CRSP Bonds
     * Value-Weighted Market Portfolio
     * 60/40 Stock-Bond Portfolio
     * Unlevered RP Portfolio
     * Levered RP Portfolio

---

## Methodology

The implementation followed the empirical approach described in Appendix A of Asness, Frazzini, and Pedersen (2012).
Each function corresponds to one of the problem set’s tasks and produces intermediate outputs for verification.

| Function   | Description                                                                                       | Output                    |
| ---------- | ------------------------------------------------------------------------------------------------- | ------------------------- |
| `PS2_Q1()` | Computes monthly equal-weighted and value-weighted bond returns with lagged market capitalization | `PS2_Q1.csv`              |
| `PS2_Q2()` | Combines stock, bond, and T-bill datasets to calculate monthly excess returns                     | `PS2_Q2_output.csv`       |
| `PS2_Q3()` | Calculates risk-parity portfolio returns (unlevered and levered) and 60/40 benchmark              | DataFrame with 12 columns |
| `PS2_Q4()` | Produces a 6×6 table of performance statistics                                                    | Summary table of results  |

All data were accessed directly from **WRDS/CRSP** using the Python API (`wrds.Connection()`).

---

## Results Summary

The replication results closely matched those reported in Asness et al. (2012).
Below is a summary of the computed portfolio performance metrics:

| Portfolio                | Annualized Mean | Volatility | Sharpe Ratio | Skewness | Excess Kurtosis |
| ------------------------ | --------------: | ---------: | -----------: | -------: | --------------: |
| CRSP Stocks              |           6.75% |      19.1% |         0.35 |     0.23 |            7.64 |
| CRSP Bonds               |           1.39% |       2.8% |         0.50 |     0.21 |            4.09 |
| Value-Weighted Portfolio |           6.73% |      19.1% |         0.35 |     0.23 |            7.63 |
| 60/40 Portfolio          |           4.60% |      11.6% |         0.40 |     0.24 |            7.40 |
| Unlevered RP             |           2.10% |       3.5% |         0.60 |     0.11 |            2.68 |
| Levered RP               |           12.2% |      18.6% |         0.66 |     0.02 |            5.66 |

Differences between the replicated and published values were minor and **economically negligible**, confirming the accuracy of the methodology.

---

## Key Insights

* The **risk-parity portfolio** achieves a higher **Sharpe ratio** than traditional 60/40 or value-weighted portfolios.
* **Leverage aversion** explains why risk-parity portfolios outperform on a risk-adjusted basis.
* The replication validates the original findings of Asness et al. (2012) using independent CRSP and WRDS data.
* Demonstrates application of **financial econometrics**, **portfolio theory**, and **Python-based data analysis** in asset management research.

---

## Tools and Libraries

* Python 3.10+
* Pandas, NumPy
* SciPy (for skewness and kurtosis)
* WRDS API (for direct data access)
* Matplotlib / JupyterLab (for visualization and analysis)

---

## File Outputs

| Output File          | Description                                                                          |
| -------------------- | ------------------------------------------------------------------------------------ |
| `PS2_Q1.csv`         | Bond market aggregated returns (equal-weighted, value-weighted, lagged market value) |
| `PS2_Q2_output.csv`  | Combined stock, bond, and risk-free monthly excess returns                           |
| `PS2_Q3_output.csv`  | Portfolio returns for unlevered and levered risk-parity portfolios                   |
| `PS2_Q4_results.csv` | Summary statistics and replication table                                             |

---

## References

* Asness, C. S., Frazzini, A., & Pedersen, L. H. (2012). *Leverage Aversion and Risk Parity.* Financial Analysts Journal, 68(1).
* UCLA Anderson School of Management – MGMTMFE 431: Quantitative Asset Management, Spring 2025.

---

## Author

**Vikalp Thukral**
MFE Candidate, UCLA Anderson School of Management
Email: [vikalp.thukral@anderson.ucla.edu](mailto:vikalp.thukral@anderson.ucla.edu)
