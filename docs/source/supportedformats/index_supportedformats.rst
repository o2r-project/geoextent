======================
Supported file formats
======================

The library supoorts the following file formats so far. The development process is persistent to expand the number of supported formats.

.. jupyter-execute::
   :hide-code:

   import geoextent.__main__ as geoextent
   geoextent.print_supported_formats()


Examples:-
----------

**Example 1:** Extracting geoextent from a GeoJSON file:

The file used in the example obtianed from `here <https://raw.githubusercontent.com/o2r-project/geoextent/master/tests/testdata/geojson/muenster_ring_zeit.geojson>`_ 
::

   geoextent -b -t -input= 'muenster_ring_zeit.geojson'

output

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent
   import subprocess

   # (1) Download showcase file and extract geoextent data
   subprocess.run('mkdir showcase_geojson', shell=True)
   subprocess.run('wget -P showcase_geojson https://raw.githubusercontent.com/o2r-project/geoextent/master/tests/testdata/geojson/muenster_ring_zeit.geojson', shell=True)

   geoextent.fromFile('showcase_geojson/muenster_ring_zeit.geojson', True, True)

.. jupyter-execute::
   :hide-code:
   :hide-output:

   # (2) Remove downloaded showcase file
   subprocess.run(["rm", "-rf", "showcase_geojson"])
   


**Example 2:** Extracting geoextent from Tabular data (.csv):

The file used in the example obtianed from `here <https://sandbox.zenodo.org/record/256820#.XeGcJJko85k>`_ 
::

   geoextent -b -t -input= 'cities_NL.csv'

output

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent
   import subprocess

   # (1) Download showcase file and extract geoextent data
   subprocess.run('mkdir showcase_csv', shell=True)
   subprocess.run('wget -P showcase_csv https://sandbox.zenodo.org/record/256820/files/cities_NL.csv', shell=True)

   geoextent.fromFile('showcase_csv/cities_NL.csv', True, True)

.. jupyter-execute::
   :hide-code:
   :hide-output:

   # (2) Remove downloaded showcase file
   subprocess.run(["rm", "-rf", "showcase_csv"])  #Hello



**Example 3:** Extracting geoextent from a GeoTIFF file:

The file used in the example obtianed from `here <https://github.com/o2r-project/geoextent/blob/master/tests/testdata/tif/wf_100m_klas.tif>`_ 
::

   geoextent -b -input= 'wf_100m_klas.tif'

output

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent
   import subprocess

   # (1) Download showcase file and extract geoextent data
   subprocess.run('mkdir showcase_geotiff', shell=True)
   subprocess.run('wget -P showcase_geotiff https://github.com/o2r-project/geoextent/raw/master/tests/testdata/tif/wf_100m_klas.tif', shell=True)

   geoextent.fromFile('showcase_geotiff/wf_100m_klas.tif', True, False)

.. jupyter-execute::
   :hide-code:
   :hide-output:

   # (2) Remove downloaded showcase file
   subprocess.run(["rm", "-rf", "showcase_geotiff"]
   


**Example 4:** Extracting geoextent from a shapefile:

The file used in the example obtianed from `here <https://www.geofabrik.de/data/shapefiles_toulouse.zip>`_ 
::

   geoextent 'gis_osm_buildings_a_07_1.shp'

output

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent
   import subprocess

   # (1) Download showcase file and extract geoextent data
   subprocess.run('mkdir showcase_shp', shell=True)
   subprocess.run('wget -P showcase_shp https://www.geofabrik.de/data/shapefiles_toulouse.zip', shell=True)
   subprocess.run('cd showcase_shp; unzip shapefiles_toulouse.zip', shell=True)

   geoextent.fromFile('showcase_shp/gis_osm_buildings_a_07_1.shp', True, False)

.. jupyter-execute::
   :hide-code:
   :hide-output:

   # (2) Remove downloaded showcase file
   subprocess.run(["rm", "-rf", "showcase_shp"]