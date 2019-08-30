import numpy as np


def GetRSI(tadict, periods):

    """
    :param tadict:      Dictionary with OHLC & TAs
    :param periods:     input periods e.g. 9 & 14

    :return:            Matrix (l - period)x1 with indicator ranging between 0-1

    Description:        Relative Strength Index (RSI) is a momentum indicator that measures the magnitude
                        of recent price changes to evaluate overbought or oversold conditions in the price
                        of a stock or other asset.

    Formulas:           SMMA = (previous_val * (period - 1) + new_data) / period
                        RS   = SMMA(U) / SMMA(D)
                        RSI  = 100 - {100 / {1 + RS}}
    """

    temp = tadict['prices'][:, 3]
    results = {}

    for period in periods:

        a1 = np.zeros((len(temp), 3))                   # storing overall gains and losses
        a2 = np.zeros((len(temp) - period + 1, 4))      # storing period gains and losses (RSI)

        # CALCULATING TRUE GAINS AND LOSSES
        for j in range(1, len(temp)):

            a1[j, 0] = temp[j] - temp[j - 1]
            if a1[j, 0] > 0:            # If closing prices have changed positively (U)
                a1[j, 1] = a1[j, 0]

            elif a1[j, 0] < 0:          # If closing prices have changed negatively (D)
                a1[j, 2] = -a1[j, 0]

        # CALCULATING AVERAGE GAINS AND LOSSES
        a2[0, 0] = np.mean(a1[0:period, 1])
        a2[0, 1] = np.mean(a1[0:period, 2])

        for j in range(1, len(a2)):
            a2[j, 0] = (a2[j - 1, 0]*(period - 1) + a1[j + period - 1, 1]) / period  # SMMA(U)
            a2[j, 1] = (a2[j - 1, 1]*(period - 1) + a1[j + period - 1, 2]) / period  # SMMA(D)

        # CALCULATING THE RS & RSIs
        for j in range(0, len(a2)):
            if a2[j, 1] != 0:
                a2[j, 2] = a2[j, 0] / a2[j, 1]          # RS
                a2[j, 3] = 100 - 100 / (1 + a2[j, 2])   # RSI
            else:
                a2[j, 3] = 100

        results[period] = a2[:, 3]/100  # Storing it between 0-1 (for NN input), not 0-100 as generally done

    return results
