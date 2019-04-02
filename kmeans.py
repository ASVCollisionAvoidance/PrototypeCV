import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def classifyROI(retval, labels, mask, pic):
    """
    Uses k-means clustering to classify the detected regions
    into two distinct groups. One group is considered to be
    obstacles for the surfboard. The other group is discarded.

    Parameters
    ----------
    retval: int
        the number of distinct connected components in the input mask

    labels: numpy N-dimensional array
        each of the connected components in the input mask is given a label,
        starting at 0 and increasing by 1 for each additional connected component

    mask: numpy N-dimensional array
        a binary image in which the regions of interest have a pixel value of 255 (white),
        and every other pixel value is 0 (black)

    pic: numpy N-dimensional array
        the original input photo

    Returns
    -------
    averageXY: list
        the average (x, y) pixel coordinates for each of the regions classified as
        an obstacle

    mask: numpy N-dimensional array
        a binary image only containing the regions classified by k-means clustering
        as an obstacle
    """
    # calculate stats on the connected components
    sample = np.uint8(labels)
    averageXY = [(0,0) for _ in range(int(retval) -1)]
    data = [[0, 0, 0] for _ in range(int(retval)-1)]

    for i in range(int(retval)-1):
        indices = np.where(sample == i+1)

        if(len(indices) > 0):
            data[i][0] = np.mean(pic[indices[0], indices[1]])
            data[i][1] = int(np.mean(indices[0]))
            averageXY[i] = (int(np.mean(indices[1])), int(pic.shape[0] - np.mean(indices[0])))


    data = np.asarray(data)
    averages = np.float32(data[:,0])

    # Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # Set flags (Just to avoid line break in the code)
    flags = cv.KMEANS_RANDOM_CENTERS

    # Apply KMeans
    compactness,labels_kmeans,centers = cv.kmeans(averages,2,None,criteria,10,flags)

    for i in range(int(retval)-1):
        if(labels_kmeans[i][0] == 1):
            indices = np.where(sample == i+1)

            if(len(indices) > 0):
                mask[indices[0], indices[1]] = 0

    return (averageXY, mask)
