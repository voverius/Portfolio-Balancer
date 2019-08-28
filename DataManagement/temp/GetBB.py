import numpy as np


def GetBB(tadict, periods, dev=2):

    """
    :param tadict:      Dictionary with OHLC & TAs
    :param periods:     input period of days desired - e.g. 50, 100, 200
    :param dev:         input deviation for the BB, default = 2

    :return:            Bollinger Bands

    Description:        Set of lines plotted two standard deviations (positively and negatively)
                        away from a simple moving average (SMA) of the security's price
    """

    temp = tadict['prices'][:, 3]  # Only CLOSING values
    results = {}

    for period in periods:

        output = np.zeros(((len(temp) - period + 1), 3))
        upper = np.zeros((len(output)))
        lower = upper.copy()

        for i in range(0, len(output)):
            sma = tadict['sma'][period][i]
            std = tadict['std'][period][i]

            upper[i] = sma + dev*std
            lower[i] = sma - dev*std

        # Storing the results
        output[:, 0] = upper
        output[:, 1] = tadict['sma'][period]
        output[:, 2] = lower

        results[period] = output

    return results
