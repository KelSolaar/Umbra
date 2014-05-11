#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**testsruntime_globals.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines units tests for :mod:`umbra.globals.runtime_globals` module.

**Others:**

"""

from __future__ import unicode_literals

import os
import sys
if sys.version_info[:2] <= (2, 6):
	import unittest2 as unittest
else:
	import unittest

from umbra.globals.runtime_globals import RuntimeGlobals

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["TestRuntimeGlobals"]

class TestRuntimeGlobals(unittest.TestCase):
	"""
	Defines :class:`umbra.globals.runtime_globals.RuntimeGlobals` class units tests methods.
	"""

	def test_required_attributes(self):
		"""
		Tests presence of required attributes.
		"""

		required_attributes = ("parameters",
							"arguments",
							"logging_console_handler",
							"logging_file_handler",
							"logging_session_handler",
							"logging_session_handler_stream",
							"logging_formatters",
							"logging_active_formatter",
							"verbosity_level",
							"logging_file",
							"requests_stack",
							"engine",
							"patches_manager",
							"components_manager",
							"actions_manager",
							"file_system_events_manager",
							"notifications_manager",
							"layouts_manager",
							"reporter",
							"application",
							"user_application_data_directory",
							"resources_directories",
							"ui_file",
							"patches_file",
							"settings_file",
							"settings",
							"last_browsed_path",
							"splashscreen_image",
							"splashscreen")

		for attribute in required_attributes:
			self.assertIn(attribute, RuntimeGlobals.__dict__)

	def test_resources_paths_attribute(self):
		"""
		Tests :attr:`umbra.globals.runtime_globals.RuntimeGlobals.resources_directories` attribute.
		"""

		self.assertIsInstance(RuntimeGlobals.resources_directories, list)

	def test_last_browsed_path(self):
		"""
		Tests :attr:`umbra.globals.runtime_globals.RuntimeGlobals.last_browsed_path` attribute.
		"""

		self.assertTrue(os.path.exists(RuntimeGlobals.last_browsed_path))

if __name__ == "__main__":
	unittest.main()
