#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**runtime_globals.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **Umbra** package runtime globals through the :class:`RuntimeGlobals` class.

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

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["RuntimeGlobals"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class RuntimeGlobals():
	"""
	Defines **Umbra** package runtime constants.
	"""

	parameters = None
	"""Application startup parameters."""
	arguments = None
	"""Application startup arguments."""

	logging_console_handler = None
	"""Logging console handler instance."""
	logging_file_handler = None
	"""Logging file handler instance."""
	logging_session_handler = None
	"""Logging session handler instance."""
	logging_session_handler_stream = None
	"""Logging session handler stream."""
	logging_formatters = None
	"""Logging formatters."""
	logging_active_formatter = None
	"""Logging current formatter."""

	verbosity_level = None
	"""Logging current verbosity level."""
	logging_file = None
	"""Application logging file."""

	requests_stack = None
	"""Application requests stack."""

	engine = None
	"""Application engine instance."""

	patches_manager = None
	"""Application patches manager instance."""
	components_manager = None
	"""Application components manager instance."""
	actions_manager = None
	"""Application actions manager instance."""
	file_system_events_manager = None
	"""Application file system events manager instance."""
	notifications_manager = None
	"""Application notifications manager instance."""
	layouts_manager = None
	"""Application layouts manager instance."""

	reporter = None
	"""Application reporter instance."""

	application = None
	"""Application instance."""
	user_application_data_directory = None
	"""Application user data directory."""

	resources_directories = []
	"""Resources paths."""

	ui_file = None
	"""Application ui file."""

	patches_file = None
	"""Application patches file."""

	settings_file = None
	"""Application settings file."""
	settings = None
	"""Application settings instance."""

	last_browsed_path = os.getcwd()
	"""Last browsed path."""

	splashscreen_image = None
	"""Application splashscreen picture."""
	splashscreen = None
	"""Application splashscreen instance."""
