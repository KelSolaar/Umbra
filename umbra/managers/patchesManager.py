#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**patchesManager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`PatchesManager` and :class:`Patches` classes.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
import sys

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
import foundations.strings as strings
import foundations.walkers
import umbra.exceptions
from foundations.io import File
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

__all__ = ["LOGGER", "Patch", "PatchesManager"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Patch(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for :class:`PatchesManager` class patch.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: name, path, module, apply, uid. ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class PatchesManager(object):
	"""
	This class defines the Application patches manager. 
	"""

	@core.executionTrace
	def __init__(self, historyFile=None, paths=None, extension="py"):
		"""
		This method initializes the class.

		:param historyFile: Patches history file. ( String )
		:param paths: Patches paths. ( Tuple / List )
		:param extension: Patches extension. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__historyFile = None
		self.historyFile = historyFile
		self.__paths = None
		self.paths = paths
		self.__extension = None
		self.extension = extension

		if foundations.common.pathExists(self.__historyFile) is False:
			open(self.__historyFile, "w").close()

		self.__patches = {}

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def historyFile(self):
		"""
		This method is the property for **self.__historyFile** attribute.

		:return: self.__historyFile. ( String )
		"""

		return self.__historyFile

	@historyFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def historyFile(self, value):
		"""
		This method is the setter method for **self.__historyFile** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"historyFile", value)
		self.__historyFile = value

	@historyFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def historyFile(self):
		"""
		This method is the deleter method for **self.__historyFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "historyFile"))

	@property
	def paths(self):
		"""
		This method is the property for **self.__paths** attribute.

		:return: self.__paths. ( Tuple / List )
		"""

		return self.__paths

	@paths.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def paths(self, value):
		"""
		This method is the setter method for **self.__paths** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
			"paths", value)
			for element in value:
				assert type(element) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"paths", element)
				assert os.path.exists(element), "'{0}' attribute: '{1}' directory doesn't exists!".format("paths", element)
		self.__paths = value

	@paths.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def paths(self):
		"""
		This method is the deleter method for **self.__paths** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "paths"))

	@property
	def extension(self):
		"""
		This method is the property for **self.__extension** attribute.

		:return: self.__extension. ( String )
		"""

		return self.__extension

	@extension.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def extension(self, value):
		"""
		This method is the setter method for **self.__extension** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"extension", value)
		self.__extension = value

	@extension.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def extension(self):
		"""
		This method is the deleter method for **self.__extension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "extension"))

	@property
	def patches(self):
		"""
		This method is the property for **self.__patches** attribute.

		:return: self.__patches. ( Dictionary )
		"""

		return self.__patches

	@patches.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def patches(self, value):
		"""
		This method is the setter method for **self.__patches** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "patches"))

	@patches.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def patches(self):
		"""
		This method is the deleter method for **self.__patches** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "patches"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __getitem__(self, patch):
		"""
		This method reimplements the :meth:`object.__getitem__` method.

		:param patch: Patch name. ( String )
		:return: Patch. ( Patch )
		"""

		return self.__patches.__getitem__(patch)

	@core.executionTrace
	def __iter__(self):
		"""
		This method reimplements the :meth:`object.__iter__` method.

		:return: Patchs iterator. ( Object )
		"""

		return self.__patches.iteritems()

	@core.executionTrace
	def __contains__(self, patch):
		"""
		This method reimplements the :meth:`object.__contains__` method.

		:param patch: Patch name. ( String )
		:return: Patch existence. ( Boolean )
		"""

		return patch in self.__patches.keys()

	@core.executionTrace
	def __len__(self):
		"""
		This method reimplements the :meth:`object.__len__` method.

		:return: Patchs count. ( Integer )
		"""

		return len(self.__patches.keys())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listPatches(self):
		"""
		This method returns the registered patches.

		:return: Patches list. ( List )
		"""

		return sorted(self.__patches.keys())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def isPatchRegistered(self, patch):
		"""
		This method returns if the given patch is registered.

		:param patch: Patch. ( String )
		:return: Is patch registered. ( Boolean )
		"""

		return patch in self

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, umbra.exceptions.PatchInterfaceError)
	def registerPatch(self, name, path):
		"""
		This method registers given patch.

		:param name: Patch name. ( String )
		:param path: Patch path. ( String )
		:return: Method success. ( Boolean )
		"""

		patch = strings.getSplitextBasename(path)
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

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, umbra.exceptions.PatchRegistrationError)
	def registerPatches(self):
		"""
		This method registers the patches.

		:return: Method success. ( Boolean )
		"""

		if not self.__paths:
			return False

		unregisteredPatches = []
		for path in self.paths:
			for file in foundations.walkers.filesWalker(path, ("\.{0}$".format(self.__extension),), ("\._",)):
				name = strings.getSplitextBasename(file)
				if not self.registerPatch(name, file):
					unregisteredPatches.append(name)

		if not unregisteredPatches:
			return True
		else:
			raise umbra.exceptions.PatchRegistrationError(
			"{0} | '{1}' patches failed to register!".format(self.__class__.__name__,
																", ".join(unregisteredPatches)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, umbra.exceptions.PatchApplyError)
	def applyPatch(self, patch):
		"""
		This method applies given patch.

		:param patch: Patch. ( Patch )
		:return: Method success. ( Boolean )
		"""

		historyFile = File(self.__historyFile)
		patchesHistory = historyFile.read() and [line.strip() for line in historyFile.content] or list()

		if patch.uid not in patchesHistory:
			LOGGER.debug("> Applying '{0}' patch!".format(patch.name))
			if patch.apply():
				historyFile.content = ["{0}\n".format(patch.uid)]
				historyFile.append()
			else:
				raise umbra.exceptions.PatchApplyError("{0} | '{1}' patch failed to apply!".format(
				self.__class__.__name__, patch.path))
		else:
			LOGGER.debug("> '{0}' patch is already applied!".format(patch.name))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def applyPatches(self):
		"""
		This method applies the patches.

		:return: Method success. ( Boolean )
		"""

		success = True
		for name, patch in sorted(self):
			success = self.applyPatch(patch)
		return success

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getPatchFromUid(self, uid):
		"""
		This method returns the patch with given uid.

		:param uid: Patch uid. ( String )
		:return: Patch. ( Patch )
		"""

		for name, patch in self:
			if patch.uid == uid:
				return patch
