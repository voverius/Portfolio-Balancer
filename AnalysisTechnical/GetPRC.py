import numpy as np


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

