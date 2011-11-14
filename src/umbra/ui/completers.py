#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**completers.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	| This module defines the Application completers classes.
	| Each completer class completion list is initialized only once per session and cached at the first class instantiation.

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
from foundations.parsers import SectionsFileParser
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "ENGLISH_WORDS_FILE", "DefaultCompleter", "EnglishCompleter"]

LOGGER = logging.getLogger(Constants.logger)

ENGLISH_WORDS_FILE = umbra.ui.common.getResourcePath("others/English_Words.rc")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class DefaultCompleter(QCompleter):
	"""
	This class is a `QCompleter <http://doc.qt.nokia.com/4.7/qcompleter.html>`_ subclass used
	as a completion widget.
	"""

	__tokens = {}

	@core.executionTrace
	def __init__(self, parent=None, parser=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__parser = None
		self.parser = parser

		self.__language = self.__parser.getValue("Name", "Language")

		self.__setTokens()

		QCompleter.__init__(self,
		DefaultCompleter._DefaultCompleter__tokens[self.__language], parent)

		self.setCaseSensitivity(Qt.CaseSensitive)
		self.setCompletionMode(QCompleter.PopupCompletion)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def parser(self):
		"""
		This method is the property for **self.__parser** attribute.

		:return: self.__parser. ( String )
		"""

		return self.__parser

	@parser.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def parser(self, value):
		"""
		This method is the setter method for **self.__parser** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) is SectionsFileParser, "'{0}' attribute: '{1}' type is not 'SectionsFileParser'!".format("parser", value)
		self.__parser = value

	@parser.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def parser(self):
		"""
		This method is the deleter method for **self.__parser** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "parser"))

	@property
	def language(self):
		"""
		This method is the property for **self.__language** attribute.

		:return: self.__language. ( String )
		"""

		return self.__language

	@language.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def language(self, value):
		"""
		This method is the setter method for **self.__language** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "language"))

	@language.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def language(self):
		"""
		This method is the deleter method for **self.__language** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "language"))

	@property
	def tokens(self):
		"""
		This method is the property for **DefaultCompleter._DefaultCompleter__tokens** attribute.

		:return: DefaultCompleter._DefaultCompleter__tokens. ( Dictionary )
		"""

		return DefaultCompleter._PythonCompleter__tokens

	@tokens.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def tokens(self, value):
		"""
		This method is the setter method for **DefaultCompleter._DefaultCompleter__tokens** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tokens"))

	@tokens.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tokens(self):
		"""
		This method is the deleter method for **DefaultCompleter._DefaultCompleter__tokens** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tokens"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __setTokens(self, splitter="|"):
		"""
		This method sets the tokens.

		:param splitters: Splitter character. ( String )
		"""

		if DefaultCompleter._DefaultCompleter__tokens.get(self.__language):
			return

		sections = self.__parser.sections
		DefaultCompleter._DefaultCompleter__tokens[self.__language] = [token for attribute in sections["Tokens"].values()
																for token in attribute.split(splitter)]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def updateModel(self, words):
		"""
		This method updates the completer model.

		:param words: Words to update the completer with. ( Tuple / List )
		:return: Method success. ( Boolean )
		"""

		extendedWords = DefaultCompleter._DefaultCompleter__tokens[self.__language][:]
		extendedWords.extend((word for word in set(words)
							if word not in DefaultCompleter._DefaultCompleter__tokens[self.__language]))
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
