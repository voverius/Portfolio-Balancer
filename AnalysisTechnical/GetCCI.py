import numpy as np


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

