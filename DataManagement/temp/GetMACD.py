from AnalysisTechnical.GetEMA import *


def GetMACD(tadict, periods):

    """
    :param tadict:      Dictionary with OHLC & TAs
    :param periods:     input three periods e.g. 12, 26 & 9

    :return:            A dictionary with periods as keys with MACD numpy matrices

    Description:        Moving Average Convergence Divergence (MACD) - is a trend-following
                        momentum indicator that shows the relationship between two moving averages
    """

    results = {}
    prices = tadict['prices'][:, 3]
    output = np.zeros((len(prices), 3))

    # MACD equals to the difference between the two period EMAs
    ema = GetEMA(tadict, periods[0:2])
    macd = ema[periods[0]] - ema[periods[1]]

    # Calculating the signal - EMA of the MACD
    signal = GetEMA(macd, [periods[2]])
    signal = signal[periods[2]]

    # Calculating the differences
    diff = np.subtract(macd, signal)

    # Storing the results
    output[:, 0] = macd
    output[:, 1] = signal
    output[:, 2] = diff
    results[periods[0]] = output

    return results

