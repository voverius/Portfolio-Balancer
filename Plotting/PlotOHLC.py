import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import numpy as np


def PlotOHLC(prices, dates, name='test', time=False):

    """
    :param prices:  OHLC matrix
    :param dates:   dates in str format
    :param name:    plot name
    :param time:    True/False - x axis in date format/sequential
    :return:
    """

    # Setting up the variables
    fig, ax = plt.subplots()
    temp = np.zeros((len(prices), 5))

    if time:
        dates = mdates.datestr2num(dates)
        temp[:, 0] = dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y %Hh'))
        width = 0.02
    else:
        temp[:, 0] = np.arange(len(prices))
        width = 0.4

    temp[:, 1:5] = prices[:, 0:4]

    # Preparing the plot
    candlestick_ohlc(ax, temp, width=width, colorup='g', colordown='r')

    for label in ax.xaxis.get_ticklabels():
        label.set_rotation(45)

    ax.xaxis.set_major_locator(mticker.MaxNLocator(10))
    # ax.grid(True)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(name)
    plt.legend()
    # plt.show()

    return ax


if __name__ == "__main__":
    PlotOHLC()

