
Command-Line Interface (CLI)
============================

**geoextent** is called with this Command::
   
   python3 geoextent [-h] [-b] [-t] input

**input**
   Input file or path

**-h, --help**
   Show this help message and exit

**-b, --bounding-box**
   Extract spatial extent (bounding box)

**-t, --time-box**
   Extract temporal extent

Examples:-
----------
**Ex (1):** Show help message:

::

   python3 geoextent -h

output

::

   usage: geoextent [-h] [-b] [-t] input [input ...]

   geoextent is a Python library for extracting geospatial and temporal extents of a file or a directory of multiple geospatial data formats.

   positional arguments:
   input               input file or path

   optional arguments:
   -h, --help          show this help message and exit
   -b, --bounding-box  extract spatial extent (bounding box)
   -t, --time-box      extract temporal extent

   By default, both bounding box and temporal extent are extracted.

   Examples:

   geoextent path/to/geofile.ext
   geoextent -b path/to/directory_with_geospatial_data
   geoextent -t path/to/file_with_temporal_extent
   geoextent -b -t path/to/geospatial_files

   Supported formats:
   - GeoJSON (.geojson)
   - Tabular data (.csv)
   - Shapefile (.shp)
   - GeoTIFF (.geotiff, .tif)

**Ex (2):** Extract bounding box:

::

   python3 geoextent -b -t 'file.geojson'

output

::

   {'format': 'application/geojson', 'crs': 4326, 'bbox': [7.60168075561523, 51.9488147720619, 7.64725685119629, 51.9746240298775]}

**Ex (3):** Extract time interval:

::

   python3 geoextent -b -t 'file.geojson'

output

::

   {'format': 'application/geojson', 'crs': 4326, 'bbox': [7.60168075561523, 51.9488147720619, 7.64725685119629, 51.9746240298775]}

**Ex (4):** Extract both bounding box and time interval:

::

   python3 geoextent -b -t 'file.geojson'

output

::

   {'format': 'application/geojson', 'bbox': [7.60168075561523, 51.9488147720619, 7.64725685119629, 51.9746240298775], 'tbox': ['2018-11-14', '2018-11-14'], 'crs': 4326}