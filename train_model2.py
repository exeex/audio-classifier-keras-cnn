import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

from keras.models import Sequential, Model
from keras.layers import Input, Dense, TimeDistributed, LSTM, Dropout, Activation
from keras.layers import Conv2D, MaxPooling2D, Flatten ,Lambda
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import ELU
from keras.callbacks import ModelCheckpoint
from keras import backend
from keras.utils import np_utils
import os
from os.path import isfile
from read_annotation_csv import Csv_parser as Csv

csv = Csv()
path = "Preproc2/"
sr = 16000

def get_sample_dimensions(path='Preproc2/'):
    classname = os.listdir(path)[0]
    files = os.listdir(path + classname)
    infilename = files[0]
    audio_path = path + classname + '/' + infilename
    melgram = np.load(audio_path)
    print("   get_sample_dimensions: melgram.shape = ", melgram.shape)
    return melgram.shape



def get_total_filelist():
    return csv.get_total_files()

def get_total_y():
    y = []
    for idx in range(csv.get_file_numbers()):
        y.append(csv.get_tag_np_vector(0))
    return y

def get_total_x():
    filelist = get_total_filelist()
    mel_dims = get_sample_dimensions(path=path)
    total = csv.get_file_numbers()
    x = []
    printevery = 100
    for idx,filepath in enumerate(filelist):
        audio_path = path + filepath
        if 0 == idx % printevery:
            print("load {0} / {1} file".format(idx,total))
        melgram = np.load(audio_path + ".npy")
        x.append(melgram[:, :, :, 0:mel_dims[3]])
    return x

def build_datasets(train_percentage=0.8, preproc=False):
    X_train = np.zeros((total_train, mel_dims[1], mel_dims[2], mel_dims[3]))
    Y_train = np.zeros((total_train, nb_classes))
    X_test = np.zeros((total_test, mel_dims[1], mel_dims[2], mel_dims[3]))
    Y_test = np.zeros((total_test, nb_classes))
    return


def shuffle_XY_paths(X, Y, paths):
    return