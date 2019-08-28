import numpy as np


def GetCCI(tadict, periods):

    """
    :param tadict:      Dictionary with OHLC & TAs
    :param periods:     Periods for which to calculate CCI

    :return:            A dictionary with periods as keys with CCI numpy matrices

    Description:        Commodity Channel Index (CCI) - It is  used to assess price trend direction and strength.
    """

    prices = tadict['prices'][:, 3]
    results = {}

    for period in periods:

        cci = np.zeros((len(prices) - period + 1))

        for j in range(0, len(cci)):
            std = tadict['std'][period][j]
            sma = tadict['sma'][period][j]

            if std != 0:
                cci[j] = (prices[j] - sma) / (0.015 * std)

        results[period] = cci

    return results
