
import sys, os, getopt, datetime
import geoextent.lib.helpfunctions as hf
import geoextent.lib.extent as extent
import logging

COMMAND = None

# the capabilities of our CLI
def usage():
    """Provide usage instructions"""
    return '''
        NAME
            geoextent.py 

        Usage example
            extract_metadata.py -b </absoulte/path/to/directory>

        Supported formats:
            - (.geojson)
            - (.csv)
            - (.shp)
            - (.geotiff)

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