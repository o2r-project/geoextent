import os         # used to get the location of the testdata
import sys
import pytest
import geoextent.lib.extent as geoextent

def test_geojson_extract_bbox():
    result = geoextent.fromFile('testdata/muenster_ring_zeit.geojson', 'b')
    assert result["bbox"] == [7.60168075561523, 51.9488147720619, 7.64725685119629, 51.9746240298775]

def test_invalid_coordinate_geojson_extract_bbox():
    with pytest.raises(Exception) as excinfo:
        geoextent.fromFile('testdata/invalid_coordinate.geojson', 'b')
    assert "The file is not valid" in str(excinfo.value)

def test_one_point_geojson_extract_bbox():
    result = geoextent.fromFile('testdata/onePoint.geojson', 'b')
    assert result["bbox"] == [6.22049331665039, 50.5215036027663, 6.22049331665039, 50.5215036027663]

def test_empty_file_geojson_extract_bbox():
    with pytest.raises(Exception) as excinfo:
        geoextent.fromFile('testdata/empty.geojson', 'b')
    assert "The file is empty" in str(excinfo.value)

def test_geojson_extract_time():
    assert geoextent.fromFile("/testdata/folder/muenster_ring_zeit.geojson", 't') == ['2018-11-14', '2018-11-14']

def test_empty_file_geojson_extract_time(capsys):
    sys.stderr.write("error message")
    out, error = capsys.readouterr()
    assert out == "Empty geojson file\n"
    assert geoextent.fromFile("/testdata/empty.geojson", 't') == [None]

def test_geojson_extract_bbox_time():
    assert geoextent.fromFile("/testdata/folder/muenster_ring_zeit.geojson", 'bt') == [[7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454],['2018-11-14', '2018-11-14']]
    
def test_invalid_coordinate_geojson_extract_bbox_time(capsys):
    sys.stderr.write("error message")
    out, error = capsys.readouterr()
    assert out == "Invalid geojson file\n"
    assert geoextent.fromFile("/testdata/invalid_coordinate.geojson", 'bt') == [[None],[None]]

def test_one_point_geojson_extract_bbox_time():
    assert geoextent.fromFile("/testdata/onePoint.geojson", 'bt') == [[6.220493316650391, 50.52150360276628, 6.220493316650391, 50.52150360276628],[None]]

def test_empty_file_geojson_extract_bbox_time(capsys):
    sys.stderr.write("error message")
    out, error = capsys.readouterr()
    assert out == "Empty geojson file\n"
    assert geoextent.fromFile("/testdata/empty.geojson", 'bt') == [[None],[None]]
