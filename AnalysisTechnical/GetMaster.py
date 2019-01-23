from AnalysisTechnical.GetBB import *
from AnalysisTechnical.GetCCI import *
from AnalysisTechnical.detrend import *
from AnalysisTechnical.GetEMA import *
from AnalysisTechnical.GetFF import *
from AnalysisTechnical.GetHA import *
from AnalysisTechnical.GetMACD import *
from AnalysisTechnical.GetMOM import *
from AnalysisTechnical.GetPRC import *
from AnalysisTechnical.GetRSI import *
from AnalysisTechnical.GetS import *
from AnalysisTechnical.GetSLOPE import *
from AnalysisTechnical.GetSMA import *
from AnalysisTechnical.GetW import *
from AnalysisTechnical.GetWAD import *

from DataManagement.ConvertToPandas import *
from DataManagement.RemoveDuplicates import *
from DataManagement.GetCSV import *
from DataManagement.SaveCSV import *

import time
t0 = time.time()


def GetMaster(name='EURUSD2'):

    """
    :param name:    Name of the CSV file to open
    :return:        Dataframe with all of the Technical Indicators
    """

    prices, dates = GetCSV(name)
    prices, dates = RemoveDuplicates(prices, dates)

    # List of parameters used for the TAs
    BBkey = [15]
    CCIkey = [15]
    EMAkey = [25, 50, 100]
    Dkey = [15]
    FFkey = [10, 20, 30]
    SFkey = [3, 5]
    HAkey = [15]
    MACDkey = [12, 26, 9]
    MOMkey = [3, 4, 5, 8, 9, 10]
    PRCkey = [12, 13, 14, 15]
    RSIkey = [9, 14]
    Skey = [3, 4, 5, 8, 9, 10]
    SLOPEkey = [3, 4, 5, 10, 20, 30]
    SMAkey = [25, 50, 100]
    Wkey = [15]
    WADkey = [15]

    keys = [BBkey, CCIkey, EMAkey, Dkey, FFkey, SFkey, HAkey, MACDkey, MOMkey, PRCkey, RSIkey,
            Skey, SLOPEkey, SMAkey, Wkey, WADkey]

    # Generating the Technical Indicators
    BB = GetBB(prices, BBkey)
    CCI = GetCCI(prices, CCIkey)
    EMA = GetEMA(prices, EMAkey)
    D = detrend(prices, Dkey)

    # FF = GetFF(prices, FFkey)
    # SF = GetSF(prices, SFkey)
    FF = GetSMA(prices, FFkey)
    SF = GetSMA(prices, SFkey)

    HA = GetHA(prices, HAkey)
    MACD = GetMACD(prices, MACDkey)
    MOM = GetMOM(prices, MOMkey)
    PRC = GetPRC(prices, PRCkey)
    RSI = GetRSI(prices, RSIkey)
    S = GetS(prices, Skey)
    SLOPE = GetSLOPE(prices, SLOPEkey)
    SMA = GetSMA(prices, SMAkey)
    W = GetW(prices, Wkey)
    WAD = GetWAD(prices, WADkey)

    TIs = [BB, CCI, EMA, D, FF, SF, HA, MACD, MOM, PRC, RSI, S, SLOPE, SMA, W, WAD]
    IDs = ['BB', 'CCI', 'EMA', 'D', 'FF', 'SF', 'HA', 'MACD', 'MOM', 'PRC', 'RSI',
           'S', 'SLOPE', 'SMA', 'W', 'WAD']
    fid = []  # This will store the final names

    # Putting all of the Technical Indicators in a MasterMatrix
    master = ConvertToPandas(prices, dates, 'OHLC')

    for i in range(0, len(TIs)):
        if len(TIs[i][keys[i][0]].shape) == 1:
            for j in range(0, len(keys[i])):
                name = IDs[i] + ': ' + str(keys[i][j])
                fid.append(name)

                loc = keys[i][j]
                temp = ConvertToPandas(TIs[i][loc], dates, name)
                master[name] = temp
        else:
            if IDs[i] == 'BB':
                name2 = ['upper', 'SMA', 'lower']
            elif IDs[i] == 'FF':
                name2 = ['a0', 'a1', 'b1', 'w']
            elif IDs[i] == 'SF':
                name2 = ['a0', 'b1', 'w']
            elif IDs[i] == 'HA':
                name2 = ['Open', 'High', 'Low', 'Close']
            elif IDs[i] == 'MACD':
                name2 = ['macd', 'signal', 'difference']
            elif IDs[i] == 'MOM':
                name2 = ['close', 'open']
            else:
                name2 = []
                print('unknown Technical Indicator')

            for j in range(0, len(keys[i])):
                name = [None] * len(name2)
                for k in range(0, len(name2)):
                    name[k] = IDs[i] + ' ' + name2[k] + ': ' + str(keys[i][j])
                    fid.append(name[k])

                keys[7] = [keys[7][0]]  # MACD is indexed by the first period
                loc = keys[i][j]
                temp = ConvertToPandas(TIs[i][loc], dates, name)
                master[name] = temp

    # path = SaveCSV('test')
    # master.to_csv(path)

    return master


if __name__ == "__main__":
    GetMaster()
