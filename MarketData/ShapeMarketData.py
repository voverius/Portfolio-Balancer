import numpy as np


def ShapeMarketData(master):

    '''
    :param data:    A dictionary with pairs that need shaping
    :return:        A 3D numpy array with all the market data shaped
    '''

    bottoms = []
    tops = []
    for key in master:
        bottoms.append(master[key][-1, 0])
        tops.append(master[key][0, 0])

    master_top = max(tops)
    master_bottom = min(bottoms)
    shaped = []

    for key in master:
        top = np.where(master[key][:, 0] == master_top)[0][0]
        bottom = np.where(master[key][:, 0] == master_bottom)[0][0]

        shaped.append(master[key][top:bottom, :])

    matrix = np.zeros((shaped[0].shape[0], len(shaped), shaped[0].shape[1]))

    for i in range(0, len(shaped)):
        matrix[:, i, :] = shaped[i]

    # Check if the data is SEQUENTIAL and aligned:
    for i in range(matrix.shape[0]):
        if not all(matrix[i, :, 0] == matrix[i, 0, 0]):
            print('ERROR - The data in MASTER file are NOT SEQUENTIAL')

    return matrix


if __name__ == "__main__":
    ShapeMarketData()


