#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**completers.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	| Defines the Application completers classes.
	| Each completer class completion list is initialized only once per session and
	| cached at the first class instantiation.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QCompleter
from PyQt4.QtGui import QStringListModel

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "DefaultCompleter"]

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class DefaultCompleter(QCompleter):
	"""
	Defines a `QCompleter <http://doc.qt.nokia.com/qcompleter.html>`_ subclass used
	as a completion widget.
	"""

	__tokens = {}
	"""
	:param __tokens: Tokens cache.
	:type __tokens: dict
	"""

	def __init__(self, parent=None, language=None, tokens=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param language: Language name.
		:type language: unicode
		:param tokens: Completer tokens list.
		:type tokens: tuple or list
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__language = None
		self.language = language

		self.__set_cache(tokens)

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
		Property for **self.__language** attribute.

		:return: self.__language.
		:rtype: unicode
		"""

		return self.__language

	@language.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def language(self, value):
		"""
		Setter for **self.__language** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"language", value)
		self.__language = value

	@language.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def language(self):
		"""
		Deleter for **self.__language** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "language"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __set_cache(self, tokens):
		"""
		Sets the tokens cache.
		
		:param tokens: Completer tokens list.
		:type tokens: tuple or list
		"""

		if DefaultCompleter._DefaultCompleter__tokens.get(self.__language):
			return

		DefaultCompleter._DefaultCompleter__tokens[self.__language] = tokens

	def update_model(self, words):
		"""
		Updates the completer model.

		:param words: Words to update the completer with.
		:type words: tuple or list
		:return: Method success.
		:rtype: bool
		"""

		extended_words = DefaultCompleter._DefaultCompleter__tokens[self.__language][:]
		extended_words.extend((word for word in set(words)
							if word not in DefaultCompleter._DefaultCompleter__tokens[self.__language]))
		self.setModel(QStringListModel(extended_words))
		return True
