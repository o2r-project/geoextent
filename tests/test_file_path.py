import pytest
import geoextent.lib.helpfunctions as hf

def test_check_relative_file_path():
    assert hf.checkPath("relative.geojson")

def test_check_abs_file_path():
    assert hf.checkPath("/testdata/muenster_ring_zeit.geojson")

def test_check_invalid_file_path():
    with pytest.raises(Exception) as excinfo:
        hf.checkPath("/testdata/invalid.geojson")
    assert "No such file or directory" in str(excinfo.value)