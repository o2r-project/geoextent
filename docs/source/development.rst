Development
===========

Notes for developers of ``geoextent``.

Environment
-----------

All commands in this file assume you work in a virtual environment created with [``virtualenvwrapper``](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) as follows (please keep up to date!):

::

    # pip install virtualenvwrapper
    
    # Add to .bashrc:
    # export WORKON_HOME=$HOME/.virtualenvs
    # source ~/.local/bin/virtualenvwrapper.sh
    
    # Where are my virtual envs stored?
    # echo $WORKON_HOME
    
    # Create environment using Python 3
    #mkvirtualenv -p $(which python3) geoextent
    
    # Activate env
    workon geoextent
    
    # Deactivate env
    deactivate
    
    #cdvirtualenv
    #rmvirtualenv

Required packages
-----------------

In the environment created above, run

::

    pip install -r requirements.txt
    
Install a matching version of gdal-python into the virtual environment:

::

    gdal-config --version

    CPLUS_INCLUDE_PATH=/usr/include/gdal C_INCLUDE_PATH=/usr/include/gdal pip install gdal==`gdal-config --version`

For the installation to suceed you need the following system packages (on Debian/Ubuntu):

- ``libproj-dev``
- ``libgdal-dev``
- ``libgeos-dev``
- ``gdal-bin``

Run tests
---------

To install development requirements, run

::

    pip install -r requirements-dev.txt

Either install the lib and run ``pytest``, or run ``python -m pytest``.
You can also run individual files:

::

    pytest tests/test_api.py

Documentation
-------------

The documentation is based on Sphinx_.
The source files can be found in the directory ``docs/`` and the rendered online documentation is at https://o2r.info/geoextent/.

Build documentation locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    cd docs/
    pip install -r requirements-docs.txt
    make html

Build documentation website
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The deployed documentation website is built on Travis CI, see file ``.travis.yml`` for details.
In short, an extra stage ``build docs`` is executed only on the ``master`` branch and not for pull requests.

.. _Sphinx: https://www.sphinx-doc.org

Release
-------

Prerequisites
^^^^^^^^^^^^^

Required tools:

- ``setuptools``
- ``wheel``
- ``twine``

::

    pip install --upgrade setuptools wheel twine

Run tests
^^^^^^^^^

Make sure that all tests work locally by running

::

    pytest

and check the tests on `Travis CI o2r-project/geoextent`_ before continuing with the following tasks.

.. _`Travis CI o2r-project/geoextent`: https://travis-ci.org/github/o2r-project/geoextent

Bump version for release
^^^^^^^^^^^^^^^^^^^^^^^^

Follow the `Semantic Versioning specification`_ to clearly mark changes as a new major version, minor changes, or patches.
The version number is centrally managed in the file ``geoextent/__init__.py``.

.. _Semantic Versioning specification: https://semver.org/

Update changelog
^^^^^^^^^^^^^^^^

Update the changelog in file ``docs/source/changelog.rst``, use the `sphinx-issues`_ syntax for referring to pull requests and contributors for changes where appropriate.

.. _sphinx-issues: https://github.com/sloria/sphinx-issues

Build distribution archive
^^^^^^^^^^^^^^^^^^^^^^^^^^

See the PyPI documentation on generating a distribution archive, https://packaging.python.org/tutorials/packaging-projects/, for details.

::

    # remove previous releases and builds
    rm dist/*
    rm -rf build *.egg-info

    python3 setup.py sdist bdist_wheel

Upload to test repository
^^^^^^^^^^^^^^^^^^^^^^^^^

First upload to the test repository and check everything is in order.

::

    # upload with twine, make sure only one wheel is in dist/
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*

Check if the information on https://test.pypi.org/project/geoextent/ is correct.
Then switch to a new Python environment or use a Python 3 container to get an "empty" setup.
Install geoextent from TestPyPI and ensure the package is functional:

::

    docker run --rm -it -v $(pwd)/tests/testdata/:/testdata python:3-buster /bin/bash

    # install system deps
    apt-get update
    apt-get install gdal-bin libgdal-dev libproj-dev libgeos-dev libspatialite-dev netcdf-bin

    # in the container, first install packages not on TestPyPI
    pip install geojson pyproj gdal==`gdal-config --version`

    pip install -i https://test.pypi.org/simple/ geoextent
    geoextent --help
    geoextent --version

    geoextent -b -t -input= /testdata/geojson/muenster_ring_zeit.geojson
    geoextent -b -t -input= /testdata/shapefile/gis_osm_buildings_a_free_1.shp

Alternatively, use Debian Testing container to try out a more recent version of GDAL which matches the current release of the GDAL package on PyPI:

::
    
    docker run --rm -it debian:testing
    
    # Python + PIP
    apt-get update
    apt-get install python3 python3-pip wget

    # System dependencies
    apt-get install gdal-bin libgdal-dev libproj-dev libgeos-dev

    wget https://github.com/o2r-project/geoextent/blob/master/tests/testdata/tif/wf_100m_klas.tif


Upload to PyPI
^^^^^^^^^^^^^^

::

    twine upload dist/*


Check if information on https://pypi.org/project/geoextent/ is all correct.
Install the library from PyPI into a new environment, e.g., by reusing the container session from above, and check that everything works.

Add tag
^^^^^^^

Add a version tag to the commit of the release and push it to the main repository.
Go to GitHub and create a new release by using the "Draft a new release" button and using the just pushed tag.
