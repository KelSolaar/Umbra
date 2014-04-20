#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**file_system_events_manager.py**

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

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class FileSystemEventsManager(QThread):
	"""
	Defines the file system events manager.
	"""

	# Custom signals definitions.
	file_changed = pyqtSignal(unicode)
	"""
	This signal is emited by the :class:`FileSystemEventsManager` class when a file is changed.

	:return: Current changed file.
	:rtype: unicode
	"""

	file_invalidated = pyqtSignal(unicode)
	"""
	This signal is emited by the :class:`FileSystemEventsManager` class when a file is invalidated.

	:return: Current invalidated file.
	:rtype: unicode
	"""

	directory_changed = pyqtSignal(unicode)
	"""
	This signal is emited by the :class:`FileSystemEventsManager` class when a directory is changed.

	:return: Current changed directory.
	:rtype: unicode
	"""

	directory_invalidated = pyqtSignal(unicode)
	"""
	This signal is emited by the :class:`FileSystemEventsManager` class when a directory is invalidated.

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
		self.__timer_cycle_multiplier = 5

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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		Setter for **self.__container** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def paths(self, value):
		"""
		Setter for **self.__paths** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "paths"))

	@paths.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def timer(self, value):
		"""
		Setter for **self.__timer** attribute.

		:param value: Attribute value.
		:type value: QTimer
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "timer"))

	@timer.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def timer(self):
		"""
		Deleter for **self.__timer** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "timer"))

	@property
	def timer_cycle_multiplier(self):
		"""
		Property for **self.__timer_cycle_multiplier** attribute.

		:return: self.__timer_cycle_multiplier.
		:rtype: float
		"""

		return self.__timer_cycle_multiplier

	@timer_cycle_multiplier.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def timer_cycle_multiplier(self, value):
		"""
		Setter for **self.__timer_cycle_multiplier** attribute.

		:param value: Attribute value.
		:type value: float
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "timer_cycle_multiplier"))

	@timer_cycle_multiplier.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def timer_cycle_multiplier(self):
		"""
		Deleter for **self.__timer_cycle_multiplier** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "timer_cycle_multiplier"))

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

	def __setitem__(self, path, modified_time):
		"""
		Reimplements the :meth:`object.__setitem__` method.

		:param path: Path.
		:type path: unicode
		:param modified_time: Modified time.
		:type modified_time: int or float
		"""

		self.register_path(path, modified_time)

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
		self.__timer.start(Constants.default_timer_cycle * self.__timer_cycle_multiplier)

		self.__timer.timeout.connect(self.__watch_file_system, Qt.DirectConnection)

		self.exec_()

	def __watch_file_system(self):
		"""
		Watches the file system for paths that have been changed or invalidated on disk.
		"""

		for path, data in self.__paths.items():
			stored_modified_time, is_file = data
			try:
				if not foundations.common.path_exists(path):
					LOGGER.warning(
					"!> {0} | '{1}' path has been invalidated and will be unregistered!".format(self.__class__.__name__, path))
					del(self.__paths[path])
					if is_file:
						self.file_invalidated.emit(path)
					else:
						self.directory_invalidated.emit(path)
					continue
			except KeyError:
				LOGGER.debug("> {0} | '{1}' path has been unregistered while iterating!".format(
				self.__class__.__name__, path))
				continue

			try:
				modified_time = self.get_path_modified_time(path)
			except OSError:
				LOGGER.debug("> {0} | '{1}' path has been invalidated while iterating!".format(
				self.__class__.__name__, path))
				continue

			if stored_modified_time != modified_time:
				self.__paths[path] = (modified_time, os.path.isfile(path))
				LOGGER.debug("> {0} | '{1}' path has been changed!".format(self.__class__.__name__, path))
				if is_file:
					self.file_changed.emit(path)
				else:
					self.directory_changed.emit(path)

	def list_paths(self):
		"""
		Returns the registered paths.

		:return: Registered paths.
		:rtype: list
		"""

		return sorted(self.__paths.keys())

	def is_path_registered(self, path):
		"""
		Returns if the given path is registered.

		:param path: Path name.
		:type path: unicode
		:return: Is path registered.
		:rtype: bool
		"""

		return path in self

	@foundations.exceptions.handle_exceptions(foundations.exceptions.PathExistsError,
											umbra.exceptions.PathRegistrationError)
	def register_path(self, path, modified_time=None):
		"""
		Registers given path.

		:param path: Path name.
		:type path: unicode
		:param modified_time: Custom modified time.
		:type modified_time: int or float
		:return: Method success.
		:rtype: bool
		"""

		if not foundations.common.path_exists(path):
			raise foundations.exceptions.PathExistsError("{0} | '{1}' path doesn't exists!".format(
			self.__class__.__name__, path))

		if path in self:
			raise umbra.exceptions.PathRegistrationError("{0} | '{1}' path is already registered!".format(
			self.__class__.__name__, path))

		self.__paths[path] = (self.get_path_modified_time(path) if modified_time is None else modified_time, os.path.isfile(path))
		return True

	@foundations.exceptions.handle_exceptions(umbra.exceptions.PathExistsError)
	def unregister_path(self, path):
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
	def get_path_modified_time(path):
		"""
		Returns given path modification time.

		:param path: Path.
		:type path: unicode
		:return: Modification time.
		:rtype: int
		"""

		return float(foundations.common.get_first_item(str(os.path.getmtime(path)).split(".")))
