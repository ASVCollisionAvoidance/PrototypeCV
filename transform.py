# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 11:14:17 2019

@author: ryley
"""

#   Function that performs the same operation as cv.warpPerspective
#   Takes an array instead of an img
#   Used to transform individual points to the inverse perspective space

def transform(points, matrix):

    transformed_points = [round((matrix[0,0]*points[0]+matrix[0,1]*points[1]+matrix[0,2])/
                                (matrix[2,0]*points[0]+matrix[2,1]*points[1]+matrix[2,2])),
                                round((matrix[1,0]*points[0]+matrix[1,1]*points[1]+matrix[1,2])/
                                (matrix[2,0]*points[0]+matrix[2,1]*points[1]+matrix[2,2]))]
    
    return transformed_points