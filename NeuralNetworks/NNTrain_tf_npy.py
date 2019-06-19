from time import time
import tensorflow as tf
import tflearn
import numpy as np
import os


class NNTrain:
    def __init__(self, config, agent, data, model_option='train', save=True, load_pvm=False):

        '''
        :param config:          Config file with all the parameters
        :param agent:           NNAgent class created from scratch
        :param data:            Data class contains all the training/testing data and batches
        :param model_option:    Train - train from scratch, Load - load an already developed model
        :param save:            Save the newly trained model
        :param load_pvm:        Load the previously saved PVM file
        '''

        self.config = config
        self.agent = agent
        self.data = data

        self.log_file_dir = 'D:\\OneDrive\Trade\\Daft Punk\\TrainingPackages\\' + str(config['package']) + \
                            '\\tensorboard'
        self.save_path = 'D:\\OneDrive\Trade\\Daft Punk\\TrainingPackages\\' + str(config['package']) + '\\'

        self.tensor_board = self.initialize_tensor_board()
        start_time = time()

        # if model_option == 'train':
        #
        #     total_epochs = self.config['training']['epochs']
        #
        #     # Load the previously saved PVM file
        #     if os.path.isfile(self.save_path + 'PVM.npy') and load_pvm:
        #         self.data.PVM = np.load(self.save_path + 'PVM.npy')
        #
        #     print(f'Start TRAINING the model with {total_epochs} epochs and {self.data.PVM.shape[0]} data lines')
        #     for epoch in range(0, total_epochs):
        #         t0 = time()
        #         results = self.train_epoch()
        #         print(f'finished {epoch + 1}/{total_epochs} epochs, time taken: {round(time() - t0, 1)}s '
        #               f'test_pv = {round(results[0][1].astype(float), 2)}, '
        #               f'last deviation = {round(np.var(results[0][5][-1, :]) * 100, 5)}')
        #
        #     if save:
        #         self.agent.saver.save(sess=self.agent.network.session, save_path=(self.save_path + 'netfile'))
        #         np.save((self.save_path + 'PVM.npy'), self.data.PVM)
        #
        #     print('total time: ', time() - start_time)
        #
        if model_option == 'load':
            # Loading the network with weights
            loc = 'D:\\OneDrive\\Trade\\Daft Punk\\TrainingPackages\\' + str(config['package']) + '\\'
            meta = loc + 'netfile.meta'
            saver = tf.train.import_meta_graph(meta)
            saver.restore(sess=self.agent.network.session, save_path=tf.train.latest_checkpoint(loc))

            # Loading the data.PVM pickle
            # self.data.PVM = pd.read_pickle(self.save_path + '_PVM.pkl')

    # ---------------------------------------------------------------------------------------------------
    def train_epoch(self):

        # Preparing the batches
        random_batch_indexes = np.arange(self.data.train_data['x'].shape[0])
        np.random.shuffle(random_batch_indexes)
        training_batches = self.data.create_batches(random_batch_indexes)

        tflearn.is_training(True, self.agent.network.session)
        for batch in training_batches:
            self.eval_tensors(batch=batch, tensors=self.agent.train_operation, net=self.agent.network)
        tflearn.is_training(False, self.agent.network.session)

        # Evaluate the Epoch:
        testing_tensors = [self.tensor_board['summary'], self.agent.portfolio_value, self.agent.log_mean,
                           self.agent.loss, self.agent.log_mean_free, self.agent.network.output_layer]

        results = self.eval_tensors(batch=self.data.test_data, tensors=testing_tensors, net=self.agent.network)
        result_dict = {'summary': results[0][0],
                       'v_pv': results[0][1],
                       'v_log_mean': results[0][2],
                       'v_loss': results[0][3],
                       'log_mean_free': results[0][4],
                       'weights': results[0][5]}

        # self.tensor_board['test_writer'].add_summary(result_dict['summary'], 1)  # instead of 1 should be 'epoch'

        return results

    # ---------------------------------------------------------------------------------------------------
    def eval_tensors(self, batch, tensors, net):
        '''
        :param batch:       raw data for the input
        :param tensors:     a list of tensors
        :param net:         network agent
        :return:
        '''

        tensors = [tensors, self.agent.network.output_layer]

        # This part checks if any of the numbers are NaN
        assert not np.any(np.isnan(batch['x']))
        assert not np.any(np.isnan(batch['y']))
        assert not np.any(np.isnan(batch['last_w'])), "the last_w is {}".format(batch['last_w'])

        '''
        This below actually evaluates the given data over given tensors
        '''
        feed_dict = {self.agent.network.input_tensor: batch['x'],
                     self.agent.y: batch['y'],
                     self.agent.network.previous_w: self.data.PVM[batch['last_w'], :],
                     self.agent.network.input_num: batch['x'].shape[0]}

        results = net.session.run(tensors, feed_dict=feed_dict)

        # placing part of the results into data.PVM... placed matrix is the size of batch_size*coin_number
        if 'last_w' in batch:
            self.data.PVM[(batch['last_w'] + 1), :] = results[-1][:, 1:]

        return results[:-1]

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