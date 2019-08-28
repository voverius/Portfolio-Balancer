import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter


def PlotBacktest(prices, portfolio_vector, time_values, signal_gap=10, name=''):

    '''
    :param prices:              The matrix with actual prices from the market
    :param portfolio_vector:    Predicted and invested matrix into an asset
    :param time_values:         Time values from the pandas matrix of the original prices
    :param signal_gap:          At what interval to check for peaks&troughs in the portfolio_vector
    :param name:                Name of the asset that is being shown. e.g. BTC
    :return:                    Plot the 3 curves
    '''

    # FILTERING OUT THE CONSECUTIVE BUY/SELL SIGNALS
    # -----------------------------------------------------------------------------------------------------------------
    imax = np.array([])
    imin = np.array([])

    cp = 0  # Current Position
    signal_gap = signal_gap/100  # convert back from percentage
    flag = False  # False - last sold (no holdings), True - last bought (holding)
    skip = False  # how many steps to skip

    for i in range(0, portfolio_vector.shape[0] - 2):

        if skip:
            skip = False
            continue

        # Check if growing
        if portfolio_vector[i] > cp + signal_gap:

            # Check if next is not SELL
            if portfolio_vector[i + 1] > portfolio_vector[i] - signal_gap:
                # If still growing
                if portfolio_vector[i + 1] > portfolio_vector[i] + signal_gap:

                    if portfolio_vector[i + 2] > portfolio_vector[i + 1] + signal_gap:
                        skip = True
                        continue
                    continue

                # If still growing, but further down (in case of a small kink on a mountain profile)
                elif portfolio_vector[i + 2] > portfolio_vector[i] + signal_gap:
                    skip = True
                    continue

            # Check in case it is double BUY
            if not flag:
                imax = np.append(imax, i)
            else:
                imax[-1] = i

            cp = portfolio_vector[i]
            flag = True

        # Check if shrinking
        elif portfolio_vector[i] < cp - signal_gap:

            # Check if not BUY
            if portfolio_vector[i + 1] < portfolio_vector[i] + signal_gap:
                if portfolio_vector[i + 1] < portfolio_vector[i] - signal_gap:

                    if portfolio_vector[i + 2] < portfolio_vector[1] - signal_gap:
                        skip = True
                        continue
                    continue

                # If still shrinking, but further down (in case of a small kink on a mountain profile)
                elif portfolio_vector[i + 2] < portfolio_vector[i] - signal_gap:
                    skip = True
                    continue

            # Check in case it is double SELL
            if flag:
                imin = np.append(imin, i)
            else:
                imin[-1] = i

            cp = portfolio_vector[i]
            flag = False

        # Adjust the price if not in the range of the signal filter
        elif portfolio_vector[i] > cp and flag or portfolio_vector[i] < cp and not flag:
            cp = portfolio_vector[i]

    imax = imax.astype(int)
    imin = imin.astype(int)

    # CUTTING OFF USELESS EDGES FROM THE DATA
    # -----------------------------------------------------------------------------------------------------------------

    # run_off = 5
    # sp = 0
    # fp = prices.shape[0]
    #
    # if imax[-1] > imin[-1]:
    #     if imax[-1] < fp - run_off:
    #         fp = imax[-1] + run_off
    # else:
    #     if imin[-1] < fp - run_off:
    #         fp = imax[-1] + run_off
    #
    # if imax[0] > run_off:
    #     sp = imax[0] - run_off
    #     imin = imin - (imax[0] - run_off)
    #     imax = imax - (imax[0] - run_off)
    #
    # prices = prices[sp:fp]
    # portfolio_vector = portfolio_vector[sp:fp]
    # time_values = time_values[sp:fp]

    # CALCULATING THE RETURN OF THE GIVEN ASSET
    # -----------------------------------------------------------------------------------------------------------------
    cv = np.ones(portfolio_vector.shape[0])

    for i in range(1, cv.shape[0]):
        price_change = prices[i] / prices[i - 1]
        cv[i] = cv[i - 1] * (1 + (price_change - 1) * portfolio_vector[i - 1])

    # STARTING TO CONSTRUCT THE PLOT
    # -----------------------------------------------------------------------------------------------------------------

    # Format into percentage
    cv -= 1
    cv *= 100
    portfolio_vector *= 100

    plt.style.use('seaborn')
    fig, ax = plt.subplots(nrows=3, ncols=1, sharex=True)

    ax[0].plot(prices)
    ax[0].scatter(imax, prices[imax], color='green', s=25)
    ax[0].scatter(imin, prices[imin], color='red', s=25)
    ax[0].grid(True)

    ax[1].plot(portfolio_vector)
    ax[1].scatter(imax, portfolio_vector[imax], color='green', s=25)
    ax[1].scatter(imin, portfolio_vector[imin], color='red', s=25)
    ax[1].yaxis.set_major_formatter(PercentFormatter())
    ax[1].grid(True)

    ax[2].plot(cv)
    ax[2].scatter(imax, cv[imax], color='green', s=25)
    ax[2].scatter(imin, cv[imin], color='red', s=25)
    ax[2].yaxis.set_major_formatter(PercentFormatter())
    ax[2].grid(True)

    # Setting the X ticks
    spacing = np.linspace(0, 1, 11)
    time_locations = np.around(spacing*prices.shape[0])
    time_locations = time_locations.astype(int)
    time_locations[-1] -= 1
    time_labels = [time_values[i] for i in time_locations]
    plt.xticks(time_locations, time_labels, rotation=20)
    fig.autofmt_xdate()

    fig.suptitle(name)

    # This makes full screen
    figManager = plt.get_current_fig_manager()
    figManager.full_screen_toggle()

    plt.show()


if __name__ == "__main__":
    PlotBacktest()

