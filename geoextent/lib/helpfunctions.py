import sys, os, platform, datetime, math, random
import getopt
import pandas as pd
from pandas.core.tools.datetimes import _guess_datetime_format_for_array as time_format
import numpy as np
from osgeo import ogr
from osgeo import osr
import logging
from pyproj import Proj, transform
import csv
PREFERRED_SAMPLE_SIZE = 30
WGS84_EPSG_ID = 4326
logger = logging.getLogger("geoextent")

def getAllRowElements(rowname, elements):
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
                return getAllRowElements(x, elements)


def transformingIntoWGS84(crs, coordinate):
    '''
    Function purpose: transforming SRS into WGS84 (EPSG:4978; used by the GPS satellite navigation system) \n
    Input: crs, point \n
    Output: retPoint constisting of x2, y2 (transformed points)
    '''
    # TODO: check whether current src is 4326
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
    # print("----<>", pointArray)#
    array = []
    # vector_rep
    if type(pointArray[0]) == list:
        for x in pointArray:
            array.append(transformingIntoWGS84(crs, x))
        return array
    # bbox
    elif len(pointArray) == 4:
        bbox = [[pointArray[0], pointArray[1]], [pointArray[2], pointArray[3]]]
        transf_bbox = transformingArrayIntoWGS84(crs, bbox)
        return [transf_bbox[0][0], transf_bbox[0][1], transf_bbox[1][0], transf_bbox[1][1]]


def validate(date_text):
    try:
        if datetime.datetime.strptime(date_text, '%Y-%m-%d'):
            return True
    except:
        return False


def getDelimiter(csv_file):
    dialect = csv.Sniffer().sniff(csv_file.readline(1024))
    # To reset back position to beginning of the file
    csv_file.seek(0)
    return csv.reader(csv_file.readlines(), delimiter=dialect.delimiter)


def get_time_format(time_list, num_sample):
    '''
    Function purpose: 'Guess' time format of a list of 'strings' by taking a representative sample
    time_list:  list of strings \n
    num_sample: size of the sample to determine time format \n
    Output: time format in string format (e.g '%Y.%M.d')
    '''

    if num_sample is None:
        num_sample = PREFERRED_SAMPLE_SIZE
        logger.error("num_sample not provided, num_sample modified to SAMPLE_SIZE {}".format(PREFERRED_SAMPLE_SIZE))
    elif(type(num_sample) is not int):
        raise Exception('num_sample parameter  must be an integer')
    elif(num_sample <= 0):
        raise Exception('num_sample parameter: {} must be greater than 0'.format(num_sample))

    if len(time_list) < num_sample:
        time_sample = time_list
        logger.error("num_sample is greater than the length of the list. num_sample modified to length of list {}".format(len(time_list)))
    else:
        time_sample = random.sample(time_list, num_sample)

    format_list = []

    for i in range(0, len(time_sample)):
        format_list.append(time_format(np.array([time_sample[i]])))
    unique_formats = list(set(format_list))

    if unique_formats is not None:
        for tf in unique_formats:
            try:
                pd.to_datetime(time_sample, format=tf)
                date_time_format = tf
            except:
                pass
    else:
        return None

    return date_time_format


def date_parser(datetime_list, num_sample = None):
    '''
    Function purpose: transform list of strings into ISO8601 ('%Y-%m-%d')
    datetime_list: list of date-times (strings) \n
    Output: list of DatetimeIndex
    '''

    datetime_format = get_time_format(datetime_list, num_sample)

    if datetime_format is not None:
        parse_time = pd.to_datetime(datetime_list, format=datetime_format, errors='coerce')
    else:
        parse_time = None

    return parse_time
