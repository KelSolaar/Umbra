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

	application_name = "Umbra"
	"""
	:param application_name: Package Application name.
	:type application_name: unicode
	"""
	major_version = "1"
	"""
	:param major_version: Package major version.
	:type major_version: unicode
	"""
	minor_version = "0"
	"""
	:param minor_version: Package minor version.
	:type minor_version: unicode
	"""
	change_version = "9"
	"""
	:param change_version: Package change version.
	:type change_version: unicode
	"""
	version = ".".join((major_version, minor_version, change_version))
	"""
	:param version: Package version.
	:type version: unicode
	"""

	logger = "Umbra_Logger"
	"""
	:param logger: Package logger name.
	:type logger: unicode
	"""
	verbosity_level = 3
	"""
	:param verbosity_level: Default logging verbosity level.
	:type verbosity_level: int
	"""
	verbosity_labels = ("Critical", "Error", "Warning", "Info", "Debug")
	"""
	:param verbosity_labels: Logging verbosity labels.
	:type verbosity_labels: tuple
	"""
	logging_default_formatter = "Default"
	"""
	:param logging_default_formatter: Default logging formatter name.
	:type logging_default_formatter: unicode
	"""
	logging_separators = "*" * 96
	"""
	:param logging_separators: Logging separators.
	:type logging_separators: unicode
	"""

	default_codec = umbra.DEFAULT_CODEC
	"""
	:param default_codec: Default codec.
	:type default_codec: unicode
	"""
	codec_error = umbra.CODEC_ERROR
	"""
	:param codec_error: Default codec error behavior.
	:type codec_error: unicode
	"""

	application_directory = os.sep.join(("Umbra", ".".join((major_version, minor_version))))
	"""
	:param application_directory: Package Application directory.
	:type application_directory: unicode
	"""
	if platform.system() in ("Windows", "Microsoft") or platform.system() == "Darwin":
		provider_directory = "HDRLabs"
		"""
		:param provider_directory: Package provider directory.
		:type provider_directory: unicode
		"""
	elif platform.system() == "Linux":
		provider_directory = ".HDRLabs"
		"""
		:param provider_directory: Package provider directory.
		:type provider_directory: unicode
		"""

	patches_directory = "patches"
	"""
	:param patches_directory: Application patches directory.
	:type patches_directory: unicode
	"""
	settings_directory = "settings"
	"""
	:param settings_directory: Application settings directory.
	:type settings_directory: unicode
	"""
	user_components_directory = "components"
	"""
	:param user_components_directory: Application user components directory.
	:type user_components_directory: unicode
	"""
	logging_directory = "logging"
	"""
	:param logging_directory: Application logging directory.
	:type logging_directory: unicode
	"""
	io_directory = "io"
	"""
	:param io_directory: Application io directory.
	:type io_directory: unicode
	"""

	preferences_directories = (patches_directory,
								settings_directory,
								user_components_directory,
								logging_directory,
								io_directory)
	"""
	:param preferences_directories: Application preferences directories.
	:type preferences_directories: tuple
	"""

	factory_components_directory = "components/factory"
	"""
	:param factory_components_directory: Application factory components directory.
	:type factory_components_directory: unicode
	"""

	factory_addons_components_directory = "components/addons"
	"""
	:param factory_addons_components_directory: Application addons components directory.
	:type factory_addons_components_directory: unicode
	"""

	resources_directory = "resources"
	"""
	:param resources_directory: Application resources directory.
	:type resources_directory: unicode
	"""

	patches_file = "Umbra_Patches.rc"
	"""
	:param patches_file: Application settings file.
	:type patches_file: unicode
	"""
	settings_file = "Umbra_Settings.rc"
	"""
	:param settings_file: Application settings file.
	:type settings_file: unicode
	"""
	logging_file = "Umbra_Logging_{0}.log"
	"""
	:param logging_file: Application logging file.
	:type logging_file: unicode
	"""

	libraries_directory = "libraries"
	"""
	:param libraries_directory: Application libraries directory.
	:type libraries_directory: unicode
	"""

	default_timer_cycle = 125
	"""
	:param default_timer_cycle: Default timer cycle length in milliseconds.
	:type default_timer_cycle: int
	"""
	null_object = "None"
	"""
	:param null_object: Default null object string.
	:type null_object: unicode
	"""
