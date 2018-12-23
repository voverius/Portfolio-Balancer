import numpy as np


def GetEMA(prices, periods):
    """
    :param prices:      input OHLC matrix
    :param periods:     input two periods e.g. 9&14
    :return:            Exponential Moving Average
    """

    prices = prices.copy()
    if len(prices.shape) > 1:
        temp = prices[:, 3]     # When feeding in OHLC matrix
    else:
        temp = prices           # When feeding back EMA matrix
    results = {}

    for i in range(0, len(periods)):

        # EMA is as long as the input matrix
        ema = np.zeros((len(prices)))

        # Calculating the first input
        ema[0] = np.mean(temp[0: periods[i]])

        # Filling in the rest of the averages
        k = 2 / (periods[i] + 1)

        for j in range(1, len(ema)):
            ema[j] = ema[j-1] + k*(temp[j] - ema[j-1])

        results[periods[i]] = ema

    return results


if __name__ == "__main__":
    GetEMA()

