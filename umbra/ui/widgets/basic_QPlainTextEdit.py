#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**basic_QPlainTextEdit.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`Basic_QPlainTextEdit` class.

**Others:**
	Portions of the code from codeeditor.py by Roberto Alsina: http://lateral.netmanagers.com.ar/weblog/posts/BB832.html,
	KhtEditor.py by Benoit Hervier: http://khertan.net/khteditor, Ninja IDE: http://ninja-ide.org/ and
	Prymatex: https://github.com/D3f0/prymatex/
"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import re
from PyQt4.QtCore import QChar
from PyQt4.QtCore import QRegExp
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QPlainTextEdit
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextDocument
from PyQt4.QtGui import QTextOption

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.dataStructures
import foundations.exceptions
import foundations.strings
import foundations.trace
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

__all__ = ["LOGGER", "editBlock", "anchorTextCursor", "centerTextCursor", "Basic_QPlainTextEdit"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def editBlock(object):
	"""
	Handles edit blocks undo states.

	:param object: Object to decorate.
	:type object: object
	:return: Object.
	:rtype: object
	"""

	@functools.wraps(object)
	def editBlockWrapper(*args, **kwargs):
		"""
		Handles edit blocks undo states.

		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Object.
		:rtype: object
		"""

		if args:
			cursor = foundations.common.getFirstItem(args).textCursor()
			cursor.beginEditBlock()
		value = None
		try:
			value = object(*args, **kwargs)
		finally:
			if args:
				cursor.endEditBlock()
			return value

	return editBlockWrapper

def anchorTextCursor(object):
	"""
	Anchors the text cursor position.

	:param object: Object to decorate.
	:type object: object
	:return: Object.
	:rtype: object
	"""

	@functools.wraps(object)
	def anchorTextCursorWrapper(*args, **kwargs):
		"""
		Anchors the text cursor position.

		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Object.
		:rtype: object
		"""

		if args:
			if hasattr(foundations.common.getFirstItem(args), "storeTextCursorAnchor"):
				foundations.common.getFirstItem(args).storeTextCursorAnchor()

		value = object(*args, **kwargs)

		if args:
			if hasattr(foundations.common.getFirstItem(args), "restoreTextCursorAnchor"):
				foundations.common.getFirstItem(args).storeTextCursorAnchor()

		return value

	return anchorTextCursorWrapper

def centerTextCursor(object):
	"""
	Centers the text cursor position.

	:param object: Object to decorate.
	:type object: object
	:return: Object.
	:rtype: object
	"""

	@functools.wraps(object)
	def centerTextCursorWrapper(*args, **kwargs):
		"""
		Centers the text cursor position.

		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Object.
		:rtype: object
		"""

		if args:
			if hasattr(foundations.common.getFirstItem(args), "setCenterOnScroll"):
				foundations.common.getFirstItem(args).setCenterOnScroll(True)

		value = object(*args, **kwargs)

		if args:
			if hasattr(foundations.common.getFirstItem(args), "setCenterOnScroll"):
				foundations.common.getFirstItem(args).setCenterOnScroll(False)

		return value

	return centerTextCursorWrapper

class Basic_QPlainTextEdit(QPlainTextEdit):
	"""
	Defines a `QPlainTextEdit <http://doc.qt.nokia.com/qplaintextedit.html>`_ subclass providing
	a basic editor base class.
	"""

	# Custom signals definitions.
	patternsReplaced = pyqtSignal(list)
	"""
	This signal is emited by the :class:`Basic_QPlainTextEdit` class
	when patterns have been replaced. ( pyqtSignal )

	:return: Replaced patterns.
	:rtype: list
	"""

	def __init__(self, parent=None, *args, **kwargs):
		"""
		Initializes the class.

		:param parent: Widget parent.
		:type parent: QObject
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QPlainTextEdit.__init__(self, parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__searchPattern = None
		self.__minimumFontPointSize = 6
		self.__maximumFontPointSize = 24

		self.__textCursorAnchor = None

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def searchPattern(self):
		"""
		Property for **self.__searchPattern** attribute.

		:return: self.__searchPattern.
		:rtype: unicode
		"""

		return self.__searchPattern

	@searchPattern.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def searchPattern(self, value):
		"""
		Setter for **self.__searchPattern** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) in (unicode, QString), \
			"'{0}' attribute: '{1}' type is not 'unicode' or 'QString'!".format("searchPattern", value)
		self.__searchPattern = value

	@searchPattern.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def searchPattern(self):
		"""
		Deleter for **self.__searchPattern** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchPattern"))

	@property
	def minimumFontPointSize(self):
		"""
		Property for **self.__minimumFontPointSize** attribute.

		:return: self.__minimumFontPointSize.
		:rtype: int
		"""

		return self.__minimumFontPointSize

	@minimumFontPointSize.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def minimumFontPointSize(self, value):
		"""
		Setter for **self.__minimumFontPointSize** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) in (int, float), "'{0}' attribute: '{1}' type is not 'int' or 'float'!".format(
			"minimumFontPointSize", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("minimumFontPointSize", value)
		self.__minimumFontPointSize = value

	@minimumFontPointSize.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def minimumFontPointSize(self):
		"""
		Deleter for **self.__minimumFontPointSize** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "minimumFontPointSize"))

	@property
	def maximumFontPointSize(self):
		"""
		Property for **self.__maximumFontPointSize** attribute.

		:return: self.__maximumFontPointSize.
		:rtype: int
		"""

		return self.__maximumFontPointSize

	@maximumFontPointSize.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def maximumFontPointSize(self, value):
		"""
		Setter for **self.__maximumFontPointSize** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) in (int, float), "'{0}' attribute: '{1}' type is not 'int' or 'float'!".format(
			"maximumFontPointSize", value)
			assert value > self.__minimumFontPointSize, \
			"'{0}' attribute: '{1}' need to be exactly superior to '{2}'!".format(
			"maximumFontPointSize", value, self.__minimumFontPointSize)
		self.__maximumFontPointSize = value

	@maximumFontPointSize.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def maximumFontPointSize(self):
		"""
		Deleter for **self.__maximumFontPointSize** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "maximumFontPointSize"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@foundations.trace.untracable
	def wheelEvent(self, event):
		"""
		Reimplements the :meth:`QPlainTextEdit.wheelEvent` method.

		:param event: Event.
		:type event: QEvent
		"""

		if event.modifiers() == Qt.ControlModifier:
			if event.delta() == 120:
				self.zoomIn()
			elif event.delta() == -120:
				self.zoomOut()
			event.ignore()
		else:
			QPlainTextEdit.wheelEvent(self, event)

	def __selectTextUnderCursorBlocks(self, cursor):
		"""
		Selects the document text under cursor blocks.

		:param cursor: Cursor.
		:type cursor: QTextCursor
		"""

		startBlock = self.document().findBlock(cursor.selectionStart()).firstLineNumber()
		endBlock = self.document().findBlock(cursor.selectionEnd()).firstLineNumber()
		cursor.setPosition(self.document().findBlockByLineNumber(startBlock).position())
		cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
		cursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor, endBlock - startBlock)
		cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)

	def getSelectedTextMetrics(self):
		"""
		Returns current document selected text metrics.

		:return: Selected text metrics.
		:rtype: tuple
		"""

		selectedText = self.getSelectedText()
		if not selectedText:
			return tuple()

		return (selectedText, self.getCursorLine(), self.getCursorColumn() - len(selectedText))

	def getDefaultTextOption(self):
		"""
		Returns default text option.

		:return: Default text options.
		:rtype: QTextOption
		"""

		return self.document().defaultTextOption()

	def setDefaultTextOption(self, textOption):
		"""
		Sets default text option using given flag.

		:param textOption: Text option.
		:type textOption: QTextOption
		:return: Method success.
		:rtype: bool
		"""

		self.document().setDefaultTextOption(textOption)
		return True

	def storeTextCursorAnchor(self):
		"""
		Stores the document cursor anchor.

		:return: Method success.
		:rtype: bool
		"""

		self.__textCursorAnchor = (self.textCursor(),
								self.horizontalScrollBar().sliderPosition(),
								self.verticalScrollBar().sliderPosition())
		return True

	def restoreTextCursorAnchor(self):
		"""
		Restores the document cursor anchor.

		:return: Method success.
		:rtype: bool
		"""

		if not self.__textCursorAnchor:
			return False

		textCursor, horizontalScrollBarSliderPosition, verticalScrollBarSliderPosition = self.__textCursorAnchor
		self.setTextCursor(textCursor)
		self.horizontalScrollBar().setSliderPosition(horizontalScrollBarSliderPosition)
		self.verticalScrollBar().setSliderPosition(verticalScrollBarSliderPosition)
		return True

	def getCursorLine(self):
		"""
		Returns the document cursor line.

		:return: Cursor line.
		:rtype: int
		"""

		return self.textCursor().blockNumber()

	def getCursorColumn(self):
		"""
		Returns the document cursor column.

		:return: Cursor column.
		:rtype: int
		"""

		return self.textCursor().columnNumber()

	def getPreviousCharacter(self):
		"""
		Returns the character before the cursor.

		:return: Previous cursor character.
		:rtype: QString
		"""

		cursor = self.textCursor()
		cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
		return cursor.selectedText()

	def getNextCharacter(self):
		"""
		Returns the character after the cursor.

		:return: Next cursor character.
		:rtype: QString
		"""

		cursor = self.textCursor()
		cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
		return cursor.selectedText()

	def getWords(self):
		"""
		Returns the document words.

		:return: Document words.
		:rtype: list
		"""

		words = []
		block = self.document().findBlockByLineNumber(0)
		while block.isValid():
			blockWords = foundations.strings.getWords(foundations.strings.toString(block.text()))
			if blockWords:
				words.extend(blockWords)
			block = block.next()
		return words

	def getSelectedText(self):
		"""
		Returns the document text under cursor.

		:return: Text under cursor.
		:rtype: QString
		"""

		return self.textCursor().selectedText()

	def getWordUnderCursorLegacy(self):
		"""
		Returns the document word under cursor ( Using Qt legacy "QTextCursor.WordUnderCursor" ).

		:return: Word under cursor.
		:rtype: QString
		"""

		cursor = self.textCursor()
		cursor.select(QTextCursor.WordUnderCursor)
		return cursor.selectedText()

	def getWordUnderCursor(self):
		"""
		Returns the document word under cursor.

		:return: Word under cursor.
		:rtype: QString
		"""

		if not re.match(r"^\w+$", foundations.strings.toString(self.getPreviousCharacter())):
			return QString()

		cursor = self.textCursor()
		cursor.movePosition(QTextCursor.PreviousWord, QTextCursor.MoveAnchor)
		cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
		return cursor.selectedText()

	def getPartialWordUnderCursor(self):
		"""
		Returns the document partial word under cursor ( From word start to cursor position ).

		:return: Partial word under cursor.
		:rtype: QString
		"""

		if not re.match(r"^\w+$", foundations.strings.toString(self.getPreviousCharacter())):
			return QString()

		cursor = self.textCursor()
		position = cursor.position()
		cursor.movePosition(QTextCursor.PreviousWord, QTextCursor.KeepAnchor)
		return cursor.selectedText()

	def isModified(self):
		"""
		Returns if the document is modified.

		:return: Document modified state.
		:rtype: bool
		"""

		return self.document().isModified()

	def setModified(self, state):
		"""
		Sets the document modified state.

		:param state: Modified state.
		:type state: bool
		:return: Method success.
		:rtype: bool
		"""

		self.document().setModified(state)
		return True

	def isEmpty(self):
		"""
		Returns if the document is empty.

		:return: Document empty state.
		:rtype: bool
		"""

		return self.document().isEmpty()

	@editBlock
	def setContent(self, content):
		"""
		Sets document with given content while providing undo capability.

		:param content: Content to set.
		:type content: list
		:return: Method success.
		:rtype: bool
		"""

		cursor = self.textCursor()
		cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
		cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
		cursor.removeSelectedText()
		for line in content:
			self.moveCursor(QTextCursor.End)
			self.insertPlainText(line)
		return True

	def delete(self):
		"""
		Deletes the document text under cursor.

		:return: Method success.
		:rtype: bool
		"""

		self.textCursor().removeSelectedText()
		return True

	@editBlock
	def deleteLines(self):
		"""
		Deletes the document lines under cursor.

		:return: Method success.
		:rtype: bool
		"""

		cursor = self.textCursor()
		self.__selectTextUnderCursorBlocks(cursor)
		cursor.removeSelectedText()
		cursor.deleteChar()
		return True

	@editBlock
	def duplicateLines(self):
		"""
		Duplicates the document lines under cursor.

		:return: Method success.
		:rtype: bool
		"""

		cursor = self.textCursor()
		self.__selectTextUnderCursorBlocks(cursor)
		text = cursor.selectedText()

		cursor.setPosition(cursor.block().next().position())
		cursor.position() == cursor.document().firstBlock().position() and cursor.setPosition(
		cursor.document().lastBlock().position())

		startPosition = cursor.position()
		cursor.insertText(text)
		endPosition = cursor.position()
		cursor.insertText(QChar(QChar.ParagraphSeparator))

		cursor.setPosition(startPosition, QTextCursor.MoveAnchor)
		cursor.setPosition(endPosition, QTextCursor.KeepAnchor)
		self.setTextCursor(cursor)

		return True

	@editBlock
	def moveLines(self, direction=QTextCursor.Up):
		"""
		Moves the document lines under cursor.

		:param direction: Move direction ( QTextCursor.Down / QTextCursor.Up ). ( QTextCursor.MoveOperation )
		:return: Method success.
		:rtype: bool
		"""

		cursor = self.textCursor()
		if (direction == QTextCursor.Up and cursor.block() == cursor.document().firstBlock()) or \
		(direction == QTextCursor.Down and cursor.block() == cursor.document().lastBlock()):
			return False

		self.__selectTextUnderCursorBlocks(cursor)
		text = cursor.selectedText()
		cursor.removeSelectedText()
		cursor.deleteChar()

		cursor.setPosition(cursor.block().next().position() if direction == QTextCursor.Down else \
						cursor.block().previous().position())
		if cursor.position() == cursor.document().firstBlock().position() and direction == QTextCursor.Down:
			cursor.movePosition(QTextCursor.End)
			cursor.insertText(QChar(QChar.ParagraphSeparator))

		startPosition = cursor.position()
		cursor.insertText(text)
		endPosition = cursor.position()
		not cursor.atEnd() and cursor.insertText(QChar(QChar.ParagraphSeparator))

		cursor.setPosition(startPosition, QTextCursor.MoveAnchor)
		cursor.setPosition(endPosition, QTextCursor.KeepAnchor)
		self.setTextCursor(cursor)

		return True

	def moveLinesUp(self):
		"""
		Moves up the document lines under cursor.

		:return: Method success.
		:rtype: bool
		"""

		return self.moveLines(QTextCursor.Up)

	def moveLinesDown(self):
		"""
		Moves down the document lines under cursor.

		:return: Method success.
		:rtype: bool
		"""

		return self.moveLines(QTextCursor.Down)

	@centerTextCursor
	def search(self, pattern, **kwargs):
		"""
		Searchs given pattern text in the document.

		Usage::

			>>> scriptEditor = Umbra.componentsManager.getInterface("factory.scriptEditor")
			True
			>>> codeEditor = scriptEditor.getCurrentEditor()
			True
			>>> codeEditor.search(searchPattern, caseSensitive=True, wholeWord=True, regularExpressions=True, \
backwardSearch=True, wrapAround=True)
			True

		:param pattern: Pattern to search for.
		:type pattern: unicode
		:param \*\*kwargs: Search settings.
		:type \*\*kwargs: dict
		:return: Method success.
		:rtype: bool
		"""

		settings = foundations.dataStructures.Structure(**{"caseSensitive" : False,
								"wholeWord" : False,
								"regularExpressions" : False,
								"backwardSearch" : False,
								"wrapAround" : True})
		settings.update(kwargs)

		self.__searchPattern = pattern

		if settings.regularExpressions:
			pattern = QRegExp(pattern)
			pattern.setCaseSensitivity(Qt.CaseSensitive if settings.caseSensitive else Qt.CaseInsensitive)

		flags = QTextDocument.FindFlags()
		if settings.caseSensitive:
			flags = flags | QTextDocument.FindCaseSensitively
		if settings.wholeWord:
			flags = flags | QTextDocument.FindWholeWords
		if settings.backwardSearch:
			flags = flags | QTextDocument.FindBackward

		cursor = self.document().find(pattern, self.textCursor(), flags)
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

	@centerTextCursor
	def searchNext(self):
		"""
		Searchs the next search pattern in the document.

		:return: Method success.
		:rtype: bool
		"""

		pattern = self.getSelectedText() or self.__searchPattern
		if not pattern:
			return False

		return self.search(pattern, **{"caseSensitive" : True,
										"wholeWord" : False,
										"regularExpressions" : False,
										"backwardSearch" : False,
										"wrapAround" : True})

	@centerTextCursor
	def searchPrevious(self):
		"""
		Searchs the previous search pattern in the document.

		:return: Method success.
		:rtype: bool
		"""

		pattern = self.getSelectedText() or self.__searchPattern
		if not pattern:
			return False

		return self.search(pattern, **{"caseSensitive" : True,
										"wholeWord" : False,
										"regularExpressions" : False,
										"backwardSearch" : True,
										"wrapAround" : True})

	@centerTextCursor
	@editBlock
	def replace(self, pattern, replacementPattern, **kwargs):
		"""
		Replaces current given pattern occurence in the document with the replacement pattern.

		Usage::

			>>> scriptEditor = Umbra.componentsManager.getInterface("factory.scriptEditor")
			True
			>>> codeEditor = scriptEditor.getCurrentEditor()
			True
			>>> codeEditor.replace(searchPattern, replacementPattern, caseSensitive=True, wholeWord=True, \
regularExpressions=True, backwardSearch=True, wrapAround=True)
			True

		:param pattern: Pattern to replace.
		:type pattern: unicode
		:param replacementPattern: Replacement pattern.
		:type replacementPattern: unicode
		:param \*\*kwargs: Format settings.
		:type \*\*kwargs: dict
		:return: Method success.
		:rtype: bool
		"""

		settings = foundations.dataStructures.Structure(**{"caseSensitive" : False,
														"regularExpressions" : False})
		settings.update(kwargs)


		selectedText = self.getSelectedText()
		regex = "^{0}$".format(pattern if settings.regularExpressions else re.escape(foundations.strings.toString(pattern)))
		flags = int() if settings.caseSensitive else re.IGNORECASE
		if not selectedText or not re.search(regex, selectedText, flags=flags):
			self.search(pattern, **kwargs)
			return False

		cursor = self.textCursor()
		metrics = self.getSelectedTextMetrics()
		if cursor.isNull():
			return False

		if not cursor.hasSelection():
			return False

		cursor.insertText(replacementPattern)

		self.patternsReplaced.emit([metrics])

		self.search(pattern, **kwargs)

		return True

	@centerTextCursor
	@anchorTextCursor
	@editBlock
	def replaceAll(self, pattern, replacementPattern, **kwargs):
		"""
		| Replaces every given pattern occurrences in the document with the replacement pattern.

		.. warning::

			Initializing **wrapAround** keyword to **True** leads to infinite recursion loop
			if the search pattern and the replacementPattern are the same.

		:param pattern: Pattern to replace.
		:type pattern: unicode
		:param replacementPattern: Replacement pattern.
		:type replacementPattern: unicode
		:param \*\*kwargs: Format settings.
		:type \*\*kwargs: dict
		:return: Method success.
		:rtype: bool
		"""

		editCursor = self.textCursor()

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

		self.patternsReplaced.emit(patternsReplaced)

		return True

	@centerTextCursor
	def gotoLine(self, line):
		"""
		Moves the text cursor to given line.

		:param line: Line to go to.
		:type line: int
		:return: Method success.
		:rtype: bool
		"""

		cursor = self.textCursor()
		cursor.setPosition(self.document().findBlockByNumber(line - 1).position())
		self.setTextCursor(cursor)
		return True

	def gotoColumn(self, column):
		"""
		Moves the text cursor to given column.

		:param column: Column to go to.
		:type column: int
		:return: Method success.
		:rtype: bool
		"""

		cursor = self.textCursor()
		cursor.setPosition(cursor.block().position() + column)
		self.setTextCursor(cursor)
		return True

	def gotoPosition(self, position):
		"""
		Moves the text cursor to given position.

		:param position: Position to go to.
		:type position: int
		:return: Method success.
		:rtype: bool
		"""

		cursor = self.textCursor()
		cursor.setPosition(position)
		self.setTextCursor(cursor)
		return True

	def toggleWordWrap(self):
		"""
		Toggles document word wrap.

		:return: Method success.
		:rtype: bool
		"""

		self.setWordWrapMode(not self.wordWrapMode() and QTextOption.WordWrap or QTextOption.NoWrap)
		return True

	def toggleWhiteSpaces(self):
		"""
		Toggles document white spaces display.

		:return: Method success.
		:rtype: bool
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

	def setFontIncrement(self, value):
		"""
		Increments the document font size.

		:param value: Font size increment.
		:type value: int
		:return: Method success.
		:rtype: bool
		"""

		font = self.font()
		pointSize = font.pointSize() + value
		if pointSize < self.__minimumFontPointSize or pointSize > self.__maximumFontPointSize:
			return False

		font.setPointSize(pointSize)
		self.setFont(font)
		return True

	def zoomIn(self):
		"""
		Increases the document font size.

		:return: Method success.
		:rtype: bool
		"""

		return self.setFontIncrement(1)

	def zoomOut(self):
		"""
		Increases the document font size.

		:return: Method success.
		:rtype: bool
		"""

		return self.setFontIncrement(-1)

