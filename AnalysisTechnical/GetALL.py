import numpy as np
from scipy.optimize import *
import warnings
import matplotlib.pyplot as plt


# _________________________________________BB_____________________________________


def GetBB(prices, periods, dev=2):

    """
    :param prices:      input OHLC matrix
    :param periods:     input period of days desired - e.g. 50, 100, 200
    :param dev:         input deviation for the BB, default = 2
    :return:            Bollinger Bands
    """

    prices = prices.copy()
    temp = prices[:, 3]
    results = {}

    for i in range(0, len(periods)):

        sma = np.zeros((len(prices) - periods[i] + 1))
        upper = sma.copy()
        lower = sma.copy()

        for j in range(0, len(sma)):
            sma[j] = np.mean(temp[j:(j + periods[i])])
            std = np.std(temp[j:(j + periods[i])])

            upper[j] = sma[j] + dev*std
            lower[j] = sma[j] - dev*std

        results['upper'] = upper
        results['mid'] = sma
        results['lower'] = lower

    return results


if __name__ == "__main__":
    GetBB()


# _________________________________________CCI_____________________________________


def GetCCI(prices, periods):

    """
    :param prices:      OHLC matrix
    :param periods:     Periods for which to calculate CCI
    :return:            Commodity Channel Index
    """

    prices = prices.copy()
    temp = prices[:, 3]
    results = {}

    for i in range(0, len(periods)):

        cci = np.zeros((len(prices) - periods[i] + 1))

        for j in range(0, len(cci)):
            std = np.std(temp[j:(j + periods[i])])
            sma = np.mean(temp[j:(j + periods[i])])
            cci[j] = (temp[j] - sma) / (0.015 * std)

        results[periods[i]] = cci

    return results


if __name__ == "__main__":
    GetCCI()


# ______________________________________DETREND_____________________________________


def detrend(prices, method='percentile'):

    prices = prices.copy()
    detrended = np.zeros(len(prices))

    if method == 'linear':
        for i in range(1, len(prices)):
            detrended[i] = prices[i, 3] - prices[i-1, 3]
    elif method == 'percentile':
        for i in range(1, len(prices)):
            detrended[i] = ((prices[i, 3] / prices[i-1, 3]) - 1)*100

    return detrended


if __name__ == "__main__":
    detrend()


# _________________________________________EMA_____________________________________


def GetEMA(prices, periods):

    """
    :param prices:      input OHLC matrix
    :param periods:     input two periods e.g. 9&14
    :return:            Exponential Moving Average
    """

    prices = prices.copy()
    if len(prices.shape) > 1:
        temp = prices[:, 3]  # When feeding in OHLC matrix
    else:
        temp = prices  # When feeding back EMA matrix
    results = {}

    for i in range(0, len(periods)):

        # EMA is as long as the input matrix
        ema = np.zeros((len(prices)))

        # Calculating the first input
        ema[0] = np.mean(temp[0: periods[i]])

        # Filling in the rest of the averages
        k = 2 / (periods[i] + 1)

        for j in range(1, len(ema)):
            ema[j] = ema[j - 1] + k * (temp[j] - ema[j - 1])

        results[periods[i]] = ema

    return results


if __name__ == "__main__":
    GetEMA()


# _________________________________________FF_____________________________________


def fseries(x, a0, a1, b1, w):          # FOURIER SERIES CURVE FITTING
    return a0 + a1*np.sin(w*x) + b1*np.cos(w*x)


def sseries(x, a0, b1, w):              # SINE SERIES CURVE FITTING
    return a0 + b1*np.sin(w*x)


def GetFF(prices, periods, method='linear'):        # FOURIER FUNCTION COEFFICIENTS

    """
    :param prices:      OHLC matrix
    :param periods:     Array of periods
    :param method:      Detrending method
    :return:            Matrix of coefficients for each period
    """

    plot = False

    # Calculating the coefficients of the series
    detrended = detrend(prices, method)
    results = {}

    for i in range(0, len(periods)):

        coeffs = np.zeros(((len(prices)-periods[i]+1), 4))

        for j in range(0, len(coeffs)):

            x = np.arange(0, periods[i])
            y = detrended[j:(j+periods[i])]

            try:
                temp, extras = curve_fit(fseries, x, y)
                flag = True

            except(RuntimeError, OptimizeWarning):
                temp = np.empty((1, 4))
                temp[0, :] = np.NAN
                flag = False

            if plot & flag:
                xt = np.linspace(0, periods[i], periods[i]*10)
                yt = fseries(xt, temp[0], temp[1], temp[2], temp[3])

                plt.plot(x, y)
                plt.plot(xt, yt, 'r')
                plt.show()

            coeffs[j, :] = temp

        warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
        results[periods[i]] = coeffs

    return results


