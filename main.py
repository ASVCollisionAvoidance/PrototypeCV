import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import os
from horizon import detect_horizon
from mser import detect_MSERregions

show = 1 # if show = 1: displays figures, if show = 0: suppresses figures

# returns the connected components and a mask from the MSER regions
def getCC(regions, gray):
    hulls = [cv.convexHull(p.reshape(-1, 1, 2)) for p in regions]
    cv.polylines(gray, hulls, 1, (0, 255, 0), 3)

    mask = np.zeros((gray.shape[0], gray.shape[1], 1), dtype=np.uint8)
    mask = cv.dilate(mask, np.ones((150, 150), np.uint8))

    for contour in hulls:
        cv.drawContours(mask, [contour], -1, (255, 255, 255), -1)

    retval, labels = cv.connectedComponents(mask)

    return (labels, mask)


for filename in os.listdir('../PrototypeCV/Inputs'):
    if filename.endswith(".jpg") or filename.endswith(".JPG"):
        name = filename.split(".")[0]
        pic = cv.imread('Inputs/' + filename)

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

        b_with_image = cv.bitwise_and(pic, pic, mask=threshB)
        #plt.imshow(b_with_image)
        #plt.show()


        # Thresholding an image based on the Value channel of HSV colour space
        ret, threshVal = cv.threshold(v,aveV,255,0)
        #plt.imshow(threshVal)
        #plt.show()

        val_w_image = cv.bitwise_and(pic, pic, mask=threshVal)
        #plt.imshow(val_w_image)
        #plt.show()

        # find contours with binary image
        imCopy = pic.copy()
        contours, hierarchy = cv.findContours(threshB, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        cv.drawContours(imCopy, contours, -1, (0,255,0), 3)
        #plt.imshow(imCopy)
        #plt.show()

        # find horizon
        horizon = detect_horizon(pic)
        gray = cv.cvtColor(horizon,cv.COLOR_BGR2GRAY)
        plt.imshow(horizon)
        plt.show()

        regions = detect_MSERregions(gray)

        labels, mask = getCC(regions, gray)
        print(labels)

        print("\nnum connected components: " + str(int(len(labels))) + "\n")

        label_hue = np.uint8(179*labels/np.max(labels))
        blank_ch = 255*np.ones_like(label_hue)
        labeled_img = cv.merge([label_hue, blank_ch, blank_ch])

        labeled_img = cv.cvtColor(labeled_img, cv.COLOR_HSV2BGR)

        labeled_img[label_hue==0] = 0

        plt.imshow(labeled_img)
        plt.show()

        #for i in range(1,int(retval)):
        #    continue


        mask_with_image = cv.bitwise_and(pic, pic, mask=mask)

        cv.imwrite('Outputs/' + name + '-output.jpg', mask_with_image)
        cv.imwrite('Outputs/' + name + '-mask-only.jpg', mask)
        cv.imwrite('Outputs/' + name + '.jpg', pic)
        cv.imwrite('Outputs/' + name + '-thresh.jpg', b_with_image)
        cv.imwrite('Outputs/' + name + '-threshVal.jpg', val_w_image)
        cv.imwrite('Outputs_horizon/' + name + '-horizon.jpg', horizon)

        if show:
            print("Original")
            plt.imshow(pic)
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
