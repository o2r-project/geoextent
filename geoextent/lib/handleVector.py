import logging
from osgeo import ogr
from osgeo import gdal
from . import helpfunctions as hf
import re
from osgeo import osr

null_island = [0] * 4
fileType = "application/shp"
search = {"time": ["(.)*timestamp(.)*", "(.)*datetime(.)*", "(.)*time(.)*", "date$", "^date","^begin"]}
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

    datasource = ogr.Open(filepath)
    layer_count = datasource.GetLayerCount()
    logger.debug("{} contains {} layers".format(filepath,layer_count))
    datetime_list = []
    for layer in datasource:

        logger.debug("{} : Extracting temporal extent from layer {} ".format(filepath, layer))
        layerDefinition = layer.GetLayerDefn()
        field_names = []
        for i in range(layerDefinition.GetFieldCount()):
            field_names.append(layerDefinition.GetFieldDefn(i).GetName())

        match_list = []
        for x in search["time"]:
            term = re.compile(x, re.IGNORECASE)
            for j in field_names:
                match = term.search(j)
                if match is not None:
                    match_list.append(j)
        logger.debug(match_list)

        if len(match_list) == 0:
            logger.debug("File:{} /Layer: {}: No matched fields for temporal extent".format(filepath,layer))
            pass
        else:
            datetime_list = []
            for time_feature in match_list:
                time_list = []
                logger.debug(time_feature)
                for feat in layer:
                    time = feat.GetField(time_feature)
                    if time is not None:
                        time_list.append(time)
                layer.ResetReading()

                if len(time_list) != 0:
                    parsed_time = hf.date_parser(time_list)
                    if parsed_time is not None:
                        datetime_list.extend(parsed_time)
                    else:
                        logger.debug('File:{} /Layer: {}: : Matched temporal extent "{}" field do not have recognizable time format'.format(filepath,layer,time_feature))
                        pass
                else:
                    logger.debug("File:{} / Layer: {}: No values found in {} fields.".format(filepath,layer, time_feature))
                    pass

        logger.debug(match_list)
    if len(datetime_list) == 0:
        logger.debug("File {} do not have recognizable temporal extent".format(filepath))
        return None
    else:
        tbox = [min(datetime_list).strftime(hf.output_time_format), max(datetime_list).strftime(hf.output_time_format)]

    return tbox


def getBoundingBox(filepath):
    """ extracts bounding box from vector file \n
    input "filepath": type string, file path to vector \n
    returns bounding box of the file: type list, length = 4
    """
    datasource = ogr.Open(filepath)
    geo_dict = {}
    for layer in datasource:
        layer_name = layer.GetDescription()
        ext = layer.GetExtent()
        bbox = [ext[0], ext[2], ext[1], ext[3]]

        try:
            crs = layer.GetSpatialRef().GetAttrValue("GEOGCS|AUTHORITY", 1)
        except Exception:
            crs = None

        geo_dict[layer_name] = {"bbox": bbox, "crs": crs}

        if bbox == null_island or crs is None:
            del geo_dict[layer_name]["crs"]
        logger.debug(geo_dict)

    bbox_merge = hf.bbox_merge(geo_dict, filepath)

    return bbox_merge
