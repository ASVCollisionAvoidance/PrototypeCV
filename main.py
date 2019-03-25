import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import os
from horizon import detect_horizon
from mser import detect_MSERregions
from kmeans import classifyROI
from board import removeBoard
from distance import findDistances

show = 0 # if show = 1: displays figures, if show = 0: suppresses figures
save = 1 # if save = 1: saves output images to Outputs folder

# returns the connected components and a mask from the MSER regions
def getCC(regions, gray):
    hulls = [cv.convexHull(p.reshape(-1, 1, 2)) for p in regions]
    cv.polylines(gray, hulls, 1, (0, 255, 0), 3)

    mask = np.zeros((gray.shape[0], gray.shape[1], 1), dtype=np.uint8)
    mask = cv.dilate(mask, np.ones((150, 150), np.uint8))

    for contour in hulls:
        cv.drawContours(mask, [contour], -1, (255, 255, 255), -1)

    retval, labels = cv.connectedComponents(mask)

    return (retval, labels, mask)


for filename in os.listdir('../PrototypeCV/Inputs'):
    if filename.endswith(".jpg") or filename.endswith(".JPG"):
        # read image file
        name = filename.split(".")[0]
        pic = cv.imread('Inputs/' + filename)
        print("name: " + name + "\n")
        print("image size: " + str(pic.shape[0]) + " x " + str(pic.shape[1]))

        # display original image (remove this part when done project)
        plt.imshow(pic)
        plt.show()


        # find horizon
        horizon = detect_horizon(pic)
        #plt.imshow(horizon)
        #plt.show()

        # remove part of picture below/beside board
        noBoard = removeBoard(horizon)
        gray = cv.cvtColor(noBoard,cv.COLOR_BGR2GRAY)
        #plt.imshow(noBoard)
        #plt.show()

        # detect regions of interest with MSER (maximally stable extremal regions) feature detector
        regions = detect_MSERregions(gray)

        # get the connected components from the MSER regions
        retval, labels, mask = getCC(regions, gray)

        mserRegions = cv.bitwise_and(pic, pic, mask=mask)
        #plt.imshow(mserRegions)
        #plt.show()

        pitch = 1 # SUSCRIBE TO AHRS.PY from Adrien's code

        # classify the detected ROI as 'Objects to Avoid' vs. other
        if(int(retval) > 2):
            averageXY, mask, labels_kmeans = classifyROI(retval, labels, mask, pic)
            print("\n\nAverageXY!")
            print(averageXY)

            distanceList = findDistances(averageXY, pitch)
            print("\nDistance List!")
            print(distanceList)
        else:
            distanceList = []
            print("\nDistance List!")
            print(distanceList)

        mask_with_image = cv.bitwise_and(pic, pic, mask=mask)
        #plt.imshow(mask_with_image)
        #plt.show()

        if save:
            mask_with_image = cv.bitwise_and(pic, pic, mask=mask)

            #cv.imwrite('Outputs/' + name + '-output.jpg', mask_with_image)
            #cv.imwrite('Outputs/' + name + '-mask-only.jpg', mask)
            cv.imwrite('Outputs/' + name + '.jpg', pic)
            #cv.imwrite('Outputs_horizon/' + name + '-horizon.jpg', horizon)
            cv.imwrite('Outputs/' + name + '-mser.jpg', mserRegions)

        if show:
            mask_with_image = cv.bitwise_and(pic, pic, mask=mask)

            print("Original")
            plt.imshow(pic)
            plt.show()

            print("Mask with Image: ")
            plt.imshow(mask_with_image)
            plt.show()

            print("Mask: ")
            plt.imshow(mask)
            plt.show()
