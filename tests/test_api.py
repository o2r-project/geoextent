import os         # used to get the location of the testdata
import sys
import pytest
import geoextent.lib.extent as geoextent
import geoextent.__main__ as geoextent_main

###############
# --detail=bbox
###############

def test_netcdf_extract_bbox():
    assert geoextent.fromFile("/testdata/nc/ECMWF_ERA-40_subset.nc", 'b') == [-90.0, 0.0, 90.0, 357.5]

def test_kml_extract_bbox():
    assert geoextent.fromFile("/testdata/kml/aasee.kml", 'b') == [7.594213, 51.942466, 7.618246, 51.957278]

def test_gpkg_extract_bbox():
    assert geoextent.fromFile("/testdata/nc/nc.gpkg", 'b') == [33.882, -84.3239, 36.5896, -75.457]

def test_gml_extract_bbox():
    assert geoextent.fromFile("/testdata/gml/clc_1000_PT.gml", 'b') == [-17.5420724159224, 32.3966928193202, -6.95938792923511, 39.3011352746141]

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
    assert geoextent.fromFile("/testdata/nc/ECMWF_ERA-40_subset.nc", 't') == ['2002-07-01','2002-07-31']

def test_gml_extract_time():
    assert geoextent.fromFile("/testdata/gml/clc_1000_PT.gml", 't') == ['2013-11-30T23:00:00Z', '2013-11-30T23:00:00Z']


######################
# --detail=bbox & time
######################

def test_netcdf_extract_bbox_time():
    assert geoextent.fromFile("/testdata/nc/ECMWF_ERA-40_subset.nc", 'bt') == [[-90.0, 0.0, 90.0, 357.5],['2002-07-01','2002-07-31']]

def test_kml_extract_bbox_time():
    assert geoextent.fromFile("/testdata/kml/aasee.kml", 'bt') == [[7.594213, 51.942466, 7.618246, 51.957278],[None]]

def test_gpkg_extract_bbox_time():
    assert geoextent.fromFile("/testdata/nc/nc.gpkg", 'bt') == [[33.882, -84.3239, 36.5896, -75.457],[None]]

def test_gml_extract_bbox_time():
    assert geoextent.fromFile("/testdata/gml/clc_1000_PT.gml", 'bt') == [[-17.5420724159224, 32.3966928193202, -6.95938792923511, 39.3011352746141],['2013-11-30T23:00:00Z', '2013-11-30T23:00:00Z']]

def test_json_extract_bbox_time():
    assert geoextent.fromFile("/testdata/folder/schutzhuetten_aachen.json", 'bt') == [[292063.81225905, 5618144.09259115, 302531.3161606, 5631223.82854667],[None]]

def test_folder_multiple_files():
    assert [7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454] in geoextent.fromFile('/testdata/folder', 'bt')
    assert [6.574722, 51.434444, 4.3175, 53.217222] in geoextent.fromFile('/testdata/folder', 'b')
    assert [292063.81225905, 5618144.09259115, 302531.3161606, 5631223.82854667] not in geoextent.fromFile('/testdata/folder', 't')


######################
# --file handling
######################

def test_not_found_file():
    with pytest.raises(Exception) as excinfo:
        geoextent.fromFile('testdata/empt.geojson', 'b')
    assert "The file is not valid" in str(excinfo.value)

def test_not_suppotred_file_format():
    with pytest.raises(Exception) as excinfo:
        geoextent_main.getOutput('testdata/geojson/empty.geo', 'b') 
    assert "This file format is not supported" in str(excinfo.value)
