import geoextent.__main__ as geoextent
geoextent.print_supported_formats()

def get_showcase_file(folder_name, url, unzip_file = None):
   import subprocess

   # Download showcase file and extract geoextent data
   subprocess.run('mkdir -p showcase_folder', shell=True)
   subprocess.run('wget -P showcase_folder '+ url, shell=True)

   if unzip_file:
      subprocess.run('cd showcase_folder; unzip '+ unzip_file, shell=True)

import geoextent.lib.extent as geoextent

dir_name = 'showcase_geojson'
file_url = 'https://raw.githubusercontent.com/o2r-project/geoextent/master/tests/testdata/geojson/muenster_ring_zeit.geojson'
get_showcase_file(dir_name, file_url)

geoextent.fromFile('showcase_folder/muenster_ring_zeit.geojson', True, True)

import geoextent.lib.extent as geoextent

dir_name = 'showcase_csv'
file_url = 'https://sandbox.zenodo.org/record/256820/files/cities_NL.csv'
get_showcase_file(dir_name, file_url)

geoextent.fromFile('showcase_folder/cities_NL.csv', True, True)

import geoextent.lib.extent as geoextent

dir_name = 'showcase_geotiff'
file_url = 'https://github.com/o2r-project/geoextent/raw/master/tests/testdata/tif/wf_100m_klas.tif'
get_showcase_file(dir_name, file_url)

geoextent.fromFile('showcase_folder/wf_100m_klas.tif', True, False)

import geoextent.lib.extent as geoextent

dir_name = 'showcase_shp'
file_url = 'https://www.geofabrik.de/data/shapefiles_toulouse.zip'
get_showcase_file(dir_name, file_url, 'shapefiles_toulouse.zip')

geoextent.fromFile('showcase_folder/gis_osm_buildings_a_07_1.shp', True, False)

import subprocess
# (2) Remove downloaded showcase files
subprocess.run(["rm", "-rf", "showcase_folder"])