# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 10:56:44 2020

@author: Frankenstein
"""

import os
os.chdir("/content/drive/My Drive/LSR_machine_learning")

import cv2
import tensorflow as tf
import glob

CATEGORIES = ["LSR_O", "LSR_X"] # O=0, X=1

def prepare(filepath):
    IMG_SIZE = 128                                              # 50 in txt-based
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)      # read in the image, convert to grayscale
    img_array = img_array/255.0
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))     # resize image to match model's expected sizing
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)         # return the image with shaping that TF wants.

test_files_list = glob.glob("test_files/*.jpg")
models_list = glob.glob("models/*.*")

for test_model in models_list:
    model = tf.keras.models.load_model(test_model)
    print(test_model)
    
    for test_file in test_files_list:
        filename = os.path.splitext(test_file) [0]
        prediction = model.predict_classes([prepare(test_file)])
        print ("{}".format(filename), (CATEGORIES[int(prediction)]))