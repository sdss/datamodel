
.. _design:

Designing Datamodels
====================

Here we describe the process of designing new datamodels for files that do not yet exist in
the SDSS ecosystem.  Most of the code examples on this page pertain to designing FITS files, but
the workflow is the same when designing other files, e.g. Yanny parameter files.     

.. _designstub:

Creating the Design Stub
------------------------

Designing a datamodel for a new file is very similar to generating a datamodel for an existing one.  It
consists of generating a YAML datamodel file, which can then be updated with new HDU information.

For the following examples, let's assume we are interested in designing a datamodel for a new MaNGA
FITS file, which will be a new summary catalog file produced by the MaNGA pipeline, for each plate
observed.  The planned file species name is ``mangaCatalog``, and the planned location of this file 
will be ``$MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-catalog-{plate}.fits.gz``, e.g.  
``$MANGA_SPECTRO_REDUX/v3_2_0/8485/stack/manga-catalog-8485.fits.gz``.

When desiging a new datamodel, use the :ref:`datamodel design cli <usage-dmdesign>` or specify 
the ``design=True`` keyword argument when using `~datamodel.generate.datamodel.DataModel` in Python.  For Yanny 
par files, the syntax below is exactly the same, just replace the path with a designed path to a Yanny parameter file.

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

For Yanny parameter files, the designed YAML stub is identical to that of above with a ``par`` section instead of an 
``hdus`` section.

.. code-block:: yaml

    par:
      comments: |
        #This is designer Yanny par
        #
        #Add comments here
      header:
      - key: key1
        value: value1
        comment: description for key1
      - key: key2
        value: value2
        comment: description for key2
      tables:
        TABLE:
          name: TABLE
          description: description for TABLE
          n_rows: 0
          structure:
          - name: col1
            type: int
            description: description for col1
            unit: ''
            is_array: false
            is_enum: false
            example: 1

For FITS files, see the :ref:`designhdu` section.  For Yanny parameters files, see the :ref:`designpar` section.

.. _designhdu:

Designing an HDU
----------------

After the initial design of the datamodel, you can now add additional HDUs to the datamodel.  
This can be done in two ways, in Python or in the YAML file itself.  Using our example of the new
``mangaCatalog`` datamodel, let's add two new extensions: a new `~astropy.io.fits.ImageHDU` called 
``SUMMARY``, and a new `~astropy.io.fits.BinTableHDU` called ``CATALOG``.  The new image HDU 
extension will contain a header with three custom keys, and the table HDU will contain three columns
in the binary table data.       

Adding HDUs with Python
^^^^^^^^^^^^^^^^^^^^^^^

To design a new HDU in Python, use the `~datamodel.generate.datamodel.DataModel.design_hdu` method.  The ``ext``
keyword argument is used to specify the kind of HDU, either `~astropy.io.fits.PrimaryHDU`, 
`~astropy.io.fits.ImageHDU`, and or `~astropy.io.fits.BinTableHDU`.  Let's first 
create a new ImageHDU with the name ``SUMMARY`` and a header with three custom keys.  We also 
optionally include a description for the HDU, which fills the ``description`` field in the YAML file.  
::

    >>> # create the header rows, as a list of tuples
    >>> hdr = [('CNAME', '', 'the name of the catalog'), 
    >>>        ('CSOURCE', '', 'the source of the catalog'), 
    >>>        ('SDATA', '', 'the type of data aggegrated as summary')]

    >>> # create a new ImageHDU with the custom header
    >>> dm.design_hdu(ext='image', name='SUMMARY', header=hdr, description='aggregated summary data')
    [WARNING]: Found existing extensions.  Using next extension id 1

When specifying a new header for an HDU, the ``header`` keyword accepts either a 
`~astropy.io.fits.Header` instance, a list of tuples of header ``(keyword, value, comment)``, 
or a list of dictionaries of header ``{"keyword": keyword, "value": value, "comment": comment}``. 

