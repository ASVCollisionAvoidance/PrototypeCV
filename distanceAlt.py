# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:27:46 2019

@author: ryley
"""

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

#img = cv.imread('Inputs/GOPR0076.jpg',0)

#horizon = 1400

xscale = 0.25   #Distance from centre to edge of board in meters
yscale = 1      #Distance from centre to tip of board in meters

def findDistance(img, horizon, tip, edge, points):
    pts1 = np.float32([[1900, horizon], [2000, horizon],[0, 3000], [4000, 3000]])
    pts2 = np.float32([[1800, 0], [2200, 0], [1800, 3000], [2200, 3000]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
#    img2 = cv.warpPerspective(img, matrix, (4000, 3000))
    transformed_points = cv.warpPerspective(points, matrix, (4000, 3000))
    minx = []
    maxx = []
    miny = []
    maxy = []
    for blob in transformed_points:
        minx.append(np.argmin(blob,0))
        maxx.append(np.argmax(blob,0))
        miny.append(np.argmin(blob,1))
        maxy.append(np.argmax(blob,1))
        
    xref, yref = edge-tip[0], 3000-tip[1]
    minxdist = (minx-tip[0])/xref*xscale
    maxxdist = (maxx-tip[0])/xref*xscale
    minydist = (miny-tip[1])/yref*yscale
    maxydist = (maxy-tip[1])/yref*yscale
    
    dist = zip(minxdist, maxxdist, minydist, maxydist)
    
    return dist

#plt.imshow(img2)
#plt.show()

#cv.imwrite('Outputs/distTest.jpg', img2)