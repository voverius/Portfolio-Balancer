import numpy as np


def GetSTD(tadict, periods):

    """
    :param tadict:      Dictionary with OHLC & TAs
    :param periods:     Input period desired - e.g. 50, 100, 200

    :return:            A dictionary with periods as keys with STD numpy matrices

    Description:        Standard Deviation (STD) - is measured as the spread of data distribution
                        in the given data set
    """

    results = {}                                        # Prepare output dictionary
    prices = tadict['prices'][:, 3]                     # Only take the CLOSING values

    for period in periods:                              # Loop through all the periods

        std = np.zeros((len(prices) - period + 1))      # Prepare output matrix

        for j in range(0, len(std)):                    # loop through all the output values
            std[j] = np.std(prices[j:(j + period)])     # get the averages

        results[period] = std                           # store the output matrix in dictionary

    return results
