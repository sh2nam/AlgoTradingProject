import pandas as pd
import numpy as np


def calculate_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates daily returns
    :param df: DataFrame
    :return: DataFrame
    """
    # sort DataFrame
    df.sort_values(by=['Ticker', 'Date'], ascending=True, inplace=True)

    df['Daily Return'] = np.where(df['Ticker'] != df['Ticker'].shift(1), np.nan,
                                  (df['Adj Close'] - df['Adj Close'].shift(1))/df['Adj Close'].shift(1))
    # todo: do intra day returns
    # todo: think about a way to separate different types of returns to handle return calculation for different cases

    return df


if __name__ == "__main__":
    from algo_trading.data_source.stock_tickers import GetTickers
    price = GetTickers().get_data_from_yahoo_tickers(['AMZN', 'AAPL'], '2018-01-01', '2018-03-01')
    a = calculate_returns(price)
    print(price)