
datamodel's documentation
=============================================

This is the documentation for the SDSS Python product datamodel. The current version
is |datamodel_version|. You can install the package by doing

.. code-block:: console

  $ git clone https://github.com/sdss/datamodel
  $ cd datamodel
  $ pip install -e .

By default the datamodel package supports FITS files only.  Support for additional file types requires
extra dependency packages to be installed.

.. list-table:: Supported Files
   :widths: 25 25 25 25
   :header-rows: 1

   * - Filetype
     - Suffix
     - Package
     - Install Command
   * - FITS
     - .fits
     - `astropy <https://docs.astropy.org/en/stable/>`_
     - N/A
   * - Yanny files
     - .par
     - `pydl <https://pydl.readthedocs.io/en/latest/>`_
     - ".[par]"
   * - HDF5 files
     - .h5
     - `h5py <https://docs.h5py.org/en/stable/>`_
     - ".[hdf]"

To install all extra file dependencies, run ``pip install -e ".[all]"`` during the installation process.

The sdss ``datamodel`` product is a python package for creating, validating, and navigating
datamodels for SDSS data products.

.. toctree::
  :maxdepth: 2
  :caption: Content

  Generating Datamodels <generate>
  Navigating Datamodels <navigate>
  Designing Datamodels <design>
  Examples - Generate <examples_generate>
  Examples - Design <examples_design>

.. toctree::
   :maxdepth: 1
   :caption: Reference

   api
   CHANGELOG
   commands
   adding_files

