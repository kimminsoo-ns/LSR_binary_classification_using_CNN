# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 08:28:47 2020

@author: Frankenstein
"""

import os
os.chdir("D:\\LSR_ALL\\LSR_original\\tests_set_2")

from PIL import Image, ImageFile, ImageFilter
ImageFile.LOAD_TRUNCATED_IMAGES = True
import glob

file_list = glob.glob("*.jpg")
filter1_list = [5] # list(range(1, 11, 2))
filter2_list = [3] # list(range(1, 11, 2))

for file in file_list:
    for filter1 in filter1_list:
        for filter2 in filter2_list:
            filename = os.path.splitext(file) [0]
            
            im = Image.open(file) # Create an image object from a file
            im = im.filter(ImageFilter.MinFilter(size= filter1))
            im = im.crop((15, 220, 735, 940)) #im = im.convert("L")
            im = im.resize((256,256)) # Resizing to 256x256
            im = im.filter(ImageFilter.MinFilter(size= filter2)) # Apply minimum filter twice to the image
                     
            # cropped = "cropped-{}-{}-filter1-{}-filter2".format(filename, filter1, filter2)
            # im.save(cropped, format="JPEG")
            
            class Point:
                def __init__(self, width, height):
                    self.info = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
                def __setitem__(self, key, value):
                    self.info[key[0]][key[1]] = value
                def __getitem__(self, item):
                    return self.info[item[0]][item[1]]
            
            if __name__ == '__main__':
                p = Point (3, 3) # print(p[1, 1])
                p[1, 1] = (-1, -1, -1) # print(p[1, 1])
            
            def gray(ori):
                dst = Image.new("RGB", ori.size, (0, 0, 0))
                (width, height) = ori.size
                pixels_dst = dst.load()
                pixels_ori = ori.load()
                for y in range(0, height):
                    for x in range(0, width):
                        color = pixels_ori[x, y]
                        aver = sum(color)//len(color)
                        pixels_dst[x, y] = (aver, aver, aver)
                return dst
            
            if __name__ == '__main__':
                img = gray(ori=im)

            grayscale = "grayscale-{}-{}-filter1-{}-filter2".format(filename, filter1, filter2)
            img.save(grayscale, format="JPEG")

            img2 = img
            pixels = img2.load()
            for i in range(img2.size[0]): # for every pixel:
                for j in range(img2.size[1]):
                    if pixels[i,j] != (0, 0, 0): # if not black:
                        pixels[i,j] = (255, 255, 255) # change to white
            
            # black = "{}".format(filename)
            # black = "black-{}-{}-filter1-{}-filter2".format(filename, filter1, filter2)
            # img2.save(black, format="JPEG")