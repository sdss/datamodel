.. _datamodel-changelog:

==========
Change Log
==========

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


