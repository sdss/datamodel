.. _datamodel-changelog:

==========
Change Log
==========

0.5.1 (unreleased)
------------------
- Refactored internal git code to use ``GitPython`` package
- Change to datamodel to force work in a new git branch, outside of the main branch
- Adds new tests for install and git modules of the datamodel

0.5.0 (05-02-2022)
------------------
- Added support for HDF5 files (PR :pr:`40`)
- Refactored code for easier addition of new file types
- Updating docs for adding new filetypes
- Moves `pydl` and `h5py` packages to extras dependencies

0.4.2 (02-22-2022)
------------------
- Fix issue :issue:`37` - add missing enum support to Yanny par datamodels

0.4.1 (02-11-2022)
------------------
- Fixed bug when environment is not defined in tree but defined locally

0.4.0 (02-11-2022)
------------------
- Added support for Yanny parameter files (PR :pr:`36`)
- Refactored code for easier addition of new file types
- Removed remaining deprecated wiki code and references

0.3.3 (01-07-2022)
------------------
- Removed all references to the old datamodel wiki code, now deprecated for the DSI
- Fix to Github Action to build sphinx documentation
- Fix issue :issue:`28` - duplicate access path keywords
- Fix issue :issue:`19` - invalid file_species when "-" present
- Fix issue :issue:`32` - new table columns not present in old caches
- Fix issue :issue:`34` - improved access path validation


0.3.2 (07-08-2021)
------------------
- Bug fixing issue :issue:`13` keyword requirement when no keywords in path
- Issue :issue:`14` - adds Release model to yaml; sorts releases/changelog by release_date
- Issue :issue:`15` - verifies paths with special functions work
- Adds new `access_path_name` field to `DataModel` to allow for case when sdss_access path names different than file species names

0.3.1 (07-02-2021)
------------------
- Bug fix in YAML changelog boolean logic

0.3.0 (07-02-2021)
------------------
- Adds basic Python object representation of data products and metadata models
- See new product classes `~datamodel.products.product.SDSSDataModel`, `~datamodel.products.product.DataProducts`, `~datamodel.products.product.Product`
- See new metadata model classes, `~datamodel.models.releases.Releases`, `~datamodel.models.surveys.Surveys`, and `~datamodel.models.surveys.Phases`

0.2.0 (06-04-2021)
------------------
- Refactored datamodel to allow for data release versioning. Public, internal, or "work" releases.
- Renamed `data` directory to `datamodel`.
- Refactored datamodel products directory structure around file_species, `datamodel/products/yaml/xxx.yaml`
- Added YAML validation before production of any markdown, JSON, or access files
- Updated Sphinx documentation

0.1.0 (02-10-2021)
------------------
- Initial tag and release of datamodel code
- Captures original functionality of SDSS-IV datamodel


