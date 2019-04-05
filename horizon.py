import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import parameters as p

def detect_horizon(pic):
    """
    Detects and removes the area above the horizon in each input photo.

    Uses Canny edge detection to find the edges in the photo and then Hough
    line transform to find the straight line formed by the horizon.

    Parameters
    ----------
    pic: numpy N-dimensional array
        input picture in which to detect horizon

    Returns
    -------
    imCopy: numpy N-dimensional array
        a copy of the input image with all of the
        pixels above the horizon line converted to black
    """

    # convert to grayscale
    gray = cv.cvtColor(pic,cv.COLOR_BGR2GRAY)

    # Canny Edge Detection
    edges = cv.Canny(gray,125,175)

    # Hough Line Transform
    lines = cv.HoughLines(edges,1,np.pi/180,200)

    xyList = []
    imCopy = pic.copy()
    for rho,theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        xyList = [(x1,y1), (x2,y2)]

        cv.line(imCopy,(x1,y1),(x2,y2),(0,0,255),10)

    x1 = xyList[0][0]
    x2 = xyList[1][0]
    y1 = xyList[0][1]
    y2 = xyList[1][1]

    # find slope and y-intercept
    m = (y2-y1)/(x2-x1)
    b = (x1/(x1-x2))*y2 - (x2/(x1-x2))*y1

    horizon = pic.copy()
    p1x = 0
    p1y = int(b)
    p2x = horizon.shape[1]
    p2y = int(m*p2x + b)
    cv.line(horizon,(p1x,p1y), (p2x,p2y), (255,0,0), 15)
    mid = m*p.tip[0]+b

    imCopy = pic.copy()
    vertices = np.array([[(p1x,p1y), (p2x,p2y), (horizon.shape[1],0), (0,0)]], dtype=np.int32)
    cv.fillConvexPoly(imCopy,vertices,(0,0,0))

    return imCopy, mid
