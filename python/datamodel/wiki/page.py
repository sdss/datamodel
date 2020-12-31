# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: page.py
# @License: BSD 3-Clause
# @Copyright: SDSS.


__author__ = 'Joel Brownstein <joelbrownstein@sdss.org>'

class Page(object):
    """Class to store and update wiki pages.

    Parameters
    ----------
    options : command-line options, optional
    tree_ver : str, optional
        Override the tree version default set by modules
    spec : str, optional
        Name of file species
    path : str, optional
        Symbolic path to fits file (can be combined from
        the env_label/location if omitted)
    env_label : str, optional
        the tree environmental variable (can be parsed from
        the symbolic path if omitted)
    location: str, optional
        the partial symbolic path (can be parsed from the
        symbolic path if omitted)
    format : str, either md (default) or html
    force : bool (default false)
        set True to over-write the human edited yaml and
        restore it to the original template / fits file.
    """
    
    def __init__(self, options = None, tree_ver = None, spec = None, path = None, env_label = None, location = None, format = None, force = None, verbose = None, debug = None):
        self.tree_ver = options.tree_ver if options else tree_ver
        self.spec = options.spec if options else spec
        self.path = options.path if options else path
        if self.path is None:
            self.env_label = options.env_label if options else env_label
            self.location = options.location if options else location
            self.path = join(self.env_label, self.location)
        else:
            try: self.env_label, self.location = self.path.split(sep, 1)
            except:
                self.env_label = options.env_label if options else env_label
                self.location = options.location if options else location
        self.format = options.format if options else format
        self.force = options.force if options else force
        self.verbose = options.verbose if options else verbose
        self.debug = options.debug if options else debug
        self.set_tree()

