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
from PyQt4.QtGui import QSyntaxHighlighter
from PyQt4.QtGui import QTextCharFormat

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
from foundations.nodes import AbstractCompositeNode
from umbra.globals.constants import Constants
from umbra.ui.nodes import DefaultNode
from umbra.ui.nodes import FormatNode
from umbra.ui.themes import DEFAULT_THEME

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"Rule",
			"FormatsTree",
			"AbstractHighlighter",
			"DefaultHighlighter"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Rule(foundations.dataStructures.Structure):
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

		foundations.dataStructures.Structure.__init__(self, **kwargs)

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

		if value is not None:
			assert issubclass(value.__class__, AbstractCompositeNode), \
			"'{0}' attribute: '{1}' is not a '{2}' subclass!".format("rootNode", value, AbstractCompositeNode.__name__)
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

		for item in sorted(theme):
			currentNode = self.__rootNode
			for format in item.split("."):
				nodes = [node for node in currentNode.children if node.name == format]
				formatNode = foundations.common.getFirstItem(nodes)
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
	@core.memoize(None)
	def getFormat(self, name):
		"""
		This method returns the closest format or closest parent format associated to given name.
		
		:param name: Format name. ( String)
		:return: Format. ( QTextCharFormat )
		"""

		formats = [format for format in self.listFormats(self.__rootNode) if format in name]
		if not formats:
			return QTextCharFormat()

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
	This class is a `QSyntaxHighlighter <http://doc.qt.nokia.com/qsyntaxhighlighter.html>`_ subclass used
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

		if value is not None:
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

		if value is not None:
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
		This method reimplements the :meth:`QSyntaxHighlighter.highlightBlock` method.

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
	def __init__(self, parent=None, rules=None, theme=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		:param rules: Rules. ( Tuple / List )
		:param theme: Theme. ( Dictionary )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractHighlighter.__init__(self, parent)

		# --- Setting class attributes. ---
		self.rules = rules
		self.__theme = None
		self.theme = theme

		self.__setFormats()

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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

		if value is not None:
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

	# @core.executionTrace
	def highlightBlock(self, block):
		"""
		This method reimplements the :meth:`AbstractHighlighter.highlightBlock` method.

		:param block: Text block. ( QString )
		"""

		self.highlightText(block, 0, len(block))
		self.setCurrentBlockState(0)

		state = 1
		for rule in self.rules:
			if re.match("comment\.block\.[\w\.]*start", rule.name):
				format = self.formats.getFormat(rule.name) or self.formats.getFormat("default")
				if self.highlightMultilineBlock(block, rule.pattern, foundations.common.getFirstItem([item for item in self.rules
										if item.name == rule.name.replace("start", "end")]).pattern, state, format):
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
