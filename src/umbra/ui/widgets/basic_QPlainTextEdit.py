#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**basic_QPlainTextEdit.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Basic_QPlainTextEdit` class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import logging
from PyQt4.QtCore import QRegExp
from PyQt4.QtCore import QString
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextDocument
from PyQt4.QtGui import QTextOption

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
import foundations.strings
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

__all__ = ["LOGGER", "anchorTextCursor", "Basic_QPlainTextEdit"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def anchorTextCursor(object):
	"""
	This decorator is used to anchor the text cursor position.
	
	:param object: Object to decorate. ( Object )
	:return: Object. ( Object )
	"""

	@functools.wraps(object)
	def function(*args, **kwargs):
		"""
		This decorator is used to anchor the text cursor position.

		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		:return: Object. ( Object )
		"""

		if args:
			if hasattr(args[0], "storeTextCursorAnchor"):
				args[0].storeTextCursorAnchor()

		value = object(*args, **kwargs)

		if args:
			if hasattr(args[0], "restoreTextCursorAnchor"):
				args[0].storeTextCursorAnchor()

		return value

	return function

class Basic_QPlainTextEdit(QPlainTextEdit):
	"""
	This class is a `QPlainTextEdit <http://doc.qt.nokia.com/qplaintextedit.html>`_ subclass providing
	a basic editor base class.
	"""

	# Custom signals definitions.
	patternsReplaced = pyqtSignal(list)
	"""
	This signal is emited by the :class:`Basic_QPlainTextEdit` class
	when patterns have been replaced. ( pyqtSignal )
	
	:return: Replaced patterns. ( List )		
	"""

	@core.executionTrace
	def __init__(self, parent=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QPlainTextEdit.__init__(self, parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__searchPattern = None

		self.__textCursorAnchor = None

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def searchPattern(self):
		"""
		This method is the property for **self.__searchPattern** attribute.

		:return: self.__searchPattern. ( String )
		"""

		return self.__searchPattern

	@searchPattern.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def searchPattern(self, value):
		"""
		This method is the setter method for **self.__searchPattern** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode, QString), \
			"'{0}' attribute: '{1}' type is not 'str', 'unicode' or 'QString'!".format("searchPattern", value)
		self.__searchPattern = value

	@searchPattern.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchPattern(self):
		"""
		This method is the deleter method for **self.__searchPattern** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchPattern"))

	@core.executionTrace
	def getSelectedTextMetrics(self):
		"""
		This method returns current document selected text metrics.

		:return: Selected text metrics. ( Tuple )		
		"""

		selectedText = self.getSelectedText()
		if not selectedText:
			return

		return (selectedText, self.getCursorLine(), self.getCursorColumn() - len(selectedText))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getDefaultTextOption(self):
		"""
		This method returns default text option.

		:return: Default text options. ( QTextOption )		
		"""

		return self.document().defaultTextOption()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setDefaultTextOption(self, textOption):
		"""
		This method sets default text option using given flag.

		:param textOption: Text option. ( QTextOption )
		:return: Method success. ( Boolean )
		"""

		self.document().setDefaultTextOption(textOption)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def storeTextCursorAnchor(self):
		"""
		This method stores the document cursor anchor.

		:return: Method success. ( Boolean )
		"""

		self.__textCursorAnchor = (self.textCursor(),
								self.horizontalScrollBar().sliderPosition(),
								self.verticalScrollBar().sliderPosition())
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def restoreTextCursorAnchor(self):
		"""
		This method restores the document cursor anchor.

		:return: Method success. ( Boolean )
		"""

		if not self.__textCursorAnchor:
			return

		textCursor, horizontalScrollBarSliderPosition, verticalScrollBarSliderPosition = self.__textCursorAnchor
		self.setTextCursor(textCursor)
		self.horizontalScrollBar().setSliderPosition(horizontalScrollBarSliderPosition)
		self.verticalScrollBar().setSliderPosition(verticalScrollBarSliderPosition)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getCursorLine(self):
		"""
		This method returns the document cursor line.

		:return: Cursor line. ( Integer )		
		"""

		return self.textCursor().blockNumber()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getCursorColumn(self):
		"""
		This method returns the document cursor column.

		:return: Cursor column. ( Integer )		
		"""

		return self.textCursor().columnNumber()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getWords(self):
		"""
		This method returns the document words.

		:return: Document words. ( List )		
		"""

		words = []
		block = self.document().findBlockByLineNumber(0)
		while block.isValid():
			blockWords = foundations.strings.getWords(unicode(block.text(),
																Constants.encodingFormat,
																Constants.encodingError))
			if blockWords:
				words.extend(blockWords)
			block = block.next()
		return words

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getSelectedText(self):
		"""
		This method returns the document text under cursor.

		:return: Text under cursor. ( QString )		
		"""

		return self.textCursor().selectedText()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getWordUnderCursorLegacy(self):
		"""
		This method returns the document word under cursor ( Using Qt legacy "QTextCursor.WordUnderCursor" ).

		:return: Word under cursor. ( QString )		
		"""

		cursor = self.textCursor()
		cursor.select(QTextCursor.WordUnderCursor)
		return cursor.selectedText()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def isModified(self):
		"""
		This method returns if the document is modified.

		:return: Document modified state. ( Boolean )
		"""

		return self.document().isModified()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setModified(self, state):
		"""
		This method sets the document modified state.

		:param state: Modified state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		self.document().setModified(state)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def isEmpty(self):
		"""
		This method returns if the document is empty.

		:return: Document empty state. ( Boolean )
		"""

		return self.document().isEmpty()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getWordUnderCursor(self):
		"""
		This method returns the document word under cursor.

		:return: Word under cursor. ( QString )		
		"""

		cursor = self.textCursor()
		cursor.movePosition(QTextCursor.PreviousWord, QTextCursor.KeepAnchor)
		return cursor.selectedText()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setContent(self, content):
		"""
		This method sets document with given content while providing undo capability.

		:param content: Content to set. ( List )
		:return: Method success. ( Boolean )
		"""

		cursor = self.textCursor()
		cursor.beginEditBlock()
		cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
		cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
		cursor.removeSelectedText()
		for line in content:
			self.moveCursor(QTextCursor.End)
			self.insertPlainText(line)
		cursor.endEditBlock()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def delete(self):
		"""
		This method deletes the document text under cursor.

		:return: Method success. ( Boolean )
		"""

		self.textCursor().removeSelectedText()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def search(self, pattern, **kwargs):
		"""
		This method searchs given pattern text in the document.
		
		Usage::
			
			>>> scriptEditor = Umbra.componentsManager.getInterface("factory.scriptEditor")
			True
			>>> codeEditor = scriptEditor.getCurrentEditor()
			True
			>>> codeEditor.search(searchPattern, caseSensitive=True, wholeWord=True, regularExpressions=True, \
backwardSearch=True, wrapAround=True)
			True
				
		:param pattern: Pattern to search for. ( String )
		:param \*\*kwargs: Search settings. ( Key / Value pairs )
		:return: Method success. ( Boolean )
		"""

		settings = foundations.dataStructures.Structure(**{"caseSensitive" : False,
								"wholeWord" : False,
								"regularExpressions" : False,
								"backwardSearch" : False,
								"wrapAround" : True})
		settings.update(kwargs)

		self.__searchPattern = pattern

		flags = QTextDocument.FindFlags()
		if settings.caseSensitive:
			flags = flags | QTextDocument.FindCaseSensitively
		if settings.wholeWord:
			flags = flags | QTextDocument.FindWholeWords
		if settings.backwardSearch:
			flags = flags | QTextDocument.FindBackward

		cursor = self.textCursor()
		if settings.regularExpressions:
			cursor = self.document().find(QRegExp(pattern), cursor, flags)
		else:
			cursor = self.document().find(pattern, cursor, flags)
		if not cursor.isNull():
			self.setTextCursor(cursor)
			return True
		else:
			if settings.wrapAround:
				self.storeTextCursorAnchor()
				cursor = self.textCursor()
				if settings.backwardSearch:
					cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
				else:
					cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
				self.setTextCursor(cursor)
				settings.wrapAround = False
				if self.search(pattern, **settings):
					return True
				else:
					self.restoreTextCursorAnchor()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def searchNext(self):
		"""
		This method searchs the next search pattern in the document.

		:return: Method success. ( Boolean )
		"""

		pattern = self.getSelectedText() or self.__searchPattern
		if not pattern:
			return

		return self.search(pattern, **{"caseSensitive" : True,
										"wholeWord" : False,
										"regularExpressions" : False,
										"backwardSearch" : False,
										"wrapAround" : True})

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def searchPrevious(self):
		"""
		This method searchs the previous search pattern in the document.

		:return: Method success. ( Boolean )
		"""

		pattern = self.getSelectedText() or self.__searchPattern
		if not pattern:
			return

		return self.search(pattern, **{"caseSensitive" : True,
										"wholeWord" : False,
										"regularExpressions" : False,
										"backwardSearch" : True,
										"wrapAround" : True})

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def replace(self, pattern, replacementPattern, **kwargs):
		"""
		This method replaces current given pattern occurence in the document with the replacement pattern.

		Usage::
			
			>>> scriptEditor = Umbra.componentsManager.getInterface("factory.scriptEditor")
			True
			>>> codeEditor = scriptEditor.getCurrentEditor()
			True
			>>> codeEditor.replace(searchPattern, replacementPattern, caseSensitive=True, wholeWord=True, \
regularExpressions=True, backwardSearch=True, wrapAround=True)
			True

		:param pattern: Pattern to replace. ( String )
		:param replacementPattern: Replacement pattern. ( String )
		:param \*\*kwargs: Format settings. ( Key / Value pairs )
		:return: Method success. ( Boolean )
		"""

		selectedText = self.getSelectedText()
		if not selectedText or selectedText != pattern:
			self.search(pattern, **kwargs)
			return

		cursor = self.textCursor()
		metrics = self.getSelectedTextMetrics()
		cursor.beginEditBlock()
		if cursor.isNull():
			return

		if not cursor.hasSelection():
			return

		cursor.insertText(replacementPattern)
		cursor.endEditBlock()

		self.patternsReplaced.emit([metrics])

		self.search(pattern, **kwargs)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	@anchorTextCursor
	def replaceAll(self, pattern, replacementPattern, **kwargs):
		"""
		| This method replaces every given pattern occurences in the document with the replacement pattern.
		
		.. warning::

			Initializing **wrapAround** keyword to **True** leads to infinite recursion loop
			if the search pattern and the replacementPattern are the same.

		:param pattern: Pattern to replace. ( String )
		:param replacementPattern: Replacement pattern. ( String )
		:param \*\*kwargs: Format settings. ( Key / Value pairs )
		:return: Method success. ( Boolean )
		"""

		editCursor = self.textCursor()
		editCursor.beginEditBlock()

		editCursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
		self.setTextCursor(editCursor)

		patternsReplaced = []
		while True:
			if not self.search(pattern, **kwargs):
				break

			cursor = self.textCursor()
			metrics = self.getSelectedTextMetrics()
			if cursor.isNull():
				break

			if not cursor.hasSelection():
				break
			cursor.insertText(replacementPattern)
			patternsReplaced.append(metrics)
		editCursor.endEditBlock()

		self.patternsReplaced.emit(patternsReplaced)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def gotoLine(self, line):
		"""
		This method moves the text cursor to given line.

		:param line: Line to go to. ( Integer )
		:return: Method success. ( Boolean )
		"""

		cursor = self.textCursor()
		cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
		cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, line - 1)
		self.setTextCursor(cursor)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def toggleWordWrap(self):
		"""
		This method toggles document word wrap.

		:return: Method success. ( Boolean )
		"""

		self.setWordWrapMode(not self.wordWrapMode() and QTextOption.WordWrap or QTextOption.NoWrap)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def toggleWhiteSpaces(self):
		"""
		This method toggles document white spaces display.

		:return: Method success. ( Boolean )
		"""

		textOption = self.getDefaultTextOption()
		if textOption.flags().__int__():
			textOption = QTextOption()
			textOption.setTabStop(self.tabStopWidth())
		else:
			textOption.setFlags(
			textOption.flags() | QTextOption.ShowTabsAndSpaces | QTextOption.ShowLineAndParagraphSeparators)
		self.setDefaultTextOption(textOption)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setFontIncrement(self, value):
		"""
		This method increments the document font size.

		:param value: Font size increment. ( Integer )
		:return: Method success. ( Boolean )
		"""

		font = self.font()
		pointSize = font.pointSize() + value
		if pointSize <= 0:
			return
		font.setPointSize(pointSize)
		self.setFont(font)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def zoomIn(self):
		"""
		This method increases the document font size.

		:return: Method success. ( Boolean )
		"""

		return self.setFontIncrement(1)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def zoomOut(self):
		"""
		This method increases the document font size.

		:return: Method success. ( Boolean )
		"""

		return self.setFontIncrement(-1)