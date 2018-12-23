import numpy as np


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
