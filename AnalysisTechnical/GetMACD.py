import numpy as np
from TA.GetEMA import *


def GetMACD(prices, periods):
    """
    :param prices:      input OHLC matrix
    :param periods:     input three periods e.g. 12, 26 & 9
    :return:            Moving Average Convergence Divergence
    """

    prices = prices.copy()
    output = np.zeros((len(prices), 3))
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
    output[:, 0] = macd
    output[:, 1] = signal
    output[:, 2] = diff
    results[periods[0]] = output

    return results


if __name__ == "__main__":
    GetMACD()

