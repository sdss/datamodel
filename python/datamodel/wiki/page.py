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
    space : str, optional
        Set the wiki space
    """
    
    def __init__(self, space = None, verbose = None):
        self.space = space
        self.verbose = verbose
