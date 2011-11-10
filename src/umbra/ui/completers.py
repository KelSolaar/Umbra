#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**completers.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	| This module defines the Application completers classes.
	| Each completer class completion list is initialized only once per session at the first class instantiation.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QCompleter
from PyQt4.QtGui import QStringListModel

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import umbra.ui.common
from umbra.globals.constants import Constants
from umbra.globals.uiConstants import UiConstants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
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

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class PythonCompleter(QCompleter):
	"""
	This class is a `QCompleter <http://doc.qt.nokia.com/4.7/qcompleter.html>`_ subclass used
	as a Python completion widget.
	"""

	__pythonTokens = None

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__setPythonTokens()

		QCompleter.__init__(self, PythonCompleter._PythonCompleter__pythonTokens, parent)

		self.setCaseSensitivity(Qt.CaseSensitive)
		self.setCompletionMode(QCompleter.PopupCompletion)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def pythonTokens(self):
		"""
		This method is the property for **PythonCompleter._PythonCompleter__pythonTokens** attribute.

		:return: PythonCompleter._PythonCompleter__pythonTokens. ( Tuple / List )
		"""

		return PythonCompleter._PythonCompleter__pythonTokens

	@pythonTokens.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def pythonTokens(self, value):
		"""
		This method is the setter method for **PythonCompleter._PythonCompleter__pythonTokens** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
			"pythonTokens", value)
			for element in value:
				assert type(element) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"pythonTokens", element)				
		PythonCompleter._PythonCompleter__pythonTokens = value

	@pythonTokens.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def pythonTokens(self):
		"""
		This method is the deleter method for **PythonCompleter._PythonCompleter__pythonTokens** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "pythonTokens"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __setPythonTokens(self, splitter="|"):
		"""
		This method sets the Python tokens.

		:param splitters: Splitter character. ( String )
		"""

		if PythonCompleter._PythonCompleter__pythonTokens:
			return

		sections = umbra.ui.common.getTokensParser(PYTHON_TOKENS_FILE).sections
		PythonCompleter._PythonCompleter__pythonTokens = [token for section in sections["Tokens"].values()
														for token in section.split(splitter)]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def updateModel(self, words):
		"""
		This method updates the completer model.

		:param words: Words to update the completer with. ( Tuple / List )
		:return: Method success. ( Boolean )
		"""

		extendedWords = PythonCompleter._PythonCompleter__pythonTokens[:]
		extendedWords.extend((word for word in set(words) if word not in PythonCompleter._PythonCompleter__pythonTokens))
		self.setModel(QStringListModel(extendedWords))
		return True

class EnglishCompleter(QCompleter):
	"""
	This class is a `QCompleter <http://doc.qt.nokia.com/4.7/qcompleter.html>`_ subclass used
	as an english text completion widget.
	"""

	__englishWords = None

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__setEnglishWords()

		QCompleter.__init__(self, EnglishCompleter._EnglishCompleter__englishWords, parent)

		self.setCaseSensitivity(Qt.CaseSensitive)
		self.setCompletionMode(QCompleter.PopupCompletion)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def englishWords(self):
		"""
		This method is the property for **self.__englishWords** attribute.

		:return: self.__englishWords. ( Tuple / List )
		"""

		return EnglishCompleter._EnglishCompleter__englishWords

	@englishWords.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def englishWords(self, value):
		"""
		This method is the setter method for **EnglishCompleter._EnglishCompleter__englishWords** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
			"englishWords", value)
			for element in value:
				assert type(element) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"englishWords", element)				
		EnglishCompleter._EnglishCompleter__englishWords = value

	@englishWords.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def englishWords(self):
		"""
		This method is the deleter method for **EnglishCompleter._EnglishCompleter__englishWords** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "englishWords"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __setEnglishWords(self):
		"""
		This method sets the english words.
		"""

		if EnglishCompleter._EnglishCompleter__englishWords:
			return

		EnglishCompleter._EnglishCompleter__englishWords = []
		with open(ENGLISH_WORDS_FILE, "r") as file:
			for line in iter(file):
				EnglishCompleter._EnglishCompleter__englishWords.append(line.strip())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def updateModel(self, words):
		"""
		This method updates the completer model.

		:param words: Words to update the completer with. ( Tuple / List )
		:return: Method success. ( Boolean )
		"""

		extendedWords = EnglishCompleter._EnglishCompleter__englishWords[:]
		extendedWords.extend((word for word in set(words) if word not in EnglishCompleter._EnglishCompleter__englishWords))
		self.setModel(QStringListModel(extendedWords))
		return True
