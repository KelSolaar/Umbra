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

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import re
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QTextCursor

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

__all__ = ["LOGGER",
			"getEditorCapability",
			"indentationPreEventInputAccelerators",
			"indentationPostEventInputAccelerators",
			"performCompletion",
			"completionPreEventInputAccelerators",
			"completionPostEventInputAccelerators",
			"symbolsExpandingPreEventInputAccelerators"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getEditorCapability(editor, capability):
	"""
	This definition returns given editor capability.
	
	:param editor: Document editor. ( QWidget )
	:param capability: Capability to retrieve. ( String )
	:return: Capability. ( Object )
	"""

	if not hasattr(editor, "language"):
		return

	return editor.language.get(capability)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def indentationPreEventInputAccelerators(editor, event):
	"""
	This definition implements indentation pre event input accelerators.
	
	:param editor: Document editor. ( QWidget )
	:param event: Event being handled. ( QEvent )
	:return: Process event. ( Boolean )
	"""

	processEvent = True
	if not hasattr(editor, "indent") and hasattr(editor, "unindent"):
		return processEvent

	if event.key() == Qt.Key_Tab:
		processEvent = editor.indent() and False
	elif event.key() == Qt.Key_Backtab:
		processEvent = editor.unindent() and False
	return processEvent

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def indentationPostEventInputAccelerators(editor, event):
	"""
	This definition implements indentation post event input accelerators.
	
	:param editor: Document editor. ( QWidget )
	:param event: Event being handled. ( QEvent )
	:return: Method success. ( Boolean )
	"""

	if event.key() in (Qt.Key_Enter, Qt.Key_Return):
		cursor = editor.textCursor()
		block = cursor.block().previous()
		if block.isValid():
			indent = re.match(r"(\s*)", unicode(block.text())).group(1)
			indentationSymbols = getEditorCapability(editor, "indentationSymbols")
			if indentationSymbols:
				for symbol in indentationSymbols:
					if unicode(block.text(), Constants.encodingFormat, Constants.encodingError).endswith(symbol):
						indent += editor.indentMarker
			cursor.insertText(indent)
	return True

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def performCompletion(editor):
	"""
	This definition performs the completion on given editor.

	:param editor: Document editor. ( QWidget )
	:return: Process event. ( Boolean )
	"""

	completionPrefix = editor.getWordUnderCursor()
	if completionPrefix.length() >= 1 :
		words = editor.getWords()
		completionPrefix in words and words.remove(completionPrefix)
		editor.completer.updateModel(words)
		editor.completer.setCompletionPrefix(completionPrefix)
		if editor.completer.completionCount() == 1:
			completion = editor.completer.completionModel().data(
						editor.completer.completionModel().index(0, 0)).toString()
			cursor = editor.textCursor()
			if completionPrefix != editor.getWordUnderCursorLegacy():
				cursor.movePosition(QTextCursor.PreviousWord, QTextCursor.MoveAnchor)
			cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.MoveAnchor)
			cursor.insertText(completion[len(completionPrefix):])
			editor.setTextCursor(cursor)
		else:
			popup = editor.completer.popup()
			popup.setCurrentIndex(editor.completer.completionModel().index(0, 0))

			completerRectangle = editor.cursorRect()
			hasattr(editor, "marginArea_LinesNumbers_widget") and completerRectangle.moveTo(
			completerRectangle.topLeft().x() + editor.marginArea_LinesNumbers_widget.getWidth(),
			completerRectangle.topLeft().y())
			completerRectangle.setWidth(editor.completer.popup().sizeHintForColumn(0) + \
			editor.completer.popup().verticalScrollBar().sizeHint().width())
			editor.completer.complete(completerRectangle)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def completionPreEventInputAccelerators(editor, event):
	"""
	This definition implements completion pre event input accelerators.

	:param editor: Document editor. ( QWidget )
	:param event: Event being handled. ( QEvent )
	:return: Process event. ( Boolean )
	"""

	processEvent = True

	if editor.completer:
		if editor.completer.popup().isVisible():
			if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
				event.ignore()
				processEvent = False
				return processEvent

	if event.modifiers() in (Qt.ControlModifier, Qt.MetaModifier) and event.key() == Qt.Key_Space:
		processEvent = False
		if not editor.completer:
			return processEvent

		performCompletion(editor)

	return processEvent

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def completionPostEventInputAccelerators(editor, event):
	"""
	This definition implements completion post event input accelerators.

	:param editor: Document editor. ( QWidget )
	:param event: Event being handled. ( QEvent )	
	:return: Process event. ( Boolean )
	"""

	if editor.completer:
		if editor.completer.popup().isVisible():
			performCompletion(editor)
	return True

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def symbolsExpandingPreEventInputAccelerators(editor, event):
	"""
	This definition implements symbols expanding pre event input accelerators.

	:param editor: Document editor. ( QWidget )
	:param event: Event being handled. ( QEvent )
	:return: Process event. ( Boolean )
	"""

	processEvent = True

	symbolsPairs = getEditorCapability(editor, "symbolsPairs")
	if not symbolsPairs:
		return processEvent

	text = unicode(event.text(), Constants.encodingFormat, Constants.encodingError)
	if text in symbolsPairs:
		cursor = editor.textCursor()
		cursor.beginEditBlock()
		if not cursor.hasSelection():
			cursor.insertText(event.text())
			cursor.insertText(symbolsPairs[text])
			cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor)
		else:
			selectionText = cursor.selectedText()
			cursor.insertText(event.text())
			cursor.insertText(selectionText)
			cursor.insertText(symbolsPairs[text])
		editor.setTextCursor(cursor)
		cursor.endEditBlock()
		processEvent = False

	if event.key() in (Qt.Key_Backspace,):
		cursor = editor.textCursor()
		cursor.beginEditBlock()
		cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)
		leftText = cursor.selectedText()
		for i in range(2):
			cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
		rightText = cursor.selectedText()

		if symbolsPairs.get(unicode(leftText, Constants.encodingFormat, Constants.encodingError)) == \
		unicode(rightText, Constants.encodingFormat, Constants.encodingError):
			cursor.deleteChar()
		cursor.endEditBlock()
	return processEvent
