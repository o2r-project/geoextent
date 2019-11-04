import geoextent.lib.extent as geoextent

def test_shapefile_extract_bbox():
    result = geoextent.fromFile('testdata/shapefile/Abgrabungen_Kreis_Kleve_Shape.shp', 'b')
    assert result["bbox"] == [295896.274870878, 5694747.64703736, 325999.79578122497, 5747140.98659967]

def test_shapefile_extract_time():
    result = geoextent.fromFile('testdata/shapefile/Abgrabungen_Kreis_Kleve_Shape.shp', 'b')
    assert result["temporal_extent"] == 'None'