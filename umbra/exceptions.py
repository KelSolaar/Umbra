#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**exceptions.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Umbra** package exceptions. 

**Others:**

"""

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["AbstractEngineError",
			"EngineConfigurationError",
			"EngineInitializationError",
			"ResourceExistsError",
			"AbstractActionsManagerError",
			"CategoryExistsError",
			"ActionExistsError",
			"AbstractPatchesManagerError",
			"PatchRegistrationError",
			"PatchInterfaceError",
			"PatchApplyError",
			"AbstractLayoutsManagerError",
			"LayoutRegistrationError",
			"LayoutExistError",
			"AbstractFileSystemEventsManagerError",
			"PathRegistrationError",
			"PathExistsError"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class AbstractEngineError(foundations.exceptions.AbstractError):
	"""
	This class is the abstract base class for engine related exceptions.
	"""

	pass

class EngineConfigurationError(foundations.exceptions.AbstractError):
	"""
	This class is used for engine configuration exceptions.
	"""

	pass

class EngineInitializationError(foundations.exceptions.AbstractError):
	"""
	This class is used for engine initialization exceptions.
	"""

	pass

class ResourceExistsError(foundations.exceptions.AbstractOsError):
	"""
	This class is used for non existing resource exceptions.
	"""

	pass

class AbstractActionsManagerError(foundations.exceptions.AbstractError):
	"""
	This class is the abstract base class for :class:`umbra.managers.actionsManager.ActionsManager` related exceptions.
	"""

	pass

class CategoryExistsError(AbstractActionsManagerError):
	"""
	This class is used for non existing category exceptions.
	"""

	pass

class ActionExistsError(AbstractActionsManagerError):
	"""
	This class is used for non existing action exceptions.
	"""

	pass

class AbstractPatchesManagerError(foundations.exceptions.AbstractError):
	"""
	This class is the abstract base class for :class:`umbra.managers.patchesManager.PatchesManager` related exceptions.
	"""

	pass

class PatchRegistrationError(AbstractPatchesManagerError):
	"""
	This class is used for patch registration exceptions.
	"""

	pass

class PatchInterfaceError(AbstractPatchesManagerError):
	"""
	This class is used for patch interface exceptions.
	"""

	pass

class PatchApplyError(AbstractPatchesManagerError):
	"""
	This class is used for patch apply exceptions.
	"""

	pass

class AbstractLayoutsManagerError(foundations.exceptions.AbstractError):
	"""
	This class is the abstract base class for :class:`umbra.managers.layoutsManager.LayoutsManager` related exceptions.
	"""

	pass

class LayoutRegistrationError(AbstractLayoutsManagerError):
	"""
	This class is used for layout registration exceptions.
	"""

	pass

class LayoutExistError(AbstractLayoutsManagerError):
	"""
	This class is used for non existing layout exceptions.
	"""

	pass

class AbstractFileSystemEventsManagerError(foundations.exceptions.AbstractError):
	"""
	This class is the abstract base class for :class:`umbra.managers.fileSystemEventsManager.FileSystemEventsManager`
	related exceptions.
	"""

	pass

class PathRegistrationError(AbstractFileSystemEventsManagerError):
	"""
	This class is used for path registration exceptions.
	"""

	pass

class PathExistsError(AbstractFileSystemEventsManagerError):
	"""
	This class is used for non existing path exceptions.
	"""

	pass
