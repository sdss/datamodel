.. _clis:

Command-line Interface
======================

.. _usage-quick:

Quick Reference
---------------

.. click:: datamodel.cli:cli
   :prog: datamodel
   :nested: short

.. _usage-full:

Commands
--------

.. _usage-dmgen:

.. click:: datamodel.cli:generate
   :prog: generate
   :nested: full

.. _usage-dmdesign:

.. click:: datamodel.cli:design
   :prog: design
   :nested: full

.. _usage-dminstall:

.. click:: datamodel.cli:install
   :prog: install
   :nested: full

.. _usage-dmtree:

.. click:: datamodel.cli:tree
   :prog: tree
   :nested: full

.. _usage-dmvalid:

.. click:: datamodel.cli:validate
   :prog: validate
   :nested: full

.. _usage-dmmove:

.. click:: datamodel.cli:move
   :prog: move
   :nested: full

.. _cli-diff:

Cli Differences
---------------

In ``datamodel 0.2.1``, the command-line tools switched from
`argparse <https://docs.python.org/3/library/argparse.html>`_ to
`click <https://click.palletsprojects.com/en/8.0.x/>`_ for improved cli handling and
consolidation of sub-commands under an umbrella cli.  The behavior and syntax is
mostly the same with the exception of the following:

- commands are no longer snake case, but rather two separate words.  i.e. ``datamodel_generate`` -> ``datamodel generate``
- each ``-k``, ``--keywords`` argument to ``datamodel generate`` must now be specified individually,
  as ``click`` does not allow the equivalent of ``narg="*"``. See
  `click multiple <https://click.palletsprojects.com/en/8.0.x/options/#multiple-options>`_ vs
  `argparse nargs <https://docs.python.org/3/library/argparse.html#nargs>`_.
  i.e. ``-k plate=8485 ifu=1901`` -> ``-k plate=8485 -k ifu=1901``

For backwards compatibility, we retain the original snake_case scripts, which call the underlying
``click`` command.  If you pip-install the ``datamodel`` product, you can call ``


