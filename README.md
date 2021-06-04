# datamodel

![Versions](https://img.shields.io/badge/python->3.7-blue)
[![Documentation Status](https://readthedocs.org/projects/sdss-datamodel/badge/?version=latest)](https://sdss-datamodel.readthedocs.io/en/latest/?badge=latest)
[![Travis (.org)](https://img.shields.io/travis/sdss/datamodel)](https://travis-ci.org/sdss/datamodel)
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