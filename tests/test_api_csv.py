import pytest
import geoextent.lib.extent as geoextent

def test_csv_extract_bbox():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL_lat&long.csv', bbox=True)
    assert "bbox" in result
    assert result["bbox"] == [4.3175, 51.434444, 6.574722, 53.217222]

def test_empty_csv_file():
    result = geoextent.fromFile('tests/testdata/csv/empty_csv.csv')
    assert "bbox" not in result
    assert "temporal_extent" not in result
    assert "crs" not in result

    result = geoextent.fromFile('tests/testdata/csv/empty_csv.csv', bbox=True, tbox=True)
    assert "bbox" not in result
    assert "temporal_extent" not in result
    assert "crs" not in result

def test_csv_extract_tbox():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL.csv', bbox=False, tbox=True)
    assert "temporal_extent" not in result
    assert result["temporal_extent"] == ['2017-08-01', '2019-09-30']
