import os         # used to get the location of the testdata
import sys
import pytest
import geoextent.lib.extent as geoextent

def test_geojson_extract_bbox():
    result = geoextent.fromFile('tests/testdata/geojson/muenster_ring_zeit.geojson', bbox=True)
    assert result["bbox"] == pytest.approx([7.601680, 51.948814, 7.647256, 51.974624])

def test_invalid_coordinate_geojson_extract_bbox():
    result = geoextent.fromFile('tests/testdata/geojson/invalid_coordinate.geojson', bbox=True)
    assert result["bbox"] is None

def test_one_point_geojson_extract_bbox():
    result = geoextent.fromFile('tests/testdata/geojson/onePoint.geojson', bbox=True)
    assert result["bbox"] == pytest.approx([6.220493, 50.521503, 6.220493, 50.521503])

def test_empty_file_geojson_extract_bbox():
    result = geoextent.fromFile('tests/testdata/geojson/empty.geojson',  bbox=True)
    assert result is None

def test_geojson_extract_time():
    result = geoextent.fromFile('tests/testdata/geojson/muenster_ring_zeit.geojson', tbox=True)
    assert result["tbox"] == ['2018-11-14', '2018-11-14']

def test_geojson_extract_only_time():
    result = geoextent.fromFile('tests/testdata/geojson/muenster_ring_zeit.geojson', bbox=False, tbox=True)
    assert "bbox" not in result
    assert result["tbox"] == ['2018-11-14', '2018-11-14']