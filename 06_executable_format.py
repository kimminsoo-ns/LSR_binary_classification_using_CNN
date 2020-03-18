import os
os.chdir("D:\\LSR_ALL\\LSR_binary_classification")

import tensorflow as tf
import cv2, pyautogui
from numpy import array
from PIL import ImageFile, ImageFilter
ImageFile.LOAD_TRUNCATED_IMAGES = True
import tkinter as tk

# Selected model
CATEGORIES = ["LSR_O", "LSR_X"] # O=0, X=1
model = tf.keras.models.load_model('4-128-4-50.model')

def imaging():
    # Screenshot preparation
    im01 = pyautogui.screenshot(
        region=(15, 220, 720, 720)).filter(
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
    pyautogui.alert(text=CATEGORIES[int(prediction_value)], title='LSR_discrimination', button='OK')

# Program execution
root= tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 150)
canvas1.pack()
    
myButton = tk.Button(text='LSR_O or LSR_X?',
                     command=imaging,
                     bg='green',
                     fg='white',
                     font=10)
canvas1.create_window(150, 75, window=myButton)

root.call('wm', 'attributes', '.', '-topmost', '1')
root.mainloop()
