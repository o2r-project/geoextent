import pytest
import geoextent.lib.extent as geoextent

def test_shapefile_extract_bbox():
    result = geoextent.fromFile('tests/testdata/shapefile/Abgrabungen_Kreis_Kleve_Shape.shp', bbox=True, tbox=False)
    assert "temporal_extent" not in result
    assert result["bbox"] == [295896.274870878, 5694747.64703736, 325999.79578122497, 5747140.98659967]
    
@pytest.mark.skip(reason="temporal extent for Shapefile not implemented yet")
def test_shapefile_extract_time():
    result = geoextent.fromFile('tests/testdata/shapefile/Abgrabungen_Kreis_Kleve_Shape.shp', bbox=False, tbox=True)
    assert "bbox" not in result
    assert result["temporal_extent"] == []
