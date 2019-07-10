from algo_trading.data_source.stock_tickers import GetTickers
from algo_trading.trading_strategy.linear_mean_reverting import calculate_ma
from algo_trading.trading_strategy.linear_mean_reverting import calculate_moving_std

class BuyOnGapStrat():

    def __init__(self):
        self.topN = 10
        self.entryZscore = 1
        self.lookback = 20

    def buy_on_gap_strategy(self, universe):
        price_df = GetTickers().get_data_from_yahoo_tickers(universe)
        price_df = calculate_ma(price_df, 'Adj Close', 20)
        price_df = calculate_moving_std(price_df, 'Adj Close', 90)

        price_df['Criteria 1'] = (price_df['Open'] - price_df['Low'].shift(1)) < -price_df['MStd 90']
        price_df['Criteria_2'] = price_df['Open'] > price_df['MA 20']
        price_df['Buy'] = (price_df['Criteria 1'] & price_df['Criteria_2'])

        price_df = price_df[price_df['Buy']]
        # todo: include 10 low returns
        # todo: include short ability
        # todo: include hedged version
        return price_df

if __name__ == "__main__":
    a = BuyOnGapStrat().buy_on_gap_strategy(['A', 'AA', 'AAC', 'AAN', 'AAP'])
    print(a)