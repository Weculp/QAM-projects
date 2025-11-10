# Market Portfolio Construction (MFE_PS1)

## Overview

This repository contains the implementation for **Market Portfolio Construction**, a problem set from *Quantitative Asset Management (MGMTMFE 431)* at UCLA Anderson School of Management.

The objective is to replicate the **Fama–French Market Portfolio** using CRSP data by constructing both **value-weighted** and **equal-weighted** market returns and comparing them with the official Fama–French market excess return series.

---

## Problem Statement – `MFE_PS1.pdf`

The problem statement outlines three main tasks:

1. **Market Return Construction**

   * Build monthly value-weighted and equal-weighted returns from CRSP data (1926–2024).
   * Include delisting returns and compute lagged market capitalization.
   * Restrict the sample to common stocks traded on NYSE, AMEX, and NASDAQ.

2. **Summary Statistics Comparison**

   * Compare CRSP-based market excess returns to the Fama–French market excess return.
   * Compute annualized mean, volatility, Sharpe ratio, skewness, and excess kurtosis.

3. **Replication Accuracy Assessment**

   * Calculate the correlation and maximum absolute difference between the two series.
   * Analyze the economic significance of any observed deviations.

---

## Solution – `PS1_406534669.pdf`

This file provides the full **Python (Jupyter Notebook)** implementation for all tasks described in the problem statement.

Key components:

* **Data Preprocessing:** Cleaning CRSP monthly data, converting data types, and filtering securities.
* **Return Construction:**

  * Combine `RET` and `DLRET` to compute full cumulative returns.
  * Generate lagged market capitalization to avoid look-ahead bias.
* **Aggregation:**

  * Calculate equal-weighted and value-weighted market returns.
* **Statistical Analysis:**

  * Compare CRSP and Fama–French series using correlation and difference metrics.
  * Achieved correlation of **0.999992**, confirming high replication accuracy.

---

## Explanation – `WRD_PS1_406534669v2.pdf`

This document explains the workflow, rationale, and validation process used in the Python implementation.
It provides:

* Step-by-step explanation of the methodology.
* Discussion of assumptions and data limitations.
* Interpretation of results confirming close alignment with the Fama–French benchmark.

