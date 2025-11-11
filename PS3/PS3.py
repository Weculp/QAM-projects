def compute_ranking_return(group):
    group = group.sort_values('date')
    rolling_ret = (
        (1 + group['RET'].fillna(0)).shift(2).rolling(window=11)
        .apply(np.prod, raw=True) - 1
    )
    group['Ranking_Ret'] = rolling_ret
    return group


def PS3_Q1(df):
    int_columns = [
    'PERMNO',
    'SHRCD',
    'EXCHCD',
    'RET',
    'DLRET',
    'PRC',
    'SHROUT'
    ]
    df[int_columns] = df[int_columns].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    
    df['Year'] = df['date'].dt.year
    df['Month'] = df['date'].dt.month
    
    df = df[df['SHRCD'].isin([10, 11])]
    df = df[df['EXCHCD'].isin([1, 2, 3])]
    df = df.sort_values(['PERMNO', 'date'])
    
    df['RET_FULL'] = (1 + df['RET'].fillna(0)) * (1 + df['DLRET'].fillna(0)) - 1
    df['MC'] = df['PRC'].abs() * df['SHROUT']
    df['lag_Mkt_Cap'] = df.groupby('PERMNO')['MC'].shift(1)
    
    df = df.groupby('PERMNO').apply(compute_ranking_return)
    df = df.reset_index(drop=True)
    
    df = df.rename(columns={'RET_FULL': 'Ret'})
    df = df[['Year', 'Month', 'PERMNO', 'EXCHCD', 'lag_Mkt_Cap', 'Ret', 'Ranking_Ret']]
    df['lag_Mkt_Cap'] = df['lag_Mkt_Cap'] / 1e6
    df = df.dropna(subset=['Ranking_Ret'])
    df = df[(df['Year'] >= 1927) & (df['Year'] <= 2024)]
    return df
    

import pandas as pd
import numpy as np

def PS3_Q2(df):
    """
    Calculates monthly deciles for stocks based on their 'Ranking_Ret'.

    The function computes two types of deciles: 'DM_decile' and 'KRF_decile'.
    It processes the input DataFrame month by month.

    - 'DM_decile': Stocks are sorted into 10 deciles based on their 'Ranking_Ret'
      within the full universe of stocks for that specific month.
    - 'KRF_decile': Decile breakpoints are determined using 'Ranking_Ret' from
      NYSE-listed stocks (EXCHCD == 1) only for that month. These NYSE-based
      breakpoints are then used to assign all stocks (NYSE, AMEX, NASDAQ)
      in that month to one of the 10 deciles. If there are fewer than 10
      NYSE stocks in a given month, 'KRF_decile' will be NaN for all stocks
      in that month.

    Parameters:
    ----------
    df : pd.DataFrame
        Input DataFrame containing stock data. Must include the following columns:
        - 'Ranking_Ret': The variable used for ranking (e.g., past returns).
        - 'EXCHCD': Exchange code (1 for NYSE, 2 for AMEX, 3 for NASDAQ).
        - 'Year': The year of the observation.
        - 'Month': The month of the observation.
        Other columns (e.g., stock identifiers like 'PERMNO') will be preserved.

    Returns:
    -------
    pd.DataFrame
        The original DataFrame with two additional columns:
        - 'DM_decile': Integer decile (1-10) based on full universe sort. NaN if undecidable.
        - 'KRF_decile': Integer decile (1-10) based on NYSE breakpoints. NaN if undecidable.
        Both decile columns are of type 'Int64' (supports pd.NA).
    """
    working_df = df.copy()

    def assign_deciles_to_group(monthly_group_df):
        """
        Assigns DM_decile and KRF_decile to the given monthly group of stocks.
        """
        try:
            monthly_group_df['DM_decile'] = pd.qcut(monthly_group_df['Ranking_Ret'], 10, labels=False, duplicates='drop') + 1
        except ValueError:
            monthly_group_df['DM_decile'] = np.nan

        nyse_stocks_in_group_df = monthly_group_df[monthly_group_df['EXCHCD'] == 1]

        if nyse_stocks_in_group_df.shape[0] >= 10:
            try:
                krf_decile_breakpoints = pd.qcut(nyse_stocks_in_group_df['Ranking_Ret'], 10, retbins=True, duplicates='drop')[1]
                monthly_group_df['KRF_decile'] = pd.cut(monthly_group_df['Ranking_Ret'], bins=krf_decile_breakpoints, labels=False, include_lowest=True) + 1
            except ValueError:
                monthly_group_df['KRF_decile'] = np.nan
        else:
            monthly_group_df['KRF_decile'] = np.nan
            
        return monthly_group_df

    working_df = working_df.groupby(['Year', 'Month'], group_keys=False).apply(assign_deciles_to_group)

    working_df['DM_decile'] = working_df['DM_decile'].astype('Int64')
    working_df['KRF_decile'] = working_df['KRF_decile'].astype('Int64')

    return working_df


