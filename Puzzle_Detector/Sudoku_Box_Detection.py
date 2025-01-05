#!/usr/bin/env python
# coding: utf-8

import numpy as np 
import matplotlib.pyplot as plt
import cv2
import keras
from pathlib import Path

import os, random
from PIL import Image 

import tkinter
from tkinter import filedialog

# file = r"C:\Users\atcut\Documents\ML_Proj\Digit Classification\puzzles"
# file = file + '\\' +random.choice(os.listdir(file))
# # file = r"C:\Users\atcut\Documents\ML_Proj\Digit Classification\puzzles\_4_3941682.jpeg"
# print(file)
# img = cv2.imread(file)
# plt.imshow(img)
# plt.show()

# Image Preprocessing 
# Removing extraneous noise and resizing images

def prep(img):
    size = cv2.resize(img, (450,450))
    gray = cv2.cvtColor(size, cv2.COLOR_BGR2GRAY) 
    blur = cv2.GaussianBlur(gray, (3,3),6) #remember (3,3) is kernel
    new_img = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
    return size, new_img

# References Used: 
# https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
# https://pyimagesearch.com/2021/10/06/opencv-contour-approximation/
# Douglas-Peucker Algorithm: https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm
# 

#Assumption: sudoku is the largest rectangular contour in given image
def outline(contour):
    dim = np.array([])
    max_area = 0
    for c in contour:
        area = cv2.contourArea(c)
        if area > 100: #100 is arbitrary. May increase value     
            perimeter = cv2.arcLength(c, True)
            #Approximates a polygonal curve(s) with the specified precision. 
            approx = cv2.approxPolyDP(c, 0.05* perimeter, True)
            #Ignores Non-rectangular Contours
            if area > max_area and len(approx) ==4:
                dim = approx
                max_area = area
    return dim, max_area

def corners(points):
    points = points.reshape((4, 2)) #4 rows, 2 columns
    imgCorners = np.zeros((4,1,2),dtype = np.int32)
    
    #Adds X, Y coordinates together to determine each corners' distance from 0
    add = points.sum(1)
    imgCorners[0] = points[np.argmin(add)] #Determining Corner closest to (0,0)
    imgCorners[3] = points[np.argmax(add)] #Determining Corner furthest from (0,0)

    diff = np.diff(points, axis =1)
    imgCorners[1] = points[np.argmin(diff)] #Positive Diff = Upper Right Corner
    imgCorners[2] = points[np.argmax(diff)] #Negative Diff = Bottom Left Corner
    return imgCorners


def adjusted_img(contour_img, main_img):
    
    points, maxArea = outline(contour_img)
    print(points.size)
    if points.size == 8:
        points = corners(points)
        cv2.drawContours(main_img.copy(), points, -1,(0, 0, 230),10)
        temp1 = np.float32(points)
        temp2 = np.float32([[0,0],[450,0],[0,450],[450,450]])
        matrix = cv2.getPerspectiveTransform(temp1,temp2)  
        imagewrap = cv2.warpPerspective(main_img,matrix,(450,450))
        imagewrap = cv2.cvtColor(imagewrap, cv2.COLOR_BGR2GRAY)
                
        return imagewrap

#Alter Function to box_detect(image_input)
def box_detect(file):
    # file = r"C:\Users\atcut\Documents\ML_Proj\Digit Classification\puzzles"
    # file = file + '\\' +random.choice(os.listdir(file))
    img = cv2.imread(file)
    img, test = prep(img)

    img_1 = img.copy()
    contour, hierarchy = cv2.findContours(test,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img_1, contour,-1,(0, 0, 230),3)
    
    result = adjusted_img(contour, img)
    return result
    

#Break up grid into 9x9 
#Predict each cell's number & and threshold is above 70% to accept it otherwise default 0
def cell_division(image):
    rows = np.vsplit(image, 9)
    matrix = []
    for i in rows:
        cells = np.hsplit(i, 9)
        for j in cells:
            matrix.append(j)
        
    return matrix

def sudoku_predict(grid, model):
    assert isinstance(grid, list), "Input must be a list"

    if len(grid) != 81:
        raise Exception("List does not have 81 cells. Missing Data")
    
    pre_grid = []
    for c in grid:
        cell = np.asarray(c)
        cell = cell[7:cell.shape[0] - 7, 7:cell.shape[1] -7]
        cell = cv2.resize(cell, (32, 32))
        cell = cell / 255        
        cell = cell.reshape(1, 32, 32, 1)

        predictions = model.predict(cell)
        if np.max(predictions) >= 0.7:
            pre_grid.append(np.argmax(predictions).item())
        else:
            pre_grid.append(0)

    return pre_grid


#requires implementation of accessing File System and selecting an image
#Frontend will handle this aspect and send image through an API

def main(input):
    print("hi", input)
    if (input.lower().endswith(('.png', '.jpg', '.jpeg')) is False):
        raise Exception("Incompatiable File Type.") 
        
    input_crop = box_detect(input) #need to include the file system input but not compatible with Jupiter Notebook

    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    input_crop = cv2.filter2D(input_crop, -1, sharpen_kernel)
    grid = cell_division(input_crop)

    #Model developed in Digits_Detector.ipynb
    p = Path(__file__).with_name('tf_digit_classifier.keras')
    model = keras.models.load_model(p)

    output = sudoku_predict(grid, model)
    
    res_matrix =[]

    for i in range(9):
        res_matrix.append(output[i*9:(i+1)*9])
        print(res_matrix[i])

    return output


def openFile():
    filepath =filedialog.askopenfilename(filetypes=[("Allowed File Types", ".jpg .jpeg .png")])
    #root.withdraw()
    print(filepath)
    result = main(filepath)
    root.destroy()

root = tkinter.Tk()
button = tkinter.Button(root, text = "Select File", command= openFile)
button.pack()
root.mainloop()
