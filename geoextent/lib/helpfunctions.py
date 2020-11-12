import sys, os, platform, datetime, math, random
import zipfile, re
from os.path import basename
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

    with zipfile.ZipFile(abs_path) as zipf:
        zipf.extractall(zip_folder_path)

def create_zip(folder):
    '''
    Function purpose: create a zip file
    Input: filepath
    Source: https://thispointer.com/python-how-to-create-a-zip-archive-from-multiple-files-or-directory/
    '''

    with zipfile.ZipFile(folder +'.zip', 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(folder):
            for filename in filenames:
                # create complete filepath of file in directory
                file_root = os.path.abspath(folderName)
                filePath = os.path.join(file_root, filename)
                zipObj.write(filePath)


def bbox_merge(metadata):
    boxes_extent = []
    for x, y in metadata.items():
        if isinstance(y, dict):
            try:
                bbox_extent = [y['bbox'], y['crs']]
                boxes_extent.append(bbox_extent)
            except:
                pass
    if len(boxes_extent) == 0:
        return None
    elif len(boxes_extent) > 0:

        multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
        des_srs = ogr.osr.SpatialReference()
        des_srs.ImportFromEPSG(WGS84_EPSG_ID)
        multipolygon.AssignSpatialReference(des_srs)

        for bbox in boxes_extent:

            try:

                box = ogr.Geometry(ogr.wkbLinearRing)
                box.AddPoint(bbox[0][0], bbox[0][1])
                box.AddPoint(bbox[0][2], bbox[0][1])
                box.AddPoint(bbox[0][2], bbox[0][3])
                box.AddPoint(bbox[0][0], bbox[0][3])
                box.AddPoint(bbox[0][0], bbox[0][1])

                if bbox[1] != "4326":
                    logger.warning("Transforming bbox CRS from EPSG [{}] to [{}] ".format(bbox[1], WGS84_EPSG_ID))
                    source = osr.SpatialReference()
                    source.ImportFromEPSG(int(bbox[1]))
                    transform = osr.CoordinateTransformation(source, des_srs)
                    box.Transform(transform)

                polygon = ogr.Geometry(ogr.wkbPolygon)
                polygon.AddGeometry(box)
                multipolygon.AddGeometry(polygon)

            except:

                continue

        if multipolygon.GetGeometryCount() > 0:
            env = multipolygon.GetEnvelope()
            metadata_merge = [env[0], env[2], env[1], env[3]]
        else:
            metadata_merge = None

    return metadata_merge

def tbox_merge(metadata):

    boxes = []
    time_ext = []
    for x, y in metadata.items():
        if isinstance(y, dict):
            try:
                boxes.append(y['tbox'][0])
                boxes.append(y['tbox'][1])
            except:
                pass

    if len(boxes) == 0:
        time_ext = None

    elif len(boxes) >= 1:
        logger.info("Boxes to compare {}".format(boxes))
        for i in range(0, len(boxes)):
            boxes[i] = datetime.datetime.strptime(boxes[i], '%Y-%m-%d')
        min_date = min(boxes).strftime('%Y-%m-%d')
        max_date = max(boxes).strftime('%Y-%m-%d')
        time_ext = [min_date, max_date]

    return time_ext



