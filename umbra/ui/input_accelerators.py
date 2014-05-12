#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**input_accelerators.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the Application input accelerators objects.

**Others:**
"""

from __future__ import unicode_literals

import re
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QTextCursor

import foundations.common
import foundations.strings
import foundations.verbose

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
           "get_editor_capability",
           "is_symbols_pair_complete",
           "perform_completion",
           "indentation_pre_event_input_accelerators",
           "indentation_post_event_input_accelerators",
           "completion_pre_event_input_accelerators",
           "completion_post_event_input_accelerators",
           "symbols_expanding_pre_event_input_accelerators"]

LOGGER = foundations.verbose.install_logger()


def get_editor_capability(editor, capability):
    """
    Returns given editor capability.

    :param editor: Document editor.
    :type editor: QWidget
    :param capability: Capability to retrieve.
    :type capability: unicode
    :return: Capability.
    :rtype: object
    """

    if not hasattr(editor, "language"):
        return

    return editor.language.get(capability)


def is_symbols_pair_complete(editor, symbol):
    """
    Returns if the symbols pair is complete on current editor line.

    :param editor: Document editor.
    :type editor: QWidget
    :param symbol: Symbol to check.
    :type symbol: unicode
    :return: Is symbols pair complete.
    :rtype: bool
    """

    symbols_pairs = get_editor_capability(editor, "symbols_pairs")
    if not symbols_pairs:
        return

    cursor = editor.textCursor()
    cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
    cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
    selected_text = foundations.strings.to_string(cursor.selectedText())
    if symbol == symbols_pairs[symbol]:
        return selected_text.count(symbol) % 2 == 0
    else:
        return selected_text.count(symbol) == selected_text.count(symbols_pairs[symbol])


def perform_completion(editor):
    """
    Performs the completion on given editor.

    :param editor: Document editor.
    :type editor: QWidget
    :return: Method success.
    :rtype: bool
    """

    completion_prefix = editor.get_partial_word_under_cursor()
    if not completion_prefix:
        return

    words = editor.get_words()
    completion_prefix in words and words.remove(completion_prefix)
    editor.completer.update_model(words)
    editor.completer.setCompletionPrefix(completion_prefix)
    if editor.completer.completionCount() == 1:
        completion = editor.completer.completionModel().data(
            editor.completer.completionModel().index(0, 0)).toString()
        cursor = editor.textCursor()
        cursor.insertText(completion[len(completion_prefix):])
        editor.setTextCursor(cursor)
    else:
        popup = editor.completer.popup()
        popup.setCurrentIndex(editor.completer.completionModel().index(0, 0))

        completer_rectangle = editor.cursorRect()
        hasattr(editor, "margin_area_LinesNumbers_widget") and completer_rectangle.moveTo(
            completer_rectangle.topLeft().x() + editor.margin_area_LinesNumbers_widget.get_width(),
            completer_rectangle.topLeft().y())
        completer_rectangle.setWidth(editor.completer.popup().sizeHintForColumn(0) +
                                     editor.completer.popup().verticalScrollBar().sizeHint().width())
        editor.completer.complete(completer_rectangle)
    return True


def indentation_pre_event_input_accelerators(editor, event):
    """
    Implements indentation pre event input accelerators.

    :param editor: Document editor.
    :type editor: QWidget
    :param event: Event being handled.
    :type event: QEvent
    :return: Process event.
    :rtype: bool
    """

    process_event = True
    if not hasattr(editor, "indent"):
        return process_event

    if event.key() == Qt.Key_Tab:
        process_event = editor.indent() and False
    elif event.key() == Qt.Key_Backtab:
        process_event = editor.unindent() and False
    return process_event


def indentation_post_event_input_accelerators(editor, event):
    """
    Implements indentation post event input accelerators.

    :param editor: Document editor.
    :type editor: QWidget
    :param event: Event being handled.
    :type event: QEvent
    :return: Method success.
    :rtype: bool
    """

    if event.key() in (Qt.Key_Enter, Qt.Key_Return):
        cursor = editor.textCursor()
        block = cursor.block().previous()
        if block.isValid():
            indent = match = re.match(r"(\s*)", foundations.strings.to_string(block.text())).group(1)
            cursor.insertText(indent)

            indentation_symbols = get_editor_capability(editor, "indentation_symbols")
            if not indentation_symbols:
                return True

            if not block.text():
                return True

            if not foundations.strings.to_string(block.text())[-1] in indentation_symbols:
                return True

            symbols_pairs = get_editor_capability(editor, "symbols_pairs")
            if not symbols_pairs:
                return True

            cursor.insertText(editor.indent_marker)

            position = cursor.position()
            cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
            previous_character = foundations.strings.to_string(cursor.selectedText())
            cursor.setPosition(position)
            next_character = editor.get_next_character()
            if previous_character in symbols_pairs:
                if next_character in symbols_pairs.values():
                    cursor.insertBlock()
                    cursor.insertText(match)
                    cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor)
                    cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)
                    editor.setTextCursor(cursor)
    return True


def completion_pre_event_input_accelerators(editor, event):
    """
    Implements completion pre event input accelerators.

    :param editor: Document editor.
    :type editor: QWidget
    :param event: Event being handled.
    :type event: QEvent
    :return: Process event.
    :rtype: bool
    """

    process_event = True

    if editor.completer:
        # TODO: Investigate the slowdown on popup visibility test.
        if editor.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                event.ignore()
                process_event = False
                return process_event

    if event.modifiers() in (Qt.ControlModifier, Qt.MetaModifier) and event.key() == Qt.Key_Space:
        process_event = False
        if not editor.completer:
            return process_event

        perform_completion(editor)

    return process_event


def completion_post_event_input_accelerators(editor, event):
    """
    Implements completion post event input accelerators.

    :param editor: Document editor.
    :type editor: QWidget
    :param event: Event being handled.
    :type event: QEvent
    :return: Process event.
    :rtype: bool
    """

    if editor.completer:
        if editor.completer.popup().isVisible():
            perform_completion(editor)
    return True


def symbols_expanding_pre_event_input_accelerators(editor, event):
    """
    Implements symbols expanding pre event input accelerators.

    :param editor: Document editor.
    :type editor: QWidget
    :param event: Event being handled.
    :type event: QEvent
    :return: Process event.
    :rtype: bool
    """

    process_event = True

    symbols_pairs = get_editor_capability(editor, "symbols_pairs")
    if not symbols_pairs:
        return process_event

    text = foundations.strings.to_string(event.text())
    if text in symbols_pairs:
        cursor = editor.textCursor()
        if not is_symbols_pair_complete(editor, text):
            cursor.insertText(event.text())
        else:
            if not cursor.hasSelection():
                cursor.insertText(event.text())
                # TODO: Provide an efficient code alternative.
                # position = cursor.position()
                # cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
                # selected_text = foundations.strings.to_string(cursor.selectedText())
                # cursor.setPosition(position)
                # if not selected_text.strip():
                cursor.insertText(symbols_pairs[text])
                cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor)
            else:
                selected_text = cursor.selectedText()
                cursor.insertText(event.text())
                cursor.insertText(selected_text)
                cursor.insertText(symbols_pairs[text])
        editor.setTextCursor(cursor)
        process_event = False

    if event.key() in (Qt.Key_Backspace,):
        cursor = editor.textCursor()
        cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)
        left_text = cursor.selectedText()
        foundations.common.repeat(lambda: cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor), 2)
        right_text = cursor.selectedText()

        if symbols_pairs.get(foundations.strings.to_string(left_text)) == foundations.strings.to_string(right_text):
            cursor.deleteChar()
    return process_event
