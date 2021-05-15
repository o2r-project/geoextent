import csv
import datetime
import itertools
import logging
import os
import random
import re
import zipfile
import numpy as np
import pandas as pd
from osgeo import ogr
from osgeo import osr
from pandas.core.tools.datetimes import _guess_datetime_format_for_array as time_format
from pathlib import Path

output_time_format = '%Y-%m-%d'
PREFERRED_SAMPLE_SIZE = 30
WGS84_EPSG_ID = 4326
logger = logging.getLogger("geoextent")

https_regexp = re.compile('https://(.*)')

# doi_regexp, is_doi, and normalize_doi are from idutils (https://github.com/inveniosoftware/idutils)
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2018 Alan Rubin.
# Licensed under BSD-3-Clause license
doi_regexp = re.compile(
    r"(doi:\s*|(?:https?://)?(?:dx\.)?doi\.org/)?(10\.\d+(.\d+)*/.+)$", flags=re.I)

zenodo_regexp = re.compile(
    r"(https://zenodo.org/record/)?(.\d*)$", flags=re.I
)


def getAllRowElements(row_name, elements, exp_data=None):
    """
    Function purpose: help-function to get all row elements for a specific string \n
    Input: row name, elements, exp_format \n
    Output: array values
    """
    values = []
    for idx, val in enumerate(elements[0]):
        if row_name in val:
            indexOf = idx
            for x in elements:
                try:
                    if x[indexOf] != row_name:
                        values.append(x[indexOf].replace(" ", ""))
                except IndexError as e:
                    logger.info("Row skipped,file might be corrupted. Error {}".format(e))
                    pass

    if exp_data == 'time':
        if get_time_format(values, 30) is not None:
            return values

    elif exp_data == 'numeric':
        try:
            values_num = list(map(float_convert, values))
            values_num_none = [i for i in values_num if i]
            if len(values_num_none) == 0:
                return None
            else:
                return values_num_none
        except Exception as e:
            logger.debug(e)
            return None
    else:
        return values


def float_convert(val):
    try:
        return float(val)
    except ValueError:
        pass


def searchForParameters(elements, param_array, exp_data=None):
    """
    Function purpose: return all attributes of a elements in the first row of a file \n
    Function purpose: return all attributes of a elements in the first row of a file \n
    Input: paramArray, elements \n
    Output: getAllRowElements(x,elements)
    """
    matching_elements = []
    for x in param_array:
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
    """
    Function purpose: transforming SRS into WGS84 (EPSG:4326) \n
    Input: crs, point \n
    Output: retPoint constisting of x2, y2 (transformed points)
    """
    # TODO: check whether current src is 4326
    source = osr.SpatialReference()
    source.ImportFromEPSG(int(crs))

    target = osr.SpatialReference()
    target.ImportFromEPSG(WGS84_EPSG_ID)

    transform = osr.CoordinateTransformation(source, target)

    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(float(coordinate[0]), float(coordinate[1]))
    point = point.ExportToWkt()
    point = ogr.CreateGeometryFromWkt(point)

    point.Transform(transform)

    return [point.GetX(), point.GetY()]


def transformingArrayIntoWGS84(crs, pointArray):
    """
    Function purpose: transforming SRS into WGS84 (EPSG 4326) from an array
    Input: crs, pointArray \n
    Output: array array
    """
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


def validate_bbox_wgs84(bbox):
    """
    Function purpose: Validate if bbox is correct for WGS84
    bbox: bounding box (list)
    Output: True if bbox is correct for WGS84
    """
    valid = True
    lon_values = bbox[0:3:2]
    lat_values = bbox[1:4:2]

    if sum(list(map(lambda x: x < -90 or x > 90, lat_values))) + sum(
            list(map(lambda x: x < -180 or x > 180, lon_values))) > 0:
        valid = False

    return valid


def flip_bbox(bbox):
    """
    bbox: Bounding box (list)
    Output: bbox flipped (Latitude to longitude if possible)
    """
    # Flip values
    lon_values = bbox[1:4:2]
    lat_values = bbox[0:3:2]

    bbox_flip = [lon_values[0], lat_values[0], lon_values[1], lat_values[1]]
    if validate_bbox_wgs84(bbox_flip):
        logger.warning("Longitude and latitude values flipped")
        return bbox_flip
    else:
        raise Exception("Latitude and longitude values extracted do not seem to be correctly transformed. We tried "
                        "flipping latitude and longitude values but both bbox are incorrect")


