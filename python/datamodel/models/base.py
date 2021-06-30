# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Filename: base.py
# Project: models
# Author: Brian Cherinka
# Created: Monday, June 28 2021 4:08:00 pm
# License: BSD 3-clause "New" or "Revised" License
# Copyright (c) 2021 Brian Cherinka
# Last Modified: Monday, June 28 2021 4:08:00 pm
# Modified By: Brian Cherinka

from datetime import date
from pydantic import BaseModel
from typing import Iterator, Union, Callable


class BaseList(BaseModel):
    """ Base pydantic class for lists of models """

    def __iter__(self) -> Iterator:
        return iter(self.__root__)

    def __contains__(self, value) -> bool:
        """ Uses the model name to check list inclusion """
        if isinstance(value, str):
            return value in [i.name for i in self]
        return value in self

    def __getitem__(self, item: Union[str, int]) -> BaseModel:
        """ Allows item access by index or model name """
        if isinstance(item, str) and item in self:
            vals = [i.name for i in self.__root__]
            return self.__root__[vals.index(item)]
        return self.__root__[item]

    def __repr__(self) -> str:
        """ Creates a simple repr in a verbose list format """
        val = '\n '.join(repr(i) for i in self)
        return f"[{val}]"

    def __str__(self) -> str:
        """ Stringifies the model names """
        return f"[{', '.join([i.name for i in self])}]"
    
    def __len__(self) -> int:
        """ Returns the length of the list """
        return len(self.__root__)

    def sort(self, field: str, key: Callable = None, **kwargs) -> None:
        """ Sort the list of models by a pydantic field name

        Performs an in-place sort of the Pydantic Models using Python's
        built-in ``sorted()`` method. Sets the newly sorted list to the
        ``__root__`` attribute, to preserve the original BaseList object
        instance.  By default, the input sort ``key`` to the ``sorted`` 
        function is the field attribute on the model.   

        Parameters
        ----------
        field : str
            The Pydantic field name
        key : Callable, optional
            a function to be passed into the sorted() function, by default None
        """
        if not key:
            if field == 'release_date':
                key = lambda x: date.fromisoformat('0001-01-01') if x.release_date == 'unreleased' else x.release_date
            else:
                key = lambda x: getattr(x, field)
        vals = sorted(self.__root__.copy(), key=key, **kwargs)
        self.__root__ = vals
        
    def list_names(self):
        """ Create a simplified list of name attributes """
        return [item.name for item in self.__root__]