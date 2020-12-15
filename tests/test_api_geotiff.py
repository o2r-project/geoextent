import geoextent.lib.extent as geoextent
from help_functions_test import tolerance
import pytest
from osgeo import gdal

def test_geotiff_extract_bbox():
    result = geoextent.fromFile('tests/testdata/tif/wf_100m_klas.tif', bbox=True)
    assert "bbox" in result
    assert result["bbox"] == pytest.approx([5.915300, 50.310251, 9.468398, 52.530775], abs=tolerance)

def test_geotiff_extract_time():
    result = geoextent.fromFile('tests/testdata/tif/wf_100m_klas.tif', bbox=True)
    assert "temporal_extent" not in result

def test_geotiff_crs_used():
    result = geoextent.fromFile('tests/testdata/tif/wf_100m_klas.tif', bbox=True)
    assert "crs" in result
    assert result["crs"] == '4326'
