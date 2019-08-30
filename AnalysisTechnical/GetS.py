import numpy as np


def GetS(prices, periods):
    """
    :param prices:      OHLC Matrix
    :param periods:     Periods for the Technical Indicator  e.g. [5, 10, 15....]
    :return:            Stochastic Indicator
    """

    results = {}

    for i in range(0, len(periods)):

        K = np.zeros((len(prices) - periods[i] + 1))    # Stochastic Factor Indicator

        for j in range(0, len(K)):

            H = np.amax(prices[j:(j+periods[i]), 1])    # HIGH
            L = np.amin(prices[j:(j+periods[i]), 2])    # LOW
            C = prices[j+periods[i] - 1, 3]             # CLOSE

            if H != L:
                K[j] = 100 * (C - L) / (H - L)

        results[periods[i]] = K

    return results


if __name__ == "__main__":
    GetS()
