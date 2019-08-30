import numpy as np


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

        output = np.zeros(((len(prices) - periods[i] + 1), 3))
        sma = np.zeros((len(output)))
        upper = sma.copy()
        lower = sma.copy()

        for j in range(0, len(sma)):
            sma[j] = np.mean(temp[j:(j + periods[i])])
            std = np.std(temp[j:(j + periods[i])])

            upper[j] = sma[j] + dev*std
            lower[j] = sma[j] - dev*std

        # Storing the results
        output[:, 0] = upper
        output[:, 1] = sma
        output[:, 2] = lower

        results[periods[i]] = output

    return results


if __name__ == "__main__":
    GetBB()

