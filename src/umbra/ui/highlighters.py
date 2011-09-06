#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**highlighters.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application highlighters classes.

**Others:**
	Portions of the code from PyQtWiki: http://diotavelli.net/PyQtWiki/Python%20syntax%20highlighting

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
from foundations.parser import Parser
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

__all__ = ["LOGGER", "PYTHON_TOKENS_FILE" , "getFormat" , "Rule", "Formats", "Highlighter", "LoggingHighlighter", "PythonHighlighter"]

LOGGER = logging.getLogger(Constants.logger)

PYTHON_TOKENS_FILE = umbra.ui.common.getResourcePath(UiConstants.pythonTokensFile)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
@core.executionTrace
def getFormat(**kwargs):
	"""
	This definition returns a `QTextCharFormat <http://doc.qt.nokia.com/4.7/qtextcharformat.html>`_ format.
	
	:param \*\*kwargs: Format settings. ( Key / Value pairs )
	:return: Format. ( QTextCharFormat )
	"""

	settings = core.Structure(**{"format" : QTextCharFormat(),
								"backgroundColor" : None,
								"color" : None,
								"fontWeight" : None,
								"fontPointSize" : None,
								"italic" : False})
	settings.update(kwargs)

	format = QTextCharFormat(settings.format)
	
	settings.backgroundColor and format.setBackground(settings.backgroundColor)
	settings.color and format.setForeground(settings.color)
	settings.fontWeight and format.setFontWeight(settings.fontWeight)
	settings.fontPointSize and format.setFontPointSize(settings.fontPointSize)
	settings.italic and	format.setFontItalic(True)

	return format

class Rule(core.Structure):
	"""
	This class represents a storage object for highlighters rule. 
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: pattern, format. ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

class Formats(core.Structure):
	"""
	This class represents a storage object for highlighters formats. 
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: name. ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

