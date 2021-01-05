import pytest
from help_functions_test import tolerance
import geoextent.lib.extent as geoextent


def test_shapefile_with_crs_extract_bbox():
    result = geoextent.fromFile('tests/testdata/shapefile/gis_osm_buildings_a_free_1.shp', bbox=True, tbox=False)
    assert "temporal_extent" not in result
    assert result["bbox"] == pytest.approx([-167.400123, -89.998844, 166.700078, -60.708069], abs=tolerance)
    assert result["crs"] == "4326"


def test_shapefile_without_crs_extract_bbox():
    result = geoextent.fromFile('tests/testdata/shapefile/Abgrabungen_Kreis_Kleve_Shape.shp', bbox=True, tbox=False)
    assert "tbox" not in result
    assert "bbox" not in result
    assert "crs" not in result


def test_shapefile_extract_bbox_with_crs():
    result = geoextent.fromFile('tests/testdata/shapefile/gis_osm_buildings_a_free_1.shp', bbox=True, tbox=False)
    assert "temporal_extent" not in result
    assert result["bbox"] == pytest.approx([-167.400123, -89.998844, 166.700078, -60.708069], abs=tolerance)
    assert result["crs"] == "4326"


def test_shapefile_extract_time():
    result = geoextent.fromFile('tests/testdata/shapefile/ifgi_denkpause.shp', bbox=False, tbox=True)
    assert "bbox" not in result
    assert "crs" not in result
    assert "tbox" in result
    assert result['tbox'] == ['2021-01-01', '2021-01-01']
