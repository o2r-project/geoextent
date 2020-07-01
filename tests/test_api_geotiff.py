import geoextent.lib.extent as geoextent
from pytest import approx

def test_geotiff_extract_bbox():
    result = geoextent.fromFile('tests/testdata/tif/wf_100m_klas.tif', bbox=True)
    assert "bbox" in result
    assert result["bbox"] == approx([50.310252, 5.9153008, 52.5307755, 9.4683987])

def test_geotiff_extract_time():
    result = geoextent.fromFile('tests/testdata/tif/wf_100m_klas.tif', bbox=True)
    assert "temporal_extent" not in result

def test_geotiff_crs_used():
    result = geoextent.fromFile('tests/testdata/tif/wf_100m_klas.tif', bbox=True)
    assert "crs" in result
    assert result["crs"] == '4326'