class Highlighter(QSyntaxHighlighter):
	"""
	This class is a `QSyntaxHighlighter <http://doc.qt.nokia.com/4.7/qsyntaxhighlighter.html>`_ subclass used as a base for highlighters classes.
	"""

	@core.executionTrace
	def __init__(self, parent):
		"""
		This method initializes the class.

		:param parent: Syntax highlighter parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QSyntaxHighlighter.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__formats = None
		self.__rules = None

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def formats(self):
		"""
		This method is the property for **self.__formats** attribute.

		:return: self.__formats. ( Formats )
		"""

		return self.__formats

	@formats.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def formats(self, value):
		"""
		This method is the setter method for **self.__formats** attribute.

		:param value: Attribute value. ( Formats )
		"""

		if value:
			assert type(value) is Formats, "'{0}' attribute: '{1}' type is not 'Formats'!".format("formats", value)
		self.__formats = value

	@formats.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def formats(self):
		"""
		This method is the deleter method for **self.__formats** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("formats"))

	@property
	def rules(self):
		"""
		This method is the property for **self.__rules** attribute.

		:return: self.__rules. ( Tuple / List )
		"""

		return self.__rules

	@rules.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def rules(self, value):
		"""
		This method is the setter method for **self.__rules** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format("rules", value)
		self.__rules = value

	@rules.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def rules(self):
		"""
		This method is the deleter method for **self.__rules** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("rules"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	# @core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, NotImplementedError)
	def highlightBlock(self, block):
		"""
		This method highlights provided text block.

		:param block: Text block. ( QString )
		"""

		raise NotImplementedError("'{0}' must be implemented by '{1}' subclasses!".format(self.highlightBlock.__name__, self.__class__.__name__))

	# @core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def highlightText(self, text, start, end):
		"""
		This method highlights provided text.

		:param text: Text. ( QString )
		:param start: Text start index. ( Integer )
		:param end: Text end index. ( Integer )
		:return: Method success. ( Boolean )
		"""

		for rule in self.__rules:
			index = rule.pattern.indexIn(text, start)
			while index >= start and index < end:
				length = rule.pattern.matchedLength()
				self.setFormat(index, min(length, end - index), rule.format)
				index = rule.pattern.indexIn(text, index + length)
		return True

class LoggingHighlighter(Highlighter):
	"""
	This class is a :class:`Highlighter` subclass subclass providing syntax highlighting for Application logging documents.
	"""

	@core.executionTrace
	def __init__(self, parent):
		"""
		This method initializes the class.

		:param parent: Syntax highlighter parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QSyntaxHighlighter.__init__(self, parent)

		self.__setFormats()
		self.__setRules()

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __setFormats(self):
		"""
		This method sets the highlighting formats.

		:return: Method success. ( Boolean )
		"""

		self.formats = Formats(default=getFormat(color=QColor(192, 192, 192)))

		self.formats.loggingCritical = getFormat(format=self.formats.default, color=QColor(48, 48, 48), backgroundColor=QColor(255, 64, 64))
		self.formats.loggingError = getFormat(format=self.formats.default, color=QColor(255, 64, 64))
		self.formats.loggingWarning = getFormat(format=self.formats.default, color=QColor(255, 128, 0))
		self.formats.loggingInfo = getFormat(format=self.formats.default)
		self.formats.loggingDebug = getFormat(format=self.formats.default, italic=True)

		self.formats.loggingDebugTraceIn = getFormat(format=self.formats.loggingDebug, color=QColor(128, 160, 192))
		self.formats.loggingDebugTraceOut = getFormat(format=self.formats.loggingDebug, color=QColor(QColor(192, 160, 128)))

		return True

	@core.executionTrace
	def __setRules(self):
		"""
		This method sets the highlighting rules.

		:return: Method success. ( Boolean )
		"""

		self.__multiLineSingleString = QRegExp(r"\"\"\"|'''")
		self.__multiLineDoubleString = QRegExp(r"\"\"\"|'''")

		self.rules = []

		self.rules.append(Rule(pattern=QRegExp(r"^CRITICAL\s*:.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*CRITICAL\s*:.*$"), format=self.formats.loggingCritical))
		self.rules.append(Rule(pattern=QRegExp(r"^ERROR\s*:.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*ERROR\s*:.*$"), format=self.formats.loggingError))
		self.rules.append(Rule(pattern=QRegExp(r"^WARNING\s*:.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*WARNING\s*:.*$"), format=self.formats.loggingWarning))
		self.rules.append(Rule(pattern=QRegExp(r"^INFO\s*:.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*INFO\s*:.*$"), format=self.formats.loggingInfo))
		self.rules.append(Rule(pattern=QRegExp(r"^DEBUG\s*:.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*DEBUG\s*:.*$"), format=self.formats.loggingDebug))

		self.rules.append(Rule(pattern=QRegExp(r"^DEBUG\s*:\s--->>>.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*DEBUG\s*:\s--->>>.*$"), format=self.formats.loggingDebugTraceIn))
		self.rules.append(Rule(pattern=QRegExp(r"^DEBUG\s*:\s---<<<.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*DEBUG\s*:\s---<<<.*$"), format=self.formats.loggingDebugTraceOut))

		return True

	# @core.executionTrace
	def highlightBlock(self, block):
		"""
		This method highlights provided text block.

		:param block: Text block. ( QString )
		"""

		self.highlightText(block, 0, len(block))

class PythonHighlighter(Highlighter):
	"""
	This class is a :class:`Highlighter` subclass providing syntax highlighting for Python documents.
	"""

	@core.executionTrace
	def __init__(self, parent):
		"""
		This method initializes the class.

		:param parent: Syntax highlighter parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QSyntaxHighlighter.__init__(self, parent)

		self.__multiLineSingleString = None
		self.__multiLineDoubleString = None

		self.__setPythonTokens()
		self.__setFormats()
		self.__setRules()

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def multiLineSingleString(self):
		"""
		This method is the property for **self.__multiLineSingleString** attribute.

		:return: self.__multiLineSingleString. ( QRegExp )
		"""

		return self.__multiLineSingleString

	@multiLineSingleString.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def multiLineSingleString(self, value):
		"""
		This method is the setter method for **self.__multiLineSingleString** attribute.

		:param value: Attribute value. ( QRegExp )
		"""

		if value:
			assert type(value) is QRegExp, "'{0}' attribute: '{1}' type is not 'QRegExp'!".format("multiLineSingleString", value)
		self.__multiLineSingleString = value

	@multiLineSingleString.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def multiLineSingleString(self):
		"""
		This method is the deleter method for **self.__multiLineSingleString** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("multiLineSingleString"))

	@property
	def multiLineDoubleString(self):
		"""
		This method is the property for **self.__multiLineDoubleString** attribute.

		:return: self.__multiLineDoubleString. ( QRegExp )
		"""

		return self.__multiLineDoubleString

	@multiLineDoubleString.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def multiLineDoubleString(self, value):
		"""
		This method is the setter method for **self.__multiLineDoubleString** attribute.

		:param value: Attribute value. ( QRegExp )
		"""

		if value:
			assert type(value) is QRegExp, "'{0}' attribute: '{1}' type is not 'QRegExp'!".format("multiLineDoubleString", value)
		self.__multiLineDoubleString = value

	@multiLineDoubleString.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def multiLineDoubleString(self):
		"""
		This method is the deleter method for **self.__multiLineDoubleString** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("multiLineDoubleString"))

	@property
	def pythonTokens(self):
		"""
		This method is the property for **self.__pythonTokens** attribute.

		:return: self.__pythonTokens. ( Parser )
		"""

		return self.__pythonTokens

	@pythonTokens.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def pythonTokens(self, value):
		"""
		This method is the setter method for **self.__pythonTokens** attribute.

		:param value: Attribute value. ( Parser )
		"""

		if value:
			assert type(value) is Parser, "'{0}' attribute: '{1}' type is not 'Parser'!".format("pythonTokens", value)
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
	def __setPythonTokens(self):
		"""
		This method sets the Python tokens.

		:return: Method success. ( Boolean )
		"""

		self.__pythonTokens = umbra.ui.common.getTokensParser(PYTHON_TOKENS_FILE)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __setKeywords(self, splitter="|"):
		"""
		This method sets the highlighting keywords.

		:param splitters: Splitter character. ( String )
		:return: Method success. ( Boolean )
		"""

		self.__keywords = self.__pythonTokens.getValue("keywords", "Tokens").split(splitter)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __setFormats(self):
		"""
		This method sets the highlighting formats.

		:return: Method success. ( Boolean )
		"""

		self.formats = Formats(default=getFormat(color=QColor(192, 192, 192)))

		self.formats.keyword = getFormat(format=self.formats.default, color=QColor(205, 170, 105), bold=True)

		self.formats.numericConstant = getFormat(format=self.formats.default, color=QColor(205, 105, 75))
		self.formats.numericIntegerDecimal = getFormat(format=self.formats.numericConstant)
		self.formats.numericIntegerLongDecimal = getFormat(format=self.formats.numericConstant)
		self.formats.numericIntegerHexadecimal = getFormat(format=self.formats.numericConstant)
		self.formats.numericIntegerLongHexadecimal = getFormat(format=self.formats.numericConstant)
		self.formats.numericIntegerOctal = getFormat(format=self.formats.numericConstant)
		self.formats.numericIntegerLongOctal = getFormat(format=self.formats.numericConstant)
		self.formats.numericFloat = getFormat(format=self.formats.numericConstant)
		self.formats.numericComplex = getFormat(format=self.formats.numericConstant)

		self.formats.modifierGlobal = getFormat(format=self.formats.default, color=QColor(250, 240, 150))
		self.formats.modifierSpecialGlobal = getFormat(format=self.formats.modifierGlobal)

		self.formats.operator = getFormat(format=self.formats.keyword)
		self.formats.operatorComparison = getFormat(format=self.formats.operator)
		self.formats.operatorAssignement = getFormat(format=self.formats.operator)
		self.formats.operatorAssignementAugmented = getFormat(format=self.formats.operator)
		self.formats.operatorArithmetic = getFormat(format=self.formats.operator)

		self.formats.entity = getFormat(format=self.formats.default, color=QColor(155, 110, 165))
		self.formats.entityClass = getFormat(format=self.formats.entity)
		self.formats.entityFunction = getFormat(format=self.formats.entity)
		self.formats.entityDecorator = getFormat(format=self.formats.entity)

		self.formats.builtins = getFormat(format=self.formats.default, color=QColor(115, 135, 175))
		self.formats.builtinsExceptions = getFormat(format=self.formats.builtins)
		self.formats.builtinsFunctions = getFormat(format=self.formats.builtins)
		self.formats.builtinsMiscellaneous = getFormat(format=self.formats.builtins)
		self.formats.builtinsObjectMethods = getFormat(format=self.formats.builtins)
		self.formats.magicMethods = getFormat(format=self.formats.builtins)

		self.formats.magicObject = getFormat(format=self.formats.default, fontWeight=QFont.Bold)

		self.formats.decoratorArgument = getFormat(format=self.formats.default, color=QColor(115, 135, 175), italic=True)

		self.formats.singleLineComment = getFormat(format=self.formats.default, color=QColor(128, 128, 128))

		self.formats.multiLineString = getFormat(format=self.formats.default, color=QColor(205, 105, 75), italic=True)

		self.formats.quotation = getFormat(format=self.formats.default, color=QColor(145, 160, 105), italic=True)
		self.formats.doubleQuotation = getFormat(format=self.formats.quotation)
		self.formats.singleQuotation = getFormat(format=self.formats.quotation)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __setRules(self):
		"""
		This method sets the highlighting rules.

		:return: Method success. ( Boolean )
		"""

		self.__multiLineSingleString = QRegExp(r"^\s*\"\"\"|\"\"\"\s*$")
		self.__multiLineDoubleString = QRegExp(r"^\s*'''|'''\s*$")

		self.rules = []
		self.rules.append(Rule(pattern=QRegExp(r"\b({0})\b".format(self.__pythonTokens.getValue("keywords", "Tokens"))), format=self.formats.keyword))

		self.rules.append(Rule(pattern=QRegExp(r"\b[-+]?[1-9]+\d*|0\b"), format=self.formats.numericIntegerDecimal))
		self.rules.append(Rule(pattern=QRegExp(r"\b([-+]?[1-9]+\d*|0)L\b"), format=self.formats.numericIntegerLongDecimal))
		self.rules.append(Rule(pattern=QRegExp(r"\b[-+]?0x[a-fA-F\d]+L\b"), format=self.formats.numericIntegerLongHexadecimal))
		self.rules.append(Rule(pattern=QRegExp(r"\b[-+]?0x[a-fA-F\d]+\b"), format=self.formats.numericIntegerHexadecimal))
		self.rules.append(Rule(pattern=QRegExp(r"\b[-+]?0x[a-fA-F\d]+L\b"), format=self.formats.numericIntegerLongHexadecimal))
		self.rules.append(Rule(pattern=QRegExp(r"\b[-+]?0[0-7]+\b"), format=self.formats.numericIntegerOctal))
		self.rules.append(Rule(pattern=QRegExp(r"\b[-+]?0[0-7]+L\b"), format=self.formats.numericIntegerLongOctal))
		self.rules.append(Rule(pattern=QRegExp(r"[-+]?\d*\.?\d+([eE][-+]?\d+)?"), format=self.formats.numericFloat))
		self.rules.append(Rule(pattern=QRegExp(r"[-+]?\d*\.?\d+([eE][-+]?\d+)?\s*\s*[-+]?\d*\.?\d+([eE][-+]?\d+)?[jJ]"), format=self.formats.numericComplex))

		self.rules.append(Rule(pattern=QRegExp(r"\b(global)\b"), format=self.formats.modifierGlobal))
		self.rules.append(Rule(pattern=QRegExp(r"\b[A-Z_]+\b"), format=self.formats.modifierSpecialGlobal))

		self.rules.append(Rule(pattern=QRegExp(r"<\=|>\=|\=\=|<|>|\!\="), format=self.formats.operatorComparison))
		self.rules.append(Rule(pattern=QRegExp(r"\="), format=self.formats.operatorAssignement))
		self.rules.append(Rule(pattern=QRegExp(r"\+\=|-\=|\*\=|/\=|//\=|%\=|&\=|\|\=|\^\=|>>\=|<<\=|\*\*\="), format=self.formats.operatorAssignementAugmented))
		self.rules.append(Rule(pattern=QRegExp(r"\+|\-|\*|\*\*|/|//|%|<<|>>|&|\||\^|~"), format=self.formats.operatorArithmetic))

		# This rules don't work: QRegExp lacks of lookbehind support.		
		self.rules.append(Rule(pattern=QRegExp(r"(?<=class\s)\w+(?=\s?\(\)\s?:)"), format=self.formats.entityClass))
		self.rules.append(Rule(pattern=QRegExp(r"(?<=def\s)\w+(?=\s?\(\)\s?:)"), format=self.formats.entityFunction))

		self.rules.append(Rule(pattern=QRegExp(r"@[\w\.]+"), format=self.formats.entityDecorator))

		self.rules.append(Rule(pattern=QRegExp(r"\b({0})\b".format(self.__pythonTokens.getValue("builtinsExceptions", "Tokens"))), format=self.formats.builtinsExceptions))
		self.rules.append(Rule(pattern=QRegExp(r"\b({0})\b".format(self.__pythonTokens.getValue("builtinsFunctions", "Tokens"))), format=self.formats.builtinsFunctions))
		self.rules.append(Rule(pattern=QRegExp(r"\b({0})\b".format(self.__pythonTokens.getValue("builtinsMiscellaneous", "Tokens"))), format=self.formats.builtinsMiscellaneous))
		self.rules.append(Rule(pattern=QRegExp(r"\b({0})\b".format(self.__pythonTokens.getValue("builtinsObjectMethods", "Tokens"))), format=self.formats.builtinsObjectMethods))
		self.rules.append(Rule(pattern=QRegExp(r"\b({0})\b".format(self.__pythonTokens.getValue("magicMethods", "Tokens"))), format=self.formats.magicMethods))

		self.rules.append(Rule(pattern=QRegExp(r"\b(?:(?!({0}|{1}|{2}))__\w+__)\b".format(self.__pythonTokens.getValue("builtinsMiscellaneous", "Tokens"), self.__pythonTokens.getValue("builtinsObjectMethods", "Tokens"), self.__pythonTokens.getValue("magicMethods", "Tokens"))), format=self.formats.magicObject))

		self.rules.append(Rule(pattern=QRegExp(r"\bself\b"), format=self.formats.decoratorArgument))

		self.rules.append(Rule(pattern=QRegExp(r"#.*$\n?"), format=self.formats.singleLineComment))

		self.rules.append(Rule(pattern=QRegExp(r"\"[^\n\"]*\""), format=self.formats.doubleQuotation))
		self.rules.append(Rule(pattern=QRegExp(r"'[^\n']*'"), format=self.formats.singleQuotation))

		return True

	# @core.executionTrace
	def highlightBlock(self, block):
		"""
		This method highlights provided text block.

		:param block: Text block. ( QString )
		"""

		self.highlightText(block, 0, len(block))
		self.setCurrentBlockState(0)

		not self.highlightMultilineBlock(block, self.__multiLineSingleString, 1, self.formats.multiLineString) and self.highlightMultilineBlock(block, self.__multiLineDoubleString, 2, self.formats.multiLineString)

	# @core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def highlightMultilineBlock(self, block, pattern, state, format):
		"""
		This method highlights provided multiline text block.

		:param block: Text block. ( QString )
		:param pattern: Regex pattern. ( QRegExp )
		:param state: Block state. ( Integer )
		:param format: Format. ( QTextCharFormat )
		:return: Current block matching state. ( Boolean )
		"""

		if self.previousBlockState() == state:
			start = 0
			extend = 0
		else:
			start = pattern.indexIn(block)
			extend = pattern.matchedLength()

		while start >= 0:
			end = pattern.indexIn(block, start + extend)
			if end >= extend:
				length = end - start + extend + pattern.matchedLength()
				self.setCurrentBlockState(0)
			else:
				self.setCurrentBlockState(state)
				length = block.length() - start + extend
			self.setFormat(start, length, format)
			start = pattern.indexIn(block, start + length)

		if self.currentBlockState() == state:
			return True
		else:
			return False
