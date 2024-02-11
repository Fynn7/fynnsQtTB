from tensorflow import keras
from tensorflow.keras import layers
from matplotlib import pyplot as plt
import tensorflow as tf
import sys



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


import pandas as pd
def exampleNN(input_shape: int, 
              train_test_data: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame],):
    '''sample model'''
    model = keras.Sequential([
        keras.Input(shape=input_shape),
        layers.Dense(512),
        # Do something here between dense and the activate. Equivalent to layer.Dense(512, activation='relu') but more flexible
        layers.Activation('relu'),

        layers.Dense(512),
        # Do something here between dense and the activate
        layers.Activation('relu'),

        layers.Dense(512),
        layers.Activation('relu'),

        layers.Dense(1),
    ])
    model.compile(optimizer='adam', loss='mae', metrics=['accuracy'])

    X_train, y_train, X_valid, y_valid = train_test_data
    # test fit
    history = model.fit(
        X_train, y_train,
        validation_data=(X_valid, y_valid),
        batch_size=256,
        epochs=10,
    )

    # convert the training history to a dataframe
    history_df = pd.DataFrame(history.history)
    # use Pandas native plot method
    history_df['loss'].plot()

    return model


if __name__ == '__main__':
    show_activation_function()
    sys.exit(0)
