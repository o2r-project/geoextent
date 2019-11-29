import os         # used to get the location of the testdata
import sys
import pytest
import geoextent.lib.extent as geoextent
<<<<<<< HEAD
import geoextent.__main__ as geoextent_main
=======
>>>>>>> 3a5f99d0a44035230fff7cd40075ba16e3298159

###############
# --detail=bbox
###############

<<<<<<< HEAD
=======
def test_csv_extract_bbox():
    #assert extent.fromFile("/testdata/folder/cities_NL.csv", 'bbox') == [6.574722, 51.434444, 4.3175, 53.217222]
    result = geoextent.fromFile('testdata/cities_NL_lat&long.csv', 'b')
    assert result["bbox"] == [4.3175, 51.434444, 6.574722, 53.217222]

def test_empty_csv_file_extract_bbox():
    with pytest.raises(Exception) as excinfo:
        geoextent.fromFile('testdata/empty_csv.csv', 'b')
    assert "The file is empty" in str(excinfo.value)

>>>>>>> 3a5f99d0a44035230fff7cd40075ba16e3298159
def test_netcdf_extract_bbox():
    assert geoextent.fromFile("/testdata/ECMWF_ERA-40_subset1.nc", 'b') == [-90.0, 0.0, 90.0, 357.5]

def test_kml_extract_bbox():
    assert geoextent.fromFile("/testdata/aasee.kml", 'b') == [7.594213, 51.942466, 7.618246, 51.957278]

<<<<<<< HEAD
=======
def test_geotiff_extract_bbox():
    assert geoextent.fromFile("/testdata/wf_100m_klas.tif", 'b') == [5.9153007564753155, 50.31025197410836, 9.468398712484145, 52.5307755328733]

>>>>>>> 3a5f99d0a44035230fff7cd40075ba16e3298159
def test_gpkg_extract_bbox():
    assert geoextent.fromFile("/testdata/nc.gpkg", 'b') == [33.882, -84.3239, 36.5896, -75.457]

def test_gml_extract_bbox():
    assert geoextent.fromFile("/testdata/clc_1000_PT.gml", 'b') == [-17.5420724159224, 32.3966928193202, -6.95938792923511, 39.3011352746141]

<<<<<<< HEAD
=======
def test_shapefile_extract_bbox():
    assert geoextent.fromFile("/testdata/Abgrabungen_Kreis_Kleve_Shape.shp", 'b') == [295896.274870878, 5694747.64703736, 325999.79578122497, 5747140.98659967]

>>>>>>> 3a5f99d0a44035230fff7cd40075ba16e3298159
def test_json_extract_bbox():
    assert geoextent.fromFile("/testdata/folder/schutzhuetten_aachen.json", 'b') == [292063.81225905, 5618144.09259115, 302531.3161606, 5631223.82854667]

def test_folder_multiple_files():
    assert [7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454] in geoextent.fromFile('testdata/folder/', 'b')
    assert [6.574722, 51.434444, 4.3175, 53.217222] in geoextent.fromFile('testdata/folder', 'b')
    assert [292063.81225905, 5618144.09259115, 302531.3161606, 5631223.82854667] in geoextent.fromFile('testdata/folder', 'b')


###############
# --detail=time
###############

def test_netcdf_extract_time():
    assert geoextent.fromFile("/testdata/ECMWF_ERA-40_subset1.nc", 't') == ['2002-07-01','2002-07-31']

<<<<<<< HEAD
=======
def test_csv_extract_time():
    assert geoextent.fromFile("/testdata/folder/cities_NL.csv", 't') == ['2018-09-30', '2018-09-30']

>>>>>>> 3a5f99d0a44035230fff7cd40075ba16e3298159
def test_gml_extract_time():
    assert geoextent.fromFile("/testdata/clc_1000_PT.gml", 't') == ['2013-11-30T23:00:00Z', '2013-11-30T23:00:00Z']


######################
# --detail=bbox & time
######################

def test_netcdf_extract_bbox_time():
    assert geoextent.fromFile("/testdata/ECMWF_ERA-40_subset1.nc", 'bt') == [[-90.0, 0.0, 90.0, 357.5],['2002-07-01','2002-07-31']]

def test_kml_extract_bbox_time():
    assert geoextent.fromFile("/testdata/aasee.kml", 'bt') == [[7.594213, 51.942466, 7.618246, 51.957278],[None]]

<<<<<<< HEAD
def test_gpkg_extract_bbox_time():
    assert geoextent.fromFile("/testdata/nc.gpkg", 'bt') == [[33.882, -84.3239, 36.5896, -75.457],[None]]

def test_gml_extract_bbox_time():
    assert geoextent.fromFile("/testdata/clc_1000_PT.gml", 'bt') == [[-17.5420724159224, 32.3966928193202, -6.95938792923511, 39.3011352746141],['2013-11-30T23:00:00Z', '2013-11-30T23:00:00Z']]

=======
def test_geotiff_extract_bbox_time():
    assert geoextent.fromFile("/testdata/wf_100m_klas.tif", 'bt') == [[5.9153007564753155, 50.31025197410836, 9.468398712484145, 52.5307755328733],[None]]

def test_gpkg_extract_bbox_time():
    assert geoextent.fromFile("/testdata/nc.gpkg", 'bt') == [[33.882, -84.3239, 36.5896, -75.457],[None]]

def test_csv_extract_bbox_time():
    assert geoextent.fromFile("/testdata/folder/cities_NL.csv", 'bt') == [[6.574722, 51.434444, 4.3175, 53.217222],['2018-09-30', '2018-09-30']]

def test_gml_extract_bbox_time():
    assert geoextent.fromFile("/testdata/clc_1000_PT.gml", 'bt') == [[-17.5420724159224, 32.3966928193202, -6.95938792923511, 39.3011352746141],['2013-11-30T23:00:00Z', '2013-11-30T23:00:00Z']]

def test_shapefile_extract_bbox_time():
    assert geoextent.fromFile("/testdata/Abgrabungen_Kreis_Kleve_Shape.shp", 'bt') == [[295896.274870878, 5694747.64703736, 325999.79578122497, 5747140.98659967],[None]]

>>>>>>> 3a5f99d0a44035230fff7cd40075ba16e3298159
def test_json_extract_bbox_time():
    assert geoextent.fromFile("/testdata/folder/schutzhuetten_aachen.json", 'bt') == [[292063.81225905, 5618144.09259115, 302531.3161606, 5631223.82854667],[None]]

def test_folder_multiple_files():
    assert [7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454] in geoextent.fromFile('/testdata/folder', 'bt')
    assert [6.574722, 51.434444, 4.3175, 53.217222] in geoextent.fromFile('/testdata/folder', 'b')
    assert [292063.81225905, 5618144.09259115, 302531.3161606, 5631223.82854667] not in geoextent.fromFile('/testdata/folder', 't')
<<<<<<< HEAD


######################
# --file handling
######################

def test_not_found_file():
    with pytest.raises(Exception) as excinfo:
        geoextent.fromFile('testdata/empt.geojson', 'b')
    assert "The file is not valid" in str(excinfo.value)

def test_not_suppotred_file_format():
    with pytest.raises(Exception) as excinfo:
        geoextent_main.getOutput('testdata/empty.geo', 'b') 
    assert "This file format is not supported" in str(excinfo.value)
=======
>>>>>>> 3a5f99d0a44035230fff7cd40075ba16e3298159
