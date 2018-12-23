import numpy as np


def detrend(prices, periods, method='percentile'):

    prices = prices.copy()
    detrended = np.zeros(len(prices))
    results = {}

    if method == 'linear':
        for i in range(1, len(prices)):
            detrended[i] = prices[i, 3] - prices[i-1, 3]
    elif method == 'percentile':
        for i in range(1, len(prices)):
            detrended[i] = ((prices[i, 3] / prices[i-1, 3]) - 1)*100

    results[periods[0]] = detrended

    return results


if __name__ == "__main__":
    detrend()
