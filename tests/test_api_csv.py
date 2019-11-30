import pytest
import geoextent.lib.extent as geoextent

def test_csv_extract_bbox():
    result = geoextent.fromFile('testdata/csv/cities_NL_lat&long.csv', 'b')
    assert result["bbox"] == [4.3175, 51.434444, 6.574722, 53.217222]

def test_empty_csv_file_extract_bbox():
    with pytest.raises(Exception) as excinfo:
        geoextent.fromFile('testdata/csv/empty_csv.csv', 'b')
    assert "The file is empty" in str(excinfo.value)

def test_empty_csv_file_extract_time():
    with pytest.raises(Exception) as excinfo:
        geoextent.fromFile('testdata/csv/empty_csv.csv', 'b')
    assert "The file is empty" in str(excinfo.value)