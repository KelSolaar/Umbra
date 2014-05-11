#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**engine.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    | Defines various classes, methods and definitions to run, maintain and exit the Application.
    | The main Application object is the :class:`Umbra` class.

**Others:**

"""

from __future__ import unicode_literals

import collections
import functools
import gc
import os
import optparse
import platform
import re
import sys
import time
from PyQt4.QtCore import PYQT_VERSION_STR
from PyQt4.QtCore import QEvent
from PyQt4.QtCore import QEventLoop
from PyQt4.QtCore import QString
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QPixmap

def _set_package_directory():
    """
    Sets the Application package directory in the path.
    """

    package_directory = os.path.normpath(os.path.join(os.path.dirname(__file__), "../"))
    package_directory not in sys.path and sys.path.append(package_directory)

_set_package_directory()

import foundations.globals.constants
import manager.globals.constants
import umbra.globals.constants
from umbra.globals.constants import Constants
from umbra.globals.runtime_globals import RuntimeGlobals
from umbra.globals.ui_constants import UiConstants

def _override_dependencies_globals():
    """
    Overrides dependencies globals.
    """

    foundations.globals.constants.Constants.logger = manager.globals.constants.Constants.logger = Constants.logger
    foundations.globals.constants.Constants.application_directory = \
        manager.globals.constants.Constants.application_directory = Constants.application_directory

_override_dependencies_globals()

import foundations.common

def _extend_resources_paths():
    """
    Extend resources paths.
    """

    for path in (os.path.join(umbra.__path__[0], Constants.resources_directory),
                 os.path.join(os.getcwd(), umbra.__name__, Constants.resources_directory)):
        path = os.path.normpath(path)
        if foundations.common.path_exists(path):
            path not in RuntimeGlobals.resources_directories and RuntimeGlobals.resources_directories.append(path)

_extend_resources_paths()

import foundations.core
import foundations.data_structures
import foundations.exceptions
import foundations.environment
import foundations.io
import foundations.namespace
import foundations.strings
import foundations.trace
import foundations.ui.common
import foundations.verbose
import manager.exceptions
import umbra.exceptions
import umbra.managers.actions_manager
import umbra.managers.file_system_events_manager
import umbra.managers.notifications_manager
import umbra.managers.patches_manager
import umbra.managers.layouts_manager
import umbra.reporter
import umbra.ui.common
import umbra.ui.widgets.message_box
from manager.components_manager import Manager
from umbra.preferences import Preferences
from umbra.processing import Processing
from umbra.ui.widgets.application_QToolBar import Application_QToolBar
from umbra.ui.widgets.delayed_QSplashScreen import Delayed_QSplashScreen

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
           "SESSION_HEADER_TEXT",
           "SESSION_FOOTER_TEXT",
           "show_processing",
           "encapsulate_processing",
           "Umbra",
           "set_user_application_data_directory",
           "get_command_line_parameters_parser",
           "get_logging_file",
           "run",
           "exit"]

LOGGER = foundations.verbose.install_logger()

def _initialize_logging():
    """
    Initializes the Application logging.
    """

    # Starting the console handler if a terminal is available.
    if sys.stdout.isatty() or platform.system() in ("Darwin", "Linux"):
        RuntimeGlobals.logging_console_handler = foundations.verbose.get_logging_console_handler()

    # Defining logging formatters.
    RuntimeGlobals.logging_formatters = {"Default": foundations.verbose.LOGGING_DEFAULT_FORMATTER,
                                        "Extended": foundations.verbose.LOGGING_EXTENDED_FORMATTER,
                                        "Standard": foundations.verbose.LOGGING_STANDARD_FORMATTER}

_initialize_logging()

def _initialize_application():
    """
    Initializes the Application.
    """

    RuntimeGlobals.application = umbra.ui.common.get_application_instance()
    umbra.ui.common.set_window_default_icon(RuntimeGlobals.application)

    RuntimeGlobals.reporter = umbra.reporter.install_exception_reporter()

_initialize_application()

@umbra.reporter.critical_exception_handler
def _initialize_applicationUiFile():
    """
    Initializes the Application ui file.
    """

    RuntimeGlobals.ui_file = umbra.ui.common.get_resource_path(UiConstants.ui_file)
    if not foundations.common.path_exists(RuntimeGlobals.ui_file):
        raise foundations.exceptions.FileExistsError("'{0}' ui file is not available, {1} will now close!".format(
            UiConstants.ui_file, Constants.application_name))

_initialize_applicationUiFile()

SESSION_HEADER_TEXT = ("{0} | Copyright ( C ) 2008 - 2014 Thomas Mansencal - thomas.mansencal@gmail.com".format(
    Constants.application_name),
                       "{0} | This software is released under terms of GNU GPL V3 license.".format(
                           Constants.application_name),
                       "{0} | http://www.gnu.org/licenses/ ".format(Constants.application_name),
                       "{0} | Version: {1}".format(Constants.application_name, Constants.version))

SESSION_FOOTER_TEXT = ("{0} | Closing interface! ".format(Constants.application_name),
                       Constants.logging_separators,
                       "{0} | Session ended at: {1}".format(Constants.application_name, time.strftime('%X - %x')),
                       Constants.logging_separators)

def show_processing(message=""):
    """
    Shows processing behavior.

    :param message: Operation description.
    :type message: unicode
    :return: Object.
    :rtype: object
    """

    def show_processingDecorator(object):
        """
        Shows processing behavior.

        :param object: Object to decorate.
        :type object: object
        :return: Object.
        :rtype: object
        """

        @functools.wraps(object)
        def show_processingWrapper(*args, **kwargs):
            """
            Shows processing behavior.

            :param \*args: Arguments.
            :type \*args: \*
            :param \*\*kwargs: Keywords arguments.
            :type \*\*kwargs: \*\*
            """

            RuntimeGlobals.engine.start_processing(message, warning=False)
            try:
                return object(*args, **kwargs)
            finally:
                RuntimeGlobals.engine.stop_processing(warning=False)

        return show_processingWrapper

    return show_processingDecorator

def encapsulate_processing(object):
    """
    Encapsulates a processing operation.

    :param object: Object to decorate.
    :type object: object
    :return: Object.
    :rtype: object
    """

    @functools.wraps(object)
    def encapsulate_processing_wrapper(*args, **kwargs):
        """
        Encapsulates a processing operation.

        :param \*args: Arguments.
        :type \*args: \*
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        RuntimeGlobals.engine._Umbra__store_processing_state()
        RuntimeGlobals.engine.stop_processing(warning=False)
        try:
            return object(*args, **kwargs)
        finally:
            RuntimeGlobals.engine.stop_processing(warning=False)
            RuntimeGlobals.engine._Umbra__restore_processing_state()

    return encapsulate_processing_wrapper

