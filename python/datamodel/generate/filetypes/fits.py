# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os

from typing import List, Union
from astropy.io import fits

from datamodel import log
from datamodel.models.yaml import HDU
from .base import BaseFile, format_bytes


class FitsFile(BaseFile):
    """ Class for supporting FITS files """
    suffix = 'FITS'
    cache_key = 'hdus'

    def _update_partial_cache(self, cached_hdus: dict, old_hdus: dict) -> dict:
        """ Partially updates an existing cache

        Updates a new cache with values from an old cache.  Useful for reusing human-edited
        cache content.

        Parameters
        ----------
        cached_hdus : dict
            The new cache hdus section
        old_hdus : dict
            The old cache hdus section

        Returns
        -------
        dict
            The cache dictionary
        """
        old_names = [v['name'] for v in old_hdus.values()]

        for k, v in cached_hdus.items():
            # skip extensions that aren't in the old HDU
            if v['name'] not in old_names:
                continue

            # get current hdu index
            current_idx = int(k.split('hdu')[-1])

            # get the matching old hdu index
            idx = old_names.index(v['name']) if v['name'] else current_idx
            oldkey = f'hdu{idx}'

            # issue a warning if the extension has no name
            if not v['name']:
                log.warning(f'HDU ext {current_idx} in {self.file_species} has no '
                            'proper FITS extension name.  This breaks SDSS name formatting.  '
                            'Please correct the FITS file.')

            # update the HDU description
            v['description'] = old_hdus[oldkey]['description']

            # skip processing of image extensions
            if v['is_image'] is True:
                continue

            for kk, vv in v['columns'].items():
                # if a new column is not in the old cache of columns, add it
                if kk not in old_hdus[oldkey]['columns']:
                    column = self._extract_hdu_column(current_idx, kk)
                    v['columns'][kk] = self._generate_column_dict(column)
                    continue
                vv['unit'] = old_hdus[oldkey]['columns'][kk]['unit']
                vv['description'] = old_hdus[oldkey]['columns'][kk]['description']

        return cached_hdus

    def _generate_new_cache(self) -> dict:
        """ Generates a branch new HDU cache

        Loops over all the HDUs in a FITS file and converts them
        to dictionary format for insertion into the cache.

        Returns
        -------
        dict
            the HDU formatted for the YAML dictionary
        """
        hdus = {}

        with fits.open(self.filename) as hdulist:
            for hdu_number, hdu in enumerate(hdulist):

                # issue a warning if the extension has no name
                if not hdu.name:
                    log.warning(f'HDU ext {hdu_number} in {self.file_species} has no '
                                'proper FITS extension name.  This breaks SDSS name formatting.  '
                                'Please correct the FITS file.')

                # convert an HDU to a dictionary
                row = self._convert_hdu_to_dict(hdu)

                # generate HDU extension number
                extno = f'hdu{hdu_number}'
                hdus[extno] = row
        return hdus

    def _convert_hdu_to_dict(self, hdu: fits.hdu.base._BaseHDU, description: str = None) -> dict:
        """ Convert an HDU into a dictionary entry """
        header = hdu.header

        # create a new one
        row = {
            'name': hdu.name,
            'description': description or 'replace me description',
            'is_image': hdu.is_image,
            'size': format_bytes(hdu.size),
        }

        if hdu.is_image:
            row['header'] = []
            for key, value in header.items():
                if self._is_header_keyword(key=key):
                    column = {"key": key, "value": value, "comment": header.comments[key]}
                    row['header'].append(column)
        else:
            row['columns'] = {}
            for column in hdu.columns:
                row['columns'][column.name] = self._generate_column_dict(column)
        return row

    def _extract_hdu_column(self, ext: str, key: str) -> fits.Column:
        """ Extract a column from a Astropy HDU table extension """
        with fits.open(self.filename) as hdulist:
            return hdulist[ext].columns[key]

    def _generate_column_dict(self, column: fits.Column) -> dict:
        """ Generates a dictionary entry for an Astropy table column """
        return {'name': column.name.upper(),
                'type': self._format_type(column.format),
                'unit': self._nonempty_string(column.unit),
                'description': self._nonempty_string()}

    def design_content(self, ext: str = 'primary', extno: int = None, name: str = 'EXAMPLE',
                   description: str = None, header: Union[list, dict, fits.Header] = None,
                   columns: List[Union[list, dict, fits.Column]] = None, **kwargs) -> None:
        """ Design a new HDU

        Design a new astropy HDU for the given datamodel.  Specify the extension type ``ext``
        to indicate a PRIMARY, IMAGE, or BINTABLE HDU extension.  Each new HDU is added to the
        YAML structure using next hdu extension id found, or the one provided with ``extno``.  Use
        ``name`` to specify the name of the HDU extension.

        ``header`` can be a `~astropy.io.fits.Header` instance, a list of tuples of header keywords,
        conforming to (keyword, value, comment), or list of dictionaries conforming to
        {"keyword": keyword, "value": value, "comment": comment}.

        ``columns`` can be a list of `~astropy.io.fits.Column` objects, a list of tuples
        minimally conforming to (name, format, unit), or list of dictionaries minimally conforming
        to {"name": name, "format": format, "unit": unit}.  See Astropy's Binary Table
        `Column Format <https://docs.astropy.org/en/stable/io/fits/usage/table.html#column-creation>`_
        for the allowed format values.  When supplying a list of tuples or dictionaries, can include
        any number of valid arguments into `~astropy.io.fits.Column`.

        Parameters
        ----------
        ext : str, optional
            the type of HDU to create, by default 'primary'
        extno : int, optional
            the extension number, by default None
        name : str, optional
            the name of the HDU extension, by default 'EXAMPLE'
        description: str, optional
            a description for the HDU, by default None
        header : Union[list, dict, fits.Header], optional
            valid input to create a Header, by default None
        columns : List[Union[list, dict, fits.Column]], optional
            a list of binary table columns, by default None
        force : bool
            If True, forces a new design even if the HDU already exists, by default None
        **kwargs, optional
            additional keyword arguments to pass to the HDU constructor

        Raises
        ------
        ValueError
            when the ext type is not supported
        ValueError
            when the table columns input is not a list
        """
        if not self.design or (self.filename and os.path.exists(self.filename)):
            log.warning('Cannot design an HDU when not in the datamodel design phase or '
                        'if a real file already exists.')
            return

        cached_hdus = self._cache['releases']['WORK'][self.cache_key]

        if ext not in ['primary', 'image', 'table']:
            raise ValueError('Can only design a primary, image, or table HDU extension.')

        # check header keyword
        if header and not isinstance(header, fits.Header) and isinstance(header, (list, dict)):
            header = fits.Header(header)
        else:
            header = fits.Header()

        # check binary table column keywords
        if ext == 'table':
            if columns and not isinstance(columns, list):
                raise ValueError('columns keyword must be a valid list')
            elif not columns:
                columns = [fits.Column(name='EXAMPLE', format='A5')]
            elif isinstance(columns[0], dict):
                columns = [fits.Column(**c) for c in columns]
            elif isinstance(columns[0], (list, tuple)):
                columns = [fits.Column(*c) for c in columns]

        # generate a new HDU extension
        if ext == 'primary':
            hdu = fits.PrimaryHDU(header=header, **kwargs)
        elif ext == 'image':
            hdu = fits.ImageHDU(name=name, header=header, **kwargs)
        elif ext == 'table':
            hdu = fits.BinTableHDU.from_columns(name=name,
                                                columns=columns,
                                                header=header, **kwargs)

        # convert the new HDU to a dictionary
        row = self._convert_hdu_to_dict(hdu, description=description)

        # determine the extension number
        existing_hdus = [int(i.split('hdu')[-1]) for i in cached_hdus]
        if existing_hdus:
            max_extno = max(existing_hdus)
            if extno and extno <= max_extno:
                log.warning(f'ExtNo {extno} is lower than existing max extension {max_extno}. '
                            'Using next extension id {max_extno + 1}')
            elif not extno:
                log.warning(f'Found existing extensions.  Using next extension id {max_extno + 1}')
            extno = max_extno + 1
        else:
            extno = 0 if ext == 'primary' else 1

        # add the designed HDU to the cache
        extno = f'hdu{extno}'
        cached_hdus[extno] = row
        self._cache['releases']['WORK'][self.cache_key] = cached_hdus

    @staticmethod
    def _get_designed_object(data: dict):
        """ Return a valid fits HDUList

        Parses and validates the hdus YAML cache into a proper Pydantic model
        and converts the model into an HDUList

        Parameters
        ----------
        data : dict
            The hdus cache

        Returns
        -------
        fits.HDUList
            A valid astropy fits.HDUList object
        """
        return fits.HDUList([HDU.parse_obj(v).convert_hdu() for v in data.values()])

    def write_design(self, file: str, overwrite: bool = True) -> None:
        """ Write out the designed file

        Write out a designed fits.HDUList object to a file on disk.  Must have run
        create_from_cache method first.

        Parameters
        ----------
        file : str
            The designed filename
        overwrite : bool, optional
            If True, overwrites any existing file, by default True

        Raises
        ------
        AttributeError
            when the designed object does not exit
        """
        if not self._designed_object:
            raise AttributeError('Cannot write.  Designed object does not exist.')

        self._designed_object.writeto(file, overwrite=overwrite, checksum=True)

    @staticmethod
    def _is_header_keyword(key: str = None) -> bool:
        """Test for hdu header keyword

        Returns
        -------
        bool
            ``True`` if `key` does *not* contain 'TFORM' or 'TTYPE'.
        """
        return tuple(key.find(f) for f in ("TFORM", "TTYPE")) == (-1, -1)

    @staticmethod
    def _format_type(value: str = None) -> str:
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
        fmap = {"A": "char", "I": "int16", "J": "int32", "K": "int64", "E": "float32",
                "D": "float64", "B": "bool", "L": "bool"}
        out = [
            val if value.isalpha() else "{0}[{1}]".format(val, value[:-1])
            for key, val in fmap.items()
            if key in value
        ]
        return out[0]

