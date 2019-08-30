import tensorflow as tf
import tflearn

class NeuralNetwork:
    def __init__(self, data, layers):

        coin_number = data.train_data['x'].shape[1]
        feature_number = data.train_data['x'].shape[2]
        window_size = data.train_data['x'].shape[3]

        tf_config = tf.ConfigProto()
        self.session = tf.Session(config=tf_config)
        self.input_num = tf.placeholder(tf.int32, shape=[])
        self.previous_w = tf.placeholder(tf.float32, shape=[None, coin_number])
        self.input_tensor = tf.placeholder(tf.float32, shape=[None, coin_number, feature_number, window_size])

        self.layer_dict = {}
        layer_count = 0

        network = tf.transpose(self.input_tensor, [0, 1, 3, 2])
        network = network / network[:, :, -1, 0, None, None]

        for layer_number, layer in enumerate(layers):

            if layer['type'] == "ConvLayer":
                network = tflearn.layers.conv_2d(network, int(layer["filter_number"]),
                                                 layer["filter_shape"],
                                                 layer["strides"],
                                                 layer["padding"],
                                                 layer["activation_function"],
                                                 regularizer=layer["regularizer"],
                                                 weight_decay=layer["weight_decay"])
                self.layer_dict, layer_count = self.add_layer_to_dict(self.layer_dict, layer_count,
                                                                      layer['type'], network)

            elif layer["type"] == "EIIE_Dense":
                width = network.get_shape()[2]
                network = tflearn.layers.conv_2d(network, int(layer["filter_number"]),
                                                 [1, width],
                                                 [1, 1],
                                                 "valid",
                                                 layer["activation_function"],
                                                 regularizer=layer["regularizer"],
                                                 weight_decay=layer["weight_decay"])
                self.layer_dict, layer_count = self.add_layer_to_dict(self.layer_dict, layer_count,
                                                                      layer['type'], network)

            elif layer["type"] == "EIIE_Output_WithW":
                height = network.get_shape()[1]
                width = network.get_shape()[2]
                features = network.get_shape()[3]

                network = tf.reshape(network, [self.input_num, int(height), 1, int(width * features)])
                w = tf.reshape(self.previous_w, [-1, int(height), 1, 1])

                # Convolutional Layer
                network = tf.concat([network, w], axis=3)
                network = tflearn.layers.conv_2d(network, 1, [1, 1], padding="valid",
                                                 regularizer=layer["regularizer"],
                                                 weight_decay=layer["weight_decay"])
                self.layer_dict, layer_count = self. add_layer_to_dict(self.layer_dict, layer_count,
                                                                       layer['type'], network)

                # Voting Layer
                network = network[:, :, 0, 0]
                btc_bias = tf.get_variable("btc_bias", [1, 1], dtype=tf.float32,
                                           initializer=tf.zeros_initializer)
                btc_bias = tf.tile(btc_bias, [self.input_num, 1])
                network = tf.concat([btc_bias, network], 1)
                self.layer_dict, layer_count = self.add_layer_to_dict(self.layer_dict, layer_count,
                                                                      'voting', network)

                # Softmax Layer
                network = tflearn.layers.core.activation(network, activation="softmax")
                self.output_layer = network
                self.layer_dict, layer_count = self.add_layer_to_dict(self.layer_dict, layer_count,
                                                                      'softmax_layer', network)

        print('finished NeuralNetwork')

    def add_layer_to_dict(self, layer_dict, layer_count, layer, network, weights=True):
        layer_dict[f'{str(layer_count)}_{layer}'] = network
        layer_count += 1
        return layer_dict, layer_count





