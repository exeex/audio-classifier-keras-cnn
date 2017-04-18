import numpy as np
import librosa

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
    try:
        classname = os.listdir(path)[0]
        files = os.listdir(path + classname)
        infilename = files[0]
        audio_path = path + classname + '/' + infilename
        melgram = np.load(audio_path)
        print("   get_sample_dimensions: melgram.shape = ", melgram.shape)
    except FileNotFoundError:
        return None
    return melgram.shape


mel_dims = get_sample_dimensions(path=path)

def get_total_filelist():
    return csv.get_total_files()

def get_total_y():
    y = []
    for idx in range(csv.get_file_numbers()):
        y.append(csv.get_tag_np_vector(0))
    return y

def get_total_x():
    filelist = get_total_filelist()
    total = csv.get_file_numbers()
    x = np.zeros((total,1,mel_dims[2],mel_dims[3]),'float32')
    printevery = 100
    for idx,filepath in enumerate(filelist):
        audio_path = path + filepath
        if 0 == idx % printevery:
            print("load {0} / {1} file".format(idx,total))
        melgram = np.load(audio_path + ".npy")
        x[idx,:,:] = melgram

    return x

def get_train_x(total_x):
    return
def get_train_y(y):
    return
def get_test_x(x):
    return
def get_test_y(y):
    return

def build_datasets(train_percentage=0.8, preproc=False):



    X_train = np.zeros((total_train, mel_dims[1], mel_dims[2], mel_dims[3]))
    Y_train = np.zeros((total_train, nb_classes))
    X_test = np.zeros((total_test, mel_dims[1], mel_dims[2], mel_dims[3]))
    Y_test = np.zeros((total_test, nb_classes))
    return train_x ,train_y ,test_x , test_y


