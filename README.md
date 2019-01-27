# Draft Computer Vision Algorithm for ASV project
* processes a folder of images at a time
* add JPEG images to 'Inputs' folder to process new images

## MSER
Uses MSER (Maximally Stable Extremal Regions) algorithm to detect Regions of Interest within image.

#### Important Parameters:
**minArea**: minimum area of blob to be detected
* 0.1% of total image area

**maxArea**: maximum area of blob to be detected
* 30% of total image area

**delta**: maximum variation from one blob to the next
* current set at delta = 12 (needs to be adjusted)
