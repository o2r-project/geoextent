import os       
import sys
import pytest
import geoextent.lib.extent as geoextent

def test_csv_extract_bbox():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL_lat&long.csv', bbox=True)
    assert "bbox" in result
    assert "tbox" not in result
    assert result["bbox"] == [4.3175, 51.434444, 6.574722, 53.217222]

def test_csv_extract_tbox():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL.csv', bbox=False, tbox=True)
    assert "bbox" not in result
    assert "tbox" in result
    assert result["tbox"] == ['2017-08-01', '2019-09-30']

def test_csv_extract_bbox_and_tbox():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == pytest.approx([4.3175, 51.434444, 6.574722, 53.217222])
    assert result["tbox"] == ['2017-08-01', '2019-09-30']

def test_empty_csv_file():
    result = geoextent.fromFile('tests/testdata/csv/empty_csv.csv', bbox=True)
    assert result is None

def test_csv_extract_bbox_and_tbox_semicolon_delimiter():
    result = geoextent.fromFile('tests/testdata/csv/csv_semicolon_delimiter.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == pytest.approx([4.3175, 51.434444, 6.574722, 53.217222])
    assert result["tbox"] == ['2017-08-01', '2019-09-30']

def test_csv_extract_bbox_and_tbox_comma_delimiter():
    result = geoextent.fromFile('tests/testdata/csv/csv_comma_delimiter.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == pytest.approx([4.3175, 51.434444, 6.574722, 53.217222])
    assert result["tbox"] == ['2017-08-01', '2019-09-30']

def test_csv_extract_bbox_and_tbox_with_Time():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL_Time.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == pytest.approx([4.3175, 51.434444, 6.574722, 53.217222])
    assert result["tbox"] == ['2017-08-01', '2019-09-30']

def test_csv_extract_bbox_and_tbox_with_TimeStamp():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL_TimeStamp.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == pytest.approx([4.3175, 51.434444, 6.574722, 53.217222])
    assert result["tbox"] == ['2017-08-01', '2019-09-30']

def test_csv_extract_bbox_and_tbox_with_TIME():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL_TIME.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == pytest.approx([4.3175, 51.434444, 6.574722, 53.217222])
    assert result["tbox"] == ['2017-08-01', '2019-09-30']

def test_csv_extract_bbox_and_tbox_with_Datetime():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL_Datetime.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == pytest.approx([4.3175, 51.434444, 6.574722, 53.217222])
    assert result["tbox"] == ['2017-08-01', '2019-09-30']

def test_csv_extract_bbox_and_tbox_with_LATITUDE_LONGITUDE():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL_LATITUDE.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == pytest.approx([4.3175, 51.434444, 6.574722, 53.217222])
    assert result["tbox"] == ['2017-08-01', '2019-09-30']

def test_csv_extract_bbox_and_tbox_with_LAT_LONG():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL_LAT.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == pytest.approx([4.3175, 51.434444, 6.574722, 53.217222])
    assert result["tbox"] == ['2017-08-01', '2019-09-30']

def test_csv_extract_bbox_and_tbox_with_TIME_DATE():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL_TIME_DATE.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == pytest.approx([4.3175, 51.434444, 6.574722, 53.217222])
    assert result["tbox"] == ['2010-09-01', '2019-09-30']

def test_csv_extract_bbox_and_tbox_with_cols_diff_order():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL_case1.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == pytest.approx([4.3175, 51.434444, 6.574722, 53.217222])
    assert result["tbox"] == ['2017-08-01', '2019-09-30']

def test_csv_extract_bbox_and_tbox_with_cols_diff_order_capitalisations():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL_case2.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == pytest.approx([4.3175, 51.434444, 6.574722, 53.217222])
    assert result["tbox"] == ['2017-08-01', '2019-09-30']

def test_csv_extract_bbox_and_tbox_with_cols_diff_order_and_alt_names1():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL_case3.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == pytest.approx([4.3175, 51.434444, 6.574722, 53.217222])
    assert result["tbox"] == ['2017-08-01', '2019-09-30']

def test_csv_extract_bbox_and_tbox_with_cols_diff_order_and_alt_names2():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL_case4.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == pytest.approx([4.3175, 51.434444, 6.574722, 53.217222])
    assert result["tbox"] == ['2017-08-01', '2019-09-30']

def test_csv_extract_bbox_and_tbox_with_cols_diff_order_and_alt_names3():
    result = geoextent.fromFile('tests/testdata/csv/cities_NL_case5.csv', bbox=True, tbox=True)
    assert "bbox" in result
    assert "tbox" in result
    assert result["bbox"] == pytest.approx([4.3175, 51.434444, 6.574722, 53.217222])
    assert result["tbox"] == ['2017-08-01', '2019-09-30']

def test_csv_extract_tbox_ISO8601_time_format():
    result = geoextent.fromFile('tests/testdata/csv/3DCMTcatalog_TakemuraEPS.csv', bbox=False, tbox = True)
    assert "bbox" not in result
    assert "tbox" in result
    assert result["tbox"] == ['2017-04-08', '2020-02-06']

def test_csv_extract_tbox_DD_MM_YYYY_time_format():
    result = geoextent.fromFile('tests/testdata/csv/3DCMTcatalog_TakemuraEPS_dd_mm_yyyy.csv', bbox=False, tbox = True)
    assert "bbox" not in result
    assert "tbox" in result
    assert result["tbox"] == ['2017-04-19', '2018-01-31']

def test_csv_extract_tbox_month_abbr_dd_yyyy_time_formats():
    result = geoextent.fromFile('tests/testdata/csv/3DCMTcatalog_TakemuraEPS_month_abbr_dd_yyyy_time_format.csv', bbox=False, tbox = True)
    assert "bbox" not in result
    assert result["tbox"] == ['2017-04-09', '2017-07-20']

def test_csv_extract_tbox_two_diff_time_formats():
    result = geoextent.fromFile('tests/testdata/csv/3DCMTcatalog_TakemuraEPS_mixed_time_formats.csv', bbox=False, tbox = True)
    assert "bbox" not in result
    assert "tbox" not in result

def test_csv_extract_tbox_random_sample():
    result = geoextent.fromFile('tests/testdata/csv/3DCMTcatalog_TakemuraEPS.csv', bbox=False, tbox=True , num_sample = 5)
    assert "bbox" not in result
    assert "tbox" in result
    assert result["tbox"] == ['2017-04-08', '2020-02-06']

def test_csv_extract_tbox_random_sample_invalid():
    result = geoextent.fromFile('tests/testdata/csv/3DCMTcatalog_TakemuraEPS.csv', bbox=False, tbox=True , num_sample = -1)
    assert "bbox" not in result
    assert "tbox" not in result

def test_csv_extract_tbox_random_sample_value_larger_than_data():
    result = geoextent.fromFile('tests/testdata/csv/3DCMTcatalog_TakemuraEPS.csv', bbox=False, tbox=True , num_sample = 1000000)
    assert "bbox" not in result
    assert "tbox" in result
    assert result["tbox"] == ['2017-04-08', '2020-02-06']