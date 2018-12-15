import numpy as np


def GetWAD(prices, periods):
    """
    :param prices:      OHLC Matrix
    :param periods:     Periods for the Technical Indicator  e.g. [5, 10, 15....]
    :return:            William Accumulation Distribution Matrixx
    """

    prices = prices.copy()
    results = {}

    for i in range(0, len(periods)):

        WAD = np.zeros((len(prices)))

        # Working out the True high and low prices
        for j in range(1, len(WAD)):
            TRH = np.amax([prices[j, 1], prices[j-1, 3]])
            TRL = np.amin([prices[j, 2], prices[j-1, 3]])

            # Working out the Price Move
            if prices[j, 3] > prices[j-1, 3]:
                PM = prices[j, 3] - TRL
            elif prices[j, 3] < prices[j-1, 3]:
                PM = prices[j, 3] - TRH
            else:
                PM = 0

            # Calculating the Accumulation Distribution
            WAD[j] = PM * prices[j, 4] + WAD[j-1]

        results[periods[i]] = WAD

    return results
