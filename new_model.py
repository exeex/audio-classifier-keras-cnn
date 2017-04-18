from __future__ import absolute_import
from __future__ import print_function
import scipy.io
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.advanced_activations import ELU
from keras.layers.normalization import BatchNormalization
from keras.optimizers import SGD, Adadelta, Adagrad
from keras.utils import np_utils, generic_utils


def build_model(X,Y):


    input_shape=(1,X[2],X[3])
    nb_classes = 10

    channel_axis = 1
    freq_axis = 2
    time_axis =3
    batch_index_axis = 0

    model = Sequential()

    filter_nb = [64,128,128]
    filter_size =[(3,3),(3,3),(3,3)]
    pool_size=[(2,2),(2,2),(2,2)]

    model.add(BatchNormalization(axis=freq_axis))

    layer_index = 0

    #layer 1
    model.add(Conv2D(filter_nb[layer_index],filter_size[layer_index],padding='same'))
    model.add(ELU())
    model.add(MaxPooling2D(pool_size[layer_index]))
    model.add(BatchNormalization(axis=channel_axis))
    layer_index+=1

    #layer 2
    model.add(Conv2D(filter_nb[layer_index],filter_size[layer_index],padding='same'))
    model.add(ELU())
    model.add(MaxPooling2D(pool_size[layer_index]))
    model.add(BatchNormalization(axis=channel_axis))
    layer_index+=1

    #layer 3
    model.add(Conv2D(filter_nb[layer_index],filter_size[layer_index],padding='same'))
    model.add(ELU())
    model.add(MaxPooling2D(pool_size[layer_index]))
    model.add(BatchNormalization(axis=channel_axis))
    layer_index+=1

    model.add(Flatten())

    model.add(Dense(nb_classes))

    #final layer

    model.compile(loss='binary_crossentropy', optimizer='adam')







# batch_size = 100
# nb_classes = 5
# nb_epoch = 5
# data_augmentation = True
#
# shapex, shapey = 64, 64
#
# nb_filters = [32, 64]
#
# nb_pool = [4, 3]
#
# nb_conv = [5, 4]
#
# image_dimensions = 3
#
#
# mat = scipy.io.loadmat('E:\scene.mat')
#
# X_train = mat['x_train']
# Y_train = mat['y_train']
# X_test =  mat['x_test']
# Y_test =  mat['y_test']
# print(X_train.shape)
# print(X_test.shape)

if not data_augmentation:
    print("Not using data augmentation or normalization")

    X_train = X_train.astype("float32")
    X_test = X_test.astype("float32")
    X_train /= 255
    X_test /= 255
    model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch)
    score = model.evaluate(X_test, Y_test, batch_size=batch_size)
    print('Test score:', score)

else:
    print("Using real time data augmentation")

    # this will do preprocessing and realtime data augmentation
    datagen = ImageDataGenerator(
        featurewise_center=True,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=True,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=20,  # randomly rotate images in the range (degrees, 0 to 180)
        width_shift_range=0.2,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.2,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False)  # randomly flip images

    datagen.fit(X_train)
    model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch)
    score = model.evaluate(X_test, Y_test, batch_size=batch_size)
    print (model.predict(X_test[1,:]))