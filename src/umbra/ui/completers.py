#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**completers.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application completers classes.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import umbra.ui.common
from umbra.globals.constants import Constants
from umbra.globals.uiConstants import UiConstants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "PYTHON_TOKENS_FILE" , "ENGLISH_WORDS_FILE", "PythonCompleter", "EnglishCompleter"]

LOGGER = logging.getLogger(Constants.logger)

PYTHON_TOKENS_FILE = umbra.ui.common.getResourcePath(UiConstants.pythonTokensFile)
ENGLISH_WORDS_FILE = umbra.ui.common.getResourcePath("others/English_Words.rc")

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class PythonCompleter(QCompleter):
	"""
	This class is a `QCompleter <http://doc.qt.nokia.com/4.7/qcompleter.html>`_ subclass used as a Python completion widget.
	"""

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__setPythonTokens()

		QCompleter.__init__(self, self.__pythonTokens, parent)

		self.setCaseSensitivity(Qt.CaseSensitive)
		self.setCompletionMode(QCompleter.PopupCompletion)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def pythonTokens(self):
		"""
		This method is the property for **self.__pythonTokens** attribute.

		:return: self.__pythonTokens. ( Tuple / List )
		"""

		return self.__pythonTokens

	@pythonTokens.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def pythonTokens(self, value):
		"""
		This method is the setter method for **self.__pythonTokens** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format("pythonTokens", value)
		self.__pythonTokens = value

	@pythonTokens.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def pythonTokens(self):
		"""
		This method is the deleter method for **self.__pythonTokens** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("pythonTokens"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __setPythonTokens(self, splitter="|"):
		"""
		This method sets the Python tokens.

		:param splitters: Splitter character. ( String )
		:return: Method success. ( Boolean )
		"""

		sections = umbra.ui.common.getTokensParser(PYTHON_TOKENS_FILE).sections
		self.__pythonTokens = [token for section in sections["Tokens"].values() for token in section.split(splitter)]
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def updateModel(self, words):
		"""
		This method updates the completer model.

		:param words: Words to update the completer with. ( Tuple / List )
		:return: Method success. ( Boolean )
		"""

		extendedWords = self.__pythonTokens[:]
		extendedWords.extend((word for word in set(words) if word not in self.__pythonTokens))
		self.setModel(QStringListModel(extendedWords))
		return True

class EnglishCompleter(QCompleter):
	"""
	This class is a `QCompleter <http://doc.qt.nokia.com/4.7/qcompleter.html>`_ subclass used as an english text completion widget.
	"""

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__setEnglishWords()

		QCompleter.__init__(self, self.__englishWords, parent)

		self.setCaseSensitivity(Qt.CaseSensitive)
		self.setCompletionMode(QCompleter.PopupCompletion)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def englishWords(self):
		"""
		This method is the property for **self.__englishWords** attribute.

		:return: self.__englishWords. ( Tuple / List )
		"""

		return self.__englishWords

	@englishWords.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def englishWords(self, value):
		"""
		This method is the setter method for **self.__englishWords** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format("englishWords", value)
		self.__englishWords = value

	@englishWords.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def englishWords(self):
		"""
		This method is the deleter method for **self.__englishWords** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("englishWords"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __setEnglishWords(self):
		"""
		This method sets the english words.

		:return: Method success. ( Boolean )
		"""

		self.__englishWords = []
		with open(ENGLISH_WORDS_FILE, "r") as file:
			for line in iter(file):
				self.__englishWords.append(line.strip())
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def updateModel(self, words):
		"""
		This method updates the completer model.

		:param words: Words to update the completer with. ( Tuple / List )
		:return: Method success. ( Boolean )
		"""

		extendedWords = self.__englishWords[:]
		extendedWords.extend((word for word in set(words) if word not in self.__englishWords))
		self.setModel(QStringListModel(extendedWords))
		return True
