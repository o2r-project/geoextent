import geoextent.lib.extent as geoextent

def test_geotiff_extract_bbox():
    result = geoextent.fromFile('testdata/tif/wf_100m_klas.tif', bbox=True)
    assert result["bbox"] == [5.91530075647532, 50.3102519741084, 9.46839871248415, 52.5307755328733]

def test_geotiff_extract_time():
    result = geoextent.fromFile('testdata/tif/wf_100m_klas.tif', bbox=True)
    assert "temporal_extent" not in result

def test_geotiff_crs_used():
    result = geoextent.fromFile('testdata/tif/wf_100m_klas.tif', bbox=True)
    assert result["crs"] == '4326'