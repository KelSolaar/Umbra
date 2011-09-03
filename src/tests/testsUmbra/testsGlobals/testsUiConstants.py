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

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import re
import unittest

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
from umbra.globals.uiConstants import UiConstants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class UiConstantsTestCase(unittest.TestCase):
	"""
	This class defines :class:`umbra.globals.uiConstants.UiConstants` class units tests methods.
	"""

	def testRequiredAttributes(self):
		"""
		This method tests presence of required attributes.
		"""

		requiredAttributes = ("uiFile",
								"windowsStylesheetFile",
								"darwinStylesheetFile",
								"linuxStylesheetFile",
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
								"layoutIcon",
								"layoutHoverIcon",
								"layoutActiveIcon",
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
								"restoreGeometryOnLayoutChange",
								"pythonTokensFile")

		for attribute in requiredAttributes:
			self.assertIn(attribute, UiConstants.__dict__)

	def testUiFileAttribute(self):
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
		self.assertRegexpMatches(UiConstants.splashScreenImage, "\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

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

	def testLayoutIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.layoutIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.layoutIcon, "\w+")

	def testLayoutHoverIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.layoutHoverIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.layoutHoverIcon, "\w+")

	def testLayoutActiveIconAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.layoutActiveIcon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.layoutActiveIcon, "\w+")

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

	def testRestoreGeometryOnLayoutChangeAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.restoreGeometryOnLayoutChange` attribute.
		"""

		self.assertIsInstance(UiConstants.restoreGeometryOnLayoutChange, bool)

	def testPythonTokensFileAttribute(self):
		"""
		This method tests :attr:`umbra.globals.uiConstants.UiConstants.pythonTokensFile` attribute.
		"""

		self.assertRegexpMatches(UiConstants.pythonTokensFile, "\w+")

if __name__ == "__main__":
	unittest.main()
