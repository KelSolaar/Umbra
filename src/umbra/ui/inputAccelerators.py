#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**inputAccelerators.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application input accelerators objects.

**Others:**
"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "DEFAULT_SYMBOLS_PAIRS", "indentationPreEventInputAccelerators", "performCompletion", "completionPreEventInputAccelerators", "completionPostEventInputAccelerators", "pythonPreEventInputAccelerators", "pythonPreEventInputAccelerators"]

LOGGER = logging.getLogger(Constants.logger)

DEFAULT_SYMBOLS_PAIRS = {"(" : ")",
						"[" : "]",
						"{" : "}",
						"\"" : "\"",
						"'" : "'"}

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
@core.executionTrace
def indentationPreEventInputAccelerators(container, event):
	"""
	This definition implements indentation pre event input accelerators.
	
	:return: Process event. ( Boolean )
	"""

	processEvent = True
	if not hasattr(container, "indent") and hasattr(container, "unindent"):
		return processEvent

	if event.key() == Qt.Key_Tab:
		processEvent = container.indent() and False
	elif event.key() == Qt.Key_Backtab:
		processEvent = container.unindent() and False
	return processEvent

@core.executionTrace
def performCompletion(container):
	"""
	This definition performs the completion on given container.
	
	:return: Process event. ( Boolean )
	"""

	completionPrefix = container.wordUnderCursor()
	if completionPrefix.length() >= 1 :
		words = container.getWords()
		completionPrefix in words and words.remove(completionPrefix)
		container.completer.updateModel(words)
		container.completer.setCompletionPrefix(completionPrefix)
		if container.completer.completionCount() == 1:
			completion = container.completer.completionModel().data(container.completer.completionModel().index(0, 0)).toString()
			cursor = container.textCursor()
			if completionPrefix != container.textUnderCursor():
				cursor.movePosition(QTextCursor.PreviousWord, QTextCursor.MoveAnchor)
			cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.MoveAnchor)
			cursor.insertText(completion[len(completionPrefix):])
			container.setTextCursor(cursor)
		else:
			popup = container.completer.popup()
			popup.setCurrentIndex(container.completer.completionModel().index(0, 0))

			completerRectangle = container.cursorRect()
			hasattr(container, "marginArea_LinesNumbers_widget") and completerRectangle.moveTo(completerRectangle.topLeft().x() + container.marginArea_LinesNumbers_widget.getWidth(), completerRectangle.topLeft().y())
			completerRectangle.setWidth(container.completer.popup().sizeHintForColumn(0) + container.completer.popup().verticalScrollBar().sizeHint().width())
			container.completer.complete(completerRectangle)

@core.executionTrace
def completionPreEventInputAccelerators(container, event):
	"""
	This definition implements completion pre event input accelerators.
	
	:return: Process event. ( Boolean )
	"""

	processEvent = True

	if container.completer:
		if container.completer.popup().isVisible():
			if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
				event.ignore()
				processEvent = False
				return processEvent

	if event.modifiers() in (Qt.ControlModifier, Qt.MetaModifier) and event.key() == Qt.Key_Space:
		processEvent = False
		if not container.completer:
			return processEvent

		performCompletion(container)

	return processEvent

@core.executionTrace
def completionPostEventInputAccelerators(container, event):
	"""
	This definition implements completion post event input accelerators.
	
	:return: Process event. ( Boolean )
	"""

	if container.completer:
		if container.completer.popup().isVisible():
			performCompletion(container)
	return True

@core.executionTrace
def symbolsExpandingPreEventInputAccelerators(container, event):
	"""
	This definition implements symbols expanding pre event input accelerators.
	
	:return: Process event. ( Boolean )
	"""

	processEvent = True
	if event.text() in DEFAULT_SYMBOLS_PAIRS.keys():
		cursor = container.textCursor()
		cursor.beginEditBlock()
		if not cursor.hasSelection():
			cursor.insertText(event.text())
			cursor.insertText(DEFAULT_SYMBOLS_PAIRS[unicode(event.text(), Constants.encodingFormat, Constants.encodingError)])
			cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor)
		else:
			selectionText = cursor.selectedText()
			cursor.insertText(event.text())
			cursor.insertText(selectionText)
			cursor.insertText(DEFAULT_SYMBOLS_PAIRS[unicode(event.text(), Constants.encodingFormat, Constants.encodingError)])
		container.setTextCursor(cursor)
		cursor.endEditBlock()
		processEvent = False

	if event.key() in (Qt.Key_Backspace,):
		cursor = container.textCursor()
		cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)
		leftText = cursor.selectedText()
		for i in range(2):
			cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
		rightText = cursor.selectedText()
		if not rightText:
			return processEvent

		if unicode(leftText, Constants.encodingFormat, Constants.encodingError) in DEFAULT_SYMBOLS_PAIRS.keys() and unicode(rightText, Constants.encodingFormat, Constants.encodingError) in DEFAULT_SYMBOLS_PAIRS.values():
			cursor.deleteChar()
	return processEvent

@core.executionTrace
def pythonPostEventInputAccelerators(container, event):
	"""
	This definition implements pythons post event input accelerators.
	
	:return: Method success. ( Boolean )
	"""

	if event.key() in (Qt.Key_Enter, Qt.Key_Return):
		cursor = container.textCursor()
		block = cursor.block().previous()
		if block.isValid():
			indent = re.match(r"(\s*)", unicode(block.text())).group(1)
			if unicode(block.text(), Constants.encodingFormat, Constants.encodingError).endswith(":"):
				indent += container.indentMarker
			cursor.insertText(indent)
	return True
