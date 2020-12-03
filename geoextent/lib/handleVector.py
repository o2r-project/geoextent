import logging
from osgeo import ogr
from osgeo import gdal
from osgeo import osr

fileType = "application/shp"

logger = logging.getLogger("geoextent")

def checkFileValidity(filepath):
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

    return None

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
