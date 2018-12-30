import numpy as np


def GeoBat(diff, err_allowed=0.1):

    """
    :param diff:            a matrix with the values of the last 5 peaks
    :param err_allowed:     Percentage of error allowed, default - 10%
    :return:                True / False
    """

    # Creating top and bottom levels for the values to be in
    ABrange1 = np.array([0.382 - 0.382 * err_allowed, 0.382 + 0.382 * err_allowed]) * abs(diff[0])
    ABrange2 = np.array([0.500 - 0.500 * err_allowed, 0.500 + 0.500 * err_allowed]) * abs(diff[0])
    BCrange1 = np.array([0.382 - 0.382 * err_allowed, 0.382 + 0.382 * err_allowed]) * abs(diff[1])
    BCrange2 = np.array([0.886 - 0.886 * err_allowed, 0.886 + 0.886 * err_allowed]) * abs(diff[1])
    CDrange1 = np.array([1.618 - 1.618 * err_allowed, 1.618 + 1.618 * err_allowed]) * abs(diff[2])
    CDrange2 = np.array([2.618 - 2.618 * err_allowed, 2.618 + 2.618 * err_allowed]) * abs(diff[2])
    XDrange = np.array([0.886 - 0.886 * err_allowed, 0.886 + 0.886 * err_allowed]) * abs(diff[0])

    # Checking if the ABCD pattern fits Gartley ratios
    condition1 = [ABrange1[0] < abs(diff[1]) < ABrange1[1], BCrange1[0] < abs(diff[2]) < BCrange1[1],
                  CDrange1[0] < abs(diff[3]) < CDrange1[1], XDrange[0] < abs(diff[3]) < XDrange[1]]
    condition2 = [ABrange2[0] < abs(diff[1]) < ABrange2[1], BCrange2[0] < abs(diff[2]) < BCrange2[1],
                  CDrange2[0] < abs(diff[3]) < CDrange2[1], XDrange[0] < abs(diff[3]) < XDrange[1]]
    if all(condition1) or all(condition2):
        return True
    else:
        return False


if __name__ == "__main__":
    GeoBat()

