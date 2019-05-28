import numpy as np
from scipy.signal import argrelextrema


def GeoPeaks(prices, gap=5):

    max_idx = list(argrelextrema(prices[:, 1], np.greater, order=gap)[0])
    min_idx = list(argrelextrema(prices[:, 2], np.less, order=gap)[0])

    idx = np.zeros(((len(max_idx) + len(min_idx)), 4))
    idx1 = 0  # max peak indicator (up to the size of max_idx)
    idx2 = 0  # min peak indicator (up to the size of min_idx)
    idx3 = 0  # idx indicator

    for i in range(0, len(prices)):
        if idx1 < len(max_idx) and i == max_idx[idx1]:
            temp = [max_idx[idx1], prices[max_idx[idx1], 1], prices[max_idx[idx1], 3], 0]
            idx[idx3, :] = temp
            idx1 += 1
            idx3 += 1
        elif idx2 < len(min_idx) and i == min_idx[idx2]:
            temp = [min_idx[idx2], prices[min_idx[idx2], 2], 0, prices[min_idx[idx2], 3]]
            idx[idx3, :] = temp
            idx2 += 1
            idx3 += 1

    return idx


if __name__ == "__main__":
    GeoPeaks()