class Umbra(foundations.ui.common.QWidget_factory(ui_file=RuntimeGlobals.ui_file)):
    """
    Defines the main class of the **Umbra** package.
    """

    # Custom signals definitions.
    verbosity_level_changed = pyqtSignal(int)
    """
    This signal is emited by the :class:`Umbra` class when the current verbosity level has changed.

    :return: Current verbosity level.
    :rtype: int
    """

    content_dropped = pyqtSignal(QEvent)
    """
    This signal is emited by the :class:`Umbra` class when it receives dropped content.

    :return: Event.
    :rtype: QEvent
    """

    size_changed = pyqtSignal(QEvent)
    """
    This signal is emited by the :class:`Umbra` class when its size changes.

    :return: Event.
    :rtype: QEvent
    """

    def __new__(cls, *args, **kwargs):
        """
        Constructor of the class.

        :param \*args: Arguments.
        :type \*args: \*
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        :return: Class instance.
        :rtype: Umbra
        """

        RuntimeGlobals.engine = super(Umbra, cls).__new__(cls)
        return RuntimeGlobals.engine

    @umbra.reporter.critical_exception_handler
    def __init__(self,
                 parent=None,
                 *args,
                 **kwargs):
        """
        Initializes the class.

        :param parent: QWidget parent.
        :type parent: QWidget
        :param \*args: Arguments.
        :type \*args: \*
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        # --- Running pre initialisation method. ---
        hasattr(self, "on_pre_initialisation") and self.on_pre_initialisation()

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        settings = foundations.data_structures.Structure(**{"components_paths": None,
                                                           "requisite_components": None,
                                                           "visible_components": None,
                                                           "splashscreen": None,
                                                           "requests_stack": None,
                                                           "patches_manager": None,
                                                           "user_application_data_directory": None,
                                                           "logging_session_handler": None,
                                                           "logging_file_handler": None,
                                                           "logging_console_handler": None,
                                                           "logging_session_handler_stream": None,
                                                           "logging_active_formatter": None,
                                                           "settings": None,
                                                           "verbosity_level": None,
                                                           "parameters": None,
                                                           "arguments": None})

        settings.update(dict((key, value) for key, value in kwargs.iteritems() if key in settings))

        super(Umbra, self).__init__(parent,
                                    *args,
                                    **dict((key, value) for key, value in kwargs.iteritems() if key not in settings))

        # --- Running initialisation method. ---
        hasattr(self, "on_initialisation") and self.on_initialisation()

        # --- Setting class attributes. ---
        self.__components_paths = settings.components_paths or []
        self.__requisite_components = settings.requisite_components or []
        self.__visible_components = settings.visible_components or []

        self.__splashscreen = settings.splashscreen

        self.__timer = None
        self.__requests_stack = settings.requests_stack
        self.__patches_manager = settings.patches_manager
        self.__components_manager = None
        self.__actions_manager = None
        self.__file_system_events_manager = None
        self.__notifications_manager = None
        self.__layouts_manager = None
        self.__user_application_data_directory = settings.user_application_data_directory
        self.__logging_session_handler = settings.logging_session_handler
        self.__logging_file_handler = settings.logging_file_handler
        self.__logging_console_handler = settings.logging_console_handler
        self.__logging_session_handler_stream = settings.logging_session_handler_stream
        self.__logging_active_formatter = settings.logging_active_formatter
        self.__verbosity_level = settings.verbosity_level
        self.__settings = settings.settings
        self.__parameters = settings.parameters
        self.__arguments = settings.arguments
        self.__worker_threads = []
        self.__is_processing = False
        self.__locals = {}

        self.__processing_state = None

        # --- Initializing Application timer. ---
        self.__timer = QTimer(self)
        self.__timer.start(Constants.default_timer_cycle)

        # --- Initializing Application. ---
        self.__splashscreen and self.__splashscreen.show_message(
            "{0} - {1} | Initializing interface.".format(self.__class__.__name__, Constants.version),
            wait_time=0.25)

        # --- Initializing the Actions Manager. ---
        self.__actions_manager = RuntimeGlobals.actions_manager = umbra.managers.actions_manager.ActionsManager(self)

        # --- Initializing the File System Events Manager. ---
        self.__file_system_events_manager = RuntimeGlobals.file_system_events_manager = \
            umbra.managers.file_system_events_manager.FileSystemEventsManager(self)
        self.__worker_threads.append(self.__file_system_events_manager)
        if not self.__parameters.deactivate_worker_threads:
            self.__file_system_events_manager.start()
        else:
            LOGGER.info("{0} | File system events ignored by '{1}' command line parameter value!".format(
                self.__class__.__name__, "deactivate_worker_threads"))

        # --- Initializing the Notifications Manager. ---
        self.__notifications_manager = RuntimeGlobals.notifications_manager = \
            umbra.managers.notifications_manager.NotificationsManager(self)

        # --- Initializing the Layouts Manager. ---
        self.__layouts_manager = RuntimeGlobals.layouts_manager = umbra.managers.layouts_manager.LayoutsManager(self)

        # Visual style initialization.
        self.set_visual_style()
        umbra.ui.common.set_window_default_icon(self)

        # Various ui initializations.
        self.setAcceptDrops(True)

        # Setting window title and toolBar and statusBar.
        self.setWindowTitle("{0} - {1}".format(Constants.application_name, Constants.version))
        self.toolBar = Application_QToolBar(self)
        self.addToolBar(self.toolBar)

        # Setting processing widget.
        self.Application_Progress_Status_processing = Processing(self, Qt.Window)
        self.statusBar.addPermanentWidget(self.Application_Progress_Status_processing)
        self.Application_Progress_Status_processing.hide()

        # --- Initializing the Components Manager. ---
        self.__splashscreen and self.__splashscreen.show_message(
            "{0} - {1} | Initializing Components manager.".format(self.__class__.__name__, Constants.version),
            wait_time=0.25)

        self.__components_manager = RuntimeGlobals.components_manager = Manager(settings.components_paths)
        self.__components_manager.register_components()

        if not self.__components_manager.components:
            self.notifications_manager.warnify("{0} | '{1}' Components Manager has no Components!".format(
                self.__class__.__name__, Constants.application_name))

        self.__components_manager.instantiate_components(self.__components_instantiation_callback)

        # --- Activating requisite Components. ---
        self.__set_components(requisite=True)

        # --- Activating others Components. ---
        self.__set_components(requisite=False)

        # --- Initializing requests_stack. ---
        self.__set_locals()
        # Signals / Slots.
        self.__timer.timeout.connect(self.__process_requests_stack)

        # Hiding splashscreen.
        LOGGER.debug("> Hiding splashscreen.")
        if self.__splashscreen:
            self.__splashscreen.show_message("{0} - {1} | Initialization done.".format(
                self.__class__.__name__, Constants.version))
            self.__splashscreen.hide()

        # --- Running on_startup components methods. ---
        for component in self.__components_manager.list_components():
            try:
                interface = self.__components_manager.get_interface(component)
                if not interface:
                    continue

                if interface.activated:
                    hasattr(interface, "on_startup") and interface.on_startup()
            except Exception as error:
                umbra.reporter.base_exception_handler(umbra.exceptions.EngineInitializationError(
                    "'{0}' Component 'on_startup' method raised an exception, unexpected behavior may occur!\n Exception raised: {1}".format(
                        component, error)))

        self.__layouts_manager.restore_startup_layout()

        # --- Running post initialisation method. ---
        hasattr(self, "on_post_initialisation") and self.on_post_initialisation()

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
    def requests_stack(self):
        """
        Property for **self.__requests_stack** attribute.

        :return: self.__requests_stack. ( collections.deque )
        """

        return self.__requests_stack

    @requests_stack.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def requests_stack(self, value):
        """
        Setter for **self.__requests_stack** attribute.

        :param value: Attribute value. ( collections.deque )
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "requests_stack"))

    @requests_stack.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def requests_stack(self):
        """
        Deleter for **self.__requests_stack** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "requests_stack"))

    @property
    def components_paths(self):
        """
        Property for **self.__components_paths** attribute.

        :return: self.__components_paths.
        :rtype: tuple or list
        """

        return self.__components_paths

    @components_paths.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def components_paths(self, value):
        """
        Setter for **self.__components_paths** attribute.

        :param value: Attribute value.
        :type value: tuple or list
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "components_paths"))

    @components_paths.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def components_paths(self):
        """
        Deleter for **self.__components_paths** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "components_paths"))

    @property
    def requisite_components(self):
        """
        Property for **self.__requisite_components** attribute.

        :return: self.__requisite_components.
        :rtype: tuple or list
        """

        return self.__requisite_components

    @requisite_components.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def requisite_components(self, value):
        """
        Setter for **self.__requisite_components** attribute.

        :param value: Attribute value.
        :type value: tuple or list
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "requisite_components"))

    @requisite_components.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def requisite_components(self):
        """
        Deleter for **self.__requisite_components** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "requisite_components"))

    @property
    def visible_components(self):
        """
        Property for **self.__visible_components** attribute.

        :return: self.__visible_components.
        :rtype: tuple or list
        """

        return self.__visible_components

    @visible_components.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def visible_components(self, value):
        """
        Setter for **self.__visible_components** attribute.

        :param value: Attribute value.
        :type value: tuple or list
        """

        if value is not None:
            assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
                "visible_components", value)
            for element in value:
                assert type(element) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
                    "visible_components", element)
        self.__visible_components = value

    @visible_components.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def visible_components(self):
        """
        Deleter for **self.__visible_components** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "visible_components"))

    @property
    def splashscreen(self):
        """
        Property for **self.__splashscreen** attribute.

        :return: self.__splashscreen.
        :rtype: Delayed_QSplashScreen
        """

        return self.__splashscreen

    @splashscreen.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def splashscreen(self, value):
        """
        Setter for **self.__splashscreen** attribute.

        :param value: Attribute value.
        :type value: Delayed_QSplashScreen
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "splashscreen"))

    @splashscreen.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def splashscreen(self):
        """
        Deleter for **self.__splashscreen** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "splashscreen"))

    @property
    def patches_manager(self):
        """
        Property for **self.__patches_manager** attribute.

        :return: self.__patches_manager.
        :rtype: PatchesManager
        """

        return self.__patches_manager

    @patches_manager.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def patches_manager(self, value):
        """
        Setter for **self.__patches_manager** attribute.

        :param value: Attribute value.
        :type value: PatchesManager
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "patches_manager"))

    @patches_manager.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def patches_manager(self):
        """
        Deleter for **self.__patches_manager** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "patches_manager"))

    @property
    def components_manager(self):
        """
        Property for **self.__components_manager** attribute.

        :return: self.__components_manager.
        :rtype: ComponentsManager
        """

        return self.__components_manager

    @components_manager.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def components_manager(self, value):
        """
        Setter for **self.__components_manager** attribute.

        :param value: Attribute value.
        :type value: ComponentsManager
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "components_manager"))

    @components_manager.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def components_manager(self):
        """
        Deleter for **self.__components_manager** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "components_manager"))

    @property
    def notifications_manager(self):
        """
        Property for **self.__notifications_manager** attribute.

        :return: self.__notifications_manager.
        :rtype: NotificationsManager
        """

        return self.__notifications_manager

    @notifications_manager.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def notifications_manager(self, value):
        """
        Setter for **self.__notifications_manager** attribute.

        :param value: Attribute value.
        :type value: NotificationsManager
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "notifications_manager"))

    @notifications_manager.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def notifications_manager(self):
        """
        Deleter for **self.__notifications_manager** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "notifications_manager"))

    @property
    def actions_manager(self):
        """
        Property for **self.__actions_manager** attribute.

        :return: self.__actions_manager.
        :rtype: ActionsManager
        """

        return self.__actions_manager

    @actions_manager.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def actions_manager(self, value):
        """
        Setter for **self.__actions_manager** attribute.

        :param value: Attribute value.
        :type value: ActionsManager
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "actions_manager"))

    @actions_manager.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def actions_manager(self):
        """
        Deleter for **self.__actions_manager** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "actions_manager"))

    @property
    def file_system_events_manager(self):
        """
        Property for **self.__file_system_events_manager** attribute.

        :return: self.__file_system_events_manager.
        :rtype: FileSystemEventsManager
        """

        return self.__file_system_events_manager

    @file_system_events_manager.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def file_system_events_manager(self, value):
        """
        Setter for **self.__file_system_events_manager** attribute.

        :param value: Attribute value.
        :type value: FileSystemEventsManager
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "file_system_events_manager"))

    @file_system_events_manager.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def file_system_events_manager(self):
        """
        Deleter for **self.__file_system_events_manager** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "file_system_events_manager"))

    @property
    def layouts_manager(self):
        """
        Property for **self.__layouts_manager** attribute.

        :return: self.__layouts_manager.
        :rtype: LayoutsManager
        """

        return self.__layouts_manager

    @layouts_manager.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def layouts_manager(self, value):
        """
        Setter for **self.__layouts_manager** attribute.

        :param value: Attribute value.
        :type value: LayoutsManager
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "layouts_manager"))

    @layouts_manager.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def layouts_manager(self):
        """
        Deleter for **self.__layouts_manager** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "layouts_manager"))

    @property
    def user_application_data_directory(self):
        """
        Property for **self.__user_application_data_directory** attribute.

        :return: self.__user_application_data_directory.
        :rtype: unicode
        """

        return self.__user_application_data_directory

    @user_application_data_directory.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def user_application_data_directory(self, value):
        """
        Setter for **self.__user_application_data_directory** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "user_application_data_directory"))

    @user_application_data_directory.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def user_application_data_directory(self):
        """
        Deleter for **self.__user_application_data_directory** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "user_application_data_directory"))

    @property
    def logging_session_handler(self):
        """
        Property for **self.__logging_session_handler** attribute.

        :return: self.__logging_session_handler.
        :rtype: Handler
        """

        return self.__logging_session_handler

    @logging_session_handler.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def logging_session_handler(self, value):
        """
        Setter for **self.__logging_session_handler** attribute.

        :param value: Attribute value.
        :type value: Handler
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "logging_session_handler"))

    @logging_session_handler.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def logging_session_handler(self):
        """
        Deleter for **self.__logging_session_handler** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "logging_session_handler"))

    @property
    def logging_file_handler(self):
        """
        Property for **self.__logging_file_handler** attribute.

        :return: self.__logging_file_handler.
        :rtype: Handler
        """

        return self.__logging_file_handler

    @logging_file_handler.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def logging_file_handler(self, value):
        """
        Setter for **self.__logging_file_handler** attribute.

        :param value: Attribute value.
        :type value: Handler
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "logging_file_handler"))

    @logging_file_handler.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def logging_file_handler(self):
        """
        Deleter for **self.__logging_file_handler** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "logging_file_handler"))

    @property
    def logging_console_handler(self):
        """
        Property for **self.__logging_console_handler** attribute.

        :return: self.__logging_console_handler.
        :rtype: Handler
        """

        return self.__logging_console_handler

    @logging_console_handler.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def logging_console_handler(self, value):
        """
        Setter for **self.__logging_console_handler** attribute.

        :param value: Attribute value.
        :type value: Handler
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "logging_console_handler"))

    @logging_console_handler.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def logging_console_handler(self):
        """
        Deleter for **self.__logging_console_handler** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "logging_console_handler"))

    @property
    @foundations.trace.untracable
    def logging_session_handler_stream(self):
        """
        Property for **self.__logging_session_handler_stream** attribute.

        :return: self.__logging_session_handler_stream.
        :rtype: StreamObject
        """

        return self.__logging_session_handler_stream

    @logging_session_handler_stream.setter
    @foundations.trace.untracable
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def logging_session_handler_stream(self, value):
        """
        Setter for **self.__logging_session_handler_stream** attribute.

        :param value: Attribute value.
        :type value: StreamObject
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "logging_session_handler_stream"))

    @logging_session_handler_stream.deleter
    @foundations.trace.untracable
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def logging_session_handler_stream(self):
        """
        Deleter for **self.__logging_session_handler_stream** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "logging_session_handler_stream"))

    @property
    def logging_active_formatter(self):
        """
        Property for **self.__logging_active_formatter** attribute.

        :return: self.__logging_active_formatter.
        :rtype: Formatter
        """

        return self.__logging_active_formatter

    @logging_active_formatter.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def logging_active_formatter(self, value):
        """
        Setter for **self.__logging_active_formatter** attribute.

        :param value: Attribute value.
        :type value: unicode or QString
        """

        if value is not None:
            assert type(value) in (
            unicode, QString), "'{0}' attribute: '{1}' type is not 'unicode' or 'QString'!".format(
                "logging_active_formatter", value)
        self.__logging_active_formatter = value

    @logging_active_formatter.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def logging_active_formatter(self):
        """
        Deleter for **self.__logging_active_formatter** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "logging_active_formatter"))

    @property
    def verbosity_level(self):
        """
        Property for **self.__verbosity_level** attribute.

        :return: self.__verbosity_level.
        :rtype: int
        """

        return self.__verbosity_level

    @verbosity_level.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def verbosity_level(self, value):
        """
        Setter for **self.__verbosity_level** attribute.

        :param value: Attribute value.
        :type value: int
        """

        if value is not None:
            assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("verbosity_level", value)
            assert value >= 0 and value <= 4, "'{0}' attribute: Value need to be exactly beetween 0 and 4!".format(
                "verbosity_level")
        self.__verbosity_level = value

    @verbosity_level.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def verbosity_level(self):
        """
        Deleter for **self.__verbosity_level** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "verbosity_level"))

    @property
    def settings(self):
        """
        Property for **self.__settings** attribute.

        :return: self.__settings.
        :rtype: Preferences
        """

        return self.__settings

    @settings.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def settings(self, value):
        """
        Setter for **self.__settings** attribute.

        :param value: Attribute value.
        :type value: Preferences
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

    @settings.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def settings(self):
        """
        Deleter for **self.__settings** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

    @property
    def parameters(self):
        """
        Property for **self.__parameters** attribute.

        :return: self.__parameters.
        :rtype: object
        """

        return self.__parameters

    @parameters.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def parameters(self, value):
        """
        Setter for **self.__parameters** attribute.

        :param value: Attribute value.
        :type value: object
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "parameters"))

    @parameters.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def parameters(self):
        """
        Deleter for **self.__parameters** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "parameters"))

    @property
    def arguments(self):
        """
        Property for **self.__arguments** attribute.

        :return: self.__arguments.
        :rtype: list
        """

        return self.__arguments

    @arguments.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def arguments(self, value):
        """
        Setter for **self.__arguments** attribute.

        :param value: Attribute value.
        :type value: list
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "arguments"))

    @arguments.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def arguments(self):
        """
        Deleter for **self.__arguments** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "arguments"))

    @property
    def worker_threads(self):
        """
        Property for **self.__worker_threads** attribute.

        :return: self.__worker_threads.
        :rtype: list
        """

        return self.__worker_threads

    @worker_threads.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def worker_threads(self, value):
        """
        Setter for **self.__worker_threads** attribute.

        :param value: Attribute value.
        :type value: list
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "worker_threads"))

    @worker_threads.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def worker_threads(self):
        """
        Deleter for **self.__worker_threads** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "worker_threads"))

    @property
    def is_processing(self):
        """
        Property for **self.__is_processing** attribute.

        :return: self.__is_processing.
        :rtype: bool
        """

        return self.__is_processing

    @is_processing.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def is_processing(self, value):
        """
        Setter for **self.__is_processing** attribute.

        :param value: Attribute value.
        :type value: bool
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "is_processing"))

    @is_processing.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def is_processing(self):
        """
        Deleter for **self.__is_processing** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "is_processing"))

    @property
    def locals(self):
        """
        Property for **self.__locals** attribute.

        :return: self.__locals.
        :rtype: dict
        """

        return self.__locals

    @locals.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def locals(self, value):
        """
        Setter for **self.__locals** attribute.

        :param value: Attribute value.
        :type value: dict
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "locals"))

    @locals.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def locals(self):
        """
        Deleter for **self.__locals** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "locals"))

    def dragEnterEvent(self, event):
        """
        Reimplements the :meth:`QWidget.dragEnterEvent` method.

        :param event: QEvent.
        :type event: QEvent
        """

        LOGGER.debug("> Application drag enter event accepted!")
        event.accept()

    def dragMoveEvent(self, event):
        """
        Reimplements the :meth:`QWidget.dragMoveEvent` method.

        :param event: QEvent.
        :type event: QEvent
        """

        LOGGER.debug("> Application drag move event accepted!")
        event.accept()

    def dropEvent(self, event):
        """
        Reimplements the :meth:`QWidget.dropEvent` method.

        :param event: QEvent.
        :type event: QEvent
        """

        LOGGER.debug("> Application drop event accepted!")
        self.content_dropped.emit(event)

    def show(self):
        """
        Reimplements the :meth:`QWidget.show` method.
        """

        super(Umbra, self).show(setGeometry=False)

    def closeEvent(self, event):
        """
        Reimplements the :meth:`QWidget.closeEvent` method.

        :param event: QEvent.
        :type event: QEvent
        """

        self.quit(event=event)

    def resizeEvent(self, event):
        """
        Reimplements the :meth:`QWidget.resizeEvent` method.

        :param event: QEvent.
        :type event: QEvent
        """

        LOGGER.debug("> Application resize event accepted!")
        self.size_changed.emit(event)
        event.accept()

    def __set_components(self, requisite=True):
        """
        Sets the Components.

        :param requisite: Set only requisite Components.
        :type requisite: bool
        """

        components = self.__components_manager.list_components()
        candidate_components = \
            getattr(set(components), "intersection" if requisite else "difference")(self.__requisite_components)
        deactivated_components = self.__settings.get_key("Settings", "deactivated_components").toString().split(",")
        candidate_components = \
            sorted(filter(lambda x: x not in deactivated_components, candidate_components), key=(components).index)

        for component in candidate_components:
            try:
                profile = self.__components_manager.components[component]
                interface = self.__components_manager.get_interface(component)

                setattr(self,
                        "_{0}__{1}".format(self.__class__.__name__, foundations.namespace.get_leaf(component, ".")),
                        interface)

                self.__splashscreen and self.__splashscreen.show_message(
                    "{0} - {1} | Activating {2}.".format(self.__class__.__name__, Constants.version, component))
                interface.activate(self)
                if profile.category in ("Default", "QObject"):
                    interface.initialize()
                elif profile.category == "QWidget":
                    interface.add_widget()
                    interface.initialize_ui()
            except Exception as error:
                if requisite:
                    message = "'{0}' Component failed to activate!\nException raised: {1}"
                    handler = umbra.reporter.system_exit_exception_handler
                else:
                    message = "'{0}' Component failed to activate, unexpected behavior may occur!\nException raised: {1}"
                    handler = umbra.reporter.base_exception_handler

                exception = manager.exceptions.ComponentActivationError(message.format(component, error))
                handler(exception)

    def __set_locals(self):
        """
        Sets the locals for the requests_stack.
        """

        for globals in (Constants, RuntimeGlobals, UiConstants):
            self.__locals[globals.__name__] = globals

        self.__locals[Constants.application_name] = self
        self.__locals["application"] = self
        self.__locals["patches_manager"] = self.__patches_manager
        self.__locals["components_manager"] = self.__components_manager
        self.__locals["actions_manager"] = self.__actions_manager
        self.__locals["file_system_events_manager"] = self.__file_system_events_manager
        self.__locals["notifications_manager"] = self.__notifications_manager
        self.__locals["layouts_manager"] = self.__layouts_manager
        self.__locals["LOGGER"] = LOGGER

        LOGGER.debug("> Defined locals: '{0}'.".format(self.__locals))

    def __process_requests_stack(self):
        """
        Process the requests stack.
        """

        while self.__requests_stack:
            try:
                exec self.__requests_stack.popleft() in self.__locals
            except Exception as error:
                umbra.exceptions.notify_exception_handler(error)

    def __components_instantiation_callback(self, profile):
        """
        Defines a callback for Components instantiation.

        :param profile: Component Profile.
        :type profile: Profile
        """

        self.__splashscreen and self.__splashscreen.show_message(
            "{0} - {1} | Instantiating {2} Component.".format(self.__class__.__name__, Constants.version,
                                                              profile.name))

    def __store_processing_state(self):
        """
        Stores the processing state.
        """

        steps = self.Application_Progress_Status_processing.Processing_progressBar.maximum()
        value = self.Application_Progress_Status_processing.Processing_progressBar.value()
        message = self.Application_Progress_Status_processing.Processing_label.text()
        state = self.__is_processing

        self.__processing_state = steps, value, message, state

    def __restore_processing_state(self):
        """
        Restores the processing state.
        """

        steps, value, message, state = self.__processing_state

        self.Application_Progress_Status_processing.Processing_progressBar.setRange(0, steps)
        self.Application_Progress_Status_processing.Processing_progressBar.setValue(value)
        self.set_processing_message(message, warning=False)
        self.__is_processing = state
        state and self.Application_Progress_Status_processing.show()

    def set_verbosity_level(self, verbosity_level):
        """
        Sets the Application verbosity level.

        :param verbosity_level: Verbosity level.
        :type verbosity_level: int
        :return: Method success.
        :rtype: bool

        :note: The expected verbosity level value is an integer between 0 to 4.
        """

        self.__verbosity_level = verbosity_level
        foundations.verbose.set_verbosity_level(verbosity_level)
        self.__settings.set_key("Settings", "verbosity_level", verbosity_level)
        self.verbosity_level_changed.emit(verbosity_level)
        return True

    @foundations.exceptions.handle_exceptions(foundations.exceptions.FileExistsError)
    def set_visual_style(self, full_screen_style=False):
        """
        Sets the Application visual style.

        :param full_screen_style: Use fullscreen stylesheet file.
        :type full_screen_style: bool
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Setting Application visual style.")
        platform_styles = {"Windows": (("Windows", "Microsoft"),
                                      UiConstants.windows_style,
                                      UiConstants.windows_stylesheet_file,
                                      UiConstants.windows_full_screen_stylesheet_file),
                          "Darwin": (("Darwin",),
                                     UiConstants.darwin_style,
                                     UiConstants.darwin_stylesheet_file,
                                     UiConstants.darwin_full_screen_stylesheet_file),
                          "Linux": (("Linux",),
                                    UiConstants.linux_style,
                                    UiConstants.linux_stylesheet_file,
                                    UiConstants.linux_full_screen_stylesheet_file)}

        style_sheet_file = None
        for platform_style, settings in platform_styles.iteritems():
            LOGGER.debug("> Setting '{0}' visual style.".format(platform_style))
            platform_systems, style, styleSheeFile, full_screen_style_sheet_file = settings
            if platform.system() in platform_systems:
                RuntimeGlobals.application.setStyle(style)
                style_sheet_path = umbra.ui.common.get_resource_path(styleSheeFile)
                if full_screen_style:
                    full_screen_style_sheet_path = umbra.ui.common.get_resource_path(full_screen_style_sheet_file,
                                                                               raise_exception=False)
                    style_sheet_path = full_screen_style_sheet_path or style_sheet_path
                style_sheet_file = foundations.io.File(style_sheet_path)
                break

        if not style_sheet_file:
            raise foundations.exceptions.FileExistsError(
                "{0} | No stylesheet file found, visual style will not be applied!".format(self.__class__.__name__))

        if foundations.common.path_exists(style_sheet_file.path):
            LOGGER.debug("> Reading style sheet file: '{0}'.".format(style_sheet_file.path))
            style_sheet_file.cache()
            for i, line in enumerate(style_sheet_file.content):
                search = re.search(r"url\((?P<url>.*)\)", line)
                if not search:
                    continue

                style_sheet_file.content[i] = line.replace(search.group("url"),
                                                         foundations.strings.to_forward_slashes(
                                                             umbra.ui.common.get_resource_path(search.group("url"))))
            RuntimeGlobals.application.setStyleSheet(QString("".join(style_sheet_file.content)))
            return True
        else:
            raise foundations.exceptions.FileExistsError(
                "{0} | '{1}' stylesheet file is not available, visual style will not be applied!".format(
                    self.__class__.__name__, style_sheet_file.path))

    def is_full_screen(self):
        """
        Returns if Application is in fullscreen state.

        :return: FullScreen state.
        :rtype: bool
        """

        return True if self.windowState().__int__() == 4 else False

    def toggle_full_screen(self, *args):
        """
        Toggles Application fullscreen state.

        :param \*args: Arguments.
        :type \*args: \*
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Toggling FullScreen state.")

        if self.is_full_screen():
            self.setUnifiedTitleAndToolBarOnMac(True)
            self.set_visual_style(full_screen_style=False)
            self.showNormal()
            # TODO: Remove hack that ensure toolBar is repainted.
            platform.system() == "Darwin" and self.resize(self.size().width() + 1, self.size().height() + 1)
        else:
            self.setUnifiedTitleAndToolBarOnMac(False)
            self.set_visual_style(full_screen_style=True)
            self.showFullScreen()
        return True

    def process_events(self, flags=QEventLoop.AllEvents):
        """
        Process Application events.

        :param flags: Events flags.
        :type flags: int
        :return: Method success.
        :rtype: bool
        """

        QApplication.processEvents(flags)
        return True

    def set_processing_message(self, message, warning=True):
        """
        Sets the processing operation message.

        :param message: Operation description.
        :type message: unicode
        :param warning: Emit warning message.
        :type warning: int
        :return: Method success.
        :rtype: bool
        """

        if not self.__is_processing:
            warning and LOGGER.warning(
                "!> {0} | Engine not processing, 'set_processing_message' request has been ignored!".format(
                    self.__class__.__name__))
            return False

        LOGGER.debug("> Setting processing message!")

        self.Application_Progress_Status_processing.Processing_label.setText(message)
        self.process_events()
        return True

    def start_processing(self, message, steps=0, warning=True):
        """
        Registers the start of a processing operation.

        :param message: Operation description.
        :type message: unicode
        :param steps: Operation steps.
        :type steps: int
        :param warning: Emit warning message.
        :type warning: int
        :return: Method success.
        :rtype: bool
        """

        if self.__is_processing:
            warning and LOGGER.warning(
                "!> {0} | Engine is already processing, 'start_processing' request has been ignored!".format(
                    self.__class__.__name__))
            return False

        LOGGER.debug("> Starting processing operation!")

        self.__is_processing = True
        self.Application_Progress_Status_processing.Processing_progressBar.setRange(0, steps)
        self.Application_Progress_Status_processing.Processing_progressBar.setValue(0)
        self.Application_Progress_Status_processing.show()
        self.set_processing_message(message)
        return True

    def step_processing(self, warning=True):
        """
        Steps the processing operation progress indicator.

        :param warning: Emit warning message.
        :type warning: int
        :return: Method success.
        :rtype: bool
        """

        if not self.__is_processing:
            warning and LOGGER.warning(
                "!> {0} | Engine is not processing, 'step_processing' request has been ignored!".format(
                    self.__class__.__name__))
            return False

        LOGGER.debug("> Stepping processing operation!")

        self.Application_Progress_Status_processing.Processing_progressBar.setValue(
            self.Application_Progress_Status_processing.Processing_progressBar.value() + 1)
        self.process_events()
        return True

    def stop_processing(self, warning=True):
        """
        Registers the end of a processing operation.

        :param warning: Emit warning message.
        :type warning: int
        :return: Method success.
        :rtype: bool
        """

        if not self.__is_processing:
            warning and LOGGER.warning(
                "!> {0} | Engine is not processing, 'stop_processing' request has been ignored!".format(
                    self.__class__.__name__))
            return False

        LOGGER.debug("> Stopping processing operation!")

        self.__is_processing = False
        self.Application_Progress_Status_processing.Processing_label.setText(QString())
        self.Application_Progress_Status_processing.Processing_progressBar.setRange(0, 100)
        self.Application_Progress_Status_processing.Processing_progressBar.setValue(0)
        self.Application_Progress_Status_processing.hide()
        return True

    def garbage_collect(self):
        """
        Triggers the garbage collecting.

        :return: Number of unreachable objects found.
        :rtype: int
        """

        LOGGER.debug("> Garbage collecting!")

        return gc.collect()

    def quit(self, exit_code=0, event=None):
        """
        Quits the Application.

        :param exit_code: Exit code.
        :type exit_code: int
        :param event: QEvent.
        :type event: QEvent
        """

        # --- Running on_close components methods. ---
        for component in reversed(self.__components_manager.list_components()):
            interface = self.__components_manager.get_interface(component)
            if not interface:
                continue

            if not interface.activated:
                continue

            if not hasattr(interface, "on_close"):
                continue

            if not interface.on_close():
                event and event.ignore()
                return

        # Storing current layout.
        self.__layouts_manager.store_startup_layout()
        self.__settings.settings.sync()

        # Stopping worker threads.
        for worker_thread in self.__worker_threads:
            LOGGER.debug("> Stopping worker thread: '{0}'.".format(worker_thread))
            if not worker_thread.isFinished():
                worker_thread.quit()
            worker_thread.wait()

        foundations.verbose.remove_logging_handler(self.__logging_file_handler)
        foundations.verbose.remove_logging_handler(self.__logging_session_handler)
        # foundations.verbose.remove_logging_handler(self.__logging_console_handler)

        # Stopping the Application timer.
        self.__timer.stop()
        self.__timer = None

        self.deleteLater()
        event and event.accept()

        exit(exit_code)

