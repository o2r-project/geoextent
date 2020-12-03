import logging
import os
import threading
import zipfile
from osgeo import ogr
from osgeo import gdal

from . import handleCSV
from . import handleVector
from . import handleRaster
from . import helpfunctions as hf

logger = logging.getLogger("geoextent")

handle_modules = {'CSV': handleCSV,"raster":handleRaster,"vector":handleVector}

def computeBboxInWGS84(module, path):
    ''' 
    input "module": type module, module from which methods shall be used \n
    input "path": type string, path to file \n
    returns a bounding box, type list, length = 4 , type = float, schema = [min(longs), min(lats), max(longs), max(lats)], the boudning box has either its original crs or WGS84 (transformed).
    '''
    bbox_in_orig_crs = module.getBoundingBox(path)
    try:
        # TODO: Add function using to reproject coordinates system
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

    logger.info("Extracting bbox={} tbox={} from Directory {}".format(bbox, tbox, path))

    if not bbox and not tbox:
        logger.error("Require at least one of extraction options, but bbox is {} and tbox is {}".format(bbox, tbox))
        raise Exception("No extraction options enabled!")
    metadata = {}
    # initialization of later output dict
    metadata_directory = {}

    isZip = zipfile.is_zipfile(path)

    if isZip:
        logger.info("Inspecting zipfile {}".format(path))
        hf.extract_zip(path)
        extract_folder = path[:-4]
        logger.info("Extract_folder zipfile {}".format(extract_folder))
        path = extract_folder

    for filename in os.listdir(path):
        logger.info("path {}, folder/zipfile {}".format(path,filename))
        isZip = zipfile.is_zipfile(os.path.join(path, filename))
        if isZip:
            logger.info("**Inspecting folder {}, is zip ? {}**".format(filename, str(isZip)))
            metadata_directory[filename] = fromDirectory(os.path.join(path,filename),bbox,tbox)
        else:
            logger.info("Inspecting folder {}, is zip ? {}".format(filename, str(isZip)))
            if os.path.isdir(os.path.join(path,filename)):
                metadata_directory[filename] = fromDirectory(os.path.join(path, filename), bbox, tbox)
            else:
                metadata_file = fromFile(os.path.join(path, filename), bbox, tbox)
                metadata_directory[str(filename)] = metadata_file

    file_format = "zip" if isZip else 'folder'
    metadata['format'] = file_format

    if bbox:
        bbox_ext = hf.bbox_merge(metadata_directory,path)
        if bbox_ext is not None:
            metadata['crs'] = "4326"
            metadata['bbox'] = bbox_ext
        else:
            logger.warning("The {} {} has no identifiable bbox - Coordinate reference system (CRS) may be missing".format(file_format,path))

    if tbox:
        tbox_ext = hf.tbox_merge(metadata_directory,path)
        if tbox_ext is not None:
            metadata['tbox'] = tbox_ext
        else:
            logger.warning("The {} {} has no identifiable time extent".format(file_format,path))

    #metadata['details'] = metadata_directory

    return metadata

def fromFile(filePath, bbox=True, tbox=True, num_sample=None):
    ''' TODO: update these docs
    
    function is called when filePath is included in commandline (with tag 'b')
    how this is done depends on the file format - the function calls the handler for each supported format \n
    extracted data are bounding box, temporal extent and crs, a seperate thread is dedicated to each extraction process \n
    input "filePath": type string, path to file from which the metadata shall be extracted \n
    input "whatMetadata": type string, specifices which metadata should be extracted  \n
    returns None if the format is not supported, else returns the metadata of the file as a dict 
    (possible) keys of the dict: 'temporal_extent', 'bbox', 'vector_reps', 'crs'
    '''
    logger.info("Extracting bbox={} tbox={} from file {}".format(bbox, tbox, filePath))

    if bbox == False and tbox == False:
        logger.error("Require at least one of extraction options, but bbox is {} and tbox is {}".format(bbox, tbox))
        raise Exception("No extraction options enabled!")

    fileFormat = os.path.splitext(filePath)[1][1:]

    usedModule = None

    # initialization of later output dict
    metadata = {}

    # get the module that will be called (depending on the format of the file)

    for i in handle_modules:
        valid = handle_modules[i].checkFileValidity(filePath)
        if valid == True:
            usedModule = handle_modules[i]
            break

    # If file format is not supported
    if not usedModule:
        logger.info("Did not find a compatible module for file format {} of file {}".format(fileFormat, filePath))
        return None

    # get Bbox, Temporal Extent, Vector representation and crs parallel with threads
    class thread(threading.Thread):
        def __init__(self, task):
            threading.Thread.__init__(self)
            self.task = task

        def run(self):

            metadata["format"] = usedModule.fileType

            # with lock:

            logger.debug("Starting  thread {} on file {}".format(self.task, filePath))
            if self.task == "bbox":
                try:
                    if bbox:
                        metadata["bbox"] = computeBboxInWGS84(usedModule, filePath)
                except Exception as e:
                    logger.warning("Error for {} extracting bbox:\n{}".format(filePath, str(e)))
            elif self.task == "tbox":
                try:
                    if tbox:
                        if usedModule.fileType == 'text/csv':
                            extract_tbox = usedModule.getTemporalExtent(filePath, num_sample)
                        else:
                            if num_sample is not None:
                                logger.warning("num_sample parameter is ignored, only applies to CSV files")
                            extract_tbox = usedModule.getTemporalExtent(filePath)
                        metadata["tbox"] = extract_tbox
                except Exception as e:
                    logger.warning("Error extracting tbox, time format not found \n {}:".format(str(e)))
            elif self.task == "crs":
                try:
                    # the CRS is not necessarily required
                    if bbox and hasattr(usedModule, 'getCRS'):
                        metadata["crs"] = usedModule.getCRS(filePath)
                    elif tbox and hasattr(usedModule, 'getCRS'):
                        metadata["crs"] = usedModule.getCRS(filePath)
                    else:
                        logger.debug("The CRS cannot be extracted from the file {}".format(filePath))
                except Exception as e:
                    logger.warning("Error for {} extracting CRS:\n{}".format(filePath, str(e)))
            else:
                raise Exception("Unsupported thread task {}".format(self.task))

            logger.debug("Completed thread {} on file {}".format(self.task, filePath))

    thread_bbox_except = thread("bbox")
    thread_temp_except = thread("tbox")
    thread_crs_except = thread("crs")

    # lock = threading.Lock()
    logger.debug("Starting 3 threads for extraction.")

    thread_bbox_except.start()
    thread_temp_except.start()
    thread_crs_except.start()

    thread_bbox_except.join()
    thread_temp_except.join()
    thread_crs_except.join()

    logger.debug("Extraction finished: {}".format(str(metadata)))
    return metadata


