#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**highlighters.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the Application highlighters classes.

**Others:**
    Portions of the code from PyQtWiki: http://diotavelli.net/PyQtWiki/Python%20syntax%20highlighting
"""

from __future__ import unicode_literals

import re
from PyQt4.QtGui import QSyntaxHighlighter
from PyQt4.QtGui import QTextCharFormat

import foundations.common
import foundations.data_structures
import foundations.decorators
import foundations.exceptions
import foundations.verbose
from foundations.nodes import AbstractCompositeNode
from umbra.ui.nodes import DefaultNode
from umbra.ui.nodes import FormatNode
from umbra.ui.themes import DEFAULT_THEME

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
           "Rule",
           "FormatsTree",
           "AbstractHighlighter",
           "DefaultHighlighter"]

LOGGER = foundations.verbose.install_logger()


class Rule(foundations.data_structures.Structure):
    """
    Defines a storage object for highlighters rule.
    """

    def __init__(self, **kwargs):
        """
        Initializes the class.

        :param \*\*kwargs: pattern, format.
        :type \*\*kwargs: dict
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        foundations.data_structures.Structure.__init__(self, **kwargs)


class FormatsTree(object):
    """
    Defines the formats tree object representing higlighters theme.
    """

    def __init__(self, theme=None):
        """
        Initializes the class.

        :param theme: Theme.
        :type theme: dict
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        # --- Setting class attributes. ---
        self.__root_node = DefaultNode("Formats Tree")

        self._FormatsTree__initialize_tree(theme or DEFAULT_THEME)

    @property
    def root_node(self):
        """
        Property for **self.__root_node** attribute.

        :return: self.__root_node.
        :rtype: AbstractCompositeNode
        """

        return self.__root_node

    @root_node.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def root_node(self, value):
        """
        Setter for **self.__root_node** attribute.

        :param value: Attribute value.
        :type value: AbstractCompositeNode
        """

        if value is not None:
            assert issubclass(value.__class__, AbstractCompositeNode), \
                "'{0}' attribute: '{1}' is not a '{2}' subclass!".format(
                    "root_node", value, AbstractCompositeNode.__name__)
        self.__root_node = value

    @root_node.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def root_node(self):
        """
        Deleter for **self.__root_node** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".root_node(self.__class__.__name__, "root_node"))

    def __initialize_tree(self, theme):
        """
        Initializes the object formats tree.

        :param theme: Theme.
        :type theme: dict
        """

        for item in sorted(theme):
            current_node = self.__root_node
            for format in item.split("."):
                nodes = [node for node in current_node.children if node.name == format]
                format_node = foundations.common.get_first_item(nodes)
                if not format_node:
                    format_node = FormatNode(format, format=theme[item])
                    current_node.add_child(format_node)
                current_node = format_node

    def list_formats(self, node, path=(), formats=None):
        """
        Lists the object formats in sorted order.

        :param node: Root node to start listing the formats from.
        :type node: AbstractCompositeNode
        :param path: Walked paths.
        :type path: tuple
        :param formats: Formats.
        :type formats: list
        :return: Formats.
        :rtype: list
        """

        if formats == None:
            formats = []

        for child in node.children:
            self.list_formats(child, path + (child.name,), formats)
        path and formats.append(".".join(path))
        return sorted(formats)

    @foundations.decorators.memoize(None)
    def get_format(self, name):
        """
        Returns the closest format or closest parent format associated to given name.

        :param name: Format name.
        :type name: unicode
        :return: Format.
        :rtype: QTextCharFormat
        """

        formats = [format for format in self.list_formats(self.__root_node) if format in name]
        if not formats:
            return QTextCharFormat()

        name = max(formats)

        format = None
        current_node = self.__root_node
        for selector in name.split("."):
            nodes = [node for node in current_node.children if node.name == selector]
            format_node = nodes and nodes[0] or None
            if not format_node:
                break

            current_node = format_node

            if not format_node.format:
                continue

            format = format_node.format
        return format


