import numpy as np


def GetHA(prices, periods):

    """
    :param prices:      input OHLC matrix
    :return:            Heiken Ashi matrix
    """

    prices = prices.copy()
    ha = prices.copy()
    results = {}

    for i in range(1, len(prices)):
        ha[i][0] = (prices[i-1, 0] + prices[i-1, 3]) / 2                    # OPEN
        ha[i][1] = np.amax([prices[i, 0], prices[i, 1], prices[i, 3]])      # HIGH
        ha[i][2] = np.amin([prices[i, 0], prices[i, 2], prices[i, 3]])      # LOW
        ha[i][3] = np.sum(prices[i, 0:4]) / 4                               # CLOSE

    results[periods[0]] = ha
    return results


if __name__ == "__main__":
    GetHA()
