
Command-Line Interface (CLI)
============================

``geoextent`` can be called on the command line with this command:
   
.. autoprogram:: geoextent.__main__:argparser
   :prog: \


Examples
--------

.. note::
   Depending on the local configuration, **geoextent** might need to be called with the python interpreter prepended:
   
   `python -m geoextent ...`

Show help message
^^^^^^^^^^^^^^^^^

::

   geoextent -h

.. jupyter-execute::
   :hide-code:
   :stderr:

   import geoextent.__main__ as geoextent
   geoextent.print_help_fun()

Extract bounding box from single file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
   You can find the file used in the examples of this section from `muenster_ring_zeit <https://raw.githubusercontent.com/o2r-project/geoextent/master/tests/testdata/geojson/muenster_ring_zeit.geojson>`_. Furthermore, for displaying the rendering of the file contents, see `rendered blob <https://github.com/o2r-project/geoextent/blob/master/tests/testdata/geojson/muenster_ring_zeit.geojson>`_.

::

   geoextent -b -input= 'muenster_ring_zeit.geojson'

Output:

.. jupyter-execute::
   :hide-code:
   :stderr:

   import geoextent.lib.extent as geoextent
   geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', True, False)

Extract time interval
^^^^^^^^^^^^^^^^^^^^^

::

   geoextent -t -input='file.geojson'

Output:

.. jupyter-execute::
   :hide-code:
   :stderr:

   import geoextent.lib.extent as geoextent
   geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', False, True)

Extract both bounding box and time interval from a single file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   geoextent -b -t -input= 'file.geojson'

.. jupyter-execute::
   :hide-code:
   :stderr:

   import geoextent.lib.extent as geoextent
   geoextent.fromFile('../tests/testdata/geojson/muenster_ring_zeit.geojson', True, True)
