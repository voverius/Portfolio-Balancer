import pandas as pd
import numpy as np
import pickle
import random
from datetime import datetime
import time

from MarketData.ConstructMarketData import *


class CreateDataMatricesPandas:
    def __init__(self, config, option='load', update=False):

        if option == 'load':
            pickle_in = open((config['package_directory'] + 'exchange_master_data.p'), "rb")
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

        self.start = time.mktime(datetime.strptime(config['input']["start_date"], "%Y/%m/%d").timetuple())
        self.start = int(self.start)
        self.end = time.mktime(datetime.strptime(config['input']["end_date"], "%Y/%m/%d").timetuple())
        self.end = int(self.end)
        time_span = self.end - self.start

        # self.features = get_type_list(feature_number)
        self.coin_no = int(config['input']["coin_number"])  # 11
        self.feature_number = int(config['input']["feature_number"])  # 3
        self.period_length = int(config['input']["global_period"])  # 1800
        self.is_permed = config['input']["is_permed"]
        self.fake_ratio = config["input"]["fake_ratio"]
        self.norm_method = config["input"]["norm_method"]
        self.window_size = int(config['input']["window_size"])
        self.data_length = self.global_data.shape[2]
        self.batch_size = int(config['training']["batch_size"])
        self.commission_rate = config["trading"]["trading_consumption"]
        self.test_portion = config['input']["test_portion"]
        self.last_omega = np.zeros((self.global_data.shape[1] + 1,))
        self.last_omega[0] = 1.0
        self.asset_vector = np.zeros(self.coin_no + 1)
        self.delta = 0
        portion_reversed = config['input']["portion_reversed"]
        test_portion = config['input']["test_portion"]

        if portion_reversed:
            volume_forward = 0
        else:
            volume_forward = time_span * test_portion

        # what is this used for?
        self.PVM = pd.DataFrame(index=self.global_data.minor_axis, columns=self.global_data.major_axis)
        self.PVM = self.PVM.fillna(1.0 / self.coin_no)

        # Prepare to get Test and Train data
        self.train_ind, self.test_ind = self.divide_data(test_portion, portion_reversed)
        self.end_index = self.train_ind[-1]
        # self.replay_buffer = np.array([self.train_ind])

        # call for Test and Train Data
        self.train_data = self.pack_samples(self.train_ind)
        self.test_data = self.pack_samples(self.test_ind)

        self.train_batches = self.create_batches(self.train_data)
        self.test_batches = self.create_batches(self.test_data)

    # ---------------------------------------------------------------------------------------------------
    def divide_data(self, test_portion, portion_reversed):
        train_portion = 1 - test_portion

        if portion_reversed:
            portions = np.array([test_portion])
            portion_split = (portions * self.data_length).astype(int)
            indices = np.arange(self.data_length)
            test_ind, train_ind = np.split(indices, portion_split)
        else:
            index = int(self.data_length*train_portion)
            data_indexes = np.arange(self.data_length)
            train_ind = data_indexes[:index]
            test_ind = data_indexes[index:]
        return train_ind, test_ind

    # ---------------------------------------------------------------------------------------------------
    def pack_samples(self, indexes):
        '''
        indexes = an array from zero to the number of inputs - [0, 1, 2, 3 ... 50000]

        Cutting indexes short, because this has to be added in the get_submatrix
        pgportfolio has differently sized indexes at this point!
        '''

        indexes = np.array(indexes[:-self.window_size])
        last_w = self.PVM.values[indexes-1, :]

        def setw(w):
            self.PVM.iloc[indexes, :] = w

        '''
        Creating a 4 dimensional matrix that stores: sequence, OHLC, coin, 32 latest values
        hard brackets show to compile index[-1] amount of matrices into one 4 dimensional         
        '''

        M = [self.get_submatrix(index) for index in indexes]
        M = np.array(M)
        X = M[:, :, :, :-1]


        '''
        y output is the latest time values for all coins at every 32 x window
        It is then divided by previous CLOSE to have a proportional change e.g. 1.00235268
        
        NOTE: why all OHLC values are only divided by the close value?        
        '''

        y = M[:, :, :, -1] / M[:, 0, None, :, -2]
        return {"X": X, "y": y, "last_w": last_w, "setw": 0}

    # ---------------------------------------------------------------------------------------------------
    def get_submatrix(self, ind):
        return self.global_data.values[:, :, ind:ind+self.window_size+1]

    # ---------------------------------------------------------------------------------------------------
    def create_batches(self, data):
        '''
        :param data:    all the 'packed' data
        :return:        A list of dictionarias that contain data for batch length

        NOTE: !!! batches contain repeated data!!!
        '''

        batch = []
        indices = np.arange(data['X'].shape[0])
        random.shuffle(indices)
        Xdata = data['X'][indices]
        ydata = data['y'][indices]

        for i in range(0, (data['X'].shape[0] - self.batch_size)):
            temp = {}
            temp['X'] = data['X'][i:i + self.batch_size, :, :, :]
            temp['y'] = data['y'][i:i + self.batch_size, :, :]
            # temp['X'] = Xdata[i:i + self.batch_size, :, :, :]
            # temp['y'] = ydata[i:i + self.batch_size, :, :]
            temp['last_w'] = data['last_w'][i:(i + self.batch_size), :]
            temp['index'] = i
            # temp['setw'] = data['setw']
            batch.append(temp)

        return batch























