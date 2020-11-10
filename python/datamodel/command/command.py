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
        self.options._name = name if self.options else None

def datamodel_generate():
    parser = ArgumentParser()
    parser.add_argument("-r", "--root_path", help="path of root directory",metavar="ROOT_PATH")
    parser.add_argument("-p", "--partition", help="disk partition",metavar="PARTITION")
    parser.add_argument("-t", "--tree_ver", help="tree version",metavar="TREE_VER")
    parser.add_argument("-l", "--location", help="location to walk",metavar="LOCATION")
    parser.add_argument("-e", "--env_label", help="env_label",metavar="ENV_LABEL")
    parser.add_argument("-m", "--max_depth", help="traverse to max depth", type=int, metavar="MAX_DEPTH")
    parser.add_argument("-X", "--exclude", action="append", dest="exclude", metavar="DIR", help="Exclude directory")
    parser.add_argument("-I", "--initial", help="initial probe (fast)", action="store_true")
    parser.add_argument("-f", "--force", help="force",action="store_true")
    parser.add_argument("-v", "--verbose", help="verbose",action="store_true")
    parser.add_argument("-d", "--debug", help="debug",action="store_true")
    parser.add_argument("-N", "--nolog", help="nolog",action="store_true")
    parser.add_argument("-K", "--skip_count", help="skip_count",action="store_true")
    parser.add_argument("-C", "--count_only", help="count_only",action="store_true")
    return parser.parse_args()
