# geoextent

![Python package](https://github.com/o2r-project/geoextent/workflows/Python%20package/badge.svg?branch=master) [![Build Status](https://travis-ci.org/o2r-project/geoextent.svg?branch=master)](https://travis-ci.org/github/o2r-project/geoextent) [![PyPI version](https://badge.fury.io/py/geoextent.svg)](https://pypi.org/project/geoextent/0.1.0/)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/o2r-project/geoextent/master) [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3925694.svg)](https://doi.org/10.5281/zenodo.3925694) [![SWH](https://archive.softwareheritage.org/badge/origin/https://github.com/o2r-project/geoextent.git/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/o2r-project/geoextent.git) [![SWH](https://archive.softwareheritage.org/badge/swh:1:dir:ff1e19d884833b2bc2c1ef7d9265ba45b5314332/)](https://archive.softwareheritage.org/swh:1:dir:ff1e19d884833b2bc2c1ef7d9265ba45b5314332;origin=https://github.com/o2r-project/geoextent.git;visit=swh:1:snp:609428a8b466b7877f2ca39921d69a5f6a11df9f;anchor=swh:1:rev:6aca93956d5cd6742318fd3ab27bb176b5f8c24b;path=//)

Python library for extracting geospatial extent of files and directories with multiple data formats

This project is developed as part of the [DFG-funded](https://o2r.info/about/#funding) research project Opening Reproducible Research (o2r, [https://o2r.info](https://o2r.info)).

## Installation

### System requirements

Python: `3.x`

The package relies on common system libraries for reading geospatial datasets, such as GDAL and NetCDF.
On Debian systems, the [UbuntuGIS](https://wiki.ubuntu.com/UbuntuGIS) project offers easy installation of up to date versions of those libraries.

See the `packages` list in `travis.yml` for a full list of dependencies on Linux.

### Install from PyPI

You must install a suitable version of `pygdal` manually first, see [instructions](https://pypi.org/project/pygdal/) and [this related SO thread with different helpful answers](https://gis.stackexchange.com/questions/28966/python-gdal-package-missing-header-file-when-installing-via-pip/124420#124420).
We use `pygdal` for better compatibility with virtual environments.

```bash
# pip install pygdal=="`gdal-config --version`.*"
pip install geoextent
```

### Source installation

```bash
git clone https://github.com/o2r-project/geoextent
cd geoextent
pip install -r requirements.txt

pip install -e .
```

## Use

Run

```bash
geoextent --help
```

to see usage instructions.

## Supported data formats

- GeoJSON (.geojson)
- Tabular data (.csv)
- Shapefile (.shp)
- GeoTIFF (.geotiff, .tif)

## Contribute

All help is welcome: asking questions, providing documentation, testing, or even development.

Please note that this project is released with a [Contributor Code of Conduct](https://github.com/o2r-project/geoextent/blob/master/CONDUCT.md).
By participating in this project you agree to abide by its terms.

See [CONTRIBUTING.md](https://github.com/o2r-project/geoextent/blob/master/CONTRIBUTING.md) for details.

## How to cite

> Nüst, Daniel; Garzón, Sebastian and Qamaz, Yousef. (2021, May 11). o2r-project/geoextent (Version v0.7.1). Zenodo. https://doi.org/10.5281/zenodo.3925693

See also the `CITATION.cff` and `codemeta.json` files in this repository, which can possibly be imported in the reference manager of your choice.

## License

`geoextent` is licensed under MIT license, see file [LICENSE](https://github.com/o2r-project/geoextent/blob/master/LICENSE).

Copyright (C) 2020 - o2r project.