class AbstractHighlighter(QSyntaxHighlighter):
    """
    Defines a `QSyntaxHighlighter <http://doc.qt.nokia.com/qsyntaxhighlighter.html>`_ subclass used
    as a base for highlighters classes.
    """

    def __init__(self, parent=None):
        """
        Initializes the class.

        :param parent: Widget parent.
        :type parent: QObject
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        QSyntaxHighlighter.__init__(self, parent)

        # --- Setting class attributes. ---
        self.__formats = None
        self.__rules = None

    @property
    def formats(self):
        """
        Property for **self.__formats** attribute.

        :return: self.__formats.
        :rtype: FormatsTree
        """

        return self.__formats

    @formats.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def formats(self, value):
        """
        Setter for **self.__formats** attribute.

        :param value: Attribute value.
        :type value: FormatsTree
        """

        if value is not None:
            assert type(value) is FormatsTree, "'{0}' attribute: '{1}' type is not 'FormatsTree'!".format(
                "formats", value)
        self.__formats = value

    @formats.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def formats(self):
        """
        Deleter for **self.__formats** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "formats"))

    @property
    def rules(self):
        """
        Property for **self.__rules** attribute.

        :return: self.__rules.
        :rtype: tuple or list
        """

        return self.__rules

    @rules.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def rules(self, value):
        """
        Setter for **self.__rules** attribute.

        :param value: Attribute value.
        :type value: tuple or list
        """

        if value is not None:
            assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
                "rules", value)
        self.__rules = value

    @rules.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def rules(self):
        """
        Deleter for **self.__rules** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "rules"))

    @foundations.exceptions.handle_exceptions(NotImplementedError)
    def highlightBlock(self, block):
        """
        Reimplements the :meth:`QSyntaxHighlighter.highlightBlock` method.

        :param block: Text block.
        :type block: QString
        """

        raise NotImplementedError("{0} | '{1}' must be implemented by '{2}' subclasses!".format(self.__class__.__name__,
                                                                                                self.highlightBlock.__name__,
                                                                                                self.__class__.__name__))

    def highlight_text(self, text, start, end):
        """
        Highlights given text.

        :param text: Text.
        :type text: QString
        :param start: Text start index.
        :type start: int
        :param end: Text end index.
        :type end: int
        :return: Method success.
        :rtype: bool
        """

        for rule in self.__rules:
            index = rule.pattern.indexIn(text, start)
            while index >= start and index < end:
                length = rule.pattern.matchedLength()
                format = self.formats.get_format(rule.name) or self.formats.get_format("default")
                self.setFormat(index, min(length, end - index), format)
                index = rule.pattern.indexIn(text, index + length)
        return True


class DefaultHighlighter(AbstractHighlighter):
    """
    Defines a :class:`AbstractHighlighter` subclass providing syntax highlighting for documents.
    """

    def __init__(self, parent=None, rules=None, theme=None):
        """
        Initializes the class.

        :param parent: Widget parent.
        :type parent: QObject
        :param rules: Rules.
        :type rules: tuple or list
        :param theme: Theme.
        :type theme: dict
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        AbstractHighlighter.__init__(self, parent)

        # --- Setting class attributes. ---
        self.rules = rules
        self.__theme = None
        self.theme = theme

        self.__set_formats()

    @property
    def theme(self):
        """
        Property for **self.__theme** attribute.

        :return: self.__theme.
        :rtype: dict
        """

        return self.__theme

    @theme.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def theme(self, value):
        """
        Setter for **self.__theme** attribute.

        :param value: Attribute value.
        :type value: dict
        """

        if value is not None:
            assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("theme", value)
        self.__theme = value

    @theme.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def theme(self):
        """
        Deleter for **self.__theme** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "theme"))

    def __set_formats(self):
        """
        Sets the highlighting formats.
        """

        self.formats = FormatsTree(self.__theme)

    def highlightBlock(self, block):
        """
        Reimplements the :meth:`AbstractHighlighter.highlightBlock` method.

        :param block: Text block.
        :type block: QString
        """

        self.highlight_text(block, 0, len(block))
        self.setCurrentBlockState(0)

        state = 1
        for rule in self.rules:
            if re.match("comment\.block\.[\w\.]*start", rule.name):
                format = self.formats.get_format(rule.name) or self.formats.get_format("default")
                if self.highlight_multiline_block(block, rule.pattern,
                                                  foundations.common.get_first_item([item for item in self.rules
                                                                                     if item.name == rule.name.replace(
                                                              "start", "end")]).pattern, state, format):
                    break
                state += 1

    def highlight_multiline_block(self, block, start_pattern, end_pattern, state, format):
        """
        Highlights given multiline text block.

        :param block: Text block.
        :type block: QString
        :param pattern: Start regex pattern.
        :type pattern: QRegExp
        :param pattern: End regex pattern.
        :type pattern: QRegExp
        :param format: Format.
        :type format: QTextCharFormat
        :param state: Block state.
        :type state: int
        :return: Current block matching state.
        :rtype: bool
        """

        if self.previousBlockState() == state:
            start = 0
            extend = 0
        else:
            start = start_pattern.indexIn(block)
            extend = start_pattern.matchedLength()

        while start >= 0:
            end = end_pattern.indexIn(block, start + extend)
            if end >= extend:
                length = end - start + extend + end_pattern.matchedLength()
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(state)
                length = block.length() - start + extend
            self.setFormat(start, length, format)
            start = start_pattern.indexIn(block, start + length)

        if self.currentBlockState() == state:
            return True
        else:
            return False
