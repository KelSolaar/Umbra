#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**completers.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	| This module defines the Application completers classes.
	| Each completer class completion list is initialized only once per session and
	| cached at the first class instantiation.

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
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "DefaultCompleter"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class DefaultCompleter(QCompleter):
	"""
	This class is a `QCompleter <http://doc.qt.nokia.com/qcompleter.html>`_ subclass used
	as a completion widget.
	"""

	__tokens = {}
	"""Tokens cache. ( Dictionary )"""

	@core.executionTrace
	def __init__(self, parent=None, language=None, tokens=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param language: Language name. ( String )
		:param tokens: Completer tokens list. ( Tuple / List )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__language = None
		self.language = language

		self.__setCache(tokens)

		QCompleter.__init__(self,
		DefaultCompleter._DefaultCompleter__tokens[self.__language], parent)

		self.setCaseSensitivity(Qt.CaseSensitive)
		self.setCompletionMode(QCompleter.PopupCompletion)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"language", value)
		self.__language = value

	@language.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def language(self):
		"""
		This method is the deleter method for **self.__language** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "language"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __setCache(self, tokens):
		"""
		This method sets the tokens cache.
		
		:param tokens: Completer tokens list. ( Tuple / List )
		"""

		if DefaultCompleter._DefaultCompleter__tokens.get(self.__language):
			return

		DefaultCompleter._DefaultCompleter__tokens[self.__language] = tokens

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
