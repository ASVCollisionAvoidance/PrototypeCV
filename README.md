# Draft Computer Vision Algorithm for ASV project
* processes a folder of images at a time
* detects horizon
* detects objects in water

## Important Steps after cloning repo:
1. Create two new folders titled 'Inputs' and 'Outputs', respectively.
2. Add images to be processed into the Inputs folder.

### MSER
Uses MSER (Maximally Stable Extremal Regions) algorithm to detect Regions of Interest within image.

#### Important Parameters:
**minArea**: minimum area of blob to be detected
* 0.1% of total image area

**maxArea**: maximum area of blob to be detected
* 30% of total image area

**delta**: maximum variation from one blob to the next
* current set at delta = 12 (needs to be adjusted)

### Horizon Detection
* uses Canny Edge Detection and Hough Line Transform to find the horizon in each image
* segments the image based on the horizon line
