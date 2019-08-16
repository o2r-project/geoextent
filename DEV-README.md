# Development notes for `geoextent`

## Environment

All commands in this file assume you work in a virtual environment created with [`virtualenvwrapper`](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) as follows (please keep up to date!):

```bash
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
```

## Release

### [Generate distibution archive](https://packaging.python.org/tutorials/packaging-projects/)

Prerequisites: `setuptools wheel twine`

```bash
python3 setup.py sdist bdist_wheel
```

Upload to test repository and check everything is in order:

Check https://test.pypi.org/project/geoextent/

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# TODO switch environment

# TODO install from TestPyPI and try out package
```

Upload to PyPI:

Check **https://pypi.org/project/geoextent/**

```bash
twine upload dist/*

# TODO switch environment

# TODO install from TestPyPI and try out package
```
