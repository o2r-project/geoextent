from osgeo import gdal,osr

def test_crs_geotiff():
    ds=gdal.Open(r'testdata/tif/wf_100m_klas.tif')
    prj=ds.GetProjection()
    srs=osr.SpatialReference(wkt=prj)
    assert srs.IsProjected
    assert srs.GetAttrValue('AUTHORITY',1) == '4326'