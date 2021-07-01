.. _navigate:

Navigating Datamodels
=====================

Here we describe using Python to navigate the SDSS Datamodel system.

The SDSS Datamodel
------------------

The highest level entry point into is the datamodel is the `~datamodel.products.SDSSDataModel`.  It
essentially acts as a container object for all SDSS data products and metadata.  The ``SDSSDataModel``
currently contains the following accessible properties

- **releases**: a list of all public and internal data releases, plus the active "WORK" release
- **surveys**: a list of all SDSS surveys
- **phases**: a list of all SDSS phases
- **products**: a list of all SDSS data products

.. code-block:: python

    >>> from datamodel.products import SDSSDataModel
    >>> dm = SDSSDataModel()
    >>> dm
    <SDSS DataModel (n_releases=30, n_products=1, n_surveys=13, n_phases=5)>

You can access each property from the datamodel itself.
::

    >>> # display the list of SDSS surveys
    >>> dm.surveys
    [Survey(name='MWM', long='Milky Way Mapper', description='A time-domain, optical+IR spectroscopic survey of Milky Way stars of all types.', phase=Phase(name='Phase-V', id=5, start=2020, end=None, active=True))
     Survey(name='BHM', long='Black Hole Mapper', description='An optical time-domain spectroscopic survey of quasars and X-ray sources', phase=Phase(name='Phase-V', id=5, start=2020, end=None, active=True))
     ...]

.. note::

    The datamodel examples on this page only have a single "mangaRss" datamodel product.  These
    examples will be updated with more realistic results once more example datamodels 
    have been generated.    

Metadata Models
---------------

The ``datamodel`` products contains SDSS metadata accessible for lookup, or for use within web
applications or Python software.  These metadata files are defined as YAML files, and serialized 
into Python objects using `Pydantic <https://pydantic-docs.helpmanual.io/>`_.  For example, 
the ``datamodel/releases.yaml`` file defines the list of all available public or internal SDSS
data releases, and gets converted into `.datamodel.models.releases.Releases`, a list of 
`.datamodel.models.releases.Release` objects.

Each metadata YAML file is structured in the same way, with two parts: a ``schema`` section, and 
a "named" list section of objects, e.g. "releases".  The ``schema`` section defines the parameters 
attached to each object, while the named section defines the object themselves.  For example: 

.. code-block:: yaml

    schema:
      title: Release
      key: release
      description: SDSS data release versions
      properties:
        name:
          title: name
          description: the name of the data release
          type: string
          required: true
        description:
          title: description
          description: a short description of the data release
          type: string
          required: true
        public:
          title: release
          description: a flag whether it is public or not
          type: bool
          required: false
          default: false
        release_date:
          title: release_date
          description: the date the data was released to the public or the collaboration, in str isoformat
          type: str
          required: false
          default: unreleased

    releases:
      - name: DR17
        description: SDSS public data release 17
        public: true
        release_date: '2021-12-06'
      - name: DR16
        description: SDSS public data release 16
        public: true
        release_date: '2019-12-09'
      ...

When the ``datamodel`` package reads in these files and serializes them, they become accessible as 
navigable objects.  For example, to access the list of SDSS releases, you can do the following:
::

    >>> # import the SDSS releases 
    >>> from datamodel.models import releases
    >>> releases
    [Release(name='DR17', description='SDSS public data release 17', public=True, release_date=datetime.date(2021, 12, 6))
     Release(name='DR16', description='SDSS public data release 16', public=True, release_date=datetime.date(2019, 12, 9))
     ...
     Release(name='WORK', description='SDSS unreleased data.  Represents any work-in-progress data.', public=False, release_date='unreleased')
     Release(name='MPL11', description='SDSS MaNGA internal product release 11.  Equivalent to DR17.', public=False, release_date=datetime.date(2021, 3, 1))
     Release(name='MPL10', description='SDSS MaNGA internal product release 10', public=False, release_date=datetime.date(2020, 7, 13))
     ...]
        
    >>> # check for containment
    >>> 'DR17' in releases
    True 

    >>> # select a release by index or name
    >>> releases[0] 
    Release(name='DR17', description='SDSS public data release 17', public=True, release_date=datetime.date(2021, 12, 6))
    >>> releases["DR13"]
    Release(name='DR13', description='SDSS public data release 13', public=True, release_date=datetime.date(2016, 7, 31))

All metadata objects subclass from `.datamodel.models.base.BaseList`, and behave the same way.  To list
just the names of each item, use the ``list_names`` method.
::

    >>> # list just the names of the releases
    >>> releases.list_names()
    ['DR17',
    'DR16',
    'DR15',
    ...]

By default, the order of the items in each list is defined by the order in the YAML file.  You 
can sort (in-place) the list of items by any attribute on the object.  To sort the releases 
by ``release_date`` from most recent to oldest, do:
::

    >>> # sort the releases by date in descending order
    >>> releases.sort('release_date', reverse=True)
    >>> releases
    [Release(name='DR17', description='SDSS public data release 17', public=True, release_date=datetime.date(2021, 12, 6))
     Release(name='MPL11', description='SDSS MaNGA internal product release 11.  Equivalent to DR17.', public=False, release_date=datetime.date(2021, 3, 1))
     Release(name='MPL10', description='SDSS MaNGA internal product release 10', public=False, release_date=datetime.date(2020, 7, 13))
     Release(name='DR16', description='SDSS public data release 16', public=True, release_date=datetime.date(2019, 12, 9))
     Release(name='MPL9', description='SDSS MaNGA internal product release 9', public=False, release_date=datetime.date(2019, 12, 2))
     ...]

