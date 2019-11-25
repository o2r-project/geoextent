import sys, os, datetime, argparse
import geoextent.lib.helpfunctions as hf
import geoextent.lib.extent as extent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

help_description = '''
geoextent is a Python library for extracting geospatial and temporal extents of files and directories with multiple data formats.
'''

help_epilog = '''
By default, both bounding box and temporal extent are extracted.

Examples:

geoextent -b path/to/directory_with_geospatial_data
geoextent -t path/to/file_with_temporal_extent

Supported formats:
- GeoJSON (.geojson)
- Tabular data (.csv)
- Shapefile (.shp)
- GeoTIFF (.geotiff, .tif)
'''

def getOutput(filePath, typeOfData):
    output = extent.fromFile(filePath, typeOfData)
    if output is None:
        raise Exception("This file format is not supported")
    return output

def get_argparser():
    """Get arguments to extract geoextent """
    parser = argparse.ArgumentParser(
        prog='geoextent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=help_description,
        epilog=help_epilog,
    )

    parser.add_argument(
        'inputs',
        metavar='input',
        # TODO support files and directory, see e.g. https://stackoverflow.com/questions/11415570/directory-path-types-with-argparse
        type=argparse.FileType('r'),
        nargs=1, # later: '+' (one or more)
        help="input file or path"
    )

    parser.add_argument(
        '-b', '--bounding-box',
        action='store_true',
        help='extract spatial extent (bounding box)'
    )

    parser.add_argument(
        '-t', '--time-box',
        action='store_true',
        help='extract temporal extent'
    )

    return parser


def main():
    argparser = get_argparser()

    # Check if there is no arguments, then print help
    if len(sys.argv[1:])==0:
        argparser.print_help()
        argparser.exit()

    args = vars(argparser.parse_args())

    logger.debug('Extracting from inputs %s', args['inputs'])

    path = args['inputs'][0]

    # handle the boolean parameters as boolean, the following would me much more explicit:
    # output = getOutput(path, bbox = args['bounding_box'], time = args['time_box'])    

    if args['bounding_box'] and args['time_box']:
        logger.info("Extract bounding box and time box from %s", path.name)
        # since we already have parse the input, it would be better to 
        output = getOutput(path.name, 'bt')
    elif args['bounding_box']:
        logger.info("Extract bounding box from %s", path)
        output = getOutput(path.name, 'b')
    elif args['time_box']:
        logger.info("Extract time box from %s", path)
        output = getOutput(path.name, 't')

    # print output differently depending on the outputs type
    if 'output' in globals():
        if type(output) == list or type(output) == dict:
            hf.printObject(output)
        else: print(output)

if __name__ == '__main__':
    main()