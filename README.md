# datamodel

![Versions](https://img.shields.io/badge/python->3.7-blue)
[![Documentation Status](https://readthedocs.org/projects/sdss-datamodel/badge/?version=latest)](https://sdss-datamodel.readthedocs.io/en/latest/?badge=latest)
[![Build and Test](https://github.com/sdss/datamodel/actions/workflows/build.yml/badge.svg)](https://github.com/sdss/datamodel/actions/workflows/build.yml)
[![Build Sphinx Docs](https://github.com/sdss/datamodel/actions/workflows/sphinx.yml/badge.svg)](https://github.com/sdss/datamodel/actions/workflows/sphinx.yml)
[![codecov](https://codecov.io/gh/sdss/datamodel/branch/main/graph/badge.svg)](https://codecov.io/gh/sdss/datamodel)

## SDSS-V Datamodel Project

For complete documentation, see the [Datamodel Docs](https://internal.sdss.org/docs/datamodel/latest/index.html)


## Installation

First clone the repo locally:
```
git clone https://github.com/sdss/datamodel datamodel
cd datamodel
```

To install the basic package for programmatic access to validated datamodels only, run:
```
pip install -e .
```

To generate new datamodels for testing and development, run:
```
pip install -e ".[test]"
```

To install everything, including packages for `hdf5` and `par` file support, run:
```
pip install -e ".[all]"

```

## Documentation

To build and view the Sphinx documentation locally, run the following commands from within the top level of the checked out git repo.  Note, this command requires `sdsstools` to be pip installed.
```
sdss docs.build
sdss docs.show
```

## Usage

After pip installation, see available command line tools with `datamodel --help`:

```
Usage: datamodel [OPTIONS] COMMAND [ARGS]...

  Command-line tool for handling SDSS datamodels

Options:
  --help  Show this message and exit.

Commands:
  design    Design a new datamodel for a new file
  generate  Generate a datamodel file for a SDSS data product
  install   Install a user copy of the datamodel product at Utah
  wiki      Upload a datamodel markdown file to the wiki
```

For help on any sub-commands, type `datamodel [command] --help`.  Information on the available command options is also available in the Sphinx docs.

**Note:**  if you did not install with pip, but instead installed the datamodel product via modules pointing to the git repo, then you will not have access to the ``datamodel`` click command.  You can either directly run `python python/datamodel/cli.py --help` or, for
backwards compatibility, you can still use the original snake_case scripts,
i.e. use ``datamodel_generate`` rather than ``datamodel generate``.  These will call the underlying cli.
