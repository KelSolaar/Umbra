#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**inputAccelerators.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the Application input accelerators objects.

**Others:**
"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import re
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QTextCursor

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.strings
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

__all__ = ["LOGGER",
		"getEditorCapability",
		"isSymbolsPairComplete",
		"performCompletion",
		"indentationPreEventInputAccelerators",
		"indentationPostEventInputAccelerators",
		"completionPreEventInputAccelerators",
		"completionPostEventInputAccelerators",
		"symbolsExpandingPreEventInputAccelerators"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def getEditorCapability(editor, capability):
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

def isSymbolsPairComplete(editor, symbol):
	"""
	Returns if the symbols pair is complete on current editor line.

	:param editor: Document editor.
	:type editor: QWidget
	:param symbol: Symbol to check.
	:type symbol: unicode
	:return: Is symbols pair complete.
	:rtype: bool
	"""

	symbolsPairs = getEditorCapability(editor, "symbolsPairs")
	if not symbolsPairs:
		return

	cursor = editor.textCursor()
	cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
	cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
	selectedText = foundations.strings.toString(cursor.selectedText())
	if symbol == symbolsPairs[symbol]:
		return selectedText.count(symbol) % 2 == 0
	else:
		return selectedText.count(symbol) == selectedText.count(symbolsPairs[symbol])

def performCompletion(editor):
	"""
	Performs the completion on given editor.

	:param editor: Document editor.
	:type editor: QWidget
	:return: Method success.
	:rtype: bool
	"""

	completionPrefix = editor.getPartialWordUnderCursor()
	if not completionPrefix:
		return

	words = editor.getWords()
	completionPrefix in words and words.remove(completionPrefix)
	editor.completer.updateModel(words)
	editor.completer.setCompletionPrefix(completionPrefix)
	if editor.completer.completionCount() == 1:
		completion = editor.completer.completionModel().data(
					editor.completer.completionModel().index(0, 0)).toString()
		cursor = editor.textCursor()
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
	return True

def indentationPreEventInputAccelerators(editor, event):
	"""
	Implements indentation pre event input accelerators.
	
	:param editor: Document editor.
	:type editor: QWidget
	:param event: Event being handled.
	:type event: QEvent
	:return: Process event.
	:rtype: bool
	"""

	processEvent = True
	if not hasattr(editor, "indent"):
		return processEvent

	if event.key() == Qt.Key_Tab:
		processEvent = editor.indent() and False
	elif event.key() == Qt.Key_Backtab:
		processEvent = editor.unindent() and False
	return processEvent

def indentationPostEventInputAccelerators(editor, event):
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
			indent = match = re.match(r"(\s*)", foundations.strings.toString(block.text())).group(1)
			cursor.insertText(indent)

			indentationSymbols = getEditorCapability(editor, "indentationSymbols")
			if not indentationSymbols:
				return True

			if not block.text():
				return True

			if not foundations.strings.toString(block.text())[-1] in indentationSymbols:
				return True

			symbolsPairs = getEditorCapability(editor, "symbolsPairs")
			if not symbolsPairs:
				return True

			cursor.insertText(editor.indentMarker)

			position = cursor.position()
			cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor)
			cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)
			cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
			previousCharacter = foundations.strings.toString(cursor.selectedText())
			cursor.setPosition(position)
			nextCharacter = editor.getNextCharacter()
			if previousCharacter in symbolsPairs:
				if nextCharacter in symbolsPairs.values():
					cursor.insertBlock()
					cursor.insertText(match)
					cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor)
					cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)
					editor.setTextCursor(cursor)
	return True

def completionPreEventInputAccelerators(editor, event):
	"""
	Implements completion pre event input accelerators.

	:param editor: Document editor.
	:type editor: QWidget
	:param event: Event being handled.
	:type event: QEvent
	:return: Process event.
	:rtype: bool
	"""

	processEvent = True

	if editor.completer:
		# TODO: Investigate the slowdown on popup visibility test.
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

def completionPostEventInputAccelerators(editor, event):
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
			performCompletion(editor)
	return True

def symbolsExpandingPreEventInputAccelerators(editor, event):
	"""
	Implements symbols expanding pre event input accelerators.

	:param editor: Document editor.
	:type editor: QWidget
	:param event: Event being handled.
	:type event: QEvent
	:return: Process event.
	:rtype: bool
	"""

	processEvent = True

	symbolsPairs = getEditorCapability(editor, "symbolsPairs")
	if not symbolsPairs:
		return processEvent

	text = foundations.strings.toString(event.text())
	if text in symbolsPairs:
		cursor = editor.textCursor()
		if not isSymbolsPairComplete(editor, text):
			cursor.insertText(event.text())
		else:
			if not cursor.hasSelection():
				cursor.insertText(event.text())
				# TODO: Provide an efficient code alternative.
				# position = cursor.position()
				# cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
				# selectedText = foundations.strings.toString(cursor.selectedText())
				# cursor.setPosition(position)
				# if not selectedText.strip():
				cursor.insertText(symbolsPairs[text])
				cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor)
			else:
				selectionText = cursor.selectedText()
				cursor.insertText(event.text())
				cursor.insertText(selectionText)
				cursor.insertText(symbolsPairs[text])
		editor.setTextCursor(cursor)
		processEvent = False

	if event.key() in (Qt.Key_Backspace,):
		cursor = editor.textCursor()
		cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor)
		leftText = cursor.selectedText()
		foundations.common.repeat(lambda: cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor), 2)
		rightText = cursor.selectedText()

		if symbolsPairs.get(foundations.strings.toString(leftText)) == foundations.strings.toString(rightText):
			cursor.deleteChar()
	return processEvent
