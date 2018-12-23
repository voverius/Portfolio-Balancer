import numpy as np


def GetMOM(prices, periods):
    """
    :param prices:      OHLC Matrix
    :param periods:     Periods for the Technical Indicator  e.g. [5, 10, 15....]
    :return:            Momentum indicator
    """

    prices = prices.copy()
    results = {}

    for i in range(0, len(periods)):

        temp = np.zeros(((len(prices) - periods[i] + 1),2))

        for j in range(0, len(temp)):

            temp[j, 0] = prices[j + periods[i] - 1, 3] - prices[j, 3]
            temp[j, 1] = prices[j + periods[i]-1, 0] - prices[j, 0]

        results[periods[i]] = temp

    return results