def GetSF(prices, periods, method='linear'):        # SINE FUNCTION COEFFICIENTS

    """
    :param prices:      OHLC matrix
    :param periods:     Array of periods
    :param method:      Detrending method
    :return:            Matrix of coefficients for each period
    """

    plot = False

    # Calculating the coefficients of the series
    detrended = detrend(prices, method)
    results = {}

    for i in range(0, len(periods)):

        coeffs = np.zeros(((len(prices)-periods[i]+1), 3))

        for j in range(0, len(coeffs)):

            x = np.arange(0, periods[i])
            y = detrended[j:(j+periods[i])]

            try:
                temp, extras = curve_fit(sseries, x, y)
                flag = True

            except(RuntimeError, OptimizeWarning):
                temp = np.empty((1, 3))
                temp[0, :] = np.NAN
                flag = False

            if plot & flag:
                xt = np.linspace(0, periods[i], periods[i]*10)
                yt = sseries(xt, temp[0], temp[1], temp[2])

                plt.plot(x, y)
                plt.plot(xt, yt, 'r')
                plt.show()

            coeffs[j, :] = temp

        warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
        results[periods[i]] = coeffs

    return results


# _________________________________________HA_____________________________________


def GetHA(prices):

    """
    :param prices:      input OHLC matrix
    :return:            Heiken Ashi matrix
    """

    prices = prices.copy()
    ha = prices.copy()

    for i in range(1, len(prices)):
        ha[i][0] = (prices[i-1, 0] + prices[i-1, 3]) / 2                  # OPEN
        ha[i][1] = np.amax([prices[i, 0], prices[i, 1], prices[i, 3]])      # HIGH
        ha[i][2] = np.amin([prices[i, 0], prices[i, 2], prices[i, 3]])      # LOW
        ha[i][3] = np.sum(prices[i, 0:4]) / 4                               # CLOSE

    return ha


if __name__ == "__main__":
    GetHA()


# _________________________________________MACD_____________________________________


def GetMACD(prices, periods):
    """
    :param prices:      input OHLC matrix
    :param periods:     input two periods e.g. 12, 26 & 9
    :return:            Moving Average Convergence Divergence
    """

    prices = prices.copy()
    results = {}

    # MACD equals to the difference between the two period EMAs
    ema = GetEMA(prices, periods[0:2])
    macd = ema[periods[0]] - ema[periods[1]]

    # Calculating the signal - EMA of the MACD
    signal = GetEMA(macd, [periods[2]])
    signal = signal[periods[2]]

    # Calculating the differences
    diff = np.subtract(macd, signal)

    # Storing the results
    results['macd'] = macd
    results['signal'] = signal
    results['diff'] = diff

    return results


if __name__ == "__main__":
    GetMACD()


# _________________________________________MOM_____________________________________


def GetMOM(prices, periods):
    """
    :param prices:      OHLC Matrix
    :param periods:     Periods for the Technical Indicator  e.g. [5, 10, 15....]
    :return:            Momentum indicator
    """

    CloseResults = {}
    OpenResults = {}
    prices = prices.copy()

    for i in range(0, len(periods)):

        Close = np.zeros(((len(prices) - periods[i] + 1)))
        Open = Close.copy()

        for j in range(0, len(Close)):

            Close[j] = prices[j + periods[i] - 1, 3] - prices[j, 3]
            Open[j] = prices[j + periods[i]-1, 0] - prices[j, 0]

        CloseResults[periods[i]] = Close
        OpenResults[periods[i]] = Open

    return CloseResults, OpenResults


# _________________________________________PRC_____________________________________


def GetPRC(prices, periods):
    """
    :param prices:      OHLC Matrix
    :param periods:     Periods for the Technical Indicator  e.g. [5, 10, 15....]
    :return:            Price Rate of Change
    """

    results = {}

    for i in range(0, len(periods)):

        prc = np.zeros((len(prices) - periods[i] + 1))    # Stochastic Factor Indicator

        for j in range(0, len(prc)):
            if prices[j, 3] != 0:
                prc[j] = ((prices[j + periods[i] - 1, 3] - prices[j, 3]) /
                          prices[j + periods[i] - 1, 3]) * 100

        results[periods[i]] = prc
    return results


# _________________________________________RSI_____________________________________


