import pandas as pd
import numpy as np
from pandas.tseries.offsets import MonthEnd

def PS2_Q1(CRSP_Bonds):
    """
    Constructs Equal-Weighted Return, Value-Weighted Return,
    and Lagged Total Bond Market Capitalization (in millions) with Year and Month columns.

    Inputs:
    - CRSP_Bonds: DataFrame with columns ['KYCRSPID', 'MCALDT', 'TMRETNUA', 'TMTOTOUT']

    Outputs:
    - DataFrame with columns ['Year', 'Month', 'Bond_lag_MV', 'Bond_Ew_Ret', 'Bond_Vw_Ret']
    """

    """Adjust 'mcaldt' to month-end and rename columns"""
    CRSP_Bonds['MCALDT'] = pd.to_datetime(CRSP_Bonds['MCALDT']) + MonthEnd(0)
    CRSP_Bonds = CRSP_Bonds.rename(columns={
        'KYCRSPID': 'idCRSP',
        'MCALDT': 'date',
        'TMRETNUA': 'ret',
        'TMTOTOUT': 'me'
    }).copy()
    
    """Filter the sample period"""
    CRSP_Bonds = CRSP_Bonds.loc[
        (CRSP_Bonds['date'] >= '1926-01-31') & (CRSP_Bonds['date'] <= '2024-12-31')
    ].copy()
    
    """Drop rows with missing returns or market cap"""
    CRSP_Bonds = CRSP_Bonds.dropna(subset=['ret', 'me'])
    
    """Group by month"""
    grouped = CRSP_Bonds.groupby('date')
    
    """Calculate Equal-weighted return"""
    equal_weighted_return = grouped['ret'].mean()
    
    """Calculate Value-weighted return"""
    value_weighted_return = grouped.apply(lambda x: np.average(x['ret'], weights=x['me']))
    
    """Calculate total market capitalization"""
    total_market_cap = grouped['me'].sum()
    
    """Lagged total market cap and scale to millions"""
    lagged_total_market_cap = total_market_cap.shift(1) / 1_000_000

    """Create the result DataFrame"""
    result = pd.DataFrame({
        'Bond_Ew_Ret': equal_weighted_return,
        'Bond_Vw_Ret': value_weighted_return,
        'Bond_lag_MV': lagged_total_market_cap
    })
    
    """Add Year and Month columns from the index (date)"""
    result['Year'] = result.index.year
    result['Month'] = result.index.month

    """Reorder columns to put Year and Month first"""
    result = result[['Year', 'Month', 'Bond_lag_MV', 'Bond_Ew_Ret', 'Bond_Vw_Ret']]

    return result

import pandas as pd

def PS2_Q2(Monthly_CRSP_Stocks, Monthly_CRSP_Bonds, Monthly_CRSP_Riskless):
    """
    Constructs the final PS2_Q2 DataFrame by aggregating lagged market values and excess returns
    for stocks and bonds from January 1926 to December 2024.

    Inputs:
    - Monthly_CRSP_Stocks: DataFrame with columns ['Year', 'Month', 'Stock lag MV', 'Stock Ew Ret', 'Stock Vw Ret']
    - Monthly_CRSP_Bonds: DataFrame output from PS2_Q1 with columns ['Year', 'Month', 'Bond_lag_MV', 'Bond_Ew_Ret', 'Bond_Vw_Ret']
    - Monthly_CRSP_Riskless: DataFrame with risk-free rates (columns ['caldt', 't90ret', 't30ret'])

    Output:
    - DataFrame with columns:
      ['Year', 'Month', 'Stock_lag_MV', 'Stock_Excess_Vw_Ret', 'Bond_lag_MV', 'Bond_Excess_Vw_Ret']
    """

    """
    Step 1: Prepare Risk-Free Rate
    Convert 'caldt' to datetime, and use 't30ret' as the 1-month risk-free rate.
    """
    Monthly_CRSP_Riskless['caldt'] = pd.to_datetime(Monthly_CRSP_Riskless['caldt'])
    Monthly_CRSP_Riskless['Year'] = Monthly_CRSP_Riskless['caldt'].dt.year
    Monthly_CRSP_Riskless['Month'] = Monthly_CRSP_Riskless['caldt'].dt.month
    riskless = Monthly_CRSP_Riskless[['Year', 'Month', 't30ret']].copy()

    """
    Step 2: Prepare Stock Data
    Merge stock returns with risk-free rate and compute excess returns.
    """
    df_stocks = Monthly_CRSP_Stocks.copy()
    df_stocks = df_stocks.merge(riskless, on=['Year', 'Month'], how='left')
    df_stocks['Stock_Excess_Vw_Ret'] = df_stocks['Stock_Vw_Ret'] - df_stocks['t30ret']
    df_stocks["Stock_lag_MV"] = df_stocks["Stock_lag_MV"] 

    """
    Step 3: Prepare Bond Data
    Merge bond returns with risk-free rate and compute excess returns.
    """
    df_bonds = Monthly_CRSP_Bonds.copy()
    df_bonds = df_bonds.merge(riskless, on=['Year', 'Month'], how='left')
    df_bonds['Bond_Excess_Vw_Ret'] = df_bonds['Bond_Vw_Ret'] - df_bonds['t30ret']

    """
    Step 4: Merge Stock and Bond Information
    Merge processed stock and bond datasets on Year and Month.
    """
    final = df_stocks[['Year', 'Month', 'Stock_lag_MV', 'Stock_Excess_Vw_Ret']].merge(
        df_bonds[['Year', 'Month', 'Bond_lag_MV', 'Bond_Excess_Vw_Ret']],
        on=['Year', 'Month'],
        how='outer'
    )

    return final

