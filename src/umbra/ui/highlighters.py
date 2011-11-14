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

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import re
from PyQt4.QtCore import QRegExp
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QSyntaxHighlighter
from PyQt4.QtGui import QTextCharFormat

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.namespace
import umbra.ui.common
from foundations.dag import AbstractCompositeNode
from foundations.parsers import SectionsFileParser
from umbra.globals.constants import Constants
from umbra.globals.uiConstants import UiConstants
from umbra.ui.models import DefaultNode

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"getFormat",
			"DEFAULT_FORMAT",
			"DEFAULT_THEME",
			"Rule",
			"FormatNode",
			"FormatsTree",
			"AbstractHighlighter",
			"DefaultHighlighter",
			"LoggingHighlighter"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
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

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
DEFAULT_FORMAT = getFormat(color=QColor(192, 192, 192))

DEFAULT_THEME = {"default" : None,
			"comment" : getFormat(format=DEFAULT_FORMAT, color=QColor(96, 96, 96)),
			"comment.line" : None,
			"comment.line.double-slash" : None,
			"comment.line.double-dash" : None,
			"comment.line.number-sign" : None,
			"comment.line.percentage" : None,
			"comment.line.character" : None,
			"comment.block" : None,
			"comment.block.documentation" : None,
			"constant" : getFormat(format=DEFAULT_FORMAT, color=QColor(205, 105, 75)),
			"constant.numeric" : None,
			"constant.character" : None,
			"constant.character.escape" : None,
			"constant.language" : None,
			"constant.other" : None,
			"entity" : getFormat(format=DEFAULT_FORMAT, color=QColor(115, 135, 175)),
			"entity.name" : None,
			"entity.name.function" : None,
			"entity.name.type" : None,
			"entity.name.tag" : None,
			"entity.name.section" : None,
			"entity.other" : None,
			"entity.inherited-class" : None,
			"entity.attribute-name" : None,
			"invalid" : None,
			"invalid.illegal" : None,
			"invalid.deprecated" : None,
			"keyword" : getFormat(format=DEFAULT_FORMAT, color=QColor(205, 170, 105), fontWeight=75),
			"keyword.control" : None,
			"keyword.operator" : getFormat(format=DEFAULT_FORMAT, color=QColor(205, 170, 105)),
			"keyword.other" : None,
			"markup" : None,
			"markup.underline" : None,
			"markup.underline.link" : None,
			"markup.bold" : None,
			"markup.heading" : None,
			"markup.italic" : None,
			"markup.list" : None,
			"markup.list.numbered" : None,
			"markup.list.unnumbered" : None,
			"markup.quote" : None,
			"markup.raw" : None,
			"markup.other" : None,
			"meta" : None,
			"storage" : None,
			"storage.type" : getFormat(format=DEFAULT_FORMAT, color=QColor(205, 170, 105), fontWeight=75),
			"storage.modifier" : getFormat(format=DEFAULT_FORMAT, italic=True),
			"string" : getFormat(format=DEFAULT_FORMAT, color=QColor(145, 160, 105), italic=True),
			"string.quoted" : None,
			"string.quoted.single" : None,
			"string.quoted.double" : None,
			"string.quoted.triple" : None,
			"string.quoted.other" : None,
			"string.unquoted" : None,
			"string.interpolated" : None,
			"string.regexp" : None,
			"string.other" : None,
			"support" : getFormat(format=DEFAULT_FORMAT, color=QColor(115, 135, 175)),
			"support.function" : None,
			"support.class" : None,
			"support.type" : None,
			"support.constant" : None,
			"support.variable" : None,
			"support.other" : None,
			"variable" : None,
			"variable.parameter" : None,
			"variable.language" : getFormat(format=DEFAULT_FORMAT, italic=True),
			"variable.language.other" : None}

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
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

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		core.Structure.__init__(self, **kwargs)