def GetRSI(prices, periods):
    """
    :param prices:      input OHLC matrix
    :param periods:     input periods e.g. 9&14
    :return:            Relative Strength Index
    """

    prices = prices.copy()
    temp = prices[:, 3]
    results = {}

    for i in range(0, len(periods)):

        a1 = np.zeros((len(temp), 3))                       # storing overall gains and losses
        a2 = np.zeros((len(temp) - periods[i] + 1, 4))      # storing period gains and losses (RSI)

        # a1[:, 0] - True Change
        # a2[:, 1] - Gains
        # a3[:, 2] - Losses

        # a2[:, 0] - Average Gain over Period
        # a1[:, 1] - Average Loss over Period
        # a1[:, 2] - Relative Strength
        # a1[:, 3] - RSI

        # CALCULATING TRUE GAINS AND LOSSES
        for j in range(1, len(temp)):

            a1[j, 0] = temp[j] - temp[j-1]
            if a1[j, 0] > 0:
                a1[j, 1] = a1[j, 0]

            elif a1[j, 0] < 0:
                a1[j, 2] = -a1[j, 0]

        # CALCULATING AVERAGE GAINS AND LOSSES
        a2[0, 0] = np.mean(a1[0:(periods[i]), 1])
        a2[0, 1] = np.mean(a1[0:(periods[i]), 2])

        for j in range(1, len(a2)):
            a2[j, 0] = (a2[j-1, 0]*(periods[i]-1) + a1[j + periods[i] - 1, 1]) / periods[i]
            a2[j, 1] = (a2[j-1, 1]*(periods[i]-1) + a1[j + periods[i] - 1, 2]) / periods[i]

        # CALCULATING THE RS & RSIs
        for j in range(0, len(a2)):
            if a2[j, 1] != 0:
                a2[j, 2] = a2[j, 0] / a2[j, 1]
                a2[j, 3] = 100 - 100 / (1 + a2[j, 2])
            else:
                a2[j, 3] = 100

        results[periods[i]] = a2[:, 3]

    return results


if __name__ == "__main__":
    GetRSI()


# _________________________________________S_____________________________________


def GetS(prices, periods):
    """
    :param prices:      OHLC Matrix
    :param periods:     Periods for the Technical Indicator  e.g. [5, 10, 15....]
    :return:            Stochastic Indicator
    """

    results = {}

    for i in range(0, len(periods)):

        K = np.zeros((len(prices) - periods[i] + 1))    # Stochastic Factor Indicator

        for j in range(0, len(K)):

            H = np.amax(prices[j:(j+periods[i]), 1])    # HIGH
            L = np.amin(prices[j:(j+periods[i]), 2])    # LOW
            C = prices[j+periods[i] - 1, 3]             # CLOSE

            if H != L:
                K[j] = 100 * (C - L) / (H - L)

        results[periods[i]] = K

    return results


if __name__ == "__main__":
    GetS()


# _________________________________________SLOPE_____________________________________


def GetSLOPE(prices, periods):
    """
    :param prices:      input OHLC matrix
    :param periods:     input periods e.g. 9&14
    :return:            Slope over given periods
    """

    prices = prices.copy()
    temp = prices[:, 1]     # has to be the high column
    results = {}

    for i in range(0, len(periods)):

        slope = np.zeros((len(temp) - periods[i] + 1))

        for j in range(0, len(slope)):
            slope[j] = (temp[j+periods[i]-1] - temp[j])/periods[i]

        results[periods[i]] = slope

    return results


if __name__ == "__main__":
    GetSLOPE()


# _________________________________________SMA_____________________________________


def GetSMA(prices, periods):

    """
    :param prices:      input OHLC matrix
    :param periods:     input period of days desired - e.g. 50, 100, 200
    :return:            Simple Moving Average
    """

    prices = prices.copy()
    temp = prices[:, 3]
    results = {}

    for i in range(0, len(periods)):

        sma = np.zeros((len(prices) - periods[i] + 1))

        for j in range(0, len(sma)):
            sma[j] = np.mean(temp[j:(j + periods[i])])

        results[periods[i]] = sma

    return results


if __name__ == "__main__":
    GetSMA()


# _________________________________________W_____________________________________


def GetW(prices, periods):
    """
    :param prices:      OHLC Matrix
    :param periods:     Periods for the Technical Indicator  e.g. [5, 10, 15....]
    :return:            Williams Indicator
    """

    results = {}

    for i in range(0, len(periods)):

        K = np.zeros((len(prices) - periods[i] + 1))    # Stochastic Factor Indicator

        for j in range(0, len(K)):

            H = np.amax(prices[j:(j+periods[i]), 1])    # HIGH
            L = np.amin(prices[j:(j+periods[i]), 2])    # LOW
            C = prices[j+periods[i] - 1, 3]             # CLOSE

            if H != L:
                K[j] = 100 * (H - C) / (H - L)

        results[periods[i]] = K

    return results


# _________________________________________WAD_____________________________________


def GetWAD(prices, periods):
    """
    :param prices:      OHLC Matrix
    :param periods:     Periods for the Technical Indicator  e.g. [5, 10, 15....]
    :return:            William Accumulation Distribution Matrixx
    """

    prices = prices.copy()
    results = {}

    for i in range(0, len(periods)):

        WAD = np.zeros((len(prices)))

        # Working out the True high and low prices
        for j in range(1, len(WAD)):
            TRH = np.amax([prices[j, 1], prices[j-1, 3]])
            TRL = np.amin([prices[j, 2], prices[j-1, 3]])

            # Working out the Price Move
            if prices[j, 3] > prices[j-1, 3]:
                PM = prices[j, 3] - TRL
            elif prices[j, 3] < prices[j-1, 3]:
                PM = prices[j, 3] - TRH
            else:
                PM = 0

            # Calculating the Accumulation Distribution
            WAD[j] = PM * prices[j, 4] + WAD[j-1]

        results[periods[i]] = WAD

    return results






