from time import time
import numpy as np

from MarketData.GetPoloniexData import *
from MarketData.ChangeDataPeriod import *


def GetMarketData(periods=[], pairs=[]):

    if len(periods) == 0:
        periods = ['15M', '30M', '1H', '4H', '1D']

    if len(pairs) == 0:
        option = 'UpdateAll'
    else:
        option = 'Update'

    if '1H' in periods:
        GetPoloniexData(option=option, loc='30M', pairs=pairs)
        ChangeDataPeriod(original_loc='30M', new_loc='1H', pairs=pairs)

        periods.remove('1H')
        if '30M' in periods:
            periods.remove('30M')

    for period in periods:
        GetPoloniexData(option=option, loc=period, pairs=pairs)


if __name__ == "__main__":
    GetMarketData()











