
.. _generate:

Generating Datamodels
=====================

Here we describe the process of generating new datamodels for existing SDSS files.  

Supported Filetypes
-------------------

Currently the datamodel product supports generating datamodels for the following filetypes:

- FITS: a common astronomy data format
- `"Yanny" parameter files <https://www.sdss.org/dr17/software/par/>`_: human- and machine-readable ASCII parameter (.par) files

The basic procedure for generating datamodels is the same, regardless of filetype.  All of the following code examples 
below are for generating datamodels for FITS files.  The same procedure can be used for generating datamodels for Yanny files.  
See the :ref:`yanny` section for explicit differences. See :ref:`examples` for code and output YAML datamodels for supported
filetypes.

Generating a datamodel
----------------------

Datamodels are documented metadata representations of data products, e.g. FITS files.  Since pipelines
can produce many different files of the same data product, e.g. with different input parameters, for
different target names or different pipeline analysis settings, we generate a single datamodel file
for a set, or "species", of data products.  This "file_species" is a representative name for all
files of a given data product, e.g. all MaNGA IFU data cubes get a single ``mangaCube`` file
species name.  Associated with a file species is a symbolic path that is a representative file path
for all files of that data product.  For example, the symbolic path to MaNGA IFU data cubes is
``$MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}CUBE.fits.gz``, where the items
in brackets, e.g. ``{plate}`` are variables to be substituted and represent parameters that can change for
individual files or files across different releases.  An example of a resolved path would be
``$MANGA_SPECTRO_REDUX/v2_4_3/8485/stack/manga-8485-1901-LOGCUBE.fits.gz``.  The file species and
symbolic path are similar to the syntax of entries in the ``sdss_access`` and ``tree`` products.
See the `Tree Path Template Syntax <https://sdss-tree.readthedocs.io/en/latest/paths.html#define-a-new-path-template>`_
for more information.

**Required Inputs**:

- **file_species**: A short name of the "species" of the file, similar to an ``sdss_access`` entry name
- **path**: An abstract file path, starting with a root environment variable, and using `Jinja2 <https://jinja.palletsprojects.com/en/3.0.x/>`_ template variable syntax, similar to an ``sdss_access`` entry path
- **keywords**: A list of keyword-value pairs, of an example file, matching the path template variable names

**Release Inputs**:

- **tree_ver**: the SDSS tree configuration name the data product is associated with.  Useful when working with modules or "work" releases.
- **release**: the data release of the data product

All the following examples walk through the creation of a datamodel for the
MaNGA Row-Stacked Spectra (RSS) data product.  Let's create the datamodel for
the MaNGA RSS file for Data Release 15 (DR15).

.. tab:: CLI

    Generate a datamodel using the command-line:

    .. code-block:: console

        $ datamodel generate -f mangaRss \
        -p MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz \
        -k plate=8485 -k ifu=1901 -k drpver=v2_4_3 -k wave=LOG -r DR15

.. tab:: Python

    or from within Python

    .. code-block:: python

        from datamodel.generate import DataModel

        # define the inputs
        file_species = "mangaRss"
        path = "MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz"
        keys = ['plate=8485', 'ifu=1901', 'drpver=v2_4_3', 'wave=LOG']

        # generate a datamodel for Data Release 15 (DR15)
        dm = DataModel(file_spec=file_species, path=path, keywords=keys, release='DR15')

        # write out the stub files
        dm.write_stubs()

As inputs, we pass in the name of the file species, the symbolic path to the file, the list of
example keyword-value pairs, and the release we're interested in.  See the
:ref:`datamodel generate cli <usage-dmgen>` for a full list of command-line arguments.

.. note::
  In 0.2.1, the cli code and syntax changed from argparse to click.  See :ref:`cli-diff` for more.

After we run the command, a stub YAML datamodel file will be created.  The code will also attempt to write
a valid markdown file, a JSON file, and access file.  These files are automatically produced and do not require
any user modification.  During the initial YAML file creation, it will produce an unvalidated
YAML file.  The additional files only get written out if, and when, the YAML file is validated.
See :ref:`yaml` and :ref:`validate` below for the next steps.

.. _yaml:

The YAML structure
------------------

