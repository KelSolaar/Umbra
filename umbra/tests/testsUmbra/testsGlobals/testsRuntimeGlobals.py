#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsRuntimeGlobals.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`umbra.globals.runtimeGlobals` module.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RuntimeGlobalsTestCase"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class RuntimeGlobalsTestCase(unittest.TestCase):
	"""
	Defines :class:`umbra.globals.runtimeGlobals.RuntimeGlobals` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		Tests presence of required attributes.
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
							"requestsStack",
							"engine",
							"patchesManager",
							"componentsManager",
							"actionsManager",
							"fileSystemEventsManager",
							"notificationsManager",
							"layoutsManager",
							"reporter",
							"application",
							"userApplicationDataDirectory",
							"resourcesDirectories",
							"uiFile",
							"patchesFile",
							"settingsFile",
							"settings",
							"lastBrowsedPath",
							"splashscreenImage",
							"splashscreen")

		for attribute in requiredAttributes:
			self.assertIn(attribute, RuntimeGlobals.__dict__)

	def testResourcesPathsAttribute(self):
		"""
		Tests :attr:`umbra.globals.runtimeGlobals.RuntimeGlobals.resourcesDirectories` attribute.
		"""

		self.assertIsInstance(RuntimeGlobals.resourcesDirectories, list)

	def testLastBrowsedPath(self):
		"""
		Tests :attr:`umbra.globals.runtimeGlobals.RuntimeGlobals.lastBrowsedPath` attribute.
		"""

		self.assertTrue(os.path.exists(RuntimeGlobals.lastBrowsedPath))

if __name__ == "__main__":
	unittest.main()
