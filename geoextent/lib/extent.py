import logging
import os
import threading
import zipfile
import tempfile
from traitlets import List
from traitlets.config import Application
from .content_providers import Zenodo
from . import handleCSV
from . import handleRaster
from . import handleVector
from . import helpfunctions as hf

logger = logging.getLogger("geoextent")
handle_modules = {'CSV': handleCSV, "raster": handleRaster, "vector": handleVector}


def compute_bbox_wgs84(module, path):
    """
    input "module": type module, module from which methods shall be used \n
    input "path": type string, path to file \n
    returns a bounding box, type list, length = 4 , type = float,
        schema = [min(longs), min(lats), max(longs), max(lats)],
        the bounding box has either its original crs or WGS84(transformed).
    """
    logger.debug("compute_bbox_wgs84: {}".format(path))
    spatial_extent_origin = module.getBoundingBox(path)

    try:
        if spatial_extent_origin['crs'] == str(hf.WGS84_EPSG_ID):
            spatial_extent = spatial_extent_origin
        else:
            spatial_extent = {'bbox': hf.transformingArrayIntoWGS84(spatial_extent_origin['crs'],
                                                                    spatial_extent_origin['bbox']),
                              'crs': str(hf.WGS84_EPSG_ID)}
    except Exception as e:
        raise Exception("The bounding box could not be transformed to the target CRS epsg:{} \n error {}"
                        .format(hf.WGS84_EPSG_ID, e))

    validate = hf.validate_bbox_wgs84(spatial_extent['bbox'])
    logger.debug("Validate: {}".format(validate))

    if not hf.validate_bbox_wgs84(spatial_extent['bbox']):
        try:
            flip_bbox = hf.flip_bbox(spatial_extent['bbox'])
            spatial_extent['bbox'] = flip_bbox

        except Exception as e:
            raise Exception("The bounding box could not be transformed to the target CRS epsg:{} \n error {}"
                            .format(hf.WGS84_EPSG_ID, e))

    return spatial_extent


def fromDirectory(path, bbox=False, tbox=False, details=False):
    """ Extracts geoextent from a directory/ZipFile
    Keyword arguments:
    path -- directory/ZipFile path
    bbox -- True if bounding box is requested (default False)
    tbox -- True if time box is requested (default False)
    """

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
        logger.info("path {}, folder/zipfile {}".format(path, filename))
        isZip = zipfile.is_zipfile(os.path.join(path, filename))
        if isZip:
            logger.info("**Inspecting folder {}, is zip ? {}**".format(filename, str(isZip)))
            metadata_directory[filename] = fromDirectory(os.path.join(path, filename), bbox, tbox, details=True)
        else:
            logger.info("Inspecting folder {}, is zip ? {}".format(filename, str(isZip)))
            if os.path.isdir(os.path.join(path, filename)):
                metadata_directory[filename] = fromDirectory(os.path.join(path, filename), bbox, tbox, details=True)
            else:
                metadata_file = fromFile(os.path.join(path, filename), bbox, tbox)
                metadata_directory[str(filename)] = metadata_file

    file_format = "zip" if isZip else 'folder'
    metadata['format'] = file_format

    if bbox:
        bbox_ext = hf.bbox_merge(metadata_directory, path)
        if bbox_ext is not None:
            if len(bbox_ext) != 0:
                metadata['crs'] = bbox_ext['crs']
                metadata['bbox'] = bbox_ext['bbox']
        else:
            logger.warning(
                "The {} {} has no identifiable bbox - Coordinate reference system (CRS) may be missing".format(
                    file_format, path))

    if tbox:
        tbox_ext = hf.tbox_merge(metadata_directory, path)
        if tbox_ext is not None:
            metadata['tbox'] = tbox_ext
        else:
            logger.warning("The {} {} has no identifiable time extent".format(file_format, path))

    if details:
        metadata['details'] = metadata_directory

    return metadata