def PS2_Q3(Monthly_CRSP_Universe):
    """
    Constructs unlevered and levered Risk-Parity (RP) portfolio returns 
    based on Monthly_CRSP_Universe (the output from PS2_Q2).

    Inputs:
    - Monthly_CRSP_Universe: DataFrame with columns:
      ['Year', 'Month', 'Stock_lag_MV', 'Stock_Excess_Vw_Ret', 'Bond_lag_MV', 'Bond_Excess_Vw_Ret']

    Outputs:
    - DataFrame with columns:
      ['Year', 'Month', 'Stock_Excess_Vw_Ret', 'Bond_Excess_Vw_Ret',
       'Excess_Vw_Ret', 'Excess_60_40_Ret',
       'Stock_inverse_sigma_hat', 'Bond_inverse_sigma_hat',
       'Unlevered_k', 'Excess_Unlevered_RP_Ret',
       'Levered_k', 'Excess_Levered_RP_Ret']
    """

    """
    Compute rolling volatilities (σ̂) using a 36-month window
    """
    Monthly_CRSP_Universe = Monthly_CRSP_Universe.copy()
    Monthly_CRSP_Universe['Stock_inverse_sigma_hat'] = 1 / Monthly_CRSP_Universe['Stock_Excess_Vw_Ret'].rolling(36).std()
    Monthly_CRSP_Universe['Bond_inverse_sigma_hat'] = 1 / Monthly_CRSP_Universe['Bond_Excess_Vw_Ret'].rolling(36).std()

    """
    Compute value-weighted portfolio returns (excess) and 60/40 portfolio returns (excess)
    """
    vw_excess_ret = (Monthly_CRSP_Universe['Stock_lag_MV'] * Monthly_CRSP_Universe['Stock_Excess_Vw_Ret'] +
                     Monthly_CRSP_Universe['Bond_lag_MV'] * Monthly_CRSP_Universe['Bond_Excess_Vw_Ret']) / \
                    (Monthly_CRSP_Universe['Stock_lag_MV'] + Monthly_CRSP_Universe['Bond_lag_MV'])
    Monthly_CRSP_Universe['Excess_Vw_Ret'] = vw_excess_ret

    Monthly_CRSP_Universe['Excess_60_40_Ret'] = 0.6 * Monthly_CRSP_Universe['Stock_Excess_Vw_Ret'] + \
                                                0.4 * Monthly_CRSP_Universe['Bond_Excess_Vw_Ret']

    """
    Compute unlevered RP portfolio returns
    """
    inverse_vol_sum = Monthly_CRSP_Universe['Stock_inverse_sigma_hat'] + Monthly_CRSP_Universe['Bond_inverse_sigma_hat']
    Monthly_CRSP_Universe['Unlevered_k'] = 1 / inverse_vol_sum

    Monthly_CRSP_Universe['Excess_Unlevered_RP_Ret'] = Monthly_CRSP_Universe['Unlevered_k'] * (
        Monthly_CRSP_Universe['Stock_inverse_sigma_hat'] * Monthly_CRSP_Universe['Stock_Excess_Vw_Ret'] +
        Monthly_CRSP_Universe['Bond_inverse_sigma_hat'] * Monthly_CRSP_Universe['Bond_Excess_Vw_Ret']
    )

    """
    Compute levered RP portfolio returns (leveraged to match Vw portfolio σ̂)
    """
    vol_Vw = Monthly_CRSP_Universe['Excess_Vw_Ret'].rolling(36).std()
    vol_RP = Monthly_CRSP_Universe['Excess_Unlevered_RP_Ret'].rolling(36).std()
    Monthly_CRSP_Universe['Levered_k'] = vol_Vw / vol_RP

    Monthly_CRSP_Universe['Excess_Levered_RP_Ret'] = Monthly_CRSP_Universe['Levered_k'] * Monthly_CRSP_Universe['Excess_Unlevered_RP_Ret']

    """
    Final output dataframe
    """
    result = Monthly_CRSP_Universe[[
        'Year', 'Month',
        'Stock_Excess_Vw_Ret', 'Bond_Excess_Vw_Ret',
        'Excess_Vw_Ret', 'Excess_60_40_Ret',
        'Stock_inverse_sigma_hat', 'Bond_inverse_sigma_hat',
        'Unlevered_k', 'Excess_Unlevered_RP_Ret',
        'Levered_k', 'Excess_Levered_RP_Ret'
    ]].copy()

    return result

