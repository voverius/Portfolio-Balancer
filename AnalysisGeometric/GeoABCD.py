import numpy as np
from geo.GeoABCDloop import *
from geo.GeoGartley import *
from geo.GeoCrab import *
from geo.GeoBat import *
from geo.GeoButterfly import *


def GeoABCD(prices, idx):

    idx = idx.copy()
    prices = prices.copy()

    # Filing in the latest data (today, now)
    temp = np.zeros((5, 4))
    finish = len(prices) - 1
    temp[4, 0:2] = [finish, prices[finish, 3]]

    if prices[finish, 3] > prices[finish - 1, 3]:
        temp[4, 2] = prices[finish, 3]
    else:
        temp[4, 3] = prices[finish, 3]

    # cropping idx matrix in case starting from the middle (development)
    for i in range((len(idx) - 1), 0, -1):
        if idx[i, 0] == finish:
            temp[4, :] = idx[i, :]
            idx = idx[:i]
            break
        elif idx[i - 1, 0] < finish < idx[i, 0]:
            idx = idx[:i]
            break

    # filling in the other 4 peaks
    temp[0:4, :] = idx[-4:]

    # checking if the last 5 values form a 'W' or 'M' pattern
    XA = temp[0, 1] - temp[1, 1]
    AB = temp[1, 1] - temp[2, 1]
    BC = temp[2, 1] - temp[3, 1]
    CD = temp[3, 1] - temp[4, 1]
    diff = np.array([XA, AB, BC, CD])

    if XA>0 and AB<0 and BC>0 and CD<0:
        pattern = 1
    elif XA<0 and AB>0 and BC<0 and CD>0:
        pattern = -1
    else:
        pattern = 0

    # Start a loop to check for feasibility with neighbouring candles & max/close values
    flag = [False] * 4
    results = np.zeros(4)
    if pattern != 0:
        err_allowed = 0.15
        # flag, temp = GeoABCDloop(prices, temp, prices[finish, :], err_allowed=err_allowed)
        flag[0] = GeoGartley(diff, err_allowed=err_allowed)
        flag[1] = GeoCrab(diff, err_allowed=err_allowed)
        flag[2] = GeoBat(diff, err_allowed=err_allowed)
        flag[3] = GeoButterfly(diff, err_allowed=err_allowed)

        if any(flag):
            for i in range(0, 4):
                if flag[i]:
                    results[i] = pattern

    return results, temp


if __name__ == "__main__":
    GeoABCD()

