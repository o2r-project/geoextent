
import sys
import os
import getopt
import datetime
import threading
import logging

import geoextent.lib.handleCSV as handleCSV
import geoextent.lib.handleGeojson as handleGeojson
import geoextent.lib.handleShapefile as handleShapefile
import geoextent.lib.helpfunctions as hf

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


def fromFile(filePath, whatMetadata):
    ''' function is called when filePath is included in commandline (with tag 'b')
    how this is done depends on the file format - the function calls the extractMetadataFrom<format>()-function \n
    input "filePath": type string, path to file from which the metadata shall be extracted \n
    input "whatMetadata": type string, specifices which metadata should be extracted  \n
    returns None if the format is not supported, else returns the metadata of the file as a dict 
    (possible) keys of the dict: 'temporal_extent', 'bbox', 'vector_reps', 'crs'
    '''
    logging.info("Extracting {} from file {}\n".format(whatMetadata, filePath))
    
    fileFormat = filePath[filePath.rfind('.')+1:]
    usedModule = None

    # initialization of later output dict
    metadata = {}

    # first get the module that will be called (depending on the format of the file)
    if fileFormat == 'geojson' or fileFormat == 'json':
        usedModule = handleGeojson
    elif fileFormat == 'csv':
        usedModule = handleCSV
    elif fileFormat == 'shp' or fileFormat == 'dbf':
        usedModule = handleShapefile
    else: 
        # file format is not supported
        return None
    #only extracts metadata if the file content is valid
    try:
        fileValidity = usedModule.checkFileValidity(filePath)
    except Exception as e:
        print("Error for " + filePath + ": " + str(e))
        fileValidity = 'notValid'

    #get Bbox, Temporal Extent, Vector representation and crs parallel with threads
    class thread(threading.Thread): 
        def __init__(self, thread_ID): 
            threading.Thread.__init__(self) 
            self.thread_ID = thread_ID
        def run(self):
            metadata["format"] = usedModule.fileType
            #print("Thread with Thread_ID " +  str(self.thread_ID) + " now running...")
            #metadata[self.thread_ID] = self.thread_ID
            if self.thread_ID == 100:
                try:
                    metadata["bbox"] = computeBboxInWGS84(usedModule, filePath)
                except Exception as e:
                    print("Warning for " + filePath + ": " + str(e)) 
            elif self.thread_ID == 101:
                try:
                    metadata["temporal_extent"] = usedModule.getTemporalExtent(filePath)
                except Exception as e:
                    print("Warning for " + filePath + ": " + str(e))
            elif self.thread_ID == 103:
                try:
                    # the CRS is not neccessarily required
                    if hasattr(usedModule, 'getCRS'):
                        metadata["crs"] = usedModule.getCRS(filePath)
                    else: 
                        print ("Warning: The CRS cannot be extracted from the file")
                except Exception as e:
                    print("Warning for " + filePath + ": " + str(e))      
            try:
                barrier.wait()
            except Exception as e:
                barrier.abort()

    thread_bbox_except = thread(100) 
    thread_temp_except = thread(101) 
    thread_crs_except = thread(103)
    
    if fileValidity == 'valid':
        if whatMetadata == "b":
            # none of the metadata field is required 
            # so the system does not crash even if it does not find anything
            barrier = threading.Barrier(4)
            thread_bbox_except.start() 
            thread_temp_except.start() 
            thread_crs_except.start()
            barrier.wait() 
            barrier.reset() 
            barrier.abort() 
    elif fileValidity == 'empty':
        raise Exception("The file is empty, file path:( " +str(filePath)+" )")
    else:
        raise Exception("The file is not valid, file path:( " +str(filePath)+" )")
        
    return metadata
