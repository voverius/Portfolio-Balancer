import numpy as np

from geo.GeoGartley import *
from geo.GeoCrab import *
from geo.GeoBat import *
from geo.GeoButterfly import *


def GeoABCDloop(prices, temp, today, err_allowed=0.1):

    package = np.zeros((4, 3, 3))
    package[0, 0:3, 0] = [temp[0, 0] - 1, temp[0, 0], temp[0, 0] + 1]
    package[1, 0:3, 0] = [temp[1, 0] - 1, temp[1, 0], temp[1, 0] + 1]
    package[2, 0:3, 0] = [temp[2, 0] - 1, temp[2, 0], temp[2, 0] + 1]
    package[3, 0:3, 0] = [temp[3, 0] - 1, temp[3, 0], temp[3, 0] + 1]

    for i in range(0, 4):
        for j in range(0, 3):
            if temp[i, 3] == 0:
                package[i, j, 1] = prices[int(package[i, j, 0]), 1]
                if prices[int(package[i, j, 0]), 3] > prices[int(package[i, j, 0]), 0]:
                    package[i, j, 2] = prices[int(package[i, j, 0]), 3]
                else:
                    package[i, j, 2] = prices[int(package[i, j, 0]), 0]
            else:
                package[i, j, 1] = prices[int(package[i, j, 0]), 2]
                if prices[int(package[i, j, 0]), 3] < prices[int(package[i, j, 0]), 0]:
                    package[i, j, 2] = prices[int(package[i, j, 0]), 3]
                else:
                    package[i, j, 2] = prices[int(package[i, j, 0]), 0]

    # This loop will feed all the package data to GeoChecks
    temp3 = np.zeros((5, 2))
    flag = [False] * 4

    for i in range(0, 4):
        temp3[4, 0:2] = [temp[4, 0], today[i]]

        # Filling in the 1st node
        for j0 in range(0, 3):
            for k0 in range(1, 3):
                temp3[0, 0:2] = [package[0, j0, 0], package[0, j0, k0]]

                # Filling in the 2nd node
                for j1 in range(0, 3):
                    for k1 in range(1, 3):
                        temp3[1, 0:2] = [package[1, j1, 0], package[1, j1, k1]]

                        # Filling in the 3rd node
                        for j2 in range(0, 3):
                            for k2 in range(1, 3):
                                temp3[2, 0:2] = [package[2, j2, 0], package[1, j2, k2]]

                                # Filling in the 4th node
                                for j3 in range(0, 3):
                                    for k3 in range(1, 3):
                                        temp3[3, 0:2] = [package[3, j3, 0], package[1, j3, k3]]

                                        # Calculating the differences Matrix
                                        diff = [temp3[0, 1] - temp3[1, 1], temp3[1, 1] - temp3[2, 1],
                                                temp3[2, 1] - temp3[3, 1], temp3[3, 1] - temp3[4, 1]]

                                        # Launching the GeoChecks
                                        flag[0] = GeoGartley(diff, err_allowed=err_allowed)
                                        flag[1] = GeoCrab(diff, err_allowed=err_allowed)
                                        flag[2] = GeoBat(diff, err_allowed=err_allowed)
                                        flag[3] = GeoButterfly(diff, err_allowed=err_allowed)

                                        if any(flag):
                                            break

    return flag, temp3


if __name__ == "__main__":
    GeoABCDloop()