@umbra.reporter.critical_exception_handler
def set_user_application_data_directory(directory):
    """
    Sets the user Application data directory.

    :param directory: Starting point for the directories tree creation.
    :type directory: unicode
    :return: Definition success.
    :rtype: bool
    """

    LOGGER.debug("> Current Application data directory '{0}'.".format(directory))
    if foundations.io.set_directory(directory):
        for sub_directory in Constants.preferences_directories:
            if not foundations.io.set_directory(os.path.join(directory, sub_directory)):
                raise OSError("{0} | '{1}' directory creation failed , '{2}' will now close!".format(
                    __name__, os.path.join(directory, sub_directory), Constants.application_name))
        return True
    else:
        raise OSError("{0} | '{1}' directory creation failed , '{2}' will now close!".format(__name__,
                                                                                             directory,
                                                                                             Constants.application_name))

def get_command_line_parameters_parser():
    """
    Returns the command line parameters parser.

    :return: Parser.
    :rtype: Parser
    """

    parser = optparse.OptionParser(formatter=optparse.IndentedHelpFormatter(indent_increment=2,
                                                                            max_help_position=8,
                                                                            width=128,
                                                                            short_first=1),
                                   add_help_option=None)

    parser.add_option("-h",
                      "--help",
                      action="help",
                      help="'Display this help message and exit.'")
    parser.add_option("-a",
                      "--about",
                      action="store_true",
                      default=False,
                      dest="about",
                      help="'Display Application about message.'")
    parser.add_option("-v",
                      "--verbose",
                      action="store",
                      type="int",
                      dest="verbosity_level",
                      help="'Application verbosity levels: 0 = Critical | 1 = Error | 2 = Warning | 3 = Info | 4 = Debug.'")
    parser.add_option("-f",
                      "--logging_formatter",
                      action="store",
                      type="string",
                      dest="logging_formatter",
                      help="'Application logging formatter: '{0}'.'".format(
                          ", ".join(sorted(RuntimeGlobals.logging_formatters))))
    parser.add_option("-u",
                      "--user_application_data_directory",
                      action="store",
                      type="string",
                      dest="user_application_data_directory",
                      help="'User Application data directory'.")
    parser.add_option("-s",
                      "--hide_splash_screen",
                      action="store_true",
                      default=False,
                      dest="hide_splash_screen",
                      help="'Hide splashscreen'.")
    parser.add_option("-w",
                      "--deactivate_worker_threads",
                      action="store_true",
                      default=False,
                      dest="deactivate_worker_threads",
                      help="'Deactivate worker threads'.")
    parser.add_option("-x",
                      "--startup_script",
                      action="store",
                      type="string",
                      dest="startup_script",
                      help="'Execute given startup script'.")
    parser.add_option("-t",
                      "--trace_modules",
                      action="store",
                      default="{}",
                      type="string",
                      dest="trace_modules",
                      help="'Trace given modules'.")
    return parser

