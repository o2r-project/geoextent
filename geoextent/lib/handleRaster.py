import osgeo
import osgeo.gdal as gdal
import osgeo.osr as osr
import logging
from . import helpfunctions as hf

fileType = "image/tiff"

logger = logging.getLogger("geoextent")

def get_handler_name():
    return "handleRaster"

def checkFileSupported(filepath):
    '''Checks whether it is valid raster file or not. \n
    input "path": type string, path to file which shall be extracted \n
    raise exception if not valid
    '''

    logger.info(filepath)
    try:
        file = gdal.OpenEx(filepath)
        driver = file.GetDriver().ShortName
    except:
        logger.debug("File {} is NOT supported by HandleRaster module".format(filepath))
        return False

    if file.RasterCount > 0:
        logger.debug("File {} is supported by HandleRaster module".format(filepath))
        return True
    else:
        logger.debug("File {} is NOT supported by HandleRaster module".format(filepath))
        return False

def getBoundingBox(filePath):

    ''' extracts bounding box from geotiff \n
    input "filepath": type string, file path to geotiff file \n
    returns bounding box of the file: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] 
    '''
    # Enable exceptions
    gdal.UseExceptions()

    geotiffContent = gdal.Open(filePath)

    # get the existing coordinate system
    old_cs = osr.SpatialReference()
    old_cs.ImportFromWkt(geotiffContent.GetProjectionRef())
    if int(osgeo.__version__[0]) >= 3:
        # GDAL 3 changes axis order: https://github.com/OSGeo/gdal/issues/1546
        old_cs.SetAxisMappingStrategy(osgeo.osr.OAMS_TRADITIONAL_GIS_ORDER)

    logger.debug("old_cs {}".format(old_cs))

    # create the new coordinate system

    new_cs = osr.SpatialReference()
    new_cs.ImportFromEPSG(hf.WGS84_EPSG_ID)

    # create a transform object to convert between coordinate systems
    transform = osr.CoordinateTransformation(old_cs, new_cs)

    # get the point to transform, pixel (0,0) in this case
    width = geotiffContent.RasterXSize
    height = geotiffContent.RasterYSize
    gt = geotiffContent.GetGeoTransform()

    minx = gt[0]
    miny = gt[3] + width * gt[4] + height * gt[5]
    maxx = gt[0] + width * gt[1] + height * gt[2]
    maxy = gt[3]
    logger.debug("DELETE ME :  MINX: {} MINY: {} MAXX: {} MAXY: {}".format(minx,miny,maxx,maxy))

    # get the coordinates in lat long
    latlongmin = transform.TransformPoint(minx, miny)
    latlongmax = transform.TransformPoint(maxx, maxy)

    # get the bBox
    bbox = [latlongmin[0], latlongmin[1], latlongmax[0], latlongmax[1]]

    return bbox


def getCRS(filePath):
    ''' gets the coordinate reference systems from the geotiff file \n
    input "filepath": type string, file path to geotiff file \n
    return epsg code of the used coordiante reference system: type int
    '''

    return "4326"

def getTemporalExtent(filePath):
    ''' extracts temporal extent of the geotiff \n
    input "filepath": type string, file path to geotiff file \n
    returns None as There is no time value for GeoTIFF files 
    '''

    print('There is no time value for GeoTIFF files')
    return 'None'
