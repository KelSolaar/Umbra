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

from __future__ import unicode_literals

import foundations.exceptions
from umbra.globals.runtime_globals import RuntimeGlobals
from umbra.globals.ui_constants import UiConstants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
        "notify_exception_handler",
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

def notify_exception_handler(*args):
    """
    Provides a notifier exception handler.

    :param \*args: Arguments.
    :type \*args: \*
    :return: Definition success.
    :rtype: bool
    """

    callback = RuntimeGlobals.components_manager["factory.script_editor"].restore_development_layout
    foundations.exceptions.base_exception_handler(*args)
    cls, instance = foundations.exceptions.extract_exception(*args)[:2]
    RuntimeGlobals.notifications_manager.exceptify(message="{0}".format(instance), notification_clicked_slot=callback)
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
    Defines the abstract base class for :class:`umbra.managers.actions_manager.ActionsManager` related exceptions.
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
    Defines the abstract base class for :class:`umbra.managers.patches_manager.PatchesManager` related exceptions.
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
    Defines the abstract base class for :class:`umbra.managers.layouts_manager.LayoutsManager` related exceptions.
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
    Defines the abstract base class for :class:`umbra.managers.file_system_events_manager.FileSystemEventsManager`
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
