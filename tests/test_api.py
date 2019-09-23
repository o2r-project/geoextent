import os           # used to get the location of the testdata
import geoextent



###############
# --detail=bbox
###############

def test_geojson_extract_bbox():
    assert geoextent.getMetadata("/Testdata/folder/muenster_ring_zeit.geojson", 'bbox') == [7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454]

def test_invalid_coordinate_geojson_extract_bbox(capsys):
    sys.stderr.write("error message")
    out, error = capsys.readouterr()
    assert out == "Invalid geojson file\n"
    assert geoextent.getMetadata("/Testdata/invalid_coordinate.geojson", 'bbox') == [None]

def test_one_point_geojson_extract_bbox():
    assert geoextent.getMetadata("/Testdata/onePoint.geojson", 'bbox') == [6.220493316650391, 50.52150360276628, 6.220493316650391, 50.52150360276628]

def test_empty_file_geojson_extract_bbox(capsys):
    sys.stderr.write("error message")
    out, error = capsys.readouterr()
    assert out == "Empty geojson file\n"
    assert geoextent.getMetadata("/Testdata/empty.geojson", 'bbox') == [None]

def test_netcdf_extract_bbox():
    assert geoextent.getMetadata("/Testdata/ECMWF_ERA-40_subset1.nc", 'bbox') == [-90.0, 0.0, 90.0, 357.5]

def test_kml_extract_bbox():
    assert geoextent.getMetadata("/Testdata/aasee.kml", 'bbox') == [7.594213, 51.942466, 7.618246, 51.957278]

def test_geotiff_extract_bbox():
    assert geoextent.getMetadata("/Testdata/wf_100m_klas.tif", 'bbox') == [5.9153007564753155, 50.31025197410836, 9.468398712484145, 52.5307755328733]

def test_gpkg_extract_bbox():
    assert geoextent.getMetadata("/Testdata/nc.gpkg", 'bbox') == [33.882, -84.3239, 36.5896, -75.457]

def test_csv_extract_bbox():
    assert geoextent.getMetadata("/Testdata/folder/cities_NL.csv", 'bbox') == [6.574722, 51.434444, 4.3175, 53.217222]

def test_gml_extract_bbox():
    assert geoextent.getMetadata("/Testdata/clc_1000_PT.gml", 'bbox') == [-17.5420724159224, 32.3966928193202, -6.95938792923511, 39.3011352746141]

def test_shapefile_extract_bbox():
    assert geoextent.getMetadata("/Testdata/Abgrabungen_Kreis_Kleve_Shape.shp", 'bbox') == [295896.274870878, 5694747.64703736, 325999.79578122497, 5747140.98659967]

def test_json_extract_bbox():
    assert geoextent.getMetadata("/Testdata/folder/schutzhuetten_aachen.json", 'bbox') == [292063.81225905, 5618144.09259115, 302531.3161606, 5631223.82854667]

def test_folder_multiple_files():
    assert [7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454] in geoextent.getMetadata(filepath, 'bbox')
    assert [6.574722, 51.434444, 4.3175, 53.217222] in geoextent.getMetadata("/Testdata/folder", 'bbox')
    assert [292063.81225905, 5618144.09259115, 302531.3161606, 5631223.82854667] in geoextent.getMetadata(filepath, 'bbox')


###############
# --detail=time
###############

def test_geojson_extract_time():
    assert geoextent.getMetadata("/Testdata/folder/muenster_ring_zeit.geojson",False, 'Time') == ['2018-11-14', '2018-11-14']

def test_empty_file_geojson_extract_time(capsys):
    sys.stderr.write("error message")
    out, error = capsys.readouterr()
    assert out == "Empty geojson file\n"
    assert geoextent.getMetadata("/Testdata/empty.geojson", False , 'Time') == [None]


def test_netcdf_extract_time():
    assert geoextent.getMetadata("/Testdata/ECMWF_ERA-40_subset1.nc", False , True) == ['2002-07-01','2002-07-31']

def test_csv_extract_time():
    assert geoextent.getMetadata("/Testdata/folder/cities_NL.csv", False , 'Time') == ['2018-09-30', '2018-09-30']

