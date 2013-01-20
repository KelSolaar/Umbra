#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**launcher.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module runs the **Umbra** package :class:`umbra.engine.Umbra` engine class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import sys

#**********************************************************************************************************************
#***	Encoding manipulations.
#**********************************************************************************************************************
def _setEncoding():
	"""
	This definition sets the Application encoding.
	"""

	reload(sys)
	sys.setdefaultencoding("utf-8")

_setEncoding()

#**********************************************************************************************************************
#***	Path manipulations.
#**********************************************************************************************************************
def _setPackageDirectory():
	"""
	This definition sets the Application package directory in the path.
	"""

	packageDirectory = os.path.normpath(os.path.join(os.path.dirname(__file__), "../"))
	packageDirectory not in sys.path and sys.path.append(packageDirectory)

_setPackageDirectory()

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import umbra.engine
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = []

#**********************************************************************************************************************
#***	Launcher.
#**********************************************************************************************************************
def main():
	"""
	This definition starts the Application.

	:return: Definition success. ( Boolean )
	"""

	componentsPaths = []
	for path in (os.path.join(umbra.__path__[0], Constants.factoryComponentsDirectory),
				os.path.join(umbra.__path__[0], Constants.factoryAddonsComponentsDirectory)):
		os.path.exists(path) and componentsPaths.append(path)
	return umbra.engine.run(umbra.engine.Umbra,
							umbra.engine.getCommandLineParametersParser().parse_args(sys.argv),
							componentsPaths,
							("factory.scriptEditor", "factory.preferencesManager", "factory.componentsManagerUi"))

if __name__ == "__main__":
	main()
