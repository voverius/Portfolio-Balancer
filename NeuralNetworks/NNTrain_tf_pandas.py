from time import time
import tensorflow as tf
import tflearn
import numpy as np
import pandas as pd


class NNTrain:
    def __init__(self, config, agent, data, model_option='train', save=True):

        '''
        :param config:          Config file with all the parameters
        :param agent:           NNAgent class created from scratch
        :param data:            Data class contains all the training/testing data and batches
        :param model_option:    Train - train from scratch, Load - load an already developed model
        :param save:            Save the newly trained model
        '''

        self.config = config
        self.agent = agent
        self.data = data

        start_time = time()
        tflearn.is_training(True, self.agent.network.session)
        self.log_file_dir = 'D:\\OneDrive\Trade\\Daft Punk\\TrainingPackages\\' + str(config['package']) +\
                            '\\tensorboard'
        self.save_path = 'D:\\OneDrive\Trade\\Daft Punk\\TrainingPackages\\' + str(config['package']) +\
                         '\\netfile'
        tensor_board = self.initialize_tensor_board()

        if model_option == 'train':
            t0 = time()

            print('-----------------------------START FIRST LOOP-------------------------------')
            # start 80 000 loop:
            # for i in range(config['training']["steps"]):
            for epoch in range(0, 1):

                random_batch_indexes = np.arange(self.data.train_data['x'].shape[0])
                np.random.shuffle(random_batch_indexes)
                train_batches = self.data.create_batches(random_batch_indexes)

                for i in range(len(data.train_batches)):

                    batch = data.train_batches[random_batch[i]]

                    self.eval_tensors(batch=batch, tensors=self.agent.train_operation, net=self.agent.network)

                    if i % 1000 == 0:
                        tflearn.is_training(False, self.agent.network.session)

                        testing_tensors = [tensor_board['summary'], self.agent.portfolio_value, self.agent.log_mean,
                                           self.agent.loss, self.agent.log_mean_free, self.agent.network.output_layer]
                        results = self.eval_tensors(batch=self.data.test_data, tensors=testing_tensors,
                                                    net=self.agent.network)
                        result_dict = {'summary': results[0][0],
                                       'v_pv': results[0][1],
                                       'v_log_mean': results[0][2],
                                       'v_loss': results[0][3],
                                       'log_mean_free': results[0][4],
                                       'weights': results[0][5]}

                        tensor_board['test_writer'].add_summary(result_dict['summary'], i)
                        tflearn.is_training(True, self.agent.network.session)

                        if save:
                            self.agent.saver.save(self.agent.network.session, self.save_path)

                    if i % 8000 == 0:
                        t1 = time()
                        print(f'{i}th loop progressing, time taken: {t1-t0}')
                        t0 = time()

                t3 = time()
                print('   ')
                print(f'finished the {epoch}th, time taken: {t3-t2}')

            # Saving all the variables
            if save:
                # self.data.PVM.to_pickle(self.save_path + '_PVM.pkl')
                self.agent.saver.save(sess=self.agent.network.session, save_path=self.save_path)
            finish_time = time()
            print('total time: ', finish_time-start_time)

        elif model_option == 'load':
            # Loading the network with weights
            # sess = tf.InteractiveSession()
            # loc = 'D:\\OneDrive\\Trade\\PGPortfolio\\my_development\\train_package\\2\\'
            loc = 'D:\\OneDrive\\Trade\\Daft Punk\\TrainingPackages\\' + str(config['package']) + '\\'
            meta = loc + 'netfile.meta'
            saver = tf.train.import_meta_graph(meta)
            saver.restore(sess=self.agent.network.session, save_path=tf.train.latest_checkpoint(loc))

            # Loading the data.PVM pickle
            # self.data.PVM = pd.read_pickle(self.save_path + '_PVM.pkl')

    # ---------------------------------------------------------------------------------------------------
    def initialize_tensor_board(self):

        tf.summary.scalar('benefit', self.agent.portfolio_value)
        tf.summary.scalar('log_mean', self.agent.log_mean)
        tf.summary.scalar('loss', self.agent.loss)
        tf.summary.scalar("log_mean_free", self.agent.log_mean_free)

        for layer_key in self.agent.network.layer_dict:
            tf.summary.histogram(layer_key, self.agent.network.layer_dict[layer_key])
        for var in tf.trainable_variables():
            tf.summary.histogram(var.name, var)

        grads = tf.gradients(self.agent.loss, tf.trainable_variables())
        for grad in grads:
            tf.summary.histogram(grad.name + '/gradient', grad)

        summary = tf.summary.merge_all()
        network_writer = tf.summary.FileWriter(self.log_file_dir + '/network', self.agent.network.session.graph)
        test_writer = tf.summary.FileWriter(self.log_file_dir + '/test')
        train_writer = tf.summary.FileWriter(self.log_file_dir + '/train')

        return {'summary': summary, 'network_writer': network_writer,
                'test_writer': test_writer, 'train_writer': train_writer}

    # ---------------------------------------------------------------------------------------------------
    def eval_tensors(self, batch, tensors, net):
        '''
        :param batch:       raw data for the input
        :param tensors:     a list of tensors
        :param net:         network agent
        :return:
        '''

        tensors = [tensors, self.agent.network.output_layer]

        assert not np.any(np.isnan(batch['x']))
        assert not np.any(np.isnan(batch['y']))
        assert not np.any(np.isnan(batch['last_w'])), "the last_w is {}".format(batch['last_w'])

        '''
        This below actually evaluates the given data over given tensors
        '''

        results = net.session.run(tensors, feed_dict={self.agent.network.input_tensor: batch['x'],
                                                      self.agent.y: batch['y'],
                                                      self.agent.network.previous_w: batch['last_w'],
                                                      self.agent.network.input_num: batch['x'].shape[0]})

        # placing part of the results into data.PVM... placed matrix is the size of batch*coin_no
        if 'index' in batch:
            # This part is for training
            end = batch['index'] + int(self.config['training']["batch_size"])
            self.data.PVM.iloc[batch['index']:end, :] = results[-1][:, 1:]
        else:
            #  This part is for testing/validation
            end = self.data.test_ind[-1] - int(self.config['input']["window_size"] - 1)
            self.data.PVM.iloc[self.data.test_ind[0]:end, :] = results[-1][:, 1:]

        return results[:-1]

    # ---------------------------------------------------------------------------------------------------
    def decide_by_history(self, history, last_omega):

        assert isinstance(history, np.ndarray), "the history should be a numpy array, not %s" % type(history)
        assert not np.any(np.isnan(last_omega))
        assert not np.any(np.isnan(history))

        tflearn.is_training(False, self.agent.network.session)
        history = history[np.newaxis, :, :, :]
        feed_dict = {self.agent.network.input_tensor: history, self.agent.network.previous_w: last_omega[np.newaxis, 1:],
                     self.agent.network.input_num: 1}
        result = self.agent.network.session.run(self.agent.network.output_layer, feed_dict=feed_dict)
        result = np.squeeze(result)  # This eliminates arbitrary axis
        return result

    # ---------------------------------------------------------------------------------------------------
    def calculate_pv_after_commission(self, w1, w0, cr):
        '''
        :param w1: target portfolio vector, first element is btc
        :param w0: rebalanced last period portfolio vector, first element is btc
        :param cr:  Commission Ratio
        :return:
        '''

        flag = False
        mu0 = 1
        mu1 = 1 - 2*cr + cr ** 2  # The cr^2 comes from the fact that on the second trade the commission rate is
        # applied to the smaller number than 1. This is equal to = (1-cr)*(1-cr) = (1-cr)^2

        # mu1 = (1 - cr * w0[0])/(1 - cr * w1[0])
        while abs(mu1-mu0) > 1e-10:
            mu0 = mu1
            mu1 = (1 - cr * w0[0] - (2 * cr - cr ** 2) *
                   np.sum(np.maximum(w0[1:] - mu1, 0))) / (1 - cr * w1[0])

            if flag:
                if mu0 != mu1:
                    a = 0
            flag = True
            if np.sum(np.maximum(w0[1:] - mu1, 0)) > 0:
                a = 0
        return mu1

    #
    #
    #
    def rolling_train(self, ):

        '''
        :return:
        '''






