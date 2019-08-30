from DataManagement.RemoveDuplicates import *
from DataManagement.GetCSV import *
import numpy as np
from plotting.PlotOHLC import *
from geo.GeoPeaks import *
from geo.GeoABCD import *
from tqdm import tqdm

err_allowed = 0.3
prices, dates = GetCSV('GSPC', platform='Yahoo')
prices, dates = RemoveDuplicates(prices, dates)

# prices = prices[:67, :]
idx = GeoPeaks(prices)
pips = np.zeros(15)
asd = np.zeros(15)

# for i in tqdm(range(int(idx[4, 0] + 1), len(prices))):
for i in range(int(idx[4, 0] + 1), len(prices)):

    ohlc = prices[:i, :]
    flag, temp = GeoABCD(ohlc, idx)
    # ax = PlotOHLC(prices[:67, :], dates)
    # plt.show()

    if any(flag) != 0:
        crop = int(temp[4, 0] - temp[0, 0])
        ohlc2 = prices.copy()
        ohlc2 = ohlc2[i-crop-1:i+16, :]
        temp[:, 0] = np.subtract(temp[:, 0], temp[0, 0])

        loc = 0
        name = ['Gartley', 'Crab', 'Bat', 'Butterfly']
        for j in range(0, 4):
            if flag[j] != 0:
                loc = j
                break

        # if flag[loc] == 1:
        #     pips += 1000 * (prices[(i+1):(i+16), 3] - prices[i, 3])
        # else:
        #     pips += 1000 * (prices[i, 3] - prices[(i+1):(i+16), 3])



        ax = PlotOHLC(ohlc2, dates, name=name[loc])
        plt.plot(temp[:, 0], temp[:, 1], c='b')
        plt.show()




# print(pips)