Now let's create the second binary table HDU extension, with name ``CATALOG``, and three table columns, 
a string column of character length 10, a integer 32 column, and a boolean column.
::

    >>> # create the table columns, as a list of tuples
    >>> columns = [('PARAM1','10A'), ('PARAM2','J'), ('PARAM3','B')]

    >>> # create a new BinTableHDU with the specified columns
    >>> dm.design_hdu(ext='table', name='CATALOG', columns=columns)
    [WARNING]: Found existing extensions.  Using next extension id 2

When specifying new table columns for an HDU, the ``columns`` keyword accepts either a list of 
`~astropy.io.fits.Column` objects, a list of tuples of column ``(name, format, unit)``, or a list of 
dictionaries of column ``{"name": name, "format": format, "unit": unit}``.

Each call to `~datamodel.generate.datamodel.DataModel.design_hdu` writes a basic new HDU out to the 
YAML datamodel file.  With the above calls, the ``hdus`` sections of designed YAML now looks like

.. code-block:: yaml

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
            description: this is the primary header
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
          hdu1:
            name: SUMMARY
            description: aggregated summary data
            is_image: true
            size: 0 bytes
            header:
            - key: XTENSION
              value: IMAGE
              comment: Image extension
            - key: BITPIX
              value: 8
              comment: array data type
            - key: NAXIS
              value: 0
              comment: number of array dimensions
            - key: PCOUNT
              value: 0
              comment: number of parameters
            - key: GCOUNT
              value: 1
              comment: number of groups
            - key: CNAME
              value: ''
              comment: the name of the catalog
            - key: CSOURCE
              value: ''
              comment: the source of the catalog
            - key: SDATA
              value: ''
              comment: the type of data aggegrated as summary
            - key: EXTNAME
              value: SUMMARY
              comment: extension name
          hdu2:
            name: CATALOG
            description: replace me description
            is_image: false
            size: 0 bytes
            columns:
            PARAM1:
                name: PARAM1
                type: char[10]
                unit: replace me - with content
                description: replace me - with content
            PARAM2:
                name: PARAM2
                type: int32
                unit: replace me - with content
                description: replace me - with content
            PARAM3:
                name: PARAM3
                type: bool
                unit: replace me - with content
                description: replace me - with content


Adding HDUs in YAML
^^^^^^^^^^^^^^^^^^^

Alternatively to Python, you can also specify HDUs in the YAML file itself.  This is done by adding
individual HDUs to the ``hdus`` dictionary of the ``WORK`` release.  Each HDU entry should
have the following syntax:

.. code-block:: yaml

    hdu[extno]:
      name: the name of the HDU 
      description: a description of the HDU extension
      is_image: whether the HDU is an ImageHDU or not
      size: the size of the HDU, can be 0 initially
      header: a list of any header keywords
      columns: a dictionary of any binary table columns (only relevant for BinTableHDUs)

Each ``header`` entry should have the following syntax:

.. code-block:: yaml

    hdu0:
      header:
      - key: the name of the header keyword
        value: the value of the header keyword, can be empty
        comment: a description of the header keyword, can be empty

Each ``column`` entry should have the following syntax:

.. code-block:: yaml

    hdu0:
      columns:
        [NAME]:
          name: the name of the table column
          type: the data type of the table column
          unit: any unit for the table column, can be empty
          description: a description of the table column

The column data type will be converted into a valid `~astropy.io.fits.Column` format; see 
`fits.Column Formats <https://docs.astropy.org/en/stable/io/fits/usage/table.html#column-creation>`_.
Valid column types are the following:

============= ===========  
Yaml          fits.Column
============= ===========
char[len]     [len]A        
bool          B, L        
int[16,32,64] I, J, K         
float[32,64]  E, D        
============= ===========

Let's manually add our two new HDU extensions, a ``SUMMARY`` ImageHDU and a ``CATALOG`` BinTableHDU.

