#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**constants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **Umbra** package default constants through the :class:`Constants` class.

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
import platform

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import umbra

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["Constants"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Constants():
	"""
	Defines **Umbra** package default constants.
	"""

	applicationName = "Umbra"
	"""
	:param applicationName: Package Application name.
	:type applicationName: unicode
	"""
	majorVersion = "1"
	"""
	:param majorVersion: Package major version.
	:type majorVersion: unicode
	"""
	minorVersion = "0"
	"""
	:param minorVersion: Package minor version.
	:type minorVersion: unicode
	"""
	changeVersion = "9"
	"""
	:param changeVersion: Package change version.
	:type changeVersion: unicode
	"""
	version = ".".join((majorVersion, minorVersion, changeVersion))
	"""
	:param version: Package version.
	:type version: unicode
	"""

	logger = "Umbra_Logger"
	"""
	:param logger: Package logger name.
	:type logger: unicode
	"""
	verbosityLevel = 3
	"""
	:param verbosityLevel: Default logging verbosity level.
	:type verbosityLevel: int
	"""
	verbosityLabels = ("Critical", "Error", "Warning", "Info", "Debug")
	"""
	:param verbosityLabels: Logging verbosity labels.
	:type verbosityLabels: tuple
	"""
	loggingDefaultFormatter = "Default"
	"""
	:param loggingDefaultFormatter: Default logging formatter name.
	:type loggingDefaultFormatter: unicode
	"""
	loggingSeparators = "*" * 96
	"""
	:param loggingSeparators: Logging separators.
	:type loggingSeparators: unicode
	"""

	defaultCodec = umbra.DEFAULT_CODEC
	"""
	:param defaultCodec: Default codec.
	:type defaultCodec: unicode
	"""
	codecError = umbra.CODEC_ERROR
	"""
	:param codecError: Default codec error behavior.
	:type codecError: unicode
	"""

	applicationDirectory = os.sep.join(("Umbra", ".".join((majorVersion, minorVersion))))
	"""
	:param applicationDirectory: Package Application directory.
	:type applicationDirectory: unicode
	"""
	if platform.system() in ("Windows", "Microsoft") or platform.system() == "Darwin":
		providerDirectory = "HDRLabs"
		"""
		:param providerDirectory: Package provider directory.
		:type providerDirectory: unicode
		"""
	elif platform.system() == "Linux":
		providerDirectory = ".HDRLabs"
		"""
		:param providerDirectory: Package provider directory.
		:type providerDirectory: unicode
		"""

	patchesDirectory = "patches"
	"""
	:param patchesDirectory: Application patches directory.
	:type patchesDirectory: unicode
	"""
	settingsDirectory = "settings"
	"""
	:param settingsDirectory: Application settings directory.
	:type settingsDirectory: unicode
	"""
	userComponentsDirectory = "components"
	"""
	:param userComponentsDirectory: Application user components directory.
	:type userComponentsDirectory: unicode
	"""
	loggingDirectory = "logging"
	"""
	:param loggingDirectory: Application logging directory.
	:type loggingDirectory: unicode
	"""
	ioDirectory = "io"
	"""
	:param ioDirectory: Application io directory.
	:type ioDirectory: unicode
	"""

	preferencesDirectories = (patchesDirectory,
								settingsDirectory,
								userComponentsDirectory,
								loggingDirectory,
								ioDirectory)
	"""
	:param preferencesDirectories: Application preferences directories.
	:type preferencesDirectories: tuple
	"""

	factoryComponentsDirectory = "components/factory"
	"""
	:param factoryComponentsDirectory: Application factory components directory.
	:type factoryComponentsDirectory: unicode
	"""

	factoryAddonsComponentsDirectory = "components/addons"
	"""
	:param factoryAddonsComponentsDirectory: Application addons components directory.
	:type factoryAddonsComponentsDirectory: unicode
	"""

	resourcesDirectory = "resources"
	"""
	:param resourcesDirectory: Application resources directory.
	:type resourcesDirectory: unicode
	"""

	patchesFile = "Umbra_Patches.rc"
	"""
	:param patchesFile: Application settings file.
	:type patchesFile: unicode
	"""
	settingsFile = "Umbra_Settings.rc"
	"""
	:param settingsFile: Application settings file.
	:type settingsFile: unicode
	"""
	loggingFile = "Umbra_Logging_{0}.log"
	"""
	:param loggingFile: Application logging file.
	:type loggingFile: unicode
	"""

	librariesDirectory = "libraries"
	"""
	:param librariesDirectory: Application libraries directory.
	:type librariesDirectory: unicode
	"""

	defaultTimerCycle = 125
	"""
	:param defaultTimerCycle: Default timer cycle length in milliseconds.
	:type defaultTimerCycle: int
	"""
	nullObject = "None"
	"""
	:param nullObject: Default null object string.
	:type nullObject: unicode
	"""
