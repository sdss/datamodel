# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-12-05 12:01:21
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-12-05 12:19:32

from __future__ import print_function, division, absolute_import


class DatamodelError(Exception):
    """A custom core Datamodel exception"""

    def __init__(self, message=None):

        message = 'There has been an error' \
            if not message else message

        super(DatamodelError, self).__init__(message)


class DatamodelNotImplemented(DatamodelError):
    """A custom exception for not yet implemented features."""

    def __init__(self, message=None):

        message = 'This feature is not implemented yet.' \
            if not message else message

        super(DatamodelNotImplemented, self).__init__(message)


class DatamodelAPIError(DatamodelError):
    """A custom exception for API errors"""

    def __init__(self, message=None):
        if not message:
            message = 'Error with Http Response from Datamodel API'
        else:
            message = 'Http response error from Datamodel API. {0}'.format(message)

        super(DatamodelAPIError, self).__init__(message)


class DatamodelApiAuthError(DatamodelAPIError):
    """A custom exception for API authentication errors"""
    pass


class DatamodelMissingDependency(DatamodelError):
    """A custom exception for missing dependencies."""
    pass


class DatamodelWarning(Warning):
    """Base warning for Datamodel."""


class DatamodelUserWarning(UserWarning, DatamodelWarning):
    """The primary warning class."""
    pass


class DatamodelSkippedTestWarning(DatamodelUserWarning):
    """A warning for when a test is skipped."""
    pass


class DatamodelDeprecationWarning(DatamodelUserWarning):
    """A warning for deprecated features."""
    pass
