
API Docs
========

Documentation for the package's Python API for usage as a library.

The main function is

::

   geoextent.fromFile(input, bbox, time)

It takes raw data (in the form of a string, boolean, boolean) to output result based on these fields.

**Parameters:**   
   - ``input``: a string value of input file or path    
   - ``bbox``: a boolean value to extract spatial extent (bounding box)
   - ``time``: a boolean value to extract temporal extent ( at "day" precision '%Y-%m-%d')

Examples
--------

Extract bounding box from a single file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Code:

::

   geoextent.fromFile('muenster_ring_zeit.geojson', True, False)

Output:

.. jupyter-execute::
   :hide-code:
   :stderr:

   import geoextent.lib.extent as geoextent
   geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', True, False)

(`source of file muenster_ring_zeit.geojson`_)

Extracting time interval from a single file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Code:

::

   geoextent.fromFile('muenster_ring_zeit.geojson', False, True)

Output:

.. jupyter-execute::
   :hide-code:
   :stderr:

   import geoextent.lib.extent as geoextent
   geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', False, True)

(`source of file muenster_ring_zeit.geojson`_)

Extracting both bounding box and time interval from a single file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Code:

::

   geoextent.fromFile('muenster_ring_zeit.geojson', True, True)

Output:

.. jupyter-execute::
   :hide-code:
   :stderr:

   import geoextent.lib.extent as geoextent
   geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', True, True)

(`source of file muenster_ring_zeit.geojson`_)

.. _source of file muenster_ring_zeit.geojson: https://github.com/o2r-project/geoextent/blob/master/tests/testdata/geojson/muenster_ring_zeit.geojson
