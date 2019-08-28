import numpy as np


def GetMM(tadict, periods):

    """
    :param tadict:      Dictionary with OHLC & TAs
    :param periods:     Input period desired - e.g. 50, 100, 200

    :return:            A dictionary with periods as keys with Min Max numpy matrices

    Description:        Minimum & Maximum (MM) - provides min and max values for a given period
    """

    prices = tadict['prices']
    results = {}  # Prepare output dictionary

    # Loop through all the periods
    for period in periods:

        mm = np.zeros(((len(prices) - period + 1), 2))  # Prepare output matrix

        for j in range(1, len(mm)):
            mm[j, 0] = np.amax(prices[j:(j + period), 1])  # HIGH
            mm[j, 1] = np.amin(prices[j:(j + period), 2])  # LOW

        results[period] = mm

    return results

