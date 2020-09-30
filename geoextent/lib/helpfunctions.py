import sys, os, platform, datetime, math, random
import zipfile, re

import getopt
import pandas as pd
import re
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


def getAllRowElements(rowname, elements, exp_data=None):
    '''
    Function purpose: help-function to get all row elements for a specific string \n
    Input: rowname, elements, exp_format \n
    Output: array values
    '''

    for idx, val in enumerate(elements[0]):
        if rowname in val:
            indexOf = idx
            values = []
            for x in elements:
                if x[indexOf] != rowname:
                    values.append(x[indexOf].replace(" ", ""))

    if exp_data == 'time':
        if get_time_format(values, 30) is not None:
            return values

    elif exp_data == 'numeric':
        try:
            list(map(float, values))
            return values
        except:
            return None

    else:
        return values


def searchForParameters(elements, paramArray, exp_data=None):
    '''
    Function purpose: return all attributes of a elements in the first row of a file \n
    Function purpose: return all attributes of a elements in the first row of a file \n
    Input: paramArray, elements \n
    Output: getAllRowElements(x,elements)
    '''

    matching_elements = []
    for x in paramArray:
        for row in elements[0]:
            p = re.compile(x, re.IGNORECASE)
            if p.search(row) is not None:
                row_to_extract = getAllRowElements(row, elements, exp_data)
                if row_to_extract is not None:
                    matching_elements.append(row_to_extract)

    matching_elements = sum(matching_elements, [])
    if len(matching_elements) == 0:
        return None

    return matching_elements

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

    date_time_format = None

    if num_sample is None:
        num_sample = PREFERRED_SAMPLE_SIZE
        logger.info("num_sample not provided, num_sample modified to SAMPLE_SIZE {}".format(PREFERRED_SAMPLE_SIZE))
    elif (type(num_sample) is not int):
        raise Exception('num_sample parameter  must be an integer')
    elif (num_sample <= 0):
        raise Exception('num_sample parameter: {} must be greater than 0'.format(num_sample))

    if len(time_list) < num_sample:
        time_sample = time_list
        logger.info(
            "num_sample is greater than the length of the list. num_sample modified to length of list {}".format(
                len(time_list)))
    else:
        # Selects first and last element
        time_sample = [[time_list[1], time_list[-1]]]
        # Selects num_sample-2 elements
        time_sample.append(random.sample(time_list[1:-1], num_sample - 2))
        time_sample = sum(time_sample, [])

    format_list = []

    for i in range(0, len(time_sample)):
        format_list.append(time_format(np.array([time_sample[i]])))
    unique_formats = list(set(format_list))

    logger.info("UNIQUE_FORMATS {}".format(unique_formats))
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


def date_parser(datetime_list, num_sample=None):
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

def extract_zip(zippedFile):
    '''
    Function purpose: unzip file (always inside a new folder)
    Input: filepath
    '''

    abs_path = os.path.abspath(zippedFile)
    root_folder = os.path.split(abs_path)[0]
    zip_name = os.path.split(abs_path)[1][:-4]
    zip_folder_path = os.path.join(root_folder, zip_name)

    #print("****************")
    #print("Abs: ", abs_path)
    #print("root_folder: ", root_folder)
    #print("zip_name: ", zip_name)
    #print("zip_folder_path: ", zip_folder_path)
    #print("****************")

    with zipfile.ZipFile(abs_path) as zipf:
        zipf.extractall(zip_folder_path)
    #os.remove(abs_path)

    for root, dirs, files in os.walk(zip_folder_path):
        for filename in files:
            if re.search(r'\.zip$', filename):
                #print("*root:", root)
                #print("*filename:", filename)
                abs_path_file = os.path.join(root, filename)
                #print("*abs_path_file:", abs_path_file)
                extract_zip(abs_path_file)


def bbox_merge(metadata):
    boxes = []
    spatial_extent = {}
    for x, y in metadata.items():
        if isinstance(y, dict):
            try:
                boxes.append(y['bbox'])
            except:
                print('An exception flew by!')

    if len(boxes) == 0:
        spatial_extent = None
        metadata = None
    elif len(boxes) > 0:
        multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
        des_srs = ogr.osr.SpatialReference()
        des_srs.ImportFromEPSG(4326)
        multipolygon.AssignSpatialReference(des_srs)

        for bbox in boxes:
            box = ogr.Geometry(ogr.wkbLinearRing)
            box.AddPoint(bbox[0], bbox[1])
            box.AddPoint(bbox[2], bbox[1])
            box.AddPoint(bbox[2], bbox[3])
            box.AddPoint(bbox[0], bbox[3])
            box.AddPoint(bbox[0], bbox[1])

            polygon = ogr.Geometry(ogr.wkbPolygon)
            polygon.AddGeometry(box)

            multipolygon.AddGeometry(polygon)

        env = multipolygon.GetEnvelope()
        spatial_extent = [env[0], env[2], env[1], env[3]]
        metadata = spatial_extent

    return metadata

def tbox_merge(metadata):
    boxes = []
    for x, y in metadata.items():
        if isinstance(y, dict):
            try:
                boxes.append(datetime.strptime(y['tbox'][0], '%d.%m.%Y'))
                boxes.append(datetime.strptime(y['tbox'][1], '%d.%m.%Y'))
            except:
                print('An exception flew by!')
    if len(boxes) == 0:
        time_ext = None

    elif len(boxes) >= 1:
        min_date = min(boxes).strftime('%d.%m.%Y')
        max_date = max(boxes).strftime('%d.%m.%Y')
        time_ext = [min_date, max_date]

    return time_ext

