import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers
from matplotlib import pyplot as plt
import tensorflow as tf
import sys
import traceback

from learntools.deep_learning_intro.dltools import animate_sgd

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

class DLModel:
    '''Only for type hinting'''
    pass

def fynnsNN(input_shape: int|tuple|list[int], sequential_layers_data: list[tuple[int, str]] = [(512, 'relu'), (512, 'relu'), (512, 'relu'), (1, 'linear')],
            optimizer:str='adam', loss:str='mae', metrics:list=['accuracy'],
            train_test_data: tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame] | None = None, batch_size:int=256, epochs:int=10,
            animate_sgd:bool=False)->tuple[DLModel, None|keras.src.callbacks.History]:
    '''
    https://www.kaggle.com/code/ryanholbrook/stochastic-gradient-descent
    sample model
    
    input_shape: (FEATURE_DIM,) eg: (13,) , [11], 11
    sequential_layers_data: [(units, activation), ...]
    optimizer: 'adam', 'sgd', ...
    loss: 'mae', 'mse', ...
    metrics: ['accuracy', ...]
    train_test_data: (X_train, X_valid, y_train, y_valid)
    # NOTE: technically it is not necessary to provide X_valid and y_valid, could just input X,y as training data. But we won't know the accuracy of the model, as in when training data, keras will output accuracy as 0
    batch_size: 256
    epochs: 10

    return:
    model: `keras.Model`
    history: `keras.src.callbacks.History`

    NOTE: use `history.history` to get the training history
    use `pd.DataFrame(history.history)` to convert the history to a dataframe
    and use `history_df['loss'].plot()` to plot the loss
    '''
    # dealing sequential_layers pipeline
    sequential_layers=[keras.Input(shape=input_shape)]
    history:keras.src.callbacks.History|None = None

    for units, activation in sequential_layers_data:
        sequential_layers.append(layers.Dense(units))
        # Do something here between dense and the activate. Equivalent to layer.Dense(512, activation='relu') but more flexible
        sequential_layers.append(layers.Activation(activation))
    print("got sequential_layers: ", sequential_layers, "with input_shape: ", input_shape, "and sequential_layers_data: ", sequential_layers_data, "train_test_data: ", train_test_data, "batch_size: ", batch_size, "epochs: ", epochs)
    try:
        model = keras.Sequential(sequential_layers)
    except Exception as e:
        print("Building sequential layers failed: ", e)
    # compile the model
    try:
        model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
    except Exception as e:
        print("Compile failed: ", e)
    if not train_test_data:
        print("No train_test_data provided. Ignore to fit.")
    else:
        try:
            X_train, X_valid, y_train, y_valid = train_test_data
            # test fit
            history:keras.src.callbacks.History= model.fit(
                X_train, y_train,
                validation_data=(X_valid, y_valid),
                batch_size=batch_size,
                epochs=epochs,
            )

            # convert the training history to a dataframe
            history_df = pd.DataFrame(history.history)
            # use Pandas native plot method
            history_df['loss'].plot()
        except Exception as e:
            print("Fit model failed: ", e)
            # traceback.print_exc()
        if animate_sgd:
            try:
                animate_sgd(history)
            except Exception as e:
                print("animate_sgd failed: ", e)
                # traceback.print_exc()
    return model, history



if __name__ == '__main__':
    print("Testing DLModel")
    # show_activation_function()
    # sys.exit(0)
