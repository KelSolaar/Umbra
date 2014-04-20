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
import foundations.data_structures
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

__all__ = ["LOGGER", "edit_block", "anchor_text_cursor", "center_text_cursor", "Basic_QPlainTextEdit"]

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def edit_block(object):
	"""
	Handles edit blocks undo states.

	:param object: Object to decorate.
	:type object: object
	:return: Object.
	:rtype: object
	"""

	@functools.wraps(object)
	def edit_block_wrapper(*args, **kwargs):
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
			cursor = foundations.common.get_first_item(args).textCursor()
			cursor.beginEditBlock()
		value = None
		try:
			value = object(*args, **kwargs)
		finally:
			if args:
				cursor.endEditBlock()
			return value

	return edit_block_wrapper

def anchor_text_cursor(object):
	"""
	Anchors the text cursor position.

	:param object: Object to decorate.
	:type object: object
	:return: Object.
	:rtype: object
	"""

	@functools.wraps(object)
	def anchor_text_cursorWrapper(*args, **kwargs):
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
			if hasattr(foundations.common.get_first_item(args), "store_text_cursor_anchor"):
				foundations.common.get_first_item(args).store_text_cursor_anchor()

		value = object(*args, **kwargs)

		if args:
			if hasattr(foundations.common.get_first_item(args), "restore_text_cursor_anchor"):
				foundations.common.get_first_item(args).store_text_cursor_anchor()

		return value

	return anchor_text_cursorWrapper

def center_text_cursor(object):
	"""
	Centers the text cursor position.

	:param object: Object to decorate.
	:type object: object
	:return: Object.
	:rtype: object
	"""

	@functools.wraps(object)
	def center_text_cursor_wrapper(*args, **kwargs):
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
			if hasattr(foundations.common.get_first_item(args), "setCenterOnScroll"):
				foundations.common.get_first_item(args).setCenterOnScroll(True)

		value = object(*args, **kwargs)

		if args:
			if hasattr(foundations.common.get_first_item(args), "setCenterOnScroll"):
				foundations.common.get_first_item(args).setCenterOnScroll(False)

		return value

	return center_text_cursor_wrapper

