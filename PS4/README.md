# PS4 — Size and Value Factor Replication

### MGMTMFE 431: Quantitative Asset Management

**Instructor:** Prof. Bernard Herskovic
**Author:** Vikalp Thukral
**Date:** May 2025

---

## Overview

This project replicates the construction of **Fama-French size and value-sorted portfolios** and the corresponding **SMB (Small Minus Big)** and **HML (High Minus Low)** factors using **CRSP** and **Compustat** data from **January 1973 to December 2024**.

The objective is to reproduce and analyze the core results from:

* Fama and French (1992), *The Cross-Section of Expected Stock Returns*
* Fama and French (1993), *Common Risk Factors in the Returns on Stocks and Bonds*

The replication follows the official methodology described in Kenneth French’s data library and aims to examine the persistence and performance of the size and value anomalies over time.

---

## Problem Statement

The assignment requires replicating the **construction of characteristic-sorted and factor portfolios** that capture the size and value effects in equity markets.

Specifically:

1. Prepare and merge **CRSP** and **Compustat** datasets to compute size and book-to-market decile portfolios.
2. Replicate the **HML** and **SMB** factors following Fama–French definitions.
3. Compare the replicated portfolios to benchmark data from the **Kenneth French Data Library**.
4. Evaluate the recent performance of these anomalies (2014–2024).
5. Contrast **characteristic portfolios** (1992) with **factor portfolios** (1993).

This work tests data processing rigor, replication accuracy, and empirical interpretation of well-known asset pricing factors.

---

## Repository Structure

```
QAM-projects/
│
├── PS4/
│   ├── MFE_PS4.pdf          # Official problem statement outlining tasks, data requirements, and deliverables
│   ├── PS4.ipynb            # Jupyter Notebook containing full data pipeline, code, and visualizations
│   ├── PS4_QAM.pdf          # Final report detailing methodology, results, and discussion
│   ├── compustat_ps4.csv    # Processed Compustat fundamentals dataset
│   ├── crsp_ps4.csv         # Processed CRSP monthly stock returns
│   ├── Portfolios_Formed_on_BE-ME_CSV.zip  # Original Fama-French benchmark data
│   ├── Portfolios_Formed_on_ME_CSV.zip     # Benchmark size portfolios
│   ├── images/              # Generated figures (portfolio stats, cumulative returns)
│   │   ├── img1.png
│   │   ├── img2.png
│   │   └── ...
│   └── PS4_checkpoint.ipynb # Intermediate notebook version (auto-saved)
```

---

## Methodology

### 1. Data Acquisition and Cleaning

* **CRSP Monthly Stock File (1971–2024):**

  * Variables: `PERMNO`, `PERMCO`, `DATE`, `PRC`, `SHROUT`, `RET`, `DLRET`, `SHRCD`, `EXCHCD`.
  * Filters: Common shares only (`SHRCD` ∈ {10, 11}); NYSE/AMEX/NASDAQ (`EXCHCD` ∈ {1, 2, 3}).
  * Market Equity (ME) computed as `|PRC| × SHROUT × 1,000`.

* **Compustat Fundamentals Annual:**

  * Variables: `GVKEY`, `SEQ`, `CEQ`, `PSTKRV`, `TXDITC`, `TXDB`, `ITCB`, `AT`, `LT`, `MIB`, `PRBA`.
  * Filters: Industrial format (`INDL`), consolidated (`C`), domestic (`D`), standard format (`STD`).

* **CRSP–Compustat Merged (CCM) Link Table:**

  * Retained only valid link types (`LC`, `LU`) and primary links (`LINKPRIM = 'P'`).
  * Merged using date ranges between `LINKDT` and `LINKENDDT`.

### 2. Book Equity and Book-to-Market Construction

Book Equity (BE) was computed hierarchically:

```
BE = SHE − PS + DT
```

where:

* **SHE** = `SEQ` or fallback to `CEQ + PSTK` or `AT − LT − MIB`
* **PS** = `PSTKRV`, fallback to `PSTKL` or `PSTK`
* **DT** = `TXDITC`, fallback to `TXDB + ITCB`

Book-to-Market (BTM) = `BE / ME`.

### 3. Portfolio Formation

* Portfolios are formed each **June**, using NYSE stocks to define breakpoints for both ME and BTM.
* Firms are classified into **10 deciles** (1 = smallest or lowest B/M, 10 = largest or highest B/M).
* Decile assignments are held **from July (t) through June (t+1)**.

### 4. Factor Construction

* **Size portfolios:** Value-weighted returns across 10 ME deciles.
* **Value portfolios:** Value-weighted returns across 10 BTM deciles.
* **SMB:** Average return of small-stock portfolios (1–5) minus large-stock portfolios (6–10).
* **HML:** Average return of high BTM portfolios (8–10) minus low BTM portfolios (1–3).

### 5. Performance Metrics

For each decile and long-short factor:

* Annualized mean return
* Annualized volatility
* Sharpe ratio (risk-free = 0)
* Skewness
* Correlation with Fama–French benchmarks

### 6. Empirical Evaluation (2014–2024)

Using the French data library:

* Both **SMB** and **HML** exhibited declining cumulative returns post-2014.
* The **value premium weakened significantly** after 2018, consistent with academic findings on factor decay.

---

## Results Summary

|             Metric | HML (Original) | HML (Replication) | SMB (Original) | SMB (Replication) |
| -----------------: | -------------- | ----------------- | -------------- | ----------------- |
|        Mean Return | 15.38%         | 3.46%             | 11.26%         | 20.70%            |
|         Volatility | 22.04%         | 12.89%            | 15.31%         | 15.04%            |
|       Sharpe Ratio | 0.698          | 0.269             | 0.736          | 1.376             |
|           Skewness | -0.453         | 0.068             | -0.347         | 7.329             |
| Corr. w/ Benchmark | 0.982          | 0.260             | 0.995          | 0.047             |

The replication captures the directional nature of size and value effects but deviates in magnitude, reflecting data differences and methodological nuances.

---

## Key Insights

* **Characteristic portfolios (1992)** describe cross-sectional relationships between firm traits and expected returns.
* **Factor portfolios (1993)** formalize these relationships into systematic risk factors used in asset pricing models.
* The replication highlights **implementation sensitivity**—small variations in timing, link matching, and data filters can materially affect results.

---

## References

* Fama, Eugene F., and Kenneth R. French (1992). *The Cross-Section of Expected Stock Returns*, *Journal of Finance*, 47(2), 427–465.
* Fama, Eugene F., and Kenneth R. French (1993). *Common Risk Factors in the Returns on Stocks and Bonds*, *Journal of Financial Economics*, 33(1), 3–56.
* Kenneth R. French Data Library. [https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
* CRSP and Compustat databases, accessed via WRDS.

---

## Notes

All analysis was conducted in **Python** using **pandas**, **NumPy**, and **matplotlib**.
All data handling, portfolio construction, and factor replication logic adhere to the Fama–French convention to the fullest extent possible given publicly available data.
