from tensorflow import keras
from tensorflow.keras import layers
from matplotlib import pyplot as plt
import tensorflow as tf


def quickNN(input_shape, num_classes):
    '''
    quick to build code, does not mean running quicker'''
    model = keras.Sequential([
        keras.Input(shape=input_shape),
        layers.Dense(512),
        # Do something here between dense and the activate. Equivalent to layer.Dense(512, activation='relu') but more flexible
        layers.Activation('relu'),
        layers.Dense(256),
        # Do something here between dense and the activate
        layers.Activation('relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    return model


def show_activation_function(together_in_one_plot=False, funcs: list[str] = ['relu', 'elu', 'selu', 'swish']):
    fig = plt.figure(dpi=100)
    if together_in_one_plot:
        for af in funcs:
            activation_layer = layers.Activation(af)
            x = tf.linspace(-3.0, 3.0, 100)
            y = activation_layer(x)
            plt.plot(x, y, label=af)
        plt.title(funcs)
        plt.legend(funcs)
        plt.xlim(-3, 3)
        plt.xlabel("Input")
        plt.ylabel("Output")
        plt.show()
    else:
        for af in funcs:
            activation_layer = layers.Activation(af)
            x = tf.linspace(-3.0, 3.0, 100)
            y = activation_layer(x)
            plt.title(activation_layer.name+':'+af)
            plt.plot(x, y)
            plt.xlim(-3, 3)
            plt.xlabel("Input")
            plt.ylabel("Output")
            plt.show()