class Basic_QPlainTextEdit(QPlainTextEdit):
	"""
	Defines a `QPlainTextEdit <http://doc.qt.nokia.com/qplaintextedit.html>`_ subclass providing
	a basic editor base class.
	"""

	# Custom signals definitions.
	patterns_replaced = pyqtSignal(list)
	"""
	This signal is emited by the :class:`Basic_QPlainTextEdit` class
	when patterns have been replaced.

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
		self.__search_pattern = None
		self.__minimum_font_point_size = 6
		self.__maximum_font_point_size = 24

		self.__text_cursor_anchor = None

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def search_pattern(self):
		"""
		Property for **self.__search_pattern** attribute.

		:return: self.__search_pattern.
		:rtype: unicode
		"""

		return self.__search_pattern

	@search_pattern.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def search_pattern(self, value):
		"""
		Setter for **self.__search_pattern** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) in (unicode, QString), \
			"'{0}' attribute: '{1}' type is not 'unicode' or 'QString'!".format("search_pattern", value)
		self.__search_pattern = value

	@search_pattern.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def search_pattern(self):
		"""
		Deleter for **self.__search_pattern** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "search_pattern"))

	@property
	def minimum_font_point_size(self):
		"""
		Property for **self.__minimum_font_point_size** attribute.

		:return: self.__minimum_font_point_size.
		:rtype: int
		"""

		return self.__minimum_font_point_size

	@minimum_font_point_size.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def minimum_font_point_size(self, value):
		"""
		Setter for **self.__minimum_font_point_size** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) in (int, float), "'{0}' attribute: '{1}' type is not 'int' or 'float'!".format(
			"minimum_font_point_size", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("minimum_font_point_size", value)
		self.__minimum_font_point_size = value

	@minimum_font_point_size.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def minimum_font_point_size(self):
		"""
		Deleter for **self.__minimum_font_point_size** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "minimum_font_point_size"))

	@property
	def maximum_font_point_size(self):
		"""
		Property for **self.__maximum_font_point_size** attribute.

		:return: self.__maximum_font_point_size.
		:rtype: int
		"""

		return self.__maximum_font_point_size

	@maximum_font_point_size.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def maximum_font_point_size(self, value):
		"""
		Setter for **self.__maximum_font_point_size** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) in (int, float), "'{0}' attribute: '{1}' type is not 'int' or 'float'!".format(
			"maximum_font_point_size", value)
			assert value > self.__minimum_font_point_size, \
			"'{0}' attribute: '{1}' need to be exactly superior to '{2}'!".format(
			"maximum_font_point_size", value, self.__minimum_font_point_size)
		self.__maximum_font_point_size = value

	@maximum_font_point_size.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def maximum_font_point_size(self):
		"""
		Deleter for **self.__maximum_font_point_size** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "maximum_font_point_size"))

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
				self.zoom_in()
			elif event.delta() == -120:
				self.zoom_out()
			event.ignore()
		else:
			QPlainTextEdit.wheelEvent(self, event)

	def __select_text_under_cursor_blocks(self, cursor):
		"""
		Selects the document text under cursor blocks.

		:param cursor: Cursor.
		:type cursor: QTextCursor
		"""

		start_block = self.document().findBlock(cursor.selectionStart()).firstLineNumber()
		end_block = self.document().findBlock(cursor.selectionEnd()).firstLineNumber()
		cursor.setPosition(self.document().findBlockByLineNumber(start_block).position())
		cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
		cursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor, end_block - start_block)
		cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)

	def get_selected_text_metrics(self):
		"""
		Returns current document selected text metrics.

		:return: Selected text metrics.
		:rtype: tuple
		"""

		selected_text = self.get_selected_text()
		if not selected_text:
			return tuple()

		return (selected_text, self.get_cursor_line(), self.get_cursor_column() - len(selected_text))

	def get_default_text_option(self):
		"""
		Returns default text option.

		:return: Default text options.
		:rtype: QTextOption
		"""

		return self.document().defaultTextOption()

	def set_default_text_option(self, text_option):
		"""
		Sets default text option using given flag.

		:param text_option: Text option.
		:type text_option: QTextOption
		:return: Method success.
		:rtype: bool
		"""

		self.document().set_default_text_option(text_option)
		return True

	def store_text_cursor_anchor(self):
		"""
		Stores the document cursor anchor.

		:return: Method success.
		:rtype: bool
		"""

		self.__text_cursor_anchor = (self.textCursor(),
								self.horizontalScrollBar().sliderPosition(),
								self.verticalScrollBar().sliderPosition())
		return True

	def restore_text_cursor_anchor(self):
		"""
		Restores the document cursor anchor.

		:return: Method success.
		:rtype: bool
		"""

		if not self.__text_cursor_anchor:
			return False

		text_cursor, horizontal_scroll_bar_slider_position, vertical_scroll_bar_slider_position = self.__text_cursor_anchor
		self.setTextCursor(text_cursor)
		self.horizontalScrollBar().setSliderPosition(horizontal_scroll_bar_slider_position)
		self.verticalScrollBar().setSliderPosition(vertical_scroll_bar_slider_position)
		return True

	def get_cursor_line(self):
		"""
		Returns the document cursor line.

		:return: Cursor line.
		:rtype: int
		"""

		return self.textCursor().blockNumber()

	def get_cursor_column(self):
		"""
		Returns the document cursor column.

		:return: Cursor column.
		:rtype: int
		"""

		return self.textCursor().columnNumber()

	def get_previous_character(self):
		"""
		Returns the character before the cursor.

		:return: Previous cursor character.
		:rtype: QString
		"""

		cursor = self.textCursor()
		cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
		return cursor.selectedText()

	def get_next_character(self):
		"""
		Returns the character after the cursor.

		:return: Next cursor character.
		:rtype: QString
		"""

		cursor = self.textCursor()
		cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
		return cursor.selectedText()

	def get_words(self):
		"""
		Returns the document words.

		:return: Document words.
		:rtype: list
		"""

		words = []
		block = self.document().findBlockByLineNumber(0)
		while block.isValid():
			blockWords = foundations.strings.get_words(foundations.strings.to_string(block.text()))
			if blockWords:
				words.extend(blockWords)
			block = block.next()
		return words

	def get_selected_text(self):
		"""
		Returns the document text under cursor.

		:return: Text under cursor.
		:rtype: QString
		"""

		return self.textCursor().selectedText()

	def get_word_under_cursor_legacy(self):
		"""
		Returns the document word under cursor ( Using Qt legacy "QTextCursor.WordUnderCursor" ).

		:return: Word under cursor.
		:rtype: QString
		"""

		cursor = self.textCursor()
		cursor.select(QTextCursor.WordUnderCursor)
		return cursor.selectedText()

	def get_word_under_cursor(self):
		"""
		Returns the document word under cursor.

		:return: Word under cursor.
		:rtype: QString
		"""

		if not re.match(r"^\w+$", foundations.strings.to_string(self.get_previous_character())):
			return QString()

		cursor = self.textCursor()
		cursor.movePosition(QTextCursor.PreviousWord, QTextCursor.MoveAnchor)
		cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
		return cursor.selectedText()

	def get_partial_word_under_cursor(self):
		"""
		Returns the document partial word under cursor ( From word start to cursor position ).

		:return: Partial word under cursor.
		:rtype: QString
		"""

		if not re.match(r"^\w+$", foundations.strings.to_string(self.get_previous_character())):
			return QString()

		cursor = self.textCursor()
		position = cursor.position()
		cursor.movePosition(QTextCursor.PreviousWord, QTextCursor.KeepAnchor)
		return cursor.selectedText()

	def is_modified(self):
		"""
		Returns if the document is modified.

		:return: Document modified state.
		:rtype: bool
		"""

		return self.document().isModified()

	def set_modified(self, state):
		"""
		Sets the document modified state.

		:param state: Modified state.
		:type state: bool
		:return: Method success.
		:rtype: bool
		"""

		self.document().setModified(state)
		return True

	def is_empty(self):
		"""
		Returns if the document is empty.

		:return: Document empty state.
		:rtype: bool
		"""

		return self.document().isEmpty()

	@edit_block
	def set_content(self, content):
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

	@edit_block
	def delete_lines(self):
		"""
		Deletes the document lines under cursor.

		:return: Method success.
		:rtype: bool
		"""

		cursor = self.textCursor()
		self.__select_text_under_cursor_blocks(cursor)
		cursor.removeSelectedText()
		cursor.deleteChar()
		return True

	@edit_block
	def duplicate_lines(self):
		"""
		Duplicates the document lines under cursor.

		:return: Method success.
		:rtype: bool
		"""

		cursor = self.textCursor()
		self.__select_text_under_cursor_blocks(cursor)
		text = cursor.selectedText()

		cursor.setPosition(cursor.block().next().position())
		cursor.position() == cursor.document().firstBlock().position() and cursor.setPosition(
		cursor.document().lastBlock().position())

		start_position = cursor.position()
		cursor.insertText(text)
		end_position = cursor.position()
		cursor.insertText(QChar(QChar.ParagraphSeparator))

		cursor.setPosition(start_position, QTextCursor.MoveAnchor)
		cursor.setPosition(end_position, QTextCursor.KeepAnchor)
		self.setTextCursor(cursor)

		return True

	@edit_block
	def move_lines(self, direction=QTextCursor.Up):
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

		self.__select_text_under_cursor_blocks(cursor)
		text = cursor.selectedText()
		cursor.removeSelectedText()
		cursor.deleteChar()

		cursor.setPosition(cursor.block().next().position() if direction == QTextCursor.Down else \
						cursor.block().previous().position())
		if cursor.position() == cursor.document().firstBlock().position() and direction == QTextCursor.Down:
			cursor.movePosition(QTextCursor.End)
			cursor.insertText(QChar(QChar.ParagraphSeparator))

		start_position = cursor.position()
		cursor.insertText(text)
		end_position = cursor.position()
		not cursor.atEnd() and cursor.insertText(QChar(QChar.ParagraphSeparator))

		cursor.setPosition(start_position, QTextCursor.MoveAnchor)
		cursor.setPosition(end_position, QTextCursor.KeepAnchor)
		self.setTextCursor(cursor)

		return True

	def move_lines_up(self):
		"""
		Moves up the document lines under cursor.

		:return: Method success.
		:rtype: bool
		"""

		return self.move_lines(QTextCursor.Up)

	def move_lines_down(self):
		"""
		Moves down the document lines under cursor.

		:return: Method success.
		:rtype: bool
		"""

		return self.move_lines(QTextCursor.Down)

	@center_text_cursor
	def search(self, pattern, **kwargs):
		"""
		Searchs given pattern text in the document.

		Usage::

			>>> script_editor = Umbra.components_manager.get_interface("factory.script_editor")
			True
			>>> codeEditor = script_editor.get_current_editor()
			True
			>>> codeEditor.search(search_pattern, case_sensitive=True, whole_word=True, regular_expressions=True, \
backward_search=True, wrap_around=True)
			True

		:param pattern: Pattern to search for.
		:type pattern: unicode
		:param \*\*kwargs: Search settings.
		:type \*\*kwargs: dict
		:return: Method success.
		:rtype: bool
		"""

		settings = foundations.data_structures.Structure(**{"case_sensitive" : False,
								"whole_word" : False,
								"regular_expressions" : False,
								"backward_search" : False,
								"wrap_around" : True})
		settings.update(kwargs)

		self.__search_pattern = pattern

		if settings.regular_expressions:
			pattern = QRegExp(pattern)
			pattern.setCaseSensitivity(Qt.CaseSensitive if settings.case_sensitive else Qt.CaseInsensitive)

		flags = QTextDocument.FindFlags()
		if settings.case_sensitive:
			flags = flags | QTextDocument.FindCaseSensitively
		if settings.whole_word:
			flags = flags | QTextDocument.FindWholeWords
		if settings.backward_search:
			flags = flags | QTextDocument.FindBackward

		cursor = self.document().find(pattern, self.textCursor(), flags)
		if not cursor.isNull():
			self.setTextCursor(cursor)
			return True
		else:
			if settings.wrap_around:
				self.store_text_cursor_anchor()
				cursor = self.textCursor()
				if settings.backward_search:
					cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
				else:
					cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
				self.setTextCursor(cursor)
				settings.wrap_around = False
				if self.search(pattern, **settings):
					return True
				else:
					self.restore_text_cursor_anchor()

	@center_text_cursor
	def search_next(self):
		"""
		Searchs the next search pattern in the document.

		:return: Method success.
		:rtype: bool
		"""

		pattern = self.get_selected_text() or self.__search_pattern
		if not pattern:
			return False

		return self.search(pattern, **{"case_sensitive" : True,
										"whole_word" : False,
										"regular_expressions" : False,
										"backward_search" : False,
										"wrap_around" : True})

	@center_text_cursor
	def search_previous(self):
		"""
		Searchs the previous search pattern in the document.

		:return: Method success.
		:rtype: bool
		"""

		pattern = self.get_selected_text() or self.__search_pattern
		if not pattern:
			return False

		return self.search(pattern, **{"case_sensitive" : True,
										"whole_word" : False,
										"regular_expressions" : False,
										"backward_search" : True,
										"wrap_around" : True})

	@center_text_cursor
	@edit_block
	def replace(self, pattern, replacement_pattern, **kwargs):
		"""
		Replaces current given pattern occurence in the document with the replacement pattern.

		Usage::

			>>> script_editor = Umbra.components_manager.get_interface("factory.script_editor")
			True
			>>> codeEditor = script_editor.get_current_editor()
			True
			>>> codeEditor.replace(search_pattern, replacement_pattern, case_sensitive=True, whole_word=True, \
regular_expressions=True, backward_search=True, wrap_around=True)
			True

		:param pattern: Pattern to replace.
		:type pattern: unicode
		:param replacement_pattern: Replacement pattern.
		:type replacement_pattern: unicode
		:param \*\*kwargs: Format settings.
		:type \*\*kwargs: dict
		:return: Method success.
		:rtype: bool
		"""

		settings = foundations.data_structures.Structure(**{"case_sensitive" : False,
														"regular_expressions" : False})
		settings.update(kwargs)


		selected_text = self.get_selected_text()
		regex = "^{0}$".format(pattern if settings.regular_expressions else re.escape(foundations.strings.to_string(pattern)))
		flags = int() if settings.case_sensitive else re.IGNORECASE
		if not selected_text or not re.search(regex, selected_text, flags=flags):
			self.search(pattern, **kwargs)
			return False

		cursor = self.textCursor()
		metrics = self.get_selected_text_metrics()
		if cursor.isNull():
			return False

		if not cursor.hasSelection():
			return False

		cursor.insertText(replacement_pattern)

		self.patterns_replaced.emit([metrics])

		self.search(pattern, **kwargs)

		return True

	@center_text_cursor
	@anchor_text_cursor
	@edit_block
	def replace_all(self, pattern, replacement_pattern, **kwargs):
		"""
		| Replaces every given pattern occurrences in the document with the replacement pattern.

		.. warning::

			Initializing **wrap_around** keyword to **True** leads to infinite recursion loop
			if the search pattern and the replacement_pattern are the same.

		:param pattern: Pattern to replace.
		:type pattern: unicode
		:param replacement_pattern: Replacement pattern.
		:type replacement_pattern: unicode
		:param \*\*kwargs: Format settings.
		:type \*\*kwargs: dict
		:return: Method success.
		:rtype: bool
		"""

		edit_cursor = self.textCursor()

		edit_cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor)
		self.setTextCursor(edit_cursor)

		patterns_replaced = []
		while True:
			if not self.search(pattern, **kwargs):
				break

			cursor = self.textCursor()
			metrics = self.get_selected_text_metrics()
			if cursor.isNull():
				break

			if not cursor.hasSelection():
				break
			cursor.insertText(replacement_pattern)
			patterns_replaced.append(metrics)

		self.patterns_replaced.emit(patterns_replaced)

		return True

	@center_text_cursor
	def go_to_line(self, line):
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

	def go_to_column(self, column):
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

	def go_to_position(self, position):
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

	def toggle_word_wrap(self):
		"""
		Toggles document word wrap.

		:return: Method success.
		:rtype: bool
		"""

		self.setWordWrapMode(not self.wordWrapMode() and QTextOption.WordWrap or QTextOption.NoWrap)
		return True

	def toggle_white_spaces(self):
		"""
		Toggles document white spaces display.

		:return: Method success.
		:rtype: bool
		"""

		text_option = self.get_default_text_option()
		if text_option.flags().__int__():
			text_option = QTextOption()
			text_option.setTabStop(self.tabStopWidth())
		else:
			text_option.setFlags(
			text_option.flags() | QTextOption.ShowTabsAndSpaces | QTextOption.ShowLineAndParagraphSeparators)
		self.set_default_text_option(text_option)
		return True

	def set_font_increment(self, value):
		"""
		Increments the document font size.

		:param value: Font size increment.
		:type value: int
		:return: Method success.
		:rtype: bool
		"""

		font = self.font()
		point_size = font.pointSize() + value
		if point_size < self.__minimum_font_point_size or point_size > self.__maximum_font_point_size:
			return False

		font.setPointSize(point_size)
		self.setFont(font)
		return True

	def zoom_in(self):
		"""
		Increases the document font size.

		:return: Method success.
		:rtype: bool
		"""

		return self.set_font_increment(1)

	def zoom_out(self):
		"""
		Increases the document font size.

		:return: Method success.
		:rtype: bool
		"""

		return self.set_font_increment(-1)

if __name__ == "__main__":
	import sys
	from PyQt4.QtGui import QGridLayout
	from PyQt4.QtGui import QLineEdit
	from PyQt4.QtGui import QPushButton
	from PyQt4.QtGui import QWidget

	import umbra.ui.common
	from umbra.globals.constants import Constants

	application = umbra.ui.common.get_application_instance()

	widget = QWidget()

	grid_layout = QGridLayout()
	widget.setLayout(grid_layout)

	content = "\n".join(("Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
			"Phasellus tincidunt tempus volutpat.",
			"Cras malesuada nunc id neque fermentum accumsan.",
			"Aenean mauris lorem, faucibus et viverra iaculis, vulputate ac augue.",
			"Mauris consequat urna enim."))

	basic_QPlainTextEdit = Basic_QPlainTextEdit()
	basic_QPlainTextEdit.set_content(content)
	grid_layout.addWidget(basic_QPlainTextEdit)

	line_edit = QLineEdit("basic_QPlainTextEdit.replace(\"Lorem\", \"Nemo\")")
	grid_layout.addWidget(line_edit)

	def _pushButton__clicked(*args):
		statement = unicode(line_edit.text(), Constants.default_codec, Constants.codec_error)
		exec(statement)

	push_button = QPushButton("Execute Statement")
	push_button.clicked.connect(_pushButton__clicked)
	grid_layout.addWidget(push_button)

	widget.show()
	widget.raise_()

	sys.exit(application.exec_())
