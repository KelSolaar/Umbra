#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**codeEditor_QPlainTextEdit.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	| Defines the :class:`LinesNumbers_QWidget` and :class:`CodeEditor_QPlainTextEdit` classes.
	| Those objects provides the basics building blocks of a code editor widget.

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
import re
from PyQt4.QtCore import QSize
from PyQt4.QtCore import pyqtSignal
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
import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.ui.common
import umbra.ui.languages
from umbra.ui.widgets.basic_QPlainTextEdit import Basic_QPlainTextEdit
from umbra.ui.widgets.basic_QPlainTextEdit import editBlock
from umbra.ui.widgets.basic_QPlainTextEdit import anchorTextCursor

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "LinesNumbers_QWidget",
		"CodeEditor_QPlainTextEdit"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class LinesNumbers_QWidget(QWidget):
	"""
	Defines a `QWidget <http://doc.qt.nokia.com/qwidget.html>`_ subclass providing a lines numbers widget.
	"""

	def __init__(self, parent, *args, **kwargs):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QWidget.__init__(self, parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__editor = parent

		self.__margin = 16
		self.__separatorWidth = 4
		self.__backgroundColor = QColor(48, 48, 48)
		self.__color = QColor(192, 192, 192)
		self.__separatorColor = QColor(48, 48, 48)

		self.setEditorViewportMargins(0)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def editor(self):
		"""
		Property for **self.__editor** attribute.

		:return: self.__editor.
		:rtype: QWidget
		"""

		return self.__editor

	@editor.setter
	def editor(self, value):
		"""
		Setter for **self.__editor** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		self.__editor = value

	@editor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def editor(self):
		"""
		Deleter for **self.__editor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "editor"))

	@property
	def margin(self):
		"""
		Property for **self.__margin** attribute.

		:return: self.__margin.
		:rtype: int
		"""

		return self.__margin

	@margin.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def margin(self, value):
		"""
		Setter for **self.__margin** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("margin", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("margin", value)
		self.__margin = value

	@margin.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def margin(self):
		"""
		Deleter for **self.__margin** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "margin"))

	@property
	def separatorWidth(self):
		"""
		Property for **self.__separatorWidth** attribute.

		:return: self.__separatorWidth.
		:rtype: int
		"""

		return self.__separatorWidth

	@separatorWidth.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def separatorWidth(self, value):
		"""
		Setter for **self.__separatorWidth** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("separatorWidth", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("separatorWidth", value)
		self.__separatorWidth = value

	@separatorWidth.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def separatorWidth(self):
		"""
		Deleter for **self.__separatorWidth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "separatorWidth"))

	@property
	def backgroundColor(self):
		"""
		Property for **self.__backgroundColor** attribute.

		:return: self.__backgroundColor.
		:rtype: QColor
		"""

		return self.__backgroundColor

	@backgroundColor.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def backgroundColor(self, value):
		"""
		Setter for **self.__backgroundColor** attribute.

		:param value: Attribute value.
		:type value: QColor
		"""

		if value is not None:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("backgroundColor", value)
		self.__backgroundColor = value

	@backgroundColor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def backgroundColor(self):
		"""
		Deleter for **self.__backgroundColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "backgroundColor"))

	@property
	def color(self):
		"""
		Property for **self.__color** attribute.

		:return: self.__color.
		:rtype: QColor
		"""

		return self.__color

	@color.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def color(self, value):
		"""
		Setter for **self.__color** attribute.

		:param value: Attribute value.
		:type value: QColor
		"""

		if value is not None:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("color", value)
		self.__color = value

	@color.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def color(self):
		"""
		Deleter for **self.__color** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "color"))

	@property
	def separatorColor(self):
		"""
		Property for **self.__separatorColor** attribute.

		:return: self.__separatorColor.
		:rtype: QColor
		"""

		return self.__separatorColor

	@separatorColor.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def separatorColor(self, value):
		"""
		Setter for **self.__separatorColor** attribute.

		:param value: Attribute value.
		:type value: QColor
		"""

		if value is not None:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("separatorColor", value)
		self.__separatorColor = value

	@separatorColor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def separatorColor(self):
		"""
		Deleter for **self.__separatorColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "separatorColor"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def sizeHint(self):
		"""
		Reimplements the :meth:`QWidget.sizeHint` method.

		:return: Size hint.
		:rtype: QSize
		"""

		return QSize(self.getWidth(), 0)

	def paintEvent(self, event):
		"""
		Reimplements the :meth:`QWidget.paintEvent` method.
		
		:param event: Event.
		:type event: QEvent
		"""

		def __setBold(state):
			"""
			Sets the current painter font bold state.

			:return: Definiton success.
			:rtype: bool
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
			painter.drawText(self.width() - metrics.width(foundations.strings.toString(blockNumber)) - self.__margin / 3,
							round(position.y() + metrics.ascent() + metrics.descent() - \
							(self.__editor.blockBoundingRect(block).height() * 8.0 / 100)),
							foundations.strings.toString(blockNumber))
			block = block.next()

		painter.end()
		QWidget.paintEvent(self, event)

	def getWidth(self):
		"""
		Returns the Widget target width.

		:return: Widget target width.
		:rtype: int
		"""

		return self.__margin + \
		self.__editor.fontMetrics().width(foundations.strings.toString(max(1, self.__editor.blockCount())))

	def setEditorViewportMargins(self, newBlocksCount):
		"""
		Sets the editor viewport margins.
		
		:param newBlocksCount: Updated editor blocks count.
		:type newBlocksCount: int
		:return: Method success.
		:rtype: bool
		"""

		self.__editor.setViewportMargins(self.getWidth(), 0, 0, 0)
		return True

	def updateRectangle(self, rectangle, scrollY):
		"""
		Updates the given Widget rectangle.
		
		:param rectangle: Rectangle to update.
		:type rectangle: QRect
		:param scrollY: Amount of pixels the viewport was scrolled.
		:type scrollY: int
		:return: Method success.
		:rtype: bool
		"""

		if scrollY:
			self.scroll(0, scrollY)
		else:
			self.update(0, rectangle.y(), self.width(), rectangle.height())

		if rectangle.contains(self.__editor.viewport().rect()):
			self.setEditorViewportMargins(0)
		return True

	def updateGeometry(self):
		"""
		Updates the Widget geometry.
		
		:return: Method success.
		:rtype: bool
		"""

		self.setGeometry(self.__editor.contentsRect().left(),
						self.__editor.contentsRect().top(),
						self.getWidth(),
						self.__editor.contentsRect().height())
		return True

