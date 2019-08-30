import os           # used to get the location of the testdata
import pygeoj       # used to parse the geojson file
import shapefile 
import xarray as xr

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

###############################
# Check file existence
###############################
def test_geojson_file_exist():
    filepath=__location__+"/Testdata/muenster_ring_zeit.geojson"
    assert os.path.isfile(filepath) == True

def test_nc_file_exist():
    filepath=__location__+"/Testdata/ECMWF_ERA-40_subset1.nc"
    assert os.path.isfile(filepath) == True

def test_kml_file_exist():
    filepath=__location__+"/Testdata/aasee.kml"
    assert os.path.isfile(filepath) == True

def test_tif_file_exist():
    filepath=__location__+"/Testdata/wf_100m_klas.tif"
    assert os.path.isfile(filepath) == True

def test_gpkg_file_exist():
    filepath=__location__+"/Testdata/nc.gpkg"
    assert os.path.isfile(filepath) == True

def test_csv_file_exist():
    filepath=__location__+"/Testdata/cities_NL.csv"
    assert os.path.isfile(filepath) == True

def test_gml_file_exist():
    filepath=__location__+"/Testdata/clc_1000_PT.gml"
    assert os.path.isfile(filepath) == True

def test_shp_file_exist():
    filepath=__location__+"/Testdata/Abgrabungen_Kreis_Kleve_Shape.shp"
    assert os.path.isfile(filepath) == True

def test_dbf_file_exist():
    filepath=__location__+"/Testdata/Abgrabungen_Kreis_Kleve_Shape.dbf"
    assert os.path.isfile(filepath) == True

###############################
# Check bbox extraction
###############################
def test_geojson_extract_bbox():
    filepath=__location__+"/Testdata/muenster_ring_zeit.geojson"
    geojson = pygeoj.load(filepath)
    bbox = (geojson).bbox
    assert bbox == [7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454]

def test_invalid_coordinate_geojson_extract_bbox():
    filepath=__location__+"/Testdata/invalid_coordinate.geojson"
    captured = capsys.readouterr()
    assert captured.out == "Invalid geojson file"

def test_one_point_geojson_extract_bbox():
    filepath=__location__+"/Testdata/onePoint.geojson"
    geojson = pygeoj.load(filepath)
    bbox = (geojson).bbox
    assert bbox == [6.220493316650391, 50.52150360276628, 6.220493316650391, 50.52150360276628]

def test_empty_file_geojson_extract_bbox(capsys):
    filepath=__location__+"/Testdata/empty.geojson"
    captured = capsys.readouterr()
    assert captured.out == "Empty file"

def test_nc_extract_bbox():
    filepath=__location__+"/Testdata/ECMWF_ERA-40_subset1.nc"
    assert netcdf_bbox(filepath) == [0.0, -90.0, 357.5, 90.0]

def test_shapefile_extract_bbox():
    filepath=__location__+"/Testdata/Abgrabungen_Kreis_Kleve_Shape.shp"
    sf = shapefile.Reader(filepath)
    output = sf.bbox
    print(output)
    assert output == [295896.274870878, 5694747.64703736, 325999.79578122497, 5747140.98659967]

###############################
# Functions
###############################
"""
Function for extracting the bbox of netcdf file

:param filepath: path to the file
:returns: bounding box of the netCDF in the format [minlon, minlat, maxlon, maxlat]
"""
def netcdf_bbox(filepath):
    ds = xr.open_dataset(filepath)
    try:
        lats = ds.coords["lat"]
        lons = ds.coords["lon"]
    except Exception as e:
        try:
            lats = ds.coords["latitude"]
            lons = ds.coords["longitude"]
        except Exception as e:
            click.echo(e)

    min_lat=min(lats).values
    min_lat_float=float(min_lat)
    min_lon=min(lons).values
    min_lon_float=float(min_lon)
    max_lat=max(lats).values
    max_lat_float=float(max_lat)
    max_lon=max(lons).values
    max_lon_float=float(max_lon)

    bbox = [min_lon_float,min_lat_float,max_lon_float,max_lat_float]
    ds.close()
    return bbox