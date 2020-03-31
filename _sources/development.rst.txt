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

Build locally
^^^^^^^^^^^^^

::

    cd docs/
    pip install -r requirements-docs.txt
    make html

Build documentation website
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The documentation website is built on Travis CI using ``travis-sphinx_``.
See the ``travis-sphinx`` documentation and the file ``.travis.yml`` for details.

.. _Sphinx: https://www.sphinx-doc.org
.. _travis-sphinx: https://github.com/syntaf/travis-sphinx

Release
-------

Prerequisites
^^^^^^^^^^^^^

See the PyPI documentation on generating a distribution archive, https://packaging.python.org/tutorials/packaging-projects/, for details.

Required tools:

- ``setuptools``
- ``wheel``
- ``twine``

::

    pip install --upgrade setuptools wheel twine

::

    python3 setup.py sdist bdist_wheel

Upload to test repository
^^^^^^^^^^^^^^^^^^^^^^^^^

First upload to the test repository and check everything is in order.

::

    # upload with twine, make sure only one wheel is in dist/
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*

Check if the information on https://test.pypi.org/project/geoextent/ is correct.
Then switch to a new Python environment, install geoextent from TestPyPI and try out package:

::

    pip install -i https://test.pypi.org/simple/ geoextent

Upload to PyPI
^^^^^^^^^^^^^^

::

    twine upload dist/*


Check if information on https://pypi.org/project/geoextent/ is all correct.
Install the library from PyPI into a new Python environment and chech that everything works:

::

    ...
