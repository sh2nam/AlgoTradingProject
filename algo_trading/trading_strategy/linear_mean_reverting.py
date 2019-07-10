import pandas as pd
import numpy as np
from algo_trading.data_source.quandl_downloader import DownloadTs


def calculate_ma(df: pd.DataFrame, price_col: str, days: int) -> pd.DataFrame:

    # sort time series from oldest to recent
    df.sort_values(by='Date', ascending=True, inplace=True)

    df['MA ' + str(days)] = df[price_col].rolling(window=days).mean()
    df.dropna(subset=['MA ' + str(days)], inplace=True)
    return df


def calculate_moving_std(df: pd.DataFrame, price_col: str, days: int) -> pd.DataFrame:

    # sort time series from oldest to recent
    df.sort_values(by='Date', ascending=True, inplace=True)

    df['MStd ' + str(days)] = df[price_col].rolling(window=days).std()
    df.dropna(subset=['MStd ' + str(days)], inplace=True)

    return df

def linear_mean_reverting_strat(df: pd.DataFrame) -> pd.DataFrame:

    # todo: call half life function from stat_test
    days = 5

    # todo: think about a good way to not copy
    df_copy = df.copy()

    # get moving average and moving standard deviation
    df_ma = calculate_ma(df, 'Settle', days)
    df_ms = calculate_moving_std(df_copy, 'Settle', days)
    final = pd.merge(df_ma, df_ms, how='inner', on=['Date', 'Settle'])

    final['Trade'] = final['MA ' + str(days)] / final['MStd ' + str(days)]

    return final

def bollinger_band_strat(df: pd.DataFrame, col: str) -> pd.DataFrame:

    # todo: call half life function from stat_test
    days = 5

    # todo: think about a way to determine entry z score / exit z score
    entry_zscore = 1
    exit_zscore = 0

    # todo: think about a good way to not copy
    df_copy = df.copy()

    # get moving average and moving standard deviation
    df_ma = calculate_ma(df, col, days)
    df_ms = calculate_moving_std(df_copy, col, days)
    final = pd.merge(df_ma, df_ms, how='inner', on=['Date', col])

    final['Z Score'] = (final[col] - final['MA ' + str(days)]) / final['MStd ' + str(days)]

    final['Longs Position'] = np.where(final['Z Score'] < -entry_zscore, 1, np.nan)
    final['Longs Position'] = np.where(final['Z Score'] >= -exit_zscore, 0, final['Longs Position'])
    final['Longs Position'] = final['Longs Position'].fillna(method='ffill')
    final['Longs Position'].fillna(0, inplace=True)

    final['Shorts Position'] = np.where(final['Z Score'] > entry_zscore, -1, np.nan)
    final['Shorts Position'] = np.where(final['Z Score'] <= exit_zscore, 0, final['Shorts Position'])
    final['Shorts Position'] = final['Shorts Position'].fillna(method='ffill')
    final['Shorts Position'].fillna(0, inplace=True)

    final['Aggregated Position'] = final['Longs Position'] + final['Shorts Position']

    return final



if __name__ == "__main__":
    df1 = DownloadTs().get_price('ECB/EURCAD', '2018-01-01', '2018-10-01')
    df2 = DownloadTs().get_price('ECB/EURUSD', '2018-01-01', '2018-10-01')
    print(a)