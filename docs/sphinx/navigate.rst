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
- **tags**: a list of all SDSS software tags
- **products**: a list of all SDSS data products
- **vacs**: a list of SDSS VAC environment variables

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

Much of this metadata are described as a list of models, and can be accessed independently of the
``SDSSDataModel`` or ``Products`` objects.  See :ref:`metadata` for more details.

.. note::

    The datamodel examples on this page only have a single "mangaRss" datamodel product.  These
    examples will be updated with more realistic results once more example datamodels
    have been generated.

.. _products:

Data Products
-------------

Each SDSS JSON datamodel is converted, and serialized, into a `~datamodel.products.product.Product`,
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

Loading Content
^^^^^^^^^^^^^^^

By default, `~datamodel.products.product.DataProducts` lazy-loads all data products.  This means that
the underlying JSON datamodel content will not be loaded upon instantiation.  Only when a ``Product``
is retrieved from the ``DataProducts`` list, is when the JSON content is read in.  This allows for
efficient navigation of the list of data products for a large number of items.  You can load a product
manually by passing in ``load=True`` on instantiation, or call the Product's
`~datamodel.products.product.Product.load` method.
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

Retrieving Content
^^^^^^^^^^^^^^^^^^

The underlying JSON `~datamodel.models.yaml.ProductModel` is available on each product, accessible via
the ``_model`` attribute.  A subset of the model attributes have been "extracted" up on the ``Product``
object itself, e.g. the ``general.releases``, ``general.short``, and ``general.description``
attributes.  The ``_extract`` class attribute contains a list of ``general`` parameters to be included.
Additional parameters can be included by adding them to this list, reinstantiating, and reloading
the product.
::

    >>> # list the product releases
    >>> rss.releases
    [Release(name='MPL5', description='SDSS MaNGA internal product release 5', public=False, release_date='2016-06-27'),
     Release(name='DR14', description='SDSS public data release 14', public=True, release_date='2017-07-31'),
     Release(name='DR15', description='SDSS public data release 15', public=True, release_date='2018-12-10'),
     Release(name='DR16', description='SDSS public data release 16', public=True, release_date='2019-12-09'),
     Release(name='MPL10', description='SDSS MaNGA internal product release 10', public=False, release_date='2020-07-13'),
     Release(name='WORK', description='SDSS unreleased data.  Represents any work-in-progress data.', public=False, release_date='unreleased')]

    >>> # list the product short and long descriptions
    >>> rss.short, rss.description
    ('A MaNGA Row-Stacked Spectra (RSS) product',
     "The MaNGA DRP provides summary row-stacked spectra (RSS; with both logarithmic and
     linear wavelength solutions) for each galaxy that combine individual fiber spectra of
     that galaxy across multiple exposures into a single row-stacked format. The RSS files are a
     two-dimensional array with horizontal size N_spec and vertical size N = \\sum N_fiber(i)
     where N_fiber(i) is the number of fibers in the IFU targeting this galaxy for the i''th
     exposure and the sum runs over all exposures."
    )