.. code-block:: yaml

    releases:
      WORK:
        template: $MANGA_SPECTRO_REDUX/[DRPVER]/[PLATE]/stack/manga-catalog-[PLATE].fits
        example: v3_1_1/8485/stack/manga-catalog-8485.fits
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
            description: this is the primary header
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
          hdu1:
            name: SUMMARY
            description: aggregated summary data
            is_image: true
            size: 0
            header:
            - key: CNAME
              comment: the name of the catalog
            - key: CSOURCE
              comment: the source of the catalog
            - key: SDATA
              comment: the type of data aggegrated as summary
          hdu2:
            name: CATALOG
            description: a table of measured catalog parameters
            is_image: false
            size: 0
            columns:
              PARAM1:
                name: PARAM1
                description: parameter 1
                type: char[10]
                unit: ''
              PARAM2:
                name: PARAM2
                description: parameter 2
                type: int32
                unit: ''
              PARAM3:
                name: PARAM3
                description: parameter 3
                type: bool
                unit: ''

.. _designpar:

Designing a Par File
--------------------

After the initial design of the datamodel, you can now add additional Yanny content to the datamodel, such as file 
comments, header keyword-value pairs, or table information. This can be done in two ways, in Python or in the YAML 
file itself.  

Let's say we're designing a new observation plans file to live in the ``platelist`` product, at the top level directory of
the product.  Using the file_species name of "obsPlans", we create the initial stub with:

.. code-block:: python

    dm = DataModel(file_spec="obsPlans", path="PLATELIST_DIR/obsPlans.par", verbose=True, design=True)
    dm.write_stubs()

This creates a YAML like above. Now let's add some new header keywords, a few new column definitions to the "TABLE" table, 
and add a brand new table definition, called "NEW".    

Adding Content with Python
^^^^^^^^^^^^^^^^^^^^^^^^^^

To design new Yanny par content in Python, use the `~datamodel.generate.datamodel.DataModel.design_par` method.

There is only one header for a Yanny file.  You can add new keywords with the ``header`` argument.  The keywords
accepts either a list of tuples of header ``(keyword, value, comment)``, a list of dictionaries 
of header ``{"key": keyword, "value": value, "comment": comment}``, or a simple dictionary of key-value pairs.

The ``name`` keyword argument specifies the table you want to modify or add.  Table column definitions are added
with the ``columns`` keyword.  It accepts either a list of column names, a list of tuples of column 
``(name, type)`` or ``(name, type, description)``, or a list of dictionaries of column 
``{"name": name, "type": type, "description": description}`` as shorthand or the full YAML dictionary definition.     

Allowed column types are any valid Yanny par types, input as strings, e.g. "int", "float", "char".
Array columns can be specified by including the array size in "[]", e.g. "float[6]".  Enum types
are defined by setting ``is_enum`` to True, and by providing a list of possible values via ``enum_values``.  

Let's first update the header with a single key "cart" , and define three columns in the table: a string, a float 
array of 5 elements, and an integer.  Let's also create a brand new table in the yaml file, called "NEW", with three 
new columns, and update the header with three new keys. And finally, let's add an enumerated column, ``ecol``, 
to our table using the full column definition syntax.

.. code-block:: python

    # add a single header keyword, along with new columns to the existing table, "TABLE"
    dm.design_par(header=("cart", "3", "cart id"), name="TABLE", columns=[("a", "char"), ("b", "float[5]"), ("c", "int")])

    # add three new header keys, and a new table definition, "NEW"
    dm.design_par(header={"d": 1, "e": 2, "f": 3}, name="NEW", columns=[("d1", "float[6]"), ("d2", "int"), ("d3", "char[2]")])

    # add an enumerated column to the existing table, "TABLE", using the full column dict definition
    ecol = {"name": "ecol", "description": "a new enum column", "type": "ETYPE", "unit": "", "is_array": False,
            "is_enum": True, "enum_values": ["GO", "NO", "FO", "SO"], "example": "GO"}
    dm.design_par(name="TABLE", columns=[ecol])

