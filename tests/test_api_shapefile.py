import pytest
import geoextent.lib.extent as geoextent

def test_shapefile_withCRS_extract_bbox():
    result = geoextent.fromFile('tests/testdata/shapefile/gis_osm_buildings_a_free_1.shp', bbox=True, tbox=False)
    assert "temporal_extent" not in result
    assert result["bbox"] == [-167.4001236, -89.9988441, 166.7000786, -60.7080691]

def test_shapefile_without_CRS_extract_bbox():
    result = geoextent.fromFile('tests/testdata/shapefile/Abgrabungen_Kreis_Kleve_Shape.shp', bbox=True, tbox=False)
    assert "tbox " not in result
    assert result["bbox"] is None

def test_shapefile_extract_bbox_with_CRS():
    result = geoextent.fromFile('tests/testdata/shapefile/gis_osm_buildings_a_free_1.shp', bbox=True, tbox=False)
    assert "temporal_extent" not in result
    assert result["bbox"] == [-167.4001236, -89.9988441, 166.7000786, -60.7080691]
    
@pytest.mark.skip(reason="temporal extent for Shapefile not implemented yet")
def test_shapefile_extract_time():
    result = geoextent.fromFile('tests/testdata/shapefile/Abgrabungen_Kreis_Kleve_Shape.shp', bbox=False, tbox=True)
    assert "bbox" not in result
    assert result["temporal_extent"] == []
