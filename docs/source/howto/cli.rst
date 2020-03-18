
Command-Line Interface (CLI)
============================

**geoextent** is called with this command:
   
.. autoprogram:: geoextent.__main__:argparser
   :prog: \


Examples:-
----------

.. note::
   Depending on the local configuration, **geoextent** might need to be called with the python interpreter prepended.

**Example 1:** Show help message:

::

   geoextent -h

output

.. jupyter-execute::
   :hide-code:

   import geoextent.__main__ as geoextent
   geoextent.print_help_fun()

**Example 2:** Extract bounding box:

::

   geoextent -b 'file.geojson'

output

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent
   geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', True, False)

**Example 3:** Extract time interval:

::

   geoextent -t 'file.geojson'

output

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent
   geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', False, True)

**Example 4:** Extract both bounding box and time interval:

::

   geoextent -b -t 'file.geojson'

output

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent
   geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', True, True)


   