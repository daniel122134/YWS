#!/usr/bin/env python
# coding: utf-8

# ## Detection of size of body parts
# In this project we are going to use, image processing to calculate the size of body parts(shoulders), from the images and then predict the shirt size for the person.
# 
# This Notebook is divided into parts-
# 1. Crop the images into suitable size
# 2. Image Segmentation
# 3. Calcuate the distances between the extreme points
# 4. Predict the shoulder width

# In[1]:
from scipy.spatial import distance as dist
import imutils
import pandas as pd
import seaborn as sns
import sklearn.preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import sklearn.metrics as m


import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


# We have made a dataset which contains images clicked as-
# - Distance between the subject and camera is approx. 75cm
# - Distance between the subject and camera is approx. 100cm
# - Distance between the subject and camera is approx. 200cm
# 
# Nomenclature- 75cm: img75-1;
#               100cm: img100-1;
#               200cm: img200-1;
# where 1 is the number assigned to the subject

# In[2]:




# cut to top
def crop_to_top(image,exTop):
        x1=image.shape[0]*1/2
        #x1=image.shape[0]*4/9
        x2=image.shape[0]
        y2=image.shape[1]
        #print(x1," height= ",x2," width= ",y2)
        #cropped_img = image(Rect(0, image.rows/2, image.cols, image.rows/2))
        cropped_img = image[int(exTop[1]):x2,0:int(y2)]
        #print("cropped_img")
        #print("height=",cropped_img.shape[0]," width=",cropped_img.shape[1])
        return cropped_img

def get_top_of_head(image):
        cropimg = crop_bottom_half(image)
        cropped = cv.GaussianBlur(cropimg, (5,5),0)
        gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(gray, 0, 255,cv.THRESH_BINARY_INV + cv.THRESH_OTSU )
        kernel = np.ones((5,5),np.uint8)
        closing = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
        edges = cv.Canny(closing,100,200)
        
        kernel = np.ones((5,5),np.uint8)
        opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel)
        edges_o = cv.Canny(opening,100,200)
        
        
        cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv.contourArea)
        
        # determine the most extreme points along the contour
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])
        return extTop

# In[3]:




def get_line_data(image_path):
        image = cv.imread(image_path)
        image.shape
        return get_line_data_for_image(image)

def get_line_data_for_image(image):
        
        top_of_head = get_top_of_head(image)
        
        cropped = crop_to_top(image,top_of_head)
        plt.imshow(cropped)
        plt.show()
        
        cropimg = crop_three4(cropped)
        plt.imshow(cropimg)
        plt.show()
        cropped = cv.GaussianBlur(cropimg, (5,5),0)
        gray = cv.cvtColor(cropped, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(gray, 0, 255,cv.THRESH_BINARY_INV + cv.THRESH_OTSU )
        kernel = np.ones((5,5),np.uint8)
        closing = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
        edges = cv.Canny(closing,100,200)
        
        kernel = np.ones((5,5),np.uint8)
        opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel)
        edges_o = cv.Canny(opening,100,200)
        plt.imshow(edges_o)
        plt.show()
        
        cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv.contourArea)
        
        # determine the most extreme points along the contour
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])
        extract_prediction(extLeft,extRight,extTop,extBot,c,cropped)
        return extLeft,extRight,top_of_head


# In[4]:


def crop_bottom_half(image):
        x1=image.shape[0]*1/2
        #x1=image.shape[0]*4/9
        x2=image.shape[0]
        y2=image.shape[1]
        #print(x1," height= ",x2," width= ",y2)
        #cropped_img = image(Rect(0, image.rows/2, image.cols, image.rows/2))
        cropped_img = image[0:int(x1),0:int(y2)]
        #print("cropped_img")
        #print("height=",cropped_img.shape[0]," width=",cropped_img.shape[1])
        return cropped_img

def crop_three4(image):
        x1=image.shape[0]*1/4
        #x1=image.shape[0]*4/9
        x2=image.shape[0]
        y2=image.shape[1]
        #print(x1," height= ",x2," width= ",y2)
        #cropped_img = image(Rect(0, image.rows/2, image.cols, image.rows/2))
        cropped_img = image[0:int(x1),0:int(y2)]
        #print("cropped_img")
        #print("height=",cropped_img.shape[0]," width=",cropped_img.shape[1])
        return cropped_img


def crop_top_half(image):
        x1=image.shape[0]*1/2
        #x1=image.shape[0]*4/9
        x2=image.shape[0]
        y2=image.shape[1]
        #print(x1," height= ",x2," width= ",y2)
        #cropped_img = image(Rect(0, image.rows/2, image.cols, image.rows/2))
        cropped_img = image[int(x1):x2,0:int(y2)]
        #print("cropped_img")
        #print("height=",cropped_img.shape[0]," width=",cropped_img.shape[1])
        return cropped_img

# In[5]:




# In[6]:


def crop_twobynine(image):
        x1=image.shape[0]*2/9
        x2=image.shape[0]
        y2=image.shape[1]
        #print(x1," height= ",x2," width= ",y2)
        #cropped_img = image(Rect(0, image.rows/2, image.cols, image.rows/2))
        cropped_img = image[0:int(x1),0:int(y2)]
        #print("cropped_img")
        #print("height=",cropped_img.shape[0]," width=",cropped_img.shape[1])
        return cropped_img


# In[7]:




def extract_prediction(extLeft,extRight,extTop,extBot, c,image ):


        #dB1 = dist.euclidean((extLeft[0], extRight[0]), (extLeft[1], extRight[1]))
        #print("left: ",extLeft," right: ",extRight)

        dB = dist.euclidean(extLeft,extRight)
        dB = dist.euclidean(extLeft,extRight)

        #dB = dist.euclidean(extLeft,extBot)
        #print(dB," ",dB1)
        print(dB)
        cv.putText(image, "{:.1f}in".format(dB),
                 (10,500), cv.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

        # draw the outline of the object, then draw each of the
        # extreme points, where the left-most is red, right-most
        # is green, top-most is blue, and bottom-most is teal
        print("hi", cv.drawContours(image, [c], -1, (0, 255, 255), 2))
        cv.drawContours(image, [c], -1, (0, 255, 255), 2)
        cv.circle(image, extLeft, 8, (0, 0, 255), -1)
        cv.circle(image, extRight, 8, (0, 255, 0), -1)
        cv.circle(image, extTop, 8, (255, 0, 0), -1)
        cv.circle(image, extBot, 8, (255, 255, 0), -1)
        plt.imshow(image)



        df = pd.read_csv("backend/book.csv")
        Y=df[["Actual (in cm)"]]
        z=df[["ratio75","ratio100","ratio150"]]#for multiple linear regression

        predict =z.iloc[32:40,]
        vector=Y.iloc[0:32,]
        poly = PolynomialFeatures(degree=2)
        x=z.iloc[0:32,]

        X_ = poly.fit_transform(x)
        predict_ = poly.fit_transform(predict)
        clf = sklearn.linear_model.LinearRegression()
        clf.fit(X_, vector)
        Yhat=clf.predict(predict_)
        print("predicted values")
        print(Yhat)
        print("--------------------------")


        # In[21]:


        print(m.r2_score(Y[32:40],Yhat))
        print(m.mean_squared_error(Y[32:40],Yhat))
        ax1 = sns.distplot(df['Actual (in cm)'], hist=False, color="r", label="Actual Value")
        sns.distplot(Yhat, hist=False, color="b", label="Fitted Values" , ax=ax1)#Yhat is given as a predicted values (calculated before)
        plt.show()

if __name__ == '__main__':
        get_line_data("backend/shirtSize/front.jpeg")