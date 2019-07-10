import bs4 as bs
import requests
import datetime as dt
import pandas_datareader as pdr
import time
import pandas as pd


class GetTickers():

    def __init__(self):
        self.web = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    def save_sp500_tickers(self):
        resp = requests.get(self.web)
        soup = bs.BeautifulSoup(resp.text, features="html.parser")
        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers = []

        for row in table.findAll('tr')[1:]:

            ticker = row.findAll('td')[0].text
            tickers.append(ticker)

        return tickers

    def get_data_from_yahoo(self, ticker: str, start: str, end: str):
        start = dt.datetime.strptime(start, "%Y-%m-%d")
        end = dt.datetime.strptime(end, "%Y-%m-%d")
        df = pdr.get_data_yahoo(ticker, start=start, end=end)
        df['Ticker'] = ticker
        return df

    def get_data_from_yahoo_tickers(self, tickers, start: str, end: str):
        result = []

        for ticker in tickers:

            try:
                result.append(self.get_data_from_yahoo(ticker, start, end))
            except Exception:
                print(ticker + " does not exist in yahoo")
                pass

        return pd.concat(result)


if __name__ == "__main__":
    ticker = GetTickers().save_sp500_tickers()
    ticker = ['AAPL']
    t = time.time()
    data = GetTickers().get_data_from_yahoo_tickers(ticker, '2018-01-01', '2018-03-01')
    print(time.time()-t)
    print(data)