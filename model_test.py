import numpy as np
from train_network import build_model
from keras.models import Sequential, Model
from keras.layers import Input, Dense, TimeDistributed, LSTM, Dropout, Activation
from keras.layers import Conv2D, MaxPooling2D, Flatten
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import ELU
from keras.callbacks import ModelCheckpoint
from keras import backend
from keras.utils import np_utils
from keras.utils import plot_model
from keras import losses

from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot




def get_model():
    X = np.zeros((1, 1, 200, 911))
    Y = ""
    return build_model(X,Y,20)


def load_weights(model):
    model.load_weights(filepath, by_name=False)
# gg = SVG(model_to_dot(model).create(prog='dot', format='svg'))

def get_layer_output(model, layer_name):
    # get the symbolic outputs of each "key" layer (we gave them unique names).
    layer_dict = dict([(layer.name, layer) for layer in model.layers])
    layer = layer_dict[layer_name].get_output()
    return layer

def get_layer_weight(model, layer_name):
    # get the symbolic outputs of each "key" layer (we gave them unique names).
    layer_dict = dict([(layer.name, layer) for layer in model.layers])
    weights = layer_dict[layer_name].get_weights()
    return weights

def get_layer_names(model):
    names = []
    for layer in model.layers:
        names.append(layer.name)

def plot_filter(filter):
    return

def plot_filters(layer_weights):
    for x in range(layer_weights.shape[3]):
        print(x)
        plot_filter(layer_weights[:,:,0,0])

filepath = 'weightsss'
model = get_model()

# model.load_weights(filepath,by_name=False)
# conv2d_1 = get_layer_weight(model,'conv2d_1')[0]




# from keras import backend as K
#
# inp = model.input                                           # input placeholder
# outputs = [layer.output for layer in model.layers]          # all layer outputs
# functors = [K.function([inp]+ [K.learning_phase()], [out]) for out in outputs]  # evaluation functions
#
# # Testing
# test = np.random.random(input_shape)[np.newaxis,...]
# layer_outs = [func([test, 1.]) for func in functors]
# print(layer_outs)