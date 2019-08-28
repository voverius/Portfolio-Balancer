import numpy as np


def GetWAD(tadict, periods):

    """
    :param tadict:      Dictionary with OHLC & TAs
    :param periods:     Periods for the Technical Indicator  e.g. [5, 10, 15....]

    :return:            A dictionary with periods as keys with WAD numpy matrices

    Description:        William Accumulation Distribution (WAD) - a cumulative indicator that uses volume
                        and price to assess whether a stock is being accumulated or distributed.
    """

    results = {}
    prices = tadict['prices']

    for period in periods:

        wad = np.zeros((len(prices) - period + 1))

        for i in range(0, len(wad)):

            H = tadict['mm'][period][i, 0]   # High
            L = tadict['mm'][period][i, 1]   # Low
            C = prices[(i + period - 1), 3]  # Close

            if H != L:
                pm = ((C - L) - (H - C)) / (H - L)
            else:
                pm = 0

            wad[i] = wad[i - 1] + pm * np.sum(tadict['volumes'][i:(i + period)])

        results[period] = wad

    return results
