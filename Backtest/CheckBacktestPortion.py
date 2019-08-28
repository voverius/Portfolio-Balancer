import numpy as np
from Plotting.PlotBacktest import *

# LOADING THE MARKET DATA
file_path = 'D:\\OneDrive\\Trade\\Daft Punk\\TrainingPackages\\4\\'

global_matrix = np.load(file_path + 'exchange_master_data.p')
predictions = np.load(file_path + 'bt_predictions.npy')
future_prices = np.load(file_path + 'bt_future_data.npy')
pvm = np.load(file_path + 'PVM.npy')

a = global_matrix['data'][31:, :]

coin = 7
start = 0
# length = 2000
length = predictions.shape[0]

values = global_matrix['data']

# FORMATTING
data_length = predictions.shape[0]
testing_values = global_matrix['data'][-(data_length+1):-1, :, :]
time_values = global_matrix['datestamps'][-(data_length+1):-1]


# PLOTTING
# --------------------------------------------------------------------------------------------------------------------

PlotBacktest(prices=testing_values[start:(start+length), coin, 3],
             portfolio_vector=predictions[start:(start+length), coin+1],
             time_values=time_values, signal_gap=5, name=global_matrix['pairs'][coin])

# PlotBacktest(prices=a[start:(start+length), coin, 3],
#              portfolio_vector=pvm[start:(start+length), coin],
#              time_values=time_values, signal_gap=5, name=global_matrix['pairs'][coin])



















