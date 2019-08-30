import numpy as np


def GetHA(tadict, periods):

    """
    :param tadict:      Dictionary with OHLC & TAs
    :param periods:     Input period desired - e.g. 50, 100, 200

    :return:            A dictionary with periods as keys with HA numpy matrices

    Description:        Haiken Ashi (HA) - means "average bar", this technique can be used
                        in conjunction with candlestick charts.
    """

    results = {}
    prices = tadict['prices']

    for period in periods:
        ha = np.zeros((prices.shape[0], prices.shape[1]))

        for i in range(1, len(prices)):
            ha[i, 0] = (prices[i - 1, 0] + prices[i - 1, 3]) / 2                # OPEN
            ha[i, 1] = prices[i, 1]                                             # HIGH
            ha[i, 2] = prices[i, 2]                                             # LOW
            ha[i, 3] = np.sum(prices[i, :]) / 4                                 # CLOSE

        results[period] = ha
    return results

