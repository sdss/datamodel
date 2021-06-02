
.. _intro:

Introduction to datamodel
=========================

The sdss ``datamodel`` product is a python package for creating, validating, and accessing datamodels
for SDSS data products.

Generating a datamodel
----------------------

Datamodels are documented metadata representations of data products, e.g. FITS files.  Since pipelines
can produce many different files of the same data product, e.g. with different input parameters, for
different target names or different pipeline analysis settings, we generate a single datamodel file
for a set, or "species", of data products.  For this reason, the ``datamodel`` product is structured
around th

This "file_species" is a representative name for all files of a given data product,
e.g. all MaNGA IFU data cubes get a single ``mangaCube`` file species name.


Required Inputs:
^^^^^^^^^^^^^^^^

- **file_species**: A short name of the "species" of the file, similar to an ``sdss_access`` entry name
- **path**: An abstract file path using `Jinja2 <https://jinja.palletsprojects.com/en/3.0.x/>`_ template variable syntax, similar to an ``sdss_access`` entry path
- **keywords**: A list of keyword-value pairs matching the path template variable names

Release Inputs:
^^^^^^^^^^^^^^^

- **tree_ver**: the SDSS tree configuration name the data product is associated with
- **release**: the data release of the data product


From the Command-Line
^^^^^^^^^^^^^^^^^^^^^

To generate a datamodel using the command-Line  See :ref:`usage-dmgen` for a full list of command-line arguments.

.. code-block:: bash

    datamodel_generate -f mangaRss -p MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz -k plate=8485 ifu=1901 drpver=v2_4_3 wave=LOG -r DR15



From Python
^^^^^^^^^^^

.. code-block:: python

    from datamodel.generate import DataModel

    file_species = "mangaRss"
    path = "MANGA_SPECTRO_REDUX/{drpver}/{plate}/stack/manga-{plate}-{ifu}-{wave}RSS.fits.gz"
    keys = ['plate=8485', 'ifu=1901', 'drpver=v2_4_3', 'wave=LOG']

    # generate a datamodel for Data Release 15 (DR15)
    dm = DataModel(file_spec=file_species, path=path, keywords=keys, release='DR15')

    # write out the stubs
    dm.write_stubs()


Validating datamodels
---------------------

Adding new releases
-------------------

Public or Internal Releases
^^^^^^^^^^^^^^^^^^^^^^^^^^^

"Work" Releases
^^^^^^^^^^^^^^^

Generating a datamodel by file
------------------------------

You can also generate a datamodel with only a filename


Adding the datamodel to the Wiki
--------------------------------

Once a valid datamodel markdown is created, you will need to upload it to the wiki.  It is best to do this step
at Utah.  From the Utah machines, run
::

    datamodel_wiki -e MANGA_SPECTRO_REDUX -f mangaRss


Updating your netrc file
^^^^^^^^^^^^^^^^^^^^^^^^

In order to use the ``datamodel_wiki`` function, you must first add your wiki credentials to a private
**.netrc** file in your home directory.  Add the following line to ``~/.netrc``,
::

    machine wiki.sdss.org
        login <username>
        password <password>

replacing ``username`` and ``password`` with your wiki credentials.  You also need to confirm that
your ``~/.netrc`` is not readable, by running `chmod 600 ~/.netrc`.

