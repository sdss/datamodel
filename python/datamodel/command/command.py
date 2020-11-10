# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: command.py
# @License: BSD 3-Clause
# @Copyright: Joel Brownstein, SDSS.

from argparse import ArgumentParser
from os import getenv

class Command:

    def __init__(self, name=None):
        self.get_options = globals()[name] if name in globals().keys() else None
        self.options = self.get_options() if self.get_options else None
        if self.options: self.options._name = name

def datamodel_generate():
    parser = ArgumentParser()
    parser.add_argument("-t", "--tree_ver", help="tree version",metavar="TREE_VER")
    parser.add_argument("-l", "--location", help="location of file",metavar="LOCATION")
    parser.add_argument("-e", "--env_label", help="env_label",metavar="ENV_LABEL")
    parser.add_argument("-f", "--force", help="force",action="store_true")
    parser.add_argument("-v", "--verbose", help="verbose",action="store_true")
    parser.add_argument("-d", "--debug", help="debug",action="store_true")
    parser.add_argument("-N", "--nolog", help="nolog",action="store_true")
    return parser.parse_args()
