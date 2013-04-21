#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**constants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Umbra** package default constants through the :class:`Constants` class.

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
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
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
	This class provides **Umbra** package default constants.
	"""

	applicationName = "Umbra"
	"""Package Application name: '**Umbra**' ( String )"""
	majorVersion = "1"
	"""Package major version: '**4**' ( String )"""
	minorVersion = "0"
	"""Package minor version: '**0**' ( String )"""
	changeVersion = "8"
	"""Package change version: '**8**' ( String )"""
	releaseVersion = ".".join((majorVersion, minorVersion, changeVersion))
	"""Package release version: '**1.0.8**' ( String )"""

	logger = "Umbra_Logger"
	"""Package logger name: '**Umbra_Logger**' ( String )"""
	verbosityLevel = 3
	"""Default logging verbosity level: '**3**' ( Integer )"""
	verbosityLabels = ("Critical", "Error", "Warning", "Info", "Debug")
	"""Logging verbosity labels: ('**Critical**', '**Error**', '**Warning**', '**Info**', '**Debug**') ( Tuple )"""
	loggingDefaultFormatter = "Default"
	"""Default logging formatter name: '**Default**' ( String )"""
	loggingSeparators = "*" * 96
	"""Logging separators: '*' * 96 ( String )"""

	encodingCodec = "utf-8"
	"""Default encoding format: '**utf-8**' ( String )"""
	encodingError = "ignore"
	"""Default encoding error behavior: '**ignore**' ( String )"""

	applicationDirectory = os.sep.join(("Umbra", ".".join((majorVersion, minorVersion))))
	"""Package Application directory: '**Umbra**' ( String )"""
	if platform.system() == "Windows" or platform.system() == "Microsoft" or platform.system() == "Darwin":
		providerDirectory = "HDRLabs"
		"""Package provider directory: '**HDRLabs** on Windows / Darwin, **.HDRLabs** on Linux' ( String )"""
	elif platform.system() == "Linux":
		providerDirectory = ".HDRLabs"
		"""Package provider directory: '**HDRLabs** on Windows / Darwin, **.HDRLabs** on Linux' ( String )"""

	patchesDirectory = "patches"
	"""Application patches directory: '**patches**' ( String )"""
	settingsDirectory = "settings"
	"""Application settings directory: '**settings**' ( String )"""
	userComponentsDirectory = "components"
	"""Application user components directory: '**components**' ( String )"""
	loggingDirectory = "logging"
	"""Application logging directory: '**logging**' ( String )"""
	ioDirectory = "io"
	"""Application io directory: '**io**' ( String )"""

	preferencesDirectories = (patchesDirectory,
								settingsDirectory,
								userComponentsDirectory,
								loggingDirectory,
								ioDirectory)
	"""Application preferences directories ( Tuple )"""

	factoryComponentsDirectory = "components/factory"
	"""Application factory components directory: '**components/factory**' ( String )"""

	factoryAddonsComponentsDirectory = "components/addons"
	"""Application addons components directory: '**components/addons**' ( String )"""

	resourcesDirectory = "resources"
	"""Application resources directory: '**resources**' ( String )"""

	patchesFile = "Umbra_Patches.rc"
	"""Application settings file: '**Umbra_Patches.rc**' ( String )"""
	settingsFile = "Umbra_Settings.rc"
	"""Application settings file: '**Umbra_Settings.rc**' ( String )"""
	loggingFile = "Umbra_Logging_{0}.log"
	"""Application logging file: '**Umbra_Logging_{0}.log**' ( String )"""

	librariesDirectory = "libraries"
	"""Application libraries directory: '**libraries**' ( String )"""

	defaultTimerCycle = 125
	"""Default timer cycle length in milliseconds: '**125**' ( Integer )"""
	nullObject = "None"
	"""Default null object string: '**None**' ( String )"""
