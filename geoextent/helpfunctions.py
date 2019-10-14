
import sys, os, platform, datetime, math, shapefile, fiona 

import getopt
from osgeo import ogr
from osgeo import osr
from pyproj import Proj, transform

WGS84_EPSG_ID = 4326

def printObject(object):
    '''
    Function purpose: output of metadata object \n
    Input: object \n
    Output: print("/n")
    '''
    print("\n")
    for a,b in object.items():
        print(str(a) + ": " + str(b))
    print("\n")




def transformingIntoWGS84 (crs, coordinate):
    '''
    Function purpose: transforming SRS into WGS84 (EPSG:4978; used by the GPS satellite navigation system) \n
    Input: crs, point \n
    Output: retPoint constisting of x2, y2 (transformed points)
    '''
    #TODO: check whether current src is 4326
    source = osr.SpatialReference()
    source.ImportFromEPSG(int(crs))

    target = osr.SpatialReference()
    target.ImportFromEPSG(4326)

    transform = osr.CoordinateTransformation(source, target)
        
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(float(coordinate[0]), float(coordinate[1]))
    point = point.ExportToWkt()
    point = ogr.CreateGeometryFromWkt(point)
  
    point.Transform(transform)
    return [point.GetX(), point.GetY()]





def transformingArrayIntoWGS84(crs, pointArray):
    '''
    Function purpose: transforming SRS into WGS84 (EPSG:4978; used by the GPS satellite navigation system) from an array \n
    Input: crs, pointArray \n
    Output: array array
    '''
    #print("----<>", pointArray)#
    array = []
    #vector_rep
    if type(pointArray[0]) == list:
        for x in pointArray:
            array.append(transformingIntoWGS84(crs, x))
        return array
    #bbox
    elif len(pointArray) == 4:
        bbox = [[pointArray[0], pointArray[1]],[pointArray[2], pointArray[3]]]
        transf_bbox = transformingArrayIntoWGS84(crs, bbox)
        return [transf_bbox[0][0],transf_bbox[0][1], transf_bbox[1][0], transf_bbox[1][1]]