def validate(date_text):
    try:
        if datetime.datetime.strptime(date_text, output_time_format):
            return True
    except:
        return False


def getDelimiter(csv_file):
    dialect = csv.Sniffer().sniff(csv_file.readline(1024))
    # To reset back position to beginning of the file
    csv_file.seek(0)
    return csv.reader(csv_file.readlines(), delimiter=dialect.delimiter)


def get_time_format(time_list, num_sample):
    """
    Function purpose: 'Guess' time format of a list of 'strings' by taking a representative sample
    time_list:  list of strings \n
    num_sample: size of the sample to determine time format \n
    Output: time format in string format (e.g '%Y.%M.d')
    """

    date_time_format = None

    if num_sample is None:
        num_sample = PREFERRED_SAMPLE_SIZE
        logger.info("num_sample not provided, num_sample modified to SAMPLE_SIZE {}".format(PREFERRED_SAMPLE_SIZE))
    elif type(num_sample) is not int:
        raise Exception('num_sample parameter  must be an integer')
    elif num_sample <= 0:
        raise Exception('num_sample parameter: {} must be greater than 0'.format(num_sample))

    if len(time_list) < num_sample:
        time_sample = time_list
        logger.info(
            "num_sample is greater than the length of the list. num_sample modified to length of list {}".format(
                len(time_list)))
    else:
        # Selects first and last element
        time_sample = [[time_list[1], time_list[-1]], random.sample(time_list[1:-1], num_sample - 2)]
        # Selects num_sample-2 elements
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
    """
    Function purpose: transform list of strings into date-time format
    datetime_list: list of date-times (strings) \n
    Output: list of DatetimeIndex
    """

    datetime_format = get_time_format(datetime_list, num_sample)

    if datetime_format is not None:
        parse_time_input_format = pd.to_datetime(datetime_list, format=datetime_format, errors='coerce')
        parse_time = pd.to_datetime(parse_time_input_format, format=output_time_format, errors='coerce')
    else:
        parse_time = None

    return parse_time


def extract_zip(filepath):
    """
    Function purpose: unzip file (always inside a new folder)
    filepath: filepath to zipfile
    """

    abs_path = os.path.abspath(filepath)
    root_folder = os.path.split(abs_path)[0]
    zip_name = os.path.split(abs_path)[1][:-4]
    zip_folder_path = os.path.join(root_folder, zip_name)

    with zipfile.ZipFile(abs_path) as zip_file:
        zip_file.extractall(zip_folder_path)


def bbox_merge(metadata, origin):
    """
    Function purpose: merge bounding boxes
    metadata: metadata with geoextent extraction from multiple files (dict)
    origin: folder path or filepath (str)
    Output: Merged bbox (dict)
    """
    logger.debug("metadata {}".format(metadata))
    boxes_extent = []
    metadata_merge = {}
    num_files = len(metadata.items())
    for x, y in metadata.items():
        if isinstance(y, dict):
            try:
                bbox_extent = [y['bbox'], y['crs']]
                boxes_extent.append(bbox_extent)
            except:
                logger.debug("{} does not have identifiable geographical extent (CRS+bbox)".format(x))
                pass
    if len(boxes_extent) == 0:
        logger.debug(
            " ** {} does not have geometries with identifiable geographical extent (CRS+bbox)".format(origin))
        return None
    elif len(boxes_extent) > 0:

        multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
        des_crs = ogr.osr.SpatialReference()
        des_crs.ImportFromEPSG(WGS84_EPSG_ID)
        multipolygon.AssignSpatialReference(des_crs)

        for bbox in boxes_extent:

            try:
                box = ogr.Geometry(ogr.wkbLinearRing)
                box.AddPoint(bbox[0][0], bbox[0][1])
                box.AddPoint(bbox[0][2], bbox[0][1])
                box.AddPoint(bbox[0][2], bbox[0][3])
                box.AddPoint(bbox[0][0], bbox[0][3])
                box.AddPoint(bbox[0][0], bbox[0][1])

                if bbox[1] != str(WGS84_EPSG_ID):
                    source = osr.SpatialReference()
                    source.ImportFromEPSG(int(bbox[1]))
                    transform = osr.CoordinateTransformation(source, des_crs)
                    box.Transform(transform)

                polygon = ogr.Geometry(ogr.wkbPolygon)
                polygon.AddGeometry(box)
                multipolygon.AddGeometry(polygon)

            except Exception as e:
                logger.debug(
                    "Error extracting geographic extent. CRS {} may be invalid. Error: {}".format(int(bbox[1]), e))
                continue

        num_geo_files = multipolygon.GetGeometryCount() / 4
        if num_geo_files > 0:
            logger.debug('{} contains {} geometries out of {} with identifiable geographic extent'.format(origin, int(
                num_geo_files), num_files))
            env = multipolygon.GetEnvelope()
            metadata_merge['bbox'] = [env[0], env[2], env[1], env[3]]
            metadata_merge['crs'] = str(WGS84_EPSG_ID)
        else:
            logger.debug(" {} does not have geometries with identifiable geographical extent (CRS+bbox)".format(origin))
            metadata_merge = None

    return metadata_merge


