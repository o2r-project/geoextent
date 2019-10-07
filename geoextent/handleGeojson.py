
import helpfunctions as hf
import json
import sys
from datetime import datetime
import datetime
from django.utils.dateparse import parse_datetime
import django, pytz
import unicodedata
import pygeoj
import iso8601

DATATYPE = "application/geojson"

def extractContentFromPath(filePath):
    ''' method to extract geojson content from a file by using its filepath \n
    input "filepath": type string, path to file which shall be extracted \n
    returns geojson content of the filePath: type string,  returns  geojson content of filepath 
    '''  
    gjson = open(filePath, "rb")
    gjsonContent = json.load(gjson)
    gjson.close()
    return gjsonContent

def isValid(filePath):
    '''Checks whether it is gjson->->valid geojson or not. \n
    input "filepath": type string, path to file which shall be extracted \n
    output true if file is valid, false if not
    '''
    #TODO: make the function less complex using the function above
    try :
        ##print("H_gjson->->", "////////////////////")#
        gjson = open(filePath, "rb")
        ##print("gjson->->", gjson)#
        gjsonContent = json.load(gjson)
        ##print("gjsonContent->->", gjsonContent)#
        gjson.close()
        if not gjsonContent: #TODO: this exception dose not raised
            raise Exception('The geojson file from is empty')
        return True

    except ValueError as e:
        raise Exception ('The geojson file from ' + filePath + ' is not valid.' + str(e)) 

    except RuntimeError as e:
        raise Exception ('(geo)json file cannot be opened or read.' + str(e))
 
   
def convert3dto2d(filePath):
    '''transforms 3d to 2d coordinates in a geojson file. \n
    input "filepath": type string, path to file which shall be extracted \n
    returns geojson with 2d coordinates
    '''
    gjsonContent = extractContentFromPath(filePath)

    def extractAfterKeyword(searchParam, content):
        ''' searches for the value fo the dict entry with keyword which is given as input \n
        input "searchParam": type string, keyword for which is searched in the dict \n
        input "gjsonContent": type dict, Content of geojson File
        '''
        if type(content) == dict:
            for keyContent, valueContent in content.items():
                if keyContent == searchParam:   
                    valueContent = extractCoordinates(valueContent)
                if type(valueContent) == dict or type(valueContent) == list:
                    ##print("\n\n\ntest12",valueContent)#
                    extractAfterKeyword(searchParam, valueContent)
        if type(content) == list:
            for element in content:
                extractAfterKeyword(searchParam, element)


    def extractCoordinates(coordsList):
        ''' extract coordinates out of a some more lists (e.g. with Multipolygons), cuts the height from 3d coordinates \n
        input "coordsList": type list, value of dict entry with key "coordinates" \n
        returns list with 2 coordinates or list with list with 2 coordinates
        '''
        if type(coordsList) == list and len(coordsList) == 3 and (type(coordsList[0]) == float or type(coordsList[0]) == int) and (type(coordsList[1]) == float or type(coordsList[1]) == int) and (type(coordsList[2]) == float or type(coordsList[2]) == int):
            coordsList = coordsList.pop()
            ##print("\n\n\ntest1",coordsList)#
        elif type(coordsList) == list and len(coordsList) != 0:
            ##print("\n\n\ntest1",coordsList)#
            for value in coordsList:
                extractCoordinates(value)
        return coordsList

    #TODO:It works the same even when this line is Commented out
    extractAfterKeyword("coordinates", gjsonContent) 
    #print("\n\n\n1>>?22222",gjsonContent)#
    return gjsonContent


def getBoundingBox (filePath):
    ''' extract bounding box from geojson content \n
    input "filePath": type string, file path to geojson File \n
    returns bounding box: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] 
    '''
    bbox = None
    
    #gjsonContent is a FeatureCollection
    try:
        gjsonContent = pygeoj.load(data = convert3dto2d(filePath))
        #print("\n\n\n1>>?33333",convert3dto2d(filePath))#
        bbox = gjsonContent.bbox
    #gjsonContent is a single geometrie and has to be converted to a FeatureCollection
    except ValueError:
        gjsonContent = convert3dto2d(filePath)

        gjsonFeatureColl = {"type": "FeatureCollection", "features": []}
        gjsonFeatureColl["features"].append(gjsonContent)
        gjsonContent_FeatureColl = pygeoj.load(data=gjsonFeatureColl)
        bbox = gjsonContent_FeatureColl.bbox
    
    if not bbox:
        raise Exception("Bounding box could not be extracted")
    return bbox




