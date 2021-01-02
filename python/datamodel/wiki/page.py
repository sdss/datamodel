# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: page.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

from tree import Tree
from datamodel.wiki import Remote
from os.path import join, exists


__author__ = 'Joel Brownstein <joelbrownstein@sdss.org>'

class Page(object):
    """Class to store and update wiki pages.

    Parameters
    ----------
    options : command-line options, optional
    tree_ver : str, optional
        Override the tree version default set by modules
    space_ver : str, optional (defaults to sdsswork)
        Set the version of the datamodel space on the wiki
    file_spec : str, required
        Name of file species
    path : str, optional (required w/out env_label + location)
        Symbolic path to fits file (can be combined from
        the env_label/location if omitted)
    env_label : str, optional (required w/out path)
        the tree environmental variable (can be parsed from
        the symbolic path if omitted)
    location: str, optional (required w/out path)
        the partial symbolic path (can be parsed from the
        symbolic path if omitted)
    format : str, either md (default) or html
    force : bool (default false)
        set True to over-write the human edited yaml and
        restore it to the original template / fits file.
    """
    
    def __init__(self, options = None, tree_ver = None, space_ver = None, file_spec = None, path = None, env_label = None, location = None, format = None, force = None, verbose = None, debug = None):
        self.tree_ver = options.tree_ver if options else tree_ver
        self.space_ver = options.space_ver if options else space_ver
        if self.space_ver is None: self.space_ver = "sdsswork"
        self.file_spec = options.file_spec if options else file_spec
        self.path = options.path if options else path
        if self.path is None:
            self.env_label = options.env_label if options else env_label
            self.location = options.location if options else location
            self.path = join(self.env_label, self.location) if self.env_label and self.location else None
        else:
            try: self.env_label, self.location = self.path.split(sep, 1)
            except:
                self.env_label = options.env_label if options else env_label
                self.location = options.location if options else location
        self.format = options.format if options else format
        self.force = options.force if options else force
        self.verbose = options.verbose if options else verbose
        self.debug = options.debug if options else debug

    def set_tree(self):
        """Set the Tree from input options, or default to the current loaded module
        """
        if self.tree_ver is None:
            try:  self.tree_ver = environ['TREE_VER']
            except: pass
        self.tree = Tree(config = self.tree_ver)
        if self.tree_ver != self.tree.config_name: self.tree_ver = self.tree.config_name

    def set_remote(self):
        self.remote = Remote(verbose = self.verbose)
        self.remote.set_login()
        
    def get_title(self, root = None, parent = None):
        title = "Datamodel" if root else self.env_label if parent else self.file_spec
        title = ".%s v%s" % (title, self.space_ver) if title and self.space_ver else None
        return title

    def get_content(self, parent = None):
        if parent:
            content = "parent content"
        else:
            content = "file spec content"
        return content

    def set_remote_pagelist(self, root = None):
        self.remote.set_pagelist(parent = self.get_title(root = root))

    def create_parent(self):
        if self.remote.pagelist:
            if self.verbose: print("PAGE> found %s page (version=%r)" % (self.env_label, self.space_ver))
        else:
            self.set_remote_pagelist(root = True)
            self.create_page(title = self.get_title(parent = True), content = self.get_content(parent = True))
            self.set_remote_pagelist()

    def create_datamodel(self):
        if self.remote.pagelist:
            title = self.get_title()
            pages = self.remote.pagelist['data']
            pages = [page for page in pages if page['title'] == title]
            page = pages[0] if len(pages) == 1 else None
            if page:
                if self.verbose: print("PAGE> found %s page (version=%r)" % (self.file_spec, self.space_ver))
            else:
                self.create_page(title = title, content = self.get_content())
        else:
            print("PAGE> error creating %s page without finding parent %s page (version=%r)." % (self.file_spec, self.env_label, self.space_ver))

    def create_page(self, title = None, content = None):
        try: parent = self.remote.pagelist['parent']
        except: parent = None
        if parent and title and content:
            print("PAGE> create %s: %s with content=%r" % (parent,title,content))