class CodeEditor_QPlainTextEdit(Basic_QPlainTextEdit):
	"""
	Defines	a code editor base class.
	"""

	languageChanged = pyqtSignal()
	"""
	This signal is emited by the :class:`Editor` class when :obj:`ComponentsManagerUi.language` class property language
	is changed. ( pyqtSignal )
	"""

	def __init__(self,
				parent=None,
				language=umbra.ui.languages.PYTHON_LANGUAGE,
				indentMarker="\t",
				indentWidth=4,
				commentMarker="#",
				*args,
				**kwargs):
		"""
		Initializes the class.

		:param parent: Widget parent.
		:type parent: QObject
		:param language: Editor language.
		:type language: Language
		:param indentMarker: Indentation marker.
		:type indentMarker: unicode
		:param indentWidth: Indentation spaces count.
		:type indentWidth: int
		:param commentMarker: Comment marker.
		:type commentMarker: unicode
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		Basic_QPlainTextEdit.__init__(self, parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__language = language

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
	def language(self):
		"""
		Property for **self.__language** attribute.

		:return: self.__language.
		:rtype: Language
		"""

		return self.__language

	@language.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def language(self, value):
		"""
		Setter for **self.__language** attribute.

		:param value: Attribute value.
		:type value: Language
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "language"))

	@language.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def language(self):
		"""
		Deleter for **self.__language** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "language"))


	@property
	def indentMarker(self):
		"""
		Property for **self.__indentMarker** attribute.

		:return: self.__indentMarker.
		:rtype: unicode
		"""

		return self.__indentMarker

	@indentMarker.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def indentMarker(self, value):
		"""
		Setter for **self.__indentMarker** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"indentMarker", value)
			assert re.search(r"\s", value), "'{0}' attribute: '{1}' is not a whitespace character!".format(
			"indentMarker", value)
		self.__indentMarker = value

	@indentMarker.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def indentMarker(self):
		"""
		Deleter for **self.__indentMarker** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "indentMarker"))

	@property
	def indentWidth(self):
		"""
		Property for **self.__indentWidth** attribute.

		:return: self.__indentWidth.
		:rtype: int
		"""

		return self.__indentWidth

	@indentWidth.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def indentWidth(self, value):
		"""
		Setter for **self.__indentWidth** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("indentWidth", value)
		self.__indentWidth = value

	@indentWidth.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def indentWidth(self):
		"""
		Deleter for **self.__indentWidth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "indentWidth"))

	@property
	def commentMarker(self):
		"""
		Property for **self.__commentMarker** attribute.

		:return: self.__commentMarker.
		:rtype: unicode
		"""

		return self.__commentMarker

	@commentMarker.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def commentMarker(self, value):
		"""
		Setter for **self.__commentMarker** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"commentMarker", value)
		self.__commentMarker = value

	@commentMarker.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def commentMarker(self):
		"""
		Deleter for **self.__commentMarker** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "commentMarker"))

	@property
	def marginArea_LinesNumbers_widget(self):
		"""
		Property for **self.__marginArea_LinesNumbers_widget** attribute.

		:return: self.__marginArea_LinesNumbers_widget.
		:rtype: LinesNumbers_QWidget
		"""

		return self.__marginArea_LinesNumbers_widget

	@marginArea_LinesNumbers_widget.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def marginArea_LinesNumbers_widget(self, value):
		"""
		Setter for **self.__marginArea_LinesNumbers_widget** attribute.

		:param value: Attribute value.
		:type value: LinesNumbers_QWidget
		"""

		if value is not None:
			assert type(value) is LinesNumbers_QWidget, \
			"'{0}' attribute: '{1}' type is not 'LinesNumbers_QWidget'!".format("checked", value)
		self.__marginArea_LinesNumbers_widget = value

	@marginArea_LinesNumbers_widget.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def marginArea_LinesNumbers_widget(self):
		"""
		Deleter for **self.__marginArea_LinesNumbers_widget** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "marginArea_LinesNumbers_widget"))

	@property
	def highlighter(self):
		"""
		Property for **self.__highlighter** attribute.

		:return: self.__highlighter.
		:rtype: QSyntaxHighlighter
		"""

		return self.__highlighter

	@highlighter.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def highlighter(self, value):
		"""
		Setter for **self.__highlighter** attribute.

		:param value: Attribute value.
		:type value: QSyntaxHighlighter
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "highlighter"))

	@highlighter.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def highlighter(self):
		"""
		Deleter for **self.__highlighter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "highlighter"))

	@property
	def completer(self):
		"""
		Property for **self.__completer** attribute.

		:return: self.__completer.
		:rtype: QCompleter
		"""

		return self.__completer

	@completer.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def completer(self, value):
		"""
		Setter for **self.__completer** attribute.

		:param value: Attribute value.
		:type value: QCompleter
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "completer"))

	@completer.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def completer(self):
		"""
		Deleter for **self.__completer** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "completer"))

	@property
	def preInputAccelerators(self):
		"""
		Property for **self.__preInputAccelerators** attribute.

		:return: self.__preInputAccelerators.
		:rtype: tuple or list
		"""

		return self.__preInputAccelerators

	@preInputAccelerators.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def preInputAccelerators(self, value):
		"""
		Setter for **self.__preInputAccelerators** attribute.

		:param value: Attribute value.
		:type value: tuple or list
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
			"preInputAccelerators", value)
		self.__preInputAccelerators = value

	@preInputAccelerators.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def preInputAccelerators(self):
		"""
		Deleter for **self.__preInputAccelerators** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "preInputAccelerators"))

	@property
	def postInputAccelerators(self):
		"""
		Property for **self.__postInputAccelerators** attribute.

		:return: self.__postInputAccelerators.
		:rtype: tuple or list
		"""

		return self.__postInputAccelerators

	@postInputAccelerators.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def postInputAccelerators(self, value):
		"""
		Setter for **self.__postInputAccelerators** attribute.

		:param value: Attribute value.
		:type value: tuple or list
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
			"postInputAccelerators", value)
		self.__postInputAccelerators = value

	@postInputAccelerators.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def postInputAccelerators(self):
		"""
		Deleter for **self.__postInputAccelerators** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "postInputAccelerators"))

	@property
	def visualAccelerators(self):
		"""
		Property for **self.__visualAccelerators** attribute.

		:return: self.__visualAccelerators.
		:rtype: tuple or list
		"""

		return self.__visualAccelerators

	@visualAccelerators.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def visualAccelerators(self, value):
		"""
		Setter for **self.__visualAccelerators** attribute.

		:param value: Attribute value.
		:type value: tuple or list
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
			"visualAccelerators", value)
		self.__visualAccelerators = value

	@visualAccelerators.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def visualAccelerators(self):
		"""
		Deleter for **self.__visualAccelerators** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "visualAccelerators"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeUi(self):
		"""
		Initializes the Widget ui.
		"""

		self.__marginArea_LinesNumbers_widget = LinesNumbers_QWidget(self)

		self.__setExtraSelections()

		self.__setLanguageDescription()

		# Signals / Slots.
		self.blockCountChanged.connect(self.__marginArea_LinesNumbers_widget.setEditorViewportMargins)
		self.updateRequest.connect(self.__marginArea_LinesNumbers_widget.updateRectangle)
		self.cursorPositionChanged.connect(self.__setExtraSelections)

	def resizeEvent(self, event):
		"""
		Reimplements the :meth:`Basic_QPlainTextEdit.resizeEvent` method.

		:param event: Event.
		:type event: QEvent
		"""

		Basic_QPlainTextEdit.resizeEvent(self, event)
		self.__marginArea_LinesNumbers_widget.updateGeometry()

	@editBlock
	def keyPressEvent(self, event):
		"""
		Reimplements the :meth:`Basic_QPlainTextEdit.keyPressEvent` method.

		:param event: Event.
		:type event: QEvent
		"""

		processEvent = True
		for accelerator in self.__preInputAccelerators:
			processEvent *= accelerator(self, event)

		if not processEvent:
			return

		Basic_QPlainTextEdit.keyPressEvent(self, event)

		for accelerator in self.__postInputAccelerators:
			accelerator(self, event)

	def __setExtraSelections(self):
		"""
		Sets current document extra selections.
		"""

		self.setExtraSelections(())
		for accelerator in self.__visualAccelerators:
			accelerator(self)

	def __insertCompletion(self, completion):
		"""
		Inserts the completion text in the current document.

		:param completion: Completion text.
		:type completion: QString
		"""

		LOGGER.debug("> Inserting '{0}' completion.".format(completion))

		textCursor = self.textCursor()
		extra = (completion.length() - self.__completer.completionPrefix().length())
		textCursor.insertText(completion.right(extra))
		self.setTextCursor(textCursor)

	def __setLanguageDescription(self):
		"""
		Sets the language accelerators.
		"""

		LOGGER.debug("> Setting language description.")

		if not self.__language:
			return

		if self.__language.highlighter:
			self.setHighlighter(self.__language.highlighter(self.document(),
															self.__language.rules,
															self.__language.theme))
			self.highlighter.rehighlight()
		else:
			self.removeHighlighter()

		if self.__language.completer:
			self.setCompleter(self.__language.completer(self.parent(), self.__language.name, self.__language.tokens))
		else:
			self.removeCompleter()

		self.indentMarker = self.__language.indentMarker
		self.commentMarker = self.__language.commentMarker
		self.preInputAccelerators = self.__language.preInputAccelerators
		self.postInputAccelerators = self.__language.postInputAccelerators
		self.visualAccelerators = self.__language.visualAccelerators

		color = "rgb({0}, {1}, {2})"
		background = self.__language.theme.get("default").background()
		foreground = self.__language.theme.get("default").foreground()
		self.setStyleSheet(
		"QPlainTextEdit{{ background-color: {0}; color: {1}; }}".format(color.format(background.color().red(),
																								background.color().green(),
																								background.color().blue()),
																				color.format(foreground.color().red(),
																							foreground.color().green(),
																							foreground.color().blue())))

		self.__tabWidth = self.fontMetrics().width(" " * self.indentWidth)
		self.setTabStopWidth(self.__tabWidth)

	def setLanguage(self, language):
		"""
		Sets the language.

		:param language: Language to set.
		:type language: Language
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Setting editor language to '{0}'.".format(language.name))
		self.__language = language or  umbra.ui.languages.PYTHON_LANGUAGE
		self.__setLanguageDescription()
		self.languageChanged.emit()
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def setHighlighter(self, highlighter):
		"""
		Sets given highlighter as the current document highlighter.

		:param highlighter: Highlighter.
		:type highlighter: QSyntaxHighlighter
		:return: Method success.
		:rtype: bool
		"""

		if not issubclass(highlighter.__class__, QSyntaxHighlighter):
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' is not a 'QSyntaxHighlighter' subclass!".format(
			self.__class__.__name__, highlighter))

		if self.__highlighter:
			self.removeHighlighter()

		LOGGER.debug("> Setting '{0}' highlighter.".format(highlighter))
		self.__highlighter = highlighter

		return True

	def removeHighlighter(self):
		"""
		Removes current highlighter.

		:return: Method success.
		:rtype: bool
		"""

		if self.__highlighter:
			LOGGER.debug("> Removing '{0}' highlighter.".format(self.__highlighter))
			self.__highlighter.deleteLater()
			self.__highlighter = None
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def setCompleter(self, completer):
		"""
		Sets given completer as the current completer.

		:param completer: Completer.
		:type completer: QCompleter
		:return: Method success.
		:rtype: bool
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

	def removeCompleter(self):
		"""
		Removes current completer.

		:return: Method success.
		:rtype: bool
		"""

		if self.__completer:
			LOGGER.debug("> Removing '{0}' completer.".format(self.__completer))
			# Signals / Slots.
			self.__completer.activated.disconnect(self.__insertCompletion)

			self.__completer.deleteLater()
			self.__completer = None
		return True

	def getMatchingSymbolsPairs(self, cursor, openingSymbol, closingSymbol, backward=False):
		"""
		Returns the cursor for matching given symbols pairs.

		:param cursor: Cursor to match from.
		:type cursor: QTextCursor
		:param openingSymbol: Opening symbol.
		:type openingSymbol: unicode
		:param closingSymbol: Closing symbol to match.
		:type closingSymbol: unicode
		:return: Matching cursor.
		:rtype: QTextCursor
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

	@editBlock
	def indent(self):
		"""
		Indents the document text under cursor.

		:return: Method success.
		:rtype: bool
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

	@editBlock
	def unindent(self):
		"""
		Unindents the document text under cursor.

		:return: Method success.
		:rtype: bool
		"""

		cursor = self.textCursor()
		if not cursor.hasSelection():
			cursor.movePosition(QTextCursor.StartOfBlock)
			line = foundations.strings.toString(self.document().findBlockByNumber(cursor.blockNumber()).text())
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

	@editBlock
	def toggleComments(self):
		"""
		Toggles comments on the document selected lines.

		:return: Method success.
		:rtype: bool
		"""

		if not self.__commentMarker:
			return True

		cursor = self.textCursor()
		if not cursor.hasSelection():
			cursor.movePosition(QTextCursor.StartOfBlock)
			line = foundations.strings.toString(self.document().findBlockByNumber(cursor.blockNumber()).text())
			if line.startswith(self.__commentMarker):
				foundations.common.repeat(cursor.deleteChar, len(self.__commentMarker))
			else:
				cursor.insertText(self.__commentMarker)
		else:
			block = self.document().findBlock(cursor.selectionStart())
			while True:
				blockCursor = self.textCursor()
				blockCursor.setPosition(block.position())

				if foundations.strings.toString(block.text()).startswith(self.__commentMarker):
					foundations.common.repeat(blockCursor.deleteChar, len(self.__commentMarker))
				else:
					blockCursor.insertText(self.__commentMarker)

				if block.contains(cursor.selectionEnd()):
					break
				block = block.next()
		return True

	@anchorTextCursor
	@editBlock
	def removeTrailingWhiteSpaces(self):
		"""
		Removes document trailing white spaces.

		:return: Method success.
		:rtype: bool
		"""

		cursor = self.textCursor()

		block = self.document().findBlockByLineNumber(0)
		while block.isValid():
			cursor.setPosition(block.position())
			if re.search(r"\s+$", block.text()):
				cursor.movePosition(QTextCursor.EndOfBlock)
				cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
				cursor.insertText(foundations.strings.toString(block.text()).rstrip())
			block = block.next()
		cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
		if not cursor.block().text().isEmpty():
			cursor.insertText("\n")
		return True

	@anchorTextCursor
	@editBlock
	def convertIndentationToTabs(self):
		"""
		Converts document indentation to tabs.

		:return: Method success.
		:rtype: bool
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

	@anchorTextCursor
	@editBlock
	def convertIndentationToSpaces(self):
		"""
		Converts document indentation to spaces.

		:return: Method success.
		:rtype: bool
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

if __name__ == "__main__":
	import sys
	from PyQt4.QtGui import QGridLayout
	from PyQt4.QtGui import QLineEdit
	from PyQt4.QtGui import QPushButton

	from umbra.globals.constants import Constants

	application = umbra.ui.common.getApplicationInstance()

	widget = QWidget()

	gridLayout = QGridLayout()
	widget.setLayout(gridLayout)

	content = "\n".join(("import os",
			"print os.getcwd()"))
	codeEditor_QPlainTextEdit = CodeEditor_QPlainTextEdit()
	codeEditor_QPlainTextEdit.setContent(content)
	gridLayout.addWidget(codeEditor_QPlainTextEdit)

	lineEdit = QLineEdit("codeEditor_QPlainTextEdit.toggleComments()")
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
