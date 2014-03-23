#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**exceptions.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **Umbra** package exceptions.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

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
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Provides a notifier exception handler.

	:param \*args: Arguments.
	:type \*args: \*
	:return: Definition success.
	:rtype: bool
	"""

	callback = RuntimeGlobals.componentsManager["factory.scriptEditor"].restoreDevelopmentLayout
	foundations.exceptions.baseExceptionHandler(*args)
	cls, instance = foundations.exceptions.extractException(*args)[:2]
	RuntimeGlobals.notificationsManager.exceptify(message="{0}".format(instance), notificationClickedSlot=callback)
	return True

class AbstractEngineError(foundations.exceptions.AbstractError):
	"""
	Defines the abstract base class for engine related exceptions.
	"""

	pass

class EngineConfigurationError(AbstractEngineError):
	"""
	Defines engine configuration exception.
	"""

	pass

class EngineInitializationError(AbstractEngineError):
	"""
	Defines engine initialization exception.
	"""

	pass

class ResourceExistsError(foundations.exceptions.AbstractOsError):
	"""
	Defines non existing resource exception.
	"""

	pass

class AbstractActionsManagerError(foundations.exceptions.AbstractError):
	"""
	Defines the abstract base class for :class:`umbra.managers.actionsManager.ActionsManager` related exceptions.
	"""

	pass

class CategoryExistsError(AbstractActionsManagerError):
	"""
	Defines non existing category exception.
	"""

	pass

class ActionExistsError(AbstractActionsManagerError):
	"""
	Defines non existing action exception.
	"""

	pass

class AbstractPatchesManagerError(foundations.exceptions.AbstractError):
	"""
	Defines the abstract base class for :class:`umbra.managers.patchesManager.PatchesManager` related exceptions.
	"""

	pass

class PatchRegistrationError(AbstractPatchesManagerError):
	"""
	Defines patch registration exception.
	"""

	pass

class PatchInterfaceError(AbstractPatchesManagerError):
	"""
	Defines patch interface exception.
	"""

	pass

class PatchApplyError(AbstractPatchesManagerError):
	"""
	Defines patch apply exception.
	"""

	pass

class AbstractLayoutsManagerError(foundations.exceptions.AbstractError):
	"""
	Defines the abstract base class for :class:`umbra.managers.layoutsManager.LayoutsManager` related exceptions.
	"""

	pass

class LayoutRegistrationError(AbstractLayoutsManagerError):
	"""
	Defines layout registration exception.
	"""

	pass

class LayoutExistError(AbstractLayoutsManagerError):
	"""
	Defines non existing layout exception.
	"""

	pass

class AbstractFileSystemEventsManagerError(foundations.exceptions.AbstractError):
	"""
	Defines the abstract base class for :class:`umbra.managers.fileSystemEventsManager.FileSystemEventsManager`
	related exceptions.
	"""

	pass

class PathRegistrationError(AbstractFileSystemEventsManagerError):
	"""
	Defines path registration exception.
	"""

	pass

class PathExistsError(AbstractFileSystemEventsManagerError):
	"""
	Defines non existing path exception.
	"""

	pass

class AbstractLanguageError(foundations.exceptions.AbstractError):
	"""
	Defines the abstract base class for language related exceptions.
	"""

	pass

class LanguageGrammarError(AbstractLanguageError):
	"""
	Defines language grammar exception.
	"""

	pass
