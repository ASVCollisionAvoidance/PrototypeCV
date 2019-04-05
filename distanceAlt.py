# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:27:46 2019

@author: ryley
"""

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import parameters as p


def findDistance(horizon, regionCount, sample):
    points = []
    for i in range(1, regionCount):
        points.append(np.where(sample == i))
    
    pts1 = np.float32([[p.tip[0]-50, horizon], [p.tip[0]+50, horizon],[0, 3000], [4000, 3000]])
    pts2 = np.float32([[1800, 0], [2200, 0], [1800, 3000], [2200, 3000]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
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
        
    xref, yref = p.edge-p.tip[0], 3000-p.tip[1]
    minxdist = (minx-p.tip[0])/xref*p.xscale
    maxxdist = (maxx-p.tip[0])/xref*p.xscale
    minydist = (miny-p.tip[1])/yref*p.yscale
    maxydist = (maxy-p.tip[1])/yref*p.yscale
    
    dist = zip(minxdist, maxxdist, minydist, maxydist)
    
    return dist