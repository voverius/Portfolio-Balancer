from time import time

t0 = time()
# from NeuralNetworks.NNAgent_tf import *
# from NeuralNetworks.NNTrain_tf_npy import *
# from Backtest.Backtest import *
from DataManagement.CreateDataMatrices import *
from TrainingPackages.SetupTrainingPackage import *
from NeuralNetworks.NNCreateKeras import *

t1 = time()
config = SetupTrainingPackage(4)
data = CreateDataMatrices(config=config, option='load', update=False)

print(time()-t1, t1-t0)
model = NNCreateKeras(config=config, data=data)


# from NeuralNetworks.NNAgent_tf import *
# NNAgent = NNAgent(config=config, data=data)
#
# a = 0
#
# from NeuralNetworks.NNTrain_tf_npy import *
# NNTrain = NNTrain(config=config, agent=NNAgent, data=data, model_option='load', save=False)

a = 0

# backtesting = backtest(config=config, agent=NNAgent, train=NNTrain, data=data, export=True, plot=True)


































































