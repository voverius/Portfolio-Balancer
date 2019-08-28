import numpy as np


def GetSMA(tadict, periods):

    """
    :param tadict:      Dictionary with OHLC & TAs
    :param periods:     Input period desired - e.g. 50, 100, 200

    :return:            A dictionary with periods as keys with SMA numpy matrices

    Description:        Simple Moving Average (SMA) - is an unweighted mean of the previous 'n' data points.
                        Current ticker for SMA represents the average of a given period prior to it
    """

    prices = tadict['prices'][:, 3]  # Only take the CLOSING values
    results = {}  # Prepare output dictionary

    # Loop through all the periods
    for period in periods:

        sma = np.zeros((len(prices) - period + 1))  # Prepare output matrix

        for j in range(0, len(sma)):    # loop through all the output values
            sma[j] = np.mean(prices[j:(j + period)])  # get the averages

        results[period] = sma  # store the output matrix in the output dictionary

    return results

