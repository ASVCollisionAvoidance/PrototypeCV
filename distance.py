
def findDistances(averageXY, pitch):
    stableRatioX = 1 # (TODO: change to actual number) ratio of pixels:cm (pixels/cm) in horizontal direction
    stableRatioY = 1 # (TODO: change to actual number) ratio of pixels:cm (pixels/cm) in vertical direction

    angleRatio = 1 # (TODO: change to actual number) ratio of pixels/cm/degree for pitch angle

    #finalRatioX = 1
    finalRatioY = angleRatio * pitch + stableRatioY

    distanceList = [(x[0]/stableRatioX, x[1]/stableRatioY) for x in averageXY]

    return distanceList
