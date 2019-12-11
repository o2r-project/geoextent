import osgeo.gdal as gdal
import osgeo.gdalconst as gdalconst
import osgeo.osr as osr
import logging
import geoextent.lib.helpfunctions as hf

fileType = "image/tiff"

def checkFileValidity(filePath):
    '''Checks whether it is valid geotiff or not.
    input filepath: type string, path to file which shall be extracted
    raise exception if not valid
    '''
    logging.info("Checking validity of {} \n".format(filePath))

    # Enable exceptions
    gdal.UseExceptions()

    try:
        gtiffContent = gdal.Open(filePath)
        
        width = gtiffContent.RasterXSize
        height = gtiffContent.RasterYSize
    except Exception as e:
        raise Exception("The GeoTIFF file {} is not valid:\n{}".format(filePath, str(e)))


def getBoundingBox(filePath):
    ''' extracts bounding box from geotiff \n
    input "filepath": type string, file path to geotiff file \n
    returns bounding box of the file: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] 
    '''

    # Enable exceptions
    gdal.UseExceptions()

    geotiffContent = gdal.Open(filePath)

    #get the existing coordinate system
    old_cs= osr.SpatialReference()
    old_cs.ImportFromWkt(geotiffContent.GetProjectionRef())
    
    # create the new coordinate system
    wgs84_wkt = """
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]]"""
    new_cs = osr.SpatialReference()
    new_cs.ImportFromWkt(wgs84_wkt)

    # create a transform object to convert between coordinate systems
    transform = osr.CoordinateTransformation(old_cs,new_cs)
    
    #get the point to transform, pixel (0,0) in this case
    width = geotiffContent.RasterXSize
    height = geotiffContent.RasterYSize
    gt = geotiffContent.GetGeoTransform()

    minx = gt[0]
    miny = gt[3] + width*gt[4] + height*gt[5]
    maxx = gt[0] + width*gt[1] + height*gt[2]
    maxy = gt[3]

    #get the coordinates in lat long
    latlongmin = transform.TransformPoint(minx,miny)
    latlongmax = transform.TransformPoint(maxx,maxy)

    #get the bBox
    bbox = [latlongmin[0], latlongmin[1], latlongmax[0], latlongmax[1]]

    return bbox



def getCRS(filePath):
    ''' gets the coordinate reference systems from the geotiff file \n
    input "filepath": type string, file path to geotiff file \n
    return epsg code of the used coordiante reference system: type int
    '''

    return '4326'



def getTemporalExtent(filePath):
    ''' extracts temporal extent of the geotiff \n
    input "filepath": type string, file path to geotiff file \n
    returns None as There is no time value for GeoTIFF files 
    '''

    print('There is no time value for GeoTIFF files')
    return 'None'