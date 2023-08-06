import numpy as np
import pandas as pd
import bluebelt.statistics.constants as constants

from bluebelt.core.exceptions import *

def std_within(df, how=None, **kwargs):
    """
    Calculate the standard deviation within subgroups
    arguments:
    df:         Pandas Dataframe
    columns:    list of colums; if not provided all columns will be treated as subgroups
    how:        the method of estimating std_within

                options when subgroup size == 1:
                - 'amr' or 'average_moving_range' (default)
                    optional argument: observations=2
                - 'mmr' or 'median_moving_range'
                - 'mssd' or 'sqrt_of_mssd'
                
                options when subgroup size > 1:
                - 'pooled_std' (default)
                - 'Rbar'
                - 'Sbar'
    """


    # check subgroup size
    # if df is a pandas Series just pass it to amr, mmr or mssd
    if isinstance(df, pd.Series) or df.shape[0] == 1:
        if how in ['mssd', 'sqrt_of_mssd']:
            return sqrt_of_mssd(series=df, **kwargs)
        elif how in ['mmr', 'median_moving_range']:
            return median_moving_range(series=df, **kwargs)
        else:
            return average_moving_range(series=df, **kwargs)
    
    else:
        if how=='Rbar':
            return Rbar(df=df, **kwargs)
        elif how == 'Sbar':
            return Sbar(df=df, **kwargs)
        else:
            return pooled_std(df=df, **kwargs)

# standard deviation within subgroups with subgroup size == 1
def average_moving_range(series, observations=2, **kwargs):
    """
    Calculate the average moving range
    """

    # get the right data format
    column = kwargs.pop('column', None)
    if isinstance(series, pd.DataFrame):
        if isinstance(column, str):
            series = series[column]
        elif series.shape[0] == 1:
            # transpose dataframe and select first column
            series = series.T.iloc[:,0]
        else:
            # select first column
            series = series.iloc[:,0]
    series = series.dropna()
    
    periods = observations - 1
    if observations >= series.shape[0]:
        raise InputError(f'The number of observations ({observations}) must be lower then the length of the series({series.shape[0]})')

    return series.diff(periods=periods).apply(abs)[periods:].dropna().mean() / constants.d2(observations)

def median_moving_range(series, observations=2, **kwargs):
    """
    Calculate the median moving range
    """
    # get the right data format
    column = kwargs.pop('column', None)
    if isinstance(series, pd.DataFrame):
        if isinstance(column, str):
            series = series[column]
        elif series.shape[0] == 1:
            # transpose dataframe and select first column
            series = series.T.iloc[:,0]
        else:
            # select first column
            series = series.iloc[:,0]
    series = series.dropna()
    
    periods = observations - 1
    if observations >= series.shape[0]:
        raise InputError(f'The number of observations ({observations}) must be lower then the length of the series({series.shape[0]})')

    return series.diff(periods=periods).apply(abs)[periods:].dropna().median() / constants.d2(observations)

def sqrt_of_mssd(series, **kwargs):
    """
    Calculate the square root of half of the mean of the squared successive differences
    """
    # get the right data format
    column = kwargs.pop('column', None)
    if isinstance(series, pd.DataFrame):
        if isinstance(column, str):
            series = series[column]
        elif series.shape[0] == 1:
            # transpose dataframe and select first column
            series = series.T.iloc[:,0]
        else:
            # select first column
            series = series.iloc[:,0]
    series = series.dropna()
    
    return (0.5 * sum(series.diff(periods=1).dropna()**2) / (series.size - 1) )**0.5 / constants.c4_(series.size)

