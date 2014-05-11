#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**launcher.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Runs the **Umbra** package :class:`umbra.engine.Umbra` engine class.

**Others:**

"""

from __future__ import unicode_literals

import os
import sys


def _set_package_directory():
    """
    Sets the Application package directory in the path.
    """

    package_directory = os.path.normpath(os.path.join(os.path.dirname(__file__), "../"))
    package_directory not in sys.path and sys.path.append(package_directory)


_set_package_directory()

import umbra.engine
from umbra.globals.constants import Constants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = []


def main():
    """
    Starts the Application.

    :return: Definition success.
    :rtype: bool
    """

    components_paths = []
    for path in (os.path.join(umbra.__path__[0], Constants.factory_components_directory),
                 os.path.join(umbra.__path__[0], Constants.factory_addons_components_directory)):
        os.path.exists(path) and components_paths.append(path)
    return umbra.engine.run(umbra.engine.Umbra,
                            umbra.engine.get_command_line_parameters_parser().parse_args(
                                [unicode(argument, Constants.default_codec, Constants.codec_error) for argument in
                                 sys.argv]),
                            components_paths,
                            ("factory.script_editor", "factory.preferences_manager", "factory.components_manager_ui"))


if __name__ == "__main__":
    main()
