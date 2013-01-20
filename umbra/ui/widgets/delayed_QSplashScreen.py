#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**delayed_QSplashScreen.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Delayed_QSplashScreen` class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QSplashScreen

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core
import foundations.exceptions
import foundations.verbose

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Delayed_QSplashScreen"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Delayed_QSplashScreen(QSplashScreen):
	"""
	This class is a `QSplashScreen <http://doc.qt.nokia.com/qsplashscreen.html>`_ subclass providing
	delayed messages capabilities.
	"""

	def __init__(self, pixmap, waitTime=0, textColor=Qt.black, *args, **kwargs):
		"""
		This method initializes the class.

		:param pixmap: Current pixmap path. ( String )
		:param waitTime: wait time. ( Integer )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QSplashScreen.__init__(self, pixmap, *args, **kwargs)

		self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

		# --- Setting class attributes. ---
		self.__waitTime = None
		self.waitTime = waitTime
		self.__textColor = None
		self.textColor = textColor

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def waitTime(self):
		"""
		This method is the property for **self.__waitTime** attribute.

		:return: self.__waitTime ( Integer / Float )
		"""

		return self.__waitTime

	@waitTime.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def waitTime(self, value):
		"""
		This method is the setter method for **self.__waitTime** attribute.

		:param value: Attribute value. ( Integer / Float )
		"""

		if value is not None:
			assert type(value) in (int, float), "'{0}' attribute: '{1}' type is not 'int' or 'float'!".format(
			"waitTime", value)
			assert value >= 0, "'{0}' attribute: '{1}' need to be positive!".format("waitTime", value)
		self.__waitTime = value

	@waitTime.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def waitTime(self):
		"""
		This method is the deleter method for **self.__waitTime** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "waitTime"))

	@property
	def textColor(self):
		"""
		This method is the property for **self.__textColor** attribute.

		:return: self.__textColor ( Integer / QColor )
		"""

		return self.__textColor

	@textColor.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def textColor(self, value):
		"""
		This method is the setter method for **self.__textColor** attribute.

		:param value: Attribute value. ( Integer / QColor )
		"""

		if value is not None:
			assert type(value) in (Qt.GlobalColor, QColor), \
			"'{0}' attribute: '{1}' type is not 'int' or 'QColor'!".format("textColor", value)
		self.__textColor = value

	@textColor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def textColor(self):
		"""
		This method is the deleter method for **self.__textColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "textColor"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def showMessage(self, message, textAlignement=Qt.AlignLeft, textColor=None, waitTime=None):
		"""
		This method reimplements the :meth:`QSplashScreen.showMessage` method.

		:param message: Message to display on the splashscreen. ( String )
		:param textAlignement: Text message alignment. ( Object )
		:param textColor: Text message color. ( Object )
		:param waitTime: Wait time. ( Integer )
		"""

		QSplashScreen.showMessage(self, message, textAlignement, self.__textColor if textColor is None else textColor)

		# Force QSplashscreen refresh.
		QApplication.processEvents()

		foundations.core.wait(self.__waitTime if waitTime is None else waitTime)

if __name__ == "__main__":
	from PyQt4.QtGui import QPixmap

	import umbra.ui.common
	from umbra.globals.uiConstants import UiConstants

	application = umbra.ui.common.getApplicationInstance()

	splashScreen = Delayed_QSplashScreen(QPixmap(umbra.ui.common.getResourcePath(UiConstants.splashScreenImage)))
	splashScreen.show()
	splashScreen.showMessage("This is a test message!", waitTime=1.5)
	splashScreen.showMessage("This is another test message!", waitTime=1.5)
	splashScreen.showMessage("This is a white test message!", textColor=Qt.white, waitTime=1.5)
	splashScreen.showMessage("This is a left aligned message!", textAlignement=Qt.AlignRight, waitTime=1.5)
