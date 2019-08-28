# import numpy as np
# from time import time
from multiprocessing import Pool
from functools import partial

from Development.loader import *

from AnalysisTechnical.GetBB import *
from AnalysisTechnical.GetCCI import *
from AnalysisTechnical.GetDetrended import *
# from AnalysisTechnical.GetEMA import *
from AnalysisTechnical.GetHA import *
from AnalysisTechnical.GetMACD import *
from AnalysisTechnical.GetMM import *
from AnalysisTechnical.GetMOM import *
from AnalysisTechnical.GetPRC import *
from AnalysisTechnical.GetRSI import *
from AnalysisTechnical.GetS import *
from AnalysisTechnical.GetSLOPE import *
from AnalysisTechnical.GetSMA import *
from AnalysisTechnical.GetSTD import *
from AnalysisTechnical.GetW import *
from AnalysisTechnical.GetWAD import *


def MasterTA(threads=20):

    """
    # :param pairs:   A list of specific pairs to be updated/created
    # :param mode:    Technical Analysis can either be created from scratch or updated (once it already exists)
    :param threads: For MultiProcessing how many threads to run the code on (base is 20)

    :return:        NO OUTPUT. All TA matrices are saved to a designated folder

    Description:    This program goes through all specified pairs and creates Technical Analysis parameters for all
                    of them. This is then stores as a numpy matrix that is the size of the smallest TA.
    """

    t = time()

    # List of parameters used for the TAs
    BBkey = [15]
    CCIkey = [15]
    EMAkey = [25, 50, 100, 200]
    HAkey = [15]
    MACDkey = [12, 26, 9]
    MOMkey = [3, 4, 5, 8, 9, 10]
    PRCkey = [12, 13, 14, 15]
    RSIkey = [9, 14]
    Skey = [3, 4, 5, 8, 9, 10]
    SLOPEkey = [3, 4, 5, 10, 20, 30]
    Wkey = [15]
    WADkey = [15]

    # List of shared parameters
    MMkey = [3, 4, 5, 8, 9, 10, 15]  # Min Max
    SMAkey = [15, 25, 50, 100, 200]  # Original 25, 50, 100, 200
    STDkey = [15]                    # Standard Deviation

    # ###################################################################################################
    # ---------------------------------   START OF SHARED INDICATORS   ----------------------------------
    # ###################################################################################################

    master = loader()
    p = Pool(processes=threads)

    # ----------------------------------------------------------------------------------------------------
    #                               Detrended

    i = 0
    output_list = p.map(GetDetrended, master.values())

    for key in master:
        master[key]['detrended'] = output_list[i]
        i = i + 1

    # ----------------------------------------------------------------------------------------------------
    #                               MM - Min Max

    i = 0
    temp = partial(GetMM, periods=MMkey)
    output_list = p.map(temp, master.values())

    for key in master:
        master[key]['mm'] = output_list[i]
        i = i + 1

    # ----------------------------------------------------------------------------------------------------
    #                               SMA - Simple Moving Average

    temp = partial(GetSMA, periods=SMAkey)
    output_list = p.map(temp, master.values())

    for key in master:
        master[key]['sma'] = output_list[i]
        i = i + 1

    # ----------------------------------------------------------------------------------------------------
    #                               STD - Standard Deviation

    i = 0
    temp = partial(GetSTD, periods=STDkey)
    output_list = p.map(temp, master.values())

    for key in master:
        master[key]['std'] = output_list[i]
        i = i + 1

    # ###################################################################################################
    # ---------------------------------   FINISH OF SHARED ONES   ---------------------------------------
    # ###################################################################################################

    #                                   BB - Bullinger Bands

    i = 0
    temp = partial(GetBB, periods=BBkey)
    output_list = p.map(temp, master.values())

    for key in master:
        master[key]['bb'] = output_list[i]
        i = i + 1

    # ----------------------------------------------------------------------------------------------------
    #                                   CCI - Commodity Channel Index

    i = 0
    temp = partial(GetCCI, periods=CCIkey)
    output_list = p.map(temp, master.values())

    for key in master:
        master[key]['cci'] = output_list[i]
        i = i + 1

    # ----------------------------------------------------------------------------------------------------
    #                                   EMA - Exponential Moving Average

    i = 0
    temp = partial(GetEMA, periods=EMAkey)
    output_list = p.map(temp, master.values())

    for key in master:
        master[key]['ema'] = output_list[i]
        i = i + 1

    # ----------------------------------------------------------------------------------------------------
    #                                   HA - Haiken Ashi Candles

    i = 0
    temp = partial(GetHA, periods=HAkey)
    output_list = p.map(temp, master.values())

    for key in master:
        master[key]['ha'] = output_list[i]
        i = i + 1

    # ----------------------------------------------------------------------------------------------------
    #                                   MACD - Moving Average Convergence Divergence

    i = 0
    temp = partial(GetMACD, periods=MACDkey)
    output_list = p.map(temp, master.values())

    for key in master:
        master[key]['macd'] = output_list[i]
        i = i + 1

    # ----------------------------------------------------------------------------------------------------
    #                                  MOM - Momentum Indicator

    i = 0
    temp = partial(GetMOM, periods=MOMkey)
    output_list = p.map(temp, master.values())

    for key in master:
        master[key]['mom'] = output_list[i]
        i = i + 1

    # ----------------------------------------------------------------------------------------------------
    #                                  PRC - Price Rate of Change

    i = 0
    temp = partial(GetPRC, periods=PRCkey)
    output_list = p.map(temp, master.values())

    for key in master:
        master[key]['prc'] = output_list[i]
        i = i + 1

    # ----------------------------------------------------------------------------------------------------
    #                                  RSI - Relative Strength Index

    i = 0
    temp = partial(GetRSI, periods=RSIkey)
    output_list = p.map(temp, master.values())

    for key in master:
        master[key]['rsi'] = output_list[i]
        i = i + 1

    # ----------------------------------------------------------------------------------------------------
    #                                  S - Stochastic Indicator

    i = 0
    temp = partial(GetS, periods=Skey)
    output_list = p.map(temp, master.values())

    for key in master:
        master[key]['s'] = output_list[i]
        i = i + 1

    # ----------------------------------------------------------------------------------------------------
    #                                  Slope - over given periods

    i = 0
    temp = partial(GetSLOPE, periods=SLOPEkey)
    output_list = p.map(temp, master.values())

    for key in master:
        master[key]['slope'] = output_list[i]
        i = i + 1

    # ----------------------------------------------------------------------------------------------------
    #                                  W - Williams Indicator

    i = 0
    temp = partial(GetW, periods=Wkey)
    output_list = p.map(temp, master.values())

    for key in master:
        master[key]['w'] = output_list[i]
        i = i + 1

    # ----------------------------------------------------------------------------------------------------
    #                                  WAD - William Accumulation Distribution

    i = 0
    temp = partial(GetWAD, periods=WADkey)
    output_list = p.map(temp, master.values())

    for key in master:
        master[key]['wad'] = output_list[i]
        i = i + 1

    # ----------------------------------------------------------------------------------------------------
    print('-------------------------------------------------')
    print(f'TOTAL TIME TAKEN: {np.round(time() - t, 2)}s, FOR {len(master)} PAIRS, WITH {threads} CORES')


if __name__ == '__main__':
    MasterTA()
