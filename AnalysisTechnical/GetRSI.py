import numpy as np


def GetRSI(prices, periods):
    """
    :param prices:      input OHLC matrix
    :param periods:     input periods e.g. 9&14
    :return:            Relative Strength Index
    """

    prices = prices.copy()
    temp = prices[:, 3]
    results = {}

    for i in range(0, len(periods)):

        a1 = np.zeros((len(temp), 3))                       # storing overall gains and losses
        a2 = np.zeros((len(temp) - periods[i] + 1, 4))      # storing period gains and losses (RSI)

        # a1[:, 0] - True Change
        # a2[:, 1] - Gains
        # a3[:, 2] - Losses

        # a2[:, 0] - Average Gain over Period
        # a1[:, 1] - Average Loss over Period
        # a1[:, 2] - Relative Strength
        # a1[:, 3] - RSI

        # CALCULATING TRUE GAINS AND LOSSES
        for j in range(1, len(temp)):

            a1[j, 0] = temp[j] - temp[j-1]
            if a1[j, 0] > 0:
                a1[j, 1] = a1[j, 0]

            elif a1[j, 0] < 0:
                a1[j, 2] = -a1[j, 0]

        # CALCULATING AVERAGE GAINS AND LOSSES
        a2[0, 0] = np.mean(a1[0:(periods[i]), 1])
        a2[0, 1] = np.mean(a1[0:(periods[i]), 2])

        for j in range(1, len(a2)):
            a2[j, 0] = (a2[j-1, 0]*(periods[i]-1) + a1[j + periods[i] - 1, 1]) / periods[i]
            a2[j, 1] = (a2[j-1, 1]*(periods[i]-1) + a1[j + periods[i] - 1, 2]) / periods[i]

        # CALCULATING THE RS & RSIs
        for j in range(0, len(a2)):
            if a2[j, 1] != 0:
                a2[j, 2] = a2[j, 0] / a2[j, 1]
                a2[j, 3] = 100 - 100 / (1 + a2[j, 2])
            else:
                a2[j, 3] = 100

        results[periods[i]] = a2[:, 3]

    return results


if __name__ == "__main__":
    GetRSI()

