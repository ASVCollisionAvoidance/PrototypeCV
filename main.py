import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import os

show = 0 # if show = 1: displays figures, if show = 0: suppresses figures

for filename in os.listdir('../PrototypeCV/Inputs'):
    if filename.endswith(".jpg"):
        name = filename.split(".")[0]
        pic = cv.imread('Inputs/' + filename)

        # convert to grayscale image
        gray = cv.cvtColor(pic,cv.COLOR_BGR2GRAY)

        # get image size
        imgSize = gray.shape

        # write a function to get info about images (ex. max and min intensity...)

        # MSER
        mser = cv.MSER_create()
        mser.setMinArea(1000) #100,000
        mser.setMaxArea(50000) #1,000,000
        mser.setDelta(25)
        regions, boxes = mser.detectRegions(gray)

        numRegions = len(regions)

        hulls = [cv.convexHull(p.reshape(-1, 1, 2)) for p in regions]
        cv.polylines(gray, hulls, 1, (0, 255, 0), 3)

        mask = np.zeros((imgSize[0], imgSize[1], 1), dtype=np.uint8)
        mask = cv.dilate(mask, np.ones((150, 150), np.uint8))

        for contour in hulls:
            cv.drawContours(mask, [contour], -1, (255, 255, 255), -1)

        mask_with_image = cv.bitwise_and(pic, pic, mask=mask)

        cv.imwrite('Outputs/' + name + '-output.jpg', mask_with_image)
        cv.imwrite('Outputs/' + name + '-mask-only.jpg', mask)

        if show:
            print("Draw Contours")
            plt.imshow(gray)
            plt.show()

            print("Mask with Image: ")
            plt.imshow(mask_with_image)
            plt.show()

            print("Mask: ")
            plt.imshow(mask)
            plt.show()

        #vis = pic.copy()

        #for p in regions:
        #    xmax, ymax = np.amax(p, axis=0)
        #    xmin, ymin = np.amin(p, axis=0)
        #    cv.rectangle(vis, (xmin,ymax), (xmax,ymin), (0, 255, 0), 1)

        #print("Rectangles: ")
        #plt.imshow(vis)
        #plt.show()