class FormatNode(AbstractCompositeNode):
	"""
	This class defines the format base node object.
	"""

	__family = "Format"

	@core.executionTrace
	def __init__(self, name=None, parent=None, children=None, format=None, **kwargs):
		"""
		This method initializes the class.

		:param name: Node name.  ( String )
		:param parent: Node parent. ( AbstractNode / AbstractCompositeNode )
		:param children: Children. ( List )
		:param format: Format. ( Object )
		:param \*\*kwargs: Keywords arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractCompositeNode.__init__(self, name, parent, children, **kwargs)

		# --- Setting class attributes. ---
		self.__format = None
		self.format = format

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def format(self):
		"""
		This method is the property for **self.__format** attribute.

		:return: self.__format. ( Object )
		"""

		return self.__format

	@format.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def format(self, value):
		"""
		This method is the setter method for **self.__format** attribute.

		:param value: Attribute value. ( Object )
		"""

		self.__format = value

	@format.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def format(self):
		"""
		This method is the deleter method for **self.__format** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "format"))

class FormatsTree(object):
	"""
	This class defines the formats tree object representing higlighters theme.
	"""

	@core.executionTrace
	def __init__(self, theme=None):
		"""
		This method initializes the class.

		:param theme: Theme. ( Dictionary )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__rootNode = DefaultNode("Formats Tree")

		self._FormatsTree__initializeTree(theme or DEFAULT_THEME)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def rootNode(self):
		"""
		This method is the property for **self.__rootNode** attribute.

		:return: self.__rootNode. ( AbstractCompositeNode )
		"""

		return self.__rootNode

	@rootNode.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def rootNode(self, value):
		"""
		This method is the setter method for **self.__rootNode** attribute.

		:param value: Attribute value. ( AbstractCompositeNode )
		"""

		if value:
			assert issubclass(value.__class__, AbstractCompositeNode), "'{0}' attribute: '{1}' is not a \
			'{2}' subclass!".format("rootNode", value, AbstractCompositeNode.__name__)
		self.__rootNode = value

	@rootNode.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def rootNode(self):
		"""
		This method is the deleter method for **self.__rootNode** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".rootNode(self.__class__.__name__, "rootNode"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __initializeTree(self, theme):
		"""
		This method initializes the object formats tree.
		
		:param theme: Theme. ( Dictionary )
		"""

		for item in sorted(theme.keys()):
			currentNode = self.__rootNode
			for format in item.split("."):
				nodes = [node for node in currentNode.children if node.name == format]
				formatNode = nodes and nodes[0] or None
				if not formatNode:
					formatNode = FormatNode(format, format=theme[item])
					currentNode.addChild(formatNode)
				currentNode = formatNode

	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listFormats(self, node, path=(), formats=None):
		"""
		This method lists the object formats in sorted order.
		
		:param node: Root node to start listing the formats from. ( AbstractCompositeNode )
		:param path: Walked paths. ( Tuple )
		:param formats: Formats. ( List )
		:return: Formats. ( List )
		"""

		if formats == None:
			formats = []

		for child in node.children:
			self.listFormats(child, path + (child.name,), formats)
		path and formats.append(".".join(path))
		return sorted(formats)

	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
	@core.memoize()
	def getFormat(self, name):
		"""
		This method returns the closest format or closest parent format associated to given name.
		
		:param name: Format name. ( String)
		:return: Format. ( QTextCharFormat )
		"""

		formats = [format for format in self.listFormats(self.__rootNode) if format in name]
		if not formats:
			return

		name = max(formats)

		format = None
		currentNode = self.__rootNode
		for selector in name.split("."):
			nodes = [node for node in currentNode.children if node.name == selector]
			formatNode = nodes and nodes[0] or None
			if not formatNode:
				break

			currentNode = formatNode

			if not formatNode.format:
				continue

			format = formatNode.format
		return format

