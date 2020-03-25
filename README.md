[![Build Status](https://travis-ci.org/o2r-project/geoextent.svg?branch=master)](https://travis-ci.org/github/o2r-project/geoextent)

# geoextent

Python library for extracting geospatial extent of files and directories with multiple data formats

This project is developed as part of the [DFG-funded](https://o2r.info/about/#funding) research project Opening Reproducible Research (o2r, https://o2r.info).

## Installation

**System requirements**

Python: `3.x`

The package relies on common system libraries for reading geospatial datasets, such as GDAL and NetCDF.
On Debian systems, the [UbuntuGIS](https://wiki.ubuntu.com/UbuntuGIS) project offers easy installation of up to date versions of those libraries.

See the `packages` list in `travis.yml` for a full list of dependencies on Linux.

**Install from PyPI**

```bash
pip install geoextent
```

**Source installation**

```bash
git clone https://github.com/o2r-project/geoextent
cd geoextent
pip install -r requirements.txt

pip install -e .
```

**System requirements**

- see `travis.yml`

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

## License

`geoextent` is licensed under MIT license, see file [LICENSE](https://github.com/o2r-project/geoextent/blob/master/LICENSE).

Copyright (C) 2020 - o2r project.