def getCRS(filePath):
    ''' extracts EPSG number of the taken coordinate reference system (short: crs), as standard the crs WGS84 is used. \n
    input "filePath": type string, file path to geojson File \n
    returns the epsg code of the used coordinate reference system: type int, EPSG number of taken crs
    ''' 
    
    def extractAfterKeyword(searchParam, gjsonContent):
        ''' searches for the value fo the dict entry with keyword which is given as input \n
        input "searchParam": type string, keyword for which is searched in the dict \n
        input "gjsonContent": type dict, Content of geojson File
        '''
        if type(gjsonContent) == dict:
            for keyContent, valueContent in gjsonContent.items():
                if keyContent == searchParam:   
                    extracted.append(valueContent)
                if type(valueContent) == dict or type(valueContent) == list:
                    extractAfterKeyword(searchParam, valueContent)
        if type(gjsonContent) == list:
            for element in gjsonContent:
                extractAfterKeyword(searchParam, element)


    try:
        gjsonContent = pygeoj.load(filePath)
        #print("\n\n\n1>>?4444",gjsonContent)#
        crsCode = gjsonContent.crs 
        ##print("\n\n\n1>>?5555",crsCode)#
        if not crsCode:
            return hf.WGS84_EPSG_ID
        else: 
            for key, value in crsCode.items():
                if key == "properties":
                    try:
                        if value["name"] == "urn:ogc:def:crs:OGC:2:84":
                            return hf.WGS84_EPSG_ID
                        elif value["name"]:
                            splittedCrs = value["name"].split(":")
                            for elem in splittedCrs:
                                try:
                                    if int(elem) is not None:
                                        crsCode = int(elem)
                                        return crsCode
                                except:
                                    pass
                    except:
                        pass
                #formats like urn:ogc:def:crs:EPSG::25832
                
        return hf.WGS84_EPSG_ID
    except:
        gjsonContent = extractContentFromPath(filePath)
    
        #4326 is the standard epsg after http://wiki.geojson.org/GeoJSON_draft_version_6#Specification
        crsCode = hf.WGS84_EPSG_ID
        extracted = []
        extractAfterKeyword("crs", gjsonContent)
        if len(extracted) != 0:
            if type(extracted[0]) == dict and "properties" in extracted[0] and "code" in extracted[0]["properties"]:
                        crsCode = extracted[0]["properties"]["code"]
        return crsCode



def getTemporalExtent (filePath):
    ''' extract time extent from json string \n
    input "filePath": type string, file path to geojson File \n
    returns the temporal extent of the file: type list, length = 2, both entries have the type dateTime, temporalExtent[0] <= temporalExtent[1]
    '''
    #type list, contains all dates
    dateArray = []
    
    
    def searchForTimeElements(gjsonContent):
        ''' searches for time elements in a json \n
        input "gjsonContent": type dict, Content of geojson File
        '''
        
        ignore = ["created_at", "closed_at", "created", "closed", "initialize", "init", "last_viewed", "last_change", "change", "last_Change", "lastChange"] 
       

        if type(gjsonContent) == dict:
            for key, value in gjsonContent.items():     
                if key not in ignore:
                    searchForTimeElements(value)    
        elif type(gjsonContent) == list:
            for element in gjsonContent:
                searchForTimeElements(element)
        elif type(gjsonContent) == str:
            datetime_object = None
            datetime_object = parse_datetime(gjsonContent)
            if datetime_object == None:
                try:
                    datetime_object = iso8601.parse_date(gjsonContent)
                except:
                    pass
            if type(datetime_object) == datetime.datetime:
                dateArray.append(gjsonContent)



    gjsonContent = extractContentFromPath(filePath)
    temporalExtent = []

    searchForTimeElements(gjsonContent)
    if len(dateArray)!= 0:
        dateArray = sorted(dateArray)
        temporalExtent.append(dateArray[0])
        temporalExtent.append(dateArray[len(dateArray)-1])
    else:
        raise Exception("Could not extract timestamp.")
    return temporalExtent
