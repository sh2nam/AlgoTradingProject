import pandas as pd
import numpy as np
from matplotlib import pyplot
import statsmodels.tsa.stattools as ts


def augmented_dickey_fuller_test(t_s, lag=1, graph=False):
    """
    Testing for mean reversion
    Augmented Dickey-Fuller test:
        Delt(y_t) = Lambda * y_t-1  + mu + beta_t + alpha_1 * delt(y_t-1) + ...........
                    + alpha_k * delt(y_t-k) + epsilon_t
    Null hypothesis: lambda = 0
    If the hypothesis can be rejected, delt(y_t) which is the next move depends on current level y_t-1
    thus, the time series is not random walk. (mean reverting)
    """
    if graph is True:
        df.plot()
        pyplot.show()

    result = ts.adfuller(t_s, lag)
    #result = {'ADF Statistic': result[0], 'P-value': result[1], 'Critical values': result[4]}

    return result


def hurst_exponent(t_s):
    """
    Stationary price series means that price series diffuses from its initial value more slowly than a geometric random
    walk would. Mathematically, we can determine the nature of the price series by measuring speed of diffusion.
    If H < 0.5, it is mean reverting, H = 0.5 then it is geometric random walk, H > 0.5 then price series is trending.
    """

    # range of lags
    lags = range(2, 100)
    tau = [np.sqrt(np.std(np.subtract(t_s[lag:], t_s[:-lag]))) for lag in lags]

    # calculate Hurst as slope of log-log plot
    m = np.polyfit(np.log(lags), np.log(tau), 2)
    hurst = m[0]*2

    return hurst

def variance_ratio_test(t_s):
    return 'skip for now'

def half_life(t_s):
    return ''

if __name__ == "__main__":

    df = pd.read_csv(r'C:\Users\shnam\daily-total-female-births-in-cal.csv')

    # Drop last row
    df.drop(df.index[-1], inplace=True)

    # Grab timeseries
    x = df[df.columns[1]]
    adf_result = hurst_exponent(x)
    print(adf_result)