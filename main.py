import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import os
from horizon import detect_horizon
from mser import detect_MSERregions

show = 0 # if show = 1: displays figures, if show = 0: suppresses figures
save = 0 # if save = 1: saves output images to Outputs folder

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

        # convert to grayscale image
        gray = cv.cvtColor(pic,cv.COLOR_BGR2GRAY)
        plt.imshow(gray)
        plt.show()

        # find horizon
        horizon = detect_horizon(pic)
        gray = cv.cvtColor(horizon,cv.COLOR_BGR2GRAY)

        # detect regions of interest with MSER (maximally stable extremal regions) feature detector
        regions = detect_MSERregions(gray)
        print("num of MSER regions: " + str(len(regions)))

        # get the connected components from the MSER regions
        retval, labels, mask = getCC(regions, gray)

        mask_with_image = cv.bitwise_and(pic, pic, mask=mask)
        plt.imshow(mask_with_image)
        plt.show()

        print("num of CC: " + str(int(retval-1)))

        # calculate stats on the connected components
        sample = np.uint8(labels)
        print("sample shape: " + str(sample.shape) + "\n")
        print("labels image size: " + str(labels.shape[0]) + " x " + str(labels.shape[1]))
        data = [[0, 0, 0] for _ in range(int(retval)-1)]

        print("program isn't frozen yet\nretval: " + str(retval))

        for i in range(int(retval)-1):
            indices = np.where(sample == i+1)
            coordinates = list(zip(indices[0], indices[1]))
            pixels = np.asarray(coordinates)
            print("i: " + str(i))

            print("num coordinates: " + str(len(indices[0])))
            if(len(pixels) > 0):
                print("max pixel coordinate: " + str(max(indices[0])) + ", " + str(max(indices[1])))
                data[i][0] = np.mean(pic[indices[0], indices[1]])

        data = np.asarray(data)
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
                print(labels_kmeans[i][0])
                indices = np.where(sample == i+1)
                coordinates = list(zip(indices[0], indices[1]))
                pixels = np.asarray(coordinates)

                if(len(pixels) > 0):
                    mask[indices[0], indices[1]] = 0

        mask_with_image = cv.bitwise_and(pic, pic, mask=mask)
        plt.imshow(mask_with_image)
        plt.show()

        if save:
            mask_with_image = cv.bitwise_and(pic, pic, mask=mask)

            cv.imwrite('Outputs/' + name + '-output.jpg', mask_with_image)
            cv.imwrite('Outputs/' + name + '-mask-only.jpg', mask)
            cv.imwrite('Outputs/' + name + '.jpg', pic)
            cv.imwrite('Outputs_horizon/' + name + '-horizon.jpg', horizon)

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
