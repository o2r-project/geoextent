======================
Supported file formats
======================

The library supports the following file formats.
Please see the `project issues <https://github.com/o2r-project/geoextent/issues>`_ for upcoming formats and feature requests.

.. jupyter-execute::
   :hide-code:

   import geoextent.__main__ as geoextent
   geoextent.print_supported_formats()

.. jupyter-execute::
   :hide-code:

   def get_showcase_file(folder_name, url, unzip_file = None):
      import subprocess

      # Download showcase file and extract geoextent data
      subprocess.run('mkdir -p showcase_folder', shell=True)
      subprocess.run('wget -q --show-progress --progress=bar:force -P showcase_folder '+ url, shell=True)

      if unzip_file:
         subprocess.run('cd showcase_folder; unzip '+ unzip_file, shell=True)

------

Examples
--------

GeoJSON
^^^^^^^

The file used in the example can be in the code repository: `muenster_ring_zeit.geojson <https://raw.githubusercontent.com/o2r-project/geoextent/master/tests/testdata/geojson/muenster_ring_zeit.geojson>`_.

::

   geoextent -b -t muenster_ring_zeit.geojson

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent

   dir_name = 'showcase_geojson'
   file_url = 'https://raw.githubusercontent.com/o2r-project/geoextent/master/tests/testdata/geojson/muenster_ring_zeit.geojson'
   get_showcase_file(dir_name, file_url)

   geoextent.fromFile('showcase_folder/muenster_ring_zeit.geojson', True, True)

CSV
^^^

Different CSV delimiters (``;``, ``,``) are automatically detected.
Supported column names, by using `Regular expressions operations <https://docs.python.org/3/library/re.html>`_, are as follows:

- Latitude
  - ``(.)*latitude(.)*``
  - ``^lat``
  - ``lat$``
  - ``^y``
  - ``y$``

- Longitude
  - ``(.)*longitude"``
  - ``(.)*long(.)``
  - ``^lon``
  - ``lon$``
  - ``(.)*lng(.)*``
  - ``^x``
  - ``x$``
- Time
  - ``(.)*timestamp(.)*``
  - ``(.)*datetime(.)*``
  - ``(.)*time(.)*``
  - ``^date``
  - ``date$``


The file used in the example can be obtained from `Zenodo Sandbox record 256820 <https://sandbox.zenodo.org/record/256820#.XeGcJJko85k>`_.

::

   geoextent -b -t cities_NL.csv

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent

   dir_name = 'showcase_csv'
   file_url = 'https://sandbox.zenodo.org/record/256820/files/cities_NL.csv'
   get_showcase_file(dir_name, file_url)

   geoextent.fromFile('showcase_folder/cities_NL.csv', True, True)

GeoTIFF
^^^^^^^

The file used in the example is available online: `wf_100m_klas.tif <https://github.com/o2r-project/geoextent/blob/master/tests/testdata/tif/wf_100m_klas.tif>`_.

::

   geoextent -b wf_100m_klas.tif

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent

   dir_name = 'showcase_geotiff'
   file_url = 'https://github.com/o2r-project/geoextent/raw/master/tests/testdata/tif/wf_100m_klas.tif'
   get_showcase_file(dir_name, file_url)

   geoextent.fromFile('showcase_folder/wf_100m_klas.tif', True, False)

Shapefile
^^^^^^^^^

The file used in the example can be found at Geofabrik: `shapefiles_toulouse.zip <https://www.geofabrik.de/data/shapefiles_toulouse.zip>`_.

::

   geoextent -b gis_osm_buildings_a_07_1.shp

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent

   dir_name = 'showcase_shp'
   file_url = 'https://www.geofabrik.de/data/shapefiles_toulouse.zip'
   get_showcase_file(dir_name, file_url, 'shapefiles_toulouse.zip')

   geoextent.fromFile('showcase_folder/gis_osm_buildings_a_07_1.shp', True, False)

GeoPackage
^^^^^^^^^^

The file used in the example is available online: `sample1_2.gpkg <http://www.geopackage.org/guide/implementation_guide.html#_level_1_4>`_.

::

   geoextent -b sample1_2.gpkg

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent

   dir_name = 'showcase_geopackage'
   file_url = 'http://www.geopackage.org/data/sample1_2.gpkg'
   get_showcase_file(dir_name, file_url)
   geoextent.fromFile('showcase_folder/sample1_2.gpkg', True, False)

GPS Exchange Format
^^^^^^^^^^^^^^^^^^^

The file used in the example is available online: `run.gpx <https://docs.mapbox.com/help/data/run.gpx>`_.

::

   geoextent -b run.gpx

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent

   dir_name = 'showcase_gpx'
   file_url = 'https://docs.mapbox.com/help/data/run.gpx'
   get_showcase_file(dir_name, file_url)
   geoextent.fromFile('showcase_folder/run.gpx', True, False)

Geography Markup Language
^^^^^^^^^^^^^^^^^^^^^^^^^

The file used in the example is available online: `clc_1000_PT.gml <https://github.com/o2r-project/geoextent/blob/master/tests/testdata/gml/clc_1000_PT.gml>`_.

::

   geoextent -b clc_1000_PT.gml

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent

   dir_name = 'showcase_gml'
   file_url = 'https://raw.githubusercontent.com/o2r-project/geoextent/master/tests/testdata/gml/clc_1000_PT.gml'
   get_showcase_file(dir_name, file_url)
   geoextent.fromFile('showcase_folder/clc_1000_PT.gml', True, False)

Keyhole Markup Language
^^^^^^^^^^^^^^^^^^^^^^^

The file used in the example is available online: `KML_Samples.kml <https://developers.google.com/kml/documentation/KML_Samples.kml>`_.

::

   geoextent -b KML_Samples.kml

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent

   dir_name = 'showcase_kml'
   file_url = 'https://developers.google.com/kml/documentation/KML_Samples.kml'
   get_showcase_file(dir_name, file_url)
   geoextent.fromFile('showcase_folder/KML_Samples.kml', True, False)


.. jupyter-execute::
   :hide-code:
   :hide-output:

   import subprocess
   # (2) Remove downloaded showcase files
   subprocess.run(["rm", "-rf", "showcase_folder"])