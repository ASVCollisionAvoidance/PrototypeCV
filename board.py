import numpy as np
import cv2 as cv

def removeBoard(pic):
    """
    Removes the pixels below the tip of the surfboard,
    based on a known pixel coordinate of the tip of the surfboard.

    The topOfBoard variable needs to be calibrated when setting up the board
    before any operation of the ASV.

    Parameters
    ----------
    pic: numpy N-dimensional array
        input image with the pixels above the horizon already removed

    Returns
    -------
    pic.copy(): numpy N-dimensional array
        input image with pixels below the a certain row value
        converted to black
    """
    topOfBoard = 1970

    vertices = np.array([[(0,pic.shape[0]), (0,1970), (pic.shape[1], topOfBoard), (pic.shape[1], pic.shape[0])]], dtype = np.int32)
    cv.fillConvexPoly(pic, vertices,(0,0,0))

    return pic.copy()
