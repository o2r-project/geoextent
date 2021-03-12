import csv
import logging
from osgeo import gdal
from . import helpfunctions as hf

logger = logging.getLogger("geoextent")

search = {"longitude": ["(.)*longitude", "(.)*long(.)*", "^lon", "lon$", "(.)*lng(.)*", "^x", "x$"],
          "latitude": ["(.)*latitude(.)*", "^lat", "lat$", "^y", "y$"],
          "time": ["(.)*timestamp(.)*", "(.)*datetime(.)*", "(.)*time(.)*", "date$", "^date"]}


def get_handler_name():
    return "handleCSV"


def checkFileSupported(filepath):
    '''Checks whether it is valid CSV or not. \n
    input "path": type string, path to file which shall be extracted \n
    raise exception if not valid
    '''

    try:
        file = gdal.OpenEx(filepath)
        driver = file.GetDriver().ShortName
    except:
        logger.debug("File {} is NOT supported by HandleCSV module".format(filepath))
        return False

    if driver == "CSV":
        with open(filepath) as csv_file:
            data = csv.reader(csv_file.readlines())
            if data is None:
                logger.debug("File {} is NOT supported by HandleCSV module".format(filepath))
                return False
            else:
                logger.debug("File {} is supported by HandleCSV module".format(filepath))
                return True
    else:
        return False


def getBoundingBox(filePath):
    '''
    Function purpose: extracts the spatial extent (bounding box) from a csv-file \n
    input "filepath": type string, file path to csv file \n
    returns spatialExtent: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] 
    '''

    with open(filePath) as csv_file:
        # To get delimiter either comma or simecolon
        date = hf.getDelimiter(csv_file)

        elements = []
        for x in date:
            elements.append(x)

        spatial_lat_extent = hf.searchForParameters(elements, search['latitude'], exp_data='numeric')

        min_lat = None
        max_lat = None

        if spatial_lat_extent is None:
            pass
        else:
            min_lat = (min(spatial_lat_extent))
            max_lat = (max(spatial_lat_extent))

        spatial_lon_extent = hf.searchForParameters(elements, search['longitude'], exp_data='numeric')

        if spatial_lon_extent is None:
            raise Exception('The csv file from ' + filePath + ' has no BoundingBox')
        else:
            min_lon = (min(spatial_lon_extent))
            max_lon = (max(spatial_lon_extent))

        bbox = [min_lon, min_lat, max_lon, max_lat]
        logger.debug("Extracted Bounding box (without projection): {}".format(bbox))
        crs = getCRS(filePath)
        logger.debug("Extracted CRS: {}".format(crs))
        spatialExtent = {"bbox": bbox, "crs": crs}
        if not bbox or not crs:
            raise Exception("Bounding box could not be extracted")

    return spatialExtent


def getTemporalExtent(filepath, num_sample):
    """ extract time extent from csv string \n
    input "filePath": type string, file path to csv File \n
    returns temporal extent of the file: type list, length = 2, both entries have the type str, temporalExtent[0] <= temporalExtent[1]
    """

    with open(filepath) as csv_file:
        # To get delimiter either comma or semicolon
        data = hf.getDelimiter(csv_file)

        elements = []
        for x in data:
            elements.append(x)

        all_temporal_extent = hf.searchForParameters(elements, search['time'], exp_data="time")
        if all_temporal_extent is None:
            raise Exception('The csv file from ' + filepath + ' has no TemporalExtent')
        else:
            tbox = []
            parsed_time = hf.date_parser(all_temporal_extent, num_sample=num_sample)

            if parsed_time is not None:
                # Min and max into ISO8601 format ('%Y-%m-%d')
                tbox.append(min(parsed_time).strftime('%Y-%m-%d'))
                tbox.append(max(parsed_time).strftime('%Y-%m-%d'))
            else:
                raise Exception('The csv file from ' + filepath + ' has no recognizable TemporalExtent')
            return tbox


def getCRS(filepath):
    '''extracts coordinatesystem from csv File \n
    input "filepath": type string, file path to csv file \n
    returns the epsg code of the used coordinate reference system, type list, contains extracted coordinate system of content from csv file
    '''

    with open(filepath) as csv_file:
        data = hf.getDelimiter(csv_file)
        elements = []
        for x in data:
            elements.append(x)

        param = hf.searchForParameters(elements, ["crs", "srsID", "EPSG"])

        if param is None:
            logger.debug("{} : There is no identifiable coordinate reference system. We will try to use EPSG: 4326".format(filepath))
            crs = "4326"

        elif len(list(set(param))) > 1:
            logger.debug("{} : Coordinate reference system of the file is ambiguous. Extraction is not possible.".format(filepath))
            raise Exception('The csv file from ' + filepath + ' has no CRS')
        else:
            crs = str(list(set(param))[0])

        return crs