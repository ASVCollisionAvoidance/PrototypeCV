# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:27:46 2019

@author: ryley
"""

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('Inputs/GOPR0066.jpg',0)

#cv.circle(img, (1900, 1400), 1, (0,0,255), -1)
#cv.circle(img, (2000, 1400), 1, (0,0,255), -1)
#cv.circle(img, (0, 3000), 1, (0,0,255), -1)
#cv.circle(img, (4000, 3000), 1, (0,0,255), -1)

horizon = 1350

pts1 = np.float32([[1900, horizon], [2000, horizon],[0, 3000], [4000, 3000]])
pts2 = np.float32([[1800, 0], [2200, 0], [1800, 3000], [2200, 3000]])
matrix = cv.getPerspectiveTransform(pts1, pts2)
img2 = cv.warpPerspective(img, matrix, (4000, 3000))

plt.imshow(img2)
plt.show()

cv.imwrite('Outputs/distTest.jpg', img2)