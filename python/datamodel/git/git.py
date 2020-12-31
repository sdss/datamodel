# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: remote.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

from os import getenv
from os.path import join, exists, basename
from subprocess import check_output


__author__ = 'Joel Brownstein <joelbrownstein@sdss.org>'

class Git(object):
    """Class to run the git commands.
    """
    
    actions = ['status', 'pull']

    def __init__(self, verbose = None):
        self.verbose = verbose
        self.set_directory()
    
    def set_directory(self):
        self.directory = getenv("DATAMODEL_DIR")
        if not self.directory: print("GIT> cannot set directory.  Please set DATAMODEL_DIR.")

    def status(self):
        self.run_action(action = 'status')
    
    def pull(self):
        self.run_action(action = 'pull')
    
    def delete(self, location = None):
        self.action = ['delete']
    
    def run_action(self, action = None):
        if action in self.actions:
            self.action = [action]
            self.set_command()
            self.set_response()
            if self.verbose: print("GIT> %r" % self.response)
        else:
            print("GIT> %r is not a valid git action" % action)

    def set_command(self):
        self.command = ['git'] + self.action if self.action else None

    def set_response(self):
        self.response = check_output(self.command,cwd=self.directory,universal_newlines=True).rstrip() if self.command and self.directory else None
