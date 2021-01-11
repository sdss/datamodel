# encoding: utf-8
#
# @Author: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: page.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

from tree import Tree
from datamodel.wiki import Remote
from datamodel import get_abstract_key
from os.path import join, exists, dirname
from os import getenv
from yaml import load, FullLoader
from jinja2 import Environment, PackageLoader
from re import findall


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
    force : bool (default false)
        set True to over-write the human edited yaml and
        restore it to the original template / fits file.
    """
    
    def __init__(self, options = None, tree_ver = None, space_ver = None, file_spec = None, path = None, env_label = None, location = None, force = None, verbose = None, debug = None):
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
        self.force = options.force if options else force
        self.verbose = options.verbose if options else verbose
        self.debug = options.debug if options else debug
        self.set_directory()
        self.set_data()
        self.set_environment()

    def set_directory(self):
        """Set the datamodel directory
        """
        self.directory= getenv('DATAMODEL_DIR')

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
        #title = ".%s v%s" % (title, self.space_ver) if title and self.space_ver else None
        return title

    def set_path_from_access(self, access = None):
        access_path = join(self.directory, access) if self.directory and access else None
        if access_path and exists(access_path):
            with open(access_path) as file:
                if self.verbose: print("PAGE> access %s" % access_path)
                self.access = load(file, Loader=FullLoader)
                _file_spec, _path = self.access.split(" = $", 2)
                if self.path is None:
                    self.path = _path
                    if self.verbose: print("PAGE> path=%r" % self.path)
                elif self.path != _path:
                    print("PAGE> Aborting due to conflict in path (does not match) access file definition")
                    self.path = None

    def set_data(self, parent = None):
        if self.file_spec:
            access = join('data', 'access', self.env_label, '%s.access' % self.file_spec) if self.env_label else None
            self.set_path_from_access(access = access)
            self.set_abstract_path()
            dir = dirname(self.abstract_path) if self.abstract_path else None
            markdown = join('data', 'md', dir, '%s.md' % self.file_spec) if dir else None
            self.data = {'markdown': markdown, 'access': access} if markdown and access else None
        else: self.data = None

    def get_content(self, parent = None):
        self.set_template(parent = parent)
        data = None if parent else self.data
        return self.template.render(data = data) if self.template else None

    def set_remote_pagelist(self, root = None, parent = None):
        self.remote.set_pagelist(parent = self.get_title(root = root, parent = parent))

    def create_parent(self):
        if self.remote.pagelist:
            if self.verbose: print("PAGE> found %s page (version=%r)" % (self.env_label, self.space_ver))
        else:
            self.set_remote_pagelist(root = True)
            try: parent = self.remote.pagelist['parent']
            except: parent = None
            title = self.get_title(parent = True)
            content = self.get_content(parent = True)
            self.create_page(parent = parent, title = title, content = content)

    def create_datamodel(self):
        if self.remote.pagelist:
            title = self.get_title()
            pages = self.remote.pagelist['data']
            pages = [page for page in pages if page['title'] == title]
            page = pages[0] if len(pages) == 1 else None
            if page:
                if self.verbose: print("PAGE> found %s page (version=%r)" % (self.file_spec, self.space_ver))
            else:
                parent = self.get_title(parent = True)
                content = self.get_content()
                self.create_page(parent = parent, title = title, content = content)
        else:
            print("PAGE> error creating %s page without finding parent %s page (version=%r)." % (self.file_spec, self.env_label, self.space_ver))

    def create_page(self, parent = None, title = None, content = None, convert = None):
        if title and content: self.remote.add_page(parent = parent, title = title, content = content, convert = convert)

    def set_environment(self):
        """Set the jina2 environment including filters for content.
        """
        loader = PackageLoader('datamodel', 'templates')
        self.environment = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

    def set_template(self, parent = None):
        """Create the Jinja2 environment and set the template.
        """
        
        pagetype = "parent" if parent else "page"
        html = "wiki-%s.html" % pagetype
        self.template = self.environment.get_template(html) if self.environment else None
    
    def set_abstract_path(self):
        """Replace keywords with upper case for
        the astract path
        """
        self.abstract_path = self.path
        if self.path:
            for keyword in findall(r'\{.*?\}', self.path):
                abstract_key = get_abstract_key(key = keyword.replace('{','').replace('}',''))
                self.abstract_path = self.abstract_path.replace(keyword, abstract_key)
        if self.verbose: print("PAGE> abstract_path=%r" % self.abstract_path)

    def write(self, format = None):
        """Write the output result to the output path.
        """
        if self.output and self.result:
            if format and format in self.output and format in self.result:
                path = self.output[format]
                try:
                    if self.verbose: print("STUB> Output to %s" % path)
                    with open(path, 'w') as file: file.write(self.result[format])
                    self.git.add(path=path)
                    self.git.commit(path=path, message='%s.%s' % (self.file_spec, format))
                except Exception as e:
                    print("STUB> Output exception %r" % e)
            else:
                print("STUB> Invalid format=%r for write" % format)