The YAML file is the main entry point for adding custom content, and is the only file you will need to
modify.  The structure of the YAML is broken up into the following sections:

- **general** - section containing general information and metadata on the data product
- **changelog** - automatically populated section containing any FITS file changes between data releases
- **releases** - section of information specific for a release
    - **access** - a section containing information on any existing sdss_access entry
    - **hdus** - a section for each HDU in the FITS file (only for FITS files)
    - **par** - a section containing the header and table content in the par file (only for Yanny files)

Most of the YAML content is automatically generated.  Values containing the text **replace me** are
areas to be replaced with user custom content, e.g. descriptions of the data product, individual
descriptions of HDU content, column units, etc.  A truncated example of the newly created
unvalidated ``datamodel/products/yaml/mangaRSS.yaml`` file is below:

.. tab:: FITS Yaml

    Example yaml datamodel for the MaNGA RSS FITS file, shortened for brevity

    .. code-block:: yaml

        general:
          name: mangaRss
          short: replace me - with a short one sentence summary of file
          description: replace me - with a longer description of the data product
          datatype: FITS
          filesize: 14 MB
          releases:
            - DR15
          environments:
            - MANGA_SPECTRO_REDUX
          naming_convention: replace me - with $MANGA_SPECTRO_REDUX/[DRPVER]/[PLATE]/stack/manga-[PLATE]-[IFU]-[WAVE]RSS.fits.gz
            or manga-8485-1901-LOGRSS.fits.gz but with regex pattern matches
          generated_by: replace me - with the name(s) of any git or svn product(s) that produces
            this product.
        changelog:
          description: Describes changes to the datamodel product and/or file structure from
            one release to another
          releases: {}
        releases:
          DR15:
            template: $MANGA_SPECTRO_REDUX/[DRPVER]/[PLATE]/stack/manga-[PLATE]-[IFU]-[WAVE]RSS.fits.gz
            example: v2_4_3/8485/stack/manga-8485-1901-LOGRSS.fits.gz
            location: '{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz'
            environment: MANGA_SPECTRO_REDUX
            access:
              in_sdss_access: true
              path_name: mangarss
              path_template: $MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz
              path_kwargs:
                - plate
                - drpver
                - wave
                - ifu
              access_string: mangaRss = $MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz
            hdus:
              hdu0:
                name: PRIMARY
                description: replace me description
                is_image: true
                size: 0 bytes
                header:
                  - key: SIMPLE
                    value: true
                    comment: ''
              hdu1:
                ...

.. _validate:

Validating datamodels
---------------------

When we first create a datamodel, we will get an unvalidated YAML file.  In the above example, we get a
new YAML file at ``datamodel/products/yaml/mangaRss.yaml``.  During the creation, you may see some log
output in the terminal of something like the following:
::

    [INFO]: Preparing datamodel: <DataModel(file_species='mangaRss', release='WORK')>.
    [INFO]: Creating stub: <Stub(format="yaml", file_species="mangaRss", release="WORK")>
    [INFO]: Creating stub: <Stub(format="access", file_species="mangaRss", release="WORK")>
    [ERROR]: 148 validation errors for YamlModel
    general -> short
      Generic text needs to be replaced with specific content! (type=value_error)
    general -> description
      Generic text needs to be replaced with specific content! (type=value_error)
    general -> naming_convention
      Generic text needs to be replaced with specific content! (type=value_error)
    ...
    [INFO]: yaml cache is not validated!
    [INFO]: No cache content to write out!

This indicates there are validation errors in the YAML file, and the remaining stubs cannot be produced.
At this stage, we need to resolve all validation errors, e.g. supplying required information, or replacing
all generic text with custom user content.  Once a YAML file is validated, we re-run the same
``datamodel_generate`` command from above to produce the remaining files in ``datamodel/products/``:

- **md/mangaRss.md**: the markdown file for human-readable representation on the DSI
- **json/mangaRss.json**: a machine-readable JSON file for the ``datamodel`` python package
- **access/mangaRss.access**: a subset YAML file containing access information

