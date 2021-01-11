import argparse
import logging
import os
import sys
import zipfile

from . import __version__ as current_version
from .lib import extent

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("geoextent")

help_description = '''
geoextent is a Python library for extracting geospatial and temporal extents of a file
 or a directory of multiple geospatial data formats.
'''

help_epilog = '''
By default, both bounding box and temporal extent are extracted.

Examples:

geoextent path/to/geo_file.ext
geoextent -b path/to/directory_with_geospatial_data
geoextent -t path/to/file_with_temporal_extent
geoextent -b -t path/to/geospatial_files
geoextent -b -t --details path/to/zipfile_with_geospatial_data
'''

supported_formats = '''
Supported formats:
- GeoJSON (.geojson)
- Tabular data (.csv)
- GeoTIFF (.geotiff, .tif)
- Shapefile (.shp)
- GeoPackage (.gpkg)
- GPS Exchange Format (.gpx)
- Geography Markup Language (.gml)
- Keyhole Markup Language (.kml)

'''


# custom action, see e.g. https://stackoverflow.com/questions/11415570/directory-path-types-with-argparse
class readable_file_or_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for candidate in values:
            if not (os.path.isdir(candidate) or os.path.isfile(candidate) or zipfile.is_zipfile(candidate)):
                raise argparse.ArgumentTypeError("{0} is not a valid directory or file".format(candidate))
            if os.access(candidate, os.R_OK):
                setattr(namespace, self.dest, candidate)
            else:
                raise argparse.ArgumentTypeError("{0} is not a readable directory or file".format(candidate))


def get_arg_parser():
    """Get arguments to extract geoextent """
    parser = argparse.ArgumentParser(
        add_help=False,
        prog='geoextent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage="geoextent [-h] [--formats] [--version] [--debug] [--details] [-b] [-t] [input file]']"
    )

    parser.add_argument(
        '-h', '--help',
        action='store_true',
        help='show help message and exit'
    )

    parser.add_argument(
        '--formats',
        action='store_true',
        help='show supported formats'
    )

    parser.add_argument(
        '--version',
        action='store_true',
        help='show installed version'
    )

    parser.add_argument(
        '--debug',
        help='turn on debug logging, alternatively set environment variable GEOEXTENT_DEBUG=1',
        action='store_true'
    )

    parser.add_argument(
        '--details',
        action='store_true',
        default=False,
        help='Returns details of folder/zipFiles geoextent extraction',
    )

    parser.add_argument(
        '-b', '--bounding-box',
        action='store_true',
        default=False,
        help='extract spatial extent (bounding box)'
    )

    parser.add_argument(
        '-t', '--time-box',
        action='store_true',
        default=False,
        help='extract temporal extent (%%Y-%%m-%%d)'
    )

    parser.add_argument(
        'files',
        action=readable_file_or_dir,
        default=os.getcwd(),
        nargs=argparse.REMAINDER,
        help="input file or path"
    )

    return parser


def print_help():
    print(help_description)
    arg_parser.print_help()
    print(help_epilog)
    print_supported_formats()


def print_supported_formats():
    print(supported_formats)


def print_version():
    print(current_version)


arg_parser = get_arg_parser()


def main():
    # Check if there is no arguments, then print help
    if len(sys.argv[1:]) == 0:
        print_help()
        arg_parser.exit()

    # version, help, and formats must be checked before parse, as otherwise files are required 
    # but arg parser gives an error if allowed to be parsed first
    if "--help" in sys.argv:
        print_help()
        arg_parser.exit()
    if "--version" in sys.argv:
        print_version()
        arg_parser.exit()
    if "--formats" in sys.argv:
        print_supported_formats()
        arg_parser.exit()

    args = vars(arg_parser.parse_args())
    files = args['files']
    logger.debug('Extracting from inputs %s', files)

    # Set logging level
    if args['debug']:
        logging.getLogger('geoextent').setLevel(logging.DEBUG)
    if os.environ.get('GEOEXTENT_DEBUG', None) == "1":
        logging.getLogger('geoextent').setLevel(logging.DEBUG)

    output = None
    # Check if file is exists happens in parser validation, see readable_file_or_dir
    try:
        if os.path.isfile(os.path.join(os.getcwd(), files)) and not zipfile.is_zipfile(
                os.path.join(os.getcwd(), files)):
            output = extent.fromFile(files, bbox=args['bounding_box'], tbox=args['time_box'])
        if os.path.isdir(os.path.join(os.getcwd(), files)) or zipfile.is_zipfile(os.path.join(os.getcwd(), files)):
            output = extent.fromDirectory(files, bbox=args['bounding_box'], tbox=args['time_box'], details=True)
            if not args['details']:
                output.pop('details', None)

    except Exception as e:
        if logger.getEffectiveLevel() >= logging.DEBUG:
            logger.exception(e)
        sys.exit(1)

    if output is None:
        raise Exception("Did not find supported files at {}".format(files))
    else:
        logger.info("Output{}:".format(output))

    if type(output) == list:
        print(str(output))
    elif type(output) == dict:
        print(str(output))
    else:
        print(output)


if __name__ == '__main__':
    main()
