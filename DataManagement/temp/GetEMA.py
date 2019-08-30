import numpy as np


def GetEMA(tadict, periods):

    """
    :param tadict:      Dictionary with OHLC & TAs
    :param periods:     input two periods e.g. 9 & 14

    :return:            A dictionary with periods as keys with EMA numpy matrices

    Description:        Exponential Moving Average (EMA) - places a greater weight and significance
                        on the most recent data points. It acts more significantly to recent price changes than
                        a simple moving average (SMA), which applies an equal weight to all observations in the period
    """

    if type(tadict) == dict:
        temp = tadict['prices'][:, 3]  # Only take the CLOSING values
    else:
        temp = tadict
    results = {}

    for period in periods:

        ema = np.zeros((len(temp)))
        ema[0] = np.mean(temp[0: period])  # Calculating the first input
        k = 2 / (period + 1)  # Filling in the rest of the averages

        for i in range(1, len(ema)):
            ema[i] = ema[i - 1] + k*(temp[i] - ema[i - 1])

        results[period] = ema

    return results

