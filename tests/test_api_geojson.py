import os         # used to get the location of the testdata
import sys
import pytest
import geoextent.lib.extent as geoextent

def test_geojson_extract_bbox():
    result = geoextent.fromFile('testdata/geojson/muenster_ring_zeit.geojson', 'b')
    assert result["bbox"] == [7.60168075561523, 51.9488147720619, 7.64725685119629, 51.9746240298775]

def test_invalid_coordinate_geojson_extract_bbox():
    with pytest.raises(Exception) as excinfo:
        geoextent.fromFile('testdata/geojson/invalid_coordinate.geojson', 'b')
    assert "The file is not valid" in str(excinfo.value)

def test_one_point_geojson_extract_bbox():
    result = geoextent.fromFile('testdata/geojson/onePoint.geojson', 'b')
    assert result["bbox"] == [6.22049331665039, 50.5215036027663, 6.22049331665039, 50.5215036027663]

def test_empty_file_geojson_extract_bbox():
    with pytest.raises(Exception) as excinfo:
        geoextent.fromFile('testdata/geojson/empty.geojson', 'b')
    assert "The file is empty" in str(excinfo.value)

def test_geojson_extract_time():
    result = geoextent.fromFile('testdata/geojson/muenster_ring_zeit.geojson', 'b')
    assert result["temporal_extent"] == ['2018-11-14', '2018-11-14']

def test_empty_file_geojson_extract_time(capsys):
    with pytest.raises(Exception) as excinfo:
        geoextent.fromFile('testdata/geojson/empty.geojson', 'b')
    assert "The file is empty" in str(excinfo.value)
