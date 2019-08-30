import pandas as pd
import numpy as np
import pickle
import random
import time

from MarketData.ConstructMarketData import *


class CreateDataMatrices:
    def __init__(self, config, option='load', update=False):

        if option == 'load':
            pickle_in = open((config['package_directory'] + 'exchange_master_data.p'), 'rb')
            self.global_data = pickle.load(pickle_in)
        elif option == 'construct':
            self.global_data = ConstructMarketData(period=config['input']['period'],
                                                   pairs=int(config['input']['coin_number']),
                                                   update=update)
            pickle_out = open((config['package_directory'] + 'exchange_master_data.p'), 'wb')
            pickle.dump(self.global_data, pickle_out)
            pickle_out.close()
        elif option == 'load_old_pandas':
            file_path = 'D:\\OneDrive\\Trade\\Daft Punk\\TrainingPackages\\15\\panel_test.h5'
            self.global_data = pd.read_hdf(file_path, 'df')

        # Establishing Global Variables
        self.window_size = int(config['input']["window_size"])
        self.data_length = self.global_data['data'].shape[0]
        self.batch_size = int(config['training']["batch_size"])
        self.commission_rate = config["trading"]["trading_consumption"]
        self.last_omega = np.zeros((self.global_data['data'].shape[1] + 1,))
        self.last_omega[0] = 1.0

        # Create 4D blocks that are going to be put directly into AI
        packed_data = self.pack_samples()
        cut_index = int(packed_data['x'].shape[0] * (1 - config['input']["test_portion"]))
        cut_index = cut_index - (cut_index % self.batch_size)  # rounding up so all batches are the same size

        self.train_data = {'x': packed_data['x'][:cut_index, :, :, :],
                           'y': packed_data['y'][:cut_index, :, :],
                           'last_w': np.arange(cut_index)}

        self.test_data = {'x': packed_data['x'][cut_index:, :, :, :],
                          'y': packed_data['y'][cut_index:, :, :],
                          'last_w': np.arange(start=cut_index, stop=packed_data['x'].shape[0])}

        # Portfolio Vector Matrix
        self.PVM = np.ones(((packed_data['x'].shape[0] + 1), packed_data['x'].shape[1]))
        self.PVM = self.PVM / self.PVM.shape[1]

    # ---------------------------------------------------------------------------------------------------
    def pack_samples(self):
        '''
        This program takes the entire exchange data and starts preparing it for AI input. it breaks it down to little
        windows (e.g. 31), takes the last value as an output target for AI, and the first 31 as input. This creates a
        4D matrix - time x pairs x OHLC x new_windows

        :return: a dictionary where 'X' is the AI input and 'y' is output target

        Creating a 4 dimensional matrix that stores: sequence, OHLC, coin, 32 latest values
        hard brackets show to compile index[-1] amount of matrices into one 4 dimensional         
        '''
        m = [self.get_submatrix(i) for i in range(0, (self.global_data['data'].shape[0] - self.window_size))]
        m = np.array(m)
        x = m[:, :, :, :-1]
        '''
        y output is the latest time values for all coins at every 32 x window
        It is then divided by previous values to have a proportional change e.g. 1.00235268      
        '''
        y = m[:, :, :, -1] / m[:, :, :, -2]
        return {'x': x, 'y': y}

    # ---------------------------------------------------------------------------------------------------
    def get_submatrix(self, ind):
        temp = self.global_data['data'][ind:ind + self.window_size + 1, :, :]
        return np.moveaxis(temp, 0, -1)

    # ---------------------------------------------------------------------------------------------------
    def create_batches(self, indexes):
        '''
        :param indexes:     An array of random indexes that need to be taken out of the sequential matrix
        :return:            A list of dictionaries that contain data for each batch
        '''

        batch = []
        for i in range(0, int(indexes.shape[0] / self.batch_size)):
            batch_indexes = indexes[(i * self.batch_size):(i * self.batch_size + self.batch_size)]
            temp = {'x': self.train_data['x'][batch_indexes, :, :, :],
                    'y': self.train_data['y'][batch_indexes, :, :],
                    'last_w': self.train_data['last_w'][batch_indexes]}
            batch.append(temp)

        return batch
