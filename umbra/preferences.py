#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**preferences.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`Preferences` class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import QVariant

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import umbra.ui.common
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

__all__ = ["LOGGER", "Preferences"]

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Preferences(object):
	"""
	| Defines methods to manipulate Application preferences / settings.
	| Those are stored and retrieved using a `QSettings <http://doc.qt.nokia.com/qsettings.html>`_ class.
	"""

	def __init__(self, file=None):
		"""
		Initializes the class.

		:param file: Current preferences file path.
		:type file: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__file = None
		self.file = file

		self.__settings = QSettings(self.__file, QSettings.IniFormat) if self.__file is not None else QSettings()

		self.__default_settings = None
		self.__default_layouts_settings = None

		# --- Initializing preferences. ---
		self.__get_default_settings()
		self.__get_default_layouts_settings()

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def file(self):
		"""
		Property for **self.__file** attribute.

		:return: self.__file.
		:rtype: unicode
		"""

		return self.__file

	@file.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def file(self, value):
		"""
		Setter for **self.__file** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"file", value)
		self.__file = value

	@file.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def file(self):
		"""
		Deleter for **self.__file** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "file"))

	@property
	def settings(self):
		"""
		Property for **self.__settings** attribute.

		:return: self.__settings.
		:rtype: QSettings
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		Setter for **self.__settings** attribute.

		:param value: Attribute value.
		:type value: QSettings
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		Deleter for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def default_settings(self):
		"""
		Property for **self.__default_settings** attribute.

		:return: self.__default_settings.
		:rtype: QSettings
		"""

		return self.__default_settings

	@default_settings.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_settings(self, value):
		"""
		Setter for **self.__default_settings** attribute.

		:param value: Attribute value.
		:type value: QSettings
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "default_settings"))

	@default_settings.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_settings(self):
		"""
		Deleter for **self.__default_settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_settings"))

	@property
	def default_layouts_settings(self):
		"""
		Property for **self.__default_layouts_settings** attribute.

		:return: self.__default_layouts_settings.
		:rtype: QSettings
		"""

		return self.__default_layouts_settings

	@default_layouts_settings.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_layouts_settings(self, value):
		"""
		Setter for **self.__default_layouts_settings** attribute.

		:param value: Attribute value.
		:type value: QSettings
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "default_layouts_settings"))

	@default_layouts_settings.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_layouts_settings(self):
		"""
		Deleter for **self.__default_layouts_settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_layouts_settings"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def set_key(self, section, key, value):
		"""
		Stores given key in settings file.

		:param section: Current section to save the key into.
		:type section: unicode
		:param key: Current key to save.
		:type key: unicode
		:param value: Current key value to save.
		:type value: object
		"""

		LOGGER.debug("> Saving '{0}' in '{1}' section with value: '{2}' in settings file.".format(
		key, section, foundations.strings.to_string(value)))

		self.__settings.beginGroup(section)
		self.__settings.setValue(key , QVariant(value))
		self.__settings.endGroup()

	def get_key(self, section, key):
		"""
		Gets key value from settings file.

		:param section: Current section to retrieve key from.
		:type section: unicode
		:param key: Current key to retrieve.
		:type key: unicode
		:return: Current key value.
		:rtype: object
		"""

		LOGGER.debug("> Retrieving '{0}' in '{1}' section.".format(key, section))

		self.__settings.beginGroup(section)
		value = self.__settings.value(key)
		LOGGER.debug("> Key value: '{0}'.".format(value))
		self.__settings.endGroup()

		return value

	def key_exists(self, section, key):
		"""
		Checks if given key exists.

		:param section: Current section to check key in.
		:type section: unicode
		:param key: Current key to check.
		:type key: unicode
		:return: Key existence.
		:rtype: bool
		"""

		LOGGER.debug("> Checking '{0}' key existence in '{1}' section.".format(key, section))

		self.__settings.beginGroup(section)
		exists = self.__settings.contains(key)
		self.__settings.endGroup()
		return exists

	def __get_default_settings(self):
		"""
		Gets the default settings.
		"""

		LOGGER.debug("> Accessing '{0}' default settings file!".format(UiConstants.settings_file))
		self.__default_settings = QSettings(umbra.ui.common.get_resource_path(UiConstants.settings_file), QSettings.IniFormat)

	def __get_default_layouts_settings(self):
		"""
		Gets the default layouts settings.
		"""

		LOGGER.debug("> Accessing '{0}' default layouts settings file!".format(UiConstants.layouts_file))
		self.__default_layouts_settings = QSettings(umbra.ui.common.get_resource_path(UiConstants.layouts_file),
												QSettings.IniFormat)

	def set_default_preferences(self):
		"""
		Defines the default settings file content.
		
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing default settings!")

		for key in self.__default_settings.allKeys():
			self.__settings.setValue(key, self.__default_settings.value(key))

		self.set_default_layouts()
		return True

	def set_default_layouts(self, ignored_layouts=None):
		"""
		Sets the default layouts in the preferences file.

		:param ignored_layouts: Ignored layouts.
		:type ignored_layouts: tuple or list
		:return: Method success.
		:rtype: bool
		"""

		for key in self.__default_layouts_settings.allKeys():
			if ignored_layouts:
				if tuple((layout for layout in ignored_layouts if layout in key)):
					continue
			self.__settings.setValue(key, self.__default_layouts_settings.value(key))
		return True
