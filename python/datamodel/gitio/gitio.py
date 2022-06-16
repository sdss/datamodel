# !/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import pathlib
import uuid

from git import Repo, InvalidGitRepositoryError, GitCommandError

from datamodel import log

__all__ = ["Git"]

class Git(object):
    """ Class to run the git commands

    Wrapper class to the GitPython package.
    """

    def __init__(self, verbose=None):
        self.verbose = verbose

        # try to initialize the git repo
        try:
            self.repo = Repo(self.directory)
        except InvalidGitRepositoryError:
            self.repo = None
        else:
            if self.verbose:
                log.info(f"Instantiating new repo for {self.directory}")

    def __repr__(self) -> str:
        return f'<Git (directory="{self.directory}", branch="{self.current_branch}")>'

    @property
    def directory(self) -> str:
        """ the directory of the git repo """
        dmdir = os.getenv("DATAMODEL_DIR")
        if not dmdir:
            p = pathlib.Path(__file__)
            dmdir = p.resolve().parent.parent.parent.parent
        return dmdir

    @property
    def current_branch(self) -> str:
        """ the current active branch"""
        return self.repo.active_branch.name if self.repo else ''

    @property
    def branch_exists_on_remote(self) -> bool:
        """ if the current active branch exists at the remote """
        return self.repo.active_branch.tracking_branch() is not None

    @property
    def is_main_branch(self) -> bool:
        """ if the current active branch is the main branch """
        return self.current_branch == 'main'

    @property
    def origin(self):
        """ the git remote origin """
        return self.repo.remotes.origin

    @property
    def is_dirty(self) -> bool:
        """ if the repo is dirty"""
        return self.repo.is_dirty()

    def list_branches(self, pprint: bool = None) -> list:
        """ List all local branches for the repo """
        return [b.name for b in self.repo.branches] if pprint else self.repo.branches

    def list_remotes(self, pprint: bool = None) -> list:
        """ List all remotes for the repo """
        return [r.name for r in self.repo.remotes] if pprint else self.repo.remotes

    def set_repo(self):
        """ Set the repo if needed """
        if not self.repo:
            self.repo = Repo(self.directory)

    def create_new_branch(self, branch: str = None):
        """ Create a new branch

        Create a new branch.  If no branch name is provided, it will create
        a branch name based on the email head found in the git user config.  If
        none found, creates a random branch name using a UUID.

        Parameters
        ----------
        branch : str, optional
            the name of the branch to create, by default None
        """

        if not branch:
            cfg = self.repo.config_reader()
            if cfg.has_option("user", "email"):
                name = cfg.get("user", "email").split("@")[0]
            else:
                name = str(uuid.uuid4())[:13]
            branch = f'dmgen_{name}'
        self.checkout(branch=branch)

    def status(self) -> str:
        """ Return the git status of the repo """
        return self.repo.git.status()

    def clone(self, product: str = None, branch: str = None):
        """ Clones the git repo

        Performs a "git clone" of the datamodel repo.

        Parameters
        ----------
        product : str, optional
            the Github repo URL by default None
        branch : str, optional
            the name or directory path of the clone, by default None

        Raises
        ------
        RuntimeError
            when the git command fails
        """
        product = product or "git@github.com:sdss/datamodel.git"
        branch = branch or self.current_branch or "main"
        self.repo = Repo.clone_from(product, branch)

        if self.verbose:
            log.info(f"Cloning new repo to {branch}.")

        # temporarily set the DATAMODEL_DIR to the new clone working directory
        os.environ["DATAMODEL_DIR"] = self.repo.working_dir

    def checkout(self, branch: str = None):
        """ Checks out a branch from the git repo

        Performs a "git checkout" on the datamodel repo.  If the branch does not
        exist, it will be created.

        Parameters
        ----------
        branch : str, optional
            the name of the branch to checkout, by default None

        Raises
        ------
        RuntimeError
            when the git command fails
        """
        # get a branch name
        branch = branch or self.current_branch or "main"

        # create the branch if needed
        if branch not in self.list_branches():
            log.warning(f"Git branch {branch} does not exist.  Creating it.")
            try:
                self.repo.git.checkout(b=branch)
            except GitCommandError as err:
                raise RuntimeError(f'Cannot perform git checkout.  Check for problems: {err}') from err
            return

        # checkout the existing branch
        try:
            self.repo.git.checkout(branch)
        except GitCommandError as err:
            raise RuntimeError(f'Cannot perform git checkout.  Check for problems: {err}') from err
        else:
            if self.verbose:
                log.info(f"Checking out branch {branch}.")

    def get_path_location(self, path: str = None) -> str:
        """ Gets the path location

        Gets the location relative to the git repo directory
        of the filepath.

        Parameters
        ----------
        path : str, optional
            the full path of the file to add, by default None

        Returns
        -------
        str
            the relative location of the path
        """
        if not path:
            return None

        x = str(path).partition(self.directory)
        if not x[-1]:
            return None

        return x[-1][1:]

    def check_if_untracked(self, path: str = None) -> bool:
        """ Checks if a file is untracked in the git repo

        Parameters
        ----------
        path : str, optional
            the full path of the file to add, by default None

        Returns
        -------
        bool
            if the file is untracked
        """
        if not path:
            return None

        location = self.get_path_location(path)
        if not location:
            return None

        return location in self.repo.untracked_files

    def rm(self, path: str = None):
        """ Remove a file from the git repo

        Performs a "git rm" on the datamodel repo

        Parameters
        ----------
        path : str, optional
            the full path of the file to remove, by default None

        Raises
        ------
        AttributeError
            when on the main branch
        RuntimeError
            when the git command fails
        """
        if self.is_main_branch:
            raise AttributeError("Cannot remove files from the main branch. Please make your changes in a new branch.")

        if not path:
            return

        try:
            self.repo.index.remove(path)
        except GitCommandError as err:
            raise RuntimeError(f'Cannot perform git rm.  Check for file conflicts: {err}') from err
        else:
            if self.verbose:
                log.info(f"Removing file {path}")

    def add(self, path: str = None):
        """ Add a file to the git repo

        Performs a "git add" on the datamodel repo

        Parameters
        ----------
        path : str, optional
            the full path of the file to add, by default None

        Raises
        ------
        AttributeError
            when on the main branch
        RuntimeError
            when the git command fails
        """
        if self.is_main_branch:
            raise AttributeError("Cannot add files to the main branch. Please make your changes in a new branch.")

        if not path:
            return

        if not self.check_if_untracked(path):
            if self.verbose:
                log.info(f"{path} is not an untracked file. Cannot add.")
            return

        try:
            self.repo.index.add(path)
        except GitCommandError as err:
            raise RuntimeError(f'Cannot perform git add.  Check for proper file and path existence: {err}') from err
        else:
            if self.verbose:
                log.info(f"Added new file {path}")

    def commit(self, message: str = None):
        """ Commit a file to the git repo

        Performs a "git commit" on the datamodel repo

        Parameters
        ----------
        message : str, optional
            a git commit message, by default None

        Raises
        ------
        AttributeError
            when on the main branch
        RuntimeError
            when the git command fails
        """
        if self.is_main_branch:
            raise AttributeError("Cannot commit files to the main branch. Please make your changes in a new branch.")

        if not message:
            message = 'a default datamodel commit message. I have done something, but do not know what.'

        try:
            self.repo.index.commit(message)
        except GitCommandError as err:
            raise RuntimeError(f'Cannot perform git commit.  Check for problems: {err}') from err
        else:
            if self.verbose:
                log.info(f"Committed change with message: {message}")

    def _push(self, cmd):
        """ Generic wrapper around git push """
        try:
            cmd
        except GitCommandError as err:
            raise RuntimeError(f'Cannot perform git push.  Check for merge conflicts or outdated local repo: {err}') from err
        else:
            if self.verbose:
                log.info("Pushing to repo.")

    def push(self):
        """ Push to Github remote origin

        Performs a "git push" on the datamodel repo

        Raises
        ------
        RuntimeError
            when the current branch does not exist on remote
        RuntimeError
            when the current repo is dirty
        RuntimeError
            when the git command fails
        """

        if self.repo.is_dirty():
            raise RuntimeError('Current repo is dirty.  Please stash or commit your changes before pushing.')

        if not self.branch_exists_on_remote:
            log.warning(f'Current active branch {self.current_branch} does not exist on remote. Setting upstream to {self.origin.name}.')
            self._push(self.origin.push(self.repo.active_branch, set_upstream=True))
            return

        self._push(self.origin.push())

    def pull(self):
        """ Pull from Github remote origin

        Performs a "git pull" on the datamodel repo

        Raises
        ------
        RuntimeError
            when the current branch does not exist on remote
        RuntimeError
            when the current repo is dirty
        RuntimeError
            when the git command fails
        """
        if not self.branch_exists_on_remote:
            raise RuntimeError(f'Current active branch {self.current_branch} does not exist on remote.')

        if self.repo.is_dirty():
            raise RuntimeError('Current repo is dirty.  Please stash or commit your changes before pulling.')

        try:
            self.origin.pull()
        except GitCommandError as err:
            raise RuntimeError(f'Cannot perform git pull.  Check for merge conflicts or remote repo exists: {err}') from err
        else:
            if self.verbose:
                log.info("Pulling from repo.")

    def fetch(self):
        """ Fetch from Github remote origin

        Performs a "git fetch" on the datamodel repo

        Raises
        ------
        RuntimeError
            when the git command fails
        """

        try:
            self.origin.fetch()
        except GitCommandError as err:
            raise RuntimeError(f'Cannot perform git fetch.  Check for merge conflicts or remote repo exists: {err}') from err
        else:
            if self.verbose:
                log.info("Fetching from repo.")
