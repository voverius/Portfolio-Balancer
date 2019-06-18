from NeuralNetworks.NNCreation_tf import *


class NNAgent:
    def __init__(self, config, data):

        coin_number = data.train_data['x'].shape[1]
        feature_number = data.train_data['x'].shape[2]
        window_size = data.train_data['x'].shape[3]

        self.network = NeuralNetwork(data=data, layers=config["layers"])

        global_step = tf.Variable(0, trainable=False)
        self.y = tf.placeholder(tf.float32, shape=[None, coin_number, feature_number])

        future_price = tf.concat([tf.ones([self.network.input_num, 1]), self.y[:, :, 3]], 1)
        future_omega = (future_price * self.network.output_layer) /\
                        tf.reduce_sum(future_price * self.network.output_layer, axis=1)[:, None]
        commission_ratio = config["trading"]["trading_consumption"]

        # Originally a separate program called __pure_pc
        w_t = future_omega[:self.network.input_num - 1]  # rebalanced
        w_t1 = self.network.output_layer[1:self.network.input_num]
        mu = 1 - tf.reduce_sum(tf.abs(w_t1[:, 1:] - w_t[:, 1:]), axis=1) * commission_ratio

        self.pv_vector = tf.reduce_sum(self.network.output_layer * future_price, reduction_indices=[1]) * \
                         (tf.concat([tf.ones(1), mu], axis=0))

        self.log_mean_free = tf.reduce_mean(tf.log(tf.reduce_sum(self.network.output_layer * future_price,
                                                                 reduction_indices=[1])))
        self.portfolio_value = tf.reduce_prod(self.pv_vector)
        self.mean = tf.reduce_mean(self.pv_vector)
        self.log_mean = tf.reduce_mean(tf.log(self.pv_vector))
        self.standard_deviation = tf.sqrt(tf.reduce_mean((self.pv_vector - self.mean) ** 2))
        self.sharp_ratio = (self.mean - 1) / self.standard_deviation

        self.loss = set_loss_function(config, self.network.output_layer, future_price,
                                      self.pv_vector, self.network.previous_w, commission_ratio)

        self.train_operation = init_train(learning_rate=config["training"]["learning_rate"],
                                          decay_steps=config["training"]["decay_steps"],
                                          decay_rate=config["training"]["decay_rate"],
                                          training_method=config["training"]["training_method"],
                                          global_step=global_step,
                                          loss=self.loss)
        self.saver = tf.train.Saver()
        self.network.session.run(tf.global_variables_initializer())
        self.init_op = tf.initialize_all_variables()


def set_loss_function(config, net, future_price, pv_vector, previous_w, commission_ratio):

    if config["training"]["loss_function"] == "loss_function4":
        loss_tensor = -tf.reduce_mean(tf.log(tf.reduce_sum(net[:] * future_price, reduction_indices=[1])))
    elif config["training"]["loss_function"] == "loss_function5":
        loss_tensor = -tf.reduce_mean(tf.log(tf.reduce_sum(net * future_price, reduction_indices=[1]))) + \
           1e-4 * tf.reduce_mean(tf.reduce_sum(-tf.log(1 + 1e-6 - net), reduction_indices=[1]))
    elif config["training"]["loss_function"] == "loss_function6":
        loss_tensor = -tf.reduce_mean(tf.log(pv_vector))
    elif config["training"]["loss_function"] == "loss_function7":
        loss_tensor = -tf.reduce_mean(tf.log(pv_vector)) + \
               1e-4 * tf.reduce_mean(tf.reduce_sum(-tf.log(1 + 1e-6 - net), reduction_indices=[1]))
    elif config["training"]["loss_function"] == "loss_function8":
        loss_tensor = -tf.reduce_mean(tf.log(tf.reduce_sum(net[:] * future_price, reduction_indices=[1])
                                             -tf.reduce_sum(tf.abs(net[:, 1:] - previous_w)
                                                            *commission_ratio, reduction_indices=[1])))
    else:
        loss_tensor = -tf.reduce_mean(tf.log(pv_vector))

    regularization_losses = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
    if regularization_losses:
        for regularization_loss in regularization_losses:
            loss_tensor += regularization_loss
    return loss_tensor


def init_train(learning_rate, decay_steps, decay_rate, training_method, global_step, loss):

    learning_rate = tf.train.exponential_decay(learning_rate, global_step,
                                               decay_steps, decay_rate, staircase=True)

    if training_method == 'GradientDescent':
        train_step = tf.train.GradientDescentOptimizer(learning_rate).\
                     minimize(loss, global_step=global_step)
    elif training_method == 'Adam':
        train_step = tf.train.AdamOptimizer(learning_rate).\
                     minimize(loss, global_step=global_step)
    elif training_method == 'RMSProp':
        train_step = tf.train.RMSPropOptimizer(learning_rate).\
                     minimize(loss, global_step=global_step)
    else:
        raise ValueError()
    return train_step