@umbra.reporter.critical_exception_handler
def get_logging_file(maximum_logging_files=10, retries=2 ^ 16):
    """
    Returns the logging file path.

    :param maximum_logging_files: Maximum allowed logging files in the logging directory.
    :type maximum_logging_files: int
    :param retries: Number of retries to generate a unique logging file name.
    :type retries: int
    :return: Logging file path.
    :rtype: unicode
    """

    logging_directory = os.path.join(RuntimeGlobals.user_application_data_directory, Constants.logging_directory)
    for file in sorted(foundations.walkers.files_walker(logging_directory),
                       key=lambda y: os.path.getmtime(os.path.abspath(y)), reverse=True)[maximum_logging_files:]:
        try:
            os.remove(file)
        except OSError:
            LOGGER.warning(
                "!> {0} | Cannot remove '{1}' file!".format(__name__, file, Constants.application_name))

    path = None
    for i in range(retries):
        path = os.path.join(RuntimeGlobals.user_application_data_directory,
                            Constants.logging_directory,
                            Constants.logging_file.format(foundations.strings.get_random_sequence()))
        if not os.path.exists(path):
            break

    if path is None:
        raise umbra.exceptions.EngineConfigurationError(
            "{0} | Logging file is not available, '{1}' will now close!".format(__name__, Constants.application_name))

    LOGGER.debug("> Current Logging file: '{0}'".format(path))

    return path

