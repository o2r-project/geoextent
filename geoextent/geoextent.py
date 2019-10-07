
import sys, os, getopt, datetime
import helpfunctions as hf
import extractFromFolderOrFile as extract

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

#print("1111111111111111")#
def errorFunction():
    print("Error: A tag is required for a command")
    print(usage())

##print("222222222222222")#
#print(sys.argv)#
#print(str(sys.argv))#
#print(len(sys.argv))#
#print(sys.argv[0])#


if len(sys.argv) == 1:
    print(usage())
    sys.exit(1)

##print("333333333333333")#
try:
    OPTS, ARGS = getopt.getopt(sys.argv[1:], 'b:h')
    ##print("opts:", OPTS)
    ##print("ARGS:", ARGS)
except getopt.GetoptError as err:
    print('\nERROR: %s' % err)
    print(usage())
    #sys.exit(2)

##print("444444444444444")#
if 'OPTS' in globals(): 
    #print("globals",globals())#
    if len(OPTS) == 0:
        errorFunction()

#process arguemnts from command line
if 'OPTS' not in globals():
    raise Exception("An Argument is required")

for o, a in OPTS:
    ##print("o",o)#
    ##print("a",a)#
    '''
    tells the program what to do with certain tags and their attributes that are
    inserted over the command line
    '''
    ending = a
    if "/" in a:
        ending = a[a.rfind("/")+1:]
    ##print("ending",ending)#
    

    #extracts spatial and temporal metadata and also the vector representation
    if o == '-b':
        COMMAND = a
        print("Extract bounding box:")
        if '.' in ending:
            # handle it as a file
            output = extract.extractMetadataFromFile(a, 'b')
            if output is None:
                raise Exception("This file format is not supported")

    elif o == '-h':  # dump help and exit
        print(usage())
        sys.exit(3)
        
    # print output differently depending on the outputs type
    if 'output' in globals():
        ##print("output->", output)#
        ##print("type_output->", type(output))#
        if type(output) == list or type(output) == dict:
            hf.printObject(output)
        else: print(output)