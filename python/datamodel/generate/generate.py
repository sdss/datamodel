# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: generate.py
# @License: BSD 3-Clause
# @Copyright: Joel Brownstein, SDSS.

class Generate:

    def __init__(self, options = None, verbose = None):
        self.verbose = options.verbose if options else verbose
