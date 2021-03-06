# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:27:46 2019

@author: ryley
"""

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import parameters as p
import transform

#   Uses an inverse perspective mapping to find the boundaries of the regions
#   relative to the board
#   Returns a list corresponding to each region
#   Each entry is a tuple of distances ordered as (xmin xmax ymin ymax)

def findDistances(horizon, regionCount, points):

    pts1 = np.float32([[p.tip[0]-50, horizon], [p.tip[0]+50, horizon],[0, 3000], [4000, 3000]])
    pts2 = np.float32([[1800, 0], [2200, 0], [1800, 3000], [2200, 3000]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)

    transformed_mask = cv.warpPerspective(points, matrix, (4000, 3000))
    transformed_tip = transform.transform(p.tip, matrix)
    transformed_edge = transform.transform(p.edge, matrix)

    regionCount, transformed_mask = cv.connectedComponents(transformed_mask)
    sorted_mask = np.uint8(transformed_mask)
    transformed_points = []
    for i in range(1, regionCount):
        transformed_points.append(np.where(sorted_mask == i))

    minx = []
    maxx = []
    miny = []
    maxy = []
    # Finds the extremal lines bounding each region
    # y component is swapped due pixel index starting from the top of the image
    for blob in transformed_points:
        minx.append(np.amin(blob[1]))
        maxx.append(np.amax(blob[1]))
        miny.append(np.amax(blob[0]))
        maxy.append(np.amin(blob[0]))

    # Find number of pixels that the known distances correspond to
    xref, yref = transformed_edge[0]-transformed_tip[0], transformed_edge[1]-transformed_tip[1]

    minxdist = list(map((lambda x: (x-transformed_tip[0])/xref*p.xscale), minx))
    maxxdist = list(map((lambda x: (x-transformed_tip[0])/xref*p.xscale), maxx))
    minydist = list(map((lambda x: (transformed_edge[1]-x)/yref*p.yscale), miny))
    maxydist = list(map((lambda x: (transformed_edge[1]-x)/yref*p.yscale), maxy))

    dist = list(zip(minxdist, maxxdist, minydist, maxydist))

    return dist