The same structure and behaviour is true for any of the other metadata files, 
e.g. SDSS Phases or Surveys.
::

    >>> # import the SDSS phases 
    >>> from datamodel.models import phases
    >>> phases
    [Phase(name='Phase-V', id=5, start=2020, end=None, active=True)
     Phase(name='Phase-IV', id=4, start=2014, end=2020, active=False)
     Phase(name='Phase-III', id=3, start=2008, end=2014, active=False)
     Phase(name='Phase-II', id=2, start=2005, end=2008, active=False)
     Phase(name='Phase-I', id=1, start=2000, end=2005, active=False)]

As a reminder, all metadata items are accessible on the main `.datamodel.products.product.SDSSDataModel`.
::

    >>> # access the list of phases from the datamodel
    >>> dm.phases
    [Phase(name='Phase-V', id=5, start=2020, end=None, active=True)
     Phase(name='Phase-IV', id=4, start=2014, end=2020, active=False)
     Phase(name='Phase-III', id=3, start=2008, end=2014, active=False)
     Phase(name='Phase-II', id=2, start=2005, end=2008, active=False)
     Phase(name='Phase-I', id=1, start=2000, end=2005, active=False)]

Data Products
-------------

Each SDSS JSON datamodel is converted, and serialzied, into a `~datamodel.products.product.Product`, 
with the complete list of data products collected into a `~datamodel.products.product.DataProducts`
list.  The list of data products is available from the datamodel, i.e. ``dm.products`` or separately.
::

    >>> # import the list of data products
    >>> from datamodel.products import DataProducts
    >>> dp = DataProducts()
    >>> dp
    <DataProducts (n_products=1)>

``DataProducts`` is a `~fuzzy_types.fuzzy.FuzzyList`, so can indexed normally, or by a fuzzy name.
::

    >>> # get item by index
    >>> dp[0]
    <Product ("mangaRss", summary="this is a manga rss")>

    >>> # get item by name
    >>> dp['mangarss']
    <Product ("mangaRss", summary="this is a manga rss")>

    >>> # get item by fuzzy name
    >>> dp['mngars']
    <Product ("mangaRss", summary="this is a manga rss")>

By default, `~datamodel.products.product.DataProducts` lazy-loads all data products.  This means that 
the underlying JSON datamodel content will not be loaded upon instantiation.  Only when a ``Product`` 
is retrieved from the ``DataProducts`` list, is when the JSON content is read in.  This allows for 
efficient navigation of the list of data products for a large number of items.  You can load a product
manually by passing in ``load=True`` on instantiation, or call the 
`.datamodel.products.product.Product.load` method.   
::

    >>> # create a new Product for the MaNGA RSS datamodel
    >>> from datamodel.products import Product
    >>> rss = Product('mangarss')
    >>> rss
    <Product ("mangarss", summary="")>

    >>> # by default it is unloaded
    >>> rss.loaded
    False

    >>> # load the JSON content
    >>> rss.load()
    >>> rss
    <Product ("mangarss", summary="this is a manga rss")>
    
    >>> rss.loaded
    True

You can also list all available products by their "file species" name.
::

    >>> # list all data products by name
    >>> dp.list_products()
    ['mangaRss']


Reorganizing
------------

By default, ``DataProducts`` is a complete list of products organized by the "file species" datamodel 
name.  To group data products by some other property, you can use the 
`~datamodel.products.product.DataProducts.group_by` method.  Possible fields to group by are
any attribute on the `~datamodel.products.product.Product` instance, or any field in the underlying
``_model`` JSON datamodel, i.e. `~datamodel.models.yaml.ProductModel`.     

To group products by a ``Product`` attribute, pass in the attribute name.  For example, to group
products by data releases, use the ``releases`` attribute:
::

    >>> # group the products by the releases attribute
    >>> group = dm.products.group_by('releases')
    >>> group
    {'DR15': [<Product ("mangaRss", summary="this is a manga rss")>],
     'DR16': [<Product ("mangaRss", summary="this is a manga rss")>],
     'MPL10': [<Product ("mangaRss", summary="this is a manga rss")>],
     'WORK': [<Product ("mangaRss", summary="this is a manga rss")>]}

To group products by an attribute on the underlying JSON ``ProductModel``, pass in a "dotted attribute
chain" path to the field.  For example, to group products by the SAS environment variable, which lives
in the "environments" field of the `~datamodel.models.yaml.GeneralSection`
of the JSON datamodel file, the full string path would be `_model.general.environments`:
::

    >>> # group the products by the environments attribute
    >>> group = dm.products.group_by('_model.general.environments')
    >>> group
    {'MANGA_SPECTRO_REDUX': [<Product ("mangaRss", summary="this is a manga rss")>]}

