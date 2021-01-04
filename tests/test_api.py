import os  # used to get the location of the testdata
import sys
import tempfile
import pytest
import geoextent.lib.extent as geoextent
from help_functions_test import create_zip, tolerance


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


def test_kml_extract_bbox():
    result = geoextent.fromFile("tests/testdata/kml/aasee.kml", bbox=True)
    assert "bbox" in result
    assert "crs" in result
    assert result["bbox"] == pytest.approx([7.594213, 51.942465, 7.618246, 51.957278], abs=tolerance)
    assert result["crs"] == "4326"


def test_kml_extract_tbox():
    result = geoextent.fromFile("tests/testdata/kml/TimeStamp_example.kml", bbox=True)
    assert "tbox" in result
    assert result["tbox"] == ['2007-01-14', '2007-01-14']


def test_gpkg_extract_bbox():
    result = geoextent.fromFile("tests/testdata/nc/nc.gpkg", bbox=True)
    assert "bbox" in result
    assert "crs" in result
    assert result['bbox'] == pytest.approx([-84.323835, 33.882102, -75.456585, 36.589757], abs=tolerance)
    assert result["crs"] == "4326"


@pytest.mark.skipif("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
                    reason="Travis GDAL version outdated")
def test_gml_extract_bbox():
    result = geoextent.fromFile("tests/testdata/gml/clc_1000_PT.gml", bbox=True)
    assert "bbox" in result
    assert "crs" in result
    assert result["bbox"] == pytest.approx([-17.542069, 32.39669, -6.959389, 39.301139], abs=tolerance)
    assert result["crs"] == "4326"


def test_gpx_extract_bbox():
    result = geoextent.fromFile("tests/testdata/gpx/gpx1.1_with_all_fields.gpx", bbox=True)
    assert "bbox" in result
    assert "crs" in result
    assert result["bbox"] == pytest.approx([-20.2, 10.0, 46.7, 14.0], abs=tolerance)
    assert result["crs"] == "4326"


def test_gpx_extract_tbox():
    result = geoextent.fromFile("tests/testdata/gpx/gpx1.1_with_all_fields.gpx", tbox=True)
    assert "tbox" in result
    assert result["tbox"] == ['2013-01-01', '2013-01-01']


@pytest.mark.skipif(sys.platform == "darwin", reason="MacOS recognize file")
def test_gpx_format_error_file():
    result = geoextent.fromFile("tests/testdata/gpx/gpx1.1_with_all_fields_error_format.gpx", tbox=True)
    assert result is None


def test_empty_folder():
    with tempfile.TemporaryDirectory() as temp:
        result = geoextent.fromDirectory(temp, bbox=True, tbox=True)
        assert "bbox" not in result
        assert "tbox" not in result


def test_folder_one_file():
    result = geoextent.fromDirectory('tests/testdata/folders/folder_one_file', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert "crs" in result
    assert result["bbox"] == pytest.approx([7.601680, 51.948814, 7.647256, 51.974624], abs=tolerance)
    assert result["crs"] == "4326"
    assert result["tbox"] == ['2018-11-14', '2018-11-14']


def test_folder_multiple_files():
    result = geoextent.fromDirectory('tests/testdata/folders/folder_two_files', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert "crs" in result
    assert result["bbox"] == pytest.approx([2.052333, 41.317038, 7.647256, 51.974624], abs=tolerance)
    assert result["crs"] == "4326"
    assert result["tbox"] == ['2018-11-14', '2019-09-11']


def test_folder_nested_files():
    result = geoextent.fromDirectory('tests/testdata/folders/nested_folder', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert "crs" in result
    assert result["bbox"] == pytest.approx([7.601680, 34.7, 142.0, 51.974624], abs=tolerance)
    assert result["crs"] == "4326"
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
        create_zip(folder_name, tmp)
        result = geoextent.fromDirectory(tmp.name, bbox=True, tbox=True)
        assert result["bbox"] == pytest.approx([7.601680, 51.948814, 7.647256, 51.974624], abs=tolerance)
        assert result["crs"] == "4326"
        assert result["tbox"] == ['2018-11-14', '2018-11-14']


def test_zipfile_nested_folders():
    folder_name = "tests/testdata/folders/nested_folder"
    with tempfile.NamedTemporaryFile(suffix=".zip") as tmp:
        create_zip(folder_name, tmp)
        result = geoextent.fromDirectory(tmp.name, bbox=True, tbox=True)
        assert result["bbox"] == pytest.approx([7.601680, 34.7, 142.0, 51.974624], abs=tolerance)
        assert result["crs"] == "4326"
        assert result["tbox"] == ['2017-04-08', '2020-02-06']


@pytest.mark.skip(reason="file format not implemented yet")
def test_netcdf_extract_time():
    assert geoextent.fromFile("tests/testdata/nc/ECMWF_ERA-40_subset.nc", tbox=True) == ['2002-07-01', '2002-07-31']


def test_gml_extract_time():
    result = geoextent.fromFile("tests/testdata/gml/clc_1000_PT.gml", tbox=True)
    assert result["tbox"] == ['2005-12-31', '2013-11-30']


@pytest.mark.skip(reason="file format not implemented yet")
def test_netcdf_extract_bbox_time():
    assert geoextent.fromFile("tests/testdata/nc/ECMWF_ERA-40_subset.nc", bbox=True, tbox=True) == [
        [-90.0, 0.0, 90.0, 357.5], ['2002-07-01', '2002-07-31']]


def test_gpkg_extract_bboxs():
    result = geoextent.fromFile("tests/testdata/geopackage/nc.gpkg", bbox=True)
    assert result['bbox'] == pytest.approx([-84.323835, 33.882102, -75.456585, 36.589757], abs=tolerance)
    assert result["crs"] == "4326"


@pytest.mark.skipif("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
                    reason="Travis GDAL version outdated")
def test_gml_extract_bbox_time():
    result = geoextent.fromFile("tests/testdata/gml/clc_1000_PT.gml", bbox=True, tbox=True)
    assert result['bbox'] == pytest.approx([-17.542069, 32.39669, -6.959389, 39.301139], abs=tolerance)
    assert result["crs"] == "4326"
    assert result['tbox'] == ['2005-12-31', '2013-11-30']


def test_not_found_file():
    result = geoextent.fromFile('tests/testdata/empt.geojson', bbox=True)
    assert result is None


def test_not_supported_file_format():
    result = geoextent.fromFile('tests/testdata/geojson/empty.geo', bbox=True)
    assert result is None


def test_bbox_and_tbox_both_false():
    with pytest.raises(Exception) as excinfo:
        geoextent.fromFile('tests/path_does_not_matter', bbox=False, tbox=False)
    assert "No extraction options" in str(excinfo.value)
