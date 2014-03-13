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

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtCore import QString
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QLabel

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Notification_QLabel"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Notification_QLabel(QLabel):
	"""
	Defines a `QLabel <http://doc.qt.nokia.com/qlabel.html>`_ subclass providing
	a notification label with fading capabilities.
	"""

	# Custom signals definitions.
	notificationClicked = pyqtSignal(QString)
	"""
	This signal is emited by the :class:`Notification_QLabel` class when it receives a mouse press event. ( pyqtSignal )

	:return: Current notification text.
	:rtype: QString
	"""

	fadedIn = pyqtSignal()
	"""
	This signal is emited by the :class:`Notification_QLabel` class when it has faded in. ( pyqtSignal )
	"""

	fadedOut = pyqtSignal()
	"""
	This signal is emited by the :class:`Notification_QLabel` class when it has faded out. ( pyqtSignal )
	"""

	def __init__(self,
				parent=None,
				color=None,
				backgroundColor=None,
				borderColor=None,
				anchor=None,
				horizontalPadding=None,
				verticalPadding=None,
				horizontalOffset=None,
				verticalOffset=None,
				fadeSpeed=None,
				targetOpacity=None,
				duration=None):
		"""
		Initializes the class.

		:param parent: Widget parent.
		:type parent: QObject
		:param color: Widget text color.
		:type color: QColor
		:param backgroundColor: Widget background color.
		:type backgroundColor: QColor
		:param borderColor: Widget border color.
		:type borderColor: QColor
		:param anchor: Widget anchoring area ( From 0 to 8 ).
		:type anchor: int
		:param horizontalPadding: Left padding relative to parent Widget.
		:type horizontalPadding: int
		:param verticalPadding: Bottom padding relative to parent Widget.
		:type verticalPadding: int
		:param horizontalOffset: Widget horizontal offset.
		:type horizontalOffset: int
		:param verticalOffset: Widget vertical offset.
		:type verticalOffset: int
		:param fadeSpeed: Notification fading speed.
		:type fadeSpeed: float
		:param targetOpacity: Notification maximum target opacity.
		:type targetOpacity: float
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
		self.__backgroundColor = QColor(32, 32, 32)
		self.__borderColor = QColor(220, 220, 220)
		self.color = color if color is not None else self.__color
		self.backgroundColor = backgroundColor if backgroundColor is not None else self.__backgroundColor
		self.borderColor = borderColor if borderColor is not None else self.__borderColor

		self.__anchor = None
		self.anchor = anchor if anchor is not None else 4
		self.__horizontalPadding = None
		self.horizontalPadding = horizontalPadding if horizontalPadding is not None else 0
		self.__verticalPadding = None
		self.verticalPadding = verticalPadding if verticalPadding is not None else 48
		self.__horizontalOffset = None
		self.horizontalOffset = horizontalOffset if horizontalOffset is not None else 0
		self.__verticalOffset = None
		self.verticalOffset = verticalOffset if verticalOffset is not None else 0
		self.__fadeSpeed = fadeSpeed
		self.fadeSpeed = fadeSpeed if fadeSpeed is not None else 0.15
		self.__targetOpacity = None
		self.targetOpacity = targetOpacity if targetOpacity is not None else 0.75
		self.__duration = None
		self.duration = duration if duration is not None else 2500

		self.__vector = 0

		self.__timer = QTimer(self)
		self.__timer.setInterval(25)
		self.__timer.timeout.connect(self.__setOpacity)

		#TODO: Check future Qt releases to remove this hack.
		RuntimeGlobals.layoutsManager and RuntimeGlobals.layoutsManager.layoutRestored.connect(self.__raise)

		self.__setStyleSheet()

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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
		self.__setStyleSheet()

	@color.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def color(self):
		"""
		Deleter for **self.__color** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "color"))

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
		self.__setStyleSheet()

	@backgroundColor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def backgroundColor(self):
		"""
		Deleter for **self.__backgroundColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "backgroundColor"))

	@property
	def borderColor(self):
		"""
		Property for **self.__borderColor** attribute.

		:return: self.__borderColor.
		:rtype: QColor
		"""

		return self.__borderColor

	@borderColor.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def borderColor(self, value):
		"""
		Setter for **self.__borderColor** attribute.

		:param value: Attribute value.
		:type value: QColor
		"""

		if value is not None:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("borderColor", value)
		self.__borderColor = value
		self.__setStyleSheet()

	@borderColor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def borderColor(self):
		"""
		Deleter for **self.__borderColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "borderColor"))

	@property
	def anchor(self):
		"""
		Property for **self.__anchor** attribute.

		:return: self.__anchor.
		:rtype: int
		"""

		return self.__anchor

	@anchor.setter
	@foundations.exceptions.handleExceptions(AssertionError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def anchor(self):
		"""
		Deleter for **self.__anchor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "anchor"))

	@property
	def horizontalPadding(self):
		"""
		Property for **self.__horizontalPadding** attribute.

		:return: self.__horizontalPadding.
		:rtype: int
		"""

		return self.__horizontalPadding

	@horizontalPadding.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def horizontalPadding(self, value):
		"""
		Setter for **self.__horizontalPadding** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("horizontalPadding", value)
			assert value >= 0, "'{0}' attribute: '{1}' need to be positive!".format("horizontalPadding", value)
		self.__horizontalPadding = value

	@horizontalPadding.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def horizontalPadding(self):
		"""
		Deleter for **self.__horizontalPadding** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "horizontalPadding"))

	@property
	def verticalPadding(self):
		"""
		Property for **self.__verticalPadding** attribute.

		:return: self.__verticalPadding.
		:rtype: int
		"""

		return self.__verticalPadding

	@verticalPadding.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def verticalPadding(self, value):
		"""
		Setter for **self.__verticalPadding** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("verticalPadding", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be positive!".format("verticalPadding", value)
		self.__verticalPadding = value

	@verticalPadding.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def verticalPadding(self):
		"""
		Deleter for **self.__verticalPadding** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "verticalPadding"))

	@property
	def horizontalOffset(self):
		"""
		Property for **self.__horizontalOffset** attribute.

		:return: self.__horizontalOffset.
		:rtype: int
		"""

		return self.__horizontalOffset

	@horizontalOffset.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def horizontalOffset(self, value):
		"""
		Setter for **self.__horizontalOffset** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("horizontalOffset", value)
		self.__horizontalOffset = value

	@horizontalOffset.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def horizontalOffset(self):
		"""
		Deleter for **self.__horizontalOffset** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "horizontalOffset"))

	@property
	def verticalOffset(self):
		"""
		Property for **self.__verticalOffset** attribute.

		:return: self.__verticalOffset.
		:rtype: int
		"""

		return self.__verticalOffset

	@verticalOffset.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def verticalOffset(self, value):
		"""
		Setter for **self.__verticalOffset** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("verticalOffset", value)
		self.__verticalOffset = value

	@verticalOffset.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def verticalOffset(self):
		"""
		Deleter for **self.__verticalOffset** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "verticalOffset"))

	@property
	def fadeSpeed(self):
		"""
		Property for **self.__fadeSpeed** attribute.

		:return: self.__fadeSpeed.
		:rtype: float
		"""

		return self.__fadeSpeed

	@fadeSpeed.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def fadeSpeed(self, value):
		"""
		Setter for **self.__fadeSpeed** attribute.

		:param value: Attribute value.
		:type value: float
		"""

		if value is not None:
			assert type(value) is float, "'{0}' attribute: '{1}' type is not 'float'!".format("fadeSpeed", value)
			assert value >= 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("fadeSpeed", value)
		self.__fadeSpeed = value

	@fadeSpeed.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def fadeSpeed(self):
		"""
		Deleter for **self.__fadeSpeed** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "fadeSpeed"))

	@property
	def targetOpacity(self):
		"""
		Property for **self.__targetOpacity** attribute.

		:return: self.__targetOpacity.
		:rtype: float
		"""

		return self.__targetOpacity

	@targetOpacity.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def targetOpacity(self, value):
		"""
		Setter for **self.__targetOpacity** attribute.

		:param value: Attribute value.
		:type value: float
		"""

		if value is not None:
			assert type(value) is float, "'{0}' attribute: '{1}' type is not 'float'!".format("targetOpacity", value)
			assert value >= 0, "'{0}' attribute: '{1}' need to be positive!".format("targetOpacity", value)
			assert value <= 1, "'{0}' attribute: '{1}' need to be less or equal than '1'!".format("targetOpacity", value)
		self.__targetOpacity = value

	@targetOpacity.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def targetOpacity(self):
		"""
		Deleter for **self.__targetOpacity** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "targetOpacity"))

	@property
	def duration(self):
		"""
		Property for **self.__duration** attribute.

		:return: self.__duration.
		:rtype: int
		"""

		return self.__duration

	@duration.setter
	@foundations.exceptions.handleExceptions(AssertionError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(AssertionError)
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
		self.__setStyleSheet()

	@opacity.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def style(self, value):
		"""
		Setter for **self.__style** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "style"))

	@style.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def style(self):
		"""
		Deleter for **self.__style** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "style"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def setParent(self, parent):
		"""
		Reimplements the :meth:`QLabel.setParent` method.

		:param parent: Parent.
		:type parent: QObject
		"""

		QLabel.setParent(self, parent)
		self.__setPosition()

	def resizeEvent(self, event):
		"""
		Reimplements the :meth:`QLabel.resizeEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		QLabel.resizeEvent(self, event)
		self.__setPosition()

	def mousePressEvent(self, event):
		"""
		Reimplements the :meth:`QLabel.mousePressEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		self.notificationClicked.emit(self.text())

	def showEvent(self, event):
		"""
		Reimplements the :meth:`QLabel.showEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		QLabel.showEvent(self, event)
		self.__setPosition()

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

	def __setPosition(self):
		"""
		Sets the Widget position relatively to its parent.
		"""

		rectangle = hasattr(self.parent(), "viewport") and self.parent().viewport().rect() or self.parent().rect()
		if not rectangle:
			return

		self.adjustSize()

		if self.__anchor == 0:
			pointX = rectangle.width() / 2 - self.width() / 2
			pointY = self.__verticalPadding
		elif self.__anchor == 1:
			pointX = rectangle.width() - self.width() - self.__horizontalPadding
			pointY = self.__verticalPadding
		elif self.__anchor == 2:
			pointX = rectangle.width() - self.width() - self.__horizontalPadding
			pointY = rectangle.height() / 2 - self.height() / 2
		elif self.__anchor == 3:
			pointX = rectangle.width() - self.width() - self.__horizontalPadding
			pointY = rectangle.height() - self.height() - self.__verticalPadding
		elif self.__anchor == 4:
			pointX = rectangle.width() / 2 - self.width() / 2
			pointY = rectangle.height() - self.height() - self.__verticalPadding
		elif self.__anchor == 5:
			pointX = self.__horizontalPadding
			pointY = rectangle.height() - self.height() - self.__verticalPadding
		elif self.__anchor == 6:
			pointX = self.__horizontalPadding
			pointY = rectangle.height() / 2 - self.height() / 2
		elif self.__anchor == 7:
			pointX = self.__horizontalPadding
			pointY = self.__verticalPadding
		elif self.__anchor == 8:
			pointX = rectangle.width() / 2 - self.width() / 2
			pointY = rectangle.height() / 2 - self.height() / 2

		self.setGeometry(pointX + self.__horizontalOffset, pointY + self.__verticalOffset, self.width(), self.height())

	def __fadeIn(self):
		"""
		Starts the Widget fade in.
		"""

		self.__timer.stop()
		self.__vector = self.__fadeSpeed
		self.__timer.start()

	def __fadeOut(self):
		"""
		Starts the Widget fade out.
		"""

		self.__timer.stop()
		self.__vector = -self.__fadeSpeed
		self.__timer.start()

	def __setOpacity(self):
		"""
		Sets the Widget opacity.
		"""

		if self.__vector > 0:
			if self.isHidden():
				self.show()
			if self.opacity <= self.__targetOpacity:
				self.opacity += self.__vector
			else:
				self.__timer.stop()
				self.fadedIn.emit()
				self.__duration and QTimer.singleShot(self.__duration, self.__fadeOut)
		elif self.__vector < 0:
			if self.opacity > 0:
				self.opacity += self.__vector
			else:
				self.__timer.stop()
				self.fadedOut.emit()
				self.hide()

	def __setStyleSheet(self):
		"""
		Sets the Widget stylesheet.
		"""

		colors = map(lambda x:"rgb({0}, {1}, {2}, {3})".format(x.red(), x.green(), x.blue(), int(self.__opacity * 255)),
														(self.__color, self.__backgroundColor, self.__borderColor))
		self.setStyleSheet(self.__style.format(*colors))

	def showMessage(self, message, duration=2500):
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

		self.__setPosition()

		if message:
			self.__fadeIn()
		else:
			self.__fadeOut()
		return True

	def hideMessage(self):
		"""
		Hides the current message.

		:return: Method success.
		:rtype: bool
		"""

		self.__fadeOut()
		return True

	def refreshPosition(self):
		"""
		Refreshes the Widget position.

		:return: Method success.
		:rtype: bool
		"""

		self.__setPosition()
		return True

if __name__ == "__main__":
	import random
	import sys
	from PyQt4.QtGui import QGridLayout
	from PyQt4.QtGui import QPlainTextEdit
	from PyQt4.QtGui import QPushButton
	from PyQt4.QtGui import QWidget

	import umbra.ui.common

	application = umbra.ui.common.getApplicationInstance()

	widget = QWidget()

	gridLayout = QGridLayout()
	widget.setLayout(gridLayout)

	plainTextEdit = QPlainTextEdit()
	plainTextEdit.setReadOnly(True)
	gridLayout.addWidget(plainTextEdit)
	notification_QLabel = Notification_QLabel(plainTextEdit, verticalPadding=64)

	def _pushButton__clicked(*args):
		notification_QLabel.color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		notification_QLabel.showMessage("This is a notification message!", 1500)

	plainTextEdit.resizeEvent = lambda event: reduce(lambda *args: None,
	(notification_QLabel.refreshPosition(), QPlainTextEdit(plainTextEdit).resizeEvent(event)))

	pushButton = QPushButton("Notify!")
	pushButton.clicked.connect(_pushButton__clicked)
	gridLayout.addWidget(pushButton)

	widget.show()
	widget.raise_()

	sys.exit(application.exec_())

