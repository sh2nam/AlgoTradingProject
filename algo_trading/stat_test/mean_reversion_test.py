import pandas as pd
import numpy as np
from matplotlib import pyplot
import statsmodels.tsa.stattools as ts
from algo_trading.data_source.quandl_downloader import DownloadTs
import statsmodels.api as sm
from statsmodels.tsa.vector_ar.vecm import coint_johansen
import datetime


class StatTest():

    def augmented_dickey_fuller_test(self, df: pd.DataFrame, col: str, lag=1, graph=False):
        """
        Testing for mean reversion
        Augmented Dickey-Fuller test:
            Delt(y_t) = Lambda * y_t-1  + mu + beta_t + alpha_1 * delt(y_t-1) + ...........
                        + alpha_k * delt(y_t-k) + epsilon_t
        Null hypothesis: lambda = 0
        If the hypothesis can be rejected, delt(y_t) which is the next move depends on current level y_t-1
        thus, the time series is not random walk. (mean reverting)

        ex) df = DownloadTs().get_price('ECB/EURCAD', '2018-09-01', '2018-10-01')
            r = StatTest().augmented_dickey_fuller_test(df, 'Value', 1)
        """

        df.sort_values(by='Date', ascending=True, inplace=True)

        if graph is True:
            df.plot()
            pyplot.show()

        result = ts.adfuller(df[col], lag)
        result = {'ADF Statistic': result[0], 'P-value': result[1], 'Critical values': result[4]}

        return result


    def hurst_exponent(self, df: pd.DataFrame, col: str):
        """
        Stationary price series means that price series diffuses from its initial value more slowly than a geometric random
        walk would. Mathematically, we can determine the nature of the price series by measuring speed of diffusion.
        If H < 0.5, it is mean reverting, H = 0.5 then it is geometric random walk, H > 0.5 then price series is trending.
        """
        df.sort_values(by='Date', ascending=True, inplace=True)

        # range of lags
        # todo: think about range
        lags = range(2, 10)
        tau = [np.sqrt(np.std(np.subtract(df[col][lag:], df[col][:-lag]))) for lag in lags]

        # calculate Hurst as slope of log-log plot
        m = np.polyfit(np.log(lags), np.log(tau), 2)
        hurst = m[0]*2

        return hurst

    def variance_ratio_test(self, t_s):

        return 'skip for now'

    def half_life(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
        """
        calculates appropriate look back period
        :param df: DataFrame of time series
        :return:
        """
        # sort time series from oldest to recent
        df.sort_values(by='Date', ascending=True, inplace=True)

        # 1 day lag and drop nulls
        df['1 day lagged'] = df[col].shift(1)
        df.dropna(inplace=True)

        # calculate delta
        df['Delta'] = df[col] - df['1 day lagged']

        # todo: check the model again. result looks weird
        # regression result
        model = sm.OLS(df['Delta'], df['1 day lagged'])
        result = model.fit()
        beta = result.params.iloc[0]
        half_life = -np.log(2) / beta

        return half_life

    def coint_augmented_dickey_fuller_test(self, df_y, col_y, df_x, col_x):

        df_final = pd.merge(df_y, df_x, how='inner', on=['Date'])

        model = sm.OLS(df_final[col_x + '_x'], df_final[col_y + '_y'])
        model_fit = model.fit()

        df_final['Residual'] = model_fit.resid
        cadf = self.augmented_dickey_fuller_test(df_final, 'Residual')

        return cadf

    def get_johansen(self, y, p):
        """
        Get the cointegration vectors at 95% level of significance
        given by the trace statistic test.
        """

        N, l = y.shape
        jres = coint_johansen(y, 0, p)
        trstat = jres.lr1  # trace statistic
        tsignf = jres.cvt  # critical values
        print(trstat)
        print(tsignf)
        for i in range(l):
            if trstat[i] > tsignf[i, 1]:  # 0: 90%  1:95% 2: 99%
                r = i + 1
        jres.r = r
        jres.evecr = jres.evec[:, :r]

        return jres


if __name__ == "__main__":

    # df = DownloadTs().get_price('ECB/EURCAD', '2018-01-01', '2018-10-01')
    # df = df['Value'].reset_index()
    # df2 = DownloadTs().get_price('ECB/EURUSD', '2018-01-01', '2018-10-01')
    # df2 = df2['Value'].reset_index()
    # result4 = StatTest().coint_augmented_dickey_fuller_test(df2, 'Value', df, 'Value')

    mu, sigma = 0, 1  # mean and standard deviation
    n = 10000
    s1 = np.random.normal(mu, sigma, n)
    s2 = np.random.normal(mu, sigma, n)
    s3 = np.random.normal(mu, sigma, n)
    s = s1
    a = 0.5
    x_1t = np.cumsum(s1) + s2
    x_2t = a * np.cumsum(s1) + s3
    x_3t = s3
    todays_date = datetime.datetime.now().date()
    index = pd.date_range(todays_date - datetime.timedelta(10), periods=n, freq='D')
    y = pd.DataFrame(index=index, data={'col1': x_1t, 'col2': x_2t, 'col3': x_3t})

    p = 1
    jres = StatTest().get_johansen(y, p)
    print("There are ", jres.r, "cointegration vectors")
    v1 = jres.evecr[:, 0]
    v2 = jres.evecr[:, 1]
    print(v1)
    print(v2)
    v3 = jres.evec[:, 2]
    print(v3)
    print(jres.evec)