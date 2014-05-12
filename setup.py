#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**setup.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    `https://pypi.python.org/pypi/Umbra <https://pypi.python.org/pypi/Umbra>`_ package setup file.

**Others:**

"""

from __future__ import unicode_literals

import re
from setuptools import setup
from setuptools import find_packages

import umbra.globals.constants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["get_long_description"]


def get_long_description():
    """
    Returns the Package long description.

    :return: Package long description.
    :rtype: unicode
    """

    description = []
    with open("README.rst") as file:
        for line in file:
            if ".. code:: python" in line and len(description) >= 2:
                blockLine = description[-2]
                if re.search(r":$", blockLine) and not re.search(r"::$", blockLine):
                    description[-2] = "::".join(blockLine.rsplit(":", 1))
                continue

            description.append(line)
    return "".join(description)


setup(name=umbra.globals.constants.Constants.application_name,
      version=umbra.globals.constants.Constants.version,
      author=umbra.globals.constants.__author__,
      author_email=umbra.globals.constants.__email__,
      include_package_data=True,
      packages=find_packages(),
      scripts=["bin/Umbra"],
      url="https://github.com/KelSolaar/Umbra",
      license="GPLv3",
      description="Umbra is the main package of sIBL_GUI and sIBL_Reporter.",
      long_description=get_long_description(),
      install_requires=["Manager>=2.0.5"],
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Environment :: Console",
                   "Environment :: MacOS X",
                   "Environment :: Win32 (MS Windows)",
                   "Environment :: X11 Applications :: Qt",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2.7",
                   "Topic :: Utilities"])