Each call to `~datamodel.generate.datamodel.DataModel.design_hdu` writes the content out to the 
YAML datamodel file.  With the above calls, the ``par`` section of designed YAML now looks like

.. code-block:: yaml

    releases:
      WORK:
        template: $PLATELIST_DIR/obsPlans.par
        example: null
        location: obsPlans.par
        environment: PLATELIST_DIR
        access:
          in_sdss_access: false
          path_name: null
          path_template: null
          path_kwargs: null
          access_string: obsPlans = $PLATELIST_DIR/obsPlans.par
        par:
          comments: |
            #This is designer Yanny par
            #
            #Add comments here
          header:
          - key: key1
            value: value1
            comment: description for key1
          - key: key2
            value: value2
            comment: description for key2
          - key: cart
            value: '3'
            comment: cart id
          - key: d
            value: 1
            comment: description for d
          - key: e
            value: 2
            comment: description for e
          - key: f
            value: 3
            comment: description for f
          tables:
            TABLE:
              name: TABLE
              description: description for TABLE
              n_rows: 0
              structure:
              - name: col1
                type: int
                description: description for col1
                unit: ''
                is_array: false
                is_enum: false
                example: 1
              - name: a
                type: char
                description: description for a
                unit: ''
                is_array: false
                is_enum: false
                example: a
              - name: b
                type: float[5]
                description: description for b
                unit: ''
                is_array: true
                is_enum: false
                example:
                - 1.0
                - 1.0
                - 1.0
                - 1.0
                - 1.0
              - name: c
                type: int
                description: description for c
                unit: ''
                is_array: false
                is_enum: false
                example: 1
              - name: ecol
                description: a new enum column
                type: ETYPE
                unit: ''
                is_array: false
                is_enum: true
                enum_values:
                - GO
                - NO
                - FO
                - SO
                example: GO
            NEW:
              name: NEW
              description: description for TABLE
              n_rows: 0
              structure:
              - name: d1
                type: char
                description: description for d1
                unit: ''
                is_array: false
                is_enum: false
                example: a
              - name: d2
                type: int
                description: description for d2
                unit: ''
                is_array: false
                is_enum: false
                example: 1
              - name: d3
                type: char[2]
                description: description for d3
                unit: ''
                is_array: false
                is_enum: false
                example: a

Adding Content in YAML
^^^^^^^^^^^^^^^^^^^^^^

Alternatively to Python, you can also specify par content in the YAML file itself.  This is done by adding
individual HDUs to the ``hdus`` dictionary of the ``WORK`` release.  

The ``par`` content should have the following syntax:

.. code-block:: yaml

    par:
      comments: a string of comments
      header: a list of header keywords
      tables: a dictionary of tables

Each ``header`` entry should have the following syntax:

.. code-block:: yaml

    header:
    - key: the name of the header keyword
      value: the value of the header keyword, can be empty
      comment: a description of the header keyword, can be empty

Each table entry in the ``tables`` section should have the following syntax:

.. code-block:: yaml

    tables:
      [NAME]:
        name: the name of the table 
        description: a description of the table
        n_rows: the number of rows in the table, can be 0 initially 
        structure: a list of table column definitions

Each column entry in the ``structure`` section should have the following syntax:

.. code-block:: yaml

    structure:
    - name: the name of the column
      type: the datatype of the column, with optional array size
      description: a description for the column
      unit: a unit of the column, if any
      is_array: whether the column is an array 
      is_enum: whether the column is an enumeration
      enum_values: a list of enumerated values, if any
      example: an example value for the column

Let's manually add our new header keys, new columns, and new tables.

