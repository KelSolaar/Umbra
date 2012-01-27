#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class Workers.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
from PyQt4.QtCore import QThread
from PyQt4.QtCore import pyqtSignal

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
from foundations.walkers import OsWalker
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

__all__ = ["LOGGER", "Grep_worker"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Grep_worker(QThread):
	"""
	This class is a `QThread <http://doc.qt.nokia.com/qthread.html>`_ subclass used
	to search for a pattern in a directory files.
	"""

	# Custom signals definitions.
#	databaseChanged = pyqtSignal(list)
#	"""
#	This signal is emited by the :class:`Grep_worker` class
#	when database Ibl Sets have been updated. ( pyqtSignal )
#	
#	:return: Updated Ibl Sets. ( List )		
#	"""

	@core.executionTrace
	def __init__(self, parent, location, settings):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QThread.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__container = parent

		self.__location = location
		self.__settings = settings

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def run(self):
		"""
		This method reimplements the :meth:`QThread.run` method.
		"""

		self.__grep()

	@core.executionTrace
	def __grep(self):
		"""
		This method performs the search.
		"""

		files = self.__location.files
		for directory in self.__location.directories:
			osWalker = OsWalker(directory)
			osWalker.walk(self.__location.filtersIn,
						self.__location.filtersOut,
						visitor=lambda x, y: foundations.common.isBinaryFile(x.get(y)) and x.pop(y))
			files.extend(osWalker.files.values())

		for file in files:
			print file
