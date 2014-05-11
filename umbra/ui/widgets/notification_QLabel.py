#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**notification_QLabel.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`Notification_QLabel` class.

**Others:**
	Portions of the code and logic from Prymatex:
	https://github.com/D3f0/prymatex/blob/master/prymatex/gui/widgets/overlay.py
"""

from __future__ import unicode_literals

from PyQt4.QtCore import QString
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QLabel

import foundations.exceptions
import foundations.verbose
from umbra.globals.runtime_globals import RuntimeGlobals

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Notification_QLabel"]

LOGGER = foundations.verbose.install_logger()

class Notification_QLabel(QLabel):
	"""
	Defines a `QLabel <http://doc.qt.nokia.com/qlabel.html>`_ subclass providing
	a notification label with fading capabilities.
	"""

	# Custom signals definitions.
	notification_clicked = pyqtSignal(QString)
	"""
	This signal is emited by the :class:`Notification_QLabel` class when it receives a mouse press event.

	:return: Current notification text.
	:rtype: QString
	"""

	faded_in = pyqtSignal()
	"""
	This signal is emited by the :class:`Notification_QLabel` class when it has faded in.
	"""

	faded_out = pyqtSignal()
	"""
	This signal is emited by the :class:`Notification_QLabel` class when it has faded out.
	"""

	def __init__(self,
				parent=None,
				color=None,
				background_color=None,
				border_color=None,
				anchor=None,
				horizontal_padding=None,
				vertical_padding=None,
				horizontal_offset=None,
				vertical_offset=None,
				fade_speed=None,
				target_opacity=None,
				duration=None):
		"""
		Initializes the class.

		:param parent: Widget parent.
		:type parent: QObject
		:param color: Widget text color.
		:type color: QColor
		:param background_color: Widget background color.
		:type background_color: QColor
		:param border_color: Widget border color.
		:type border_color: QColor
		:param anchor: Widget anchoring area ( From 0 to 8 ).
		:type anchor: int
		:param horizontal_padding: Left padding relative to parent Widget.
		:type horizontal_padding: int
		:param vertical_padding: Bottom padding relative to parent Widget.
		:type vertical_padding: int
		:param horizontal_offset: Widget horizontal offset.
		:type horizontal_offset: int
		:param vertical_offset: Widget vertical offset.
		:type vertical_offset: int
		:param fade_speed: Notification fading speed.
		:type fade_speed: float
		:param target_opacity: Notification maximum target opacity.
		:type target_opacity: float
		:param duration: Notification duration in milliseconds.
		:type duration: int
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QLabel.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__opacity = 0
		self.__style = """
						QLabel, QLabel link {{
							color: {0};
							background-color: {1};
							border: 4px solid;
							border-color: {2};
							font-size: 14px;
							padding: 16px;
						}}
						"""

		self.__color = QColor(220, 220, 220)
		self.__background_color = QColor(32, 32, 32)
		self.__border_color = QColor(220, 220, 220)
		self.color = color if color is not None else self.__color
		self.background_color = background_color if background_color is not None else self.__background_color
		self.border_color = border_color if border_color is not None else self.__border_color

		self.__anchor = None
		self.anchor = anchor if anchor is not None else 4
		self.__horizontal_padding = None
		self.horizontal_padding = horizontal_padding if horizontal_padding is not None else 0
		self.__vertical_padding = None
		self.vertical_padding = vertical_padding if vertical_padding is not None else 48
		self.__horizontal_offset = None
		self.horizontal_offset = horizontal_offset if horizontal_offset is not None else 0
		self.__vertical_offset = None
		self.vertical_offset = vertical_offset if vertical_offset is not None else 0
		self.__fade_speed = fade_speed
		self.fade_speed = fade_speed if fade_speed is not None else 0.15
		self.__target_opacity = None
		self.target_opacity = target_opacity if target_opacity is not None else 0.75
		self.__duration = None
		self.duration = duration if duration is not None else 2500

		self.__vector = 0

		self.__timer = QTimer(self)
		self.__timer.setInterval(25)
		self.__timer.timeout.connect(self.__set_opacity)

		# TODO: Check future Qt releases to remove this hack.
		RuntimeGlobals.layouts_manager and RuntimeGlobals.layouts_manager.layout_restored.connect(self.__raise)

		self.__set_style_sheet()

	@property
	def color(self):
		"""
		Property for **self.__color** attribute.

		:return: self.__color.
		:rtype: QColor
		"""

		return self.__color

	@color.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def color(self, value):
		"""
		Setter for **self.__color** attribute.

		:param value: Attribute value.
		:type value: QColor
		"""

		if value is not None:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("color", value)
		self.__color = value
		self.__set_style_sheet()

	@color.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def color(self):
		"""
		Deleter for **self.__color** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "color"))

	@property
	def background_color(self):
		"""
		Property for **self.__background_color** attribute.

		:return: self.__background_color.
		:rtype: QColor
		"""

		return self.__background_color

	@background_color.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def background_color(self, value):
		"""
		Setter for **self.__background_color** attribute.

		:param value: Attribute value.
		:type value: QColor
		"""

		if value is not None:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("background_color", value)
		self.__background_color = value
		self.__set_style_sheet()

	@background_color.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def background_color(self):
		"""
		Deleter for **self.__background_color** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "background_color"))

	@property
	def border_color(self):
		"""
		Property for **self.__border_color** attribute.

		:return: self.__border_color.
		:rtype: QColor
		"""

		return self.__border_color

	@border_color.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def border_color(self, value):
		"""
		Setter for **self.__border_color** attribute.

		:param value: Attribute value.
		:type value: QColor
		"""

		if value is not None:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("border_color", value)
		self.__border_color = value
		self.__set_style_sheet()

	@border_color.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def border_color(self):
		"""
		Deleter for **self.__border_color** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "border_color"))

	@property
	def anchor(self):
		"""
		Property for **self.__anchor** attribute.

		:return: self.__anchor.
		:rtype: int
		"""

		return self.__anchor

	@anchor.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def anchor(self, value):
		"""
		Setter for **self.__anchor** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("anchor", value)
			assert value in range(0, 9), "'{0}' attribute: '{1}' need to be in '0' to '8' range!".format("anchor", value)
		self.__anchor = value

	@anchor.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def anchor(self):
		"""
		Deleter for **self.__anchor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "anchor"))

	@property
	def horizontal_padding(self):
		"""
		Property for **self.__horizontal_padding** attribute.

		:return: self.__horizontal_padding.
		:rtype: int
		"""

		return self.__horizontal_padding

	@horizontal_padding.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def horizontal_padding(self, value):
		"""
		Setter for **self.__horizontal_padding** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("horizontal_padding", value)
			assert value >= 0, "'{0}' attribute: '{1}' need to be positive!".format("horizontal_padding", value)
		self.__horizontal_padding = value

	@horizontal_padding.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def horizontal_padding(self):
		"""
		Deleter for **self.__horizontal_padding** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "horizontal_padding"))

	@property
	def vertical_padding(self):
		"""
		Property for **self.__vertical_padding** attribute.

		:return: self.__vertical_padding.
		:rtype: int
		"""

		return self.__vertical_padding

	@vertical_padding.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def vertical_padding(self, value):
		"""
		Setter for **self.__vertical_padding** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("vertical_padding", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be positive!".format("vertical_padding", value)
		self.__vertical_padding = value

	@vertical_padding.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def vertical_padding(self):
		"""
		Deleter for **self.__vertical_padding** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "vertical_padding"))

	@property
	def horizontal_offset(self):
		"""
		Property for **self.__horizontal_offset** attribute.

		:return: self.__horizontal_offset.
		:rtype: int
		"""

		return self.__horizontal_offset

	@horizontal_offset.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def horizontal_offset(self, value):
		"""
		Setter for **self.__horizontal_offset** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("horizontal_offset", value)
		self.__horizontal_offset = value

	@horizontal_offset.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def horizontal_offset(self):
		"""
		Deleter for **self.__horizontal_offset** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "horizontal_offset"))

	@property
	def vertical_offset(self):
		"""
		Property for **self.__vertical_offset** attribute.

		:return: self.__vertical_offset.
		:rtype: int
		"""

		return self.__vertical_offset

	@vertical_offset.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def vertical_offset(self, value):
		"""
		Setter for **self.__vertical_offset** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("vertical_offset", value)
		self.__vertical_offset = value

	@vertical_offset.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def vertical_offset(self):
		"""
		Deleter for **self.__vertical_offset** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "vertical_offset"))

	@property
	def fade_speed(self):
		"""
		Property for **self.__fade_speed** attribute.

		:return: self.__fade_speed.
		:rtype: float
		"""

		return self.__fade_speed

	@fade_speed.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def fade_speed(self, value):
		"""
		Setter for **self.__fade_speed** attribute.

		:param value: Attribute value.
		:type value: float
		"""

		if value is not None:
			assert type(value) is float, "'{0}' attribute: '{1}' type is not 'float'!".format("fade_speed", value)
			assert value >= 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("fade_speed", value)
		self.__fade_speed = value

	@fade_speed.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def fade_speed(self):
		"""
		Deleter for **self.__fade_speed** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "fade_speed"))

	@property
	def target_opacity(self):
		"""
		Property for **self.__target_opacity** attribute.

		:return: self.__target_opacity.
		:rtype: float
		"""

		return self.__target_opacity

	@target_opacity.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def target_opacity(self, value):
		"""
		Setter for **self.__target_opacity** attribute.

		:param value: Attribute value.
		:type value: float
		"""

		if value is not None:
			assert type(value) is float, "'{0}' attribute: '{1}' type is not 'float'!".format("target_opacity", value)
			assert value >= 0, "'{0}' attribute: '{1}' need to be positive!".format("target_opacity", value)
			assert value <= 1, "'{0}' attribute: '{1}' need to be less or equal than '1'!".format("target_opacity", value)
		self.__target_opacity = value

	@target_opacity.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def target_opacity(self):
		"""
		Deleter for **self.__target_opacity** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "target_opacity"))

	@property
	def duration(self):
		"""
		Property for **self.__duration** attribute.

		:return: self.__duration.
		:rtype: int
		"""

		return self.__duration

	@duration.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def duration(self, value):
		"""
		Setter for **self.__duration** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("duration", value)
			assert value >= 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("duration", value)
		self.__duration = value

	@duration.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def duration(self):
		"""
		Deleter for **self.__duration** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "duration"))

	@property
	def opacity(self):
		"""
		Property for **self.__opacity** attribute.

		:return: self.__opacity.
		:rtype: float
		"""

		return self.__opacity

	@opacity.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def opacity(self, value):
		"""
		Setter for **self.__opacity** attribute.

		:param value: Attribute value.
		:type value: float
		"""

		if value is not None:
			assert type(value) in (int, float), "'{0}' attribute: '{1}' type is not 'int' or 'float'!".format("opacity",
																											value)
		if value > 1:
			value = 1
		elif value < 0:
			value = 0

		self.__opacity = float(value)
		self.__set_style_sheet()

	@opacity.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def opacity(self):
		"""
		Deleter for **self.__opacity** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "opacity"))

	@property
	def style(self):
		"""
		Property for **self.__style** attribute.

		:return: self.__style.
		:rtype: unicode
		"""

		return self.__style

	@style.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def style(self, value):
		"""
		Setter for **self.__style** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "style"))

	@style.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def style(self):
		"""
		Deleter for **self.__style** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "style"))

	def setParent(self, parent):
		"""
		Reimplements the :meth:`QLabel.setParent` method.

		:param parent: Parent.
		:type parent: QObject
		"""

		QLabel.setParent(self, parent)
		self.__set_position()

	def resizeEvent(self, event):
		"""
		Reimplements the :meth:`QLabel.resizeEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		QLabel.resizeEvent(self, event)
		self.__set_position()

	def mousePressEvent(self, event):
		"""
		Reimplements the :meth:`QLabel.mousePressEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		self.notification_clicked.emit(self.text())

	def showEvent(self, event):
		"""
		Reimplements the :meth:`QLabel.showEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		QLabel.showEvent(self, event)
		self.__set_position()

	def __raise(self, *args):
		"""
		Ensures that the Widget stays on top of the parent stack forcing the redraw.

		:param \*args: Arguments.
		:type \*args: \*
		"""

		children = self.parent().children().remove(self)
		if children:
			self.stackUnder(children[-1])
		else:
			self.lower()
		self.raise_()

	def __set_position(self):
		"""
		Sets the Widget position relatively to its parent.
		"""

		rectangle = hasattr(self.parent(), "viewport") and self.parent().viewport().rect() or self.parent().rect()
		if not rectangle:
			return

		self.adjustSize()

		if self.__anchor == 0:
			point_x = rectangle.width() / 2 - self.width() / 2
			point_y = self.__vertical_padding
		elif self.__anchor == 1:
			point_x = rectangle.width() - self.width() - self.__horizontal_padding
			point_y = self.__vertical_padding
		elif self.__anchor == 2:
			point_x = rectangle.width() - self.width() - self.__horizontal_padding
			point_y = rectangle.height() / 2 - self.height() / 2
		elif self.__anchor == 3:
			point_x = rectangle.width() - self.width() - self.__horizontal_padding
			point_y = rectangle.height() - self.height() - self.__vertical_padding
		elif self.__anchor == 4:
			point_x = rectangle.width() / 2 - self.width() / 2
			point_y = rectangle.height() - self.height() - self.__vertical_padding
		elif self.__anchor == 5:
			point_x = self.__horizontal_padding
			point_y = rectangle.height() - self.height() - self.__vertical_padding
		elif self.__anchor == 6:
			point_x = self.__horizontal_padding
			point_y = rectangle.height() / 2 - self.height() / 2
		elif self.__anchor == 7:
			point_x = self.__horizontal_padding
			point_y = self.__vertical_padding
		elif self.__anchor == 8:
			point_x = rectangle.width() / 2 - self.width() / 2
			point_y = rectangle.height() / 2 - self.height() / 2

		self.setGeometry(point_x + self.__horizontal_offset, point_y + self.__vertical_offset, self.width(), self.height())

	def __fade_in(self):
		"""
		Starts the Widget fade in.
		"""

		self.__timer.stop()
		self.__vector = self.__fade_speed
		self.__timer.start()

	def __fade_out(self):
		"""
		Starts the Widget fade out.
		"""

		self.__timer.stop()
		self.__vector = -self.__fade_speed
		self.__timer.start()

	def __set_opacity(self):
		"""
		Sets the Widget opacity.
		"""

		if self.__vector > 0:
			if self.isHidden():
				self.show()
			if self.opacity <= self.__target_opacity:
				self.opacity += self.__vector
			else:
				self.__timer.stop()
				self.faded_in.emit()
				self.__duration and QTimer.singleShot(self.__duration, self.__fade_out)
		elif self.__vector < 0:
			if self.opacity > 0:
				self.opacity += self.__vector
			else:
				self.__timer.stop()
				self.faded_out.emit()
				self.hide()

	def __set_style_sheet(self):
		"""
		Sets the Widget stylesheet.
		"""

		colors = map(lambda x:"rgb({0}, {1}, {2}, {3})".format(x.red(), x.green(), x.blue(), int(self.__opacity * 255)),
														(self.__color, self.__background_color, self.__border_color))
		self.setStyleSheet(self.__style.format(*colors))

	def show_message(self, message, duration=2500):
		"""
		Shows given message.
		
		:param message: Message.
		:type message: unicode
		:param duration: Notification duration in milliseconds.
		:type duration: int
		:return: Method success.
		:rtype: bool
		"""

		self.setText(message)
		self.__duration = duration

		self.__set_position()

		if message:
			self.__fade_in()
		else:
			self.__fade_out()
		return True

	def hide_message(self):
		"""
		Hides the current message.

		:return: Method success.
		:rtype: bool
		"""

		self.__fade_out()
		return True

	def refresh_position(self):
		"""
		Refreshes the Widget position.

		:return: Method success.
		:rtype: bool
		"""

		self.__set_position()
		return True

if __name__ == "__main__":
	import random
	import sys
	from PyQt4.QtGui import QGridLayout
	from PyQt4.QtGui import QPlainTextEdit
	from PyQt4.QtGui import QPushButton
	from PyQt4.QtGui import QWidget

	import umbra.ui.common

	application = umbra.ui.common.get_application_instance()

	widget = QWidget()

	grid_layout = QGridLayout()
	widget.setLayout(grid_layout)

	plain_text_edit = QPlainTextEdit()
	plain_text_edit.setReadOnly(True)
	grid_layout.addWidget(plain_text_edit)
	notification_QLabel = Notification_QLabel(plain_text_edit, vertical_padding=64)

	def _pushButton__clicked(*args):
		notification_QLabel.color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		notification_QLabel.show_message("This is a notification message!", 1500)

	plain_text_edit.resizeEvent = lambda event: reduce(lambda *args: None,
	(notification_QLabel.refresh_position(), QPlainTextEdit(plain_text_edit).resizeEvent(event)))

	push_button = QPushButton("Notify!")
	push_button.clicked.connect(_pushButton__clicked)
	grid_layout.addWidget(push_button)

	widget.show()
	widget.raise_()

	sys.exit(application.exec_())