def PS3_Q3(CRSP_Stocks_Momentum_decile, ff):
    import pandas as pd

    CRSP_Stocks_Momentum_decile = CRSP_Stocks_Momentum_decile.copy()
    ff = ff.copy()

    # Ensure proper dtypes
    CRSP_Stocks_Momentum_decile[['DM_decile', 'KRF_decile']] = CRSP_Stocks_Momentum_decile[['DM_decile', 'KRF_decile']].astype('Int64')

    # Value weight
    CRSP_Stocks_Momentum_decile['weight'] = CRSP_Stocks_Momentum_decile['lag_Mkt_Cap']

    # Function to compute decile returns
    def compute_returns(group, decile_col, ret_col):
        returns = group.groupby(['Year', 'Month', decile_col]).apply(
            lambda x: (x['Ret'] * x['weight']).sum() / x['weight'].sum()
        ).reset_index(name=ret_col)
        return returns

    # DM returns
    dm_ret = compute_returns(CRSP_Stocks_Momentum_decile, 'DM_decile', 'DM_Ret')
    dm_ret = dm_ret.rename(columns={'DM_decile': 'decile'})

    # KRF returns
    krf_ret = compute_returns(CRSP_Stocks_Momentum_decile, 'KRF_decile', 'KRF_Ret')
    krf_ret = krf_ret.rename(columns={'KRF_decile': 'decile'})

    # Merge
    merged = pd.merge(dm_ret, krf_ret, on=['Year', 'Month', 'decile'], how='outer')

    # Merge with Rf
    out = pd.merge(merged, ff[['Year', 'Month', 'Rf']], on=['Year', 'Month'], how='left')
    out = out.sort_values(['Year', 'Month', 'decile']).reset_index(drop=True)
    return out


import pandas as pd
import numpy as np
from scipy.stats import skew

def PS3_Q4(crsp_df: pd.DataFrame, dm_df: pd.DataFrame) -> pd.DataFrame:
    """
    Replicates part of Table 1 from Daniel & Moskowitz (2016), computing summary stats for DM deciles and WML.

    Parameters:
    - crsp_df: DataFrame with CRSP-based returns. Must include ['Year', 'Month', 'decile', 'DM_Ret', 'Rf'].
    - dm_df: DataFrame with Daniel-Moskowitz benchmark returns. Same format.

    Returns:
    - DataFrame with rows for mean excess return, volatility, Sharpe ratio, skewness, and correlation with DM.
    """
    # Filter for overlapping period
    crsp_df = crsp_df[(crsp_df['Year'] >= 1927) & (crsp_df['Year'] <= 2016)]

    # Merge for correlation
    merged = pd.merge(crsp_df, dm_df, on=['Year', 'Month', 'decile'], suffixes=('', '_DM'))

    stats = {
        'Mean Excess Return': [],
        'Volatility': [],
        'Sharpe Ratio': [],
        'Skewness': [],
        'Corr with DM': []
    }

    result_columns = []

    for d in range(1, 11):  # Deciles 1 to 10
        df_d = merged[merged['decile'] == d]
        ret = df_d['DM_Ret']
        rf = df_d['Rf']
        dm_ret = df_d['DM_Ret_DM']

        ex_ret = ret - rf
        stats['Mean Excess Return'].append(ex_ret.mean() * 12)
        stats['Volatility'].append(ex_ret.std() * np.sqrt(12))
        stats['Sharpe Ratio'].append((ex_ret.mean() / ex_ret.std()) * np.sqrt(12))
        stats['Skewness'].append(skew(np.log1p(ret)))
        stats['Corr with DM'].append(np.corrcoef(ret, dm_ret)[0, 1])
        result_columns.append(f'Decile {d}')

    # WML: Decile 10 - Decile 1
    wml_df = pd.merge(
        crsp_df[crsp_df['decile'] == 10],
        crsp_df[crsp_df['decile'] == 1],
        on=['Year', 'Month'],
        suffixes=('_10', '_1')
    )
    wml_ret = wml_df['DM_Ret_10'] - wml_df['DM_Ret_1']
    wml_rf = wml_df['Rf_10']

    ex_ret_wml = wml_ret - wml_rf
    dm_wml = dm_df[dm_df['decile'] == 10].merge(
        dm_df[dm_df['decile'] == 1], on=['Year', 'Month'], suffixes=('_10', '_1'))
    dm_wml_ret = dm_wml['DM_Ret_10'] - dm_wml['DM_Ret_1']

    stats['Mean Excess Return'].append(ex_ret_wml.mean() * 12)
    stats['Volatility'].append(ex_ret_wml.std() * np.sqrt(12))
    stats['Sharpe Ratio'].append((ex_ret_wml.mean() / ex_ret_wml.std()) * np.sqrt(12))
    stats['Skewness'].append(skew(np.log1p(wml_ret + wml_rf)))
    stats['Corr with DM'].append(np.corrcoef(wml_ret, dm_wml_ret)[0, 1])
    result_columns.append("WML")

    # Create final dataframe
    summary_df = pd.DataFrame(stats, index=result_columns).T
    return summary_df


