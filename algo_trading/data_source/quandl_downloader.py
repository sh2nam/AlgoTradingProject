import quandl
import pandas as pd


class DownloadTs():

    def __init__(self):
        quandl.ApiConfig.api_key = 'rzeAfzNCd2KwEkfV_i1U'

    def get_price(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        """
        download price from Quandl
        :param ticker:
        :param start:
        :param end:
        :return: DataFrame
        ex) DownloadTs().get_price('ECB/EURCAD', '2018-09-01', '2018-10-01')
        """
        p = quandl.get(ticker, start_date=start, end_date=end)

        return p

if __name__ == "__main__":

    price = DownloadTs().get_price('ECB/EURCAD', '2018-09-01', '2018-10-01')
    print(price)