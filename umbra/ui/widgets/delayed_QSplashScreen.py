#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**delayed_QSplashScreen.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`Delayed_QSplashScreen` class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

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
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Defines a `QSplashScreen <http://doc.qt.nokia.com/qsplashscreen.html>`_ subclass providing
	delayed messages capabilities.
	"""

	def __init__(self, pixmap, waitTime=0, textColor=Qt.black, *args, **kwargs):
		"""
		Initializes the class.

		:param pixmap: Current pixmap path.
		:type pixmap: unicode
		:param waitTime: wait time.
		:type waitTime: int
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
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
		Property for **self.__waitTime** attribute.

		:return: self.__waitTime
		:rtype: int or float
		"""

		return self.__waitTime

	@waitTime.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def waitTime(self, value):
		"""
		Setter for **self.__waitTime** attribute.

		:param value: Attribute value.
		:type value: int or float
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
		Deleter for **self.__waitTime** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "waitTime"))

	@property
	def textColor(self):
		"""
		Property for **self.__textColor** attribute.

		:return: self.__textColor
		:rtype: int or QColor
		"""

		return self.__textColor

	@textColor.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def textColor(self, value):
		"""
		Setter for **self.__textColor** attribute.

		:param value: Attribute value.
		:type value: int or QColor
		"""

		if value is not None:
			assert type(value) in (Qt.GlobalColor, QColor), \
			"'{0}' attribute: '{1}' type is not 'int' or 'QColor'!".format("textColor", value)
		self.__textColor = value

	@textColor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def textColor(self):
		"""
		Deleter for **self.__textColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "textColor"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def showMessage(self, message, textAlignement=Qt.AlignLeft, textColor=None, waitTime=None):
		"""
		Reimplements the :meth:`QSplashScreen.showMessage` method.

		:param message: Message to display on the splashscreen.
		:type message: unicode
		:param textAlignement: Text message alignment.
		:type textAlignement: object
		:param textColor: Text message color.
		:type textColor: object
		:param waitTime: Wait time.
		:type waitTime: int
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
