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
import logging
import re
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QTextDocument
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QTextFormat

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
#import foundations.core as core
#import foundations.exceptions
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
			"highlightCurrentLine",
			"highlightOccurences"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
#@core.executionTrace
#@foundations.exceptions.exceptionsHandler(None, False, Exception)
def highlightCurrentLine(editor):
	"""
	This definition highlights given editor current line.
	
	:param editor: Document editor. ( QWidget )
	:return: Method success. ( Boolean )
	"""

	format = editor.highlighter.theme.get("accelerator.line")
	if not format:
		return

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

#@core.executionTrace
#@foundations.exceptions.exceptionsHandler(None, False, Exception)
def highlightOccurences(editor):
	"""
	This definition highlights given editor current line.
	
	:param editor: Document editor. ( QWidget )
	:return: Method success. ( Boolean )
	"""

	format = editor.highlighter.theme.get("accelerator.occurences")
	if not format:
		return

	extraSelections = editor.extraSelections() or []
	if not editor.isReadOnly():
		word = editor.getWordUnderCursor()
		if re.match(r"\w+", unicode(word, Constants.encodingFormat, Constants.encodingError)):
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
