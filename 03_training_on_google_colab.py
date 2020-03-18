# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 22:51:23 2020

@author: Frankenstein
"""

import os
os.chdir("/content/drive/My Drive/LSR_machine_learning")

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import TensorBoard
import pickle
import time

pickle_in = open("X.pickle","rb")
X = pickle.load(pickle_in)

pickle_in = open("y.pickle","rb")
y = pickle.load(pickle_in)

X = X/255.0

dense_layers = [1, 2]
layer_sizes = [32, 64, 128]
conv_layers = [1, 2] 
val_splits = [0.1, 0.2]
epochs = [10, 50, 100]


for dense_layer in dense_layers:
    for layer_size in layer_sizes:
        for conv_layer in conv_layers:
            for val_split in val_splits:
                for epoch in epochs:
                    NAME = "{}-conv-{}-nodes-{}-dense-{}-val-{}-epoch-{}".format(
                        conv_layer, layer_size, dense_layer, val_split, epoch, int(time.time()))
                    model_name = "{}-conv-{}-nodes-{}-dense-{}-val-{}-epoch".format(
                        conv_layer, layer_size, dense_layer, val_split, epoch)
                    print(NAME)
        
                    model = Sequential()
                    
                    model.add(Conv2D(layer_size, (3, 3), input_shape=X.shape[1:]))  
                    model.add(Activation('relu'))
                    model.add(MaxPooling2D(pool_size=(2, 2)))
        
                    for l in range(conv_layer-1):
                        model.add(Conv2D(layer_size, (3, 3)))
                        model.add(Activation('relu'))
                        model.add(MaxPooling2D(pool_size=(2, 2)))
        
                    model.add(Flatten())
                    
                    for _ in range(dense_layer):
                        model.add(Dense(layer_size))
                        model.add(Activation('relu'))
                        model.add(Dropout(0.2)) #prevents overfitting
        
                    model.add(Dense(1))
                    model.add(Activation('sigmoid'))
        
                    tensorboard = TensorBoard(log_dir="logs/{}".format(NAME))
        
                    model.compile(loss='binary_crossentropy',
                                  optimizer='adam',
                                  metrics=['accuracy'],
                                  )
        
                    model.fit(X, y,
                              batch_size = 32,
                              epochs = int(epoch),
                              validation_split = int(val_split),
                              callbacks = [tensorboard])
                    model.save(model_name)