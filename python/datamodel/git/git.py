# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: remote.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

import re
from os import getenv
from os.path import join
from subprocess import check_output, CalledProcessError
from datamodel import log

__author__ = "Joel Brownstein <joelbrownstein@sdss.org>"


class Git(object):
    """Class to run the git commands."""

    actions = ["add", "checkout", "clone", "commit", "pull", "push", "rm", "status"]

    def __init__(self, verbose=None):
        self.verbose = verbose
        self.set_directory()

    def __repr__(self):
        return f'<Git (directory="{self.directory}")>'

    @property
    def current_branch(self):
        self.status()
        match = re.search(r'(^|#|\s+)On branch (?P<branch>[a-z0-9A-Z]+)\n', self.response)
        if match:
            return match.groupdict()['branch']

    def set_directory(self):
        self.directory = getenv("DATAMODEL_DIR")
        if not self.directory:
            log.error("GIT> cannot set directory.  Please set DATAMODEL_DIR.")

    def status(self, path=None, location=None):
        if path and not location:
            location = self.get_location_from_path(path=path)
        self.run_action(action="status", arg=location)

    def pull(self) -> None:
        """ Pull from Github remote origin

        Performs a "git pull" on the datamodel repo

        Raises
        ------
        RuntimeError
            when the subprocess git command fails
        """
        try:
            self.run_action(action="pull")
        except CalledProcessError as err:
            raise RuntimeError(f'Cannot perform git pull.  Check for merge conflicts or remote repo exists: {err}') from err

    def push(self) -> None:
        """ Push to Github remote origin

        Performs a "git push" on the datamodel repo

        Raises
        ------
        RuntimeError
            when the subprocess git command fails
        """
        try:
            self.run_action(action="push")
        except CalledProcessError as err:
            raise RuntimeError(f'Cannot perform git push.  Check for merge conflicts or outdated local repo: {err}') from err

    def rm(self, location: str = None) -> None:
        """ Remove a git remove of a file

        Performs a "git rm" on a given file.

        Parameters
        ----------
        location : str, optional
            The filepath to be removed, by default None

        Raises
        ------
        RuntimeError
            when the subprocess git command fails
        """
        try:
            self.run_action(action="rm", arg=location)
        except CalledProcessError as err:
            raise RuntimeError(f'Cannot perform git rm. Check for file conflicts: {err}') from err

    def get_location_from_path(self, path=None):
        if path:
            directory = join(self.directory, "") if self.directory else None
            location = path[len(directory):] if directory and path.startswith(directory) else None
        else:
            location = None
        return location

    def add(self, path: str = None, location: str = None) -> None:
        """ Add a file to the git repo

        Performs a "git add" on a given file.

        Parameters
        ----------
        path : str, optional
            the full path of the file to add, by default None
        location : str, optional
            the file location relative to the top datamodel directory, by default None

        Raises
        ------
        RuntimeError
            when the subprocess git command fails
        """
        # get the file location if none provided
        if path and not location:
            location = self.get_location_from_path(path=path)

        # if no file location found, do nothing
        if not location:
            return

        # get the status of the file
        self.status(location=location)
        if "Untracked files" in self.response:
            try:
                self.run_action(action="add", arg=location)
            except CalledProcessError as err:
                raise RuntimeError(f'Cannot perform git add. Check for proper file and path: {err}') from err

    def clone(self, product=None, branch=None):
        if product and branch:
            self.run_action(action="clone", args=[product, branch])

    def checkout(self, branch=None):
        if branch:
            self.run_action(action="checkout", arg=branch)

    def commit(self, path: str = None, location: str = None, all: bool = None,
               message: str = None) -> None:
        """ Commit a file to the git repo

        Performs a "git commit" on a given file.

        Parameters
        ----------
        path : str, optional
            the full path of the file to add, by default None
        location : str, optional
            the file location relative to the top datamodel directory, by default None
        all : bool, optional
            if True commits everything in the repo, by default None
        message : str, optional
            a git commit message, by default None

        Raises
        ------
        RuntimeError
            when the subprocess git command fails
        """
        args = ["--all"] if all else []

        # a git commit message is required
        if not message:
            log.error("GIT> commit requires message")
            return

        args += ["-m", message]
        # get the location if none is provided
        if path and not location:
            location = self.get_location_from_path(path=path)

        if location and not all:
            args += [location]
            self.status(location=location)
            if "new file" in self.response or "modified" in self.response:
                try:
                    self.run_action(action="commit", args=args)
                except CalledProcessError as err:
                    raise RuntimeError(f'Cannot perform git commit. Check for problems: {err}') from err
        elif all:
            try:
                self.run_action(action="commit", args=args)
            except CalledProcessError as err:
                raise RuntimeError(f'Cannot perform git commit. Check for problems: {err}') from err

    def run_action(self, action=None, arg=None, args=None):
        if action in self.actions:
            self.action = [action]
            if arg:
                self.action += [arg]
            elif args:
                self.action += args
            self.set_command()
            self.set_response()
            if self.verbose:
                self.print_response()
        else:
            print("GIT> %r is not a valid git action" % action)

    def set_command(self):
        self.command = ["git"] + self.action if self.action else None
        if self.command and self.verbose:
            log.info("GIT> %s" % " ".join(self.command))

    def set_response(self):
        self.response = (
            check_output(self.command, cwd=self.directory, universal_newlines=True).rstrip()
            if self.command and self.directory
            else None
        )

    def print_response(self):
        if self.response:
            for index, response in enumerate(self.response.split("\n")):
                if response:
                    log.info("%s %s" % (" " * 4 if index else "GIT>", response))
