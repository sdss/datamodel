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
    
    actions = ['add', 'commit', 'pull', 'push', 'rm', 'status']

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
    
    def push(self):
        self.run_action(action = 'push')
    
    def rm(self, location = None):
        self.run_action(action = 'rm', arg = location)

    def get_location_from_path(self, path = None):
        if path:
            directory = join(self.directory,'') if self.directory else None
            location = path[len(directory):] if directory and path.startswith(directory) else None
        else: location = None
        return location

    def add(self, path = None, location = None):
        if path and not location:
            location = self.get_location_from_path(path = path)
        if location: self.run_action(action = 'add', arg = location)
    
    def commit(self, path = None, location = None, all = None, message = None):
        args = ['--all'] if all else []
        if message:
            args += ['-m', messsage]
            if path and not location:
                location = self.get_location_from_path(path = path)
            if location and not all: args += [location]
            self.run_action(action = 'commit', args = args)
        else: print("GIT> commit requires message")
    
    def run_action(self, action = None, arg = None, args = None):
        if action in self.actions:
            self.action = [action]
            if arg: self.action += [arg]
            elif args: self.action += args
            self.set_command()
            self.set_response()
            if self.verbose: self.print_response()
        else:
            print("GIT> %r is not a valid git action" % action)

    def set_command(self):
        self.command = ['git'] + self.action if self.action else None
        if self.command and self.verbose: print("GIT> %s" % " ".join(self.command))

    def set_response(self):
        self.response = check_output(self.command,cwd=self.directory,universal_newlines=True).rstrip() if self.command and self.directory else None

    def print_response(self):
        if self.response:
            for index, response in enumerate(self.response.split('\n')):
                if response: print("%s %s" % (" "*4 if index else "GIT>", response))