When writing out the stubs, a successfully valid YAML will produce the following verbose output:
::

    [INFO]: Preparing datamodel: <DataModel(file_species='mangaRss', release='DR15')>.
    [INFO]: Creating stub: <Stub(format="yaml", file_species="mangaRss", release="DR15")>
    [INFO]: Creating stub: <Stub(format="access", file_species="mangaRss", release="DR15")>
    [INFO]: Creating stub: <Stub(format="md", file_species="mangaRss", release="DR15")>
    [INFO]: Creating stub: <Stub(format="json", file_species="mangaRss", release="DR15")>

Adding new releases
-------------------

There is now only a single datamodel file for each unique file species, for all releases.  New releases
can be added to the existing datamodel file by rerunning the ``datamodel_generate`` command with the
proper new inputs.  Valid releases are any new public data releases (e.g. DR15, DR16), internal
data releases (e.g. MPL4, IPL1), or a "WORK" release.  Datamodels can now be generated for any data
product that is private or as-yet-unreleased in a data release, i.e. any path or entry normally defined
in ``tree`` ``sdsswork.cfg`` or ``sdss5.cfg``.  These unreleased products are captured in a
single "WORK" release.  There can only be one "WORK" release at a time per data product, and
represents the most recent updated file one is currently working on.

Adding a public release with complete cache
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All user-defined content in the YAML file is cached and can be transferred from one release to the
next, with different options available depending on the use case.  Let's add a new entry in the
``mangaRss.yaml`` file for release DR16.  The MaNGA DR16 release is exactly the same as the DR15
release, so in this case, we want to transfer the entire YAML content from DR15 to DR16.

.. tab:: CLI

    From the command-line, we specify release DR16, and use the ``--use-cache``, or ``-c``, to instruct
    it to use the DR15 cache content. 

    .. code-block:: console

        $ datamodel generate -f mangaRss \
        -p MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz \
        -k plate=8485 -k ifu=1901 -k drpver=v2_4_3 -k wave=LOG -r DR16 --use-cache DR15

.. tab:: Python

    From python, we specify the ``use_cache_release`` and ``full_cache``
    keyword arguments to :py:func:`~datamodel.generate.datamodel.DataModel.write_stubs`.

    .. code-block:: python

        from datamodel.generate import DataModel

        # define the inputs
        file_species = "mangaRss"
        path = "MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz"
        keys = ['plate=8485', 'ifu=1901', 'drpver=v2_4_3', 'wave=LOG']

        # generate a datamodel for Data Release 16 (DR16)
        dm = DataModel(file_spec=file_species, path=path, keywords=keys, release='DR16')

        # write out the stub files with the complete DR15 cache
        dm.write_stubs(use_cache_release='DR15', full_cache=True)

In the YAML file, you should see DR16 in the general-releases list, as well as a new entry
in the ``releases`` section.
::

    general
      releases:
        - DR15
        - DR16
    release:
      DR15: &id001
        ...
      DR16: *id001

Since DR16 is complete copy of DR15, the content will be "linked" to the DR15 with YAML anchor syntax.

Adding a new internal release with partial cache
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now let's add a new internal release to the ``mangaRss.yaml`` for MaNGA MPL-10.  This release is mostly
the same as DR15 but has a few changes.  One, it was produced with a different tag of the MaNGA pipeline,
``v3_0_1`` instead of ``v2_4_3``, and two, it contains changes the internal HDU structure of the
FITS file.  In this case, we want to use only the HDU cache custom content from DR15.

.. tab:: CLI

    From the command-line, we specify release MPL10, the ``--use-cache`` argument for DR15, and now the
    ``-hdus-only`` flag.

    .. code-block:: console

        $ datamodel generate -f mangaRss \
        -p MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz \
        -k plate=8485 -k ifu=1901 -k drpver=v3_0_1 -k wave=LOG -r MPL10 --use-cache DR15 --hdus-only

.. tab:: Python

    From python, we specify only the ``use_cache_release`` keyword arguments to
    :py:func:`~datamodel.generate.datamodel.DataModel.write_stubs`.

    .. code-block:: python

        from datamodel.generate import DataModel

        # define the inputs
        file_species = "mangaRss"
        path = "MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz"
        keys = ['plate=8485', 'ifu=1901', 'drpver=v3_0_1', 'wave=LOG']

        # generate a datamodel for internal release MPL-10
        dm = DataModel(file_spec=file_species, path=path, keywords=keys, release='MPL10')

        # write out the stub files with the partial DR15 cache
        dm.write_stubs(use_cache_release='DR15')

