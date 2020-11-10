# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: generate.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

__author__ = 'Joel Brownstein <joelbrownstein@sdss.org>'

class Generate(object):
    """Class to generate a datamodel.

    Parameters
    ----------
    options : command-line options, optional
        Operate on these files.
    tree_ver : str, optional
        Override the tree version default set by modules
    """

    def __init__(self, options = None, tree_ver = None, env_label = None, location = None, force = None, verbose = None, debug = None, nolog = None):
        self.tree_ver = options.tree_ver if options else tree_ver
        self.env_label = options.env_label if options else env_label
        self.location = options.location if options else location
        self.force = options.verbose if options else force
        self.verbose = options.verbose if options else verbose
        self.debug = options.debug if options else debug
        self.nolog = options.nolog if options else nolog

    def set_file(self):
        pass
