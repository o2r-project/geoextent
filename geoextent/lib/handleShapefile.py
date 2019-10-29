
import shapefile
import sys
import os
import logging
import geoextent.lib.helpfunctions as hf

fileType = "application/shp"

def checkFileValidity(filePath):
    '''Checks whether it is valid shapefile or not. \n
    input "path": type string, path to file which shall be extracted \n
    output 'valid' if file is valid, 'empty' if file is empty, 'notValid' if not valid
    '''
    logging.info("Checking validity of {} \n".format(filePath))
    
    try:
        if(os.stat(filePath).st_size == 0):
            return 'empty'
        else:
            sf = shapefile.Reader(filePath)
            return 'valid'
    except:
        return 'notValid'


def getCRS(path):
    ''' gets the coordinate reference systems from the shapefile \n
    input "path": type string, file path to shapefile 
    '''
    
    return 'None'


def getTemporalExtent(filePath):
    ''' extracts temporal extent of the shapefile \n
    input "path": type string, file path to shapefile file
    '''

    return 'None'


def getBoundingBox(filePath):
    ''' extracts bounding box from shapfile \n
    input "path": type string, file path to shapefile \n
    returns bounding box of the file: type list, length = 4
    '''
    bbox = None

    sf = shapefile.Reader(filePath)
    bbox = sf.bbox

    if not bbox:
        raise Exception("Bounding box could not be extracted")

    return bbox