import pandas as pd
import numpy as np
from scipy.stats import skew

def PS3_Q5(crsp_df: pd.DataFrame, krf_df: pd.DataFrame) -> pd.DataFrame:
    """
    Replicates part of Table 1 from Daniel & Moskowitz (2016), using KRF_Ret and comparing with Kenneth French's KRF benchmark.

    Parameters:
    - crsp_df: DataFrame with CRSP-based KRF decile returns. Must include ['Year', 'Month', 'decile', 'KRF_Ret', 'Rf'].
    - krf_df: DataFrame with benchmark KRF returns from Kenneth French. Must include ['Year', 'Month', 'decile', 'KRF_Ret'].

    Returns:
    - DataFrame with rows for mean excess return, volatility, Sharpe ratio, skewness, and correlation with KRF benchmark.
    """

    # Filter for the common period
    crsp_df = crsp_df[(crsp_df['Year'] >= 1927) & (crsp_df['Year'] <= 2016)]

    # Merge for correlation purposes
    merged = pd.merge(crsp_df, krf_df, on=['Year', 'Month', 'decile'], suffixes=('', '_KRF'))

    stats = {
        'Mean Excess Return': [],
        'Volatility': [],
        'Sharpe Ratio': [],
        'Skewness': [],
        'Corr with KRF': []
    }

    result_columns = []

    for d in range(1, 11):
        df_d = merged[merged['decile'] == d]
        ret = df_d['KRF_Ret']
        rf = df_d['Rf']
        krf_bench = df_d['KRF_Ret_KRF']

        ex_ret = ret - rf
        stats['Mean Excess Return'].append(ex_ret.mean() * 12)
        stats['Volatility'].append(ex_ret.std() * np.sqrt(12))
        stats['Sharpe Ratio'].append((ex_ret.mean() / ex_ret.std()) * np.sqrt(12))
        stats['Skewness'].append(skew(np.log1p(ret)))
        stats['Corr with KRF'].append(np.corrcoef(ret, krf_bench)[0, 1])
        result_columns.append(f'Decile {d}')

    # WML: Decile 10 - Decile 1
    wml_df = pd.merge(
        crsp_df[crsp_df['decile'] == 10],
        crsp_df[crsp_df['decile'] == 1],
        on=['Year', 'Month'],
        suffixes=('_10', '_1')
    )
    wml_ret = wml_df['KRF_Ret_10'] - wml_df['KRF_Ret_1']
    wml_rf = wml_df['Rf_10']

    ex_ret_wml = wml_ret - wml_rf
    krf_wml = krf_df[krf_df['decile'] == 10].merge(
        krf_df[krf_df['decile'] == 1],
        on=['Year', 'Month'],
        suffixes=('_10', '_1')
    )
    krf_wml_ret = krf_wml['KRF_Ret_10'] - krf_wml['KRF_Ret_1']

    stats['Mean Excess Return'].append(ex_ret_wml.mean() * 12)
    stats['Volatility'].append(ex_ret_wml.std() * np.sqrt(12))
    stats['Sharpe Ratio'].append((ex_ret_wml.mean() / ex_ret_wml.std()) * np.sqrt(12))
    stats['Skewness'].append(skew(np.log1p(wml_ret)))
    stats['Corr with KRF'].append(np.corrcoef(wml_ret, krf_wml_ret)[0, 1])
    result_columns.append("WML")

    summary_df = pd.DataFrame(stats, index=result_columns).T
    return summary_df
