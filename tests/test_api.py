import os  # used to get the location of the testdata
import tempfile
import pytest
import geoextent.lib.extent as geoextent
from help_functions_test import create_zip
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
    assert geoextent.fromFile("tests/testdata/gml/clc_1000_PT.gml", bbox=True) == [-17.5420724159224, 32.3966928193202,
                                                                                   -6.95938792923511, 39.3011352746141]

def test_empty_folder():

    with tempfile.TemporaryDirectory() as temp:
        result = geoextent.fromDirectory(temp, bbox=True, tbox=True)
        assert "bbox" not in result
        assert "tbox" not in result

def test_folder_one_file():
    result = geoextent.fromDirectory('tests/testdata/folders/folder_one_file', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == [7.60168075561523, 51.9488147720619, 7.64725685119629, 51.9746240298775]
    assert result["tbox"] == ['2018-11-14', '2018-11-14']

def test_folder_multiple_files():
    result = geoextent.fromDirectory('tests/testdata/folders/folder_two_files', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == [2.05233338763921, 41.3170385224048, 7.64725685119629, 51.9746240298775]
    assert result["tbox"] == ['2018-11-14', '2019-09-11']

def test_folder_nested_files():
    result = geoextent.fromDirectory('tests/testdata/folders/nested_folder', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == [7.60168075561523, 34.7, 142.0, 51.9746240298775]
    assert result["tbox"] == ['2017-04-08', '2020-02-06']

def test_zipfile_unsupported_file():
    with tempfile.TemporaryDirectory() as tmp_dir:
        f = open(tmp_dir + "/unsupported_file.txt", "a")
        f.write("No geographical data")
        f.close()
        with tempfile.NamedTemporaryFile(suffix=".zip") as tmp:
            create_zip(tmp_dir, tmp)
            result = geoextent.fromDirectory(tmp.name, bbox=True, tbox=True)
            assert "bbox" not in result
            assert "tbox" not in result

def test_zipfile_one_file():
    folder_name = "tests/testdata/folders/folder_one_file"
    with tempfile.NamedTemporaryFile(suffix=".zip") as tmp:
        create_zip(folder_name,tmp)
        result = geoextent.fromDirectory(tmp.name, bbox=True, tbox=True)
        assert result["bbox"] == [7.60168075561523, 51.9488147720619, 7.64725685119629, 51.9746240298775]
        assert result["tbox"] == ['2018-11-14', '2018-11-14']

def test_zipfile_nested_folders():
    folder_name = "tests/testdata/folders/nested_folder"
    with tempfile.NamedTemporaryFile(suffix=".zip") as tmp:
        create_zip(folder_name,tmp)
        result = geoextent.fromDirectory(tmp.name, bbox=True, tbox=True)
        assert result["bbox"] == [7.60168075561523, 34.7, 142.0, 51.9746240298775]
        assert result["tbox"] == ['2017-04-08', '2020-02-06']

@pytest.mark.skip(reason="file format not implemented yet")
def test_netcdf_extract_time():
    assert geoextent.fromFile("tests/testdata/nc/ECMWF_ERA-40_subset.nc", tbox=True) == ['2002-07-01', '2002-07-31']

@pytest.mark.skip(reason="file format not implemented yet")
def test_gml_extract_time():
    assert geoextent.fromFile("tests/testdata/gml/clc_1000_PT.gml", tbox=True) == ['2013-11-30T23:00:00Z',
                                                                                   '2013-11-30T23:00:00Z']
@pytest.mark.skip(reason="file format not implemented yet")
def test_netcdf_extract_bbox_time():
    assert geoextent.fromFile("tests/testdata/nc/ECMWF_ERA-40_subset.nc", bbox=True, tbox=True) == [
        [-90.0, 0.0, 90.0, 357.5], ['2002-07-01', '2002-07-31']]

@pytest.mark.skip(reason="file format not implemented yet")
def test_kml_extract_bbox_time():
    assert geoextent.fromFile("tests/testdata/kml/aasee.kml", bbox=True, tbox=True) == [
        [7.594213, 51.942466, 7.618246, 51.957278], [None]]


@pytest.mark.skip(reason="file format not implemented yet")
def test_gpkg_extract_bbox_time():
    assert geoextent.fromFile("tests/testdata/nc/nc.gpkg", bbox=True, tbox=True) == [
        [33.882, -84.3239, 36.5896, -75.457], [None]]

@pytest.mark.skip(reason="file format not implemented yet")
def test_gml_extract_bbox_time():
    assert geoextent.fromFile("tests/testdata/gml/clc_1000_PT.gml", bbox=True, tbox=True) == [
        [-17.5420724159224, 32.3966928193202, -6.95938792923511, 39.3011352746141],
        ['2013-11-30T23:00:00Z', '2013-11-30T23:00:00Z']]

def test_not_found_file():
    with pytest.raises(Exception) as excinfo:
        geoextent.fromFile('tests/testdata/empt.geojson', bbox=True)
    assert "No such file or directory" in str(excinfo.value)

def test_not_supported_file_format():
    result = geoextent.fromFile('tests/testdata/geojson/empty.geo', bbox=True)
    assert result == None

def test_bbox_and_tbox_both_false():
    with pytest.raises(Exception) as excinfo:
        geoextent.fromFile('tests/path_does_not_matter', bbox=False, tbox=False)
    assert "No extraction options" in str(excinfo.value)
