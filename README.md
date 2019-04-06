# Computer Vision Algorithm for ASV Project
### Authors:
Paula Cameron, Amber Donnelly, Ryley Simpson


### Project Description:
This project was completed as part of the ENPH 459: Engineering Physics Project I course. It was sponsored by Adrien Emery, an Engineering Physics alum.

This repository contains a computer vision algorithm for the collision avoidance system of an autonomous surface vehicle.


### Main Steps:
1. GoPro control
  - take picture
  - download picture from GoPro
2. Detect and remove pixels above horizon
3. Remove pixels below tip of surfboard
4. Use MSER (maximally stable extremal regions) feature detection algorithm to detect regions on interest.
5. Use k-means clustering to classify detected regions as obstacles or false positives.
6. Calculate distances from each detected obstacle.
7. Output a distance for each object as a list of four points which create a bounding box around the object.
