import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import os

show = 0 # if show = 1: displays figures, if show = 0: suppresses figures

for filename in os.listdir('../PrototypeCV/Inputs'):
    if filename.endswith(".jpg") or filename.endswith(".JPG"):
        name = filename.split(".")[0]
        pic = cv.imread('Inputs/' + filename)
        b,g,r = cv.split(pic)
        pic2 = cv.merge([r,g,b])

        # convert to grayscale image
        gray = cv.cvtColor(pic,cv.COLOR_BGR2GRAY)
        #plt.imshow(gray)
        #plt.show()

        # convert to lab colour space
        lab = cv.cvtColor(pic, cv.COLOR_BGR2LAB)
        l,a,b = cv.split(lab)
        aveB = np.mean(b) # the b* channel shows high contrast for the surfboard
        stdB = np.std(b)

        # convert to hsv colour space
        hsv = cv.cvtColor(pic, cv.COLOR_BGR2HSV)
        h,s,v = cv.split(hsv)
        aveH = np.mean(h)
        aveV = np.mean(v)

        # get image size
        imgSize = gray.shape
        imgArea = imgSize[0]*imgSize[1]
        aveGray = np.mean(gray)

        print("name: " + name + "\n")

        # Thresholding an image based on b* channel of LAB colour space
        ret, threshB = cv.threshold(b,aveB + 1.75*stdB,255,0)
        #plt.imshow(thresh)
        #plt.show()

        b_with_image = cv.bitwise_and(pic2, pic2, mask=threshB)
        #plt.imshow(b_with_image)
        #plt.show()


        # Thresholding an image based on the Value channel of HSV colour space
        ret, threshVal = cv.threshold(v,aveV,255,0)
        #plt.imshow(threshVal)
        #plt.show()

        val_w_image = cv.bitwise_and(pic2, pic2, mask=threshVal)
        #plt.imshow(val_w_image)
        #plt.show()

        # find contours with binary image
        imCopy = pic2.copy()
        contours, hierarchy = cv.findContours(threshB, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        cv.drawContours(imCopy, contours, -1, (0,255,0), 3)
        #plt.imshow(imCopy)
        #plt.show()

        # Canny Edge Detection
        edges = cv.Canny(gray,125,175)
        #plt.imshow(edges)
        #plt.show()

        # Hough Line Transform
        lines = cv.HoughLines(edges,1,np.pi/180,200)

        xyList = []
        imCopy = pic2.copy()
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

        m = (y2-y1)/(x2-x1)
        b = (x1/(x1-x2))*y2 - (x2/(x1-x2))*y1

        horizon = pic2.copy()
        p1x = 0
        p1y = int(b)
        p2x = 3648
        p2y = int(m*p2x + b)
        cv.line(horizon,(p1x,p1y), (p2x,p2y), (255,0,0), 12)
        #plt.imshow(horizon)
        #plt.show()

        # MSER
        _delta = 5
        _min_area = int(0.001*imgArea)
        _max_area = int(0.05*imgArea)
        _max_variation = 0.5 # default = 0.25
        _min_diversity = 0.2 # default = 0.2
        _max_evolution = 200
        _area_threshold = 1.01
        _min_margin = 0.03
        _edge_blur_size = 5

        mser = cv.MSER_create(_delta, _min_area, _max_area, _max_variation, _min_diversity, _max_evolution, _area_threshold, _min_margin, _edge_blur_size)
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
        cv.imwrite('Outputs/' + name + '.jpg', pic)
        cv.imwrite('Outputs/' + name + '-thresh.jpg', b_with_image)
        cv.imwrite('Outputs/' + name + '-threshVal.jpg', val_w_image)
        cv.imwrite('Outputs_horizon/' + name + '-horizon.jpg', horizon)

        if show:
            print("Original")
            plt.imshow(pic2)
            plt.show()

            print("Draw Contours")
            plt.imshow(gray)
            plt.show()

            print("Mask with Image: ")
            plt.imshow(mask_with_image)
            plt.show()

            print("Mask: ")
            plt.imshow(mask)
            plt.show()
