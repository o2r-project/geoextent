import os           # used to get the location of the testdata

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def test_geojson_bbox(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/muenster_ring_zeit.geojs', 
        '--detail', 'bbox')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454]" in ret.stdout, "bbox is printed to console"

def test_geojson_bbox_invalid_coordinates(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/muenster_ring_zeit.geojs', 
        '--detail', 'bbox')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == 'invalid coordinates', "stderr should not be empty"

def test_geojson_time(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/muenster_ring_zeit.geojs', 
        '--detail', 'bbox',
        '--time')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "2018-11-14 00:00:00" in ret.stdout,  "time value is printed to console"

def test_geojson_time_invalid(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/muenster_ring_zeit.geojs', 
        '--detail', 'bbox',
        '--time')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == 'invalid time format', "stderr should not be empty"

def test_nc_bbox(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/ECMWF_ERA-40_subset1.nc', 
        '--detail', 'bbox')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454]" in ret.stdout, "bbox is printed to console"

def test_nc_time(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/ECMWF_ERA-40_subset1.nc', 
        '--detail', 'bbox',
        '--time')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "2018-11-14 00:00:00" in ret.stdout,  "time value is printed to console"

def test_nc_time_invalid(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/ECMWF_ERA-40_subset1.nc', 
        '--detail', 'bbox',
        '--time')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == 'invalid time format', "stderr should not be empty"

def test_kml_bbox(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/aasee.kml', 
        '--detail', 'bbox')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454]" in ret.stdout, "bbox is printed to console"

def test_kml_time(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/aasee.kml', 
        '--detail', 'bbox',
        '--time')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "2018-11-14 00:00:00" in ret.stdout,  "time value is printed to console"

def test_kml_time_invalid(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/aasee.kml', 
        '--detail', 'bbox',
        '--time')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == 'invalid time format', "stderr should not be empty"

def test_tif_bbox(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/wf_100m_klas.tif', 
        '--detail', 'bbox')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454]" in ret.stdout, "bbox is printed to console"

def test_gpkg_bbox(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/census2016_cca_qld_short.gpkg', 
        '--detail', 'bbox')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454]" in ret.stdout, "bbox is printed to console"

def test_csv_bbox(script_runner, tmpdir):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/cities_NL.csv', 
        '--detail', 'bbox')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[[10,20],[11,50]" in ret.stdout, "bbox is printed to console"

def test_csv_time(script_runner, tmpdir):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/cities_NL.csv', 
        '--detail', 'bbox',
        '--time')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "temporal extent is from 2017 ==> 2018" in ret.stdout, "time value is printed to console"

def test_csv_time_invalid(script_runner, tmpdir):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/cities_NL.csv', 
        '--detail', 'bbox',
        '--time')
    #print(ret.stdout)
    assert not ret.success, "process should return success"
    assert ret.stderr == 'invalid time format', "stderr should not be empty"

def test_gml_bbox(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/clc_1000_PT.gml', 
        '--detail', 'bbox')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454]" in ret.stdout, "bbox is printed to console"

def test_gml_time(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/clc_1000_PT.gml', 
        '--detail', 'bbox',
        '--time')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "2018-11-14 00:00:00" in ret.stdout,  "time value is printed to console"

def test_gml_time_invalid(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/clc_1000_PT.gml', 
        '--detail', 'bbox',
        '--time')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == 'invalid time format', "stderr should not be empty"

def test_shp_bbox(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/Abgrabungen_Kreis_Kleve_Shape.shp', 
        '--detail', 'bbox')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454]" in ret.stdout, "bbox is printed to console"

def test_dbf_bbox(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/Abgrabungen_Kreis_Kleve_Shape.dbf', 
        '--detail', 'bbox')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454]" in ret.stdout, "bbox is printed to console"

def test_json_bbox(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/schutzhuetten_aachen.json', 
        '--detail', 'bbox')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "[7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454]" in ret.stdout, "bbox is printed to console"

def test_json_time(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/schutzhuetten_aachen.json', 
        '--detail', 'bbox',
        '--time')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"
    assert "2018-11-14 00:00:00" in ret.stdout,  "time value is printed to console"

def test_json_time_invalid(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata/schutzhuetten_aachen.json', 
        '--detail', 'bbox',
        '--time')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == 'invalid time format', "stderr should not be empty"

def test_folder_multiple_files(script_runner):
    ret = script_runner.run('python3', 'geoextent',
        '--path', 'Testdata')
    #print(ret.stdout)
    assert ret.success, "process should return success"
    assert ret.stderr == '', "stderr should be empty"