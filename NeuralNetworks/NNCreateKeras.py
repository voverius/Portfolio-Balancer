import numpy as np
from time import time

t0 = time()
import keras
from keras import backend as K
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Dropout, Flatten, Conv2D, Conv3D, MaxPooling2D, Concatenate
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import TensorBoard

def NNCreateKeras(config, data):

    print('start NNCreateKeras', time()-t0)
    # tb = TensorBoard(log_dir=(config['package_directory'] + 'tensorboard\\'))

    # Preparing the data
    x_train = data.train_data['x']
    y_train = data.train_data['y']
    x_test = data.test_data['x']
    y_test = data.test_data['y']

    # Input variables
    pairs = x_train.shape[1]
    periods = x_train.shape[2]
    window = x_train.shape[3]

    # Create the model
    model = Sequential()

    # First layer - conv2d
    model.add(Conv2D(filters=3,
                     kernel_size=[1, 2],
                     strides=[1, 1],
                     padding='valid',
                     activation='relu',
                     kernel_regularizer=keras.regularizers.l2(l=0.01),
                     input_shape=(pairs, window, periods)))

    # Second layer - EIIE Dense
    model.add(Conv2D(filters=10,
                     kernel_size=[1, (window - 1)],
                     strides=[1, 1],
                     padding='valid',
                     activation='relu',
                     kernel_regularizer=keras.regularizers.l2(l=5e-08)))

    # Adding a last_w
    last_w = K.placeholder(name="last_w", shape=(None, data.PVM.shape[1]))



    # self.previous_w = tf.placeholder(tf.float32, shape=[None, coin_number])
    # w = tf.reshape(self.previous_w, [-1, int(height), 1, 1])
    # network = tf.concat([network, w], axis=3)


    a = 0

    # model.add(Conv2D(64, (3, 3)))
    # model.add(Activation('relu'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    #
    # model.add(Flatten())
    #
    # model.add(Dense(64))
    # model.add(Activation('relu'))
    #
    # model.add(Dense(1))
    # model.add(Activation('sigmoid'))
    #
    # model.compile(loss="binary_crossentropy",
    #               optimizer='adam',
    #               metrics=['accuracy'])







    a = 0








































