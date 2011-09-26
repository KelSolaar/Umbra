#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**Umbra.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module runs the **Umbra** package :class:`umbra.engine.Umbra` engine class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import os
import sys

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import umbra.engine
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = []

#***********************************************************************************************
#***	Launcher.
#***********************************************************************************************
if __name__ == "__main__":
	componentsPaths = []
	for path in (os.path.join(umbra.__path__[0], Constants.factoryComponentsDirectory), os.path.join(os.getcwd(), umbra.__name__, Constants.factoryComponentsDirectory)):
		os.path.exists(path) and componentsPaths.append(path)
	umbra.engine.run(umbra.engine.Umbra, umbra.engine.getCommandLineParametersParser().parse_args(sys.argv), componentsPaths, ("factory.scriptEditor", "factory.preferencesManager", "factory.componentsManagerUi"))
