#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**fileSystemEventsManager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`FileSystemEventsManager` class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import logging
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QThread
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import pyqtSignal

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import umbra.exceptions
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

__all__ = ["LOGGER", "FileSystemEventsManager"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class FileSystemEventsManager(QThread):
	"""
	This class defines the file system events manager. 
	"""

	# Custom signals definitions.
	fileChanged = pyqtSignal(str)
	"""
	This signal is emited by the :class:`FileSystemEventsManager` class when a file is changed. ( pyqtSignal )

	:return: Current changed file. ( String )	
	"""

	fileInvalidated = pyqtSignal(str)
	"""
	This signal is emited by the :class:`FileSystemEventsManager` class when a file is invalidated. ( pyqtSignal )

	:return: Current invalidated file. ( String )	
	"""

	@core.executionTrace
	def __init__(self, parent):
		"""
		This method initializes the class.
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QThread.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__container = parent

		self.__paths = {}

		self.__timer = None
		self.__timerCycleMultiplier = 5

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

	@property
	def paths(self):
		"""
		This method is the property for **self.__paths** attribute.

		:return: self.__paths. ( Dictionary )
		"""

		return self.__paths

	@paths.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def paths(self, value):
		"""
		This method is the setter method for **self.__paths** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "paths"))

	@paths.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def paths(self):
		"""
		This method is the deleter method for **self.__paths** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "paths"))

	@property
	def timer(self):
		"""
		This method is the property for **self.__timer** attribute.

		:return: self.__timer. ( QTimer )
		"""

		return self.__timer

	@timer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self, value):
		"""
		This method is the setter method for **self.__timer** attribute.

		:param value: Attribute value. ( QTimer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "timer"))

	@timer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self):
		"""
		This method is the deleter method for **self.__timer** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "timer"))

	@property
	def timerCycleMultiplier(self):
		"""
		This method is the property for **self.__timerCycleMultiplier** attribute.

		:return: self.__timerCycleMultiplier. ( Float )
		"""

		return self.__timerCycleMultiplier

	@timerCycleMultiplier.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timerCycleMultiplier(self, value):
		"""
		This method is the setter method for **self.__timerCycleMultiplier** attribute.

		:param value: Attribute value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "timerCycleMultiplier"))

	@timerCycleMultiplier.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timerCycleMultiplier(self):
		"""
		This method is the deleter method for **self.__timerCycleMultiplier** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "timerCycleMultiplier"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __getitem__(self, path):
		"""
		This method reimplements the :meth:`object.__getitem__` method.

		:param path: Path name. ( String )
		:return: Path. ( Path )
		"""

		return self.__paths.__getitem__(path)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __iter__(self):
		"""
		This method reimplements the :meth:`object.__iter__` method.

		:return: Paths iterator. ( Object )
		"""

		return self.__paths.iteritems()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __contains__(self, path):
		"""
		This method reimplements the :meth:`object.__contains__` method.

		:param path: Path name. ( String )
		:return: Path existence. ( Boolean )
		"""

		return path in self.__paths.keys()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __len__(self):
		"""
		This method reimplements the :meth:`object.__len__` method.

		:return: Paths count. ( Integer )
		"""

		return len(self.__paths.keys())

	@core.executionTrace
	def run(self):
		"""
		This method reimplements the :meth:`QThread.run` method.
		"""

		self.__timer = QTimer()
		self.__timer.moveToThread(self)
		self.__timer.start(Constants.defaultTimerCycle * self.__timerCycleMultiplier)

		self.__timer.timeout.connect(self.__watchFileSystem, Qt.DirectConnection)

		self.exec_()

	@core.executionTrace
	def __watchFileSystem(self):
		"""
		This method watches the file system for paths that have been changed or invalidated on disk.
		"""

		for path, storedStatus in self:
			if not foundations.common.pathExists(path):
				del(self.__paths[path])
				LOGGER.warning(
				"!> {0} | '{1}' path has been invalidated and will be unregistered!".format(self.__class__.__name__, path))
				self.fileInvalidated.emit(path)
				continue

			status = os.stat(path)
			if storedStatus.st_mtime != status.st_mtime:
				self.__paths[path] = status
				LOGGER.debug("> {0} | '{1}' path has been changed!".format(self.__class__.__name__, path))
				self.fileChanged.emit(path)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listPaths(self):
		"""
		This method returns the registered paths.

		:return: Registered paths. ( List )
		"""

		return sorted(self.__paths.keys())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def isPathRegistered(self, path):
		"""
		This method returns if the given path is registered.

		:param path: Path name. ( String )
		:return: Is path registered. ( Boolean )
		"""

		return path in self

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None,
											False,
											foundations.exceptions.PathExistsError,
											umbra.exceptions.PathRegistrationError)
	def registerPath(self, path):
		"""
		This method registers given path.

		:param path: Path name. ( String )
		:return: Method success. ( Boolean )
		"""

		if not foundations.common.pathExists(path):
			raise foundations.exceptions.PathExistsError("{0} | '{1}' path doesn't exists!".format(
			self.__class__.__name__, path))

		if path in self:
			raise umbra.exceptions.PathRegistrationError("{0} | '{1}' path is already registered!".format(
			self.__class__.__name__, path))

		self.__paths[path] = os.stat(path)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, umbra.exceptions.PathExistsError)
	def unregisterPath(self, path):
		"""
		This method unregisters given path.

		:param path: Path name. ( String )
		:return: Method success. ( Boolean )
		"""

		if not path in self:
			raise umbra.exceptions.PathExistsError("{0} | '{1}' path isn't registered!".format(
			self.__class__.__name__, path))

		del(self.__paths[path])
		return True
