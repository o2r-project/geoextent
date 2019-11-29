<<<<<<< HEAD
import sys, os, datetime, argparse
import geoextent.lib.helpfunctions as hf
import geoextent.lib.extent as extent
=======

import sys, os, getopt, datetime
import geoextent.helpfunctions as hf
import geoextent.extent as extent
>>>>>>> 3a5f99d0a44035230fff7cd40075ba16e3298159
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

<<<<<<< HEAD
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

    '''
    parser.add_argument(
        'inputs',
        metavar='input',
        # TODO support files and directory, see e.g. https://stackoverflow.com/questions/11415570/directory-path-types-with-argparse
        type=argparse.FileType('r'),
        nargs=1, # later: '+' (one or more)
        help="input file or path"
    )
    '''

    parser.add_argument(
        '-b',
        type=str,
        nargs=1,
        help='extract spatial extent (bounding box)'
    )

    parser.add_argument(
        '-t',
        type=str,
        nargs=1,
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
    logger.debug('Extracting from inputs %s', args['b'])

    if args['b']:
        path = args['b'][0]
    elif args['t']:
        path = args['t'][0]

    # Check whether file is excisted
    hf.checkPath(path)

    # handle the boolean parameters as boolean, the following would me much more explicit:
    # output = getOutput(path, bbox = args['bounding_box'], time = args['time_box'])    

    '''
    if args['bounding_box'] and args['time_box']:
        logger.info("Extract bounding box and time box from %s", path.name)
        # since we already have parse the input, it would be better to 
        output = getOutput(path.name, 'bt')
    '''
    if args['b']:
        logger.info("Extract bounding box from %s", path)
        output = getOutput(path, 'b')
    else:
        logger.info("Extract time box from %s", path)
        output = getOutput(path, 't')

    # print output differently depending on the outputs type
    if output:
        if type(output) == list or type(output) == dict:
            hf.printObject(output)
        else: 
            print(output)

if __name__ == '__main__':
    main()
=======
COMMAND = None

# the capabilities of our CLI
def usage():
    """Provide usage instructions"""
    return '''
        NAME
            geoextent.py 

        Usage example
            extract_metadata.py -b </absoulte/path/to/directory>

        Available options:
            -b    Extract bounding box
'''


def errorFunction():
    print("Error: A tag is required for a command")
    print(usage())


if len(sys.argv) == 1:
    print(usage())
    sys.exit(1)


try:
    #opts contains tag and path, args contains other args
    OPTS, ARGS = getopt.getopt(sys.argv[1:], 'b:h')
except getopt.GetoptError as err:
    print('\nERROR: %s' % err)
    print(usage())
    #sys.exit(2)


if 'OPTS' in globals(): 
    if len(OPTS) == 0:
        errorFunction()


#process arguemnts from command line
if 'OPTS' not in globals():
    raise Exception("An Argument is required")


#o contains the tag and a contains path
for o, a in OPTS:
    '''
    tells the program what to do with certain tags and their attributes that are
    inserted over the command line
    '''
    ending = a
    if "/" in a:
        ending = a[a.rfind("/")+1:]    

    #extracts spatial and temporal metadata and also the vector representation
    if o == '-b':
        COMMAND = a
        print("Extract bounding box:")
        if '.' in ending:
            # handle it as a file
            output = extent.fromFile(a, 'b')
            if output is None:
                raise Exception("This file format is not supported")

    elif o == '-h':  # dump help and exit
        print(usage())
        sys.exit(3)
        
    # print output differently depending on the outputs type
    if 'output' in globals():
        if type(output) == list or type(output) == dict:
            hf.printObject(output)
        else: print(output)
>>>>>>> 3a5f99d0a44035230fff7cd40075ba16e3298159