# standard deviation within subgroups with subgroup size > 1
def pooled_std(df, columns=None, **kwargs):
    """
    Calculate pooled standard deviation for pandas DataFrame columns.
    Pooled standard devieation is used for estimating std_within when subgroup size > 1
    
    std_within = S_p / c4(d)

    S_p = ( sum_j (sum_j( (X_ij - Xbar_i) ** 2) ) ) / d
    d = ( sum_i ( n_i - 1 ) ) + 1
    """
    
    # have the entire dataframe or just some columns
    df = df if columns is None else df[columns]

    if df.shape[0] == 1:
        raise InputError(f'The subgroup size must be > 1)')

    # check if subgroup size is constant
    if len(set([df[col].dropna().size for col in df.columns])) == 1:
        # all subgroups have the same size
        S_p = (sum([df[col].var(skipna=True, ddof=1) for col in df.columns]) / len(df.columns)) ** 0.5
        d = sum([df[col].dropna().size for col in df.columns]) - len(df.columns) + 1
    else:
        # ∑i ∑j (Xij - Xi_bar) ** 2 / 
        
        # calculate overall mean
        arr = df.to_numpy().flatten()
        Xi_bar = arr[~np.isnan(arr)].mean()
        
        S_p = (sum([sum((df[col].dropna()-Xi_bar)**2) for col in df.columns]) / sum([(df[col].dropna().size - 1) for col in df.columns])) ** 0.5
        d = sum([(df[col].dropna().size - 1) for col in df.columns]) + 1

    return S_p / constants.c4(d)

def Rbar(df, columns=None, **kwargs):
    """
    Calculate Rbar; Average of subgroup ranges for pandas DataFrame columns.
    Rbar is used for estimating std_within when subgroup size > 1

    std_within = sum_i ( (f_i * r_i) / (d2(n_i)) ) / sum_i (f_i)
    f_i = ( d2(n_i)**2 ) / ( d3(n_i)**2 )

    If all n_i are the same (all subgroup sizes are of equal length) then std_within is just the adjusted average of subgroup ranges.
    std_within = Rbar / d2(n_i)
    """

    # have the entire dataframe or just some columns
    df = df if columns is None else df[columns]

    if df.shape[0] == 1:
        raise InputError(f'The subgroup size must be > 1)')
    
    # setup lambda functions
    df_range = lambda dfr: (dfr.max() - dfr.min())
    f_i = lambda dfi: (constants.d2(dfi.size)**2) / (constants.d3(dfi.size)**2)

    # check if subgroup size is constant
    if len(set([df[col].dropna().size for col in df.columns])) == 1:
        # all subgroups have the same size
        # std_within = Rbar / d2(n_i)
        std_within = (sum([df_range(df[col].dropna()) for col in df.columns]) / df.shape[1])/ constants.d2(df.shape[0])
    else:
        # std_within = sum_i ( (f_i * r_i) / (d2(n_i)) ) / sum_i (f_i)
        # f_i = ( d2(n_i)**2 ) / ( d3(n_i)**2 )
        std_within = sum([(f_i(df[col]) * df_range(df[col])) / constants.d2(df[col].size) for col in df.columns])/sum([f_i(df[col]) for col in df.columns])
    
    return std_within

def Sbar(df, columns=None, **kwargs):
    """
    Calculate Sbar; Average of subgroup standard deviations for pandas DataFrame columns.
    Sbar is used for estimating std_within when subgroup size > 1

    
    """

    # have the entire dataframe or just some columns
    df = df if columns is None else df[columns]

    if df.shape[0] == 1:
        raise InputError(f'The subgroup size must be > 1)')
    
    # calculate overall mean and size
    arr = df.to_numpy().flatten()
    Xi_bar = arr[~np.isnan(arr)].mean()
    n_i = arr[~np.isnan(arr)].size

    # setup lambda functions
    s_i = lambda dfi: (sum( (dfi - Xi_bar)**2 ) / (dfi.size - 1) )**0.5
    h_i = lambda dfi: (constants.c4(dfi.size)**2) / (1 - (constants.c4(dfi.size)**2))
        
    # check if subgroup size is constant
    if len(set([df[col].dropna().size for col in df.columns])) == 1:
        # all subgroups have the same size
        # std_within = Sbar / c4(n_i)
        std_within = (sum([df[col].dropna().std(ddof=0) for col in df.columns]) / df.shape[1]) / constants.c4(n_i)
    else:
        # std_within = sum (h_i * s_i / c4(n_i)) / sum (h_i)
        std_within = sum([(h_i(df[col].dropna()) * s_i(df[col].dropna())) / constants.c4(df[col].dropna().size) for col in df.columns]) / sum(h_i(df[col].dropna()) for col in df.columns)
    
    return std_within

