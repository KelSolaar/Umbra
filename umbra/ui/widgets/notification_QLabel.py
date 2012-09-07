#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**notification_QLabel.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Notification_QLabel` class.

**Others:**
	Portions of the code and logic from Prymatex:
	https://github.com/D3f0/prymatex/blob/master/prymatex/gui/widgets/overlay.py
"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
from PyQt4.QtCore import QString
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QLabel

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Notification_QLabel"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Notification_QLabel(QLabel):
	"""
	This class is a `QLabel <http://doc.qt.nokia.com/qlabel.html>`_ subclass providing
	a notification label with fading capabilities.
	"""

	# Custom signals definitions.
	notificationClicked = pyqtSignal(QString)
	"""
	This signal is emited by the :class:`Notification_QLabel` class when it receives a mouse press event. ( pyqtSignal )

	:return: Current notification text. ( QString )	
	"""

	fadedIn = pyqtSignal()
	"""
	This signal is emited by the :class:`Notification_QLabel` class when it has faded in. ( pyqtSignal )
	"""

	fadedOut = pyqtSignal()
	"""
	This signal is emited by the :class:`Notification_QLabel` class when it has faded out. ( pyqtSignal )
	"""

	@core.executionTrace
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
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		:param color: Widget text color. ( QColor )
		:param backgroundColor: Widget background color. ( QColor )
		:param borderColor: Widget border color. ( QColor )
		:param anchor: Widget anchoring area ( From 0 to 8 ). ( Integer )
		:param horizontalPadding: Left padding relative to parent Widget. ( Integer )
		:param verticalPadding: Bottom padding relative to parent Widget. ( Integer )
		:param horizontalOffset: Widget horizontal offset. ( Integer )
		:param verticalOffset: Widget vertical offset. ( Integer )
		:param fadeSpeed: Notification fading speed. ( Float )
		:param targetOpacity: Notification maximum target opacity. ( Float )
		:param duration: Notification duration in milliseconds. ( Integer )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QLabel.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__opacity = 0
		self.__style = """
						QLabel, QLabel link {{
							color: {0};
							background-color: {1};
							border: 2px solid;
							border-color: {2};
							border-radius: 4px;
							font-size: 14px;
							padding: 16px;
						}}
						"""

		self.__color = QColor(220, 220, 220)
		self.__backgroundColor = QColor(32, 32, 32)
		self.__borderColor = QColor(220, 220, 220)
		self.color = color or self.__color
		self.backgroundColor = backgroundColor or self.__backgroundColor
		self.borderColor = borderColor or self.__borderColor

		self.__anchor = None
		self.anchor = anchor or 4
		self.__horizontalPadding = None
		self.horizontalPadding = horizontalPadding or 0
		self.__verticalPadding = None
		self.verticalPadding = verticalPadding or 48
		self.__horizontalOffset = None
		self.horizontalOffset = horizontalOffset or 0
		self.__verticalOffset = None
		self.verticalOffset = verticalOffset or 0
		self.__fadeSpeed = fadeSpeed
		self.fadeSpeed = fadeSpeed or 0.15
		self.__targetOpacity = None
		self.targetOpacity = targetOpacity or 0.75
		self.__duration = None
		self.duration = duration or 2500

		self.__vector = 0

		self.__timer = QTimer(self)
		self.__timer.setInterval(25)
		self.__timer.timeout.connect(self.__setOpacity)

		#TODO: Check future Qt releases to remove this hack.
		RuntimeGlobals.layoutsManager.layoutRestored.connect(self.__raise)

		self.__setStyleSheet()

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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
		self.__setStyleSheet()

	@color.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def color(self):
		"""
		This method is the deleter method for **self.__color** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "color"))

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
		self.__setStyleSheet()

	@backgroundColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def backgroundColor(self):
		"""
		This method is the deleter method for **self.__backgroundColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "backgroundColor"))

	@property
	def borderColor(self):
		"""
		This method is the property for **self.__borderColor** attribute.

		:return: self.__borderColor. ( QColor )
		"""

		return self.__borderColor

	@borderColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def borderColor(self, value):
		"""
		This method is the setter method for **self.__borderColor** attribute.

		:param value: Attribute value. ( QColor )
		"""

		if value is not None:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("borderColor", value)
		self.__borderColor = value
		self.__setStyleSheet()

	@borderColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def borderColor(self):
		"""
		This method is the deleter method for **self.__borderColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "borderColor"))

	@property
	def anchor(self):
		"""
		This method is the property for **self.__anchor** attribute.

		:return: self.__anchor. ( Integer )
		"""

		return self.__anchor

	@anchor.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def anchor(self, value):
		"""
		This method is the setter method for **self.__anchor** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("anchor", value)
			assert value in range(0, 9), "'{0}' attribute: '{1}' need to be in '0' to '8' range!".format("anchor", value)
		self.__anchor = value

	@anchor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def anchor(self):
		"""
		This method is the deleter method for **self.__anchor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "anchor"))

	@property
	def horizontalPadding(self):
		"""
		This method is the property for **self.__horizontalPadding** attribute.

		:return: self.__horizontalPadding. ( Integer )
		"""

		return self.__horizontalPadding

	@horizontalPadding.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def horizontalPadding(self, value):
		"""
		This method is the setter method for **self.__horizontalPadding** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("horizontalPadding", value)
			assert value >= 0, "'{0}' attribute: '{1}' need to be positive!".format("horizontalPadding", value)
		self.__horizontalPadding = value

	@horizontalPadding.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def horizontalPadding(self):
		"""
		This method is the deleter method for **self.__horizontalPadding** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "horizontalPadding"))

	@property
	def verticalPadding(self):
		"""
		This method is the property for **self.__verticalPadding** attribute.

		:return: self.__verticalPadding. ( Integer )
		"""

		return self.__verticalPadding

	@verticalPadding.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def verticalPadding(self, value):
		"""
		This method is the setter method for **self.__verticalPadding** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("verticalPadding", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be positive!".format("verticalPadding", value)
		self.__verticalPadding = value

	@verticalPadding.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def verticalPadding(self):
		"""
		This method is the deleter method for **self.__verticalPadding** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "verticalPadding"))

	@property
	def horizontalOffset(self):
		"""
		This method is the property for **self.__horizontalOffset** attribute.

		:return: self.__horizontalOffset. ( Integer )
		"""

		return self.__horizontalOffset

	@horizontalOffset.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def horizontalOffset(self, value):
		"""
		This method is the setter method for **self.__horizontalOffset** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("horizontalOffset", value)
		self.__horizontalOffset = value

	@horizontalOffset.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def horizontalOffset(self):
		"""
		This method is the deleter method for **self.__horizontalOffset** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "horizontalOffset"))

	@property
	def verticalOffset(self):
		"""
		This method is the property for **self.__verticalOffset** attribute.

		:return: self.__verticalOffset. ( Integer )
		"""

		return self.__verticalOffset

	@verticalOffset.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def verticalOffset(self, value):
		"""
		This method is the setter method for **self.__verticalOffset** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("verticalOffset", value)
		self.__verticalOffset = value

	@verticalOffset.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def verticalOffset(self):
		"""
		This method is the deleter method for **self.__verticalOffset** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "verticalOffset"))

	@property
	def fadeSpeed(self):
		"""
		This method is the property for **self.__fadeSpeed** attribute.

		:return: self.__fadeSpeed. ( Float )
		"""

		return self.__fadeSpeed

	@fadeSpeed.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def fadeSpeed(self, value):
		"""
		This method is the setter method for **self.__fadeSpeed** attribute.

		:param value: Attribute value. ( Float )
		"""

		if value is not None:
			assert type(value) is float, "'{0}' attribute: '{1}' type is not 'float'!".format("fadeSpeed", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("fadeSpeed", value)
		self.__fadeSpeed = value

	@fadeSpeed.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def fadeSpeed(self):
		"""
		This method is the deleter method for **self.__fadeSpeed** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "fadeSpeed"))

	@property
	def targetOpacity(self):
		"""
		This method is the property for **self.__targetOpacity** attribute.

		:return: self.__targetOpacity. ( Float )
		"""

		return self.__targetOpacity

	@targetOpacity.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def targetOpacity(self, value):
		"""
		This method is the setter method for **self.__targetOpacity** attribute.

		:param value: Attribute value. ( Float )
		"""

		if value is not None:
			assert type(value) is float, "'{0}' attribute: '{1}' type is not 'float'!".format("targetOpacity", value)
			assert value >= 0, "'{0}' attribute: '{1}' need to be positive!".format("targetOpacity", value)
			assert value <= 1, "'{0}' attribute: '{1}' need to be less or equal than '1'!".format("targetOpacity", value)
		self.__targetOpacity = value

	@targetOpacity.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def targetOpacity(self):
		"""
		This method is the deleter method for **self.__targetOpacity** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "targetOpacity"))

	@property
	def duration(self):
		"""
		This method is the property for **self.__duration** attribute.

		:return: self.__duration. ( Integer )
		"""

		return self.__duration

	@duration.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def duration(self, value):
		"""
		This method is the setter method for **self.__duration** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("duration", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("duration", value)
		self.__duration = value

	@duration.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def duration(self):
		"""
		This method is the deleter method for **self.__duration** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "duration"))

	@property
	def opacity(self):
		"""
		This method is the property for **self.__opacity** attribute.

		:return: self.__opacity. ( Float )
		"""

		return self.__opacity

	@opacity.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def opacity(self, value):
		"""
		This method is the setter method for **self.__opacity** attribute.

		:param value: Attribute value. ( Float )
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
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def opacity(self):
		"""
		This method is the deleter method for **self.__opacity** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "opacity"))

	@property
	def style(self):
		"""
		This method is the property for **self.__style** attribute.

		:return: self.__style. ( String )
		"""

		return self.__style

	@style.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def style(self, value):
		"""
		This method is the setter method for **self.__style** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "style"))

	@style.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def style(self):
		"""
		This method is the deleter method for **self.__style** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "style"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def setParent(self, parent):
		"""
		This method reimplements the :meth:`QLabel.setParent` method.

		:param parent: Parent. ( QObject )
		"""

		QLabel.setParent(self, parent)
		self.__setPosition()

	@core.executionTrace
	def resizeEvent(self, event):
		"""
		This method reimplements the :meth:`QLabel.resizeEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		QLabel.resizeEvent(self, event)
		self.__setPosition()

	@core.executionTrace
	def mousePressEvent(self, event):
		"""
		This method reimplements the :meth:`QLabel.mousePressEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		self.notificationClicked.emit(self.text())

	@core.executionTrace
	def showEvent(self, event):
		"""
		This method reimplements the :meth:`QLabel.showEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		QLabel.showEvent(self, event)
		self.__setPosition()

	@core.executionTrace
	def __raise(self, *args):
		"""
		This method ensures that the Widget stays on top of the parent stack forcing the redraw.

		:param \*args: Arguments. ( \* )
		"""

		children = self.parent().children().remove(self)
		if children:
			self.stackUnder(children[-1])
		else:
			self.lower()
		self.raise_()

	@core.executionTrace
	def __setPosition(self):
		"""
		This method sets the Widget position relatively to its parent.
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

	@core.executionTrace
	def __fadeIn(self):
		"""
		This method starts the Widget fade in.
		"""

		self.__timer.stop()
		self.__vector = self.__fadeSpeed
		self.__timer.start()

	@core.executionTrace
	def __fadeOut(self):
		"""
		This method starts the Widget fade out.
		"""

		self.__timer.stop()
		self.__vector = -self.__fadeSpeed
		self.__timer.start()

	@core.executionTrace
	def __setOpacity(self):
		"""
		This method sets the Widget opacity.
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

	@core.executionTrace
	def __setStyleSheet(self):
		"""
		This method sets the Widget stylesheet.
		"""

		colors = map(lambda x:"rgb({0}, {1}, {2}, {3})".format(x.red(), x.green(), x.blue(), int(self.__opacity * 255)),
														(self.__color, self.__backgroundColor, self.__borderColor))
		self.setStyleSheet(self.__style.format(*colors))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def showMessage(self, message, duration=2500):
		"""
		This method shows given message.
		
		:param message: Message. ( String )
		:param duration: Notification duration in milliseconds. ( Integer )
		:return: Method success. ( Boolean )
		"""

		self.setText(message)
		self.__duration = duration

		self.__setPosition()

		if message:
			self.__fadeIn()
		else:
			self.__fadeOut()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def hideMessage(self):
		"""
		This method hides the current message.

		:return: Method success. ( Boolean )
		"""

		self.__fadeOut()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def refreshPosition(self):
		"""
		This method refreshes the Widget position.

		:return: Method success. ( Boolean )
		"""

		self.__setPosition()
		return True
