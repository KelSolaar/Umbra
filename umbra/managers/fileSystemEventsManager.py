#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**fileSystemEventsManager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`FileSystemEventsManager` class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QThread
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import pyqtSignal

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import umbra.exceptions
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "FileSystemEventsManager"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class FileSystemEventsManager(QThread):
	"""
	Defines the file system events manager.
	"""

	# Custom signals definitions.
	fileChanged = pyqtSignal(unicode)
	"""
	This signal is emited by the :class:`FileSystemEventsManager` class when a file is changed. ( pyqtSignal )

	:return: Current changed file.
	:rtype: unicode
	"""

	fileInvalidated = pyqtSignal(unicode)
	"""
	This signal is emited by the :class:`FileSystemEventsManager` class when a file is invalidated. ( pyqtSignal )

	:return: Current invalidated file.
	:rtype: unicode
	"""

	directoryChanged = pyqtSignal(unicode)
	"""
	This signal is emited by the :class:`FileSystemEventsManager` class when a directory is changed. ( pyqtSignal )

	:return: Current changed directory.
	:rtype: unicode
	"""

	directoryInvalidated = pyqtSignal(unicode)
	"""
	This signal is emited by the :class:`FileSystemEventsManager` class when a directory is invalidated. ( pyqtSignal )

	:return: Current invalidated directory.
	:rtype: unicode
	"""

	def __init__(self, parent=None):
		"""
		Initializes the class.
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QThread.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__container = parent

		self.__paths = {}

		self.__timer = None
		self.__timerCycleMultiplier = 5

		self.__toRegisterPaths = {}
		self.__toUnregisterPaths = []

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def container(self):
		"""
		Property for **self.__container** attribute.

		:return: self.__container.
		:rtype: QObject
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		Setter for **self.__container** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		Deleter for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def paths(self):
		"""
		Property for **self.__paths** attribute.

		:return: self.__paths.
		:rtype: dict
		"""

		return self.__paths

	@paths.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def paths(self, value):
		"""
		Setter for **self.__paths** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "paths"))

	@paths.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def paths(self):
		"""
		Deleter for **self.__paths** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "paths"))

	@property
	def timer(self):
		"""
		Property for **self.__timer** attribute.

		:return: self.__timer.
		:rtype: QTimer
		"""

		return self.__timer

	@timer.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def timer(self, value):
		"""
		Setter for **self.__timer** attribute.

		:param value: Attribute value.
		:type value: QTimer
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "timer"))

	@timer.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def timer(self):
		"""
		Deleter for **self.__timer** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "timer"))

	@property
	def timerCycleMultiplier(self):
		"""
		Property for **self.__timerCycleMultiplier** attribute.

		:return: self.__timerCycleMultiplier.
		:rtype: float
		"""

		return self.__timerCycleMultiplier

	@timerCycleMultiplier.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def timerCycleMultiplier(self, value):
		"""
		Setter for **self.__timerCycleMultiplier** attribute.

		:param value: Attribute value.
		:type value: float
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "timerCycleMultiplier"))

	@timerCycleMultiplier.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def timerCycleMultiplier(self):
		"""
		Deleter for **self.__timerCycleMultiplier** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "timerCycleMultiplier"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __getitem__(self, path):
		"""
		Reimplements the :meth:`object.__getitem__` method.

		:param path: Path name.
		:type path: unicode
		:return: Path.
		:rtype: Path
		"""

		return self.__paths.__getitem__(path)

	def __setitem__(self, path, modifiedTime):
		"""
		Reimplements the :meth:`object.__setitem__` method.

		:param path: Path.
		:type path: unicode
		:param modifiedTime: Modified time.
		:type modifiedTime: int or float
		"""

		self.registerPath(path, modifiedTime)

	def __iter__(self):
		"""
		Reimplements the :meth:`object.__iter__` method.

		:return: Paths iterator.
		:rtype: object
		"""

		return self.__paths.iteritems()

	def __contains__(self, path):
		"""
		Reimplements the :meth:`object.__contains__` method.

		:param path: Path name.
		:type path: unicode
		:return: Path existence.
		:rtype: bool
		"""

		return path in self.__paths

	def __len__(self):
		"""
		Reimplements the :meth:`object.__len__` method.

		:return: Paths count.
		:rtype: int
		"""

		return len(self.__paths)

	def get(self, path, default=None):
		"""
		Returns given path value.

		:param path: Path name.
		:type path: unicode
		:param default: Default value if path is not found.
		:type default: object
		:return: Action.
		:rtype: QAction
		"""

		try:
			return self.__getitem__(path)
		except KeyError as error:
			return default

	def run(self):
		"""
		Reimplements the :meth:`QThread.run` method.
		"""

		self.__timer = QTimer()
		self.__timer.moveToThread(self)
		self.__timer.start(Constants.defaultTimerCycle * self.__timerCycleMultiplier)

		self.__timer.timeout.connect(self.__watchFileSystem, Qt.DirectConnection)

		self.exec_()

	def __watchFileSystem(self):
		"""
		Watches the file system for paths that have been changed or invalidated on disk.
		"""

		for path, data in self.__paths.items():
			storedModifiedTime, isFile = data
			try:
				if not foundations.common.pathExists(path):
					LOGGER.warning(
					"!> {0} | '{1}' path has been invalidated and will be unregistered!".format(self.__class__.__name__, path))
					del(self.__paths[path])
					if isFile:
						self.fileInvalidated.emit(path)
					else:
						self.directoryInvalidated.emit(path)
					continue
			except KeyError:
				LOGGER.debug("> {0} | '{1}' path has been unregistered while iterating!".format(
				self.__class__.__name__, path))
				continue

			try:
				modifiedTime = self.getPathModifiedTime(path)
			except OSError:
				LOGGER.debug("> {0} | '{1}' path has been invalidated while iterating!".format(
				self.__class__.__name__, path))
				continue

			if storedModifiedTime != modifiedTime:
				self.__paths[path] = (modifiedTime, os.path.isfile(path))
				LOGGER.debug("> {0} | '{1}' path has been changed!".format(self.__class__.__name__, path))
				if isFile:
					self.fileChanged.emit(path)
				else:
					self.directoryChanged.emit(path)

	def listPaths(self):
		"""
		Returns the registered paths.

		:return: Registered paths.
		:rtype: list
		"""

		return sorted(self.__paths.keys())

	def isPathRegistered(self, path):
		"""
		Returns if the given path is registered.

		:param path: Path name.
		:type path: unicode
		:return: Is path registered.
		:rtype: bool
		"""

		return path in self

	@foundations.exceptions.handleExceptions(foundations.exceptions.PathExistsError,
											umbra.exceptions.PathRegistrationError)
	def registerPath(self, path, modifiedTime=None):
		"""
		Registers given path.

		:param path: Path name.
		:type path: unicode
		:param modifiedTime: Custom modified time.
		:type modifiedTime: int or float
		:return: Method success.
		:rtype: bool
		"""

		if not foundations.common.pathExists(path):
			raise foundations.exceptions.PathExistsError("{0} | '{1}' path doesn't exists!".format(
			self.__class__.__name__, path))

		if path in self:
			raise umbra.exceptions.PathRegistrationError("{0} | '{1}' path is already registered!".format(
			self.__class__.__name__, path))

		self.__paths[path] = (self.getPathModifiedTime(path) if modifiedTime is None else modifiedTime, os.path.isfile(path))
		return True

	@foundations.exceptions.handleExceptions(umbra.exceptions.PathExistsError)
	def unregisterPath(self, path):
		"""
		Unregisters given path.

		:param path: Path name.
		:type path: unicode
		:return: Method success.
		:rtype: bool
		"""

		if not path in self:
			raise umbra.exceptions.PathExistsError("{0} | '{1}' path isn't registered!".format(
			self.__class__.__name__, path))

		del(self.__paths[path])
		return True

	@staticmethod
	def getPathModifiedTime(path):
		"""
		Returns given path modification time.

		:param path: Path.
		:type path: unicode
		:return: Modification time.
		:rtype: int
		"""

		return float(foundations.common.getFirstItem(str(os.path.getmtime(path)).split(".")))