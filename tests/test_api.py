import os         # used to get the location of the testdata
import sys
import pytest
import geoextent.lib.extent as geoextent
import geoextent.__main__ as geoextent_main

@pytest.mark.skip(reason="file format not implemented yet")
def test_defaults():
    result = geoextent.fromFile("tests/testdata/nc/ECMWF_ERA-40_subset.nc")
    assert "bbox" in result
    assert "temporal_extent" in result
    assert "crs" in result

    result = geoextent.fromFile("tests/testdata/nc/ECMWF_ERA-40_subset.nc", bbox=False)
    assert "bbox" not in result
    assert "temporal_extent" in result
    assert "crs" not in result
    
    result = geoextent.fromFile("tests/testdata/nc/ECMWF_ERA-40_subset.nc", tbox=False)
    assert "bbox" not in result
    assert "temporal_extent" not in result
    assert "crs" not in result

@pytest.mark.skip(reason="file format not implemented yet")
def test_netcdf_extract_bbox():
    assert geoextent.fromFile("tests/testdata/nc/ECMWF_ERA-40_subset.nc") == [-90.0, 0.0, 90.0, 357.5]

@pytest.mark.skip(reason="file format not implemented yet")
def test_kml_extract_bbox():
    assert geoextent.fromFile("tests/testdata/kml/aasee.kml", bbox=True) == [7.594213, 51.942466, 7.618246, 51.957278]

@pytest.mark.skip(reason="file format not implemented yet")
def test_gpkg_extract_bbox():
    assert geoextent.fromFile("tests/testdata/nc/nc.gpkg", bbox=True) == [33.882, -84.3239, 36.5896, -75.457]

@pytest.mark.skip(reason="file format not implemented yet")
def test_gml_extract_bbox():
    assert geoextent.fromFile("tests/testdata/gml/clc_1000_PT.gml", bbox=True) == [-17.5420724159224, 32.3966928193202, -6.95938792923511, 39.3011352746141]

@pytest.mark.skip(reason="file format not implemented yet")
def test_folder_multiple_files():
    assert [7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454] in geoextent.fromFile('tests/testdata/folder/', bbox=True)
    assert [6.574722, 51.434444, 4.3175, 53.217222] in geoextent.fromFile('tests/testdata/folder', bbox=True)
    assert [292063.81225905, 5618144.09259115, 302531.3161606, 5631223.82854667] in geoextent.fromFile('tests/testdata/folder', bbox=True)


@pytest.mark.skip(reason="file format not implemented yet")
def test_netcdf_extract_time():
    assert geoextent.fromFile("tests/testdata/nc/ECMWF_ERA-40_subset.nc", tbox=True) == ['2002-07-01','2002-07-31']

@pytest.mark.skip(reason="file format not implemented yet")
def test_gml_extract_time():
    assert geoextent.fromFile("tests/testdata/gml/clc_1000_PT.gml", tbox=True) == ['2013-11-30T23:00:00Z', '2013-11-30T23:00:00Z']

@pytest.mark.skip(reason="file format not implemented yet")
def test_netcdf_extract_bbox_time():
    assert geoextent.fromFile("tests/testdata/nc/ECMWF_ERA-40_subset.nc", bbox=True, tbox=True) == [[-90.0, 0.0, 90.0, 357.5],['2002-07-01','2002-07-31']]

@pytest.mark.skip(reason="file format not implemented yet")
def test_kml_extract_bbox_time():
    assert geoextent.fromFile("tests/testdata/kml/aasee.kml", bbox=True, tbox=True) == [[7.594213, 51.942466, 7.618246, 51.957278],[None]]

@pytest.mark.skip(reason="file format not implemented yet")
def test_gpkg_extract_bbox_time():
    assert geoextent.fromFile("tests/testdata/nc/nc.gpkg", bbox=True, tbox=True) == [[33.882, -84.3239, 36.5896, -75.457],[None]]

@pytest.mark.skip(reason="file format not implemented yet")
def test_gml_extract_bbox_time():
    assert geoextent.fromFile("tests/testdata/gml/clc_1000_PT.gml", bbox=True, tbox=True) == [[-17.5420724159224, 32.3966928193202, -6.95938792923511, 39.3011352746141],['2013-11-30T23:00:00Z', '2013-11-30T23:00:00Z']]

@pytest.mark.skip(reason="file format not implemented yet")
def test_folder_multiple_files():
    assert [7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454] in geoextent.fromFile('/testdata/folder', bbox=True, tbox=True)
    assert [6.574722, 51.434444, 4.3175, 53.217222] in geoextent.fromFile('/testdata/folder', bbox=True)
    assert [292063.81225905, 5618144.09259115, 302531.3161606, 5631223.82854667] not in geoextent.fromFile('/testdata/folder', tbox=True)


def test_not_found_file():
    with pytest.raises(Exception) as excinfo:
        geoextent.fromFile('tests/testdata/empt.geojson', bbox=True)
    assert "No such file or directory" in str(excinfo.value)

def test_not_supported_file_format():
    result = geoextent.fromFile('tests/testdata/geojson/empty.geo', bbox=True) 
    assert result == None