class AbstractHighlighter(QSyntaxHighlighter):
	"""
	This class is a `QSyntaxHighlighter <http://doc.qt.nokia.com/4.7/qsyntaxhighlighter.html>`_ subclass used
	as a base for highlighters classes.
	"""

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QSyntaxHighlighter.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__formats = None
		self.__rules = None

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def formats(self):
		"""
		This method is the property for **self.__formats** attribute.

		:return: self.__formats. ( FormatsTree )
		"""

		return self.__formats

	@formats.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def formats(self, value):
		"""
		This method is the setter method for **self.__formats** attribute.

		:param value: Attribute value. ( FormatsTree )
		"""

		if value:
			assert type(value) is FormatsTree, "'{0}' attribute: '{1}' type is not 'FormatsTree'!".format("formats", value)
		self.__formats = value

	@formats.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def formats(self):
		"""
		This method is the deleter method for **self.__formats** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "formats"))

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
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
			"rules", value)
		self.__rules = value

	@rules.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def rules(self):
		"""
		This method is the deleter method for **self.__rules** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "rules"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	# @core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, NotImplementedError)
	def highlightBlock(self, block):
		"""
		This method highlights given text block.

		:param block: Text block. ( QString )
		"""

		raise NotImplementedError("{0} | '{1}' must be implemented by '{2}' subclasses!".format(self.__class__.__name__,
		 																					self.highlightBlock.__name__,
																							self.__class__.__name__))

	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
	def highlightText(self, text, start, end):
		"""
		This method highlights given text.

		:param text: Text. ( QString )
		:param start: Text start index. ( Integer )
		:param end: Text end index. ( Integer )
		:return: Method success. ( Boolean )
		"""

		for rule in self.__rules:
			index = rule.pattern.indexIn(text, start)
			while index >= start and index < end:
				length = rule.pattern.matchedLength()
				format = self.formats.getFormat(rule.name) or self.formats.getFormat("default")
				self.setFormat(index, min(length, end - index), format)
				index = rule.pattern.indexIn(text, index + length)
		return True

