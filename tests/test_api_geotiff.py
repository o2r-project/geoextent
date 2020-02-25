import geoextent.lib.extent as geoextent

def test_geotiff_extract_bbox():
    result = geoextent.fromFile('testdata/tif/wf_100m_klas.tif', bbox=True)
    bbox = [round(result["bbox"][0],7), round(result["bbox"][1],7), round(result["bbox"][2],7), round(result["bbox"][3],7)]
    assert "bbox" in result
    assert bbox == [5.9153008, 50.310252, 9.4683987, 52.5307755]

def test_geotiff_extract_time():
    result = geoextent.fromFile('testdata/tif/wf_100m_klas.tif', bbox=True)
    assert "temporal_extent" not in result

def test_geotiff_crs_used():
    result = geoextent.fromFile('testdata/tif/wf_100m_klas.tif', bbox=True)
    assert "crs" in result
    assert result["crs"] == '4326'