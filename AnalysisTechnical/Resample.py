import numpy as np


def Resample(prices, dates, period):

    prices = prices.copy()
    dates = dates.copy()
    result = np.zeros(((len(prices) // period), 5))
    time = [None] * len(result)

    if len(prices) > period:

        index = len(prices)

        for i in range(len(result), 0, -1):

            result[i-1, 0] = prices[(index-period), 0]                  # OPEN
            result[i-1, 2] = np.max([prices[(index-period):index, 2]])  # HIGH
            result[i-1, 1] = np.min([prices[(index-period):index, 1]])  # LOW
            result[i-1, 3] = prices[index-1, 3]                         # CLOSE
            result[i-1, 4] = np.sum(prices[(index-period):index, 4])    # VOLUME

            time[i-1] = dates[index-1]
            index -= period

    return result, time

