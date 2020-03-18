# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 23:41:25 2020

@author: Frankenstein
"""


import os
os.chdir("D:\\LSR_ALL\\LSR_binary_classification")

import tensorflow as tf
import cv2, pyautogui
from numpy import array
from PIL import ImageFile, ImageFilter
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Selected model
CATEGORIES = ["LSR_O", "LSR_X"] # O=0, X=1
model = tf.keras.models.load_model('4-128-4-50.model')

# Screenshot preparation (735, 940) or (840, 840)
im01 = pyautogui.screenshot(
    region=(15, 220, 840, 840)).filter(
        ImageFilter.MinFilter(size= 7)).resize(
            (256,256)).filter(ImageFilter.MinFilter(size= 3))
im01_pixel = im01.load()
for i in range(im01.size[0]): # for every pixel:
    for j in range(im01.size[1]):
        if im01_pixel[i,j] != (0, 0, 0): # if not black:
            im01_pixel[i,j] = (255, 255, 255) # change to white

# Fitting to model
im01_L_array = array(im01.convert('L'))
img_array = im01_L_array/255.0
new_array = cv2.resize(img_array, (128, 128))
new_array2 = new_array.reshape(-1, 128, 128, 1)

# Prediction
prediction_value = model.predict(new_array2)

print ("prediction value=", prediction_value)
print ("(0, LSR_O; 1, LSR_X)")
print ("So, this is perhaps,", CATEGORIES[int(prediction_value)])

pyautogui.alert(text=CATEGORIES[int(prediction_value)], title='LSR_discrimination', button='OK')
