import numpy as np

# DOES NOT FUCKING WORK!!!!!

def GetAD(prices, periods):
    """
    :param prices:      OHLC Matrix
    :param periods:     Periods for the Technical Indicator  e.g. [5, 10, 15....]
    :return:            Stochastic Indicator
    """

    results = {}

    for i in range(0, len(periods)):

        AD = np.zeros((len(prices) - periods[i] + 1))    # Stochastic Factor Indicator
        MFV = 0
        temp = 0

        for j in range(1, len(AD)):

            H = np.amax(prices[j:(j+periods[i]), 1])    # HIGH
            L = np.amin(prices[j:(j+periods[i]), 2])    # LOW
            C = prices[j + periods[i] - 1, 3]           # CLOSE
            V = prices[j + periods[i] - 1, 4]           # VOLUME

            if H != L and H != C:
                MFM = ((C - L) / (H - C)) / (H - L)     # MONEY FLOW MULTIPLIER
                MFV = MFM * V                           # MONEY FLOW VOLUME
            elif j == 0:
                MFV = 0
            else:
                MFV = AD[j-1]

            # AD[j] = MFV + temp
            AD[j] = MFM
            temp = MFV

        results[periods[i]] = AD

    return results

