import numpy as np
import os
import tqdm
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Input, Activation
from keras.layers import Conv2D, MaxPooling2D, Flatten
from keras.utils import np_utils
from keras.models import load_model
from keras.optimizers import SGD
from sklearn.utils import shuffle
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import tensorflow as tf
import random
tf.logging.set_verbosity(tf.logging.ERROR)


def load_image(fname):
    img = load_img(fname)  # this is a PIL image
    x = img_to_array(img).reshape((-1, 48, 48))  # this is a Numpy array with shape (3, 48, 48)
    # x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 48, 48)
    return x

def load_images():
    '''loads images and puts them in X and y'''
    files = os.listdir('processed')
    X = []
    y = []
    for file in tqdm.tqdm(files):
        try:
            x_i = load_image('processed/' + file)
            if x_i.shape[1] != 48 or x_i.shape[2] != 48:
                continue
            X.append(x_i)
            y_i = [1, 0] if 'apple' in file else [0, 1]
            y.append(y_i)
        except:
            pass
    return X, y


def base_model():
    # create model
    i = Input(shape=(3, 48, 48), name='main_input')
    conv = Conv2D(32, (3, 3), padding='same', input_shape=(3, 48, 48), activation='relu')(i)
    pool = MaxPooling2D(pool_size=(2, 2))(conv)
    flat = Flatten()(pool)
    d1 = Dense(1000, activation='tanh')(flat)
    d2 = Dense(500, activation='relu')(flat)
    d3 = Dense(200, activation='tanh')(flat)
    d4 = Dense(1000, activation='relu')(flat)

    # output layer
    d2 = Dense(2, activation='softmax')(d1)

    model = Model(inputs=i, outputs=d2)

    # Compile model
    return model
 
def train_model():
    X, y = load_images()
    X, y = shuffle(X, y)
    X2 = np.array(X[-50:])
    y2 = np.array(y[-50:])
    X = X[:-50]
    y = y[:-50]
    epochs = 1000
    best_acc = 0
    # model = base_model()
    model = load_model('last.h5')
    optimizer = SGD(lr=1e-5)
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    for epoch in xrange(epochs):
        X, y = shuffle(X, y)
        print 'Doing epoch {}...'.format(epoch+1)
        model.fit(np.array(X), np.array(y), epochs=1, batch_size=10)
        print 'Evaluating model...'
        score = model.evaluate(X2, y2)[1]
        print model.predict(np.array([X[0]])), y[0]
        print("Test Accuracy: %.2f%%" % (score*100))

        if score > best_acc and score >= .75:
            model.save('cls{}_{}.h5'.format(epoch+1, score))
            best_acc = score

        print
    model.save('last.h5')

def eval_model():
    model = load_model('last.h5')
    X, y = load_images()
    score = model.evaluate(np.array(X), np.array(y))[1]
    print("Overall Accuracy: %.2f%%" % (score*100))

if __name__ == '__main__':
    # train_model()
    eval_model()
