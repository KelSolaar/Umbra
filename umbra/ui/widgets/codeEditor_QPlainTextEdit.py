#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**codeEditor_QPlainTextEdit.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	| This module defines the :class:`LinesNumbers_QWidget` and :class:`CodeEditor_QPlainTextEdit` classes.
	| Those objects provides the basics building blocks of a code editor widget.

**Others:**
	Portions of the code from codeeditor.py by Roberto Alsina: http://lateral.netmanagers.com.ar/weblog/posts/BB832.html,
	KhtEditor.py by Benoit Hervier: http://khertan.net/khteditor, Ninja IDE: http://ninja-ide.org/ and
	Prymatex: https://github.com/D3f0/prymatex/
"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import re
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QBrush
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QCompleter
from PyQt4.QtGui import QFontMetrics
from PyQt4.QtGui import QPainter
from PyQt4.QtGui import QPen
from PyQt4.QtGui import QSyntaxHighlighter
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextDocument
from PyQt4.QtGui import QWidget

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
from umbra.globals.constants import Constants
from umbra.ui.widgets.basic_QPlainTextEdit import Basic_QPlainTextEdit
from umbra.ui.widgets.basic_QPlainTextEdit import editBlock
from umbra.ui.widgets.basic_QPlainTextEdit import anchorTextCursor

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "LinesNumbers_QWidget", "CodeEditor_QPlainTextEdit"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class LinesNumbers_QWidget(QWidget):
	"""
	This class is a `QWidget <http://doc.qt.nokia.com/qwidget.html>`_ subclass providing a lines numbers widget.
	"""

	@core.executionTrace
	def __init__(self, parent, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QWidget.__init__(self, parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__editor = parent

		self.__margin = 16
		self.__separatorWidth = 2
		self.__backgroundColor = QColor(48, 48, 48)
		self.__color = QColor(192, 192, 192)
		self.__separatorColor = QColor(88, 88, 88)

		self.setEditorViewportMargins(0)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def editor(self):
		"""
		This method is the property for **self.__editor** attribute.

		:return: self.__editor. ( QWidget )
		"""

		return self.__editor

	@editor.setter
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "editor"))

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

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("margin", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("margin", value)
		self.__margin = value

	@margin.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def margin(self):
		"""
		This method is the deleter method for **self.__margin** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "margin"))

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

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("separatorWidth", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("separatorWidth", value)
		self.__separatorWidth = value

	@separatorWidth.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def separatorWidth(self):
		"""
		This method is the deleter method for **self.__separatorWidth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "separatorWidth"))

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

		if value is not None:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("backgroundColor", value)
		self.__backgroundColor = value

	@backgroundColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def backgroundColor(self):
		"""
		This method is the deleter method for **self.__backgroundColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "backgroundColor"))

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

		if value is not None:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("color", value)
		self.__color = value

	@color.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def color(self):
		"""
		This method is the deleter method for **self.__color** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "color"))

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

		if value is not None:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("separatorColor", value)
		self.__separatorColor = value

	@separatorColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def separatorColor(self):
		"""
		This method is the deleter method for **self.__separatorColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "separatorColor"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	# @core.executionTrace
	def sizeHint(self):
		"""
		This method reimplements the :meth:`QWidget.sizeHint` method.

		:return: Size hint. ( QSize )
		"""

		return QSize(self.getWidth(), 0)

	# @core.executionTrace
	def paintEvent(self, event):
		"""
		This method reimplements the :meth:`QWidget.paintEvent` method.
		
		:param event: Event. ( QEvent )
		"""

		def __setBold(state):
			"""
			This definition sets the current painter font bold state.

			:return: Definiton success. ( Boolean )
			"""

			font = painter.font()
			font.setBold(state)
			painter.setFont(font)
			return True

		painter = QPainter(self)
		painter.fillRect(event.rect(), self.__backgroundColor)

		pen = QPen(QBrush(), self.__separatorWidth)
		pen.setColor(self.__separatorColor)
		painter.setPen(pen)
		topRightCorner = event.rect().topRight()
		bottomRightCorner = event.rect().bottomRight()
		painter.drawLine(topRightCorner.x(), topRightCorner.y(), bottomRightCorner.x(), bottomRightCorner.y())
		painter.setPen(self.__color)

		viewportHeight = self.__editor.viewport().height()
		metrics = QFontMetrics(self.__editor.document().defaultFont())
		currentBlock = self.__editor.document().findBlock(
			self.__editor.textCursor().position())

		block = self.__editor.firstVisibleBlock()
		blockNumber = block.blockNumber()
		painter.setFont(self.__editor.document().defaultFont())

		while block.isValid():
			blockNumber += 1
			position = self.__editor.blockBoundingGeometry(block).topLeft() + self.__editor.contentOffset()
			if position.y() > viewportHeight:
				break

			if not block.isVisible():
				continue

			block == currentBlock and __setBold(True) or __setBold(False)
			painter.drawText(self.width() - metrics.width(strings.encode(blockNumber)) - self.__margin / 3,
							round(position.y() + metrics.ascent() + metrics.descent() - \
							(self.__editor.blockBoundingRect(block).height() * 8.0 / 100)),
							strings.encode(blockNumber))
			block = block.next()

		painter.end()
		QWidget.paintEvent(self, event)

	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getWidth(self):
		"""
		This method returns the Widget target width.

		:return: Widget target width. ( Integer )
		"""

		return self.__margin + self.__editor.fontMetrics().width(strings.encode(max(1, self.__editor.blockCount())))

	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setEditorViewportMargins(self, newBlocksCount):
		"""
		This method sets the editor viewport margins.
		
		:param newBlocksCount: Updated editor blocks count. ( Integer )
		:return: Method success. ( Boolean )
		"""

		self.__editor.setViewportMargins(self.getWidth(), 0, 0, 0)
		return True

	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
	def updateRectangle(self, rectangle, scrollY):
		"""
		This method updates the given widget rectangle.
		
		:param rectangle: Rectangle to update. ( QRect )
		:param scrollY: Amount of pixels the viewport was scrolled. ( Integer )
		:return: Method success. ( Boolean )
		"""

		if scrollY:
			self.scroll(0, scrollY)
		else:
			self.update(0, rectangle.y(), self.width(), rectangle.height())

		if rectangle.contains(self.__editor.viewport().rect()):
			self.setEditorViewportMargins(0)
		return True

	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
	def updateGeometry(self):
		"""
		This method updates the widget geometry.
		
		:return: Method success. ( Boolean )
		"""

		self.setGeometry(self.__editor.contentsRect().left(),
						self.__editor.contentsRect().top(),
						self.getWidth(),
						self.__editor.contentsRect().height())
		return True

class CodeEditor_QPlainTextEdit(Basic_QPlainTextEdit):
	"""
	This class provides	a code editor base class.
	"""

	@core.executionTrace
	def __init__(self, parent=None, indentMarker="\t", indentWidth=4, commentMarker="#", *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		:param indentMarker: Indentation marker. ( String )
		:param indentWidth: Indentation spaces count. ( Integer )
		:param commentMarker: Comment marker. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		Basic_QPlainTextEdit.__init__(self, parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__indentMarker = None
		self.indentMarker = indentMarker
		self.__indentWidth = None
		self.indentWidth = indentWidth
		self.__commentMarker = None
		self.commentMarker = commentMarker

		self.__marginArea_LinesNumbers_widget = None
		self.__highlighter = None
		self.__completer = None

		self.__occurrencesHighlightColor = QColor(80, 80, 80)

		self.__preInputAccelerators = []
		self.__postInputAccelerators = []
		self.__visualAccelerators = []

		self.__textCursorAnchor = None

		CodeEditor_QPlainTextEdit.__initializeUi(self)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"indentMarker", value)
			assert re.search(r"\s", value), "'{0}' attribute: '{1}' is not a whitespace character!".format(
			"indentMarker", value)
		self.__indentMarker = value

	@indentMarker.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def indentMarker(self):
		"""
		This method is the deleter method for **self.__indentMarker** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "indentMarker"))

	@property
	def indentWidth(self):
		"""
		This method is the property for **self.__indentWidth** attribute.

		:return: self.__indentWidth. ( Integer )
		"""

		return self.__indentWidth

	@indentWidth.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def indentWidth(self, value):
		"""
		This method is the setter method for **self.__indentWidth** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("indentWidth", value)
		self.__indentWidth = value

	@indentWidth.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def indentWidth(self):
		"""
		This method is the deleter method for **self.__indentWidth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "indentWidth"))

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

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"commentMarker", value)
		self.__commentMarker = value

	@commentMarker.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def commentMarker(self):
		"""
		This method is the deleter method for **self.__commentMarker** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "commentMarker"))

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

		if value is not None:
			assert type(value) is LinesNumbers_QWidget, \
			"'{0}' attribute: '{1}' type is not 'LinesNumbers_QWidget'!".format("checked", value)
		self.__marginArea_LinesNumbers_widget = value

	@marginArea_LinesNumbers_widget.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def marginArea_LinesNumbers_widget(self):
		"""
		This method is the deleter method for **self.__marginArea_LinesNumbers_widget** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "marginArea_LinesNumbers_widget"))

	@property
	def highlighter(self):
		"""
		This method is the property for **self.__highlighter** attribute.

		:return: self.__highlighter. ( QSyntaxHighlighter )
		"""

		return self.__highlighter

	@highlighter.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def highlighter(self, value):
		"""
		This method is the setter method for **self.__highlighter** attribute.

		:param value: Attribute value. ( QSyntaxHighlighter )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "highlighter"))

	@highlighter.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def highlighter(self):
		"""
		This method is the deleter method for **self.__highlighter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "highlighter"))

	@property
	def completer(self):
		"""
		This method is the property for **self.__completer** attribute.

		:return: self.__completer. ( QCompleter )
		"""

		return self.__completer

	@completer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completer(self, value):
		"""
		This method is the setter method for **self.__completer** attribute.

		:param value: Attribute value. ( QCompleter )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "completer"))

	@completer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def completer(self):
		"""
		This method is the deleter method for **self.__completer** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "completer"))

	@property
	def preInputAccelerators(self):
		"""
		This method is the property for **self.__preInputAccelerators** attribute.

		:return: self.__preInputAccelerators. ( Tuple / List )
		"""

		return self.__preInputAccelerators

	@preInputAccelerators.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def preInputAccelerators(self, value):
		"""
		This method is the setter method for **self.__preInputAccelerators** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
			"preInputAccelerators", value)
		self.__preInputAccelerators = value

	@preInputAccelerators.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def preInputAccelerators(self):
		"""
		This method is the deleter method for **self.__preInputAccelerators** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "preInputAccelerators"))

	@property
	def postInputAccelerators(self):
		"""
		This method is the property for **self.__postInputAccelerators** attribute.

		:return: self.__postInputAccelerators. ( Tuple / List )
		"""

		return self.__postInputAccelerators

	@postInputAccelerators.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def postInputAccelerators(self, value):
		"""
		This method is the setter method for **self.__postInputAccelerators** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
			"postInputAccelerators", value)
		self.__postInputAccelerators = value

	@postInputAccelerators.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def postInputAccelerators(self):
		"""
		This method is the deleter method for **self.__postInputAccelerators** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "postInputAccelerators"))

	@property
	def visualAccelerators(self):
		"""
		This method is the property for **self.__visualAccelerators** attribute.

		:return: self.__visualAccelerators. ( Tuple / List )
		"""

		return self.__visualAccelerators

	@visualAccelerators.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def visualAccelerators(self, value):
		"""
		This method is the setter method for **self.__visualAccelerators** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
			"visualAccelerators", value)
		self.__visualAccelerators = value

	@visualAccelerators.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def visualAccelerators(self):
		"""
		This method is the deleter method for **self.__visualAccelerators** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "visualAccelerators"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		self.__marginArea_LinesNumbers_widget = LinesNumbers_QWidget(self)

		self.__setExtraSelections()

		# Signals / Slots.
		self.blockCountChanged.connect(self.__marginArea_LinesNumbers_widget.setEditorViewportMargins)
		self.updateRequest.connect(self.__marginArea_LinesNumbers_widget.updateRectangle)
		self.cursorPositionChanged.connect(self.__setExtraSelections)

	@core.executionTrace
	def resizeEvent(self, event):
		"""
		This method reimplements the :meth:`Basic_QPlainTextEdit.resizeEvent` method.

		:param event: Event. ( QEvent )
		"""

		Basic_QPlainTextEdit.resizeEvent(self, event)
		self.__marginArea_LinesNumbers_widget.updateGeometry()

	@core.executionTrace
	@editBlock
	def keyPressEvent(self, event):
		"""
		This method reimplements the :meth:`Basic_QPlainTextEdit.keyPressEvent` method.

		:param event: Event. ( QEvent )
		"""

		processEvent = True
		for accelerator in self.__preInputAccelerators:
			processEvent *= accelerator(self, event)

		if not processEvent:
			return

		Basic_QPlainTextEdit.keyPressEvent(self, event)

		for accelerator in self.__postInputAccelerators:
			accelerator(self, event)

	# @core.executionTrace
	def __setExtraSelections(self):
		"""
		This method sets current document extra selections.
		"""

		self.setExtraSelections(())
		for accelerator in self.__visualAccelerators:
			accelerator(self)

	@core.executionTrace
	def __insertCompletion(self, completion):
		"""
		This method inserts the completion text in the current document.

		:param completion: Completion text. ( QString )
		"""

		LOGGER.debug("> Inserting '{0}' completion.".format(completion))

		textCursor = self.textCursor()
		extra = (completion.length() - self.__completer.completionPrefix().length())
		textCursor.insertText(completion.right(extra))
		self.setTextCursor(textCursor)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def setHighlighter(self, highlighter):
		"""
		This method sets given highlighter as the current document highlighter.

		:param highlighter: Highlighter. ( QSyntaxHighlighter )
		:return: Method success. ( Boolean )
		"""

		if not issubclass(highlighter.__class__, QSyntaxHighlighter):
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' is not a 'QSyntaxHighlighter' subclass!".format(
			self.__class__.__name__, highlighter))

		if self.__highlighter:
			self.removeHighlighter()

		LOGGER.debug("> Setting '{0}' highlighter.".format(highlighter))
		self.__highlighter = highlighter

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeHighlighter(self):
		"""
		This method removes current highlighter.

		:return: Method success. ( Boolean )
		"""

		if self.__highlighter:
			LOGGER.debug("> Removing '{0}' highlighter.".format(self.__highlighter))
			self.__highlighter.deleteLater()
			self.__highlighter = None
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def setCompleter(self, completer):
		"""
		This method sets given completer as the current completer.

		:param completer: Completer. ( QCompleter )
		:return: Method success. ( Boolean )
		"""

		if not issubclass(completer.__class__, QCompleter):
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' is not a 'QCompleter' subclass!".format(
			self.__class__.__name__, completer))

		if self.__completer:
			self.removeCompleter()

		LOGGER.debug("> Setting '{0}' completer.".format(completer))
		self.__completer = completer
		self.__completer.setWidget(self)

		# Signals / Slots.
		self.__completer.activated.connect(self.__insertCompletion)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeCompleter(self):
		"""
		This method removes current completer.

		:return: Method success. ( Boolean )
		"""

		if self.__completer:
			LOGGER.debug("> Removing '{0}' completer.".format(self.__completer))
			# Signals / Slots.
			self.__completer.activated.disconnect(self.__insertCompletion)

			self.__completer.deleteLater()
			self.__completer = None
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getMatchingSymbolsPairs(self, cursor, openingSymbol, closingSymbol, backward=False):
		"""
		This method returns the cursor for matching given symbols pairs.

		:param cursor: Cursor to match from. ( QTextCursor )
		:param openingSymbol: Opening symbol. ( String )
		:param closingSymbol: Closing symbol to match. ( String )
		:return: Matching cursor. ( QTextCursor )
		"""

		if cursor.hasSelection():
			startPosition = cursor.selectionEnd() if backward else cursor.selectionStart()
		else:
			startPosition = cursor.position()

		flags = QTextDocument.FindFlags()
		if backward:
			flags = flags | QTextDocument.FindBackward

		startCursor = previousStartCursor = cursor.document().find(openingSymbol, startPosition, flags)
		endCursor = previousEndCursor = cursor.document().find(closingSymbol, startPosition, flags)
		if backward:
			while startCursor > endCursor:
				startCursor = cursor.document().find(openingSymbol, startCursor.selectionStart(), flags)
				if startCursor > endCursor:
					endCursor = cursor.document().find(closingSymbol, endCursor.selectionStart(), flags)
		else:
			while startCursor < endCursor:
				startCursor = cursor.document().find(openingSymbol, startCursor.selectionEnd(), flags)
				if startCursor < endCursor:
					endCursor = cursor.document().find(closingSymbol, endCursor.selectionEnd(), flags)

		return endCursor.position() != -1 and endCursor or previousEndCursor

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	@editBlock
	def indent(self):
		"""
		This method indents the document text under cursor.

		:return: Method success. ( Boolean )
		"""

		cursor = self.textCursor()
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
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	@editBlock
	def unindent(self):
		"""
		This method unindents the document text under cursor.

		:return: Method success. ( Boolean )
		"""

		cursor = self.textCursor()
		if not cursor.hasSelection():
			cursor.movePosition(QTextCursor.StartOfBlock)
			line = strings.encode(self.document().findBlockByNumber(cursor.blockNumber()).text())
			indentMarker = re.match(r"({0})".format(self.__indentMarker), line)
			if indentMarker:
				foundations.common.repeat(cursor.deleteChar, len(indentMarker.group(1)))
		else:
			block = self.document().findBlock(cursor.selectionStart())
			while True:
				blockCursor = self.textCursor()
				blockCursor.setPosition(block.position())
				indentMarker = re.match(r"({0})".format(self.__indentMarker), block.text())
				if indentMarker:
					foundations.common.repeat(blockCursor.deleteChar, len(indentMarker.group(1)))
				if block.contains(cursor.selectionEnd()):
					break
				block = block.next()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	@editBlock
	def toggleComments(self):
		"""
		This method toggles comments on the document selected lines.

		:return: Method success. ( Boolean )
		"""

		if not self.__commentMarker:
			return True

		cursor = self.textCursor()
		if not cursor.hasSelection():
			cursor.movePosition(QTextCursor.StartOfBlock)
			line = strings.encode(self.document().findBlockByNumber(cursor.blockNumber()).text())
			if line.startswith(self.__commentMarker):
				foundations.common.repeat(cursor.deleteChar, len(self.__commentMarker))
			else:
				cursor.insertText(self.__commentMarker)
		else:
			block = self.document().findBlock(cursor.selectionStart())
			while True:
				blockCursor = self.textCursor()
				blockCursor.setPosition(block.position())

				if strings.encode(block.text()).startswith(self.__commentMarker):
					foundations.common.repeat(blockCursor.deleteChar, len(self.__commentMarker))
				else:
					blockCursor.insertText(self.__commentMarker)

				if block.contains(cursor.selectionEnd()):
					break
				block = block.next()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	@anchorTextCursor
	@editBlock
	def removeTrailingWhiteSpaces(self):
		"""
		This method removes document trailing white spaces.

		:return: Method success. ( Boolean )
		"""

		cursor = self.textCursor()

		block = self.document().findBlockByLineNumber(0)
		while block.isValid():
			cursor.setPosition(block.position())
			if re.search(r"\s+$", block.text()):
				cursor.movePosition(QTextCursor.EndOfBlock)
				cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
				cursor.insertText(strings.encode(block.text()).rstrip())
			block = block.next()
		cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
		if not cursor.block().text().isEmpty():
			cursor.insertText("\n")
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	@anchorTextCursor
	@editBlock
	def convertIndentationToTabs(self):
		"""
		This method converts document indentation to tabs.

		:return: Method success. ( Boolean )
		"""

		cursor = self.textCursor()

		block = self.document().findBlockByLineNumber(0)
		while block.isValid():
			cursor.setPosition(block.position())
			search = re.match(r"^ +", block.text())
			if search:
				cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
				searchLength = len(search.group(0))
				foundations.common.repeat(
				lambda: cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor), searchLength)
				cursor.insertText(self.__indentMarker * (searchLength / self.__indentWidth))
			block = block.next()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	@anchorTextCursor
	@editBlock
	def convertIndentationToSpaces(self):
		"""
		This method converts document indentation to spaces.

		:return: Method success. ( Boolean )
		"""

		cursor = self.textCursor()

		block = self.document().findBlockByLineNumber(0)
		while block.isValid():
			cursor.setPosition(block.position())
			search = re.match(r"^\t+", block.text())
			if search:
				cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
				searchLength = len(search.group(0))
				foundations.common.repeat(
				lambda: cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor), searchLength)
				cursor.insertText(" " * (searchLength * self.__indentWidth))
			block = block.next()
		return True

