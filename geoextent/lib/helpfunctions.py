import sys, os, platform, datetime, math
import getopt
from parser import ParserError
import pandas as pd
from pandas.core.tools.datetimes import _guess_datetime_format_for_array as time_format
import numpy as np
import dateutil
from osgeo import ogr
from osgeo import osr
from pyproj import Proj, transform
import csv
import dateutil.parser

WGS84_EPSG_ID = 4326

def getAllRowElements(rowname,elements):
    '''
    Function purpose: help-function to get all row elements for a specific string \n
    Input: rowname, elements \n
    Output: array values
    '''
    for idx, val in enumerate(elements[0]):
        if rowname in val.lower():
            indexOf = idx
            values = []
            for x in elements:
                if x[indexOf].lower() != rowname:
                    values.append(x[indexOf])
            return values


def searchForParameters(elements, paramArray):
    '''
    Function purpose: return all attributes of a elements in the first row of a file \n
    Input: paramArray, elements \n
    Output: getAllRowElements(x,elements)
    '''
    for x in paramArray:
        for row in elements[0]:
            if x in row.lower():
                return getAllRowElements(x,elements)

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


def validate(date_text):
    try:
        if datetime.datetime.strptime(date_text, '%Y-%m-%d'):
            return True
    except :
        return False


def getDelimiter(csv_file):
    dialect = csv.Sniffer().sniff(csv_file.readline(1024))
    # To reset back position to beginning of the file
    csv_file.seek(0)
    return csv.reader(csv_file.readlines(), delimiter=dialect.delimiter)

def date_parser_iso8601(list):
    '''
    Function purpose: help-function to transform tbox from extracted time format into ISO8601
    Input: list (tbox) \n
    Output: array values
    '''

    time_1, time_2 = None, None
    time_form = [time_format(np.array([list[0]])), time_format(np.array([list[1]]))]

    if time_form[0] == time_form[1]:
        time_1 = pd.to_datetime(list[0], format=time_form[0])
        time_2 = pd.to_datetime(list[1], format=time_form[0])

    else:
        for i in time_form:
            try:
                time_1 = pd.to_datetime(list[0], format=i)
                time_2 = pd.to_datetime(list[1], format=i)
            except:
                pass

    if time_1 is not None and time_2 is not None:
        time_1 = time_1.strftime('%Y-%m-%d')
        time_2 = time_2.strftime('%Y-%m-%d')

    bbox_iso8601 = [time_1, time_2]

    return bbox_iso8601
