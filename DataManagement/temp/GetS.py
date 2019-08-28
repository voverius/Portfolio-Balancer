import numpy as np


def GetS(tadict, periods):

    """
    :param tadict:      Dictionary with OHLC & TAs
    :param periods:     Periods for the Technical Indicator  e.g. [5, 10, 15....]

    :return:            A dictionary with periods as keys with S numpy matrices

    Description:        The Stochastic Indicator (S) - is a momentum indicator which shows the position
                        of the most recent closing price relative to the previous high-low range
    """

    results = {}
    prices = tadict['prices']

    for period in periods:

        s = np.zeros((len(prices) - period + 1))

        for i in range(0, len(s)):

            H = tadict['mm'][period][i, 0]   # High
            L = tadict['mm'][period][i, 1]   # Low
            C = prices[(i + period - 1), 3]  # Close

            if H != L:
                s[i] = (C - L) / (H - L)

        results[period] = s

    return results
