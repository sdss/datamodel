# @Author: Brian Cherinka
# @Date: Mar 7, 2016
# @Revised by: Joel Brownstein <joelbrownstein@sdss.org>
# @Date: Nov 9, 2020
# @Filename: stub.py
# @License: BSD 3-Clause
# @Copyright: SDSS.

import os
import yaml
import json
from json import dumps
from os.path import basename, exists, getsize, join, sep, splitext

from astropy.io import fits
from jinja2 import Environment, PackageLoader
from yaml import FullLoader, dump, load

from .parse import get_abstract_path
from ..git import Git


__author__ = "Brian Cherinka, Joel Brownstein"


# TODO - add path template to markdown
# TODO - consider moving access file into yaml
# TODO - consider yaml and fits validation to occur between stub and wiki

class Stub(object):
    """Class to create a datamodel stub.

    Parameters
    ----------
    file_spec : str, optional
        (unique) file species name
    directory : dict, optional
        dictionary of paths to output stub
    verbose : bool , optional
        if True, uses verbose output
    force : bool, optional
        if True, overwrites the HDU content only
    """

    fmap = {
        "A": "char",
        "I": "int16",
        "J": "int32",
        "K": "int64",
        "E": "float32",
        "D": "float64",
        "B": "bool",
        "L": "bool",
    }
    cache_formats = ["yaml"]

    def __init__(self, file_spec=None, directory=None, verbose=None, force=None, tree_ver=None,
                 release=None):
        # TODO - split out access into Access class
        # TODO - consolidate stub creation code
        # TODO - add git flag, i.e. update git workflow
        # TODO - create yaml stub first, not md
        # TODO - update yaml stub and add yaml validation

        self.file_spec = file_spec
        self.directory = directory
        self.verbose = verbose
        self.force = force
        self.tree_ver = tree_ver
        self.release = release

        self.template = None
        self.input = None
        self.output = None
        self.cache = None
        self.environment = None
        self.git = Git(verbose=self.verbose)

    def __repr__(self):
        return f'<Stub(file_spec={self.file_spec})>'

    def set_access(self, path: str, replace: bool = None) -> None:
        """ Sets and writes the access file

        Sets and write the access file, which contains the path name and
        template definition used by sdss_access.

        Parameters
        ----------
        path : str
            The path template, by default None
        replace : bool, optional
            If True, replaces any existing access path, by default None
        """
        self.access = None
        if not self.directory or 'access' not in self.directory:
            return

        # get access directory
        directory = self.directory["access"]
        if not exists(directory):
            print(f"STUB> nonexistent directory at {directory}")
            directory = None

        if not (directory and self.file_spec):
            return

        # construct access path
        access_path = os.path.join(directory, f"{self.file_spec}.access")

        if os.path.exists(access_path):
            with open(access_path) as file:
                print(f"STUB> access {access_path}")
                self.access = yaml.load(file, Loader=yaml.FullLoader)

                if self.release not in self.access:
                    _file_spec, _path = self.file_spec, path
                    self.access[self.release] = {'release': self.release, 'tree_ver': self.tree_ver,
                                                 'access': f"{self.file_spec} = ${path}"}
                    self.write_access(path=access_path, replace=replace)
                else:
                    _file_spec, _path = self.access[self.release]['access'].split(" = $", 2)
                    #_file_spec, _path = self.access['access'].split(" = $", 2)

                    # do nothing if the path is the same
                    if _path == path:
                        return

                    if replace:
                        self.drop_formats(file_spec=_file_spec, path=_path)
                        #self.access = f"{self.file_spec} = ${path}"
                        self.access[self.release] = {'release': self.release, 'tree_ver': self.tree_ver,
                                                     'access': f"{self.file_spec} = ${path}"}
                        self.write_access(path=access_path, replace=replace)
                    else:
                        print(f"STUB> Aborting due to conflict in existing spec: {self.access[self.tree_ver]['access']}")
        else:
            if replace:
                print(f"STUB> Nothing to replace, due to nonexistent access path: {access_path}")
            else:
                #self.access = f"{self.file_spec} = ${path}"
                self.access = {self.release: {'release': self.release, 'tree_ver': self.tree_ver,
                                              'access': f"{self.file_spec} = ${path}"}}
                self.write_access(path=access_path)

    def drop_formats(self, file_spec=None, path=None):
        formats = ["access", "yaml", "json"]
        for format in formats:
            if format == "access":
                self.drop_access(file_spec=file_spec, path=path)
            else:
                self.drop_format(format=format, file_spec=file_spec, path=path)

    def drop_access(self, file_spec: str = None, path: str = None) -> None:
        """ Removes the access file from git

        Deletes the access file locally and removes it from git

        Parameters
        ----------
        file_spec : str, optional
            the name of the file species, by default None
        path : str, optional
            the path to the access file, by default None
        """
        try:
            env_label = path.split(os.sep, 1)[0]
        except:
            env_label = None

        location = (
            os.path.join("datamodel", "products", "access", env_label, f"{file_spec}.access")
            if env_label and file_spec
            else None
        )

        if location:
            self.git.rm(location=location)
        else:
            print(f"STUB> Cannot drop access for file_spec={file_spec}, path={path}")

    def drop_format(self, format=None, file_spec=None, path=None):
        if path:
            path = get_abstract_path(path=path)
        location = (
            join("datamodel", "products", format, path, "%s.%r" % (file_spec, format))
            if format and file_spec and path
            else None
        )
        if location:
            self.git.rm(location=location)
        else:
            print("STUB> Cannot drop %s for file_spec=%r, path=%r" % (format, file_spec, path))

    def write_access(self, path: str = None, replace: bool = None) -> None:
        """ Write the access file

        Writes out the access file and commits it to git.

        Parameters
        ----------
        path : str, optional
            the access file path, by default None
        replace : bool, optional
            If True, replaces the existing file, by default None
        """
        try:
            if self.verbose:
                if replace:
                    print(f"STUB> Output to {path} [replaced!]")
                else:
                    print(f"STUB> Output to {path}")

            with open(path, "w") as file:
                file.write(yaml.dump(self.access, sort_keys=False))

            self.git.add(path=path)
            self.git.commit(path=path, message=f"committing {self.file_spec}.access")
        except Exception as e:
            print(f"STUB> Output exception {e}")

    def prepare_stub(self, path, replace, file, format='md'):
        self.set_access(path, replace=replace)
        self.set_input(path=file, format=format)
        self.set_input_hdus()
        self.set_environment()
        self.set_cache()
        self.set_template()
        self.set_output()
        self.set_result()

    def set_input(self, path: str = None, format: str = 'yaml') -> None:
        """ create the input for the stub template

        Given a file path, creates a dictionary of data inputs to be passed
        into the stub Jinja 2 template, for the given format.

        Parameters
        ----------
        path : str, optional
            A file path, by default None
        format : str, optional
            The format of the stub, by default yaml
        """
        self.input = None
        if not path or not self.access:
            return

        # create input dictionary for the template
        self.input = {"path": path, "file_spec": self.file_spec, "hdus": None}
        self.input['file_template'] = ''
        self.input["format"] = format
        self.input["basename"] = os.path.basename(path)
        self.input["filename"] = self.input["basename"].replace(".", r"\.")
        self.input["filesize"] = self.get_filesize()
        self.input["filetype"] = self.get_filetype()
        self.input["releases"] = [self.release]

        # create initial release dictionary for HDUs
        self.input['hdus'] = {self.release: None}

    def set_input_hdus(self) -> None:
        """Read the file and hdus."""
        if self.input:
            self.input["hdus"][self.release] = fits.open(self.input["path"])

    def set_environment(self) -> None:
        """Set the jina2 environment including filters for content."""
        loader = PackageLoader("datamodel", "templates")
        self.environment = Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

    def set_cache(self, format: str = "yaml") -> None:
        """ Set the cached content from the yaml file

        Retrieves any cached content and populates the
        cache dictionary.

        Parameters
        ----------
        format : str, optional
            The format of the stub, by default "yaml"
        """

        self.cache = None
        if not (self.input and format in self.cache_formats):
            return

        # get the file species and path to the cached yaml file
        file_spec = (
            self.input["file_spec"] if self.input and "file_spec" in self.input else None
        )
        dir = self.directory[format] if self.directory and format in self.directory else None
        # create an empty cached dictionary
        self.cache = (
            {"format": format, "path": join(dir, file_spec + "." + format)}
            if dir and file_spec
            else None
        )
        # read any cache content
        self.cache["content"] = self.get_content_from_cache()

        # load the hdu content into the cache
        self.set_cache_hdus()

    def update_cache_hdu_row(self, row=None, field=None):
        """ Set the name, etc. fields in the cached hdu """

        # only do something when the field is in the fits hdu or if the field is "description"
        if field and (hasattr(self.hdu, field) or field == "description"):
            if field in self.hdu_row and not self.force:
                # do nothing if the field is already in the hdu_row and we're not manually updating
                self.cached = True
            elif field == "header":
                # if field is header then add all the header keys to the hdu row
                header = self.hdu.header
                self.hdu_row[field] = []

                for key, value in header.items():
                    if self.is_header_keyword(key=key):
                        column = {"key": key, "value": value, "comment": header.comments[key]}
                        self.hdu_row["header"].append(column)

            elif field == "description":
                # add description
                self.hdu_row[field] = "replace me - with a description of the contents of this HDU"
            elif field == "size":
                # add file fize
                self.hdu_row[field] = self.format_bytes(getattr(self.hdu, field))
            else:
                # add the value of the field
                self.hdu_row[field] = getattr(self.hdu, field)
                self.cached = False

    def update_cache_hdu_column(self, row=None, index=None, column=None):
        """ Set the cached content for a colum in a hdu table """

        # create a new columns dict or access the existing one from the hdu row
        columns = self.hdu_row["columns"] if "columns" in self.hdu_row else {}

        # do nothing if the column name is already in the dict and we aren't forcing an update
        if column.name in columns and not self.force:
            pass
        else:
            # add a new column entry to the dictionary
            columns[column.name] = {
                "name": column.name.upper(),
                "type": self.format_type(column.format),
                "unit": self.nonempty_string(column.unit),
                "description": self.nonempty_string(),
            }

    def set_cache_hdus(self):
        """ Set the cached content for each hdu """

        # get the cached content and the FITS hdus for the given release
        # hdus could be an empty dict or have content
        content = self.cache["content"] if self.cache and "content" in self.cache else None
        hdus = content["hdus"][self.release] if content and "hdus" in content else None

        if hdus is not None:
            # loop over all input hdus
            for hdu_number, self.hdu in enumerate(self.input["hdus"][self.release]):
                row = f"hdu{hdu_number}"
                # create a new hdu row, dictionary containing hdu info
                self.hdu_row = (
                    hdus[row]
                    if hdus and row in hdus
                    else {}
                    if self.hdu.is_image
                    else {"columns": {}}
                )

                # add the basic information to the hdu row
                for field in ["name", "is_image", "description", "size"]:
                    self.update_cache_hdu_row(row=row, field=field)

                if self.hdu.is_image:
                    # add header keys to to the hdu row
                    if self.verbose:
                        print(f"HDU {hdu_number} >" + "IMAGE: %(name)s" % self.hdu_row)
                    self.update_cache_hdu_row(row=row, field="header")
                else:
                    # add binary table columns to the hdu row
                    if self.verbose:
                        print(
                            f"HDU {hdu_number} > " +
                            "TABLE: %(name)s" % self.hdu_row +
                            f" --> {len(self.hdu.columns)} columns"
                        )

                    # loop over all columns in the binary table
                    for index, column in enumerate(self.hdu.columns):
                        self.update_cache_hdu_column(row=row, index=index, column=column)

                # add/update the hdus content with the row
                hdus[row] = self.hdu_row

    def get_content_from_cache(self) -> dict:
        """ Retrieves the cache content from yaml file

        Looks for any existing yaml product file ands loads its content to
        the cache.  If not file exists, creates a new dictionary from the
        stub.yaml file.

        Returns
        -------
        dict
            The yaml content
        """
        # get the cache format and cache file path
        format = self.cache["format"] if self.cache and "format" in self.cache else None
        path = self.cache["path"] if self.cache and "path" in self.cache else None
        content = None

        # do nothing if format is not yaml
        if not path or format != 'yaml':
            return content

        if exists(path):
            # read in existing cached yaml file
            with open(path) as file:
                content = yaml.load(file, Loader=FullLoader)
                content = self._check_release_in_cache(content)
        else:
            # create brand new cache content using template input
            template = self.environment.get_template(f"stub.{format}")
            content = yaml.load(template.render(self.input), Loader=FullLoader)

        # add an hdus key if it doesn't exist
        if content and "hdus" not in content:
            content["hdus"] = {self.release: {}}

        # add a new release key in hdu if it doesn't exist
        if self.release not in content["hdus"]:
            content["hdus"][self.release] = {}

        return content

    def _check_release_in_cache(self, content):
        """ check that a release is in the cached content """
        releases = content['general']['releases']
        if self.release not in releases:
            releases.append(self.release)
            releases.sort()
            content['general']['releases'] = releases
        return content

    def format_bytes(self, value=None):
        """Convert an integer to human-readable format.

        Parameters
        ----------
        value : int
            An integer representing number of bytes.

        Returns
        -------
        str
            Size of the file in human-readable format.
        """

        try:
            value = int(value)
        except:
            value = 0

        for unit in ("bytes", "KB", "MB", "GB"):
            if value < 1024:
                return "{0:d} {1}".format(int(value), unit)
            else:
                value /= 1024.0

        return "{0:3.1f} {1}".format(value, "TB")

    def get_filesize(self):
        """Get the size of the input file.

        Returns
        -------
        str
            Size of the file in human-readable format.
        """
        return self.format_bytes(getsize(self.input["path"])) if self.input else None

    def get_filetype(self):
        """Get the extension of the input file.

        Returns
        -------
        str
            File type in upper case.
        """
        filename, file_extension = splitext(self.input["path"]) if self.input else None
        if "gz" in file_extension:
            filename, file_extension = splitext(filename)
        return file_extension[1:].upper()

    def nonempty_string(self, value=None):
        """Jinja2 Filter to map the format value to a string.

        Parameters
        ----------
        value : str?
            Not sure what type this is supposed to have.

        Returns
        -------
        string: str
            The string.
        """
        string = f"{value}" if value else 'replace me - with content'
        return string

    def format_type(self, value=None):
        """Jinja2 Filter to map the format type to a data type.

        Parameters
        ----------
        value : str?
            Not sure what type this is supposed to have.

        Returns
        -------
        str
            The data type.
        """
        out = [
            val if value.isalpha() else "{0}[{1}]".format(val, value[:-1])
            for key, val in self.fmap.items()
            if key in value
        ]
        return out[0]

    def is_header_keyword(self, key=None):
        """Test for hdu header keyword

        Returns
        -------
        bool
            ``True`` if `key` does *not* contain 'TFORM' or 'TTYPE'.
        """
        return tuple([key.find(f) for f in ("TFORM", "TTYPE")]) == (-1, -1)

    def set_output(self):
        # create the output file paths
        if self.input and self.template:
            self.output = {
                format: join(dir, self.file_spec + "." + format)
                for format, dir in self.directory.items()
            }
        else:
            self.output = None

    def get_yaml(self):
        return dump(self.cache["content"], sort_keys=False) if self.cache and "content" in self.cache else None

    def get_json(self):
        return dumps({}) if self.input else None

    def set_result(self, release=None, group='WORK'):
        """Set the result for the input by rendering the template,
        and set a json or yaml version of the input dictionary.
        """
        self.result = None
        format = self.input["format"] if self.input and "format" in self.input else None
        if format and self.template:
            selected_release = self.get_selected_release(release=release, group=group)
            hdus = self.cache['content']['hdus'][selected_release]
            self.input['selected_release'] = selected_release
            # render the markdown template (uses both input and cached content)
            self.result = {
                format: self.template.render(input=self.input, content=self.cache["content"],
                                             hdus=hdus)
            }
            # render the json and yaml contents
            self.result["json"] = self.get_json()
            self.result["yaml"] = self.get_yaml()

    def get_selected_release(self, release=None, group='WORK'):
        """ get the hdu content for a given release """
        cached_releases = list(self.cache['content']['hdus'].keys())
        if len(cached_releases) == 0:
            return release or self.release
        elif len(cached_releases) == 1:
            return cached_releases[0]
        elif release in cached_releases:
            return release
        else:
            if release and release not in cached_releases:
                print(f'Input release {release} unavailable in cache. '
                      f'Selecting latest release in group {group}')

            # TODO - move to separate function
            # groups releases and sorts them
            import itertools
            g = itertools.groupby(sorted(cached_releases, key=lambda x: x[0]), lambda x: x[0])
            key = {'D': 'DR', 'I': 'IPL', 'M': 'MPL', 'W': 'WORK'}
            rs = {}
            for i, gg in g:
                rs[key[i]] = sorted(gg, key=lambda x: int(x[2:]) if 'DR' in x else int(x[3:]) if 'PL' in x else x)

            # get latest release
            if group not in key.values():
                raise KeyError(f'group {group} is not a valid release group')
            elif group not in rs.keys():
                raise KeyError(f'group {group} is not yet a cached release')
            return rs[group][-1]

    def set_template(self):
        """Create the Jinja2 environment and set the template."""
        self.template = (
            self.environment.get_template("stub.%(format)s" % self.input)
            if self.environment and self.input
            else None
        )

    def write(self, format=None, skip_git=None):
        """ Write the output result to the output path.

        Parameters
        ----------
        format : str
            The file format to write to
        """
        if self.output and self.result:
            if format and format in self.output and format in self.result:
                path = self.output[format]
                try:
                    if self.verbose:
                        print("STUB> Output to %s" % path)
                    with open(path, "w") as file:
                        file.write(self.result[format])
                    if not skip_git:
                        self.git.add(path=path)
                        self.git.commit(path=path, message="%s.%s" % (self.file_spec, format))
                except Exception as e:
                    print("STUB> Output exception %r" % e)
            else:
                print("STUB> Invalid format=%r for write" % format)

    def close_input_hdus(self):
        """Close input hdus"""
        if self.input and "hdus" in self.input:
            self.input["hdus"][self.release].close()

    def remove_output(self) -> None:
        """ Delete the output format files """
        for key, val in self.output.items():
            if os.path.exists(val):
                os.remove(val)
