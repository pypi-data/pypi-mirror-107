# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Contracts for environment override."""
import os
from ._util._exceptions import UserErrorException


class Docker:
    """Docker environment settings for running a component."""
    def __init__(self, image: str=None, file: str=None):
        """
        Create docker settings from image or a dockerfile.

        :param image: docker image
        :type image: str
        :param file: the path to dockerfile
        :type file: str
        """
        self._image = None
        self._file = None
        if image:
            self.image = image
        elif file:
            self.file = file

    @property
    def image(self):
        """The image in current docker settings."""
        return self._image

    @image.setter
    def image(self, value):
        _check_str_value('image', value)
        self._image = value

    @property
    def file(self):
        """The dockerfile path in current docker settings."""
        return self._file

    @file.setter
    def file(self, value):
        _check_file_value('file', value)
        self._file = value


class Conda:
    """Conda environment settings for running a component."""
    def __init__(self, pip_requirement_file: str=None, conda_file: str=None):
        """
        Create conda settings from  a pip requirement file or a conda yaml file.

        :param pip_requirement_file: the path to pip requirement file
        :type pip_requirement_file: str
        :param conda_file: the path to conda yaml file
        :type conda_file: str
        """
        self._pip_requirement_file = None
        self._conda_file = None
        if pip_requirement_file:
            self.pip_requirement_file = pip_requirement_file
        elif conda_file:
            self.conda_file = conda_file

    @property
    def pip_requirement_file(self):
        """The pip requirement file path in current conda settings."""
        return self._pip_requirement_file

    @pip_requirement_file.setter
    def pip_requirement_file(self, value):
        _check_file_value('pip_requirement_file', value)
        self._pip_requirement_file = value

    @property
    def conda_file(self):
        """The conda yaml file path in current conda settings."""
        return self._conda_file

    @conda_file.setter
    def conda_file(self, value):
        _check_file_value('conda_file', value)
        self._conda_file = value


def _check_str_value(param_name, value):
    _check_value_type(param_name, value, str)


def _check_file_value(param_name, value):
    _check_value_type(param_name, value, str)
    if not os.path.exists(value):
        raise UserErrorException("File path '{}' does not exist.".format(value))


def _check_value_type(param_name, value, expected_type):
    if not isinstance(value, expected_type):
        raise UserErrorException(
            "Parameter '{}' type mismatched, expected type: '{}', got '{}'.".format(
                param_name, expected_type.__name__, type(value).__name__))
