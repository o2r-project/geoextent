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
geoxtent --help
```

to see usage instructions.

## Supported data formats

TODO

## License

`geoextent` is licensed under MIT license, see file LICENSE.

Copyright (C) 2019 - o2r project.
