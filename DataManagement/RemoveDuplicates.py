import numpy as np


def RemoveDuplicates(prices, dates):

    """
    :param prices:      input OHLC matrix
    :param dates:       parallel dates matrix
    :return:            output both matrices without stagnant days
    """

    prices = prices.copy()
    dates = dates.copy()
    boolean = np.ones(len(prices), dtype=bool)

    for i in range(len(prices)-1, -1, -1):
        if prices[i, 0] == prices[i, 1] == prices[i, 3]:
            boolean[i] = 0
            dates.pop(i)

    prices = prices[boolean, :]

    return prices, dates
