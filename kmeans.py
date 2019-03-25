import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def classifyROI(retval, labels, mask, pic):
    # calculate stats on the connected components
    sample = np.uint8(labels)
    averageY = [0 for _ in range(int(retval) -1)]
    data = [[0, 0, 0] for _ in range(int(retval)-1)]

    for i in range(int(retval)-1):
        indices = np.where(sample == i+1)

        if(len(indices) > 0):
            data[i][0] = np.mean(pic[indices[0], indices[1]])
            data[i][1] = int(np.mean(indices[0]))
            averageY[i] = int(np.mean(indices[0]))


    data = np.asarray(data)
    print(data)
    averages = np.float32(data[:,0])

    # Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # Set flags (Just to avoid line break in the code)
    flags = cv.KMEANS_RANDOM_CENTERS

    # Apply KMeans
    compactness,labels_kmeans,centers = cv.kmeans(averages,2,None,criteria,10,flags)
    print(labels_kmeans)

    for i in range(int(retval)-1):
        if(labels_kmeans[i][0] == 1):
            indices = np.where(sample == i+1)

            if(len(indices) > 0):
                mask[indices[0], indices[1]] = 0

    return (averageY, mask, labels_kmeans)
