
.. _design:

Designing Datamodels
====================

Here we describe the process of designing new datamodels for FITS files that do not yet exist in
the SDSS ecosystem.     

.. _designstub:

Creating the Design Stub
------------------------

Desiging a datamodel for a new file is very similar to generating a datamodel for an existing one.  It
consists of generating a YAML datamodel file, which can then be updated with new HDU information.

For the following examples, let's assume we are interested in designing a datamodel for a new MaNGA
FITS file, which will be a new summary catalog file produced by the MaNGA pipeline, for each plate
observed.  The planned file species name is ``mangaCatalog``, and the planned location of this file 
will be ``$MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-catalog-{plate}.fits.gz``, e.g.  
``$MANGA_SPECTRO_REDUX/v3_2_0/8485/stack/manga-catalog-8485.fits.gz``.

When desiging a new datamodel, use the :ref:`datamodel design cli <usage-dmdesign>` or specify 
the ``design=True`` keyword argument when using `~datamodel.generate.DataModel` in Python.

.. tab:: CLI

    Design a datamodel using the command-line:

    .. code-block:: console

        $ datamodel design -f mangaCatalog \
        -p MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-catalog-{plate}.fits.gz

.. tab:: Python

    or from within Python

    .. code-block:: python

        from datamodel.generate import DataModel

        # define the inputs
        file_species = "mangaCatalog"
        path = "MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-catalog-{plate}.fits.gz"

        # generate a datamodel for design purposes 
        dm = DataModel(file_spec=file_species, path=path, design=True)

        # write out the stub files
        dm.write_stubs()


Once the datamodel is "designed", a new YAML file is created at 
``datamodel/products/yaml/mangaCatalog.yaml``, with the following default structure:

.. code-block:: yaml

    general:
      name: mangaCatalog
      short: replace me - with a short one sentence summary of file
      description: replace me - with a longer description of the data product
      datatype: null
      filesize: null
      releases:
      - WORK
      environments:
      - MANGA_SPECTRO_REDUX
      naming_convention: replace me - with $MANGA_SPECTRO_REDUX/[DRPVER]/[PLATE]/stack/manga-catalog-[PLATE].fits
        or  but with regex pattern matches
      generated_by: replace me - with the name(s) of any git or svn product(s) that produces
        this product.
      design: true
    changelog:
      description: Describes changes to the datamodel product and/or file structure from
        one release to another
      releases: {}
    releases:
      WORK:
        template: $MANGA_SPECTRO_REDUX/[DRPVER]/[PLATE]/stack/manga-catalog-[PLATE].fits
        example: null
        location: '{drpver}/{plate}/stack/manga-catalog-{plate}.fits'
        environment: MANGA_SPECTRO_REDUX
        access:
          in_sdss_access: false
          path_name: null
          path_template: null
          path_kwargs: null
          access_string: mangaCatalog = $MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-catalog-{plate}.fits
        hdus:
          hdu0:
            name: PRIMARY
            description: replace me description
            is_image: true
            size: 0 bytes
            header:
            - key: SIMPLE
              value: true
              comment: conforms to FITS standard
            - key: BITPIX
              value: 8
              comment: array data type
            - key: NAXIS
              value: 0
              comment: number of array dimensions

The structure of the designed datamodel YAML is identical to that of datamodels generated for existing 
files, with the following changes:

- A new ``general.design`` flag is set to ``true``.
- Designed datamodels only include a "WORK" release.  Designed datamodel cannot have other releases.
- The ``example`` file is ``null`` because no real file location exists
- Any ``sdss_access`` information is ``null``, since that information is not yet available.
- A mostly empty ``hdus`` section is included, with a single, default ``PRIMARY`` HDU.

The YAML validation remains the same.  To properly validate your designed datamodel, you will need to 
resolve all validation errors e.g. filling in required fields and any "replace me" text.  You can also
take the opportunity to define parameters, e.g. ``datatype`` or the ``access`` parameters necessary
for ``sdss_access``. 

.. _designhdu:

Designing an HDU
----------------




.. _createfile:

Creating a New File
-------------------

When you've finished designing a datamodel and want to test out how it looks in FITS form, you can
easily create a new FITS file from the designed YAML hdus.  From the command-line, specify the 
``-c``, ``--create`` flag.  In order to construct a real file, you will need to specify any necessary
path keyword variables for substitution, using the ``-k``, ``--keyword`` flags, the same when using 
``datamodel generate``.  From Python, call `~datamodel.generate.DataModel.generate_designed_file`, 
passing in all relevant defined path keyword parameters.  In this example, let's create a new test 
file for MaNGA plate 8485, and DRP pipeline version ``v3_2_0``.

.. tab:: CLI

    Create a designed datamodel file using the command-line:

    .. code-block:: console

        $ datamodel design -f mangaCatalog -c -k drpver=v3_2_0 -k plate=8485 \
        -p MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-catalog-{plate}.fits.gz

.. tab:: Python

    or from within Python

    .. code-block:: python

        from datamodel.generate import DataModel

        # define the inputs
        file_species = "mangaCatalog"
        path = "MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-catalog-{plate}.fits.gz"

        # generate a datamodel for design purposes 
        dm = DataModel(file_spec=file_species, path=path, design=True)

        # create a new file
        dm.generate_designed_file(drpver='v3_2_0', plate=8485)

Once we've created the file, we can inspect it in Python with astropy.
:: 

    >>> # see the new datamodel file path
    >>> dm.file
    '/Users/Brian/Work/sdss/sas/mangawork/manga/spectro/redux/v3_2_0/8485/stack/manga-catalog-8485.fits'

    >>> # open the new file
    >>> from astropy.io import fits
    >>> hdulist = fits.open(dm.file)
    >>> hdulist.info()
    Filename: /Users/Brian/Work/sdss/sas/mangawork/manga/spectro/redux/v3_2_0/8485/stack/manga-catalog-8485.fits
    No.    Name      Ver    Type      Cards   Dimensions   Format
      0  PRIMARY       1 PrimaryHDU       5   ()

When you create a new file, you will exit the datamodel design phase. The ``design`` flag will be set 
to ``False``, and the ``example`` parameter will be populated with your new file.
