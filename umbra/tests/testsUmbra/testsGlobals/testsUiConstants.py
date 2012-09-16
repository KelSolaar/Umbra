#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsUiConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines units tests for :mod:`umbra.globals.uiConstants` module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
from umbra.globals.uiConstants import UiConstants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["UiConstantsTestCase"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class UiConstantsTestCase(unittest.TestCase):
	"""
	This class defines :class:`umbra.globals.uiConstants.UiConstants` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("uiFile",
								"processingUiFile",
								"windowsStylesheetFile",
								"darwinStylesheetFile",
								"linuxStylesheetFile",
								"windowsFullScreenStylesheetFile",
								"darwinFullScreenStylesheetFile",
								"linuxFullScreenStylesheetFile",
								"windowsStyle",
								"darwinStyle",
								"linuxStyle",
								"settingsFile",
								"layoutsFile",
								"applicationWindowsIcon",
								"applicationDarwinIcon",
								"splashScreenImage",
								"logoImage",
								"defaultToolbarIconSize",
								"customLayoutsIcon",
								"customLayoutsHoverIcon",
								"customLayoutsActiveIcon",
								"miscellaneousIcon",
								"miscellaneousHoverIcon",
								"miscellaneousActiveIcon",
								"developmentIcon",
								"developmentHoverIcon",
								"developmentActiveIcon",
								"preferencesIcon",
								"preferencesHoverIcon",
								"preferencesActiveIcon",
								"startupLayout",
								"helpFile",
								"apiFile",
								"developmentLayout",
								"pythonGrammarFile",
								"loggingGrammarFile",
								"textGrammarFile")

		for attribute in requiredAttributes:
			self.assertIn(attribute, UiConstants.__dict__)

	def testUiFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.processingUiFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.processingUiFile, "\w+")

	def testProcessingUiFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.uiFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.uiFile, "\w+")

	def testWindowsStylesheetFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.windowsStylesheetFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.windowsStylesheetFile, "\w+")

	def testDarwinStylesheetFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.darwinStylesheetFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.darwinStylesheetFile, "\w+")

	def testLinuxStylesheetFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.linuxStylesheetFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.linuxStylesheetFile, "\w+")

	def testWindowsFullScreenStylesheetFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.windowsFullScreenStylesheetFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.windowsFullScreenStylesheetFile, "\w+")

	def testDarwinFullScreenStylesheetFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.darwinFullScreenStylesheetFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.darwinFullScreenStylesheetFile, "\w+")

	def testLinuxFullScreenStylesheetFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.linuxFullScreenStylesheetFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.linuxFullScreenStylesheetFile, "\w+")

	def testWindowsStyleAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.windowsStyle` attribute.
		"""

		self.assertRegexpMatches(UiConstants.windowsStyle, "\w+")

	def testDarwinStyleAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.darwinStyle` attribute.
		"""

		self.assertRegexpMatches(UiConstants.darwinStyle, "\w+")

	def testLinuxStyleAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.linuxStyle` attribute.
		"""

		self.assertRegexpMatches(UiConstants.linuxStyle, "\w+")

	def testSettingsFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.settingsFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.settingsFile, "\w+")

	def testLayoutsFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.layoutsFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.layoutsFile, "\w+")

	def testApplicationWindowsIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.applicationWindowsIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.applicationWindowsIcon, "\w+")
		self.assertRegexpMatches(UiConstants.applicationWindowsIcon, "\.[pP][nN][gG]$")

	def testApplicationDarwinIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.applicationDarwinIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.applicationDarwinIcon, "\w+")
		self.assertRegexpMatches(UiConstants.applicationDarwinIcon, "\.[pP][nN][gG]$")

	def testSplashscreemImageAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.splashScreenImage` attribute.
		"""

		self.assertRegexpMatches(UiConstants.splashScreenImage, "\w+")
		self.assertRegexpMatches(UiConstants.splashScreenImage,
								"\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testLogoImageAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.logoImage` attribute.
		"""

		self.assertRegexpMatches(UiConstants.logoImage, "\w+")
		self.assertRegexpMatches(UiConstants.logoImage, "\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def testDefaultToolbarIconSizeAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.defaultToolbarIconSize` attribute.
		"""

		self.assertIsInstance(UiConstants.defaultToolbarIconSize, int)
		self.assertGreaterEqual(UiConstants.defaultToolbarIconSize, 8)
		self.assertLessEqual(UiConstants.defaultToolbarIconSize, 128)

	def testCustomLayoutsIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.customLayoutsIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.customLayoutsIcon, "\w+")

	def testCustomLayoutsHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.customLayoutsHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.customLayoutsHoverIcon, "\w+")

	def testCustomLayoutsActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.customLayoutsActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.customLayoutsActiveIcon, "\w+")

	def testMiscellaneousIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.miscellaneousIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.miscellaneousIcon, "\w+")

	def testMiscellaneousHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.miscellaneousHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.miscellaneousHoverIcon, "\w+")

	def testMiscellaneousActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.miscellaneousActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.miscellaneousActiveIcon, "\w+")

	def testDevelopmentIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.developmentIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.developmentIcon, "\w+")

	def testDevelopmentHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.developmentHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.developmentHoverIcon, "\w+")

	def testDevelopmentActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.developmentActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.developmentActiveIcon, "\w+")

	def testPreferencesIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.preferencesIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.preferencesIcon, "\w+")

	def testPreferencesHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.preferencesHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.preferencesHoverIcon, "\w+")

	def testPreferencesActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.preferencesActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.preferencesActiveIcon, "\w+")

	def testStartupLayoutAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.startupLayout` attribute.
		"""

		self.assertRegexpMatches(UiConstants.startupLayout, "\w+")

	def testHelpFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.helpFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.helpFile, "(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?")

	def testApiFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.apiFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.apiFile, "(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?")

	def testDevelopmentLayoutAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.developmentLayout` attribute.
		"""

		self.assertRegexpMatches(UiConstants.developmentLayout, "\w+")

	def testPythonGrammarFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.pythonGrammarFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.pythonGrammarFile, "\w+")


	def testLoggingGrammarFileFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.loggingGrammarFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.loggingGrammarFile, "\w+")

	def testTextGrammarFileFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.textGrammarFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.textGrammarFile, "\w+")

if __name__ == "__main__":
	unittest.main()