if __name__ == "__main__":
	import sys
	from PyQt4.QtGui import QGridLayout
	from PyQt4.QtGui import QLineEdit
	from PyQt4.QtGui import QPushButton
	from PyQt4.QtGui import QWidget

	import umbra.ui.common
	from umbra.globals.constants import Constants

	application = umbra.ui.common.getApplicationInstance()

	widget = QWidget()

	gridLayout = QGridLayout()
	widget.setLayout(gridLayout)

	content = "\n".join(("Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
			"Phasellus tincidunt tempus volutpat.",
			"Cras malesuada nunc id neque fermentum accumsan.",
			"Aenean mauris lorem, faucibus et viverra iaculis, vulputate ac augue.",
			"Mauris consequat urna enim."))

	basic_QPlainTextEdit = Basic_QPlainTextEdit()
	basic_QPlainTextEdit.setContent(content)
	gridLayout.addWidget(basic_QPlainTextEdit)

	lineEdit = QLineEdit("basic_QPlainTextEdit.replace(\"Lorem\", \"Nemo\")")
	gridLayout.addWidget(lineEdit)

	def _pushButton__clicked(*args):
		statement = unicode(lineEdit.text(), Constants.defaultCodec, Constants.codecError)
		exec(statement)

	pushButton = QPushButton("Execute Statement")
	pushButton.clicked.connect(_pushButton__clicked)
	gridLayout.addWidget(pushButton)

	widget.show()
	widget.raise_()

	sys.exit(application.exec_())