def fromFile(filepath, bbox=True, tbox=True, num_sample=None):
    """ Extracts geoextent from a file
    Keyword arguments:
    path -- filepath
    bbox -- True if bounding box is requested (default False)
    tbox -- True if time box is requested (default False)
    num_sample -- sample size to determine time format (Only required for csv files)
    """
    logger.info("Extracting bbox={} tbox={} from file {}".format(bbox, tbox, filepath))

    if not bbox and not tbox:
        logger.error("Require at least one of extraction options, but bbox is {} and tbox is {}".format(bbox, tbox))
        raise Exception("No extraction options enabled!")

    file_format = os.path.splitext(filepath)[1][1:]

    usedModule = None

    # initialization of later output dict
    metadata = {}

    # get the module that will be called (depending on the format of the file)

    for i in handle_modules:
        valid = handle_modules[i].checkFileSupported(filepath)
        if valid:
            usedModule = handle_modules[i]
            logger.info("{} is being used to inspect {} file".format(usedModule.get_handler_name(), filepath))
            break

    # If file format is not supported
    if not usedModule:
        logger.info("Did not find a compatible module for file format {} of file {}".format(file_format, filepath))
        return None

    # get Bbox, Temporal Extent, Vector representation and crs parallel with threads
    class thread(threading.Thread):
        def __init__(self, task):
            threading.Thread.__init__(self)
            self.task = task

        def run(self):

            metadata["format"] = file_format
            metadata["geoextent_handler"] = usedModule.get_handler_name()

            # with lock:

            logger.debug("Starting  thread {} on file {}".format(self.task, filepath))
            if self.task == "bbox":
                try:
                    if bbox:
                        spatial_extent = compute_bbox_wgs84(usedModule, filepath)
                        if spatial_extent is not None:
                            metadata["bbox"] = spatial_extent['bbox']
                            metadata["crs"] = spatial_extent['crs']
                except Exception as e:
                    logger.warning("Error for {} extracting bbox:\n{}".format(filepath, str(e)))
            elif self.task == "tbox":
                try:
                    if tbox:
                        if usedModule.get_handler_name() == 'handleCSV':
                            extract_tbox = usedModule.getTemporalExtent(filepath, num_sample)
                        else:
                            if num_sample is not None:
                                logger.warning("num_sample parameter is ignored, only applies to CSV files")
                            extract_tbox = usedModule.getTemporalExtent(filepath)
                        if extract_tbox is not None:
                            metadata["tbox"] = extract_tbox
                except Exception as e:
                    logger.warning("Error extracting tbox, time format not found \n {}:".format(str(e)))
            else:
                raise Exception("Unsupported thread task {}".format(self.task))
            logger.debug("Completed thread {} on file {}".format(self.task, filepath))

    thread_bbox_except = thread("bbox")
    thread_temp_except = thread("tbox")

    logger.debug("Starting 2 threads for extraction.")

    thread_bbox_except.start()
    thread_temp_except.start()

    thread_bbox_except.join()
    thread_temp_except.join()

    logger.debug("Extraction finished: {}".format(str(metadata)))

    return metadata


def from_repository(repository_identifier, bbox=False, tbox=False, details=False):
    try:
        geoextent = geoextent_from_repository()
        metadata = geoextent.from_repository(repository_identifier, bbox, tbox, details)
        metadata['format'] = 'repository'
    except ValueError as e:
        logger.debug("Error while inspecting repository {}: {}".format(repository_identifier, e))
        raise Exception(e)

    return metadata


class geoextent_from_repository(Application):
    content_providers = List([Zenodo.Zenodo], config=True, help="""
        Ordered list by priority of ContentProviders to try in turn to fetch
        the contents specified by the user.
        """
                             )

    def from_repository(self, repository_identifier, bbox=False, tbox=False, details=False):

        if bbox + tbox == 0:
            logger.error("Require at least one of extraction options, but bbox is {} and tbox is {}".format(bbox, tbox))
            raise Exception("No extraction options enabled!")

        for h in self.content_providers:
            repository = h()
            supported_by_geoextent = False
            if repository.validate_provider(reference=repository_identifier):
                logger.debug("Using {} to extract {}".format(repository.name, repository_identifier))
                supported_by_geoextent = True
                try:
                    with tempfile.TemporaryDirectory() as tmp:
                        repository.download(tmp)
                        metadata = fromDirectory(tmp, bbox, tbox, details)
                    return metadata
                except ValueError as e:
                    raise Exception(e)
            if supported_by_geoextent is False:
                logger.error("Geoextent can not handle this repository identifier {}"
                                 "\n Check for typos or if the repository exists. ".format(repository_identifier)
                            )
