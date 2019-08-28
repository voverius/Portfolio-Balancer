import numpy as np


def GetDetrended(tadict):

    """
    :param tadict:      Dictionary with OHLC & TAs

    :return:            Matrix with a period change percentage compared to previous period price

    Description:        This TA eliminated general values and simply gives a daily change percentage. Compared to
                        previous tick how much percentage has this gone up (positive) or down (negative).
                        Doubling in price - 100% increase is output here as 1, and 5% change as 0.05
    """

    prices = tadict['prices']
    detrended = np.zeros((prices.shape[0], prices.shape[1], 2))

    for i in range(1, len(prices)):
        for j in range(0, 4):
            detrended[i, j, 0] = (prices[i, j] / prices[(i - 1), j]) - 1
            detrended[i, j, 1] = prices[i, j] - prices[i - 1, j]

    return detrended
