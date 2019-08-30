import numpy as np


def GetSLOPE(tadict, periods):

    """
    :param tadict:      Dictionary with OHLC & TAs
    :param periods:     Input periods e.g. 9 & 14

    :return:            A dictionary with periods as keys with Slope numpy matrices

    Description:        Calculating height of the triangle for the change in HIGH prices divided by period
    """

    temp = tadict['prices'][:, 1]     # High
    results = {}

    for period in periods:

        slope = np.zeros((len(temp) - period + 1))

        for j in range(0, len(slope)):
            slope[j] = (temp[j + period - 1] - temp[j]) / period

        results[period] = slope

    return results
