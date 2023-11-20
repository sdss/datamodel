
.. _adding:

Adding New Files
================

To add support for new filetypes to the SDSS DataModel product, here are the steps to follow.

1. :ref:`dmupdate`
2. :ref:`dmfilegen`
3. :ref:`dmyaml`
4. :ref:`dmmd`
5. :ref:`dmchange`
6. :ref:`dmchangemodels`
7. :ref:`dmdesign`
8. :ref:`dmtests`
9. :ref:`dmdocs`
10. :ref:`dmpr`

.. _dmupdate:

Update the DataModel
--------------------

Add the file suffix or extension to the list of supported filetypes on the
`~datamodel.generate.datamodel.DataModel` class in ``datamodel/generate/datamodel.py``.

::

    class DataModel:
        supported_filetypes = ['.fits', '.par', '.h5']

.. _dmfilegen:

Create a New File Generator
---------------------------

Create a new python file under ``datamodel/generate/filetypes/``, with the name of your new file suffix. In
this file, create a new class subclassed from `~datamodel.generate.filetypes.base.BaseFile`. For example,

::

    from .base import BaseFile

    class FitsFile(BaseFile):
        """ Class for supporting FITS files """
        suffix = 'FITS'
        cache_key = 'hdus'

This is the class that will be used to generate the new file.  It requires several class attributes and methods
to be defined.  It requires the following class attributes:

- **suffix**: An uppercase name of the file extension or suffix
- **cache_key**: The key name used to store the data values in the YAML cache

Each new subclass must minimally override and define the following class methods:

- `~datamodel.generate.filetypes.base.BaseFile._generate_new_cache`: creates and returns the initial dictionary data that populates the ``cache_key`` YAML key
- `~datamodel.generate.filetypes.base.BaseFile._update_partial_cache`: updates the cache of new releases with any cache content from old releases, e.g. field descriptions
- `~datamodel.generate.filetypes.base.BaseFile.design_content`: when designing datamodels, updates a YAML cache with content via Python
- `~datamodel.generate.filetypes.base.BaseFile._get_designed_object`: when designing datamodels, creates a new object representation of the file from the YAML cache
- `~datamodel.generate.filetypes.base.BaseFile.write_design`: when designing datamodels, generates a new designed template file on disk

These methods are customized for each file type.  The first two methods in the list above pertain to generating
the initial cache content, and partially updating new cache with older cache data.  The last three methods
are specifically for designing new datamodels when the files do not yet exist on disk.  If this functionality
is not desired, simply create empty placeholder methods.

See the existing `~datamodel.generate.filetypes.fits.FitsFile`, `~datamodel.generate.filetypes.par.ParFile`, and
`~datamodel.generate.filetypes.hdf5.HdfFile` example classes for implementation details.

.. _dmyaml:

Describe the YAML representation
--------------------------------

To convert YAML files to validated JSON files, we need to describe the YAML structure in Python format, and the
rules necessary to validate the YAML content to ensure its of the proper format.  We use
`Pydantic <https://pydantic-docs.helpmanual.io/>`_ to construct model class representations of the
YAML content and to handle type validation.

Create a new python file under ``datamodel/models/filetypes/``, with the name of your new file suffix. In
this file, create a new class subclassed from Pydantic's `BaseModel <https://pydantic-docs.helpmanual.io/usage/models/>`_.
For example,
::

    from typing import List, Dict
    from pydantic import BaseModel

    class HDU(BaseModel):
        """ Pydantic model representing a YAML hdu section """

        name: str
        is_image: bool
        description: str
        size: str
        header: List[Header] = None
        columns: Dict[str, Column] = None

Every field or object in YAML must be represented in the model, either as an attribute on a given Pydantic model,
or as a Model itself.  Models can be nested and chained together to create more complex structures.  See, for
example, the `~datamodel.models.filetypes.fits.Header`, `~datamodel.models.filetypes.fits.Column`, and
`~datamodel.models.filetypes.fits.HDU` models that describe the YAML content of an individual FITS HDU.
Also see the existing `~datamodel.models.filetypes.fits.HDU`, `~datamodel.models.filetypes.par.ParModel`, and
`~datamodel.models.filetypes.hdf5.HdfModel` example classes for complete implementation details.

