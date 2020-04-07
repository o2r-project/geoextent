import sys, os, datetime, argparse
import geoextent.lib.helpfunctions as hf
import geoextent.lib.extent as extent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

help_description = '''
geoextent is a Python library for extracting geospatial and temporal extents of a file or a directory of multiple geospatial data formats.
'''

help_epilog = '''
By default, both bounding box and temporal extent are extracted.

Examples:

geoextent path/to/geofile.ext
geoextent -b path/to/directory_with_geospatial_data
geoextent -t path/to/file_with_temporal_extent
geoextent -b -t path/to/geospatial_files
'''

supported_formats = '''
Supported formats:
- GeoJSON (.geojson)
- Tabular data (.csv)
- Shapefile (.shp)
- GeoTIFF (.geotiff, .tif)
'''


# custom action, see e.g. https://stackoverflow.com/questions/11415570/directory-path-types-with-argparse
class readable_file_or_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for candidate in values:
            if not (os.path.isdir(candidate) or os.path.isfile(candidate)):
                raise argparse.ArgumentTypeError("{0} is not a valid directory or file".format(candidate))
            if os.access(candidate, os.R_OK):
                setattr(namespace,self.dest,candidate)
            else:
                raise argparse.ArgumentTypeError("{0} is not a readable directory or file".format(candidate))


def get_argparser():
    """Get arguments to extract geoextent """
    parser = argparse.ArgumentParser(
        add_help=False,
        prog='geoextent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage= "geoextent [-h] [-formats] [-b] [-t] [-input= '[filepath|input file]']"
    )

    parser.add_argument(
        '-h','--help',
        action='store_true',
        help='show help message and exit'
    )
    
    parser.add_argument(
        '-formats',
        action='store_true',
        help='show supported formats'
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

    parser.add_argument(
        '-input=',
        action=readable_file_or_dir,
        default=os.getcwd(),
        nargs='+',
        help="input file or path"
    )
    
    return parser

def print_help_fun():
    print(help_description)
    argparser.print_help()
    print_examples()
    print_supported_formats()

def print_examples():
    print(help_epilog)

def print_supported_formats():
    print(supported_formats)


argparser = get_argparser()


def main():
    # Check if there is no arguments, then print help
    if len(sys.argv[1:])==0:
        print_help_fun()
        argparser.exit()

    args = vars(argparser.parse_args())
    logger.debug('Extracting from inputs %s', args['input='])

    if(args['help']):
        print_help_fun()
    elif(args['formats']):
        print_supported_formats()
    else:
        # Check if file is exists happens in parser validation, see readable_file_or_dir
        if os.path.isfile(os.path.join(os.getcwd(), args['input='])):
            output = extent.fromFile(args['input='], bbox = args['bounding_box'], tbox = args['time_box'])
        if os.path.isdir(os.path.join(os.getcwd(), args['input='])):
            output = extent.fromDirectory(args['input='], bbox = args['bounding_box'], tbox = args['time_box'])
        
        if output is None:
            raise Exception("This file format is not supported")

        # print output
        if type(output) == list or type(output) == dict:
            print(str(output))
        else: 
            print(output)
    

if __name__ == '__main__':
    main()
