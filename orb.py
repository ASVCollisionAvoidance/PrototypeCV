# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 12:08:44 2019

@author: ryley
"""

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

nfeatures = 10000
scaleFactor = 1.001
nlevels = 8
edgeThreshold = 31
firstLevel = 0
WTA_K = 2
scoreType = cv.ORB_HARRIS_SCORE
patchSize = 31
fastThreshold = 20

# The draw_keypoints function seems to have been removed in the current version of opencv
# this function is essentially a copy of it
def draw_keypoints(vis, keypoints):
    for n in keypoints:
        x, y = n.pt
        temp_img = cv.circle(vis, (int(x), int(y)), 2, color=(0,128,128))
    return temp_img

def orb(img):
    orb = cv.ORB_create(nfeatures, scaleFactor, nlevels, edgeThreshold, firstLevel, WTA_K, scoreType, patchSize, fastThreshold)

    kp = orb.detect(img, None)
    kp, des = orb.compute(img, kp)

    img2 = draw_keypoints(img, kp)
    return img2