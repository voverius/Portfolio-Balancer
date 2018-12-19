import numpy as np


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

