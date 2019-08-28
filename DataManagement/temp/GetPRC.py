import numpy as np


def GetPRC(tadict, periods):

    """
    :param tadict:      Dictionary with OHLC & TAs
    :param periods:     Periods for the Technical Indicator  e.g. [5, 10, 15....]

    :return:            A dictionary with periods as keys with PRC numpy matrices

    Description:        Price Rate of Change (PRC) - measures the percentage change in price
                        between the current price and the price a certain number of periods ago
    """

    results = {}
    prices = tadict['prices']

    for period in periods:

        prc = np.zeros((len(prices) - period + 1))

        for j in range(0, len(prc)):
            if prices[j + period - 1, 3] != 0:
                prc[j] = (prices[j + period - 1, 3] - prices[j, 3]) / prices[j + period - 1, 3]

        results[period] = prc
    return results