Once the relevant models are created, we must add them to our global `~datamodel.models.yaml.YamlModel`, in
``datamodel.models.yaml.py``.  In the `~datamodel.models.yaml.Release` model, add a new attribute with the
name of the ``cache_key``, e.g. ``hdus``. Set the default to ``None`` so the field is an optional one.
For example,
::

    class Release(BaseModel):
        """ Pydantic model representing an item in the YAML releases section """
        hdus: Dict[str, HDU] = None
        par: ParModel = None
        hdfs: HdfModel = None


.. _dmmd:

Create a Markdown Stub
----------------------

Create a new markdown file under ``datamodel/templates/md/``, with the name of your new file suffix. This file
uses `Jinja <https://jinja.palletsprojects.com/en/3.1.x/>`_ template syntax.  The new file must extend the
``md/base.md`` file, i.e. ``{% extends "md/base.md" %}``. It also must contain the following two jinja ``blocks``.

- **content**: A list of structures in the file, displayed in the example, e.g. FITS HDUs or Yanny tables
- **example**: Any content from the YAML ``cache_key`` to display

For example,

.. code-block:: jinja

    {% block content %}
    {% for table in data['tables'] %}
    - [{{table}}](#{{table}})
    {% endfor %}
    {% endblock content %}

    {# Example par rendering for the example block #}
    {% block example %}
    ....
    {% endblock example %}

The YAML cache content specified in the ``cache_key`` field is available to your new markdown file as the
``data`` attribute, as a dictionary.  By default the data values used for populating the example will
come from the "WORK" release, or if not available, the latest DR release in the model.

See the examples in ``templates/md/fits.md``, ``templates/md/par.md``, and ``templates/md/h5.md`` for
implementation details.

.. _dmchange:

Create a Changelog Generator
----------------------------

Create a new python file under ``datamodel/generate/changelog/filetypes/``, with the name of your new file
suffix. In this file, create a new class subclassed from `~datamodel.generate.changelog.yaml.YamlDiff`. For
example,

::

    from datamodel.generate.changelog.yaml import YamlDiff

    class YamlFits(YamlDiff):
        """ Class for supporting YAML changelog generation for FITS files """
        suffix = 'FITS'
        cache_key = 'hdus'

This is the class that will be used to generate the changelog between releases for the new file.  It requires
several class attributes and methods to be defined.  It requires the following class attributes:

- **suffix**: An uppercase name of the file extension or suffix
- **cache_key**: The key name used to store the data values in the YAML cache

Each new subclass must minimally override and define the following class methods:

- `~datamodel.generate.changelog.yaml.YamlDiff._get_changes`: creates and returns the dictionary data that populates the ``changelog.releases`` YAML key.

This method is customized for each file type.  Its inputs are the two YAML ``cache_key`` values from one
release, and the release prior. It should return a dictionary of desired computed changes between the
two releases.  If this functionality is not desired, simply create empty placeholder methods.

See the existing `~datamodel.generate.changelog.filetypes.fits.YamlFits`,
`~datamodel.generate.changelog.filetypes.par.YamlPar`, and
`~datamodel.generate.changelog.filetypes.hdf5.YamlHDF5` example classes for implementation details.

.. _dmchangemodels:

Create Changelog Models
-----------------------

In the python file containing our new Pydantic models, we must also create new models for the changelog.  These
are created in a similar fashion to models as described above.  For example,
::

    class ChangeFits(BaseModel):
        """ Pydantic model representing the FITS hdu fields of the YAML changelog release section """
        delta_nhdus: int = None
        added_hdus: List[str] = None
        removed_hdus: List[str] = None
        primary_delta_nkeys: int = None
        added_primary_header_kwargs: List[str] = None
        removed_primary_header_kwargs: List[str] = None

See `~datamodel.models.filetypes.fits.ChangeFits`, `~datamodel.models.filetypes.par.ChangePar`, and
`~datamodel.models.filetypes.hdf5.ChangeHdf` example classes for complete implementation details.

Once our new models are created, the core model must be added to the list of subclasses in the
`~datamodel.models.yaml.ChangeRelease` model in ``datamodel/models/yaml.py``.  See
::

    class ChangeRelease(ChangeHdf, ChangePar, ChangeFits, ChangeBase):
        pass

To maintain proper field ordering, it must be added to the front of the list, e.g.
``ChangeRelease([NewModel], ChangeHdf, ChangePar, ChangeFits, ChangeBase)``.

.. _dmdesign:

Add DataModel Design Code
-------------------------

To add the option of users designing datamodels for the new file before it exists, you need to override the
following three methods in your file generation python file.

- `~datamodel.generate.filetypes.base.BaseFile.design_content`: when designing datamodels, updates a YAML cache with content via Python
- `~datamodel.generate.filetypes.base.BaseFile._get_designed_object`: when designing datamodels, creates a new object representation of the file from the YAML cache
- `~datamodel.generate.filetypes.base.BaseFile.write_design`: when designing datamodels, generates a new designed template file on disk

Designing New Content
^^^^^^^^^^^^^^^^^^^^^

On your new file class, override the `~datamodel.generate.filetypes.base.BaseFile.design_content` method, and
customize it for the specifics of the new file.  It should parse the Python inputs and convert them into the
proper YAML datamodel structure, populating the content in the ``cache_key`` field.  For example, see FITS
`~datamodel.generate.filetypes.fits.FitsFile.design_content` method for implementation details of parsing input
Python into the YAML hdus dictionary content.  Also see the Yanny par
`~datamodel.generate.filetypes.par.ParFile.design_content` and HDF5 `~datamodel.generate.filetypes.hdf5.HdfFile.design_content`
methods for details on other filetypes.

Once you've created the above method, you need to add a new ``design_xxx`` convenience method to the
`~datamodel.generate.datamodel.DataModel` class, which passes your desired inputs into the private
``_design_content`` method.  This is a convenience for users to easily design new YAML content directly
from a datamodel instance. For example, the convenient ``design_hdu`` method for FITS files looks like:
::

    def design_hdu(self, ext: str = 'primary', extno: int = None, name: str = 'EXAMPLE',
                   description: str = None, header: Union[list, dict, fits.Header] = None,
                   columns: List[Union[list, dict, fits.Column]] = None, **kwargs):
        """ Wrapper to _design_content, to design a new HDU """
        self._design_content(ext=ext, extno=extno, name=name, description=description,
                            header=header, columns=columns, **kwargs)

Creating the File
^^^^^^^^^^^^^^^^^

To create a new file object on disk, we need to convert the YAML content to a valid file representation
and we need to write out that file to disk.

First we need to override the `~datamodel.generate.filetypes.base.BaseFile._get_designed_object` method.
This is a static method whose input is the ``cache_key`` YAML dictionary content for the new file.  It should
return a new file object representation.  This method gets called by
`~datamodel.generate.filetypes.base.BaseFile.create_from_cache` and makes the new object available as the
``_designed_object`` attribute.  This method should create a new file by parsing and validating the YAML content
through its Pydantic model and calling a ``convert_xxx`` method to convert the Pydantic model to the new file.
For example, the method for FITS conversion look like:
::

    @staticmethod
    def _get_designed_object(data: dict):
        """ Return a valid fits HDUList """
        return fits.HDUList([HDU.model_validate(v).convert_hdu() for v in data.values()])

with the `~datamodel.models.filetypes.fits.HDU.convert_hdu` method:
::

    class HDU(BaseModel):
        ...

        def convert_header(self) -> fits.Header:
            """ Convert the list of header keys into a fits.Header """
            if not self.header:
                return None
            return fits.Header(i.to_tuple() for i in self.header)

        def convert_columns(self) -> List[fits.Column]:
            """ Convert the columns dict into a a list of fits.Columns """
            if not self.columns:
                return None
            return [i.to_fitscolumn() for i in self.columns.values()]

        def convert_hdu(self) -> Union[fits.PrimaryHDU, fits.ImageHDU, fits.BinTableHDU]:
            """ Convert the HDU entry into a valid fits.HDU """
            if self.name.lower() == 'primary':
                return fits.PrimaryHDU(header=self.convert_header())
            elif self.columns:
                return fits.BinTableHDU.from_columns(self.convert_columns(), name=self.name,
                                                    header=self.convert_header())
            else:
                return fits.ImageHDU(name=self.name, header=self.convert_header())

See also the `~datamodel.models.filetypes.par.ParModel.convert_par` and
`~datamodel.models.filetypes.hdf5.HdfModel.convert_hdf` methods for details on other filetypes.

Since different file packages have different mechanisms of writing to disk, we need to override the
`~datamodel.generate.filetypes.base.BaseFile.write_design` method and customize our write method for the
specifics of the file object.  The method should use the ``self._designed_object`` attribute, which contains
the file object itself.  For example, the method for writing out a new FITS file looks like:
::

    def write_design(self, file: str, overwrite: bool = True) -> None:
        """ Write out the designed file """
        if not self._designed_object:
            raise AttributeError('Cannot write.  Designed object does not exist.')

        self._designed_object.writeto(file, overwrite=overwrite, checksum=True)

.. _dmtests:

Add New Tests
-------------

All the tests are designed around creating a datamodel for a file species "test", located
at ``$TEST_REDUX/{ver}/testfile_{id}.{suffix}`` where supported filetypes fill in the ``suffix`` field.

In ``tests/conftest.py``, create a new ``create_xxx`` function for your new filetype.  This function creates
a new test file.  For example,
::

    def create_fits(name, version, extra_cols):
        """ create a test fits hdulist """
        # create the FITS HDUList
        header = fits.Header([('filename', name,'name of the file'),
                            ('testver', version, 'version of the file')])
        primary = fits.PrimaryHDU(header=header)
        imdata = fits.ImageHDU(name='FLUX', data=np.ones([5,5]))
        cols = [fits.Column(name='object', format='20A', array=['a', 'b', 'c']),
                fits.Column(name='param', format='E', array=np.random.rand(3), unit='m'),
                fits.Column(name='flag', format='I', array=np.arange(3))]
        if extra_cols:
            cols.extend([fits.Column(name='field', format='J', array=np.arange(3)),
                        fits.Column(name='mjd', format='I', array=np.arange(3))])
        bindata = fits.BinTableHDU.from_columns(cols, name='PARAMS')

        return fits.HDUList([primary, imdata, bindata])

Update the ``create_test_file`` where appropriate to call the new ``create_xxx`` method.

Add a new validated test yaml file for in ``tests/data/``.  Copy an existing test YAML file and modify it
for your new test filetype.  The validated YAML content should match the content created in the ``create_xxx``
method.

In ``tests/conftest.py``, add your new file extension to the list of suffixes ``suffixes = ['fits', 'par', 'h5']
```.

The above setup will automatically add the new filetype to some of the test suite.  Additional tests can be
added.  Minimally a new design test specific to the new filetype should be added to
the ``tests/generate/test_design.py`` file.

.. _dmdocs:

Update the Documentation
------------------------

Update the Sphinx documentation with all relevant documentation pertaining to the new supported filetype.

- Add your autodoc module API references to the ``api.rst`` file.
- Update the "Supported Filetypes" table in the ``index.rst`` file.
- Add the new filetype to the list of supported files in the ``generate.rst`` file.
- Update the docs in ``generate.rst`` with a new section of caveats for generating your file.
- Update the docs in ``design.rst`` with a new sections on designing your file.
- Add a new example to the ``examples_generate.rst`` file.
- If needed add examples to the ``examples_design.rst`` file.

You can build the docs locally using the ``sdsstools`` command ``sdss docs.build`` and ``sdss docs.show``
to open the local docs in your browser.

.. _dmpr:

Submit a Pull Request
---------------------

Submit a `Github PR <https://github.com/sdss/datamodel/pulls>`_ for review.  Follow the instructions to
`Create a PR <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request>`_.
Make sure the PR passes all `Checks <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/about-status-checks>`_.