import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis

def PS2_Q4(Port_Rets):
    """
    Computes performance statistics for different portfolios from January 1929 to June 2010.

    Inputs:
    - Port_Rets: DataFrame, the output from PS2_Q3 containing portfolio excess returns.

    Outputs:
    - stats_table: DataFrame, a 6 × 6 table reporting Annualized Mean, t-statistic of Annualized Mean,
      Annualized Standard Deviation, Annualized Sharpe Ratio, Skewness, and Excess Kurtosis.
    """

    """Restrict the sample"""
    Port_Rets = Port_Rets.copy()
    Port_Rets['date'] = pd.to_datetime(Port_Rets['Year'].astype(str) + '-' + Port_Rets['Month'].astype(str)) + pd.offsets.MonthEnd(0)
    Port_Rets = Port_Rets[(Port_Rets['date'] >= '1929-01-31') & (Port_Rets['date'] <= '2010-06-30')]

    """Identify the portfolio columns"""
    port_cols = {
        'Stock_Excess_Vw_Ret': 'CRSP stocks',
        'Bond_Excess_Vw_Ret': 'CRSP bonds',
        'Excess_Vw_Ret': 'Value-weighted portfolio',
        'Excess_60_40_Ret': '60/40 portfolio',
        'Excess_Unlevered_RP_Ret': 'Unlevered RP',
        'Excess_Levered_RP_Ret': 'Levered RP'
    }

    """Initialize dictionary to store results"""
    results = {}

    """Calculate metrics for each portfolio"""
    for col, name in port_cols.items():
        rets = Port_Rets[col].dropna()
        n = len(rets)

        ann_mean = 12 * rets.mean()
        ann_vol = np.sqrt(12) * rets.std()
        t_stat = ann_mean / (rets.std() / np.sqrt(n))
        sharpe = ann_mean / ann_vol
        skewness = skew(rets)
        ex_kurt = kurtosis(rets)  # Already excess kurtosis

        results[name] = [
            ann_mean,
            t_stat,
            ann_vol,
            sharpe,
            skewness,
            ex_kurt
        ]

    """Create final DataFrame"""
    stats_table = pd.DataFrame(results).T

    stats_table.columns = [
        'Annualized Mean', 
        't-stat of Annualized Mean',
        'Annualized Standard Deviation',
        'Annualized Sharpe Ratio',
        'Skewness',
        'Excess Kurtosis'
    ]

    return stats_table

