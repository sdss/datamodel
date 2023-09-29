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

from pydantic import BaseModel, ConfigDict
from typing import Iterator, Union, Callable, Dict, Any, Type


def add_repr(schema: Dict[str, Any], model: Type[BaseModel]) -> None:
    """ Adds custom  information into the schema """
    # "repr" flag in Field not retained when dumping model schema
    # this adds the "repr" boolean Field into the schema for each
    # property on a model.  Use until this is fixed in the core Pydantic.
    for key, mod in model.__fields__.items():
        if mod.field_info.repr is False:
            schema['properties'][key].update({'repr': False})


class CoreModel(BaseModel):
    """ Custom BaseModel """
    # TODO[pydantic]: We couldn't refactor this class, please create the `model_config` manually.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    # class Config:
    #     """ base model config """
    #     @staticmethod
    #     def schema_extra(schema: Dict[str, Any], model: Type[BaseModel]) -> None:
    #         """ Adds custom information into the schema """

    #         # "repr" flag in Field not retained when dumping model schema
    #         # this adds the "repr" boolean Field into the schema for each
    #         # property on a model.  Use until this is fixed in the core Pydantic.
    #         for key, mod in model.__fields__.items():
    #             if mod.field_info.repr is False:
    #                 schema['properties'][key].update({'repr': False})
    model_config = ConfigDict(json_schema_extra=add_repr)

    def __repr_args__(self):
        """ Custom repr args

        By default, for model fields that are complex objects, pydantic
        displays the entire object in the repr.  This allows specifying
        an object attribute to be used for display in the repr instead,
        using an extra "repr_attr" field, with the name of the attribute.
        See models Survey and Phase for example.
        """
        rargs = []
        # loop over model's repr args
        for i in super().__repr_args__():
            # get the field_info "extra" and look for the "repr_attr" key
            ext = self.__fields__[i[0]].field_info.extra
            if 'repr_attr' in ext:
                # use the object attribute specified as the repr arg
                if isinstance(i[1], list):
                    attr = [getattr(e, ext['repr_attr']) for e in i[1]]
                else:
                    attr = getattr(i[1], ext['repr_attr'])
                rargs.append((i[0], attr))
            else:
                rargs.append(i)
        return rargs


class BaseList(BaseModel):
    """ Base pydantic class for lists of models """

    def __iter__(self) -> Iterator:
        return iter(self.__root__)

    def __contains__(self, value) -> bool:
        """ Uses the model name to check list inclusion """
        if isinstance(value, str):
            return value.lower() in [i.name.lower() for i in self]
        return value in self.__root__

    def __getitem__(self, item: Union[str, int]) -> BaseModel:
        """ Allows item access by index or model name """
        if isinstance(item, str) and item in self:
            vals = [i.name.lower() for i in self.__root__]
            return self.__root__[vals.index(item.lower())]
        elif isinstance(item, BaseModel):
            return self[self.__root__.index(item)]
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
            key = lambda x: getattr(x, field)
        vals = sorted(self.__root__.copy(), key=key, **kwargs)
        self.__root__ = vals

    def list_names(self):
        """ Create a simplified list of name attributes """
        return [item.name for item in self.__root__]
