#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**codeEditor_QPlainTextEdit.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    | Defines the :class:`LinesNumbers_QWidget` and :class:`CodeEditor_QPlainTextEdit` classes.
    | Those objects provides the basics building blocks of a code editor widget.

**Others:**
    Portions of the code from codeeditor.py by Roberto Alsina: http://lateral.netmanagers.com.ar/weblog/posts/BB832.html,
    KhtEditor.py by Benoit Hervier: http://khertan.net/khteditor, Ninja IDE: http://ninja-ide.org/ and
    Prymatex: https://github.com/D3f0/prymatex/
"""

from __future__ import unicode_literals

import re
from PyQt4.QtCore import QSize
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QBrush
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QCompleter
from PyQt4.QtGui import QFontMetrics
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QPen
from PyQt4.QtGui import QSyntaxHighlighter
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextDocument
from PyQt4.QtGui import QWidget

import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.ui.common
import umbra.ui.languages
from umbra.ui.widgets.basic_QPlainTextEdit import Basic_QPlainTextEdit
from umbra.ui.widgets.basic_QPlainTextEdit import edit_block
from umbra.ui.widgets.basic_QPlainTextEdit import anchor_text_cursor

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "LinesNumbers_QWidget",
           "CodeEditor_QPlainTextEdit"]

LOGGER = foundations.verbose.install_logger()


class LinesNumbers_QWidget(QWidget):
    """
    Defines a `QWidget <http://doc.qt.nokia.com/qwidget.html>`_ subclass providing a lines numbers widget.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initializes the class.

        :param parent: Object parent.
        :type parent: QObject
        :param \*args: Arguments.
        :type \*args: \*
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        QWidget.__init__(self, parent, *args, **kwargs)

        # --- Setting class attributes. ---
        self.__editor = parent

        self.__margin = 16
        self.__separator_width = 4
        self.__background_color = QColor(48, 48, 48)
        self.__color = QColor(192, 192, 192)
        self.__separator_color = QColor(48, 48, 48)

        self.set_editor_viewport_margins(0)

    @property
    def editor(self):
        """
        Property for **self.__editor** attribute.

        :return: self.__editor.
        :rtype: QWidget
        """

        return self.__editor

    @editor.setter
    def editor(self, value):
        """
        Setter for **self.__editor** attribute.

        :param value: Attribute value.
        :type value: QWidget
        """

        self.__editor = value

    @editor.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def editor(self):
        """
        Deleter for **self.__editor** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "editor"))

    @property
    def margin(self):
        """
        Property for **self.__margin** attribute.

        :return: self.__margin.
        :rtype: int
        """

        return self.__margin

    @margin.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def margin(self, value):
        """
        Setter for **self.__margin** attribute.

        :param value: Attribute value.
        :type value: int
        """

        if value is not None:
            assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("margin", value)
            assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("margin", value)
        self.__margin = value

    @margin.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def margin(self):
        """
        Deleter for **self.__margin** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "margin"))

    @property
    def separator_width(self):
        """
        Property for **self.__separator_width** attribute.

        :return: self.__separator_width.
        :rtype: int
        """

        return self.__separator_width

    @separator_width.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def separator_width(self, value):
        """
        Setter for **self.__separator_width** attribute.

        :param value: Attribute value.
        :type value: int
        """

        if value is not None:
            assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("separator_width", value)
            assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("separator_width", value)
        self.__separator_width = value

    @separator_width.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def separator_width(self):
        """
        Deleter for **self.__separator_width** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "separator_width"))

    @property
    def background_color(self):
        """
        Property for **self.__background_color** attribute.

        :return: self.__background_color.
        :rtype: QColor
        """

        return self.__background_color

    @background_color.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def background_color(self, value):
        """
        Setter for **self.__background_color** attribute.

        :param value: Attribute value.
        :type value: QColor
        """

        if value is not None:
            assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format(
                "background_color", value)
        self.__background_color = value

    @background_color.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def background_color(self):
        """
        Deleter for **self.__background_color** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "background_color"))

    @property
    def color(self):
        """
        Property for **self.__color** attribute.

        :return: self.__color.
        :rtype: QColor
        """

        return self.__color

    @color.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def color(self, value):
        """
        Setter for **self.__color** attribute.

        :param value: Attribute value.
        :type value: QColor
        """

        if value is not None:
            assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("color", value)
        self.__color = value

    @color.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def color(self):
        """
        Deleter for **self.__color** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "color"))

    @property
    def separator_color(self):
        """
        Property for **self.__separator_color** attribute.

        :return: self.__separator_color.
        :rtype: QColor
        """

        return self.__separator_color

    @separator_color.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def separator_color(self, value):
        """
        Setter for **self.__separator_color** attribute.

        :param value: Attribute value.
        :type value: QColor
        """

        if value is not None:
            assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format(
                "separator_color", value)
        self.__separator_color = value

    @separator_color.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def separator_color(self):
        """
        Deleter for **self.__separator_color** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "separator_color"))

    def sizeHint(self):
        """
        Reimplements the :meth:`QWidget.sizeHint` method.

        :return: Size hint.
        :rtype: QSize
        """

        return QSize(self.get_width(), 0)

    def paintEvent(self, event):
        """
        Reimplements the :meth:`QWidget.paintEvent` method.

        :param event: Event.
        :type event: QEvent
        """

        def __set_bold(state):
            """
            Sets the current painter font bold state.

            :return: Definiton success.
            :rtype: bool
            """

            font = painter.font()
            font.setBold(state)
            painter.setFont(font)
            return True

        painter = QPainter(self)
        painter.fillRect(event.rect(), self.__background_color)

        pen = QPen(QBrush(), self.__separator_width)
        pen.setColor(self.__separator_color)
        painter.setPen(pen)
        top_right_corner = event.rect().topRight()
        bottom_right_corner = event.rect().bottomRight()
        painter.drawLine(top_right_corner.x(), top_right_corner.y(), bottom_right_corner.x(), bottom_right_corner.y())
        painter.setPen(self.__color)

        viewport_height = self.__editor.viewport().height()
        metrics = QFontMetrics(self.__editor.document().defaultFont())
        current_block = self.__editor.document().findBlock(
            self.__editor.textCursor().position())

        block = self.__editor.firstVisibleBlock()
        block_number = block.blockNumber()
        painter.setFont(self.__editor.document().defaultFont())

        while block.isValid():
            block_number += 1
            position = self.__editor.blockBoundingGeometry(block).topLeft() + self.__editor.contentOffset()
            if position.y() > viewport_height:
                break

            if not block.isVisible():
                continue

            block == current_block and __set_bold(True) or __set_bold(False)
            painter.drawText(
                self.width() - metrics.width(foundations.strings.to_string(block_number)) - self.__margin / 3,
                round(position.y() + metrics.ascent() + metrics.descent() -
                      (self.__editor.blockBoundingRect(block).height() * 8.0 / 100)),
                foundations.strings.to_string(block_number))
            block = block.next()

        painter.end()
        QWidget.paintEvent(self, event)

    def get_width(self):
        """
        Returns the Widget target width.

        :return: Widget target width.
        :rtype: int
        """

        return self.__margin + \
               self.__editor.fontMetrics().width(foundations.strings.to_string(max(1, self.__editor.blockCount())))

    def set_editor_viewport_margins(self, newBlocksCount):
        """
        Sets the editor viewport margins.

        :param newBlocksCount: Updated editor blocks count.
        :type newBlocksCount: int
        :return: Method success.
        :rtype: bool
        """

        self.__editor.setViewportMargins(self.get_width(), 0, 0, 0)
        return True

    def update_rectangle(self, rectangle, scroll_y):
        """
        Updates the given Widget rectangle.

        :param rectangle: Rectangle to update.
        :type rectangle: QRect
        :param scroll_y: Amount of pixels the viewport was scrolled.
        :type scroll_y: int
        :return: Method success.
        :rtype: bool
        """

        if scroll_y:
            self.scroll(0, scroll_y)
        else:
            self.update(0, rectangle.y(), self.width(), rectangle.height())

        if rectangle.contains(self.__editor.viewport().rect()):
            self.set_editor_viewport_margins(0)
        return True

    def update_geometry(self):
        """
        Updates the Widget geometry.

        :return: Method success.
        :rtype: bool
        """

        self.setGeometry(self.__editor.contentsRect().left(),
                         self.__editor.contentsRect().top(),
                         self.get_width(),
                         self.__editor.contentsRect().height())
        return True


