#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**RuntimeGlobals.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Umbra** package runtime globals through the :class:`RuntimeGlobals` class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
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
	This class provides **Umbra** package runtime constants.
	"""

	parameters = None
	"""Application startup parameters."""
	arguments = None
	"""Application startup arguments."""

	loggingConsoleHandler = None
	"""Logging console handler instance."""
	loggingFileHandler = None
	"""Logging file handler instance."""
	loggingSessionHandler = None
	"""Logging session handler instance."""
	loggingSessionHandlerStream = None
	"""Logging session handler stream."""
	loggingFormatters = None
	"""Logging formatters."""
	loggingActiveFormatter = None
	"""Logging current formatter."""

	verbosityLevel = None
	"""Logging current verbosity level."""
	loggingFile = None
	"""Application logging file."""

	requestsStack = None
	"""Application requests stack."""

	engine = None
	"""Application engine instance."""

	patchesManager = None
	"""Application patches manager instance."""
	componentsManager = None
	"""Application components manager instance."""
	actionsManager = None
	"""Application actions manager instance."""
	fileSystemEventsManager = None
	"""Application file system events manager instance."""
	notificationsManager = None
	"""Application notifications manager instance."""
	layoutsManager = None
	"""Application layouts manager instance."""

	application = None
	"""Application instance."""
	userApplicationDataDirectory = None
	"""Application user data directory."""

	resourcesDirectories = []
	"""Resources paths."""

	uiFile = None
	"""Application ui file."""

	patchesFile = None
	"""Application patches file."""

	settingsFile = None
	"""Application settings file."""
	settings = None
	"""Application settings instance."""

	lastBrowsedPath = os.getcwd()
	"""Last browsed path."""

	splashscreenImage = None
	"""Application splashscreen picture."""
	splashscreen = None
	"""Application splashscreen instance."""