The ``datamodel`` `~.datamodel.products.product.Product` contains various convenience methods of
returning content from the datamodel.  You can return the entire datamodel content has a
dictionary using `~.datamodel.products.product.Product.get_content`:
::

    >>> # return the datamodel content
    >>> rss.get_content()
    {'general': {'name': 'mangaRss',
     'short': 'this is a manga rss',
     'description': 'longer description',
     'environments': ['MANGA_SPECTRO_REDUX'],
     'datatype': 'FITS',
     ...
    }

You can return content specific to a release using `~.datamodel.products.product.Product.get_release`:
::

    >>> # return the datamodel content for DR15
    >>> rss.get_release("DR15")
    Release(
     template='$MANGA_SPECTRO_REDUX/[DRPVER]/[PLATE]/stack/manga-[PLATE]-[IFU]-[WAVE]RSS.fits.gz',
     ...)

Note that ``get_release`` method returns the `~datamodel.models.yaml.Release` object, which can be
converted to a dictionary through its own ``dict()`` method.

You can return either the example filepath, or a more general path location, for a given release.
::

    >>> # return the default datamodel example for the WORK release
    >>> rss.get_example()
    '/Users/Brian/Work/sdss/sas/mangawork/manga/spectro/redux/v3_1_1/8485/stack/manga-8485-1901-LOGRSS.fits.gz'

    >>> # return the file location for DR16
    >>> rss.get_location(drpver='v2_4_3', plate=8485, ifu=1901, wave='LOG', release='DR16')
    '/Users/Brian/Work/sdss/sas/dr16/manga/spectro/redux/v2_4_3/8485/stack/manga-8485-1901-LOGRSS.fits.gz'

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

.. _metadata:

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

.. _metatags:

Tags
^^^^

The SDSS ``Tag`` model represents a software release tag.  A specific tag is associated with a SDSS
data release, a SDSS survey, and is commonly referenced by a specific version name.
::

    >>> from datamodel.products import SDSSDataModel
    >>> dm = SDSSDataModel()
    >>> tag = dm.tags[0]
    >>> tag
    Tag(version=Version(name='drpver', description='software tag key for the MaNGA Data Reduction Pipeline (DRP)'), tag='v3_1_1', release=Release(name='DR17', description='SDSS public data release 17', public=True, release_date='2021-12-06'), survey=Survey(name='MaNGA', long='Mapping Nearby Galaxies at Apache Point Observatory', description='A wide-field optical spectroscopic IFU survey of extragalactic sources to study galaxy dynamics and kinematics', phase=Phase(name='Phase-IV', id=4, start=2014, end=2020, active=False), id='manga'))

    >>> # examine the tag release
    >>> tag.release
    Release(name='DR17', description='SDSS public data release 17', public=True, release_date='2021-12-06')

    >>> # examine the tag survey
    >>> tag.survey
    Survey(name='MaNGA', long='Mapping Nearby Galaxies at Apache Point Observatory', description='A wide-field optical spectroscopic IFU survey of extragalactic sources to study galaxy dynamics and kinematics', phase=Phase(name='Phase-IV', id=4, start=2014, end=2020, active=False), id='manga')

    >>> # examine the tag version
    >>> tag.version
    Version(name='drpver', description='software tag key for the MaNGA Data Reduction Pipeline (DRP)')

You can reorganize the list of ``Tags`` into a nested dictionary, grouped by release or survey, using
the ``group_by``.  The default ordering is by SDSS data release.

::

    >>> from datamodel.products import SDSSDataModel
    >>> dm = SDSSDataModel()
    >>> dm.tags.group_by()
    {'DR17':
        {'manga': {'drpver': 'v3_1_1', 'dapver': '3.1.0'},
         'mastar': {'drpver': 'v3_1_1'},
         'eboss': {'run2d': 'v5_13_2', 'run1d': 'v5_13_2'},
         'apogee2': {'apred_vers': 'dr17',
            'apstar_vers': 'stars',
            'aspcap_vers': 'synspec_rev1',
            'results_vers': 'synspec_rev1'},
         'legacy': {'run2d': [26, 103, 104]}},
    'DR16':
        {'manga': {'drpver': 'v2_4_3', 'dapver': '2.2.1'},
         'mastar': {'drpver': 'v2_4_3'},
         'eboss': {'run2d': 'v5_13_0', 'run1d': 'v5_13_0'},
         'apogee2': {'apred_vers': 'r12',
            'apstar_vers': 'stars',
            'aspcap_vers': 'l33',
            'results_vers': 'l33'},
         'legacy': {'run2d': [26, 103, 104]}
         },
    ...
    }

Or to reorder by SDSS survey, set `order_by` to `survey`.
::

    >>> from datamodel.products import SDSSDataModel
    >>> dm = SDSSDataModel()
    >>> dm.tags.group_by('survey')
    {'manga':
        {'DR17': {'drpver': 'v3_1_1', 'dapver': '3.1.0'},
         'DR16': {'drpver': 'v2_4_3', 'dapver': '2.2.1'},
         'DR15': {'drpver': 'v2_4_3', 'dapver': '2.2.1'},
         ...
         }
     'eboss':
        {'DR17': {'run2d': 'v5_13_2', 'run1d': 'v5_13_2'},
         'DR16': {'run2d': 'v5_13_0', 'run1d': 'v5_13_0'},
         'DR15': {'run2d': 'v5_10_0', 'run1d': 'v5_10_0'},
         ...
         },
    ...
    }
