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
import logging
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QSplashScreen

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Delayed_QSplashScreen"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Delayed_QSplashScreen(QSplashScreen):
	"""
	This class is a `QSplashScreen <http://doc.qt.nokia.com/qsplashscreen.html>`_ subclass providing
	delayed messages capabilities.
	"""

	@core.executionTrace
	def __init__(self, picture, waitTime=None):
		"""
		This method initializes the class.

		:param picture: Current picture path. ( String )
		:param waitTime: wait time. ( Integer )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QSplashScreen.__init__(self, picture)

		self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

		# --- Setting class attributes. ---
		self.__waitTime = None
		self.waitTime = waitTime

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
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def waitTime(self, value):
		"""
		This method is the setter method for **self.__waitTime** attribute.

		:param value: Attribute value. ( Integer / Float )
		"""

		if value is not None:
			assert type(value) in (int, float), "'{0}' attribute: '{1}' type is not 'int' or 'float'!".format(
			"waitTime", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("waitTime", value)
		self.__waitTime = value

	@waitTime.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def waitTime(self):
		"""
		This method is the deleter method for **self.__waitTime** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "waitTime"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def setMessage(self, message, textAlignement=Qt.AlignLeft, textColor=Qt.black, waitTime=None):
		"""
		This method initializes the class.

		:param message: Message to display on the splashscreen. ( String )
		:param textAlignement: Text message alignment. ( Object )
		:param textColor: Text message color. ( Object )
		:param waitTime: Wait time. ( Integer )
		"""

		self.showMessage(message, textAlignement, textColor)

		# Force QSplashscreen refresh.
		QApplication.processEvents()

		if self.__waitTime:
			waitTime = self.__waitTime

		waitTime and core.wait(waitTime)
