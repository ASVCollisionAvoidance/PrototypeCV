import cv2 as cv
import matplotlib.pyplot as plt

def detect_MSERregions(pic):
    imgArea = pic.shape[0]*pic.shape[1]

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
    regions, boxes = mser.detectRegions(pic)

    return regions