@umbra.reporter.critical_exception_handler
def run(engine, parameters, components_paths=None, requisite_components=None, visible_components=None):
    """
    Starts the Application.

    :param engine: Engine.
    :type engine: QObject
    :param parameters: Command line parameters.
    :type parameters: tuple
    :param components_paths: Components components_paths.
    :type components_paths: tuple or list
    :param requisite_components: Requisite components names.
    :type requisite_components: tuple or list
    :param visible_components: Visible components names.
    :type visible_components: tuple or list
    :return: Definition success.
    :rtype: bool
    """

    # Command line parameters handling.
    RuntimeGlobals.parameters, RuntimeGlobals.arguments = parameters

    foundations.trace.evaluate_trace_request(RuntimeGlobals.parameters.trace_modules, foundations.verbose.tracer)

    if RuntimeGlobals.parameters.about:
        for line in SESSION_HEADER_TEXT:
            sys.stdout.write("{0}\n".format(line))
        foundations.core.exit(1)

    # Redirecting standard output and error messages.
    sys.stdout = foundations.verbose.StandardOutputStreamer(LOGGER)
    sys.stderr = foundations.verbose.StandardOutputStreamer(LOGGER)

    # Setting application verbose level.
    foundations.verbose.set_verbosity_level(4)

    # Setting user application data directory.
    if RuntimeGlobals.parameters.user_application_data_directory:
        user_application_data_directory = RuntimeGlobals.user_application_data_directory = \
            RuntimeGlobals.parameters.user_application_data_directory
    else:
        user_application_data_directory = RuntimeGlobals.user_application_data_directory = \
            foundations.environment.get_user_application_data_directory()

    if not set_user_application_data_directory(user_application_data_directory):
        raise umbra.exceptions.EngineConfigurationError(
            "{0} | '{1}' user Application data directory is not available, '{2}' will now close!".format(
                __name__, RuntimeGlobals.user_application_data_directory, Constants.application_name))

    if foundations.environment.get_temporary_directory() in user_application_data_directory:
        umbra.ui.widgets.message_box.message_box("Error",
                                               "Error",
"{0} failed to use the default user Application data directory to store its preferences \
and has defaulted to the following directory:\n\n\t'{1}'.\n\nReasons for this are various:\n\
\t- Undefined 'APPDATA' ( Windows ) or 'HOME' ( Mac Os X, Linux ) environment variables.\n\
\t- User name with non 'UTF-8' encoding compliant characters.\n\
\t- Non 'UTF-8' encoding compliant characters in the preferences directory path.\n\n\
You will have to define your own preferences directory by launching {0} with the \
'-u \"path\\to\\the\\custom\\preferences\\directory\"' command line parameter.".format(
                                                   Constants.application_name,
                                                   user_application_data_directory))

    LOGGER.debug("> Application Python interpreter: '{0}'".format(sys.executable))
    LOGGER.debug("> Application PyQt version: '{0}'".format(PYQT_VERSION_STR))
    LOGGER.debug("> Application startup location: '{0}'".format(os.getcwd()))
    LOGGER.debug("> Session user Application data directory: '{0}'".format(RuntimeGlobals.user_application_data_directory))

    LOGGER.debug("> Initializing '{0}'!".format(Constants.application_name))

    # Getting the logging file path.
    RuntimeGlobals.logging_file = get_logging_file()
    RuntimeGlobals.logging_file_handler = foundations.verbose.get_logging_file_handler(file=RuntimeGlobals.logging_file)

    # Getting the patches file path.
    RuntimeGlobals.patches_file = os.path.join(RuntimeGlobals.user_application_data_directory,
                                              Constants.patches_directory,
                                              Constants.patches_file)
    # Initializing the patches manager.
    RuntimeGlobals.patches_manager = umbra.managers.patches_manager.PatchesManager(RuntimeGlobals.patches_file,
                                                                                 [os.path.join(path,
                                                                                               Constants.patches_directory)
                                                                                  for path in
                                                                                  RuntimeGlobals.resources_directories])
    RuntimeGlobals.patches_manager.register_patches() and RuntimeGlobals.patches_manager.apply_patches()

    # Retrieving settings file.
    RuntimeGlobals.settings_file = os.path.join(RuntimeGlobals.user_application_data_directory,
                                               Constants.settings_directory,
                                               Constants.settings_file)

    RuntimeGlobals.settings = Preferences(RuntimeGlobals.settings_file)

    LOGGER.debug("> Retrieving default layouts.")
    RuntimeGlobals.settings.set_default_layouts(("startup_centric",))

    foundations.common.path_exists(RuntimeGlobals.settings_file) or RuntimeGlobals.settings.set_default_preferences()

    LOGGER.debug("> Retrieving stored verbose level.")
    RuntimeGlobals.verbosity_level = RuntimeGlobals.parameters.verbosity_level \
        if RuntimeGlobals.parameters.verbosity_level is not None else \
        foundations.common.get_first_item(RuntimeGlobals.settings.get_key("Settings", "verbosity_level").toInt())
    LOGGER.debug("> Setting logger verbosity level to: '{0}'.".format(RuntimeGlobals.verbosity_level))
    foundations.verbose.set_verbosity_level(RuntimeGlobals.verbosity_level)
    RuntimeGlobals.settings.set_key("Settings", "verbosity_level", RuntimeGlobals.verbosity_level)

    LOGGER.debug("> Retrieving stored logging formatter.")
    logging_formatter = RuntimeGlobals.parameters.logging_formatter if RuntimeGlobals.parameters.logging_formatter is not None else \
        foundations.strings.to_string(RuntimeGlobals.settings.get_key("Settings", "logging_formatter").toString())
    logging_formatter = logging_formatter if logging_formatter in RuntimeGlobals.logging_formatters else None
    RuntimeGlobals.logging_active_formatter = logging_formatter if logging_formatter is not None else Constants.logging_default_formatter
    LOGGER.debug("> Setting logging formatter: '{0}'.".format(RuntimeGlobals.logging_active_formatter))
    for handler in (RuntimeGlobals.logging_console_handler, RuntimeGlobals.logging_file_handler):
        handler and handler.setFormatter(RuntimeGlobals.logging_formatters[RuntimeGlobals.logging_active_formatter])

    # Starting the session handler.
    RuntimeGlobals.logging_session_handler = foundations.verbose.get_logging_stream_handler()
    RuntimeGlobals.logging_session_handler_stream = RuntimeGlobals.logging_session_handler.stream

    LOGGER.info(Constants.logging_separators)
    for line in SESSION_HEADER_TEXT:
        LOGGER.info(line)
    LOGGER.info("{0} | Session started at: {1}".format(Constants.application_name, time.strftime('%X - %x')))
    LOGGER.info(Constants.logging_separators)
    LOGGER.info("{0} | Starting Interface!".format(Constants.application_name))

    # Initializing splashscreen.
    if RuntimeGlobals.parameters.hide_splash_screen:
        LOGGER.debug("> SplashScreen skipped by 'hide_splash_screen' command line parameter.")
    else:
        LOGGER.debug("> Initializing splashscreen.")

        RuntimeGlobals.splashscreen_image = QPixmap(umbra.ui.common.get_resource_path(UiConstants.splash_screen_image))
        RuntimeGlobals.splashscreen = Delayed_QSplashScreen(RuntimeGlobals.splashscreen_image, text_color=Qt.white)
        RuntimeGlobals.splashscreen.show_message(
            "{0} - {1} | Initializing {0}.".format(Constants.application_name, Constants.version))
        RuntimeGlobals.splashscreen.show()

    # Initializing requests stack.
    RuntimeGlobals.requests_stack = collections.deque()

    # Initializing engine.
    RuntimeGlobals.engine = engine(parent=None,
                                   components_paths=components_paths,
                                   requisite_components=requisite_components,
                                   visible_components=visible_components,
                                   splashscreen=RuntimeGlobals.splashscreen,
                                   requests_stack=RuntimeGlobals.requests_stack,
                                   patches_manager=RuntimeGlobals.patches_manager,
                                   user_application_data_directory=RuntimeGlobals.user_application_data_directory,
                                   logging_session_handler=RuntimeGlobals.logging_session_handler,
                                   logging_file_handler=RuntimeGlobals.logging_file_handler,
                                   logging_console_handler=RuntimeGlobals.logging_console_handler,
                                   logging_session_handler_stream=RuntimeGlobals.logging_session_handler_stream,
                                   logging_active_formatter=RuntimeGlobals.logging_active_formatter,
                                   settings=RuntimeGlobals.settings,
                                   verbosity_level=RuntimeGlobals.verbosity_level,
                                   parameters=RuntimeGlobals.parameters,
                                   arguments=RuntimeGlobals.arguments)
    RuntimeGlobals.engine.show()
    RuntimeGlobals.engine.raise_()

    return sys.exit(RuntimeGlobals.application.exec_())

def exit(exit_code=0):
    """
    Exits the Application.

    :param exit_code: Exit code.
    :type exit_code: int
    """

    for line in SESSION_FOOTER_TEXT:
        LOGGER.info(line)

    foundations.verbose.remove_logging_handler(RuntimeGlobals.logging_console_handler)

    RuntimeGlobals.application.exit(exit_code)
