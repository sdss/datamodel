# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: command.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

from argparse import ArgumentParser
from os import getenv

__author__ = 'Joel Brownstein <joelbrownstein@sdss.org>'

class Command(object):
    """Class to parse arguments from a command.

    Parameters
    ----------
    name : the command name, defining the arguments to parse
    """

    def __init__(self, name=None):
        self.get_options = globals()[name] if name in globals().keys() else None
        self.options = self.get_options() if self.get_options else None
        if self.options: self.options._name = name

def datamodel_generate():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file_spec", help="unique name of file species",metavar="FILE_SPEC")
    parser.add_argument("-t", "--tree_ver", help="tree version",metavar="TREE_VER")
    parser_group = parser.add_mutually_exclusive_group(required=True)
    parser_group.add_argument("-p", "--path", help="symbolic path of file",metavar="PATH")
    parser.add_argument("-e", "--env_label", help="env label",metavar="ENV_LABEL")
    parser_group.add_argument("-l", "--location", help="symbolic location of file",metavar="LOCATION")
    parser.add_argument("-k,", "--keywords", nargs='*', help="keyword value pair(s)",metavar="KEYWORDS")
    parser.add_argument("-H", "--html", help="generate html format",metavar="HTML")
    parser.add_argument("-R", "--replace", help="replace",action="store_true")
    parser.add_argument("-F", "--force", help="force",action="store_true")
    parser.add_argument("-v", "--verbose", help="verbose",action="store_true")
    parser.add_argument("-d", "--debug", help="debug",action="store_true")
    args = parser.parse_args()
    if args.path:
        if args.env_label: parser.error("You cannot specify an ENV_LABEL with the --path option")
    elif args.location:
        if not args.env_label: parser.error("You must specify an ENV_LABEL with the --location option")
    return args

def datamodel_wiki():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file_spec", help="unique name of file species",metavar="FILE_SPEC", required=True)
    parser.add_argument("-t", "--tree_ver", help="tree version",metavar="TREE_VER")
    parser_group = parser.add_mutually_exclusive_group()
    parser_group.add_argument("-p", "--path", help="symbolic path of file",metavar="PATH")
    parser.add_argument("-e", "--env_label", help="env label",metavar="ENV_LABEL")
    parser_group.add_argument("-l", "--location", help="symbolic location of file",metavar="LOCATION")
    parser.add_argument("-F", "--force", help="force",action="store_true")
    parser.add_argument("-v", "--verbose", help="verbose",action="store_true")
    parser.add_argument("-d", "--debug", help="debug",action="store_true")
    args = parser.parse_args()
    if args.path:
        if args.env_label: parser.error("You cannot specify an ENV_LABEL with the --path option")
    elif args.location:
        if not args.env_label: parser.error("You must specify an ENV_LABEL with the --location option")
    return args
