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
from umbra.globals.runtimeGlobals import RuntimeGlobals
from umbra.globals.uiConstants import UiConstants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
		"notifyExceptionHandler",
		"AbstractEngineError",
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
		"PathExistsError",
		"AbstractLanguageError",
		"LanguageGrammarError"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def notifyExceptionHandler(*args):
	"""
	This definition provides a notifier exception handler.

	:param \*args: Arguments. ( \* )
	:return: Definition success. ( Boolean )
	"""

	callback = RuntimeGlobals.componentsManager["factory.scriptEditor"].restoreDevelopmentLayout
	foundations.exceptions.baseExceptionHandler(*args)
	cls, instance = foundations.exceptions.extractException(*args)[:2]
	RuntimeGlobals.notificationsManager.exceptify(message="{0}".format(instance), notificationClickedSlot=callback)
	return True

class AbstractEngineError(foundations.exceptions.AbstractError):
	"""
	This class is the abstract base class for engine related exceptions.
	"""

	pass

class EngineConfigurationError(AbstractEngineError):
	"""
	This class is used for engine configuration exceptions.
	"""

	pass

class EngineInitializationError(AbstractEngineError):
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

class AbstractLanguageError(foundations.exceptions.AbstractError):
	"""
	This class is the abstract base class for language related exceptions.
	"""

	pass

class LanguageGrammarError(AbstractLanguageError):
	"""
	This class is used for language grammar exceptions.
	"""

	pass
