import sys, os, datetime, argparse
import geoextent.lib.helpfunctions as hf
import geoextent.lib.extent as extent
import logging


def getOutput(filePath, typeOfData):
    output = extent.fromFile(filePath, typeOfData)
    if output is None:
        raise Exception("This file format is not supported")
    return output



def get_argparser():
    """Get arguments to extract geoextent """
    parser = argparse.ArgumentParser(
        prog='geoextent',
        usage='\n  __main__.py -b </absoulte/path/to/directory>',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=
        '''Supported formats:\n  - (.geojson)\n  - (.csv)\n  - (.shp)\n  - (.geotiff)'''
    )

    parser.add_argument(
        '--b', 
        nargs=1, 
        type=str,
        help='Extract bounding box'
    )

    return parser



argparser = get_argparser()


# Check if there is no arguments
if len(sys.argv[1:])==0:
    argparser.print_help()
    argparser.exit()

args = vars(argparser.parse_args())

p = args['b'][0]     #TODO: add a loop in case there is more than one input
op = args.popitem()[0]


'''
tells the program what to do with certain tags and their attributes that are
inserted over the command line
'''
# Check whether path is excisted
path = hf.checkPath(p)

if "/" in path:
    ending = path[path.rfind("/")+1:]    

#extracts spatial
if op == 'b':
    print("Extract bounding box:")
    if '.' in ending:
        # handle it as a file
        output = getOutput(path, 'b')
    
# print output differently depending on the outputs type
if 'output' in globals():
    if type(output) == list or type(output) == dict:
        hf.printObject(output)
    else: print(output)