import numpy as np
from datetime import datetime

from MarketData.GetMarketData import *
from MarketData.ShapeMarketData import *


def ConstructMarketData(period, pairs=[], update=False):

    '''
    :param period:      Time interval/period for data ticks
    :param pairs:       Which particular pairs to do: empty list = all, number - find top x pairs
    :param update:      Should the data be updated before constructing
    :return:            A 3D numpy matrix with OHLC data for the selected pairs, list with the pair names
    '''

    if update:
        if type(pairs) == list:
            GetMarketData(periods=[period], pairs=pairs)
        else:
            GetMarketData(periods=[period], pairs=[])

    # Create a list of all .npy files
    file_path = os.path.dirname(os.getcwd())
    file_path = file_path + '\\ExchangeData\\Poloniex\\' + period + '\\'
    file_list = [f for f in listdir(file_path) if isfile(join(file_path, f))]

    final_master = {}
    master = {}
    keys = []
    sizes = []

    if type(pairs) == list:  # This is in case a specific list of pairs is given

        for pair in pairs:
            for name in file_list:
                if name.split(' ')[0] == 'USDT_BTC':
                    if name.split(' ')[0] == pair:
                        final_master = {'USDT_BTC': np.load(file_path + name)}
                        break
                elif name.split(' ')[0] == pair:
                    master[name.split(' ')[0]] = np.load(file_path + name)
                    keys.append(name.split(' ')[0])
                    break

        for key in master:
            final_master[key] = master[key]
        final_keys = keys.copy()

    else:  # This is in case a number of top pairs is given

        for name in file_list:
            if name.split(' ')[0].split('_')[0] == 'BTC':
                master[name.split(' ')[0]] = np.load(file_path + name)
                keys.append(name.split(' ')[0])
                sizes.append(master[name.split(' ')[0]].shape[0])
            elif name.split(' ')[0] == 'USDT_BTC':
                final_master = {'USDT_BTC': np.load(file_path + name)}
                final_master['USDT_BTC'][:, 1:5] = 1 / final_master['USDT_BTC'][:, 1:5]
                final_master['USDT_BTC'] = final_master['USDT_BTC'][:, [0, 1, 3, 2, 4, 5]]

        sorted_keys = [x for _, x in sorted(zip(sizes, keys), reverse=True)]
        sorted_keys = sorted_keys[:(pairs * 2)]
        volumes = []

        for key in sorted_keys:
            volumes.append(int(sum(master[key][:, 5])))

        final_keys = [x for _, x in sorted(zip(volumes, sorted_keys), reverse=True)]
        final_keys = final_keys[:(pairs - 1)]

        for key in final_keys:
            final_master[key] = master[key]

    matrix = ShapeMarketData(final_master)
    datestamps = []

    for i in range(0, matrix.shape[0]):
        datestamps.append(datetime.utcfromtimestamp(matrix[i, 0, 0]).strftime('%Y-%m-%d %H:%M'))

    output = {'data': matrix[:, :, 1:5],
              'timestamps': matrix[:, 0, 0],
              'datestamps': datestamps,
              'volumes': matrix[:, :, -1],
              'pairs': (['USDT_BTC'] + final_keys)}

    return output


if __name__ == "__main__":
    ConstructMarketData()
