import csv
import os
import logging
import geoextent.lib.helpfunctions as hf

fileType = "text/csv"

def checkFileValidity(filePath):
    '''Checks whether it is valid CSV or not. \n
    input "path": type string, path to file which shall be extracted \n
    raise exception if not valid
    '''
    logging.info("Checking validity of {} \n".format(filePath))
    
    with open(filePath) as csv_file:
        daten = csv.reader(csv_file.readlines())
        if daten is None:
            raise Exception("The file {} has no valid csv Attributes".format(filePath))


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

        spatialLatExtent= hf.searchForParameters(elements, ["latitude", "lat", "y"])
        minlat= None
        maxlat= None
        if spatialLatExtent is None:
            pass
        else:
            minlat= (min(spatialLatExtent))
            maxlat= (max(spatialLatExtent))

        spatialLonExtent= hf.searchForParameters(elements, ["longitude", "long", "lon", "lng", "x"])
        minlon= None
        maxlon= None
        if spatialLonExtent is None:
            raise Exception('The csv file from ' + filePath + ' has no BoundingBox')
        else:
            minlon= (min(spatialLonExtent))
            maxlon= (max(spatialLonExtent))

        spatialExtent= [minlon,minlat,maxlon,maxlat]
        if not spatialExtent:
            raise Exception("Bounding box could not be extracted")
        return spatialExtent


def getTemporalExtent(filePath):
    ''' extract time extent from csv string \n
    input "filePath": type string, file path to csv File \n
    returns temporal extent of the file: type list, length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1]
    '''
    with open(filePath) as csv_file:
        # To get delimiter either comma or simecolon
        daten = hf.getDelimiter(csv_file)

        elements = []
        for x in daten:
            elements.append(x)
            
        allspatialExtent= []
        allspatialExtent=hf.searchForParameters(elements, ["timestamp", "datetime", "time", "date"])
        if allspatialExtent is None:
            raise Exception('The csv file from ' + filePath + ' has no TemporalExtent')
        else:
            time=[]
            time.append(min(allspatialExtent))
            time.append(max(allspatialExtent))
            return time


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
        if hf.searchForParameters(elements,["longitude","latitude","long", "lat", "lon", "lng", "x", "y"]) is None:
            if hf.searchForParameters(elements, ["crs","srsID"]) is None:
                raise Exception('The csv file from ' + filePath + ' has no CRS')
            if hf.searchForParameters(elements, ["crs","srsID"]) == "WGS84":
                return "4326"
            else:
                raise Exception('The csv file from ' + filePath + ' has no WGS84 CRS')
        else:
            return "4326"