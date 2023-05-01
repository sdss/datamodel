.. _manipulate:

Manipulating Datamodels
=======================

Here we describe special cases for interacting with and manipulating datamodels
after they have been generated.


Removing Releases
-----------------

Sometimes it may be necessary to remove a release from a datamodel.  The easiest way to remove
a release from a datamodel YAML file is with the :ref:`datamodel remove cli <usage-dmrem>`.
You can also do it in Python albeit in a slightly more complicated manner.

.. tab:: CLI

    Remove a release from a datamodel using the command-line:

    .. code-block:: console

        $ datamodel remove -f astraAllStarAPOGEENet -r IPL2

.. tab:: Python

    From within Python, you need to explicitly remove the release and call to re-write
    the other datamodel files.

    .. code-block:: python

        from datamodel.generate import DataModel

        # get the datamodel
        fs = "astraAllStarAPOGEENet"
        dm = DataModel.from_yaml(fs, release="IPL2")

        # remove the IPL-2 release from the YAML stub
        s = dm.get_stub("yaml")
        s.remove_release("IPL2")
        s.write()

        # re-write the JSON, md and access files
        dm = DataModel.from_yaml(fs, release="IPL1")
        dm.write_stubs()

