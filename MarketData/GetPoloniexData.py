import os
import time
import numpy as np
from os import listdir
from os.path import isfile, join

from APIs.PoloniexAPI import *


class GetPoloniexData:
    def __init__(self, option='UpdateAll', pairs=[], loc='15M'):

        run = True
        self.polo = Poloniex()

        # set up time intervals:
        if loc[-1] == 'M':
            interval = int(loc[:-1]) * 60
        elif loc[-1] == 'H':
            interval = int(loc[:-1]) * 60 * 60
        elif loc[-1] == 'D':
            interval = int(loc[:-1]) * 60 * 60 * 24
        else:
            run = False

        # Create a list of all .npy files
        file_path = os.path.dirname(os.getcwd())
        file_path = file_path + '\\ExchangeData\\Poloniex\\' + loc + '\\'
        file_list = [f for f in listdir(file_path) if isfile(join(file_path, f))]

        # Create a list of pairs and the last datestamps
        datestamps = []
        file_locations = datestamps.copy()

        if option == 'Update':
            for pair in pairs:
                for line in file_list:
                    data = line.split(' ')
                    if data[0] == pair:
                        datestamps.append(data[2][:-4])
                        file_locations.append(line)
                        break

        elif option == 'UpdateAll':
            pairs = []
            for line in file_list:
                data = line.split(' ')
                pairs.append(data[0])
                datestamps.append(data[2][:-4])
                file_locations.append(line)

        elif option == 'Fresh':
            # This has to developed further!
            pairs = []
            for k, v in self.polo.MarketVolume.items():
                if not k.startswith('total'):
                    pairs.append(k)
        else:
            run = False

        # Start Updating files
        if run:

            print(f'Updating Poloniex - {len(pairs)} pairs for {loc} period')
            end = int(time.time())

            for i in range(0, len(pairs)):

                if end - int(datestamps[i]) > interval:
                    old = np.load(file_path + file_locations[i])
                    chart = self.GetChart(pair=pairs[i], start=int(datestamps[i]), end=end, period=interval)

                    if 'error' in chart:
                        print(f'{pairs[i]}-{loc}: {chart}')
                        continue

                    new = self.ConvertToMatrix(chart)
                    updated = np.concatenate((old, new[1:, :]), axis=0)

                    if not old[-1, 0] == updated[-1, 0]:
                        self.SaveToNPY(file_path, updated, pairs[i], file_locations[i])

                # THIS IS WRITTEN FOR UPDATE ONLY! NOT FOR FRESH DATA!!

    def GetChart(self, pair, start, end, period):

        chart = {}
        connect_success = False
        while not connect_success:
            try:
                chart = self.polo.MarketChart(pair=pair, start=start, end=end, period=int(period))
                connect_success = True
            except Exception as e:
                print(e)
        return chart

    def SaveToNPY(self, file_path, matrix, pair, file_name=[], new=False):

        loc = file_path.split('\\')[-2]
        new_file_name = f'{pair} {loc} {int(matrix[-1, 0])}.npy'

        if new:
            np.save((file_path + new_file_name), matrix)
        else:
            np.save((file_path + file_name), matrix)
            os.rename((file_path + file_name), (file_path + new_file_name))

    def ConvertToMatrix(self, chart):
        matrix = np.zeros((len(chart), 6))
        counter = 0
        for line in chart:
            matrix[counter, 0] = line['date']
            matrix[counter, 1] = line['open']
            matrix[counter, 2] = line['high']
            matrix[counter, 3] = line['low']
            matrix[counter, 4] = line['close']
            matrix[counter, 5] = line['volume']
            counter += 1
        return matrix


if __name__ == "__main__":
    GetPoloniexData()

