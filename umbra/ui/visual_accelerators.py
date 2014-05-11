#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**visual_accelerators.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the Application visual accelerators objects.

**Others:**
"""

from __future__ import unicode_literals

from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextDocument
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QTextFormat

# import foundations.exceptions
import foundations.strings
import foundations.verbose

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"highlight_current_line",
			"highlight_occurences",
			"highlight_matching_symbols_pairs"]

LOGGER = foundations.verbose.install_logger()

def highlight_current_line(editor):
	"""
	Highlights given editor current line.
	
	:param editor: Document editor.
	:type editor: QWidget
	:return: Method success.
	:rtype: bool
	"""

	format = editor.language.theme.get("accelerator.line")
	if not format:
		return False

	extra_selections = editor.extraSelections() or []
	if not editor.isReadOnly():
		selection = QTextEdit.ExtraSelection()
		selection.format.setBackground(format.background())
		selection.format.setProperty(QTextFormat.FullWidthSelection, True)
		selection.cursor = editor.textCursor()
		selection.cursor.clearSelection()
		extra_selections.append(selection)
	editor.setExtraSelections(extra_selections)
	return True

def highlight_occurences(editor):
	"""
	Highlights given editor current line.
	
	:param editor: Document editor.
	:type editor: QWidget
	:return: Method success.
	:rtype: bool
	"""

	format = editor.language.theme.get("accelerator.occurence")
	if not format:
		return False

	extra_selections = editor.extraSelections() or []
	if not editor.isReadOnly():
		word = editor.get_word_under_cursor()
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
			extra_selections.append(selection)
			cursor = editor.document().find(word,
											cursor.position(),
											QTextDocument.FindCaseSensitively | QTextDocument.FindWholeWords)
			block = block.next()
	editor.setExtraSelections(extra_selections)
	return True

def highlight_matching_symbols_pairs(editor):
	"""
	Highlights given editor matching pairs.
	
	:param editor: Document editor.
	:type editor: QWidget
	:return: Method success.
	:rtype: bool
	"""

	format = editor.language.theme.get("accelerator.pair")
	if not format:
		return False

	extra_selections = editor.extraSelections() or []
	if not editor.isReadOnly():
		start_selection = QTextEdit.ExtraSelection()
		start_selection.format.setBackground(format.background())
		end_selection = QTextEdit.ExtraSelection()
		end_selection.format.setBackground(format.background())

		cursor = editor.textCursor()
		if cursor.hasSelection():
			text = foundations.strings.to_string(cursor.selectedText())
		else:
			cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
			text = foundations.strings.to_string(cursor.selectedText())

		start_selection.cursor = cursor

		if text in editor.language.symbols_pairs.keys():
			extra_selections.append(start_selection)
			end_selection.cursor = editor.get_matching_symbols_pairs(cursor,
																text,
																editor.language.symbols_pairs[text])
		elif text in editor.language.symbols_pairs.values():
			extra_selections.append(start_selection)
			end_selection.cursor = editor.get_matching_symbols_pairs(cursor,
																text,
																editor.language.symbols_pairs.get_first_key_from_value(text),
																True)
		else:
			return False

		extra_selections.append(end_selection)
	editor.setExtraSelections(extra_selections)
	return True
