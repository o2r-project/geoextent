import os         # used to get the location of the testdata
import sys
import pytest
import geoextent.lib.extent as geoextent

def test_geojson_extract_bbox():
    result = geoextent.fromFile('tests/testdata/geojson/muenster_ring_zeit.geojson', bbox=True)
    assert result["bbox"] == [7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454]

def test_invalid_coordinate_geojson_extract_bbox():
    result = geoextent.fromFile('tests/testdata/geojson/invalid_coordinate.geojson', bbox=True)
    assert result["bbox"] is None

def test_one_point_geojson_extract_bbox():
    result = geoextent.fromFile('tests/testdata/geojson/onePoint.geojson', bbox=True)
    assert result["bbox"] == [6.220493316650391, 50.52150360276628, 6.220493316650391, 50.52150360276628]

def test_empty_file_geojson_extract_bbox():
    with pytest.raises(Exception) as excinfo:
        geoextent.fromFile('tests/testdata/geojson/empty.geojson',  bbox=True)
    assert "is not valid" in str(excinfo.value)

def test_geojson_extract_time():
    result = geoextent.fromFile('tests/testdata/geojson/muenster_ring_zeit.geojson', tbox=True)
    assert result["tbox"] == ['2018-11-14', '2018-11-14']

def test_geojson_extract_only_time():
    result = geoextent.fromFile('tests/testdata/geojson/muenster_ring_zeit.geojson', bbox=False, tbox=True)
    assert "bbox" not in result
    assert result["tbox"] == ['2018-11-14', '2018-11-14']