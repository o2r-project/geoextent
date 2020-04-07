import geoextent.__main__ as geoextent
geoextent.print_help_fun()

import geoextent.lib.extent as geoextent
geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', True, False)

import geoextent.lib.extent as geoextent
geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', False, True)

import geoextent.lib.extent as geoextent
geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', True, True)