
Command-Line Interface (CLI)
============================

**geoextent** is called with this Command:
   
.. autoprogram:: geoextent.__main__:argparser
   :prog: \


Examples:-
----------
**Ex (1):** Show help message:

::

   python3 geoextent -h

output

.. jupyter-execute::
   :hide-code:

   import geoextent.__main__ as geoextent
   geoextent.print_help_fun()

**Ex (2):** Extract bounding box:

::

   python3 geoextent -b 'file.geojson'

output

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent
   geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', True, False)

**Ex (3):** Extract time interval:

::

   python3 geoextent -t 'file.geojson'

output

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent
   geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', False, True)

**Ex (4):** Extract both bounding box and time interval:

::

   python3 geoextent -b -t 'file.geojson'

output

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent
   geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', True, True)


   