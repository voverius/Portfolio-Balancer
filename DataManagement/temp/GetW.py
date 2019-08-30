import numpy as np


def GetW(tadict, periods):

    """
    :param tadict:      Dictionary with OHLC & TAs
    :param periods:     Periods for the Technical Indicator  e.g. [5, 10, 15....]

    :return:            A dictionary with periods as keys with "W" numpy matrices

    Description:        Williams Indicator (W) - momentum indicator that moves between 0 and -100
                        and measures overbought and oversold levels. The indicator is very similar to the
                        Stochastic oscillator and is used in the same way
    """

    results = {}
    prices = tadict['prices']

    for period in periods:

        w = np.zeros((len(prices) - period + 1))

        for i in range(0, len(w)):

            H = tadict['mm'][period][i, 0]  # High
            L = tadict['mm'][period][i, 1]  # Low
            C = prices[i + period - 1, 3]   # Close

            if H != L:
                w[i] = (H - C) / (H - L)

        results[period] = w

    return results
