# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: install.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

from datamodel.git import Git
from os import environ, makedirs, remove
from os.path import join, exists, dirname
from shutil import rmtree
from pathlib import Path

__author__ = 'Joel Brownstein <joelbrownstein@sdss.org>'

class Install(object):
    """Class to install a copy in the user's directory.

    Parameters
    ----------
    options : command-line options, optional
    branch : str, optional
        the branch to install (main by default)
    force : bool (default false)
        set True to over-write the software branch
        and modulefile.
    """
    
    product = "git@github.com:sdss/datamodel.git"

    def __init__(self, options = None, branch = None, force = None, verbose = None, debug = None):
        self.branch = options.branch if options else branch
        if not self.branch: self.branch = 'main'
        self.force = options.force if options else force
        self.verbose = options.verbose if options else verbose
        self.debug = options.debug if options else debug
        self.git = Git(verbose = self.verbose)
        self.message = []

    def set_directory(self):
        """Set the software and modulefiles directory
           and confirm it exists (try making it if it doesn't)
        """
        home = str(Path.home())
        self.directory = {'home': home}
        
        try: self.directory['etc'] = join(environ['DATAMODEL_DIR'], 'etc')
        except: self.directory['etc'] = None
        
        try: self.directory['software'] = environ['DATAMODEL_INSTALL_DIR']
        except: self.directory['software'] = join(home, 'software', 'datamodel')
        
        try: self.directory['root'] = dirname(self.directory['software'])
        except: self.directory['root'] = None
        
        self.directory['modulefiles'] = join(home, '.modulefiles', 'datamodel')
        
        self.make_folder(folders = ['software', 'modulefiles'])
        self.directory['branch'] = join(self.directory['software'], self.branch) if self.directory['software'] and self.branch else None

    def make_folder(self, folders = None):
        if folders:
            for folder in folders:
                if folder in self.directory:
                    directory = self.directory[folder]
                    try:
                        if not exists(directory): makedirs(directory)
                    except Exception as e:
                        print("INSTALL> cannot make %r folder due to %r" % (folder, e))
                        self.directory[folder] = None

    def clone(self):
        if self.branch:
            if self.directory and 'software' in self.directory:
                if exists(self.directory['software']):
                    if exists(self.directory['branch']):
                        if self.force:
                            if self.verbose: print("INSTALL> removing %(branch)s due to --force" % self.directory)
                            try: rmtree(self.directory['branch'])
                            except Exception as e:
                                print("INSTALL> cannot remove branch due to %r" % e)
                                self.directory['branch'] = None
                        else:
                            print("INSTALL> Cannot overwrite branch folder at %(branch)s without --force" % self.directory)
                            self.directory['branch'] = None
                    if self.directory['branch']:
                        self.git.directory = self.directory['software']
                        if self.verbose: print("INSTALL> Preparing to clone datamodel to %(branch)s" % self.directory)
                        self.git.clone(product = self.product, branch = self.branch)
                        self.message.append(self.branch + " branch installed at path=%(branch)r" % self.directory)
                else:
                    print("INSTALL> Nonexistent install directory path=%(software)r" % self.directory)
    
    def checkout_branch(self):
        if self.branch:
            if self.directory and 'branch' in self.directory:
                if exists(self.directory['branch']):
                    self.git.directory = self.directory['branch']
                    self.git.checkout(branch = self.branch)

    def set_modulefile(self):
        self.modulefile = None
        if self.branch:
            self.modulefile = {'path': None, 'content': None, 'etc': None}
            if self.directory and 'etc' in self.directory and 'root' in self.directory:
                if self.directory['etc'] and exists(self.directory['etc']):
                    self.modulefile['etc'] = join(self.directory['etc'], 'datamodel.module')
                    with open(self.modulefile['etc']) as etc_file:
                        self.modulefile['content'] = etc_file.read()
                else:
                    print("INSTALL> Nonexistent etc directory path=%(etc)r" % self.directory)
                if self.modulefile['content'] and self.directory['root']:
                    try:
                        self.modulefile['content'] = self.modulefile['content'].format(name = "datamodel", version = self.branch, root = self.directory['root'])
                    except: self.modulefile['content'] = None
            if self.directory and 'modulefiles' in self.directory:
                if exists(self.directory['modulefiles']):
                    self.modulefile['path'] = join(self.directory['modulefiles'], self.branch)
                    if exists(self.modulefile['path']):
                        if self.force:
                            if self.verbose: print("INSTALL> removing %(path)s due to --force" % self.modulefile)
                            try: remove(self.modulefile['path'])
                            except Exception as e:
                                print("INSTALL> cannot remove modulefile due to %r" % e)
                                self.modulefile['path'] = None
                        else:
                            print("INSTALL> Cannot overwrite modulefile without --force")
                            self.modulefile['path'] = None
            if self.modulefile['path'] and self.modulefile['content']:
                try:
                    with open(self.modulefile['path'], 'w') as file: file.write(self.modulefile['content'])
                    self.message.append("please do the following in a new terminal:\n$ module load datamodel/%s" % self.branch)
                    if self.verbose: print("INSTALL> modulefile added at path=%(path)r" % self.modulefile)
                except Exception as e:
                    print("INSTALL> unable to add modulefile due to %r" % e)

    def done(self):
        if self.message: print("INSTALL> %s." % ", ".join(self.message))
