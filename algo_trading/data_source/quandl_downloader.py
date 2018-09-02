import quandl


class DownloadTs():

    def __init__(self):
        quandl.ApiConfig.api_key = 'rzeAfzNCd2KwEkfV_i1U'

    def get_price(self, ticker, start, end):

        p = quandl.get(ticker, start_date=start, end_date=end)

        return p


if __name__ == "__main__":

    price = DownloadTs().get_price('CME/CADF2018','2017-01-23','2017-02-23')
    print(price['Settle'].reset_index())