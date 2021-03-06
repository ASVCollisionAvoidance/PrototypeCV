# TODO
# import asyncio
import logging

# TODO
# move this repo into auv-control-pi and import as required to integrate
# from ..wamp import ApplicationSession, rpc
# from auv_control_pi.utils import Point

import time
import subprocess
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import os
import parameters as p
from helpers/horizon import detect_horizon
from helpers/mser import detect_MSERregions
from helpers/kmeans import classifyROI
from helpers/board import removeBoard
from helpers/distance import findDistances

logger = logging.getLogger(__name__)

def getCC(regions, gray):
    """
    When detecting regions of interest using MSER feature detector,
    some of the regions will be connected within the image.
    This function finds the distinct, unique connected componenents
    within the image and outputs the number of connected components,
    their labels and the mask of those regions.

    Parameters
    ----------
    regions: list
        a list of arrays in which each array contains all of the pixel coordinates
        of the regions detected by the MSER algorithm

    gray: numpy N-dimensional array
        the grayscale input image with pixels above the horizon removed
        and pixels below the tip of the surfboard removed

    Returns
    -------
        retval: int
            the number of connected components

        labels: list
            each of the connected components is given a label,
            starting at 0 and increasing by 1 for each additional connected component

        mask: numpy N-dimensional array
            a binary image in which the regions of interest have pixel value 255 (white),
            and every other pixel value is 0 (black)
    """
    hulls = [cv.convexHull(p.reshape(-1, 1, 2)) for p in regions]
    cv.polylines(gray, hulls, 1, (0, 255, 0), 3)

    mask = np.zeros((gray.shape[0], gray.shape[1], 1), dtype=np.uint8)
    mask = cv.dilate(mask, np.ones((150, 150), np.uint8))

    for contour in hulls:
        cv.drawContours(mask, [contour], -1, (255, 255, 255), -1)

    retval, labels = cv.connectedComponents(mask)

    return (retval, labels, mask)


def processImage(pic):
    """
    Entire obstacle detection algorithm.

    Takes the image input and calls the various functions necessary to
    detect the obstacles within the image. Then, calculates the distances
    to each of the detected obstacles and outputs these distances in a list.

    Parameters
    ----------
    pic: numpy N-dimensional array
        input image as taken by camera

    Returns
    -------
    distanceList: list
        a list of (x, y) tuples that represent the average
        distances in cm of each detected object

    mask: numpy N-dimensional array
        a binary image only containing the regions classified
        as an obstacle
    """
    # find horizon
    horizon, midpoint= detect_horizon(pic)

    # remove part of picture below/beside board
    noBoard = removeBoard(horizon)
    gray = cv.cvtColor(noBoard,cv.COLOR_BGR2GRAY)

    # detect regions of interest with MSER (maximally stable extremal regions) feature detector
    regions = detect_MSERregions(gray)

    # get the connected components from the MSER regions
    retval, labels, mask = getCC(regions, gray)

    mserRegions = cv.bitwise_and(pic, pic, mask=mask)

    # classify the detected ROI as 'Objects to Avoid' vs. other
    if(int(retval) >= 2):
        averageXY, mask, retval, sample = classifyROI(retval, labels, mask, pic)
        distanceList = findDistances(midpoint, retval, mask)
    else:
        distanceList = []

    return (distanceList, mask)

# TODO
# redefine this class to match the component convention
# class CV(ApplicationSession):
class CV:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        os.system("pwd")
        os.system("./camera/setphotomode.sh local")
        self.current_location = None
        self.obstacle_distances = []
        self.update_frequency = 0.5

    # TODO
    # subscribe to gps so that distances can be mapped later
    # @subscribe('gps.update')
    # def _update_gps(self, data):
    #     self.current_location = Point(lat=data.get('lat'), lng=data.get('lng'))

    # TODO
    # redefine this function to match the component convention
    # async def update(self):
    #     """Publish current state to anyone listening
    #     """
    def cvrun(self):
        try:
            while True:
                # send command to camera to take photo
                os.system("./camera/takephoto.sh local")
                # download latest photo off camera and save in /camera/photos/
                os.system("./camera/getlatestphoto.sh local")

                latestphoto=os.listdir("camera/photos/")[-1]
                pic = cv.imread('camera/photos/' + latestphoto)

                distanceList, mask = processImage(pic)
                self.obstacle_distances = distanceList # overwrites distances w output

                payload = {
                    'current_location': self.current_location,
                    'obstacle_distances': self.obstacle_distances
                }

                # TODO
                # FIRST trade print statements for self.publish
                # SECOND incorporate GPS data and map to absolute GPS location
                print("Obstacle distances: ")
                print(self.obstacle_distances)
                # self.publish('cv.update', payload)

                # writes the names of photos of interest to interestphotos.txt
                if len(distanceList) != 0:
                    file = open("interestphotos.txt", "a")
                    file.write(latestphoto + "\n")
                    file.close()

                os.system("./camera/deletelatestphoto.sh local")

                # TODO
                # trade time.sleep() for await asyncio.sleep()
                time.sleep(1 / self.update_frequency)
                # await asyncio.sleep(1/self.update_frequency)

        except KeyboardInterrupt: # exits when ctrl+c is pressed
            pass

# runs the while true loop that continuously takes+processes photos
realtimeprocess = CV()
realtimeprocess.cvrun()
