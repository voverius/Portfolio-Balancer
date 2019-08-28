import numpy as np


def GetMOM(tadict, periods):

    """
    :param tadict:      Dictionary with OHLC & TAs
    :param periods:     Periods for the Technical Indicator  e.g. [5, 10, 15....]

    :return:            A dictionary with periods as keys with MOM numpy matrices

    Description:        Momentum indicator (MOM) - is the measurement of the speed or
                        velocity of price changes.
    """

    prices = tadict['prices']
    results = {}

    for period in periods:

        mom = np.zeros((len(prices) - period + 1))

        for j in range(0, len(mom)):
            mom[j] = prices[j + period - 1, 3] - prices[j, 3]

        results[period] = mom  # store the output matrix in the output dictionary

    return results
