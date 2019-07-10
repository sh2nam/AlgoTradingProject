from algo_trading.data_source.stock_tickers import GetTickers
import algo_trading.util.return_calc as a
import numpy as np


class LinearLongShortStrat():

    def __init__(self):
        self.universe = GetTickers().save_sp500_tickers()

    def linear_long_short_strat(self, start: str, end: str, universe=None):
        if not universe:
            universe = self.universe

        # get price for stocks and index
        df = GetTickers().get_data_from_yahoo_tickers(universe, start, end)

        # get daily returns for stocks and index
        df = a.calculate_returns(df)
        print(df)
        # get Avg daily return
        df['Avg Daily Return'] = df.groupby(by=df.index)['Daily Return'].mean()
        df['Ret Diff'] = df['Daily Return'] - df['Avg Daily Return']
        df['Abs Ret Diff'] = np.abs(df['Ret Diff'])
        df['Divisor'] = df.groupby(df.index)['Abs Ret Diff'].sum()
        df['Weight'] = -df['Ret Diff'] / df['Divisor']

        return df


if __name__ == "__main__":
    a = LinearLongShortStrat().linear_long_short_strat('2018-01-01', '2018-03-01', ['AAPL', 'AMZN'])
    print(a)