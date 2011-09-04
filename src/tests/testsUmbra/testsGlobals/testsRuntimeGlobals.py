#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsRuntimeGlobals.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`umbra.globals.runtimeGlobals` module.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
from umbra.globals.runtimeGlobals import RuntimeGlobals

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RuntimeGlobalsTestCase"]

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class RuntimeGlobalsTestCase(unittest.TestCase):
	"""
	This class defines :class:`umbra.globals.runtimeGlobals.RuntimeGlobals` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("parameters",
								"arguments",
								"loggingConsoleHandler",
								"loggingFileHandler",
								"loggingSessionHandler",
								"loggingSessionHandlerStream",
								"loggingFormatters",
								"loggingActiveFormatter",
								"verbosityLevel",
								"loggingFile",
								"application",
								"userApplicationDatasDirectory",
								"resourcesPaths",
								"uiFile",
								"ui",
								"settingsFile",
								"settings",
								"splashscreenImage",
								"splashscreen")

		for attribute in requiredAttributes:
			self.assertIn(attribute, RuntimeGlobals.__dict__)

	def testResourcesPathsAttribute(self):
		"""
		This method tests :attr:`umbra.globals.runtimeGlobals.RuntimeGlobals.resourcesPaths` attribute.
		"""

		self.assertIsInstance(RuntimeGlobals.resourcesPaths, list)

if __name__ == "__main__":
	unittest.main()
