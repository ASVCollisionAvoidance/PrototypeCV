
def findDistances(averageXY, pitch):
    """
    Converts a list of pixel coordinates to a list of distances,
    based on known conversion factors.

    Parameters
    ----------
    averageXY: list
        a list of (x, y) tuples that represent the average coordinates
        of each detected object

    pitch: int
        pitch angle of the surfboard - a parameter that will influence
        the perceived distance of objects

    Returns
    -------
    distanceList: list
        a list of (x, y) tuples that represent the average
        distances in cm of each detected object
    """
    stableRatioX = 1060/46 # (TODO: change to actual number) ratio of pixels:cm (pixels/cm) in horizontal direction
    x = 46 #cm

    stableRatioY = 1680/87 # (TODO: change to actual number) ratio of pixels:cm (pixels/cm) in vertical direction
    y = 87 #cm


    angleRatio = 1 # (TODO: change to actual number) ratio of pixels/cm/degree for pitch angle

    #finalRatioX = 1
    finalRatioY = angleRatio * pitch + stableRatioY

    distanceList = [(x[0]/stableRatioX, x[1]/stableRatioY) for x in averageXY]

    return distanceList
