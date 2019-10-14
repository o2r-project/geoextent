import os           # used to get the location of the testdata
import pytest

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def test_geojson_bbox(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/folder/muenster_ring_zeit.geojs', 
        '--detail', 'bbox')
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454]" in ret.stdout, "bbox is printed to console"

def test_geojson_bbox_invalid_coordinates(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/folder/muenster_ring_zeit.geojs', 
        '--detail', 'bbox')
    assert ret.success, "process should return success"
    assert ret.stderr is not None
    assert ret.stderr == 'invalid coordinates', "stderr should not be empty"
    


def test_geojson_time(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/folder/muenster_ring_zeit.geojs', 
        '--detail', 'bbox',
        '--time')
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "['2018-11-14', '2018-11-14']" in ret.stdout,  "time value is printed to console"

def test_geojson_time_invalid(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/folder/muenster_ring_zeit.geojs', 
        '--detail', 'bbox',
        '--time')
    assert ret.success, "process should return success"
    ret.stderr is not None
    assert ret.stderr == 'invalid time format', "stderr should not be empty"

def test_netcdf_bbox(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/ECMWF_ERA-40_subset1.nc', 
        '--detail', 'bbox')
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[-90.0, 0.0, 90.0, 357.5]" in ret.stdout, "bbox is printed to console"

def test_netcdf_time(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/ECMWF_ERA-40_subset1.nc', 
        '--detail', 'bbox',
        '--time')
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "['2002-07-01','2002-07-31']" in ret.stdout,  "time value is printed to console"

def test_netcdf_time_invalid(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/ECMWF_ERA-40_subset1.nc', 
        '--detail', 'bbox',
        '--time')
    assert ret.success, "process should return success"
    assert ret.stderr is not None
    assert ret.stderr == 'invalid time format', "stderr should not be empty"

def test_kml_bbox(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/aasee.kml', 
        '--detail', 'bbox')
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[7.594213, 51.942466, 7.618246, 51.957278]" in ret.stdout, "bbox is printed to console"

def test_kml_time(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/aasee.kml', 
        '--detail', 'bbox',
        '--time')
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[None]" in ret.stdout,  "time value is printed to console"

def test_kml_time_invalid(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/aasee.kml', 
        '--detail', 'bbox',
        '--time')
    assert ret.success, "process should return success"
    assert ret.stderr is not None
    assert ret.stderr == 'invalid time format', "stderr should not be empty"

def test_geotiff_bbox(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/wf_100m_klas.tif', 
        '--detail', 'bbox')
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[5.9153007564753155, 50.31025197410836, 9.468398712484145, 52.5307755328733]" in ret.stdout, "bbox is printed to console"

def test_gpkg_bbox(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/nc.gpkg', 
        '--detail', 'bbox')
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[33.882, -84.3239, 36.5896, -75.457]" in ret.stdout, "bbox is printed to console"

def test_csv_bbox(script_runner, tmpdir):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/folder/cities_NL.csv', 
        '--detail', 'bbox')
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[6.574722, 51.434444, 4.3175, 53.217222]" in ret.stdout, "bbox is printed to console"

def test_csv_time(script_runner, tmpdir):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/folder/cities_NL.csv', 
        '--detail', 'bbox',
        '--time')
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "['2018-09-30', '2018-09-30']" in ret.stdout, "time value is printed to console"

def test_csv_time_invalid(script_runner, tmpdir):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/folder/cities_NL.csv', 
        '--detail', 'bbox',
        '--time')
    assert not ret.success, "process should return success"
    assert ret.stderr is not None
    assert ret.stderr == 'invalid time format', "stderr should not be empty"

def test_gml_bbox(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/clc_1000_PT.gml', 
        '--detail', 'bbox')
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[-17.5420724159224, 32.3966928193202, -6.95938792923511, 39.3011352746141]" in ret.stdout, "bbox is printed to console"

def test_gml_time(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/clc_1000_PT.gml', 
        '--detail', 'bbox',
        '--time')
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "['2013-11-30T23:00:00Z', '2013-11-30T23:00:00Z']" in ret.stdout,  "time value is printed to console"

def test_gml_time_invalid(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/clc_1000_PT.gml', 
        '--detail', 'bbox',
        '--time')
    assert ret.success, "process should return success"
    assert ret.stderr is not None
    assert ret.stderr == 'invalid time format', "stderr should not be empty"

def test_shp_bbox(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/Abgrabungen_Kreis_Kleve_Shape.shp', 
        '--detail', 'bbox')
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[295896.274870878, 5694747.64703736, 325999.79578122497, 5747140.98659967]" in ret.stdout, "bbox is printed to console"

def test_json_bbox(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/folder/schutzhuetten_aachen.json', 
        '--detail', 'bbox')
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[292063.81225905, 5618144.09259115, 302531.3161606, 5631223.82854667]" in ret.stdout, "bbox is printed to console"

def test_json_time(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/folder/schutzhuetten_aachen.json', 
        '--detail', 'bbox',
        '--time')
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[None]" in ret.stdout,  "time value is printed to console"

def test_json_time_invalid(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/folder/schutzhuetten_aachen.json', 
        '--detail', 'bbox',
        '--time')
    assert ret.success, "process should return success"
    assert ret.stderr is not None
    assert ret.stderr == 'invalid time format', "stderr should not be empty"

def test_folder_multiple_files(script_runner):
    ret = script_runner.run('python', 'geoextent',
        '--path', 'Testdata/folder',
        '--detail', 'bbox')
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454]" in ret.stdout, "bboxes and time values of all files inside folder, are printed to console"
    assert "[6.574722, 51.434444, 4.3175, 53.217222]" in ret.stdout, "bboxes and time values of all files inside folder, are printed to console"
    assert "[292063.81225905, 5618144.09259115, 302531.3161606, 5631223.82854667]" in ret.stdout, "bboxes and time values of all files inside folder, are printed to console"

'''
@pytest.mark.parametrize("test_input,expected", [(True, "param1")])
def test_string_parameter(test_input, expected):
    assert isinstance(test_input, str)

@pytest.mark.parametrize("test_input,expected", [("param1", True)])
def test_bool_parameter(test_input, expected):
    assert isinstance(test_input, bool)

@pytest.mark.parametrize("test_input,expected", [("param1", 1)])
def test_numeric_parameter(test_input, expected):
    assert isinstance(test_input, int)
'''