When we write out the stubs, we notice new validation errors, instructing us the YAML file is no longer
validated, and the markdown and JSON files have **not** been updated.  These new validation errors are
due to the changes in the FITS HDU data structure.  We've removed HDUs ``PREDISP`` and ``DISP`` and added
HDUs ``LSFPOST`` and ``LSFPRE``. We need to first validate these components and re-run the
relevant commands to fully update and write out all the content. (We won't do this here.)
::

    [ERROR]: 2 validation errors for YamlModel
    releases -> MPL10 -> hdus -> hdu4 -> description
      Generic text needs to be replaced with specific content! (type=value_error)
    releases -> MPL10 -> hdus -> hdu5 -> description
      Generic text needs to be replaced with specific content! (type=value_error)

Adding a WORK release
^^^^^^^^^^^^^^^^^^^^^

Now let's add a new file into the ``mangaRss.yaml`` that is a work-in-progress, or as-yet-unreleased,
data product.  This file is considered a part of the "WORK" release. The new MaNGA file we have been
working on was produced with a new tag of the pipeline, `v3_1_1`, but is the same as MPL-10 in all other
aspects.  We run the same ``datamodel_generate`` commands but without any release information.  This
defaults to the datamodel to a "WORK" release.  We specify to use the cache for MPL10 as it's mostly 
the same.

.. tab:: CLI

    .. code-block:: console

        $ datamodel generate -f mangaRss \
        -p MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz \
        -k plate=8485 -k ifu=1901 -k drpver=v3_1_1 -k wave=LOG --use-cache MPL10 --hdus-only

.. tab:: Python

    .. code-block:: python

        from datamodel.generate import DataModel

        # define the inputs
        file_species = "mangaRss"
        path = "MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz"
        keys = ['plate=8485', 'ifu=1901', 'drpver=v3_1_1', 'wave=LOG']

        # generate a datamodel for the latest working copy
        dm = DataModel(file_spec=file_species, path=path, keywords=keys)

        # write out the stub files with the partial MPL10 cache
        dm.write_stubs(use_cache_release='MPL10')

These commands will add a new "WORK" release into the datamodel file, using the cached HDU content from
MPL-10. If you do not want to use any cache, or generate a clean entry, simply leave out the cache
input arguments, e.g

.. tab:: CLI

    .. code-block:: console

        $ datamodel generate -f mangaRss \
        -p MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz \
        -k plate=8485 -k ifu=1901 -k drpver=v3_1_1 -k wave=LOG

.. tab:: Python

    .. code-block:: python

        dm = DataModel(file_spec=file_species, path=path, keywords=keys)
        dm.write_stubs()

All work releases will default to using the ``tree`` ``sdsswork.cfg``.  If the file is a part of
the `sdss5.cfg` ``tree`` configuration, you can specify the ``--tree_ver``, ``-t`` input keyword:

.. tab:: CLI

    .. code-block:: console

        $ datamodel generate -t sdss5 -f .....

.. tab:: Python

    .. code-block:: python

        dm = DataModel(file_spec=file_species, path=path, keywords=keys, tree_ver='sdss5')


Generating a datamodel by file
------------------------------

You can also generate a datamodel using only a filename.  In this mode, you will be given a series of
prompts asking you to either define the file_species, path, and keywords, or to look up an existing
sdss_access entry.

To generate a datamodel by file, for DR15

.. tab:: CLI

    .. code-block:: console

        $ datamodel generate -r DR15 \
        -n /Users/Brian/Work/sdss/sas/dr15/manga/spectro/redux/v2_4_3/8485/stack/manga-8485-1901-LOGRSS.fits.gz

.. tab:: Python

    .. code-block:: python

        from datamodel.generate import DataModel

        ff='/Users/Brian/Work/sdss/sas/dr15/manga/spectro/redux/v2_4_3/8485/stack/manga-8485-1901-LOGRSS.fits.gz'
        dm = DataModel.from_file(ff, tree_ver='dr15')

The ``datamodel`` code will first prompt you if an existing ``sdss_access`` definition exists:

- Does this file have an existing sdss_access definition? (y/n):

Answering ``y`` will prompt you to look up the ``sdss_access`` name, and will attempt to extract
the relevant keyword-value pairs.  If it cannnot do so, it will prompt you to define them.

::

    Does this file have an existing sdss_access definition? (y/n): y
    What is the sdss_access path_name?: mangarss
    Could not extract a value mapping for keys: ['drpver', 'wave', 'ifu', 'plate']
    Please define a list of name=value key mappings for variable substitution.
    e.g. drpver=v2_4_3, plate=8485, ifu=1901, wave=LOG
    :drpver=v2_4_3, plate=8485, ifu=1901, wave=LOG

If the file does not have an existing ``sdss_access`` entry, i.e. answering ``n``, it will prompt you
to define new inputs for the file species, symbolic path, and example keywords:
::

    Does this file have an existing sdss_access definition? (y/n): n
    Define a new path_name / file_species, e.g. mangaRss: mangaRss
    Define a new path template, starting with an environment variable label.
    Use jinja {} templating to define variable name used for substitution.
    e.g. "MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz"
    : MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz
    Define a list of name=value key mappings for variable substitution.
    e.g. drpver=v2_4_3, plate=8485, ifu=1901, wave=LOG
    : drpver=v2_4_3, plate=8485, ifu=1901, wave=LOG

Either way, at the end it will ask you to confirm your definitions:
::

    Confirm the following: (y/n):
     file = /Users/Brian/Work/sdss/sas/dr15/manga/spectro/redux/v2_4_3/8485/stack/manga-8485-1901-LOGRSS.fits.gz
     path_name = mangarss
     path_template = MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz
     path_keys = ['drpver=v2_4_3', 'plate=8485', 'ifu=1901', 'wave=LOG']


Adding the datamodel to the DSI
-------------------------------

Once a valid datamodel markdown is created, it will be automatically added to the 
SDSS Data Specification Index (`DSI <https://github.com/sdss/dsi>`_) for display.  The DSI is a 
web application accessible at https://data.sdss5.org/dsi using the standard SDSS passwords.  You
do not need to do anything extra to have your datamodel appear on the DSI, only ensure that a 
valid JSON representation has been created.  

.. _yanny:

Yanny Parameter files
---------------------

While most of the datamodel workflow is the same for `par files <https://www.sdss.org/dr17/software/par/>`_ as for FITS, 
there are a few differences, which we describe here.

The PRODUCT_ROOT environment variable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many Yanny parameter files are defined inside SVN or GIT repository software products, which can be checked out by the user or 
installed via the ``sdss-install`` product.  For example the SDSS **platePlans.par** lives inside the ``platelist`` repo, whose
path is defined as ``$PLATELIST_DIR/platePlans.par``, using the ``PLATELIST_DIR`` environment variable.  

Since the ``PLATELIST_DIR`` environment variable can point to any custom user or SAS location, or to a location 
installed by ``sdss-install``, and can also vary during data releases when software is tagged, a flexible definition 
is needed.  This flexibility is controlled by a ``PRODUCT_ROOT`` environment variable.  You can find more info on 
``PRODUCT_ROOT`` in the `SVN/Git Data Files <https://sdss-tree.readthedocs.io/en/latest/paths.html#defining-paths-to-data-files-in-svn>`_ section of the ``tree`` documentation. 

By default the datamodel product will use any existing custom environment variable definition found in your 
local ``os.environ``.  However, if one cannot be found, it falls back on any definition found in the ``tree`` product.  
This may invoke the ``PRODUCT_ROOT`` envvar.  For example, in the ``tree`` product, the ``PLATELIST_DIR`` env path 
for ``sdsswork`` is defined as ``$PRODUCT_ROOT/data/sdss/platelist/trunk``, as a general location where to find platelist files. 

The datamodel product will attempt to find a valid ``PRODUCT_ROOT`` environment variable definition in your system, in the 
following order of precedence of variable names:

- PRODUCT_ROOT
- SDSS_GIT_ROOT or SDSS_SVN_ROOT
- SDSS_INSTALL_PRODUCT_ROOT
- SDSS4_PRODUCT_ROOT
- the parent diretory of SAS_BASE_DIR


Example Par YAML
^^^^^^^^^^^^^^^^

The YAML datamodel for a par file is mostly the same as for FITS files, but with a ``par`` section instead of 
an ``hdus`` section.  Let's generate an example datamodel stub for the SDSS platePlans yanny file, located in the top-level 
directory of the platelist product.  The code to generate the datamodel stub is:

.. code-block:: python

    dm = DataModel(file_spec='platePlans', path='PLATELIST_DIR/platePlans.par', keywords=[], release="WORK")
    dm.write_stubs()

The output datamodel file, ``products/yaml/platePlans.yaml`` has the following contents:

.. tab:: PAR Yaml

    Example yaml datamodel for the SDSS plate plans par file, shortened for brevity
    
    .. code-block:: yaml

        general:
          name: platePlans
          short: replace me - with a short one sentence summary of file
          description: replace me - with a longer description of the data product
          datatype: PAR
          filesize: 1 MB
          releases:
          - WORK
          environments:
          - PLATELIST_DIR
          naming_convention: replace me - with $PLATELIST_DIR/platePlans.par or platePlans.par
            but with regex pattern matches
          generated_by: replace me - with the name(s) of any git or svn product(s) that produces
            this product.
          design: false
        changelog:
          description: Describes changes to the datamodel product and/or file structure from
            one release to another
          releases: {}
        releases:
          WORK:
            template: $PLATELIST_DIR/platePlans.par
            example: platePlans.par
            location: platePlans.par
            environment: PLATELIST_DIR
            access:
              in_sdss_access: true
              path_name: platePlans
              path_template: $PLATELIST_DIR/platePlans.par
              path_kwargs: []
              access_string: platePlans = $PLATELIST_DIR/platePlans.par
            par:
              comments: |-
                # platePlans.par
                #
                # Global plate planning file for SDSS-III
                #
                # Every plate number (plateid) has one and only one entry here.
                #
                # Numbering of plates starts after last plates of SDSS-II, which
                # were the MARVELS June 2008 pre-selection plates (3000-3014).
                # Note that SDSS-II also used plate numbers 8000-8033, which should
                # therefore be avoided
                #
                # Meaning of columns:
                #  plateid - unique ID of plate
                #  designid - ID of "design"; two plates can have the same design
                #             but be drilled for different HA, TEMP, EPOCH
                # ...
                # ...
                #
              header: []
              tables:
                PLATEPLANS:
                  name: PLATEPLANS
                  description: replace me - with a description of this table
                  n_rows: 7551
                  structure:
                  - name: plateid
                    type: int
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: 186
                  - name: designid
                    type: int
                    description: replace me - with a description of this column
                    unit: replace me - with a unit of this column
                    is_array: false
                    is_enum: false
                    example: -1
                  ...

Yaml "Par" Section
^^^^^^^^^^^^^^^^^^

The ``par`` section of the YAML file has the following content:

- **comments**: a string block of any comments found at the top of the Yanny par file, up to the "typedef" struct definition.
- **header**: a list of any header keywords found in the Yanny par file
- **tables**: a dictionary of tables defined in the Yanny par file

Each table entry has a table name (``name``), a description of the table (``description``), the number of rows 
in the table (``n_rows``), and a list of column definitions (``structure``). The column definitions are constructed
from the Yanny ``typedef`` structure definition found in the file for the given table.   

The ``type`` column parameter is pulled directly from the ``typedef`` column definition, eg. ``int plateid``.  For column
defintions with a size element, they are stored on the type itself.  For example ``char survey[20]`` is stored 
as type ``char[20]``. The array Yanny column definition ``float ha[6];`` would be converted to the yaml entry:

.. code-block:: yaml

    - name: ha
      type: float[6]
      description: replace me - with a description of this column
      unit: replace me - with a unit of this column
      is_array: true
      is_enum: false
      example:
      - -45.0
      - 0.0
      - 0.0
      - 0.0
      - 0.0
      - 0.0