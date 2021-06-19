# datamodel

![Versions](https://img.shields.io/badge/python->3.7-blue)
[![Documentation Status](https://readthedocs.org/projects/sdss-datamodel/badge/?version=latest)](https://sdss-datamodel.readthedocs.io/en/latest/?badge=latest)
[![Build and Test](https://github.com/sdss/datamodel/actions/workflows/build.yml/badge.svg)](https://github.com/sdss/datamodel/actions/workflows/build.yml)
[![Build Sphinx Docs](https://github.com/sdss/datamodel/actions/workflows/sphinx.yml/badge.svg)](https://github.com/sdss/datamodel/actions/workflows/sphinx.yml)
[![codecov](https://codecov.io/gh/sdss/datamodel/branch/main/graph/badge.svg)](https://codecov.io/gh/sdss/datamodel)

SDSS-V Datamodel Project


To clone and install the product locally:

```
git clone https://github.com/sdss/datamodel datamodel
cd datamodel
pip install -e ".[dev,docs]"

```

To install it in an isolated conda environment:
```
conda create -n datamodel python=3.8 ipython
conda activate datamodel
pip install -e ".[dev,docs]"
```

To build and view the Sphinx documentation locally, run the following commands from within the top level of the checked out git repo.  Note, this command requires `sdsstools` to be pip installed.
```
sdss docs.build
sdss docs.show
```

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