
API Docs
========
::

   geoextent.fromFile(input, bbox, time)
Takes raw data (in the form of a string, boolean, boolean) to output result based on these fields.

**Parameters:**   
   - **input** - a string value of input file or path    
   - **bbox** - a boolean value to extract spatial extent (bounding box)
   - **time** - a boolean value to extract temporal extent

Examples:-
----------

**Example 1:** Extracting bounding box:

::

   geoextent.fromFile('file.geojson', True, False)

output

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent
   geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', True, False)

**Example 2:** Extracting time interval:

::

   geoextent.fromFile('file.geojson', False, True)

output

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent
   geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', False, True)

**Example 3:** Extracting both bounding box and time interval:

::

   geoextent.fromFile('file.geojson', True, True)

output

.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent
   geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', True, True)