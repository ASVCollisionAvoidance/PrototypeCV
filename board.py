import numpy as np
import cv2 as cv

def removeBoard(pic):
    topOfBoard = 1970

    vertices = np.array([[(0,pic.shape[0]), (0,1970), (pic.shape[1], topOfBoard), (pic.shape[1], pic.shape[0])]], dtype = np.int32)
    cv.fillConvexPoly(pic, vertices,(0,0,0))

    return pic.copy()
