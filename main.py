import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import os

show = 0 # if show = 1: displays figures, if show = 0: suppresses figures

for filename in os.listdir('../PrototypeCV/Inputs'):
    if filename.endswith(".jpg") or filename.endswith(".JPG"):
        name = filename.split(".")[0]
        pic = cv.imread('Inputs/' + filename)

        # convert to grayscale image
        gray = cv.cvtColor(pic,cv.COLOR_BGR2GRAY)

        # get image size
        imgSize = gray.shape
        imgArea = imgSize[0]*imgSize[1]

        # write a function to get info about images (ex. max and min intensity...)
        print("name: " + name)
        print("size: " + str(imgSize))
        print("area: " + str(imgSize[0]*imgSize[1]))
        print("Max pixel value: " + str(np.amax(gray)))
        print("Min pixel value: " + str(np.amin(gray)))
        print("Average pixel value: " + str(np.mean(gray)))
        print("Standard deviation: " + str(np.std(gray)/255*100) + '%\n')

        # MSER
        _delta = 5
        _min_area = int(0.005*imgArea)
        _max_area = int(0.1*imgArea)
        _max_variation = 0.15 # default = 0.25
        _min_diversity = 0.15 # default = 0.2
        _max_evolution = 200
        _area_threshold = 1.01
        _min_margin = 0.03
        _edge_blur_size = 5

        mser = cv.MSER_create(_delta, _min_area, _max_area, _max_variation, _min_diversity, _max_evolution, _area_threshold, _min_margin, _edge_blur_size)
        #mser.setMinArea(int(0.005*imgArea)) # 0.1% of image area
        #mser.setMaxArea(int(0.20*imgArea)) # 30% of image area
        #mser.setDelta(5) #25 is best for log picture --> need to find a function to get delta
        regions, boxes = mser.detectRegions(gray)

        numRegions = len(regions)
        print("num regions: " + str(numRegions))

        hulls = [cv.convexHull(p.reshape(-1, 1, 2)) for p in regions]
        cv.polylines(gray, hulls, 1, (0, 255, 0), 3)

        mask = np.zeros((imgSize[0], imgSize[1], 1), dtype=np.uint8)
        mask = cv.dilate(mask, np.ones((150, 150), np.uint8))

        for contour in hulls:
            cv.drawContours(mask, [contour], -1, (255, 255, 255), -1)

        mask_with_image = cv.bitwise_and(pic, pic, mask=mask)

        cv.imwrite('Outputs/' + name + '-output.jpg', mask_with_image)
        cv.imwrite('Outputs/' + name + '-mask-only.jpg', mask)
        cv.imwrite('Outputs/' + name + '.jpg', pic)

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
