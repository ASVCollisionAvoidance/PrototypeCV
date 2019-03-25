
def findDistances(averageY):
    stableRatio = 1 # (TODO: change to actual number) ratio of pixels:cm (pixels/cm)

    distanceList = [x/stableRatio for x in averageY]

    return distanceList
