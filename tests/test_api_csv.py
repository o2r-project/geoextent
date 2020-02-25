import os       
import sys
import pytest
import geoextent.lib.extent as geoextent

def test_csv_extract_bbox():
    result = geoextent.fromFile('testdata/csv/cities_NL_lat&long.csv', bbox=True)
    assert "bbox" in result
    assert "tbox" not in result
    assert result["bbox"] == [4.3175, 51.434444, 6.574722, 53.217222]

def test_csv_extract_tbox():
    result = geoextent.fromFile('testdata/csv/cities_NL.csv', bbox=False, tbox=True)
    assert "bbox" not in result
    assert "tbox" in result
    assert result["tbox"] == ['01.08.2017', '30.09.2019']

def test_csv_extract_bbox_and_tbox():
    result = geoextent.fromFile('testdata/csv/cities_NL.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == [4.3175, 51.434444, 6.574722, 53.217222]
    assert result["tbox"] == ['01.08.2017', '30.09.2019']

def test_empty_csv_file():
    result = geoextent.fromFile('testdata/csv/empty_csv.csv', bbox=True, tbox=True)
    assert "bbox" not in result
    assert "tbox" not in result
    assert "crs" not in result

def test_csv_extract_bbox_and_tbox_semicolon_delimiter():
    result = geoextent.fromFile('testdata/csv/csv_semicolon_delimiter.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == [4.3175, 51.434444, 6.574722, 53.217222]
    assert result["tbox"] == ['01.08.2017', '30.09.2019']

def test_csv_extract_bbox_and_tbox_comma_delimiter():
    result = geoextent.fromFile('testdata/csv/csv_comma_delimiter.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == [4.3175, 51.434444, 6.574722, 53.217222]
    assert result["tbox"] == ['01.08.2017', '30.09.2019']