class CodeEditor_QPlainTextEdit(Basic_QPlainTextEdit):
    """
    Defines	a code editor base class.
    """

    language_changed = pyqtSignal()
    """
    This signal is emited by the :class:`Editor` class when :obj:`ComponentsManagerUi.language` class property language
    is changed.
    """

    def __init__(self,
                 parent=None,
                 language=umbra.ui.languages.PYTHON_LANGUAGE,
                 indent_marker=" " * 4,
                 indent_width=4,
                 comment_marker="#",
                 *args,
                 **kwargs):
        """
        Initializes the class.

        :param parent: Widget parent.
        :type parent: QObject
        :param language: Editor language.
        :type language: Language
        :param indent_marker: Indentation marker.
        :type indent_marker: unicode
        :param indent_width: Indentation spaces count.
        :type indent_width: int
        :param comment_marker: Comment marker.
        :type comment_marker: unicode
        :param \*args: Arguments.
        :type \*args: \*
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        Basic_QPlainTextEdit.__init__(self, parent, *args, **kwargs)

        # --- Setting class attributes. ---
        self.__language = language

        self.__indent_marker = None
        self.indent_marker = indent_marker
        self.__indent_width = None
        self.indent_width = indent_width
        self.__comment_marker = None
        self.comment_marker = comment_marker

        self.__margin_area_LinesNumbers_widget = None
        self.__highlighter = None
        self.__completer = None

        self.__occurrences_highlight_color = QColor(80, 80, 80)

        self.__pre_input_accelerators = []
        self.__post_input_accelerators = []
        self.__visual_accelerators = []

        self.__text_cursor_anchor = None

        CodeEditor_QPlainTextEdit.__initialize_ui(self)

    @property
    def language(self):
        """
        Property for **self.__language** attribute.

        :return: self.__language.
        :rtype: Language
        """

        return self.__language

    @language.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def language(self, value):
        """
        Setter for **self.__language** attribute.

        :param value: Attribute value.
        :type value: Language
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "language"))

    @language.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def language(self):
        """
        Deleter for **self.__language** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "language"))

    @property
    def indent_marker(self):
        """
        Property for **self.__indent_marker** attribute.

        :return: self.__indent_marker.
        :rtype: unicode
        """

        return self.__indent_marker

    @indent_marker.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def indent_marker(self, value):
        """
        Setter for **self.__indent_marker** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
                "indent_marker", value)
            assert re.search(r"\s", value), "'{0}' attribute: '{1}' is not a whitespace character!".format(
                "indent_marker", value)
        self.__indent_marker = value

    @indent_marker.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def indent_marker(self):
        """
        Deleter for **self.__indent_marker** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "indent_marker"))

    @property
    def indent_width(self):
        """
        Property for **self.__indent_width** attribute.

        :return: self.__indent_width.
        :rtype: int
        """

        return self.__indent_width

    @indent_width.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def indent_width(self, value):
        """
        Setter for **self.__indent_width** attribute.

        :param value: Attribute value.
        :type value: int
        """

        if value is not None:
            assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("indent_width", value)
        self.__indent_width = value

    @indent_width.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def indent_width(self):
        """
        Deleter for **self.__indent_width** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "indent_width"))

    @property
    def comment_marker(self):
        """
        Property for **self.__comment_marker** attribute.

        :return: self.__comment_marker.
        :rtype: unicode
        """

        return self.__comment_marker

    @comment_marker.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def comment_marker(self, value):
        """
        Setter for **self.__comment_marker** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
                "comment_marker", value)
        self.__comment_marker = value

    @comment_marker.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def comment_marker(self):
        """
        Deleter for **self.__comment_marker** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "comment_marker"))

    @property
    def margin_area_LinesNumbers_widget(self):
        """
        Property for **self.__margin_area_LinesNumbers_widget** attribute.

        :return: self.__margin_area_LinesNumbers_widget.
        :rtype: LinesNumbers_QWidget
        """

        return self.__margin_area_LinesNumbers_widget

    @margin_area_LinesNumbers_widget.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def margin_area_LinesNumbers_widget(self, value):
        """
        Setter for **self.__margin_area_LinesNumbers_widget** attribute.

        :param value: Attribute value.
        :type value: LinesNumbers_QWidget
        """

        if value is not None:
            assert type(value) is LinesNumbers_QWidget, \
                "'{0}' attribute: '{1}' type is not 'LinesNumbers_QWidget'!".format("checked", value)
        self.__margin_area_LinesNumbers_widget = value

    @margin_area_LinesNumbers_widget.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def margin_area_LinesNumbers_widget(self):
        """
        Deleter for **self.__margin_area_LinesNumbers_widget** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__,
                                                             "margin_area_LinesNumbers_widget"))

    @property
    def highlighter(self):
        """
        Property for **self.__highlighter** attribute.

        :return: self.__highlighter.
        :rtype: QSyntaxHighlighter
        """

        return self.__highlighter

    @highlighter.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def highlighter(self, value):
        """
        Setter for **self.__highlighter** attribute.

        :param value: Attribute value.
        :type value: QSyntaxHighlighter
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "highlighter"))

    @highlighter.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def highlighter(self):
        """
        Deleter for **self.__highlighter** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "highlighter"))

    @property
    def completer(self):
        """
        Property for **self.__completer** attribute.

        :return: self.__completer.
        :rtype: QCompleter
        """

        return self.__completer

    @completer.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def completer(self, value):
        """
        Setter for **self.__completer** attribute.

        :param value: Attribute value.
        :type value: QCompleter
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "completer"))

    @completer.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def completer(self):
        """
        Deleter for **self.__completer** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "completer"))

    @property
    def pre_input_accelerators(self):
        """
        Property for **self.__pre_input_accelerators** attribute.

        :return: self.__pre_input_accelerators.
        :rtype: tuple or list
        """

        return self.__pre_input_accelerators

    @pre_input_accelerators.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def pre_input_accelerators(self, value):
        """
        Setter for **self.__pre_input_accelerators** attribute.

        :param value: Attribute value.
        :type value: tuple or list
        """

        if value is not None:
            assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
                "pre_input_accelerators", value)
        self.__pre_input_accelerators = value

    @pre_input_accelerators.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def pre_input_accelerators(self):
        """
        Deleter for **self.__pre_input_accelerators** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "pre_input_accelerators"))

    @property
    def post_input_accelerators(self):
        """
        Property for **self.__post_input_accelerators** attribute.

        :return: self.__post_input_accelerators.
        :rtype: tuple or list
        """

        return self.__post_input_accelerators

    @post_input_accelerators.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def post_input_accelerators(self, value):
        """
        Setter for **self.__post_input_accelerators** attribute.

        :param value: Attribute value.
        :type value: tuple or list
        """

        if value is not None:
            assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
                "post_input_accelerators", value)
        self.__post_input_accelerators = value

    @post_input_accelerators.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def post_input_accelerators(self):
        """
        Deleter for **self.__post_input_accelerators** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "post_input_accelerators"))

    @property
    def visual_accelerators(self):
        """
        Property for **self.__visual_accelerators** attribute.

        :return: self.__visual_accelerators.
        :rtype: tuple or list
        """

        return self.__visual_accelerators

    @visual_accelerators.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def visual_accelerators(self, value):
        """
        Setter for **self.__visual_accelerators** attribute.

        :param value: Attribute value.
        :type value: tuple or list
        """

        if value is not None:
            assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
                "visual_accelerators", value)
        self.__visual_accelerators = value

    @visual_accelerators.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def visual_accelerators(self):
        """
        Deleter for **self.__visual_accelerators** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "visual_accelerators"))

    def __initialize_ui(self):
        """
        Initializes the Widget ui.
        """

        self.__margin_area_LinesNumbers_widget = LinesNumbers_QWidget(self)

        self.__set_extra_selections()

        self.__set_language_description()

        # Signals / Slots.
        self.blockCountChanged.connect(self.__margin_area_LinesNumbers_widget.set_editor_viewport_margins)
        self.updateRequest.connect(self.__margin_area_LinesNumbers_widget.update_rectangle)
        self.cursorPositionChanged.connect(self.__set_extra_selections)

    def resizeEvent(self, event):
        """
        Reimplements the :meth:`Basic_QPlainTextEdit.resizeEvent` method.

        :param event: Event.
        :type event: QEvent
        """

        Basic_QPlainTextEdit.resizeEvent(self, event)
        self.__margin_area_LinesNumbers_widget.update_geometry()

    @edit_block
    def keyPressEvent(self, event):
        """
        Reimplements the :meth:`Basic_QPlainTextEdit.keyPressEvent` method.

        :param event: Event.
        :type event: QEvent
        """

        processEvent = True
        for accelerator in self.__pre_input_accelerators:
            processEvent *= accelerator(self, event)

        if not processEvent:
            return

        Basic_QPlainTextEdit.keyPressEvent(self, event)

        for accelerator in self.__post_input_accelerators:
            accelerator(self, event)

    def __set_extra_selections(self):
        """
        Sets current document extra selections.
        """

        self.setExtraSelections(())
        for accelerator in self.__visual_accelerators:
            accelerator(self)

    def __insert_completion(self, completion):
        """
        Inserts the completion text in the current document.

        :param completion: Completion text.
        :type completion: QString
        """

        LOGGER.debug("> Inserting '{0}' completion.".format(completion))

        text_cursor = self.textCursor()
        extra = (completion.length() - self.__completer.completion_prefix().length())
        text_cursor.insertText(completion.right(extra))
        self.setTextCursor(text_cursor)

    def __set_language_description(self):
        """
        Sets the language accelerators.
        """

        LOGGER.debug("> Setting language description.")

        if not self.__language:
            return

        if self.__language.highlighter:
            self.set_highlighter(self.__language.highlighter(self.document(),
                                                             self.__language.rules,
                                                             self.__language.theme))
            self.highlighter.rehighlight()
        else:
            self.remove_highlighter()

        if self.__language.completer:
            self.set_completer(self.__language.completer(self.parent(), self.__language.name, self.__language.tokens))
        else:
            self.remove_completer()

        self.indent_marker = self.__language.indent_marker
        self.comment_marker = self.__language.comment_marker
        self.pre_input_accelerators = self.__language.pre_input_accelerators
        self.post_input_accelerators = self.__language.post_input_accelerators
        self.visual_accelerators = self.__language.visual_accelerators

        color = "rgb({0}, {1}, {2})"
        background = self.__language.theme.get("default").background()
        foreground = self.__language.theme.get("default").foreground()
        self.setStyleSheet(
            "QPlainTextEdit{{ background-color: {0}; color: {1}; }}".format(color.format(background.color().red(),
                                                                                         background.color().green(),
                                                                                         background.color().blue()),
                                                                            color.format(foreground.color().red(),
                                                                                         foreground.color().green(),
                                                                                         foreground.color().blue())))

        self.__tab_width = self.fontMetrics().width(" " * self.indent_width)
        self.setTabStopWidth(self.__tab_width)

    def set_language(self, language):
        """
        Sets the language.

        :param language: Language to set.
        :type language: Language
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Setting editor language to '{0}'.".format(language.name))
        self.__language = language or umbra.ui.languages.PYTHON_LANGUAGE
        self.__set_language_description()
        self.language_changed.emit()
        return True

    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def set_highlighter(self, highlighter):
        """
        Sets given highlighter as the current document highlighter.

        :param highlighter: Highlighter.
        :type highlighter: QSyntaxHighlighter
        :return: Method success.
        :rtype: bool
        """

        if not issubclass(highlighter.__class__, QSyntaxHighlighter):
            raise foundations.exceptions.ProgrammingError("{0} | '{1}' is not a 'QSyntaxHighlighter' subclass!".format(
                self.__class__.__name__, highlighter))

        if self.__highlighter:
            self.remove_highlighter()

        LOGGER.debug("> Setting '{0}' highlighter.".format(highlighter))
        self.__highlighter = highlighter

        return True

    def remove_highlighter(self):
        """
        Removes current highlighter.

        :return: Method success.
        :rtype: bool
        """

        if self.__highlighter:
            LOGGER.debug("> Removing '{0}' highlighter.".format(self.__highlighter))
            self.__highlighter.deleteLater()
            self.__highlighter = None
        return True

    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def set_completer(self, completer):
        """
        Sets given completer as the current completer.

        :param completer: Completer.
        :type completer: QCompleter
        :return: Method success.
        :rtype: bool
        """

        if not issubclass(completer.__class__, QCompleter):
            raise foundations.exceptions.ProgrammingError("{0} | '{1}' is not a 'QCompleter' subclass!".format(
                self.__class__.__name__, completer))

        if self.__completer:
            self.remove_completer()

        LOGGER.debug("> Setting '{0}' completer.".format(completer))
        self.__completer = completer
        self.__completer.setWidget(self)

        # Signals / Slots.
        self.__completer.activated.connect(self.__insert_completion)

        return True

    def remove_completer(self):
        """
        Removes current completer.

        :return: Method success.
        :rtype: bool
        """

        if self.__completer:
            LOGGER.debug("> Removing '{0}' completer.".format(self.__completer))
            # Signals / Slots.
            self.__completer.activated.disconnect(self.__insert_completion)

            self.__completer.deleteLater()
            self.__completer = None
        return True

    def get_matching_symbols_pairs(self, cursor, opening_symbol, closing_symbol, backward=False):
        """
        Returns the cursor for matching given symbols pairs.

        :param cursor: Cursor to match from.
        :type cursor: QTextCursor
        :param opening_symbol: Opening symbol.
        :type opening_symbol: unicode
        :param closing_symbol: Closing symbol to match.
        :type closing_symbol: unicode
        :return: Matching cursor.
        :rtype: QTextCursor
        """

        if cursor.hasSelection():
            start_position = cursor.selectionEnd() if backward else cursor.selectionStart()
        else:
            start_position = cursor.position()

        flags = QTextDocument.FindFlags()
        if backward:
            flags = flags | QTextDocument.FindBackward

        start_cursor = previous_start_cursor = cursor.document().find(opening_symbol, start_position, flags)
        end_cursor = previous_end_cursor = cursor.document().find(closing_symbol, start_position, flags)
        if backward:
            while start_cursor > end_cursor:
                start_cursor = cursor.document().find(opening_symbol, start_cursor.selectionStart(), flags)
                if start_cursor > end_cursor:
                    end_cursor = cursor.document().find(closing_symbol, end_cursor.selectionStart(), flags)
        else:
            while start_cursor < end_cursor:
                start_cursor = cursor.document().find(opening_symbol, start_cursor.selectionEnd(), flags)
                if start_cursor < end_cursor:
                    end_cursor = cursor.document().find(closing_symbol, end_cursor.selectionEnd(), flags)

        return end_cursor if end_cursor.position() != -1 else previous_end_cursor

    @edit_block
    def indent(self):
        """
        Indents the document text under cursor.

        :return: Method success.
        :rtype: bool
        """

        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.insertText(self.__indent_marker)
        else:
            block = self.document().findBlock(cursor.selectionStart())
            while True:
                block_cursor = self.textCursor()
                block_cursor.setPosition(block.position())
                block_cursor.insertText(self.__indent_marker)
                if block.contains(cursor.selectionEnd()):
                    break
                block = block.next()
        return True

    @edit_block
    def unindent(self):
        """
        Unindents the document text under cursor.

        :return: Method success.
        :rtype: bool
        """

        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.movePosition(QTextCursor.StartOfBlock)
            line = foundations.strings.to_string(self.document().findBlockByNumber(cursor.blockNumber()).text())
            indent_marker = re.match(r"({0})".format(self.__indent_marker), line)
            if indent_marker:
                foundations.common.repeat(cursor.deleteChar, len(indent_marker.group(1)))
        else:
            block = self.document().findBlock(cursor.selectionStart())
            while True:
                block_cursor = self.textCursor()
                block_cursor.setPosition(block.position())
                indent_marker = re.match(r"({0})".format(self.__indent_marker), block.text())
                if indent_marker:
                    foundations.common.repeat(block_cursor.deleteChar, len(indent_marker.group(1)))
                if block.contains(cursor.selectionEnd()):
                    break
                block = block.next()
        return True

    @edit_block
    def toggle_comments(self):
        """
        Toggles comments on the document selected lines.

        :return: Method success.
        :rtype: bool
        """

        if not self.__comment_marker:
            return True

        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.movePosition(QTextCursor.StartOfBlock)
            line = foundations.strings.to_string(self.document().findBlockByNumber(cursor.blockNumber()).text())
            if line.startswith(self.__comment_marker):
                foundations.common.repeat(cursor.deleteChar, len(self.__comment_marker))
            else:
                cursor.insertText(self.__comment_marker)
        else:
            block = self.document().findBlock(cursor.selectionStart())
            while True:
                block_cursor = self.textCursor()
                block_cursor.setPosition(block.position())
                if foundations.strings.to_string(block.text()).startswith(self.__comment_marker):
                    foundations.common.repeat(block_cursor.deleteChar, len(self.__comment_marker))
                else:
                    block_cursor.insertText(self.__comment_marker)

                if block.contains(cursor.selectionEnd()):
                    break
                block = block.next()
        return True

    @anchor_text_cursor
    @edit_block
    def remove_trailing_white_spaces(self):
        """
        Removes document trailing white spaces.

        :return: Method success.
        :rtype: bool
        """

        cursor = self.textCursor()

        block = self.document().findBlockByLineNumber(0)
        while block.isValid():
            cursor.setPosition(block.position())
            if re.search(r"\s+$", block.text()):
                cursor.movePosition(QTextCursor.EndOfBlock)
                cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
                cursor.insertText(foundations.strings.to_string(block.text()).rstrip())
            block = block.next()
        cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
        if not cursor.block().text().isEmpty():
            cursor.insertText("\n")
        return True

    @anchor_text_cursor
    @edit_block
    def convert_indentation_to_tabs(self):
        """
        Converts document indentation to tabs.

        :return: Method success.
        :rtype: bool
        """

        cursor = self.textCursor()

        block = self.document().findBlockByLineNumber(0)
        while block.isValid():
            cursor.setPosition(block.position())
            search = re.match(r"^ +", block.text())
            if search:
                cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
                searchLength = len(search.group(0))
                foundations.common.repeat(
                    lambda: cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor), searchLength)
                cursor.insertText(self.__indent_marker * (searchLength / self.__indent_width))
            block = block.next()
        return True

    @anchor_text_cursor
    @edit_block
    def convert_indentation_to_spaces(self):
        """
        Converts document indentation to spaces.

        :return: Method success.
        :rtype: bool
        """

        cursor = self.textCursor()

        block = self.document().findBlockByLineNumber(0)
        while block.isValid():
            cursor.setPosition(block.position())
            search = re.match(r"^\t+", block.text())
            if search:
                cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
                searchLength = len(search.group(0))
                foundations.common.repeat(
                    lambda: cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor), searchLength)
                cursor.insertText(" " * (searchLength * self.__indent_width))
            block = block.next()
        return True


if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QGridLayout
    from PyQt4.QtGui import QLineEdit
    from PyQt4.QtGui import QPushButton

    from umbra.globals.constants import Constants

    application = umbra.ui.common.get_application_instance()

    widget = QWidget()

    grid_layout = QGridLayout()
    widget.setLayout(grid_layout)

    content = "\n".join(("import os",
                         "print os.getcwd()"))
    code_editor_QPlainTextEdit = CodeEditor_QPlainTextEdit()
    code_editor_QPlainTextEdit.set_content(content)
    grid_layout.addWidget(code_editor_QPlainTextEdit)

    line_edit = QLineEdit("code_editor_QPlainTextEdit.toggle_comments()")
    grid_layout.addWidget(line_edit)

    def _pushButton__clicked(*args):
        statement = unicode(line_edit.text(), Constants.default_codec, Constants.codec_error)
        exec (statement)

    push_button = QPushButton("Execute Statement")
    push_button.clicked.connect(_pushButton__clicked)
    grid_layout.addWidget(push_button)

    widget.show()
    widget.raise_()

    sys.exit(application.exec_())
