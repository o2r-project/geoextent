import logging
from osgeo import ogr
from osgeo import gdal
from . import helpfunctions as hf
import re
from osgeo import osr

fileType = "application/shp"
search = { "time":["(.)*timestamp(.)*", "(.)*datetime(.)*", "(.)*time(.)*", "date$","^date"]}
logger = logging.getLogger("geoextent")

def get_handler_name():
    return "handleVector"

def checkFileSupported(filepath):
    '''Checks whether it is valid vector file or not. \n
    input "path": type string, path to file which shall be extracted \n
    '''

    logger.debug(filepath)
    try:
        file = gdal.OpenEx(filepath)
        driver = file.GetDriver().ShortName
    except:
        logger.debug("File {} is NOT supported by HandleVector module".format(filepath))
        return False
    logger.debug("Layer count: {} ".format(file.GetLayerCount()))
    if file.GetLayerCount() > 0:
        if driver != "CSV":
            logger.debug("File {} is supported by HandleVector module".format(filepath))
            return True
    else:
        logger.debug("File {} is NOT supported by HandleVector module".format(filepath))
        return False

def getCRS(filepath):

    dataset = ogr.Open(filepath)
    layer = dataset.GetLayer()

    try:
        spatialRef = layer.GetSpatialRef().GetAttrValue("GEOGCS|AUTHORITY", 1)
    except:
        logger.debug("File {} does not have a coordinate reference system !".format(filepath))
        spatialRef = None

    return spatialRef


def getTemporalExtent(filepath):
    ''' extracts temporal extent of the vector file \n
    input "path": type string, file path to vector file
    '''

    global parsed_time
    dataset = ogr.Open(filepath)
    layer = dataset.GetLayer()
    layerDefinition = layer.GetLayerDefn()

    field_names = []
    for i in range(layerDefinition.GetFieldCount()):
        field_names.append(layerDefinition.GetFieldDefn(i).GetName())

    match_list = []
    for x in search["time"]:
        for j in field_names:
            term = re.compile(x, re.IGNORECASE)
            match = term.search(j)
            if match is not None:
                match_list.append(j)

    if len(match_list) == 0:
        logger.debug('The file {} has no TemporalExtent'.format(filepath))
        return None
    else:
        timelist = []
        for time_feature in match_list:
            for feat in layer:
                time = feat.GetField(time_feature)
                if time is not None:
                    timelist.append(time)

    if len(timelist) == 0:
        logger.debug('The file {} has no TemporalExtent'.format(filepath))
        return None
    else:
        parsed_time = hf.date_parser(timelist)

    if parsed_time is None:
        logger.debug('The file {} has no recognizable TemporalExtent'.format(filepath))
        return None
    else:
        tbox = [min(parsed_time).strftime('%Y-%m-%d'), max(parsed_time).strftime('%Y-%m-%d')]

    return tbox

def getBoundingBox(filepath):
    ''' extracts bounding box from vector file \n
    input "path": type string, file path to vector \n
    returns bounding box of the file: type list, length = 4
    '''
    dataset = ogr.Open(filepath)
    layer = dataset.GetLayer()
    try:
        ext = layer.GetExtent()
        bbox_list= [ext[0],ext[2],ext[1],ext[3]]
    except:
        logger.debug("File {} does not have features".format(filepath))
        bbox_list = None

    return bbox_list