def tbox_merge(metadata, path):
    """
    Function purpose: Merge time boxes
    metadata: metadata with geoextent extraction from multiple files (dict)
    path: path of directory being merged
    Output: Merged tbox
    """
    boxes = []
    num_files = len(metadata.items())
    for x, y in metadata.items():
        if isinstance(y, dict):
            try:
                boxes.append(y['tbox'][0])
                boxes.append(y['tbox'][1])
            except:
                pass

    num_time_files = len(boxes)
    if num_time_files == 0:
        logger.debug(" ** Directory {} does not have files with identifiable temporal extent".format(path))
        return None

    else:
        for i in range(0, len(boxes)):
            boxes[i] = datetime.datetime.strptime(boxes[i], output_time_format)
        min_date = min(boxes).strftime(output_time_format)
        max_date = max(boxes).strftime(output_time_format)
        logger.debug("Folder {} contains {} files out of {} with identifiable temporal extent".format(path, int(
            num_time_files), num_files))
        time_ext = [min_date, max_date]

    return time_ext


def transform_bbox(x):
    """
    Function purpose: Transform bounding box (str) into geometry
    x: bounding box (str)
    """

    try:
        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint(x[0], x[1])
        ring.AddPoint(x[2], x[1])
        ring.AddPoint(x[2], x[3])
        ring.AddPoint(x[0], x[3])
        ring.CloseRings()
    # Create polygon
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)
        poly.FlattenTo2D()
        bbox = poly.ExportToWkt()

    except:

        bbox = None

    return bbox


def transform_tbox(x):
    """
    Function purpose: Transform time box (list) into int
    x: time box (list)
    """

    if x is None:
        return None
    elif isinstance(x, list):
        return str(x[0]) + '/' + str(x[1])


def extract_details(details):
    """
    Function purpose: Extracts details from geoextent extraction
    details: dictionary with geoextent extraction
    Output: dataframe organized by filename, file format, handler, bbox, tbox and crs by file.
    """

    filename = []
    file_format = []
    handler = []
    bbox = []
    tbox = []
    crs = []

    for i in details:

        file = details[i]

        if file is None:
            filename.append([i])
            file_format_v = os.path.splitext(i)[1][1:]
            if file_format_v == '':
                file_format_v = 'undetected'
            file_format.append([file_format_v])
            handler.append([None])
            bbox.append([None])
            tbox.append([None])
            crs.append([None])
        else:
            filename.append([i])
            file_format.append([file.get('format')])
            handler_v = file.get('geoextent_handler')
            bbox_v = file.get('bbox')
            tbox_v = file.get('tbox')
            crs_v = file.get('crs')
            handler.append([handler_v])
            bbox.append([bbox_v])
            tbox.append([tbox_v])
            crs.append([crs_v])

            if file.get('format') == 'folder':
                details_folder = extract_details(file['details'])
                filename.append(details_folder['filename'])
                file_format.append(details_folder['format'])
                handler.append(details_folder['handler'])
                bbox.append(details_folder['bbox'])
                tbox.append(details_folder['tbox'])
                crs.append(details_folder['crs'])

    if any(isinstance(i, list) for i in filename):
        filename = list(itertools.chain.from_iterable(filename))
        file_format = list(itertools.chain.from_iterable(file_format))
        handler = list(itertools.chain.from_iterable(handler))
        bbox = list(itertools.chain.from_iterable(bbox))
        tbox = list(itertools.chain.from_iterable(tbox))
        crs = list(itertools.chain.from_iterable(crs))

    d = {'filename': filename, 'format': file_format,   'handler': handler,
         'bbox': bbox,
         'tbox': tbox, 'crs': crs}
    files = pd.DataFrame(d)
    return files


