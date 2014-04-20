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

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Delayed_QSplashScreen(QSplashScreen):
	"""
	Defines a `QSplashScreen <http://doc.qt.nokia.com/qsplashscreen.html>`_ subclass providing
	delayed messages capabilities.
	"""

	def __init__(self, pixmap, wait_time=0, text_color=Qt.black, *args, **kwargs):
		"""
		Initializes the class.

		:param pixmap: Current pixmap path.
		:type pixmap: unicode
		:param wait_time: wait time.
		:type wait_time: int
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QSplashScreen.__init__(self, pixmap, *args, **kwargs)

		self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

		# --- Setting class attributes. ---
		self.__wait_time = None
		self.wait_time = wait_time
		self.__text_color = None
		self.text_color = text_color

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def wait_time(self):
		"""
		Property for **self.__wait_time** attribute.

		:return: self.__wait_time
		:rtype: int or float
		"""

		return self.__wait_time

	@wait_time.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def wait_time(self, value):
		"""
		Setter for **self.__wait_time** attribute.

		:param value: Attribute value.
		:type value: int or float
		"""

		if value is not None:
			assert type(value) in (int, float), "'{0}' attribute: '{1}' type is not 'int' or 'float'!".format(
			"wait_time", value)
			assert value >= 0, "'{0}' attribute: '{1}' need to be positive!".format("wait_time", value)
		self.__wait_time = value

	@wait_time.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def wait_time(self):
		"""
		Deleter for **self.__wait_time** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "wait_time"))

	@property
	def text_color(self):
		"""
		Property for **self.__text_color** attribute.

		:return: self.__text_color
		:rtype: int or QColor
		"""

		return self.__text_color

	@text_color.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def text_color(self, value):
		"""
		Setter for **self.__text_color** attribute.

		:param value: Attribute value.
		:type value: int or QColor
		"""

		if value is not None:
			assert type(value) in (Qt.GlobalColor, QColor), \
			"'{0}' attribute: '{1}' type is not 'int' or 'QColor'!".format("text_color", value)
		self.__text_color = value

	@text_color.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def text_color(self):
		"""
		Deleter for **self.__text_color** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "text_color"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def show_message(self, message, text_alignement=Qt.AlignLeft, text_color=None, wait_time=None):
		"""
		Reimplements the :meth:`QSplashScreen.show_message` method.

		:param message: Message to display on the splashscreen.
		:type message: unicode
		:param text_alignement: Text message alignment.
		:type text_alignement: object
		:param text_color: Text message color.
		:type text_color: object
		:param wait_time: Wait time.
		:type wait_time: int
		"""

		QSplashScreen.showMessage(self, message, text_alignement, self.__text_color if text_color is None else text_color)

		# Force QSplashscreen refresh.
		QApplication.processEvents()

		foundations.core.wait(self.__wait_time if wait_time is None else wait_time)

if __name__ == "__main__":
	from PyQt4.QtGui import QPixmap

	import umbra.ui.common
	from umbra.globals.ui_constants import UiConstants

	application = umbra.ui.common.get_application_instance()

	splashScreen = Delayed_QSplashScreen(QPixmap(umbra.ui.common.get_resource_path(UiConstants.splash_screen_image)))
	splashScreen.show()
	splashScreen.show_message("This is a test message!", wait_time=1.5)
	splashScreen.show_message("This is another test message!", wait_time=1.5)
	splashScreen.show_message("This is a white test message!", text_color=Qt.white, wait_time=1.5)
	splashScreen.show_message("This is a left aligned message!", text_alignement=Qt.AlignRight, wait_time=1.5)
