
.. _examples_des:

Examples
========

Here are examples of designing datamodels for files that do not yet exist on disk.


Converting a CSV File
---------------------

This example documents how to convert an :download:`example CSV file <_static/example.csv>` into a
valid FITS file, and produce a datamodel at the same time.  It shows how to design new datamodels for
FITS files that do not yet exist, and to generate a template FITS file from the designed datamodel at
the end of the process.  It follows the instructions in :ref:`design`.

The :download:`example CSV file <_static/example.csv>` contains 5 columns of data of types
integer, string, float, boolean, and float.

Generating the YAML stub
^^^^^^^^^^^^^^^^^^^^^^^^

First we need to specify a desired file species name and abstract path location of where we want or
expect the FITS file to live on disk.  Then we instantiate a new DataModel with the "design" flag set to True.
Then we generate the initial YAML datamodel.

::

    from datamodel.generate import DataModel

    # define the file species name and abstract path we want
    fs = "exampleCatalog"
    path = "SANDBOX_DIR/test/{ver}/example_catalog.fits"

    # create a new datamodel, with the design flag set
    dm = DataModel(file_spec=fs, path=path, design=True, tree_ver='sdss5')

    # generate the initial YAML datamodel stub
    dm.write_stubs()

This produces a YAML with the standard sections "general", "changelog", and "releases", with new
"WORK" release entry.  It adds a default PRIMARY HDU extension 0.  We can now design any additional HDUs.

We need to a design a new FITS BinaryTableHDU that maps to the tabular CSV data.   To design a new
table HDU, we specify a "table" extension, the name of the extension, and a list of desired columns.
See :ref:`designhdu` and the `~datamodel.generate.datamodel.DataModel.design_hdu` for details.  The list of
columns can be a list of tuples, with the column name, and the column format.  The allowed FITS column
formats are at `FITS Column Creation <https://docs.astropy.org/en/stable/io/fits/usage/table.html#column-creation>`_.

::

    # design a binary table hdu extension to add to the YAML file
    columns = [("a", "J"), ("b", "5A"), ("c", "E"), ("d", "L"), ("e", "D")]
    dm.design_hdu(ext="table", name="CATALOG", columns=columns)

This adds a new HDU extension into the YAML datamodel.

.. code-block:: yaml

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
      hdu1:
        name: CATALOG
        description: replace me description
        is_image: false
        size: 0 bytes
        columns:
          a:
            name: A
            type: int32
            unit: replace me - with content
            description: replace me - with content
          b:
            name: B
            type: char[5]
            unit: replace me - with content
            description: replace me - with content
          c:
            name: C
            type: float32
            unit: replace me - with content
            description: replace me - with content
          d:
            name: D
            type: bool
            unit: replace me - with content
            description: replace me - with content
          e:
            name: E
            type: float64
            unit: replace me - with content
            description: replace me - with content

Filling in the YAML content
^^^^^^^^^^^^^^^^^^^^^^^^^^^

We now have a YAML datamodel that must be properly validated and have all the "replace me" content
filled in.  Fill in any "replace me" fields with the relevant text.  This includes the general short and
long descriptions.  All designed HDU content will have "replace me" fields.  For our new BinaryTable HDU,
we must fill in a description of the extension, as well as values for the column units and descriptions.

Generating the template FITS file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once we've filled out our YAML file, and replaced all required content, we can generate a template FITS
file from our designed datamodel.  To generate a real file, we need to define example path keyword arguments
to convert our abstract path to a real path.

::

    # generate the FITS file, with version v1
    dm.generate_designed_file(ver='v1')

This code creates a new FITS file at the example path location ``$SANDBOX_DIR/test/v1/example_catalog.fits``.
We can now read it in and examine it.  The new FITS file is only a template, and will have empty data in
its HDU extensions.  See :ref:`add_data` below on how to fill our CSV table data.

::

    from astropy.io import fits

    # read in our new FITS file
    hdu = fits.open(dm.file)

    # examine the FITS file
    hdu.info()

    Filename: ../sas/sdsswork/sandbox/test/v1/example_catalog.fits
    No.    Name      Ver    Type      Cards   Dimensions   Format
    0  PRIMARY       1 PrimaryHDU       6   ()
    1  CATALOG       1 BinTableHDU     21   0R x 5C   [J, 5A, E, L, D]

Generating Valid JSON
^^^^^^^^^^^^^^^^^^^^^

A valid datamodel JSON can only be produced for existing files, outside of the design phase.  Generating
a template FITS file creates a file and exits the design phase.  If the YAML model is properly validated,
we can now write out the JSON datamodel.

::

    dm.write_stubs()

.. _add_data:

Adding Data Values
^^^^^^^^^^^^^^^^^^

An optional final step is to add the CSV table data to our new FITS file HDU extension.  We can do this
easily by reading in the CSV file as an Astropy Table object, then converting the table to a valid FITS
BinaryTableHDU, and finally copying the data over to our custom FITS file.  We use the astropy helper
function table_to_hdu to properly account for column formats, and any necessary big/little endian conversions.

.. note::
  if you get the following error during data copy, ``TypeError: Table data has incorrect type.``,
  this means that one of the columns designed in the datamodel does not match the column format Astropy
  Table has detected.  Double check that all columns have the correct format, and update any incorrect
  columns formats in the datamodel file.

::

    from astropy.io import fits
    from astropy.table import Table

    # read in our new FITS file
    hdu = fits.open(dm.file)

    # read in the csv as an Astropy Table and name the columns as the HDU columns
    t = Table.read("example.csv", format="csv", names=hdu[1].data.columns.names)

    # convert the table to HDU and write its data to our HDU
    dd = fits.table_to_hdu(t)
    hdu[1].data = dd.data
    hdu.writeto(hdu.filename(), overwrite=True)