def extract_output(result, files, current_version):
    """
    Function purpose: Extracts final output from geoextent including all files and containing folder
    result: geoextent output from extraction
    files: user input for initial extraction (e.g name of the main folder)
    current_version: Current geoextent version
    Output: Dataframe with geoextent of all files AND final output (merge) of user request
    """
    filename = files
    file_format = result.get('format')
    handler = "geoextent:" + current_version
    bbox = result.get('bbox')
    tbox = result.get('tbox')
    crs = result.get('crs')

    new_row = {'filename': filename, 'format': file_format,   'handler': handler, 'bbox': bbox, 'tbox': tbox, 'crs': crs
               }

    df = extract_details(result['details'])
    df = df.append(new_row, ignore_index=True)
    df['bbox'] = df['bbox'].apply(transform_bbox)
    df['tbox'] = df['tbox'].apply(transform_tbox)
    return df


def is_doi(val):
    """
    Function purpose: Returns None if val doesn't match pattern of a DOI.
    http://en.wikipedia.org/wiki/Digital_object_identifier.
    """
    return doi_regexp.match(val)


def normalize_doi(val):
    """
    Function purpose: Return just the DOI (e.g. 10.1234/jshd123)
    from a val that could include a url or doi
    (e.g. https://doi.org/10.1234/jshd123)
    val: DOI or URL (str)
    """
    m = doi_regexp.match(val)
    return m.group(2)


def create_geopackage(df, filename):
    """
    Function purpose: Creates a geopackage file
    df: dataframe from extract_output result
    filename: Name for the Geopackage file
    """
    sr4326 = osr.SpatialReference()
    sr4326.ImportFromEPSG(WGS84_EPSG_ID)

    if os.path.exists(filename):
        os.remove(filename)
        logger.warning("Overwriting {} ".format(filename))

    ds = ogr.GetDriverByName('GPKG').CreateDataSource(filename)
    lyr = ds.CreateLayer('files', geom_type=ogr.wkbPolygon, srs=sr4326)
    lyr.CreateField(ogr.FieldDefn('filename', ogr.OFTString))
    lyr.CreateField(ogr.FieldDefn('handler', ogr.OFTString))
    lyr.CreateField(ogr.FieldDefn('format', ogr.OFTString))
    lyr.CreateField(ogr.FieldDefn('tbox', ogr.OFTString))
    lyr.CreateField(ogr.FieldDefn('crs', ogr.OFTString))

    for i in range(len(df)):
        feat = ogr.Feature(lyr.GetLayerDefn())
        feat['filename'] = df.loc[i, "filename"]
        feat['format'] = df.loc[i, "format"]
        feat['tbox'] = df.loc[i, "tbox"]
        feat['handler'] = df.loc[i, "handler"]
        feat['crs'] = df.loc[i, "crs"]
        if df.loc[i, "bbox"] is not None:
            feat.SetGeometry(ogr.CreateGeometryFromWkt(df.loc[i, "bbox"]))
        lyr.CreateFeature(feat)

    ds = None


def path_output(path):

    if os.path.isdir(path):
        logger.error("Output must be a file, not a directory ")
        raise ValueError("Output must be a file, not a directory: {}".format(path))

    folder_path = os.path.split(path)[0]
    user_path = Path(folder_path)
    if user_path.exists():
        absolute_file_path = user_path.as_posix() + "/" + os.path.split(path)[1]
    else:
        logger.error("Output target directory does not exist: {}".format(path))
        raise ValueError("Output target directory does not exist: {}".format(path))
    return absolute_file_path


