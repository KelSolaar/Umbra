#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**patches_manager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`PatchesManager` and :class:`Patches` classes.

**Others:**

"""

from __future__ import unicode_literals

import os
import sys

import foundations.common
import foundations.data_structures
import foundations.exceptions
import foundations.strings
import foundations.verbose
import foundations.walkers
import umbra.exceptions
from foundations.io import File

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Patch", "PatchesManager"]

LOGGER = foundations.verbose.install_logger()

class Patch(foundations.data_structures.Structure):
	"""
	Defines a storage object for :class:`PatchesManager` class patch.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param \*\*kwargs: name, path, module, apply, uid.
		:type \*\*kwargs: dict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.data_structures.Structure.__init__(self, **kwargs)

class PatchesManager(object):
	"""
	Defines the Application patches manager.
	"""

	def __init__(self, history_file=None, paths=None, extension="py"):
		"""
		Initializes the class.

		:param history_file: Patches history file.
		:type history_file: unicode
		:param paths: Patches paths.
		:type paths: tuple or list
		:param extension: Patches extension.
		:type extension: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__history_file = None
		self.history_file = history_file
		self.__paths = None
		self.paths = paths
		self.__extension = None
		self.extension = extension

		if foundations.common.path_exists(self.__history_file) is False:
			open(self.__history_file, "w").close()

		self.__patches = {}

	@property
	def history_file(self):
		"""
		Property for **self.__history_file** attribute.

		:return: self.__history_file.
		:rtype: unicode
		"""

		return self.__history_file

	@history_file.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def history_file(self, value):
		"""
		Setter for **self.__history_file** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"history_file", value)
		self.__history_file = value

	@history_file.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def history_file(self):
		"""
		Deleter for **self.__history_file** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "history_file"))

	@property
	def paths(self):
		"""
		Property for **self.__paths** attribute.

		:return: self.__paths.
		:rtype: tuple or list
		"""

		return self.__paths

	@paths.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def paths(self, value):
		"""
		Setter for **self.__paths** attribute.

		:param value: Attribute value.
		:type value: tuple or list
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
				"paths", value)
			for element in value:
				assert type(element) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
					"paths", element)
				assert os.path.exists(element), "'{0}' attribute: '{1}' directory doesn't exists!".format("paths",
																										  element)
		self.__paths = value

	@paths.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def paths(self):
		"""
		Deleter for **self.__paths** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "paths"))

	@property
	def extension(self):
		"""
		Property for **self.__extension** attribute.

		:return: self.__extension.
		:rtype: unicode
		"""

		return self.__extension

	@extension.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def extension(self, value):
		"""
		Setter for **self.__extension** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"extension", value)
		self.__extension = value

	@extension.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def extension(self):
		"""
		Deleter for **self.__extension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "extension"))

	@property
	def patches(self):
		"""
		Property for **self.__patches** attribute.

		:return: self.__patches.
		:rtype: dict
		"""

		return self.__patches

	@patches.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def patches(self, value):
		"""
		Setter for **self.__patches** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "patches"))

	@patches.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def patches(self):
		"""
		Deleter for **self.__patches** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "patches"))

	def __getitem__(self, patch):
		"""
		Reimplements the :meth:`object.__getitem__` method.

		:param patch: Patch name.
		:type patch: unicode
		:return: Patch.
		:rtype: Patch
		"""

		return self.__patches.__getitem__(patch)

	def __setitem__(self, name, path):
		"""
		Reimplements the :meth:`object.__setitem__` method.

		:param name: Patch name.
		:type name: unicode
		:param path: Patch path.
		:type path: unicode
		"""

		self.register_patch(name, path)

	def __iter__(self):
		"""
		Reimplements the :meth:`object.__iter__` method.

		:return: Patchs iterator.
		:rtype: object
		"""

		return self.__patches.iteritems()

	def __contains__(self, patch):
		"""
		Reimplements the :meth:`object.__contains__` method.

		:param patch: Patch name.
		:type patch: unicode
		:return: Patch existence.
		:rtype: bool
		"""

		return patch in self.__patches

	def __len__(self):
		"""
		Reimplements the :meth:`object.__len__` method.

		:return: Patchs count.
		:rtype: int
		"""

		return len(self.__patches)

	def get(self, patch, default=None):
		"""
		Returns given patch value.

		:param patch: Patch name.
		:type patch: unicode
		:param default: Default value if patch is not found.
		:type default: object
		:return: Action.
		:rtype: QAction
		"""

		try:
			return self.__getitem__(patch)
		except KeyError as error:
			return default

	def list_patches(self):
		"""
		Returns the registered patches.

		:return: Patches list.
		:rtype: list
		"""

		return sorted(self.__patches.keys())

	def is_patch_registered(self, patch):
		"""
		Returns if the given patch is registered.

		:param patch: Patch.
		:type patch: unicode
		:return: Is patch registered.
		:rtype: bool
		"""

		return patch in self

	@foundations.exceptions.handle_exceptions(umbra.exceptions.PatchInterfaceError)
	def register_patch(self, name, path):
		"""
		Registers given patch.

		:param name: Patch name.
		:type name: unicode
		:param path: Patch path.
		:type path: unicode
		:return: Method success.
		:rtype: bool
		"""

		patch = foundations.strings.get_splitext_basename(path)
		LOGGER.debug("> Current patch: '{0}'.".format(patch))

		directory = os.path.dirname(path)
		not directory in sys.path and sys.path.append(directory)

		module = __import__(patch)
		if hasattr(module, "apply") and hasattr(module, "UID"):
			self.__patches[name] = Patch(name=name,
										 path=path,
										 module=module,
										 apply=getattr(module, "apply"),
										 uid=getattr(module, "UID"))
		else:
			raise umbra.exceptions.PatchInterfaceError(
				"{0} | '{1}' is not a valid patch and has been rejected!".format(self.__class__.__name__, patch))
		return True

	@foundations.exceptions.handle_exceptions(umbra.exceptions.PatchRegistrationError)
	def register_patches(self):
		"""
		Registers the patches.

		:return: Method success.
		:rtype: bool
		"""

		if not self.__paths:
			return False

		unregistered_patches = []
		for path in self.paths:
			for file in foundations.walkers.files_walker(path, ("\.{0}$".format(self.__extension),), ("\._",)):
				name = foundations.strings.get_splitext_basename(file)
				if not self.register_patch(name, file):
					unregistered_patches.append(name)

		if not unregistered_patches:
			return True
		else:
			raise umbra.exceptions.PatchRegistrationError(
				"{0} | '{1}' patches failed to register!".format(self.__class__.__name__,
																 ", ".join(unregistered_patches)))

	@foundations.exceptions.handle_exceptions(umbra.exceptions.PatchApplyError)
	def apply_patch(self, patch):
		"""
		Applies given patch.

		:param patch: Patch.
		:type patch: Patch
		:return: Method success.
		:rtype: bool
		"""

		history_file = File(self.__history_file)
		patches_history = history_file.cache() and [line.strip() for line in history_file.content] or []

		if patch.uid not in patches_history:
			LOGGER.debug("> Applying '{0}' patch!".format(patch.name))
			if patch.apply():
				history_file.content = ["{0}\n".format(patch.uid)]
				history_file.append()
			else:
				raise umbra.exceptions.PatchApplyError("{0} | '{1}' patch failed to apply!".format(
					self.__class__.__name__, patch.path))
		else:
			LOGGER.debug("> '{0}' patch is already applied!".format(patch.name))
		return True

	def apply_patches(self):
		"""
		Applies the patches.

		:return: Method success.
		:rtype: bool
		"""

		success = True
		for name, patch in sorted(self):
			success = self.apply_patch(patch)
		return success

	def get_patch_from_uid(self, uid):
		"""
		Returns the patch with given uid.

		:param uid: Patch uid.
		:type uid: unicode
		:return: Patch.
		:rtype: Patch
		"""

		for name, patch in self:
			if patch.uid == uid:
				return patch
