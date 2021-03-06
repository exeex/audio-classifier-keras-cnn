
''' 
Classify sounds using database
Author: Scott H. Hawley

This is kind of a mixture of Keun Woo Choi's code https://github.com/keunwoochoi/music-auto_tagging-keras
   and the MNIST classifier at https://github.com/fchollet/keras/blob/master/examples/mnist_cnn.py

Trained using Fraunhofer IDMT's database of monophonic guitar effects, 
   clips were 2 seconds long, sampled at 44100 Hz
'''

import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

from keras.models import Sequential, Model
from keras.layers import Input, Dense, TimeDistributed, LSTM, Dropout, Activation
from keras.layers import Conv2D, MaxPooling2D, Flatten
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import ELU
from keras.callbacks import ModelCheckpoint
from keras import backend
from keras.utils import np_utils
import os
from os.path import isfile
from read_annotation_csv import Csv_parser as Csv

csv = Csv()

from timeit import default_timer as timer

mono = True


def get_class_names(path="Preproc2/"):  # class names are subdirectory names in Preproc/ directory
    class_names = os.listdir(path)
    return class_names


def get_total_files(path="Preproc2/", train_percentage=0.8):
    sum_total = 0
    sum_train = 0
    sum_test = 0
    subdirs = os.listdir(path)
    for subdir in subdirs:
        files = os.listdir(path + subdir)
        n_files = len(files)
        sum_total += n_files
        n_train = int(train_percentage * n_files)
        n_test = n_files - n_train
        sum_train += n_train
        sum_test += n_test
    return sum_total, sum_train, sum_test


def get_sample_dimensions(path='Preproc2/'):
    classname = os.listdir(path)[0]
    files = os.listdir(path + classname)
    infilename = files[0]
    audio_path = path + classname + '/' + infilename
    melgram = np.load(audio_path)
    print("   get_sample_dimensions: melgram.shape = ", melgram.shape)
    return melgram.shape


def encode_class(class_name, class_names):  # makes a "one-hot" vector for each class name called
    try:
        idx = class_names.index(class_name)
        vec = np.zeros(len(class_names))
        vec[idx] = 1
        return vec
    except ValueError:
        return None


def shuffle_XY_paths(X, Y, paths):  # generates a randomized order, keeping X&Y(&paths) together
    assert (X.shape[0] == Y.shape[0])
    idx = np.array(range(Y.shape[0]))
    np.random.shuffle(idx)
    newX = np.copy(X)
    newY = np.copy(Y)
    newpaths = paths
    for i in range(len(idx)):
        newX[i] = X[idx[i], :, :]
        newY[i] = Y[idx[i], :]
        newpaths[i] = paths[idx[i]]
    return newX, newY, newpaths


'''
So we make the training & testing datasets here, and we do it separately.
Why not just make one big dataset, shuffle, and then split into train & test?
because we want to make sure statistics in training & testing are as similar as possible
'''


