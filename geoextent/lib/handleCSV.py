import csv
import logging
from osgeo import gdal
from . import helpfunctions as hf

fileType = "text/csv"

logger = logging.getLogger("geoextent")

search = { "longitude" : ["(.)*longitude","(.)*long(.)*", "^lon","lon$","(.)*lng(.)*", "^x","x$"],
                   "latitude" : ["(.)*latitude(.)*", "^lat","lat$", "^y","y$"],
           "time":["(.)*timestamp(.)*", "(.)*datetime(.)*", "(.)*time(.)*", "date$","^date"]}

def checkFileValidity(filepath):
    '''Checks whether it is valid CSV or not. \n
    input "path": type string, path to file which shall be extracted \n
    raise exception if not valid
    '''

    logger.info(filepath)
    try:
        file = gdal.OpenEx(filepath)
        driver = file.GetDriver().ShortName
    except:
        logger.debug("File {} is NOT supported by HandleCSV module".format(filepath))
        return False

    if driver == "CSV":
        with open(filepath) as csv_file:
            daten = csv.reader(csv_file.readlines())
            if daten is None:
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
        daten = hf.getDelimiter(csv_file)

        elements = []
        for x in daten:
            elements.append(x)
           
        spatialExtent= []
        spatialLatExtent=[]
        spatialLonExtent=[]

        spatialLatExtent= hf.searchForParameters(elements, search['latitude'], exp_data= 'numeric')

        minlat= None
        maxlat= None
        if spatialLatExtent is None:
            pass
        else:
            minlat= (min(spatialLatExtent))
            maxlat= (max(spatialLatExtent))

        spatialLonExtent= hf.searchForParameters(elements, search['longitude'], exp_data= 'numeric')

        if spatialLonExtent is None:
            raise Exception('The csv file from ' + filePath + ' has no BoundingBox')
        else:
            minlon= (min(spatialLonExtent))
            maxlon= (max(spatialLonExtent))

        spatialExtent= [minlon,minlat,maxlon,maxlat]
        if not spatialExtent:
            raise Exception("Bounding box could not be extracted")
        return spatialExtent

def getTemporalExtent(filePath, num_sample):
    ''' extract time extent from csv string \n
    input "filePath": type string, file path to csv File \n
    returns temporal extent of the file: type list, length = 2, both entries have the type str, temporalExtent[0] <= temporalExtent[1]
    '''


    with open(filePath) as csv_file:
        # To get delimiter either comma or simecolon
        daten = hf.getDelimiter(csv_file)

        elements = []
        for x in daten:
            elements.append(x)
        logger.info("Elements {}".format(elements))

        all_temporal_extent = hf.searchForParameters(elements, search['time'], exp_data = "time" )
        if all_temporal_extent is None:
            raise Exception('The csv file from ' + filePath + ' has no TemporalExtent')
        else:
            tbox = []
            parsed_time = hf.date_parser(all_temporal_extent, num_sample = num_sample)

            if parsed_time is not None:
                # Min and max into ISO8601 format ('%Y-%m-%d')
                tbox.append(min(parsed_time).strftime('%Y-%m-%d'))
                tbox.append(max(parsed_time).strftime('%Y-%m-%d'))
            else:
                raise Exception('The csv file from ' + filePath + ' has no recognizable TemporalExtent')
            return tbox

def getCRS(filePath):
    '''extracts coordinatesystem from csv File \n
    input "filepath": type string, file path to csv file \n
    returns the epsg code of the used coordinate reference system, type list, contains extracted coordinate system of content from csv file
    ''' 
    with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        elements = []
        for x in daten:
            elements.append(x)
        if hf.searchForParameters(elements,search['latitude']+search['longitude']) is None:
            if hf.searchForParameters(elements, ["crs","srsID"]) is None:
                raise Exception('The csv file from ' + filePath + ' has no CRS')
            if hf.searchForParameters(elements, ["crs","srsID"]) == "WGS84":
                return "4326"
            else:
                raise Exception('The csv file from ' + filePath + ' has no WGS84 CRS')
        else:
            return "4326"