def test_gml_extract_time():
    assert geoextent.getMetadata("/Testdata/clc_1000_PT.gml", False , 'Time') == ['2013-11-30T23:00:00Z', '2013-11-30T23:00:00Z']


######################
# --detail=bbox & time
######################

def test_geojson_extract_bbox_time():
    assert geoextent.getMetadata("/Testdata/folder/muenster_ring_zeit.geojson", 'bbox', 'Time') == [[7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454],['2018-11-14', '2018-11-14']]
    
def test_invalid_coordinate_geojson_extract_bbox_time(capsys):
    sys.stderr.write("error message")
    out, error = capsys.readouterr()
    assert out == "Invalid geojson file\n"
    assert geoextent.getMetadata("/Testdata/invalid_coordinate.geojson", 'bbox' , 'Time') == [[None],[None]]


def test_one_point_geojson_extract_bbox_time():
    assert geoextent.getMetadata("/Testdata/onePoint.geojson", 'bbox' , 'Time') == [[6.220493316650391, 50.52150360276628, 6.220493316650391, 50.52150360276628],[None]]

def test_empty_file_geojson_extract_bbox_time(capsys):
    sys.stderr.write("error message")
    out, error = capsys.readouterr()
    assert out == "Empty geojson file\n"
    assert geoextent.getMetadata("/Testdata/empty.geojson", 'bbox' , 'Time') == [[None],[None]]


def test_netcdf_extract_bbox_time():
    assert geoextent.getMetadata("/Testdata/ECMWF_ERA-40_subset1.nc", 'bbox' , 'Time') == [[-90.0, 0.0, 90.0, 357.5],['2002-07-01','2002-07-31']]


def test_kml_extract_bbox_time():
    assert geoextent.getMetadata("/Testdata/aasee.kml", 'bbox' , 'Time') == [[7.594213, 51.942466, 7.618246, 51.957278],[None]]

def test_geotiff_extract_bbox_time():
    assert geoextent.getMetadata("/Testdata/wf_100m_klas.tif", 'bbox' , 'Time') == [[5.9153007564753155, 50.31025197410836, 9.468398712484145, 52.5307755328733],[None]]

def test_gpkg_extract_bbox_time():
    assert geoextent.getMetadata("/Testdata/nc.gpkg", 'bbox' , 'Time') == [[33.882, -84.3239, 36.5896, -75.457],[None]]

def test_csv_extract_bbox_time():
    assert geoextent.getMetadata("/Testdata/folder/cities_NL.csv", 'bbox' , 'Time') == [[6.574722, 51.434444, 4.3175, 53.217222],['2018-09-30', '2018-09-30']]

def test_gml_extract_bbox_time():
    assert geoextent.getMetadata("/Testdata/clc_1000_PT.gml", 'bbox' , 'Time') == [[-17.5420724159224, 32.3966928193202, -6.95938792923511, 39.3011352746141],['2013-11-30T23:00:00Z', '2013-11-30T23:00:00Z']]

def test_shapefile_extract_bbox_time():
    assert geoextent.getMetadata("/Testdata/Abgrabungen_Kreis_Kleve_Shape.shp", 'bbox' , 'Time') == [[295896.274870878, 5694747.64703736, 325999.79578122497, 5747140.98659967],[None]]

def test_json_extract_bbox_time():
    assert geoextent.getMetadata("/Testdata/folder/schutzhuetten_aachen.json", 'bbox' , 'Time') == [[292063.81225905, 5618144.09259115, 302531.3161606, 5631223.82854667],[None]]

def test_folder_multiple_files():
    assert [7.6016807556152335, 51.94881477206191, 7.647256851196289, 51.974624029877454] in geoextent.getMetadata(filepath, 'bbox_time' , 'Time')
    assert [6.574722, 51.434444, 4.3175, 53.217222] in geoextent.getMetadata("/Testdata/folder", 'bbox' , 'Time')
    assert [292063.81225905, 5618144.09259115, 302531.3161606, 5631223.82854667] in geoextent.getMetadata(filepath, 'bbox' , 'Time')