.. code-block:: yaml

    par:
      comments: |
        #This is a new observation plans file
        #
      header:
      - key: cart
        value: '3'
        comment: cart id
      - key: d
        value: 1
        comment: this is a d key
      - key: e
        value: 2
        comment: this is a e key
      - key: f
        value: 3
        comment: this is a f key
      tables:
        TABLE:
          name: TABLE
          description: this is the main table
          n_rows: 0
          structure:
          - name: a
            type: char
            description: this is column a
            example: hello
          - name: b
            type: float[5]
            description: this is column b
            is_array: true
          - name: c
            type: int
            description: this is column c
          - name: ecol
            description: a new enum column
            type: ETYPE
            unit: ''
            is_array: false
            is_enum: true
            enum_values: [GO, NO, FO, SO]
            example: GO
        NEW:
          name: NEW
          description: this is a secondary but new table
          n_rows: 0
          structure:
          - name: d1
            type: char
            description: description for d1
            unit: ''
            is_array: false
            is_enum: false
            example: a
          - name: d2
            type: int
            description: description for d2
            unit: ''
            is_array: false
            is_enum: false
            example: 1
          - name: d3
            type: char[2]
            description: description for d3
            unit: ''
            is_array: false
            is_enum: false
            example: a

.. _createfile:

Creating a New File
-------------------

When you've finished designing a datamodel and want to test out how it looks in FITS form, you can
easily create a new FITS file from the designed YAML hdus.  From the command-line, specify the 
``-c``, ``--create`` flag.  In order to construct a real file, you will need to specify any necessary
path keyword variables for substitution, using the ``-k``, ``--keyword`` flags, the same when using 
``datamodel generate``.  From Python, call 
`~datamodel.generate.datamodel.DataModel.generate_designed_file`, passing in all relevant defined 
path keyword parameters.  In this example, let's create a new test file for MaNGA plate 8485, and 
DRP pipeline version ``v3_2_0``.

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
      0  PRIMARY       1 PrimaryHDU       6   ()
      1  SUMMARY       1 ImageHDU        11   ()
      2  CATALOG       1 BinTableHDU     20   0R x 3C   [10A, J, L]

    >>> # look at the SUMMARY HDU header
    >>> hdulist['SUMMARY'].header
    XTENSION= 'IMAGE   '           / Image extension
    BITPIX  =                    8 / array data type
    NAXIS   =                    0 / number of array dimensions
    PCOUNT  =                    0 / number of parameters
    GCOUNT  =                    1 / number of groups
    CNAME   = '' / the name of the catalog
    CSOURCE = '' / the source of the catalog
    SDATA   = '' / the type of data aggegrated as summary
    EXTNAME = 'SUMMARY '           / extension name
    CHECKSUM= 'VPbWYMZVVMaVVMYV'   / HDU checksum updated 2021-07-16T10:38:22
    DATASUM = '0       '           / data unit checksum updated 2021-07-16T10:38:22

    >>> # look at the CATALOG HDU header
    >>> hdulist['CATALOG'].header
    XTENSION= 'BINTABLE'           / binary table extension
    BITPIX  =                    8 / array data type
    NAXIS   =                    2 / number of array dimensions
    NAXIS1  =                   15 / length of dimension 1
    NAXIS2  =                    0 / length of dimension 2
    PCOUNT  =                    0 / number of group parameters
    GCOUNT  =                    1 / number of groups
    TFIELDS =                    3 / number of table fields
    TTYPE1  = 'PARAM1  '
    TFORM1  = '10A     '
    TTYPE2  = 'PARAM2  '
    TFORM2  = 'J       '
    TTYPE3  = 'PARAM3  '
    TFORM3  = 'L       '
    EXTNAME = 'CATALOG '           / extension name
    CHECKSUM= 'jH7bmG5bjG5bjG5b'   / HDU checksum updated 2021-07-16T10:56:58
    DATASUM = '0       '           / data unit checksum updated 2021-07-16T10:56:58

When you create a new file, you will exit the datamodel design phase. The ``design`` flag will be set 
to ``False``, and the ``example`` parameter will be populated with your new file.
