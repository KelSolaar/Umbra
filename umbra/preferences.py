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
from umbra.globals.uiConstants import UiConstants

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

LOGGER = foundations.verbose.installLogger()

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

		self.__defaultSettings = None
		self.__defaultLayoutsSettings = None

		# --- Initializing preferences. ---
		self.__getDefaultSettings()
		self.__getDefaultLayoutsSettings()

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
	@foundations.exceptions.handleExceptions(AssertionError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		Setter for **self.__settings** attribute.

		:param value: Attribute value.
		:type value: QSettings
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		Deleter for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def defaultSettings(self):
		"""
		Property for **self.__defaultSettings** attribute.

		:return: self.__defaultSettings.
		:rtype: QSettings
		"""

		return self.__defaultSettings

	@defaultSettings.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultSettings(self, value):
		"""
		Setter for **self.__defaultSettings** attribute.

		:param value: Attribute value.
		:type value: QSettings
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultSettings"))

	@defaultSettings.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultSettings(self):
		"""
		Deleter for **self.__defaultSettings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultSettings"))

	@property
	def defaultLayoutsSettings(self):
		"""
		Property for **self.__defaultLayoutsSettings** attribute.

		:return: self.__defaultLayoutsSettings.
		:rtype: QSettings
		"""

		return self.__defaultLayoutsSettings

	@defaultLayoutsSettings.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultLayoutsSettings(self, value):
		"""
		Setter for **self.__defaultLayoutsSettings** attribute.

		:param value: Attribute value.
		:type value: QSettings
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultLayoutsSettings"))

	@defaultLayoutsSettings.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultLayoutsSettings(self):
		"""
		Deleter for **self.__defaultLayoutsSettings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultLayoutsSettings"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def setKey(self, section, key, value):
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
		key, section, foundations.strings.toString(value)))

		self.__settings.beginGroup(section)
		self.__settings.setValue(key , QVariant(value))
		self.__settings.endGroup()

	def getKey(self, section, key):
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

	def keyExists(self, section, key):
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

	def __getDefaultSettings(self):
		"""
		Gets the default settings.
		"""

		LOGGER.debug("> Accessing '{0}' default settings file!".format(UiConstants.settingsFile))
		self.__defaultSettings = QSettings(umbra.ui.common.getResourcePath(UiConstants.settingsFile), QSettings.IniFormat)

	def __getDefaultLayoutsSettings(self):
		"""
		Gets the default layouts settings.
		"""

		LOGGER.debug("> Accessing '{0}' default layouts settings file!".format(UiConstants.layoutsFile))
		self.__defaultLayoutsSettings = QSettings(umbra.ui.common.getResourcePath(UiConstants.layoutsFile),
												QSettings.IniFormat)

	def setDefaultPreferences(self):
		"""
		Defines the default settings file content.
		
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing default settings!")

		for key in self.__defaultSettings.allKeys():
			self.__settings.setValue(key, self.__defaultSettings.value(key))

		self.setDefaultLayouts()
		return True

	def setDefaultLayouts(self, ignoredLayouts=None):
		"""
		Sets the default layouts in the preferences file.

		:param ignoredLayouts: Ignored layouts.
		:type ignoredLayouts: tuple or list
		:return: Method success.
		:rtype: bool
		"""

		for key in self.__defaultLayoutsSettings.allKeys():
			if ignoredLayouts:
				if tuple((layout for layout in ignoredLayouts if layout in key)):
					continue
			self.__settings.setValue(key, self.__defaultLayoutsSettings.value(key))
		return True
