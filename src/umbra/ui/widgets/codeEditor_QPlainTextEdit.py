#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**codeEditor_QPlainTextEdit.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`LinesNumbers_QWidget` and :class:`CodeEditor_QPlainTextEdit` classes.

**Others:**
	Portions of the code from codeeditor.py by Roberto Alsina: http://lateral.netmanagers.com.ar/weblog/posts/BB832.html and KhtEditor.py by Benoit Hervier: http://khertan.net/khteditor
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
import foundations.exceptions
import foundations.strings
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

__all__ = ["LOGGER", "LinesNumbers_QWidget", "CodeEditor_QPlainTextEdit"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class LinesNumbers_QWidget(QWidget):
	"""
	This class is a `QWidget <http://doc.qt.nokia.com/4.7/qwidget.html>`_ subclass providing a lines numbers widget.
	"""

	@core.executionTrace
	def __init__(self, editor):
		"""
		This method initializes the class.

		:param editor: Editor to attach the widget to. ( QTextEdit / QPlainTextEdit )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QWidget.__init__(self, editor)

		# --- Setting class attributes. ---
		self.__editor = editor

		self.__margin = 16
		self.__separatorWidth = 2
		self.__backgroundColor = QColor(48, 48, 48)
		self.__color = QColor(192, 192, 192)
		self.__separatorColor = QColor(88, 88, 88)

		self.setEditorViewportMargins(0)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def editor(self):
		"""
		This method is the property for **self.__editor** attribute.

		:return: self.__editor. ( QWidget )
		"""

		return self.__editor

	@editor.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def editor(self, value):
		"""
		This method is the setter method for **self.__editor** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		self.__editor = value

	@editor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editor(self):
		"""
		This method is the deleter method for **self.__editor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("editor"))

	@property
	def margin(self):
		"""
		This method is the property for **self.__margin** attribute.

		:return: self.__margin. ( Integer )
		"""

		return self.__margin

	@margin.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def margin(self, value):
		"""
		This method is the setter method for **self.__margin** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("margin", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("margin", value)
		self.__margin = value

	@margin.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def margin(self):
		"""
		This method is the deleter method for **self.__margin** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("margin"))

	@property
	def separatorWidth(self):
		"""
		This method is the property for **self.__separatorWidth** attribute.

		:return: self.__separatorWidth. ( Integer )
		"""

		return self.__separatorWidth

	@separatorWidth.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def separatorWidth(self, value):
		"""
		This method is the setter method for **self.__separatorWidth** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("separatorWidth", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("separatorWidth", value)
		self.__separatorWidth = value

	@separatorWidth.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def separatorWidth(self):
		"""
		This method is the deleter method for **self.__separatorWidth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("separatorWidth"))

	@property
	def backgroundColor(self):
		"""
		This method is the property for **self.__backgroundColor** attribute.

		:return: self.__backgroundColor. ( QColor )
		"""

		return self.__backgroundColor

	@backgroundColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def backgroundColor(self, value):
		"""
		This method is the setter method for **self.__backgroundColor** attribute.

		:param value: Attribute value. ( QColor )
		"""

		if value:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("backgroundColor", value)
		self.__backgroundColor = value

	@backgroundColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def backgroundColor(self):
		"""
		This method is the deleter method for **self.__backgroundColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("backgroundColor"))

	@property
	def color(self):
		"""
		This method is the property for **self.__color** attribute.

		:return: self.__color. ( QColor )
		"""

		return self.__color

	@color.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def color(self, value):
		"""
		This method is the setter method for **self.__color** attribute.

		:param value: Attribute value. ( QColor )
		"""

		if value:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("color", value)
		self.__color = value

	@color.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def color(self):
		"""
		This method is the deleter method for **self.__color** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("color"))

	@property
	def separatorColor(self):
		"""
		This method is the property for **self.__separatorColor** attribute.

		:return: self.__separatorColor. ( QColor )
		"""

		return self.__separatorColor

	@separatorColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def separatorColor(self, value):
		"""
		This method is the setter method for **self.__separatorColor** attribute.

		:param value: Attribute value. ( QColor )
		"""

		if value:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("separatorColor", value)
		self.__separatorColor = value

	@separatorColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def separatorColor(self):
		"""
		This method is the deleter method for **self.__separatorColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("separatorColor"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def sizeHint(self):
		"""
		This method reimplements the Widget **sizeHint** method.

		:return: Size hint. ( QSize )
		"""

		return QSize(self.__getWidth(), 0)

	@core.executionTrace
	def paintEvent(self, event):
		"""
		This method reimplements the Widget **paintEvent** method.
		
		:param event: Event. ( QEvent )
		"""

		painter = QPainter(self)
		painter.fillRect(event.rect(), self.__backgroundColor)

		topRightCorner = event.rect().topRight()
		bottomRightCorner = event.rect().bottomRight()
		pen = QPen(QBrush(), self.__separatorWidth)
		pen.setColor(self.__separatorColor)
		painter.setPen(pen)
		painter.drawLine(topRightCorner.x(), topRightCorner.y(), bottomRightCorner.x(), bottomRightCorner.y())

		block = self.__editor.firstVisibleBlock()
		blockNumber = block.blockNumber();
		top = int(self.__editor.blockBoundingGeometry(block).translated(self.__editor.contentOffset()).top())
		bottom = top + int(self.__editor.blockBoundingRect(block).height())

		painter.setPen(self.__color)
		while block.isValid() and top <= event.rect().bottom():
			if block.isVisible() and bottom >= event.rect().top():
				number = str(blockNumber + 1)
				painter.drawText(-self.__margin / 4, top, self.width(), self.__editor.fontMetrics().height(), Qt.AlignRight, number)
			block = block.next()

			top = bottom
			bottom = top + int(self.__editor.blockBoundingRect(block).height())
			blockNumber += 1

	@core.executionTrace
	def __getWidth(self):
		"""
		This method returns the Widget target width.

		:return: Widget target width. ( Integer )
		"""

		return self.__margin + self.__editor.fontMetrics().width(str(max(1, self.__editor.blockCount())))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setEditorViewportMargins(self, newBlocksCount):
		"""
		This method sets the editor viewport margins.
		
		:param newBlocksCount: Updated editor blocks count. ( Integer )
		:return: Method success. ( Boolean )
		"""

		self.__editor.setViewportMargins(self.__getWidth(), 0, 0, 0)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def updateRectangle(self, rectangle, scrollY):
		"""
		This method updates the provided widget rectangle.
		
		:param rectangle: Rectangle to update. ( QRect )
		:param scrollY: Amount of pixels the viewport was scrolled. ( Integer )
		:return: Method success. ( Boolean )
		"""

		if scrollY:
			self.scroll(0, scrollY);
		else:
			self.update(0, rectangle.y(), self.width(), rectangle.height())

		if rectangle.contains(self.__editor.viewport().rect()):
			self.setEditorViewportMargins(0)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def updateGeometry(self):
		"""
		This method updates the widget geometry.
		
		:return: Method success. ( Boolean )
		"""

		self.setGeometry(self.__editor.contentsRect().left(), self.__editor.contentsRect().top(), self.__getWidth(), self.__editor.contentsRect().height())
		return True

class CodeEditor_QPlainTextEdit(QPlainTextEdit):
	"""
	This class is a `QPlainTextEdit <http://doc.qt.nokia.com/4.7/qplaintextedit.html>`_ subclass providing a code editor base class.
	"""

	@core.executionTrace
	def __init__(self, parent=None, indentMarker="\t", commentMarker="#"):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		:param indentMarker: Indentation marker. ( String )
		:param commentMarker: Comment marker. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QPlainTextEdit.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__indentMarker = None
		self.indentMarker = indentMarker
		self.__commentMarker = None
		self.commentMarker = commentMarker

		self.__marginArea_LinesNumbers_widget = None
		self.__completer = None

		self.__highlightColor = QColor(56, 56, 56)

		self.__searchPattern = None

		self.__symbolsPairs = {Qt.Key_BracketLeft : Qt.Key_BracketRight, Qt.Key_ParenLeft : Qt.Key_ParenRight, Qt.Key_BraceLeft : Qt.Key_BraceRight, Qt.Key_QuoteDbl : Qt.Key_QuoteDbl, Qt.Key_Apostrophe : Qt.Key_Apostrophe}

		CodeEditor_QPlainTextEdit.initializeUi(self)

		self.__highlightCurrentLine()

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def indentMarker(self):
		"""
		This method is the property for **self.__indentMarker** attribute.

		:return: self.__indentMarker. ( String )
		"""

		return self.__indentMarker

	@indentMarker.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def indentMarker(self, value):
		"""
		This method is the setter method for **self.__indentMarker** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("indentMarker", value)
			assert re.search("\s", value), "'{0}' attribute: '{1}' is not a whitespace character!".format("indentMarker", value)
		self.__indentMarker = value

	@indentMarker.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def indentMarker(self):
		"""
		This method is the deleter method for **self.__indentMarker** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("indentMarker"))

	@property
	def commentMarker(self):
		"""
		This method is the property for **self.__commentMarker** attribute.

		:return: self.__commentMarker. ( String )
		"""

		return self.__commentMarker

	@commentMarker.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def commentMarker(self, value):
		"""
		This method is the setter method for **self.__commentMarker** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("commentMarker", value)
		self.__commentMarker = value

	@commentMarker.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def commentMarker(self):
		"""
		This method is the deleter method for **self.__commentMarker** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("commentMarker"))

	@property
	def marginArea_LinesNumbers_widget(self):
		"""
		This method is the property for **self.__marginArea_LinesNumbers_widget** attribute.

		:return: self.__marginArea_LinesNumbers_widget. ( LinesNumbers_QWidget )
		"""

		return self.__marginArea_LinesNumbers_widget

	@marginArea_LinesNumbers_widget.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def marginArea_LinesNumbers_widget(self, value):
		"""
		This method is the setter method for **self.__marginArea_LinesNumbers_widget** attribute.

		:param value: Attribute value. ( LinesNumbers_QWidget )
		"""

		if value:
			assert type(value) is LinesNumbers_QWidget, "'{0}' attribute: '{1}' type is not 'LinesNumbers_QWidget'!".format("checked", value)
		self.__marginArea_LinesNumbers_widget = value

	@marginArea_LinesNumbers_widget.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def marginArea_LinesNumbers_widget(self):
		"""
		This method is the deleter method for **self.__marginArea_LinesNumbers_widget** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("marginArea_LinesNumbers_widget"))

	@property
	def completer(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QCompleter )
		"""

		return self.__container

	@completer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completer(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QCompleter )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("completer"))

	@completer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completer(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("completer"))

	@property
	def highlightColor(self):
		"""
		This method is the property for **self.__highlightColor** attribute.

		:return: self.__highlightColor. ( QColor )
		"""

		return self.__highlightColor

	@highlightColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def highlightColor(self, value):
		"""
		This method is the setter method for **self.__highlightColor** attribute.

		:param value: Attribute value. ( QColor )
		"""

		if value:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("highlightColor", value)
		self.__highlightColor = value

	@highlightColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def highlightColor(self):
		"""
		This method is the deleter method for **self.__highlightColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("highlightColor"))

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

		if value:
			assert type(value) in (str, unicode, QString), "'{0}' attribute: '{1}' type is not 'str', 'unicode' or 'QString'!".format("searchPattern", value)
		self.__searchPattern = value

	@searchPattern.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchPattern(self):
		"""
		This method is the deleter method for **self.__searchPattern** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("searchPattern"))

	@property
	def symbolsPairs(self):
		"""
		This method is the property for **self.__symbolsPairs** attribute.

		:return: self.__symbolsPairs. ( Dictionary )
		"""

		return self.__symbolsPairs

	@symbolsPairs.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def symbolsPairs(self, value):
		"""
		This method is the setter method for **self.__symbolsPairs** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("symbolsPairs"))

	@symbolsPairs.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def symbolsPairs(self):
		"""
		This method is the deleter method for **self.__symbolsPairs** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("symbolsPairs"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the widget ui.

		:return: Method success. ( Boolean )		
		"""

		self.__marginArea_LinesNumbers_widget = LinesNumbers_QWidget(self)

		# Signals / Slots.
		self.blockCountChanged.connect(self.__marginArea_LinesNumbers_widget.setEditorViewportMargins)
		self.updateRequest.connect(self.__marginArea_LinesNumbers_widget.updateRectangle)
		self.cursorPositionChanged.connect(self.__highlightCurrentLine)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __highlightCurrentLine(self):
		"""
		This method highlights the current line.

		:return: Method success. ( Boolean )		
		"""

		extraSelections = []
		if not self.isReadOnly():
			selection = QTextEdit.ExtraSelection()
			lineColor = self.__highlightColor
			selection.format.setBackground(lineColor)
			selection.format.setProperty(QTextFormat.FullWidthSelection, True)
			selection.cursor = self.textCursor()
			selection.cursor.clearSelection()
			extraSelections.append(selection)

		self.setExtraSelections(extraSelections)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __insertCompletion(self, completion):
		"""
		This method inserts the completion text in the current document.

		:param completion: Completion text. ( QString )
		:return: Method success. ( Boolean )		
		"""

		textCursor = self.textCursor()
		extra = (completion.length() - self.__completer.completionPrefix().length())
		textCursor.movePosition(QTextCursor.Left)
		textCursor.movePosition(QTextCursor.EndOfWord)
		textCursor.insertText(completion.right(extra))
		self.setTextCursor(textCursor)
		return True

	@core.executionTrace
	def resizeEvent(self, event):
		"""
		This method reimplements the Widget **resizeEvent** method.

		:param event: Event. ( QEvent )
		"""

		QPlainTextEdit.resizeEvent(self, event)
		self.__marginArea_LinesNumbers_widget.updateGeometry()

	@core.executionTrace
	def keyPressEvent(self, event):
		"""
		This method reimplements the Widget **keyPressEvent** method.

		:param event: Event. ( QEvent )
		"""

		if event.key() == Qt.Key_Tab:
			self.indent()
			return
		elif event.key() == Qt.Key_Backtab:
			self.unindent()
			return

		if event.key() in self.__symbolsPairs.keys():
			cursor = self.textCursor()
			cursor.beginEditBlock()
			if not cursor.hasSelection():
				cursor.insertText(event.text())
				cursor.insertText(chr(self.__symbolsPairs[event.key()]))
				cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor)
			else:
				selectionText = cursor.selectedText()
				cursor.insertText(event.text())
				cursor.insertText(selectionText)
				cursor.insertText(chr(self.__symbolsPairs[event.key()]))
			self.setTextCursor(cursor)
			cursor.endEditBlock()
			return

		if self.__completer and self.__completer.popup().isVisible():
			if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
				event.ignore()
				return

		if event.modifiers() in (Qt.ControlModifier, Qt.MetaModifier) and event.key() == Qt.Key_Space:
			if not self.__completer:
				return
			completionPrefix = self.textUnderCursor()
			if completionPrefix.length() >= 1 :
				words = self.getWords()
				words.remove(completionPrefix)
				self.__completer.updateModel(words)
				self.__completer.setCompletionPrefix(completionPrefix)
				if self.__completer.completionCount() == 1:
					completion = self.__completer.completionModel().data(self.__completer.completionModel().index(0, 0)).toString()
					cursor = self.textCursor()
					cursor.insertText(completion[len(self.textUnderCursor()):])
					self.setTextCursor(cursor)
				else:
					popup = self.__completer.popup()
					popup.setCurrentIndex(self.__completer.completionModel().index(0, 0))

					completerRectangle = self.cursorRect()
					completerRectangle.setWidth(self.__completer.popup().sizeHintForColumn(0) + self.__completer.popup().verticalScrollBar().sizeHint().width())
					self.__completer.complete(completerRectangle)
		else:
			if self.__completer:
				self.__completer.popup().hide()

		QPlainTextEdit.keyPressEvent(self, event)

		if event.key() in (Qt.Key_Backspace,):
			cursor = self.textCursor()
			cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
			selectedText = cursor.selectedText()
			if not selectedText:
				return

			if ord(str(selectedText)) in self.__symbolsPairs.values():
				cursor.deleteChar()
				return

		if event.key() in (Qt.Key_Enter, Qt.Key_Return):
			cursor = self.textCursor()
			block = cursor.block().previous()
			if block.isValid():
				indent = re.match(r"(\s*)", unicode(block.text())).group(1)
				if str(block.text()).endswith(":"):
					indent += self.__indentMarker
				cursor.insertText(indent)
				return

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setCompleter(self, completer):
		"""
		This method sets provided completer as the current completer.

		:param completer: Completer. ( QCompleter )
		:return: Method success. ( Boolean )		
		"""

		if not issubclass(completer.__class__, QCompleter):
			raise Exception("'{1}' type is not 'QCompleter'!".format(completer))

		# Signals / Slots.
		if self.__completer:
			self.__completer.activated.disconnect(self.__insertCompletion)

		self.__completer = completer
		self.__completer.setWidget(self)

		# Signals / Slots.
		self.__completer.activated.connect(self.__insertCompletion)

		return True

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
		This method sets default text option using provided flag.

		:param textOption: Text option. ( QTextOption )
		:return: Method success. ( Boolean )		
		"""

		self.document().setDefaultTextOption(textOption)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getCursorLine(self):
		"""
		This method returns the text cursor line.

		:return: Cursor line. ( Integer )		
		"""

		return self.textCursor().blockNumber()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getCursorColumn(self):
		"""
		This method returns the text cursor column.

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
		block = self.firstVisibleBlock()
		while block.isValid():
			blockWords = foundations.strings.getWords(str(block.text()))
			if blockWords:
				words.extend(blockWords)
			block = block.next()
		return words

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def textUnderCursor(self):
		"""
		This method returns the text under cursor.

		:return: Text under cursor. ( QString )		
		"""

		textCursor = self.textCursor()
		textCursor.select(QTextCursor.WordUnderCursor)
		return textCursor.selectedText()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def delete(self):
		"""
		This method deletes the text under cursor.

		:return: Method success. ( Boolean )		
		"""

		self.textCursor().removeSelectedText()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def indent(self):
		"""
		This method indents the text under cursor.

		:return: Method success. ( Boolean )		
		"""

		cursor = self.textCursor()
		cursor.beginEditBlock()
		if not cursor.hasSelection():
			cursor.insertText(self.__indentMarker)
		else:
			block = self.document().findBlock(cursor.selectionStart())
			while True:
				blockCursor = self.textCursor()
				blockCursor.setPosition(block.position())
				blockCursor.insertText(self.__indentMarker)
				if block.contains(cursor.selectionEnd()):
					break
				block = block.next()
		cursor.endEditBlock()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def unindent(self):
		"""
		This method unindents the text under cursor.

		:return: Method success. ( Boolean )		
		"""

		cursor = self.textCursor()
		cursor.beginEditBlock()
		if not cursor.hasSelection():
			cursor.movePosition(QTextCursor.StartOfBlock)
			line = str(self.document().findBlockByNumber(cursor\
									  .blockNumber()).text())
			indentMarker = re.match(r"({0})".format(self.__indentMarker), line)
			if indentMarker:
				for i in range(len(indentMarker.group(1))):
					cursor.deleteChar()
		else:
			block = self.document().findBlock(cursor.selectionStart())
			while True:
				blockCursor = self.textCursor()
				blockCursor.setPosition(block.position())
				indentMarker = re.match(r"({0})".format(self.__indentMarker), block.text())
				if indentMarker:
					for i in range(len(indentMarker.group(1))):
						blockCursor.deleteChar()
				if block.contains(cursor.selectionEnd()):
					break
				block = block.next()
		cursor.endEditBlock()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def search(self, pattern, **kwargs):
		"""
		This method searchs provided pattern in the document.

		:param pattern: Pattern to search for. ( String )
		:param \*\*kwargs: Format settings. ( Key / Value pairs )
		:return: Method success. ( Boolean )		
		"""

		settings = core.Structure(**{"caseSensitive" : False,
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
		else:
			if settings.wrapAround:
				previousCursor = self.textCursor()
				if settings.backwardSearch:
					cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
				else:
					cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
				self.setTextCursor(cursor)
				settings.wrapAround = False
				self.search(pattern, **settings)
				self.textCursor().isNull() and self.setTextCursor(previousCursor)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def searchNext(self):
		"""
		This method searchs the next search pattern in the document.

		:return: Method success. ( Boolean )		
		"""

		pattern = self.textCursor().selectedText() or self.__searchPattern
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

		pattern = self.textCursor().selectedText() or self.__searchPattern
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
		This method replaces current provided pattern occurence in the document with the replacement pattern.

		:param pattern: Pattern to replace. ( String )
		:param replacementPattern: Replacement pattern. ( String )
		:param \*\*kwargs: Format settings. ( Key / Value pairs )
		:return: Method success. ( Boolean )		
		"""

		if not self.search(pattern, **kwargs):
			return

		cursor = self.textCursor()
		cursor.beginEditBlock()
		if cursor.isNull():
			return

		if not cursor.hasSelection():
			return

		cursor.insertText(replacementPattern)
		cursor.endEditBlock()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def replaceAll(self, pattern, replacementPattern, **kwargs):
		"""
		This method replaces every provided pattern occurences in the document with the replacement pattern.

		:param pattern: Pattern to replace. ( String )
		:param replacementPattern: Replacement pattern. ( String )
		:param \*\*kwargs: Format settings. ( Key / Value pairs )
		:return: Method success. ( Boolean )		
		"""

		editCursor = self.textCursor()
		editCursor.beginEditBlock()
		while True:
			if not self.search(pattern, **kwargs):
				break

			cursor = self.textCursor()
			if cursor.isNull():
				break

			if not cursor.hasSelection():
				break
			cursor.insertText(replacementPattern)
		editCursor.endEditBlock()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setContent(self, content):
		"""
		This method sets document content while providing undo capability.

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
	def gotoLine(self, line):
		"""
		This method moves the text cursor to provided line.

		:return: Method success. ( Boolean )		
		"""

		cursor = self.textCursor()
		cursor.setPosition(0, QTextCursor.MoveAnchor)
		cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, line - 1)
		self.setTextCursor(cursor)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def toggleComments(self):
		"""
		This method toggles comments on the document selected lines.

		:return: Method success. ( Boolean )		
		"""

		cursor = self.textCursor()
		cursor.beginEditBlock()
		if not cursor.hasSelection():
			cursor.movePosition(QTextCursor.StartOfBlock)
			line = str(self.document().\
				 findBlockByNumber(cursor.blockNumber()).text())
			if line.startswith(self.__commentMarker):
				cursor.deleteChar()
			else:
				cursor.insertText(self.__commentMarker)
		else:
			block = self.document().findBlock(cursor.selectionStart())
			while True:
				blockCursor = self.textCursor()
				blockCursor.setPosition(block.position())

				if str(block.text()).startswith(self.__commentMarker):
					blockCursor.deleteChar()
				else:
					blockCursor.insertText(self.__commentMarker)

				if block.contains(cursor.selectionEnd()):
					break
				block = block.next()
		cursor.endEditBlock()
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
		This method toggles document white spaces.

		:return: Method success. ( Boolean )		
		"""

		textOption = self.getDefaultTextOption()
		if textOption.flags().__int__():
			textOption = QTextOption()
			textOption.setTabStop(self.tabStopWidth())
		else:
			textOption.setFlags(textOption.flags() | QTextOption.ShowTabsAndSpaces | QTextOption.ShowLineAndParagraphSeparators)
		self.setDefaultTextOption(textOption)
		return True
