#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`umbra.languages.factory.scriptEditor.scriptEditor.ScriptEditor` Component Interface class Models.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from umbra.components.factory.scriptEditor.editor import Language
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "LanguagesModel"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class LanguagesModel(QAbstractListModel):
	"""
	This class is a `QAbstractListModel <http://doc.qt.nokia.com/4.7/qabstractListmodel.html>`_ subclass used to store **ScriptEditor** languages.
	"""

	@core.executionTrace
	def __init__(self, parent=None, languages=None):
		"""
		This method initializes the class.

		:param parent: Parent object. ( QObject )
		:param languages: Languages. ( List )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QAbstractListModel.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__languages = []
		self.languages = languages

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def languages(self):
		"""
		This method is the property for **self.__languages** attribute.

		:return: self.__languages. ( List )
		"""

		return self.__languages

	@languages.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def languages(self, value):
		"""
		This method is the setter method for **self.__languages** attribute.

		:param value: Attribute value. ( List )
		"""

		if value:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("languages", value)
		self.__languages = value

	@languages.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def languages(self):
		"""
		This method is the deleter method for **self.__languages** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "languages"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
	def rowCount(self, parent=QModelIndex()):
		"""
		This method returns the Model row count.

		:param parent: Parent. ( QModelIndex )
		:return: Row count. ( Integer )
		"""

		return len(self.__languages)

	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
	def data(self, index, role=Qt.DisplayRole):
		"""
		This method returns the Model data.

		:param index: Index. ( QModelIndex )
		:param role: Role. ( Integer )
		:return: Data. ( QVariant )
		"""

		if not index.isValid():
			return QVariant()

		if role == Qt.DisplayRole:
			return QVariant(self.__languages[index.row()].name)
		return QVariant()

	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
	def sortLanguages(self, order=Qt.AscendingOrder):
		"""
		This method sorts the Model languages.
		
		:param order: Order. ( Qt.SortOrder )
		"""

		self.beginResetModel()
		self.__languages = sorted(self.__languages, key=lambda x: (x.name), reverse=order)
		self.endResetModel()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def registerLanguage(self, language):
		"""
		This method registers provided language in the :obj:`LanguagesModel.languages` class property.
		
		:param language: Language to register. ( Language )
		:return: Method success. ( Boolean )
		"""

		if not isinstance(language, Language):
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' is not a 'Language' instance!".format(self.__class__.__name__, language))

		if self.getLanguage(language):
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' language is already registered!".format(self.__class__.__name__, language.name))

		self.__languages.append(language)
		self.sortLanguages()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def unregisterLanguage(self, name):
		"""
		This method unregisters provided language name from the :obj:`LanguagesModel.languages` class property.
		
		:param name: Language to unregister. ( String )
		:return: Method success. ( Boolean )
		"""

		if not self.getLanguage(name):
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' language isn't registered!".format(self.__class__.__name__, name))

		for i, language in enumerate(self.__languages):
			if not language.name == name:
				continue

			del(self.__languages[i])
			self.sortLanguages()
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getLanguage(self, name):
		"""
		This method returns the language associated with provided name.
		
		:param name: Language name. ( String )
		:return: File language. ( Language )
		"""

		for language in self.__languages:
			if language.name == name:
				return language

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getFileLanguage(self, file):
		"""
		This method returns the language of provided file.
		
		:param file: File to get language of. ( String )
		:return: File language. ( Language )
		"""

		for language in self.__languages:
			if re.search(language.extension, file):
				LOGGER.debug("> '{0}' file detected language: '{1}'.".format(file, language.name))
				return language

