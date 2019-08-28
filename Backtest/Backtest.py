from time import time
import tflearn
import numpy as np
from os import listdir
import tensorflow as tf
from os.path import isfile, join
from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter


class backtest:
    def __init__(self, config, agent, train, data, rolling=False, export=False, plot=True):
        '''
        :param config:
        :param agent:
        :param data:
        :param rolling_training:
        :param export:
        '''

        print('START - Backtest.py')

        self.config = config
        self.agent = agent
        self.train = train
        self.data = data

        self.save_path = 'D:\\OneDrive\Trade\\Daft Punk\\TrainingPackages\\' + str(config['package']) + '\\'

        self.total_steps = self.data.test_data['y'].shape[0]
        self.coin_quantity = self.data.test_data['y'].shape[1]
        self.last_omega = self.data.last_omega.copy()

        self.predictions = np.zeros((self.total_steps, self.coin_quantity + 1))
        self.future_data = np.zeros((self.total_steps, self.coin_quantity + 1))
        self.total_capital = np.zeros((self.total_steps + 1, self.coin_quantity + 1))
        self.total_capital[0, :] = 1
        self.commissions = np.zeros(self.total_steps)
        self.portfolio_change = np.zeros(self.total_steps)
        total_epochs = self.config['training']['epochs']

        flag = True
        finished_epochs = 0
        self.data.PVM = np.load(self.save_path + 'PVM.npy')

        saver = tf.train.import_meta_graph(self.save_path + 'netfile.meta')
        saver.restore(sess=self.agent.network.session, save_path=tf.train.latest_checkpoint(self.save_path))

        test_pv = 0

        while flag:

            # flag2 = True
            #
            # while flag2:
            #     t0 = time()
            #     results = self.train.train_epoch()
            #     if results[0][1].astype(float) > test_pv:
            #         test_pv = round(results[0][1].astype(float), 2)
            #         self.agent.saver.save(sess=self.agent.network.session, save_path=(self.save_path + 'netfile'))
            #         finished_epochs += 1
            #         flag2 = False
            #     else:
            #         self.agent.saver.restore(sess=self.agent.network.session,
            #                                  save_path=tf.train.latest_checkpoint(self.save_path))
            #     print(f'finished {finished_epochs} epochs, time taken: {round(time() - t0, 1)}s '
            #           f'test_pv = {round(results[0][1].astype(float), 2)}, '
            #           f'last deviation = {round(np.var(results[0][5][-1, :]) * 100, 5)}')

            for i in range(0, 20):
                t0 = time()
                results = self.train.train_epoch()
                finished_epochs += 1
                print(f'finished {finished_epochs} epochs, time taken: {round(time() - t0, 1)}s '
                      f'test_pv = {round(results[0][1].astype(float), 2)}, '
                      f'last deviation = {round(np.var(results[0][5][-1, :]) * 100, 5)}')

            for i in range(self.total_steps):

                predicted_omega = self.decide_by_history(self.data.test_data["x"][i], self.last_omega)
                future_price = np.concatenate((np.ones(1), self.data.test_data['y'][i, :, 3]))

                self.predictions[i, :] = predicted_omega
                self.future_data[i, :] = future_price

                commissioned_omega, self.commissions[i] = self.calculate_trades(predicted_omega,
                                                                                self.last_omega,
                                                                                self.data.commission_rate)
                future_omega = commissioned_omega * future_price

                self.total_capital[i + 1, -1] = self.total_capital[i, -1] * np.sum(future_omega)
                for j in range(0, self.coin_quantity):
                    self.total_capital[i+1, j] = self.total_capital[i, j]*(1 + (future_price[j+1] - 1)*future_omega[j+1])

                if rolling:
                    self.rolling_train(i)

                self.last_omega = future_omega / np.sum(future_omega)

            # self.total_capital = np.delete(self.total_capital, 0, 0)

            if plot:
                plt.style.use('seaborn')
                fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)

                temp = self.total_capital[:, -1].copy()

                ax[0].plot(temp)
                ax[0].grid(True)
                ax[0].set_yscale('log')

                temp -= 1
                temp *= 100
                ax[1].plot(temp)
                ax[1].yaxis.set_major_formatter(PercentFormatter())
                ax[1].grid(True)

                time_values = self.data.global_data['datestamps'][-self.total_steps:]
                spacing = np.linspace(0, 1, 11)
                time_locations = np.around(spacing * self.total_steps)
                time_locations = time_locations.astype(int)
                time_locations[-1] -= 1
                time_labels = [time_values[i] for i in time_locations]
                plt.xticks(time_locations, time_labels, rotation=20)
                fig.autofmt_xdate()

                fig.suptitle(f'Portfolio Change from {time_values[0]} to {time_values[-1]}, '
                             f'with {self.coin_quantity} assets & {finished_epochs} epochs', fontsize=16)

                # figManager = plt.get_current_fig_manager()
                # figManager.full_screen_toggle()

                # if export:
                #     plt.savefig(self.save_path + 'profit - ' + str(int(round(max(temp)))) + '-percent.png')
                # plt.show()

            if export:

                # file_list = [f for f in listdir(self.save_path) if isfile(join(self.save_path, f))]
                file_list = listdir(self.save_path)
                save_flag = False

                if 'summary.npy' in file_list:
                    summary = np.load(self.save_path + 'summary.npy')
                    if self.total_capital[-1, -1] > (summary[0] * 1.03):
                        save_flag = True
                    else:
                        print(f'Epoch NOT SAVED. Previous profit - {np.round((summary[0] - 1) * 100, 1)}%, '
                              f'new profit - {np.round((self.total_capital[-1, -1] - 1) * 100, 1)}%')
                else:
                    save_flag = True

                if save_flag:
                    print(f'Model saved with internal improvemets of'
                          f' {np.round((self.total_capital[-1, -1] / summary[0] - 1) * 100, 1)}%')

                    self.agent.saver.save(sess=self.agent.network.session, save_path=(self.save_path + 'netfile'))
                    summary = np.array([self.total_capital[-1, -1],
                                        finished_epochs,
                                        round(np.var(results[0][5][-1, :]) * 100, 5),
                                        np.round(np.var(self.total_capital[-1, :-1]) * 100, 5)])
                    np.save((self.save_path + "PVM.npy"), self.data.PVM)
                    np.save((self.save_path + "summary.npy"), summary)
                    np.save((self.save_path + "bt_predictions.npy"), self.predictions)
                    np.save((self.save_path + "bt_future_data.npy"), self.future_data)
                    np.save((self.save_path + "bt_total_capital.npy"), self.total_capital)
                    plt.savefig(self.save_path + 'plot.png')
                    plt.close()

                else:
                    plt.close()

            if finished_epochs >= total_epochs:
                flag = False
            elif finished_epochs >= 140 and (np.var(results[0][5][-1, :]) * 100) < 1:
                flag = False
                print(f'Quit training because the last deviation after {finished_epochs} epochs is still - '
                      f'{round(np.var(results[0][5][-1, :]) * 100, 5)}')

    # ---------------------------------------------------------------------------------------------------
    def decide_by_history(self, history, last_omega):

        '''
        :param history:     Input into NN to give the prediction
        :param last_omega:  the last prediction/capital allocation
        :return:            a matrix of 11 vectors on how to distribute 100% of the capital
        '''

        assert isinstance(history, np.ndarray), "the history should be a numpy array, not %s" % type(history)
        assert not np.any(np.isnan(last_omega))
        assert not np.any(np.isnan(history))

        tflearn.is_training(False, self.agent.network.session)
        history = history[np.newaxis, :, :, :]
        feed_dict = {self.agent.network.input_tensor: history,
                     self.agent.network.previous_w: last_omega[np.newaxis, 1:],
                     self.agent.network.input_num: 1}
        result = self.agent.network.session.run(self.agent.network.output_layer, feed_dict=feed_dict)
        result = np.squeeze(result)  # This eliminates arbitrary axis
        return result

    # ---------------------------------------------------------------------------------------------------
    def calculate_trades(self, omega, last_omega, cr):
        '''
        :param omega:       predicted portfolio vector target
        :param last_omega:  current portfolio vector
        :param cr:          commission ratio
        :return:            new portfolio vector with commission already rate paid & total commission paid
        '''

        # FUTURE NOTE:
        # Check if the trade is big enough and if it's worth it

        commissioned_omega = np.zeros(omega.shape[0])
        commissioned_omega[0] = omega[0]  # The base value does not get traded, only the other assets do
        commissions = np.zeros(omega.shape[0])

        for i in range(1, omega.shape[0]):
            commissions[i] = abs(omega[i] - last_omega[i])*cr
            commissioned_omega[i] = omega[i] - commissions[i]

        total_commission = commissions.sum()

        return commissioned_omega, total_commission

    # ---------------------------------------------------------------------------------------------------
    def rolling_train(self, index):

        tflearn.is_training(True, self.agent.network.session)

        tensors = [self.agent.train_operation, self.agent.network.output_layer]

        feed_dict = {self.agent.network.input_tensor:   self.data.test_data["x"][index][np.newaxis, :, :, :],
                     self.agent.y:                      self.data.test_data["y"][index][np.newaxis, :, :],
                     self.agent.network.previous_w:     self.last_omega[np.newaxis, 1:],
                     self.agent.network.input_num:      self.data.test_data["x"][index][np.newaxis, :, :, :].shape[0]}

        results = self.agent.network.session.run(tensors, feed_dict=feed_dict)

        tflearn.is_training(False, self.agent.network.session)






