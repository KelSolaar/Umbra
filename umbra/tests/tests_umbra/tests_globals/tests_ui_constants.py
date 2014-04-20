#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsui_constants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`umbra.globals.ui_constants` module.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

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
from umbra.globals.ui_constants import UiConstants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Defines :class:`umbra.globals.ui_constants.UiConstants` class units tests methods.
	"""

	def test_required_attributes(self):
		"""
		Tests presence of required attributes.
		"""

		required_attributes = ("ui_file",
								"processing_ui_file",
								"reporter_ui_file",
								"windows_stylesheet_file",
								"darwin_stylesheet_file",
								"linux_stylesheet_file",
								"windows_full_screen_stylesheet_file",
								"darwin_full_screen_stylesheet_file",
								"linux_full_screen_stylesheet_file",
								"windows_style",
								"darwin_style",
								"linux_style",
								"settings_file",
								"layouts_file",
								"application_windows_icon",
								"splash_screen_image",
								"logo_image",
								"default_toolbar_icon_size",
								"custom_layouts_icon",
								"custom_layouts_hover_icon",
								"custom_layouts_active_icon",
								"miscellaneous_icon",
								"miscellaneous_hover_icon",
								"miscellaneous_active_icon",
								"development_icon",
								"development_hover_icon",
								"development_active_icon",
								"preferences_icon",
								"preferences_hover_icon",
								"preferences_active_icon",
								"startup_layout",
								"help_file",
								"api_file",
								"development_layout",
								"python_grammar_file",
								"logging_grammar_file",
								"text_grammar_file",
								"invalid_link_html_file",
								"crittercism_id")

		for attribute in required_attributes:
			self.assertIn(attribute, UiConstants.__dict__)

	def test_ui_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.ui_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.ui_file, "\w+")

	def test_processing_ui_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.processing_ui_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.processing_ui_file, "\w+")

	def test_reporter_ui_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.reporter_ui_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.reporter_ui_file, "\w+")

	def test_windows_stylesheet_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.windows_stylesheet_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.windows_stylesheet_file, "\w+")

	def test_darwin_stylesheet_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.darwin_stylesheet_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.darwin_stylesheet_file, "\w+")

	def test_linux_stylesheet_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.linux_stylesheet_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.linux_stylesheet_file, "\w+")

	def test_windows_full_screen_stylesheet_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.windows_full_screen_stylesheet_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.windows_full_screen_stylesheet_file, "\w+")

	def test_darwin_full_screen_stylesheet_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.darwin_full_screen_stylesheet_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.darwin_full_screen_stylesheet_file, "\w+")

	def test_linux_full_screen_stylesheet_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.linux_full_screen_stylesheet_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.linux_full_screen_stylesheet_file, "\w+")

	def test_windows_style_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.windows_style` attribute.
		"""

		self.assertRegexpMatches(UiConstants.windows_style, "\w+")

	def test_darwin_style_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.darwin_style` attribute.
		"""

		self.assertRegexpMatches(UiConstants.darwin_style, "\w+")

	def test_linux_style_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.linux_style` attribute.
		"""

		self.assertRegexpMatches(UiConstants.linux_style, "\w+")

	def test_settings_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.settings_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.settings_file, "\w+")

	def test_layouts_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.layouts_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.layouts_file, "\w+")

	def test_application_windows_icon_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.application_windows_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.application_windows_icon, "\w+")
		self.assertRegexpMatches(UiConstants.application_windows_icon, "\.[pP][nN][gG]$")

	def test_splashscreem_image_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.splash_screen_image` attribute.
		"""

		self.assertRegexpMatches(UiConstants.splash_screen_image, "\w+")
		self.assertRegexpMatches(UiConstants.splash_screen_image,
								"\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def test_logo_image_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.logo_image` attribute.
		"""

		self.assertRegexpMatches(UiConstants.logo_image, "\w+")
		self.assertRegexpMatches(UiConstants.logo_image, "\.[bB][mM][pP]$|\.[jJ][pP][eE][gG]$|\.[jJ][pP][gG]|\.[pP][nN][gG]$")

	def test_default_toolbar_icon_size_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.default_toolbar_icon_size` attribute.
		"""

		self.assertIsInstance(UiConstants.default_toolbar_icon_size, int)
		self.assertGreaterEqual(UiConstants.default_toolbar_icon_size, 8)
		self.assertLessEqual(UiConstants.default_toolbar_icon_size, 128)

	def test_custom_layouts_icon_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.custom_layouts_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.custom_layouts_icon, "\w+")

	def test_custom_layouts_hover_icon_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.custom_layouts_hover_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.custom_layouts_hover_icon, "\w+")

	def test_custom_layouts_active_icon_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.custom_layouts_active_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.custom_layouts_active_icon, "\w+")

	def test_miscellaneous_icon_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.miscellaneous_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.miscellaneous_icon, "\w+")

	def test_miscellaneous_hover_icon_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.miscellaneous_hover_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.miscellaneous_hover_icon, "\w+")

	def test_miscellaneous_active_icon_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.miscellaneous_active_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.miscellaneous_active_icon, "\w+")

	def test_development_icon_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.development_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.development_icon, "\w+")

	def test_development_hover_icon_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.development_hover_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.development_hover_icon, "\w+")

	def test_development_active_icon_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.development_active_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.development_active_icon, "\w+")

	def test_preferences_icon_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.preferences_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.preferences_icon, "\w+")

	def test_preferences_hover_icon_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.preferences_hover_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.preferences_hover_icon, "\w+")

	def test_preferences_active_icon_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.preferences_active_icon` attribute.
		"""

		self.assertRegexpMatches(UiConstants.preferences_active_icon, "\w+")

	def test_startup_layout_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.startup_layout` attribute.
		"""

		self.assertRegexpMatches(UiConstants.startup_layout, "\w+")

	def test_help_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.help_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.help_file, "(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?")

	def test_api_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.api_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.api_file, "(http|ftp|https)://([a-zA-Z0-9\-\.]+)/?")

	def test_development_layout_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.development_layout` attribute.
		"""

		self.assertRegexpMatches(UiConstants.development_layout, "\w+")

	def test_python_grammar_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.python_grammar_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.python_grammar_file, "\w+")


	def test_logging_grammar_file_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.logging_grammar_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.logging_grammar_file, "\w+")

	def test_text_grammar_file_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.text_grammar_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.text_grammar_file, "\w+")

	def test_invalid_link_html_file_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.invalid_link_html_file` attribute.
		"""

		self.assertRegexpMatches(UiConstants.invalid_link_html_file, "\w+")

	def test_crittercism_id_attribute(self):
		"""
		Tests :attr:`umbra.globals.ui_constants.UiConstants.crittercism_id` attribute.
		"""

		self.assertRegexpMatches(UiConstants.crittercism_id, "\w+")
		self.assertEqual(UiConstants.crittercism_id, "51290b63421c983d17000490")

if __name__ == "__main__":
	unittest.main()
