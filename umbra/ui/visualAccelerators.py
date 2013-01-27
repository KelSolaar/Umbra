#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**visualAccelerators.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application visual accelerators objects.

**Others:**
"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextDocument
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QTextFormat

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
#import foundations.exceptions
import foundations.strings
import foundations.verbose

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"highlightCurrentLine",
			"highlightOccurences",
			"highlightMatchingPairs"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def highlightCurrentLine(editor):
	"""
	This definition highlights given editor current line.
	
	:param editor: Document editor. ( QWidget )
	:return: Method success. ( Boolean )
	"""

	format = editor.language.theme.get("accelerator.line")
	if not format:
		return False

	extraSelections = editor.extraSelections() or []
	if not editor.isReadOnly():
		selection = QTextEdit.ExtraSelection()
		selection.format.setBackground(format.background())
		selection.format.setProperty(QTextFormat.FullWidthSelection, True)
		selection.cursor = editor.textCursor()
		selection.cursor.clearSelection()
		extraSelections.append(selection)
	editor.setExtraSelections(extraSelections)
	return True

def highlightOccurences(editor):
	"""
	This definition highlights given editor current line.
	
	:param editor: Document editor. ( QWidget )
	:return: Method success. ( Boolean )
	"""

	format = editor.language.theme.get("accelerator.occurence")
	if not format:
		return False

	extraSelections = editor.extraSelections() or []
	if not editor.isReadOnly():
		word = editor.getWordUnderCursor()
		if not word:
			return False

		block = editor.document().findBlock(0)
		cursor = editor.document().find(word,
									block.position(),
									QTextDocument.FindCaseSensitively | QTextDocument.FindWholeWords)
		while block.isValid() and cursor.position() != -1:
			selection = QTextEdit.ExtraSelection()
			selection.format.setBackground(format.background())
			selection.cursor = cursor
			extraSelections.append(selection)
			cursor = editor.document().find(word,
											cursor.position(),
											QTextDocument.FindCaseSensitively | QTextDocument.FindWholeWords)
			block = block.next()
	editor.setExtraSelections(extraSelections)
	return True

def highlightMatchingSymbolsPairs(editor):
	"""
	This definition highlights given editor matching pairs.
	
	:param editor: Document editor. ( QWidget )
	:return: Method success. ( Boolean )
	"""

	format = editor.language.theme.get("accelerator.pair")
	if not format:
		return False

	extraSelections = editor.extraSelections() or []
	if not editor.isReadOnly():
		startSelection = QTextEdit.ExtraSelection()
		startSelection.format.setBackground(format.background())
		endSelection = QTextEdit.ExtraSelection()
		endSelection.format.setBackground(format.background())

		cursor = editor.textCursor()
		if cursor.hasSelection():
			text = foundations.strings.encode(cursor.selectedText())
		else:
			cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
			text = foundations.strings.encode(cursor.selectedText())

		startSelection.cursor = cursor

		if text in editor.language.symbolsPairs.keys():
			extraSelections.append(startSelection)
			endSelection.cursor = editor.getMatchingSymbolsPairs(cursor,
																text,
																editor.language.symbolsPairs[text])
		elif text in editor.language.symbolsPairs.values():
			extraSelections.append(startSelection)
			endSelection.cursor = editor.getMatchingSymbolsPairs(cursor,
																text,
																editor.language.symbolsPairs.getFirstKeyFromValue(text),
																True)
		else:
			return False

		extraSelections.append(endSelection)
	editor.setExtraSelections(extraSelections)
	return True
