
import sys, os, threading
import logging

import geoextent.lib.handleCSV as handleCSV
import geoextent.lib.handleGeojson as handleGeojson
import geoextent.lib.handleShapefile as handleShapefile
import geoextent.lib.handleGeotiff as handleGeotiff
import geoextent.lib.helpfunctions as hf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


modulesSupported = {'geojson':handleGeojson, 'json':handleGeojson,'csv':handleCSV,
    'shp':handleShapefile, 'dbf':handleShapefile, 'geotiff':handleGeotiff, 'tif':handleGeotiff}

def computeBboxInWGS84(module, path):
    ''' 
    input "module": type module, module from which methods shall be used \n
    input "path": type string, path to file \n
    returns a bounding box, type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)], the boudning box has either its original crs or WGS84 (transformed).
    '''
    bbox_in_orig_crs = module.getBoundingBox(path)
    try:
        #TODO: Add function using to reproject coordinates system
        if module.fileType == "application/shp":
            crs = 'None'
            return bbox_in_orig_crs
        else:
            crs = module.getCRS(path)
    except:
        pass
    if 'crs' in locals() and crs and bbox_in_orig_crs:
        bbox_transformed = hf.transformingArrayIntoWGS84(crs, bbox_in_orig_crs)
        return bbox_transformed
    else:
        raise Exception("The bounding box could not be related to a CRS")

def fromDirectory(path, bbox=False, tbox=False):
    ''' TODO: implement
    '''

def fromFile(filePath, bbox=True, tbox=True):
    ''' TODO: update these docs
    
    function is called when filePath is included in commandline (with tag 'b')
    how this is done depends on the file format - the function calls the handler for each supported format \n
    extracted data are bounding box, temporal extent and crs, a seperate thread is dedicated to each extraction process \n
    input "filePath": type string, path to file from which the metadata shall be extracted \n
    input "whatMetadata": type string, specifices which metadata should be extracted  \n
    returns None if the format is not supported, else returns the metadata of the file as a dict 
    (possible) keys of the dict: 'temporal_extent', 'bbox', 'vector_reps', 'crs'
    '''
    logging.info("Extracting bbox={} tbox={} from file {}".format(bbox, tbox, filePath))

    if bbox == False and tbox == False:
        raise Exception("Please enter correct arguments")
    
    fileFormat = os.path.splitext(filePath)[1][1:]

    usedModule = None

    # initialization of later output dict
    metadata = {}
    
    # get the module that will be called (depending on the format of the file)
    for key in modulesSupported.keys():
        if key == fileFormat:
            logging.info("Module used: {}".format(key))
            usedModule = modulesSupported.get(key)

    # If file format is not supported
    if not usedModule:
        logger.info("Did not find a compatible module for file format {} of file {}".format(fileFormat, filePath))
        return None
 
    # Only extract metadata if the file content is valid
    try:
        usedModule.checkFileValidity(filePath)
    except Exception as e:
        raise Exception(os.getcwd()+" The file {} is not valid (e.g. empty):\n{}".format(filePath, str(e)))
        
    #get Bbox, Temporal Extent, Vector representation and crs parallel with threads
    class thread(threading.Thread): 
        def __init__(self, thread_ID): 
            threading.Thread.__init__(self) 
            self.thread_ID = thread_ID
        def run(self):
            metadata["format"] = usedModule.fileType

            if self.thread_ID == 100:
                try:
                    if bbox:
                        metadata["bbox"] = computeBboxInWGS84(usedModule, filePath)
                except Exception as e:
                    logger.warning("Warning for {} extracting bbox:\n{}".format(filePath, str(e)))
            elif self.thread_ID == 101:
                try:
                    if tbox:
                        metadata["tbox"] = usedModule.getTemporalExtent(filePath)
                except Exception as e:
                    logger.warning("Warning for {} extracting tbox:\n{}".format(filePath, str(e)))
            elif self.thread_ID == 103:
                try:
                    # the CRS is not neccessarily required
                    if bbox and hasattr(usedModule, 'getCRS'):
                        metadata["crs"] = usedModule.getCRS(filePath)
                    else: 
                        logger.warning("Warning: The CRS cannot be extracted from the file {}".format(filePath))
                except Exception as e:
                    logger.warning("Warning for {} extracting CRS:\n{}".format(filePath, str(e)))
            try:
                barrier.wait()
            except Exception as e:
                logger.error(e)
                barrier.abort()

    thread_bbox_except = thread(100) 
    thread_temp_except = thread(101) 
    thread_crs_except = thread(103)
    
    barrier = threading.Barrier(4)
    thread_bbox_except.start() 
    thread_temp_except.start() 
    thread_crs_except.start()
    barrier.wait() 
    barrier.reset() 
    barrier.abort()

    logger.debug("Extraction finished: {}".format(str(metadata)))
    return metadata