class DefaultHighlighter(AbstractHighlighter):
	"""
	This class is a :class:`AbstractHighlighter` subclass providing syntax highlighting for documents.
	"""

	@core.executionTrace
	def __init__(self, parent=None, parser=None, theme=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		:param parser: Parser instance. ( SectionFileParser )
		:param theme: Theme. ( Dictionary )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QSyntaxHighlighter.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__parser = None
		self.parser = parser
		self.__theme = None
		self.theme = theme

		self.__setFormats()
		self.__setRules()

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
	def theme(self):
		"""
		This method is the property for **self.__theme** attribute.

		:return: self.__theme. ( Dictionary )
		"""

		return self.__theme

	@theme.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def theme(self, value):
		"""
		This method is the setter method for **self.__theme** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("theme", value)
		self.__theme = value

	@theme.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def theme(self):
		"""
		This method is the deleter method for **self.__theme** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "theme"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __setFormats(self):
		"""
		This method sets the highlighting formats.
		"""

		self.formats = FormatsTree(self.__theme)

	@core.executionTrace
	def __setRules(self):
		"""
		This method sets the highlighting rules.
		"""

		self.rules = []

		for attribute in self.__parser.sections["Rules"]:
			pattern = self.__parser.getValue(attribute, "Rules")
			if "@Tokens" in pattern:
				pattern = pattern.replace("@Tokens",
							self.__parser.getValue(foundations.namespace.removeNamespace(attribute), "Tokens"))
			self.rules.append(Rule(name=foundations.namespace.removeNamespace(attribute),
								pattern=QRegExp(pattern)))

	# @core.executionTrace
	def highlightBlock(self, block):
		"""
		This method highlights given text block.

		:param block: Text block. ( QString )
		"""

		self.highlightText(block, 0, len(block))
		self.setCurrentBlockState(0)

		state = 1
		for rule in self.rules:
			if re.match("comment\.block\.[\w+.]+start", rule.name):
				format = self.formats.getFormat(rule.name) or self.formats.getFormat("default")
				if self.highlightMultilineBlock(block, rule.pattern, [item for item in self.rules
										if item.name == rule.name.replace("start", "end")][0].pattern, state, format):
					break
				state += 1

	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
	def highlightMultilineBlock(self, block, startPattern, endPattern, state, format):
		"""
		This method highlights given multiline text block.

		:param block: Text block. ( QString )
		:param pattern: Start regex pattern. ( QRegExp )
		:param pattern: End regex pattern. ( QRegExp )
		:param format: Format. ( QTextCharFormat )
		:param state: Block state. ( Integer )
		:return: Current block matching state. ( Boolean )
		"""

		if self.previousBlockState() == state:
			start = 0
			extend = 0
		else:
			start = startPattern.indexIn(block)
			extend = startPattern.matchedLength()

		while start >= 0:
			end = endPattern.indexIn(block, start + extend)
			if end >= extend:
				length = end - start + extend + endPattern.matchedLength()
				self.setCurrentBlockState(0)
			else:
				self.setCurrentBlockState(state)
				length = block.length() - start + extend
			self.setFormat(start, length, format)
			start = startPattern.indexIn(block, start + length)

		if self.currentBlockState() == state:
			return True
		else:
			return False

class LoggingHighlighter(AbstractHighlighter):
	"""
	This class is a :class:`AbstractHighlighter` subclass providing syntax highlighting for Application logging documents.
	"""

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QSyntaxHighlighter.__init__(self, parent)

		self.__setFormats()
		self.__setRules()

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __setFormats(self):
		"""
		This method sets the highlighting formats.
		"""

		self.formats = FormatsTree(DEFAULT_THEME)
#		self.formats = Formats(default=getFormat(color=QColor(192, 192, 192)))
#
#		self.formats.loggingCritical = getFormat(format=self.formats.default,
#												color=QColor(48, 48, 48),
#												backgroundColor=QColor(255, 64, 64))
#		self.formats.loggingError = getFormat(format=self.formats.default,
#											color=QColor(255, 64, 64))
#		self.formats.loggingWarning = getFormat(format=self.formats.default,
#												color=QColor(255, 128, 0))
#		self.formats.loggingInfo = getFormat(format=self.formats.default)
#		self.formats.loggingDebug = getFormat(format=self.formats.default,
#											italic=True)
#
#		self.formats.loggingDebugTraceIn = getFormat(format=self.formats.loggingDebug,
#													color=QColor(128, 160, 192))
#		self.formats.loggingDebugTraceOut = getFormat(format=self.formats.loggingDebug,
#													color=QColor(QColor(192, 160, 128)))

	@core.executionTrace
	def __setRules(self):
		"""
		This method sets the highlighting rules.
		"""

		self.rules = []

#		self.rules.loggingInfo = Rule(pattern=QRegExp(
#								r"^INFO\s*:.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*INFO\s*:.*$"),
#								format=self.formats.loggingInfo)
#		self.rules.loggingCritical = Rule(pattern=QRegExp(
#									r"^CRITICAL\s*:.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*CRITICAL\s*:.*$"),
#									format=self.formats.loggingCritical)
#		self.rules.loggingError = Rule(pattern=QRegExp(
#								r"^ERROR\s*:.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*ERROR\s*:.*$"),
#								format=self.formats.loggingError)
#		self.rules.loggingWarning = Rule(pattern=QRegExp(
#									r"^WARNING\s*:.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*WARNING\s*:.*$"),
#									format=self.formats.loggingWarning)
#		self.rules.loggingDebug = Rule(pattern=QRegExp(
#								r"^DEBUG\s*:.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*DEBUG\s*:.*$"),
#								format=self.formats.loggingDebug)
#
#		self.rules.loggingDebugTraceIn = Rule(pattern=QRegExp(
#								r"^DEBUG\s*:\s--->>>.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*DEBUG\s*:\s--->>>.*$"),
#								format=self.formats.loggingDebugTraceIn)
#		self.rules.loggingDebugTraceOut = Rule(pattern=QRegExp(
#								r"^DEBUG\s*:\s---<<<.*$|^[\d-]+\s+[\d:,]+\s*-\s*[\da-fA-F]+\s*-\s*DEBUG\s*:\s---<<<.*$"),
#								format=self.formats.loggingDebugTraceOut)

	# @core.executionTrace
	def highlightBlock(self, block):
		"""
		This method highlights given text block.

		:param block: Text block. ( QString )
		"""

		self.highlightText(block, 0, len(block))