def build_datasets(train_percentage=0.8, preproc=False):
    if preproc:
        path = "Preproc3/"
    else:
        path = "../Music/"


    # TODO : replace by csv.get_tags("annotations_subset.csv")
    # class_names = get_class_names(path=path)
    # print("class_names = ", class_names)
    class_names = csv.get_tags()
    print("class_names = ", class_names)

    # TODO : rewrite get_total_files
    # total_files, total_train, total_test = get_total_files(path=path, train_percentage=train_percentage)
    # print("total files = ", total_files)
    #
    # nb_classes = len(class_names)




    # pre-allocate memory for speed (old method used np.concatenate, slow)
    mel_dims = get_sample_dimensions(path=path)  # Find out the 'shape' of each data file

    filelist = csv.get_total_files()    #TODO : return file list
    filelist_train = filelist[1:1000]
    filelist_test = filelist[1000:1100]
    filelist_train_test = filelist[1:1100]
    total_train = len(filelist_train)
    total_test = len(filelist_test)
    nb_classes = len(csv.get_tags())

    X_train = np.zeros((total_train, mel_dims[1], mel_dims[2], mel_dims[3]))
    Y_train = np.zeros((total_train, nb_classes))
    X_test = np.zeros((total_test, mel_dims[1], mel_dims[2], mel_dims[3]))
    Y_test = np.zeros((total_test, nb_classes))
    paths_train = []
    paths_test = []

    train_count = 0
    test_count = 0





    for idx, file in enumerate(filelist_train_test):

        this_Y = np.array(csv.get_tag_np_vector(idx))   #TODO: return np.array (dim = tag number)
        audio_path = path + csv.get_file_path(idx) #TODO: return np.array (dim = tag number)

        n_files = len(filelist_train_test)
        n_load = n_files
        n_train = int(train_percentage * n_load)
        printevery = 100

        if (0 == idx % printevery):
            print('\r Loading file: {:14s} ({:2d} of {:2d} classes)'.format(file, idx + 1, nb_classes),
                  ", file ", idx + 1, " of ", n_load, ": ", audio_path, sep="")
        # start = timer()
        if (preproc):
            melgram = np.load(audio_path+".npy")
            sr = 44100
        else:
            aud, sr = librosa.load(audio_path, mono=mono, sr=None)
            melgram = librosa.logamplitude(librosa.feature.melspectrogram(aud, sr=sr, n_mels=96), ref_power=1.0)[
                      np.newaxis, np.newaxis, :, :]
        melgram = melgram[:, :, :, 0:mel_dims[3]]  # just in case files are differnt sizes: clip to first file size

        # end = timer()
        # print("time = ",end - start)
        if (idx < total_train):
            # concatenate is SLOW for big datasets; use pre-allocated instead
            # X_train = np.concatenate((X_train, melgram), axis=0)
            # Y_train = np.concatenate((Y_train, this_Y), axis=0)
            X_train[train_count, :, :] = melgram
            Y_train[train_count, :] = this_Y
            paths_train.append(audio_path)  # list-appending is still fast. (??)
            train_count += 1
        else:
            X_test[test_count, :, :] = melgram
            Y_test[test_count, :] = this_Y
            # X_test = np.concatenate((X_test, melgram), axis=0)
            # Y_test = np.concatenate((Y_test, this_Y), axis=0)
            paths_test.append(audio_path)
            test_count += 1



    print("Shuffling order of data...")
    X_train, Y_train, paths_train = shuffle_XY_paths(X_train, Y_train, paths_train)
    X_test, Y_test, paths_test = shuffle_XY_paths(X_test, Y_test, paths_test)

    return X_train, Y_train, paths_train, X_test, Y_test, paths_test, class_names, sr


def build_model(X, Y, nb_classes):
    nb_filters = 32  # number of convolutional filters to use
    pool_size = (2, 2)  # size of pooling area for max pooling
    kernel_size = (3, 12)  # convolution kernel size
    input_shape = (1, X.shape[2], X.shape[3])

    model = Sequential()

    model.add(BatchNormalization(axis=1, input_shape=input_shape))
    #layer 1
    model.add(Conv2D(64, (200,1)))
    model.add(BatchNormalization(axis=1))
    model.add(ELU())

    print(model.output_shape)

    #layer 2
    model.add(Conv2D(32, (1,4),strides=(1,2)))
    model.add(BatchNormalization(axis=1))
    model.add(ELU())
    model.add(MaxPooling2D(pool_size=(1,2)))

    print(model.output_shape)

    #layer 3
    model.add(Conv2D(nb_filters, (1,4),strides=(1,2)))
    model.add(BatchNormalization(axis=1))
    model.add(ELU())
    model.add(MaxPooling2D(pool_size=(1,2)))
    #layer 4
    model.add(Conv2D(nb_filters, (1,4),strides=(1,2)))
    model.add(BatchNormalization(axis=1))
    model.add(ELU())
    #layer 5
    model.add(Conv2D(nb_filters, (1,4),strides=(1,2)))
    model.add(BatchNormalization(axis=1))
    model.add(ELU())

    model.add(Flatten())
    model.add(Dense(nb_classes))
    model.add(Dropout(0.6))
    model.add(Activation("softmax"))




    return model







if __name__ == '__main__':
    np.random.seed(1)

    # get the data
    X_train, Y_train, paths_train, X_test, Y_test, paths_test, class_names, sr = build_datasets(preproc=True)

    # make the model
    model = build_model(X_train, Y_train, nb_classes=len(class_names))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])
    model.summary()

    # Initialize weights using checkpoint if it exists. (Checkpointing requires h5py)
    load_checkpoint = True
    checkpoint_filepath = 'weights.hdf5'
    if (load_checkpoint):
        print("Looking for previous weights...")
        if (isfile(checkpoint_filepath)):
            print('Checkpoint file detected. Loading weights.')
            model.load_weights(checkpoint_filepath)
        else:
            print('No checkpoint file detected.  Starting from scratch.')
    else:
        print('Starting from scratch (no checkpoint)')
    checkpointer = ModelCheckpoint(filepath=checkpoint_filepath, verbose=1, save_best_only=True)

    # train and score the model
    batch_size = 128
    nb_epoch = 10
    model.fit(X_train, Y_train, batch_size=batch_size, epochs=nb_epoch,
              verbose=1, validation_data=(X_test, Y_test), callbacks=[checkpointer])
    score = model.evaluate(X_test, Y_test, verbose=0)
    print('Test score:', score[0])
    print('Test accuracy:', score[1])
