import osgeo
import osgeo.gdal as gdal
import osgeo.osr as osr
import logging
from . import helpfunctions as hf

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
        logger.debug("File {} is NOT supported by handleRaster module".format(filepath))
        return False

    if file.RasterCount > 0:
        logger.debug("File {} is supported by handleRaster module".format(filepath))
        return True
    else:
        logger.debug("File {} is NOT supported by handleRaster module".format(filepath))
        return False


def getBoundingBox(filePath):
    ''' extracts bounding box from geotiff \n
    input "filepath": type string, file path to geotiff file \n
    returns bounding box of the file: type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)] 
    '''
    # Enable exceptions

    crs_output = hf.WGS84_EPSG_ID
    gdal.UseExceptions()

    geotiffContent = gdal.Open(filePath)

    # get the existing coordinate system
    old_crs = osr.SpatialReference()
    old_crs.ImportFromWkt(geotiffContent.GetProjectionRef())

    # create the new coordinate system

    new_crs = osr.SpatialReference()
    new_crs.ImportFromEPSG(crs_output)

    # get the point to transform, pixel (0,0) in this case
    width = geotiffContent.RasterXSize
    height = geotiffContent.RasterYSize
    gt = geotiffContent.GetGeoTransform()

    minx = gt[0]
    miny = gt[3] + width * gt[4] + height * gt[5]
    maxx = gt[0] + width * gt[1] + height * gt[2]
    maxy = gt[3]

    transform = osr.CoordinateTransformation(old_crs, new_crs)
    # get the coordinates in lat long
    latlongmin = transform.TransformPoint(minx, miny)
    latlongmax = transform.TransformPoint(maxx, maxy)

    bbox = [latlongmin[0], latlongmin[1], latlongmax[0], latlongmax[1]]

    if int(osgeo.__version__[0]) >= 3:
        if old_crs.GetAxisMappingStrategy() == 1:
            bbox = [latlongmin[1], latlongmin[0], latlongmax[1], latlongmax[0]]

    spatialExtent = {"bbox": bbox, "crs": str(crs_output)}

    return spatialExtent


def getTemporalExtent(filePath):
    ''' extracts temporal extent of the geotiff \n
    input "filepath": type string, file path to geotiff file \n
    returns None as There is no time value for GeoTIFF files 
    '''

    print('There is no time value for GeoTIFF files')
    return None

