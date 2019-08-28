from AnalysisTechnical.detrend import *
import numpy as np
from scipy.optimize import *
import warnings
import matplotlib.pyplot as plt


def fseries(x, a0, a1, b1, w):          # FOURIER SERIES CURVE FITTING
    return a0 + a1*np.sin(w*x) + b1*np.cos(w*x)


def sseries(x, a0, b1, w):              # SINE SERIES CURVE FITTING
    return a0 + b1*np.sin(w*x)


def GetFF(prices, periods, method='linear'):        # FOURIER FUNCTION COEFFICIENTS

    """
    :param prices:      OHLC matrix
    :param periods:     Array of periods
    :param method:      Detrending method
    :return:            Matrix of coefficients for each period
    """

    plot = False

    # Calculating the coefficients of the series
    detrended = detrend(prices, [0], method)
    detrended = detrended[0]
    results = {}

    for i in range(0, len(periods)):

        coeffs = np.zeros(((len(prices)-periods[i]+1), 4))

        for j in range(0, len(coeffs)):

            x = np.arange(0, periods[i])
            y = detrended[j:(j+periods[i])]

            try:
                temp, extras = curve_fit(fseries, x, y)
                flag = True

            except(RuntimeError, OptimizeWarning):
                temp = np.empty((1, 4))
                temp[0, :] = np.NAN
                flag = False

            if plot & flag:
                xt = np.linspace(0, periods[i], periods[i]*10)
                yt = fseries(xt, temp[0], temp[1], temp[2], temp[3])

                plt.plot(x, y)
                plt.plot(xt, yt, 'r')
                plt.show()

            coeffs[j, :] = temp

        warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
        results[periods[i]] = coeffs

    return results


def GetSF(prices, periods, method='linear'):        # SINE FUNCTION COEFFICIENTS

    """
    :param prices:      OHLC matrix
    :param periods:     Array of periods
    :param method:      Detrending method
    :return:            Matrix of coefficients for each period
    """

    plot = False

    # Calculating the coefficients of the series
    detrended = detrend(prices, [0], method)
    detrended = detrended[0]
    results = {}

    for i in range(0, len(periods)):

        coeffs = np.zeros(((len(prices)-periods[i]+1), 3))

        for j in range(0, len(coeffs)):

            x = np.arange(0, periods[i])
            y = detrended[j:(j+periods[i])]

            try:
                temp, extras = curve_fit(sseries, x, y)
                flag = True

            except(RuntimeError, OptimizeWarning):
                temp = np.empty((1, 3))
                temp[0, :] = np.NAN
                flag = False

            if plot & flag:
                xt = np.linspace(0, periods[i], periods[i]*10)
                yt = sseries(xt, temp[0], temp[1], temp[2])

                plt.plot(x, y)
                plt.plot(xt, yt, 'r')
                plt.show()

            coeffs[j, :] = temp

        warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
        results[periods[i]] = coeffs

    return results

