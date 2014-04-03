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

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
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

#**********************************************************************************************************************
#***	Path manipulations.
#**********************************************************************************************************************
def _setPackageDirectory():
	"""
	Sets the Application package directory in the path.
	"""

	packageDirectory = os.path.normpath(os.path.join(os.path.dirname(__file__), "../"))
	packageDirectory not in sys.path and sys.path.append(packageDirectory)

_setPackageDirectory()

#**********************************************************************************************************************
#***	Dependencies globals manipulation.
#**********************************************************************************************************************
import foundations.globals.constants
import manager.globals.constants
import umbra.globals.constants
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals
from umbra.globals.uiConstants import UiConstants

def _overrideDependenciesGlobals():
	"""
	Overrides dependencies globals.
	"""

	foundations.globals.constants.Constants.logger = manager.globals.constants.Constants.logger = Constants.logger
	foundations.globals.constants.Constants.applicationDirectory = \
		manager.globals.constants.Constants.applicationDirectory = Constants.applicationDirectory

_overrideDependenciesGlobals()

import foundations.common

def _extendResourcesPaths():
	"""
	Extend resources paths.
	"""

	for path in (os.path.join(umbra.__path__[0], Constants.resourcesDirectory),
				 os.path.join(os.getcwd(), umbra.__name__, Constants.resourcesDirectory)):
		path = os.path.normpath(path)
		if foundations.common.pathExists(path):
			path not in RuntimeGlobals.resourcesDirectories and RuntimeGlobals.resourcesDirectories.append(path)

_extendResourcesPaths()

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core
import foundations.dataStructures
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
import umbra.managers.actionsManager
import umbra.managers.fileSystemEventsManager
import umbra.managers.notificationsManager
import umbra.managers.patchesManager
import umbra.managers.layoutsManager
import umbra.reporter
import umbra.ui.common
import umbra.ui.widgets.messageBox
from manager.componentsManager import Manager
from umbra.preferences import Preferences
from umbra.processing import Processing
from umbra.ui.widgets.application_QToolBar import Application_QToolBar
from umbra.ui.widgets.delayed_QSplashScreen import Delayed_QSplashScreen

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
		   "SESSION_HEADER_TEXT",
		   "SESSION_FOOTER_TEXT",
		   "showProcessing",
		   "encapsulateProcessing",
		   "Umbra",
		   "setUserApplicationDataDirectory",
		   "getCommandLineParametersParser",
		   "getLoggingFile",
		   "run",
		   "exit"]

LOGGER = foundations.verbose.installLogger()

def _initializeLogging():
	"""
	Initializes the Application logging.
	"""

	# Starting the console handler if a terminal is available.
	if sys.stdout.isatty() or platform.system() in ("Darwin", "Linux"):
		RuntimeGlobals.loggingConsoleHandler = foundations.verbose.getLoggingConsoleHandler()

	# Defining logging formatters.
	RuntimeGlobals.loggingFormatters = {"Default": foundations.verbose.LOGGING_DEFAULT_FORMATTER,
										"Extended": foundations.verbose.LOGGING_EXTENDED_FORMATTER,
										"Standard": foundations.verbose.LOGGING_STANDARD_FORMATTER}

_initializeLogging()

def _initializeApplication():
	"""
	Initializes the Application.
	"""

	RuntimeGlobals.application = umbra.ui.common.getApplicationInstance()
	umbra.ui.common.setWindowDefaultIcon(RuntimeGlobals.application)

	RuntimeGlobals.reporter = umbra.reporter.installExceptionReporter()

_initializeApplication()

@umbra.reporter.criticalExceptionHandler
def _initializeApplicationUiFile():
	"""
	Initializes the Application ui file.
	"""

	RuntimeGlobals.uiFile = umbra.ui.common.getResourcePath(UiConstants.uiFile)
	if not foundations.common.pathExists(RuntimeGlobals.uiFile):
		raise foundations.exceptions.FileExistsError("'{0}' ui file is not available, {1} will now close!".format(
			UiConstants.uiFile, Constants.applicationName))

_initializeApplicationUiFile()

SESSION_HEADER_TEXT = ("{0} | Copyright ( C ) 2008 - 2014 Thomas Mansencal - thomas.mansencal@gmail.com".format(
	Constants.applicationName),
					   "{0} | This software is released under terms of GNU GPL V3 license.".format(
						   Constants.applicationName),
					   "{0} | http://www.gnu.org/licenses/ ".format(Constants.applicationName),
					   "{0} | Version: {1}".format(Constants.applicationName, Constants.version))

SESSION_FOOTER_TEXT = ("{0} | Closing interface! ".format(Constants.applicationName),
					   Constants.loggingSeparators,
					   "{0} | Session ended at: {1}".format(Constants.applicationName, time.strftime('%X - %x')),
					   Constants.loggingSeparators)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def showProcessing(message=""):
	"""
	Shows processing behavior.

	:param message: Operation description.
	:type message: unicode
	:return: Object.
	:rtype: object
	"""

	def showProcessingDecorator(object):
		"""
		Shows processing behavior.

		:param object: Object to decorate.
		:type object: object
		:return: Object.
		:rtype: object
		"""

		@functools.wraps(object)
		def showProcessingWrapper(*args, **kwargs):
			"""
			Shows processing behavior.

			:param \*args: Arguments.
			:type \*args: \*
			:param \*\*kwargs: Keywords arguments.
			:type \*\*kwargs: \*\*
			"""

			RuntimeGlobals.engine.startProcessing(message, warning=False)
			try:
				return object(*args, **kwargs)
			finally:
				RuntimeGlobals.engine.stopProcessing(warning=False)

		return showProcessingWrapper

	return showProcessingDecorator

def encapsulateProcessing(object):
	"""
	Encapsulates a processing operation.

	:param object: Object to decorate.
	:type object: object
	:return: Object.
	:rtype: object
	"""

	@functools.wraps(object)
	def encapsulateProcessingWrapper(*args, **kwargs):
		"""
		Encapsulates a processing operation.

		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		RuntimeGlobals.engine._Umbra__storeProcessingState()
		RuntimeGlobals.engine.stopProcessing(warning=False)
		try:
			return object(*args, **kwargs)
		finally:
			RuntimeGlobals.engine.stopProcessing(warning=False)
			RuntimeGlobals.engine._Umbra__restoreProcessingState()

	return encapsulateProcessingWrapper

class Umbra(foundations.ui.common.QWidgetFactory(uiFile=RuntimeGlobals.uiFile)):
	"""
	Defines the main class of the **Umbra** package.
	"""

	# Custom signals definitions.
	verbosityLevelChanged = pyqtSignal(int)
	"""
	This signal is emited by the :class:`Umbra` class when the current verbosity level has changed. ( pyqtSignal )

	:return: Current verbosity level.
	:rtype: int
	"""

	contentDropped = pyqtSignal(QEvent)
	"""
	This signal is emited by the :class:`Umbra` class when it receives dropped content. ( pyqtSignal )

	:return: Event.
	:rtype: QEvent
	"""

	sizeChanged = pyqtSignal(QEvent)
	"""
	This signal is emited by the :class:`Umbra` class when its size changes. ( pyqtSignal )

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

	@umbra.reporter.criticalExceptionHandler
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
		hasattr(self, "onPreInitialisation") and self.onPreInitialisation()

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		settings = foundations.dataStructures.Structure(**{"componentsPaths": None,
														   "requisiteComponents": None,
														   "visibleComponents": None,
														   "splashscreen": None,
														   "requestsStack": None,
														   "patchesManager": None,
														   "userApplicationDataDirectory": None,
														   "loggingSessionHandler": None,
														   "loggingFileHandler": None,
														   "loggingConsoleHandler": None,
														   "loggingSessionHandlerStream": None,
														   "loggingActiveFormatter": None,
														   "settings": None,
														   "verbosityLevel": None,
														   "parameters": None,
														   "arguments": None})

		settings.update(dict((key, value) for key, value in kwargs.iteritems() if key in settings))

		super(Umbra, self).__init__(parent,
									*args,
									**dict((key, value) for key, value in kwargs.iteritems() if key not in settings))

		# --- Running initialisation method. ---
		hasattr(self, "onInitialisation") and self.onInitialisation()

		# --- Setting class attributes. ---
		self.__componentsPaths = settings.componentsPaths or []
		self.__requisiteComponents = settings.requisiteComponents or []
		self.__visibleComponents = settings.visibleComponents or []

		self.__splashscreen = settings.splashscreen

		self.__timer = None
		self.__requestsStack = settings.requestsStack
		self.__patchesManager = settings.patchesManager
		self.__componentsManager = None
		self.__actionsManager = None
		self.__fileSystemEventsManager = None
		self.__notificationsManager = None
		self.__layoutsManager = None
		self.__userApplicationDataDirectory = settings.userApplicationDataDirectory
		self.__loggingSessionHandler = settings.loggingSessionHandler
		self.__loggingFileHandler = settings.loggingFileHandler
		self.__loggingConsoleHandler = settings.loggingConsoleHandler
		self.__loggingSessionHandlerStream = settings.loggingSessionHandlerStream
		self.__loggingActiveFormatter = settings.loggingActiveFormatter
		self.__verbosityLevel = settings.verbosityLevel
		self.__settings = settings.settings
		self.__parameters = settings.parameters
		self.__arguments = settings.arguments
		self.__workerThreads = []
		self.__isProcessing = False
		self.__locals = {}

		self.__processingState = None

		# --- Initializing Application timer. ---
		self.__timer = QTimer(self)
		self.__timer.start(Constants.defaultTimerCycle)

		# --- Initializing Application. ---
		self.__splashscreen and self.__splashscreen.showMessage(
			"{0} - {1} | Initializing interface.".format(self.__class__.__name__, Constants.version),
			waitTime=0.25)

		# --- Initializing the Actions Manager. ---
		self.__actionsManager = RuntimeGlobals.actionsManager = umbra.managers.actionsManager.ActionsManager(self)

		# --- Initializing the File System Events Manager. ---
		self.__fileSystemEventsManager = RuntimeGlobals.fileSystemEventsManager = \
			umbra.managers.fileSystemEventsManager.FileSystemEventsManager(self)
		self.__workerThreads.append(self.__fileSystemEventsManager)
		if not self.__parameters.deactivateWorkerThreads:
			self.__fileSystemEventsManager.start()
		else:
			LOGGER.info("{0} | File system events ignored by '{1}' command line parameter value!".format(
				self.__class__.__name__, "deactivateWorkerThreads"))

		# --- Initializing the Notifications Manager. ---
		self.__notificationsManager = RuntimeGlobals.notificationsManager = \
			umbra.managers.notificationsManager.NotificationsManager(self)

		# --- Initializing the Layouts Manager. ---
		self.__layoutsManager = RuntimeGlobals.layoutsManager = umbra.managers.layoutsManager.LayoutsManager(self)

		# Visual style initialization.
		self.setVisualStyle()
		umbra.ui.common.setWindowDefaultIcon(self)

		# Various ui initializations.
		self.setAcceptDrops(True)

		# Setting window title and toolBar and statusBar.
		self.setWindowTitle("{0} - {1}".format(Constants.applicationName, Constants.version))
		self.toolBar = Application_QToolBar(self)
		self.addToolBar(self.toolBar)

		# Setting processing widget.
		self.Application_Progress_Status_processing = Processing(self, Qt.Window)
		self.statusBar.addPermanentWidget(self.Application_Progress_Status_processing)
		self.Application_Progress_Status_processing.hide()

		# --- Initializing the Components Manager. ---
		self.__splashscreen and self.__splashscreen.showMessage(
			"{0} - {1} | Initializing Components manager.".format(self.__class__.__name__, Constants.version),
			waitTime=0.25)

		self.__componentsManager = RuntimeGlobals.componentsManager = Manager(settings.componentsPaths)
		self.__componentsManager.registerComponents()

		if not self.__componentsManager.components:
			self.notificationsManager.warnify("{0} | '{1}' Components Manager has no Components!".format(
				self.__class__.__name__, Constants.applicationName))

		self.__componentsManager.instantiateComponents(self.__componentsInstantiationCallback)

		# --- Activating requisite Components. ---
		self.__setComponents(requisite=True)

		# --- Activating others Components. ---
		self.__setComponents(requisite=False)

		# --- Initializing requestsStack. ---
		self.__setLocals()
		# Signals / Slots.
		self.__timer.timeout.connect(self.__processRequestsStack)

		# Hiding splashscreen.
		LOGGER.debug("> Hiding splashscreen.")
		if self.__splashscreen:
			self.__splashscreen.showMessage("{0} - {1} | Initialization done.".format(
				self.__class__.__name__, Constants.version))
			self.__splashscreen.hide()

		# --- Running onStartup components methods. ---
		for component in self.__componentsManager.listComponents():
			try:
				interface = self.__componentsManager.getInterface(component)
				if not interface:
					continue

				if interface.activated:
					hasattr(interface, "onStartup") and interface.onStartup()
			except Exception as error:
				umbra.reporter.baseExceptionHandler(umbra.exceptions.EngineInitializationError(
					"'{0}' Component 'onStartup' method raised an exception, unexpected behavior may occur!\n Exception raised: {1}".format(
						component, error)))

		self.__layoutsManager.restoreStartupLayout()

		# --- Running post initialisation method. ---
		hasattr(self, "onPostInitialisation") and self.onPostInitialisation()

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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
	def requestsStack(self):
		"""
		Property for **self.__requestsStack** attribute.

		:return: self.__requestsStack. ( collections.deque )
		"""

		return self.__requestsStack

	@requestsStack.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def requestsStack(self, value):
		"""
		Setter for **self.__requestsStack** attribute.

		:param value: Attribute value. ( collections.deque )
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "requestsStack"))

	@requestsStack.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def requestsStack(self):
		"""
		Deleter for **self.__requestsStack** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "requestsStack"))

	@property
	def componentsPaths(self):
		"""
		Property for **self.__componentsPaths** attribute.

		:return: self.__componentsPaths.
		:rtype: tuple or list
		"""

		return self.__componentsPaths

	@componentsPaths.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def componentsPaths(self, value):
		"""
		Setter for **self.__componentsPaths** attribute.

		:param value: Attribute value.
		:type value: tuple or list
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "componentsPaths"))

	@componentsPaths.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def componentsPaths(self):
		"""
		Deleter for **self.__componentsPaths** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "componentsPaths"))

	@property
	def requisiteComponents(self):
		"""
		Property for **self.__requisiteComponents** attribute.

		:return: self.__requisiteComponents.
		:rtype: tuple or list
		"""

		return self.__requisiteComponents

	@requisiteComponents.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def requisiteComponents(self, value):
		"""
		Setter for **self.__requisiteComponents** attribute.

		:param value: Attribute value.
		:type value: tuple or list
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "requisiteComponents"))

	@requisiteComponents.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def requisiteComponents(self):
		"""
		Deleter for **self.__requisiteComponents** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "requisiteComponents"))

	@property
	def visibleComponents(self):
		"""
		Property for **self.__visibleComponents** attribute.

		:return: self.__visibleComponents.
		:rtype: tuple or list
		"""

		return self.__visibleComponents

	@visibleComponents.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def visibleComponents(self, value):
		"""
		Setter for **self.__visibleComponents** attribute.

		:param value: Attribute value.
		:type value: tuple or list
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
				"visibleComponents", value)
			for element in value:
				assert type(element) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
					"visibleComponents", element)
		self.__visibleComponents = value

	@visibleComponents.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def visibleComponents(self):
		"""
		Deleter for **self.__visibleComponents** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "visibleComponents"))

	@property
	def splashscreen(self):
		"""
		Property for **self.__splashscreen** attribute.

		:return: self.__splashscreen.
		:rtype: Delayed_QSplashScreen
		"""

		return self.__splashscreen

	@splashscreen.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def splashscreen(self, value):
		"""
		Setter for **self.__splashscreen** attribute.

		:param value: Attribute value.
		:type value: Delayed_QSplashScreen
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "splashscreen"))

	@splashscreen.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def splashscreen(self):
		"""
		Deleter for **self.__splashscreen** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "splashscreen"))

	@property
	def patchesManager(self):
		"""
		Property for **self.__patchesManager** attribute.

		:return: self.__patchesManager.
		:rtype: PatchesManager
		"""

		return self.__patchesManager

	@patchesManager.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def patchesManager(self, value):
		"""
		Setter for **self.__patchesManager** attribute.

		:param value: Attribute value.
		:type value: PatchesManager
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "patchesManager"))

	@patchesManager.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def patchesManager(self):
		"""
		Deleter for **self.__patchesManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "patchesManager"))

	@property
	def componentsManager(self):
		"""
		Property for **self.__componentsManager** attribute.

		:return: self.__componentsManager.
		:rtype: ComponentsManager
		"""

		return self.__componentsManager

	@componentsManager.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def componentsManager(self, value):
		"""
		Setter for **self.__componentsManager** attribute.

		:param value: Attribute value.
		:type value: ComponentsManager
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "componentsManager"))

	@componentsManager.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def componentsManager(self):
		"""
		Deleter for **self.__componentsManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "componentsManager"))

	@property
	def notificationsManager(self):
		"""
		Property for **self.__notificationsManager** attribute.

		:return: self.__notificationsManager.
		:rtype: NotificationsManager
		"""

		return self.__notificationsManager

	@notificationsManager.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def notificationsManager(self, value):
		"""
		Setter for **self.__notificationsManager** attribute.

		:param value: Attribute value.
		:type value: NotificationsManager
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "notificationsManager"))

	@notificationsManager.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def notificationsManager(self):
		"""
		Deleter for **self.__notificationsManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "notificationsManager"))

	@property
	def actionsManager(self):
		"""
		Property for **self.__actionsManager** attribute.

		:return: self.__actionsManager.
		:rtype: ActionsManager
		"""

		return self.__actionsManager

	@actionsManager.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def actionsManager(self, value):
		"""
		Setter for **self.__actionsManager** attribute.

		:param value: Attribute value.
		:type value: ActionsManager
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "actionsManager"))

	@actionsManager.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def actionsManager(self):
		"""
		Deleter for **self.__actionsManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "actionsManager"))

	@property
	def fileSystemEventsManager(self):
		"""
		Property for **self.__fileSystemEventsManager** attribute.

		:return: self.__fileSystemEventsManager.
		:rtype: FileSystemEventsManager
		"""

		return self.__fileSystemEventsManager

	@fileSystemEventsManager.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def fileSystemEventsManager(self, value):
		"""
		Setter for **self.__fileSystemEventsManager** attribute.

		:param value: Attribute value.
		:type value: FileSystemEventsManager
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "fileSystemEventsManager"))

	@fileSystemEventsManager.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def fileSystemEventsManager(self):
		"""
		Deleter for **self.__fileSystemEventsManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "fileSystemEventsManager"))

	@property
	def layoutsManager(self):
		"""
		Property for **self.__layoutsManager** attribute.

		:return: self.__layoutsManager.
		:rtype: LayoutsManager
		"""

		return self.__layoutsManager

	@layoutsManager.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def layoutsManager(self, value):
		"""
		Setter for **self.__layoutsManager** attribute.

		:param value: Attribute value.
		:type value: LayoutsManager
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "layoutsManager"))

	@layoutsManager.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def layoutsManager(self):
		"""
		Deleter for **self.__layoutsManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "layoutsManager"))

	@property
	def userApplicationDataDirectory(self):
		"""
		Property for **self.__userApplicationDataDirectory** attribute.

		:return: self.__userApplicationDataDirectory.
		:rtype: unicode
		"""

		return self.__userApplicationDataDirectory

	@userApplicationDataDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def userApplicationDataDirectory(self, value):
		"""
		Setter for **self.__userApplicationDataDirectory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "userApplicationDataDirectory"))

	@userApplicationDataDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def userApplicationDataDirectory(self):
		"""
		Deleter for **self.__userApplicationDataDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "userApplicationDataDirectory"))

	@property
	def loggingSessionHandler(self):
		"""
		Property for **self.__loggingSessionHandler** attribute.

		:return: self.__loggingSessionHandler.
		:rtype: Handler
		"""

		return self.__loggingSessionHandler

	@loggingSessionHandler.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def loggingSessionHandler(self, value):
		"""
		Setter for **self.__loggingSessionHandler** attribute.

		:param value: Attribute value.
		:type value: Handler
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "loggingSessionHandler"))

	@loggingSessionHandler.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def loggingSessionHandler(self):
		"""
		Deleter for **self.__loggingSessionHandler** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "loggingSessionHandler"))

	@property
	def loggingFileHandler(self):
		"""
		Property for **self.__loggingFileHandler** attribute.

		:return: self.__loggingFileHandler.
		:rtype: Handler
		"""

		return self.__loggingFileHandler

	@loggingFileHandler.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def loggingFileHandler(self, value):
		"""
		Setter for **self.__loggingFileHandler** attribute.

		:param value: Attribute value.
		:type value: Handler
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "loggingFileHandler"))

	@loggingFileHandler.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def loggingFileHandler(self):
		"""
		Deleter for **self.__loggingFileHandler** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "loggingFileHandler"))

	@property
	def loggingConsoleHandler(self):
		"""
		Property for **self.__loggingConsoleHandler** attribute.

		:return: self.__loggingConsoleHandler.
		:rtype: Handler
		"""

		return self.__loggingConsoleHandler

	@loggingConsoleHandler.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def loggingConsoleHandler(self, value):
		"""
		Setter for **self.__loggingConsoleHandler** attribute.

		:param value: Attribute value.
		:type value: Handler
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "loggingConsoleHandler"))

	@loggingConsoleHandler.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def loggingConsoleHandler(self):
		"""
		Deleter for **self.__loggingConsoleHandler** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "loggingConsoleHandler"))

	@property
	@foundations.trace.untracable
	def loggingSessionHandlerStream(self):
		"""
		Property for **self.__loggingSessionHandlerStream** attribute.

		:return: self.__loggingSessionHandlerStream.
		:rtype: StreamObject
		"""

		return self.__loggingSessionHandlerStream

	@loggingSessionHandlerStream.setter
	@foundations.trace.untracable
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def loggingSessionHandlerStream(self, value):
		"""
		Setter for **self.__loggingSessionHandlerStream** attribute.

		:param value: Attribute value.
		:type value: StreamObject
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "loggingSessionHandlerStream"))

	@loggingSessionHandlerStream.deleter
	@foundations.trace.untracable
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def loggingSessionHandlerStream(self):
		"""
		Deleter for **self.__loggingSessionHandlerStream** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "loggingSessionHandlerStream"))

	@property
	def loggingActiveFormatter(self):
		"""
		Property for **self.__loggingActiveFormatter** attribute.

		:return: self.__loggingActiveFormatter.
		:rtype: Formatter
		"""

		return self.__loggingActiveFormatter

	@loggingActiveFormatter.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def loggingActiveFormatter(self, value):
		"""
		Setter for **self.__loggingActiveFormatter** attribute.

		:param value: Attribute value.
		:type value: unicode or QString
		"""

		if value is not None:
			assert type(value) in (
			unicode, QString), "'{0}' attribute: '{1}' type is not 'unicode' or 'QString'!".format(
				"loggingActiveFormatter", value)
		self.__loggingActiveFormatter = value

	@loggingActiveFormatter.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def loggingActiveFormatter(self):
		"""
		Deleter for **self.__loggingActiveFormatter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "loggingActiveFormatter"))

	@property
	def verbosityLevel(self):
		"""
		Property for **self.__verbosityLevel** attribute.

		:return: self.__verbosityLevel.
		:rtype: int
		"""

		return self.__verbosityLevel

	@verbosityLevel.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def verbosityLevel(self, value):
		"""
		Setter for **self.__verbosityLevel** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("verbosityLevel", value)
			assert value >= 0 and value <= 4, "'{0}' attribute: Value need to be exactly beetween 0 and 4!".format(
				"verbosityLevel")
		self.__verbosityLevel = value

	@verbosityLevel.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def verbosityLevel(self):
		"""
		Deleter for **self.__verbosityLevel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "verbosityLevel"))

	@property
	def settings(self):
		"""
		Property for **self.__settings** attribute.

		:return: self.__settings.
		:rtype: Preferences
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		Setter for **self.__settings** attribute.

		:param value: Attribute value.
		:type value: Preferences
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def parameters(self, value):
		"""
		Setter for **self.__parameters** attribute.

		:param value: Attribute value.
		:type value: object
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "parameters"))

	@parameters.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def arguments(self, value):
		"""
		Setter for **self.__arguments** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "arguments"))

	@arguments.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def arguments(self):
		"""
		Deleter for **self.__arguments** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "arguments"))

	@property
	def workerThreads(self):
		"""
		Property for **self.__workerThreads** attribute.

		:return: self.__workerThreads.
		:rtype: list
		"""

		return self.__workerThreads

	@workerThreads.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def workerThreads(self, value):
		"""
		Setter for **self.__workerThreads** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "workerThreads"))

	@workerThreads.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def workerThreads(self):
		"""
		Deleter for **self.__workerThreads** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "workerThreads"))

	@property
	def isProcessing(self):
		"""
		Property for **self.__isProcessing** attribute.

		:return: self.__isProcessing.
		:rtype: bool
		"""

		return self.__isProcessing

	@isProcessing.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def isProcessing(self, value):
		"""
		Setter for **self.__isProcessing** attribute.

		:param value: Attribute value.
		:type value: bool
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "isProcessing"))

	@isProcessing.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def isProcessing(self):
		"""
		Deleter for **self.__isProcessing** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "isProcessing"))

	@property
	def locals(self):
		"""
		Property for **self.__locals** attribute.

		:return: self.__locals.
		:rtype: dict
		"""

		return self.__locals

	@locals.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def locals(self, value):
		"""
		Setter for **self.__locals** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "locals"))

	@locals.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def locals(self):
		"""
		Deleter for **self.__locals** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "locals"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
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
		self.contentDropped.emit(event)

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
		self.sizeChanged.emit(event)
		event.accept()

	def __setComponents(self, requisite=True):
		"""
		Sets the Components.

		:param requisite: Set only requisite Components.
		:type requisite: bool
		"""

		components = self.__componentsManager.listComponents()
		candidateComponents = \
			getattr(set(components), "intersection" if requisite else "difference")(self.__requisiteComponents)
		deactivatedComponents = self.__settings.getKey("Settings", "deactivatedComponents").toString().split(",")
		candidateComponents = \
			sorted(filter(lambda x: x not in deactivatedComponents, candidateComponents), key=(components).index)

		for component in candidateComponents:
			try:
				profile = self.__componentsManager.components[component]
				interface = self.__componentsManager.getInterface(component)

				setattr(self,
						"_{0}__{1}".format(self.__class__.__name__, foundations.namespace.getLeaf(component, ".")),
						interface)

				self.__splashscreen and self.__splashscreen.showMessage(
					"{0} - {1} | Activating {2}.".format(self.__class__.__name__, Constants.version, component))
				interface.activate(self)
				if profile.category in ("Default", "QObject"):
					interface.initialize()
				elif profile.category == "QWidget":
					interface.addWidget()
					interface.initializeUi()
			except Exception as error:
				if requisite:
					message = "'{0}' Component failed to activate!\nException raised: {1}"
					handler = umbra.reporter.systemExitExceptionHandler
				else:
					message = "'{0}' Component failed to activate, unexpected behavior may occur!\nException raised: {1}"
					handler = umbra.reporter.baseExceptionHandler

				exception = manager.exceptions.ComponentActivationError(message.format(component, error))
				handler(exception)

	def __setLocals(self):
		"""
		Sets the locals for the requestsStack.
		"""

		for globals in (Constants, RuntimeGlobals, UiConstants):
			self.__locals[globals.__name__] = globals

		self.__locals[Constants.applicationName] = self
		self.__locals["application"] = self
		self.__locals["patchesManager"] = self.__patchesManager
		self.__locals["componentsManager"] = self.__componentsManager
		self.__locals["actionsManager"] = self.__actionsManager
		self.__locals["fileSystemEventsManager"] = self.__fileSystemEventsManager
		self.__locals["notificationsManager"] = self.__notificationsManager
		self.__locals["layoutsManager"] = self.__layoutsManager
		self.__locals["LOGGER"] = LOGGER

		LOGGER.debug("> Defined locals: '{0}'.".format(self.__locals))

	def __processRequestsStack(self):
		"""
		Process the requests stack.
		"""

		while self.__requestsStack:
			try:
				exec self.__requestsStack.popleft() in self.__locals
			except Exception as error:
				umbra.exceptions.notifyExceptionHandler(error)

	def __componentsInstantiationCallback(self, profile):
		"""
		Defines a callback for Components instantiation.

		:param profile: Component Profile.
		:type profile: Profile
		"""

		self.__splashscreen and self.__splashscreen.showMessage(
			"{0} - {1} | Instantiating {2} Component.".format(self.__class__.__name__, Constants.version,
															  profile.name))

	def __storeProcessingState(self):
		"""
		Stores the processing state.
		"""

		steps = self.Application_Progress_Status_processing.Processing_progressBar.maximum()
		value = self.Application_Progress_Status_processing.Processing_progressBar.value()
		message = self.Application_Progress_Status_processing.Processing_label.text()
		state = self.__isProcessing

		self.__processingState = steps, value, message, state

	def __restoreProcessingState(self):
		"""
		Restores the processing state.
		"""

		steps, value, message, state = self.__processingState

		self.Application_Progress_Status_processing.Processing_progressBar.setRange(0, steps)
		self.Application_Progress_Status_processing.Processing_progressBar.setValue(value)
		self.setProcessingMessage(message, warning=False)
		self.__isProcessing = state
		state and self.Application_Progress_Status_processing.show()

	def setVerbosityLevel(self, verbosityLevel):
		"""
		Sets the Application verbosity level.

		:param verbosityLevel: Verbosity level.
		:type verbosityLevel: int
		:return: Method success.
		:rtype: bool

		:note: The expected verbosity level value is an integer between 0 to 4.
		"""

		self.__verbosityLevel = verbosityLevel
		foundations.verbose.setVerbosityLevel(verbosityLevel)
		self.__settings.setKey("Settings", "verbosityLevel", verbosityLevel)
		self.verbosityLevelChanged.emit(verbosityLevel)
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.FileExistsError)
	def setVisualStyle(self, fullScreenStyle=False):
		"""
		Sets the Application visual style.

		:param fullScreenStyle: Use fullscreen stylesheet file.
		:type fullScreenStyle: bool
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Setting Application visual style.")
		platformStyles = {"Windows": (("Windows", "Microsoft"),
									  UiConstants.windowsStyle,
									  UiConstants.windowsStylesheetFile,
									  UiConstants.windowsFullScreenStylesheetFile),
						  "Darwin": (("Darwin",),
									 UiConstants.darwinStyle,
									 UiConstants.darwinStylesheetFile,
									 UiConstants.darwinFullScreenStylesheetFile),
						  "Linux": (("Linux",),
									UiConstants.linuxStyle,
									UiConstants.linuxStylesheetFile,
									UiConstants.linuxFullScreenStylesheetFile)}

		styleSheetFile = None
		for platformStyle, settings in platformStyles.iteritems():
			LOGGER.debug("> Setting '{0}' visual style.".format(platformStyle))
			platformSystems, style, styleSheeFile, fullScreenStyleSheetFile = settings
			if platform.system() in platformSystems:
				RuntimeGlobals.application.setStyle(style)
				styleSheetPath = umbra.ui.common.getResourcePath(styleSheeFile)
				if fullScreenStyle:
					fullScreenStyleSheetPath = umbra.ui.common.getResourcePath(fullScreenStyleSheetFile,
																			   raiseException=False)
					styleSheetPath = fullScreenStyleSheetPath or styleSheetPath
				styleSheetFile = foundations.io.File(styleSheetPath)
				break

		if not styleSheetFile:
			raise foundations.exceptions.FileExistsError(
				"{0} | No stylesheet file found, visual style will not be applied!".format(self.__class__.__name__))

		if foundations.common.pathExists(styleSheetFile.path):
			LOGGER.debug("> Reading style sheet file: '{0}'.".format(styleSheetFile.path))
			styleSheetFile.cache()
			for i, line in enumerate(styleSheetFile.content):
				search = re.search(r"url\((?P<url>.*)\)", line)
				if not search:
					continue

				styleSheetFile.content[i] = line.replace(search.group("url"),
														 foundations.strings.toForwardSlashes(
															 umbra.ui.common.getResourcePath(search.group("url"))))
			RuntimeGlobals.application.setStyleSheet(QString("".join(styleSheetFile.content)))
			return True
		else:
			raise foundations.exceptions.FileExistsError(
				"{0} | '{1}' stylesheet file is not available, visual style will not be applied!".format(
					self.__class__.__name__, styleSheetFile.path))

	def isFullScreen(self):
		"""
		Returns if Application is in fullscreen state.

		:return: FullScreen state.
		:rtype: bool
		"""

		return self.windowState().__int__() == 4 and True or False

	def toggleFullScreen(self, *args):
		"""
		Toggles Application fullscreen state.

		:param \*args: Arguments.
		:type \*args: \*
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Toggling FullScreen state.")

		if self.isFullScreen():
			self.setUnifiedTitleAndToolBarOnMac(True)
			self.setVisualStyle(fullScreenStyle=False)
			self.showNormal()
			# TODO: Remove hack that ensure toolBar is repainted.
			platform.system() == "Darwin" and self.resize(self.size().width() + 1, self.size().height() + 1)
		else:
			self.setUnifiedTitleAndToolBarOnMac(False)
			self.setVisualStyle(fullScreenStyle=True)
			self.showFullScreen()
		return True

	def processEvents(self, flags=QEventLoop.AllEvents):
		"""
		Process Application events.

		:param flags: Events flags.
		:type flags: int
		:return: Method success.
		:rtype: bool
		"""

		QApplication.processEvents(flags)
		return True

	def setProcessingMessage(self, message, warning=True):
		"""
		Sets the processing operation message.

		:param message: Operation description.
		:type message: unicode
		:param warning: Emit warning message.
		:type warning: int
		:return: Method success.
		:rtype: bool
		"""

		if not self.__isProcessing:
			warning and LOGGER.warning(
				"!> {0} | Engine not processing, 'setProcessingMessage' request has been ignored!".format(
					self.__class__.__name__))
			return False

		LOGGER.debug("> Setting processing message!")

		self.Application_Progress_Status_processing.Processing_label.setText(message)
		self.processEvents()
		return True

	def startProcessing(self, message, steps=0, warning=True):
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

		if self.__isProcessing:
			warning and LOGGER.warning(
				"!> {0} | Engine is already processing, 'startProcessing' request has been ignored!".format(
					self.__class__.__name__))
			return False

		LOGGER.debug("> Starting processing operation!")

		self.__isProcessing = True
		self.Application_Progress_Status_processing.Processing_progressBar.setRange(0, steps)
		self.Application_Progress_Status_processing.Processing_progressBar.setValue(0)
		self.Application_Progress_Status_processing.show()
		self.setProcessingMessage(message)
		return True

	def stepProcessing(self, warning=True):
		"""
		Steps the processing operation progress indicator.

		:param warning: Emit warning message.
		:type warning: int
		:return: Method success.
		:rtype: bool
		"""

		if not self.__isProcessing:
			warning and LOGGER.warning(
				"!> {0} | Engine is not processing, 'stepProcessing' request has been ignored!".format(
					self.__class__.__name__))
			return False

		LOGGER.debug("> Stepping processing operation!")

		self.Application_Progress_Status_processing.Processing_progressBar.setValue(
			self.Application_Progress_Status_processing.Processing_progressBar.value() + 1)
		self.processEvents()
		return True

	def stopProcessing(self, warning=True):
		"""
		Registers the end of a processing operation.

		:param warning: Emit warning message.
		:type warning: int
		:return: Method success.
		:rtype: bool
		"""

		if not self.__isProcessing:
			warning and LOGGER.warning(
				"!> {0} | Engine is not processing, 'stopProcessing' request has been ignored!".format(
					self.__class__.__name__))
			return False

		LOGGER.debug("> Stopping processing operation!")

		self.__isProcessing = False
		self.Application_Progress_Status_processing.Processing_label.setText(QString())
		self.Application_Progress_Status_processing.Processing_progressBar.setRange(0, 100)
		self.Application_Progress_Status_processing.Processing_progressBar.setValue(0)
		self.Application_Progress_Status_processing.hide()
		return True

	def garbageCollect(self):
		"""
		Triggers the garbage collecting.

		:return: Number of unreachable objects found.
		:rtype: int
		"""

		LOGGER.debug("> Garbage collecting!")

		return gc.collect()

	def quit(self, exitCode=0, event=None):
		"""
		Quits the Application.

		:param exitCode: Exit code.
		:type exitCode: int
		:param event: QEvent.
		:type event: QEvent
		"""

		# --- Running onClose components methods. ---
		for component in reversed(self.__componentsManager.listComponents()):
			interface = self.__componentsManager.getInterface(component)
			if not interface:
				continue

			if not interface.activated:
				continue

			if not hasattr(interface, "onClose"):
				continue

			if not interface.onClose():
				event and event.ignore()
				return

		# Storing current layout.
		self.__layoutsManager.storeStartupLayout()
		self.__settings.settings.sync()

		# Stopping worker threads.
		for workerThread in self.__workerThreads:
			LOGGER.debug("> Stopping worker thread: '{0}'.".format(workerThread))
			if not workerThread.isFinished():
				workerThread.quit()
			workerThread.wait()

		foundations.verbose.removeLoggingHandler(self.__loggingFileHandler)
		foundations.verbose.removeLoggingHandler(self.__loggingSessionHandler)
		# foundations.verbose.removeLoggingHandler(self.__loggingConsoleHandler)

		# Stopping the Application timer.
		self.__timer.stop()
		self.__timer = None

		self.deleteLater()
		event and event.accept()

		exit(exitCode)

@umbra.reporter.criticalExceptionHandler
def setUserApplicationDataDirectory(directory):
	"""
	Sets the user Application data directory.

	:param directory: Starting point for the directories tree creation.
	:type directory: unicode
	:return: Definition success.
	:rtype: bool
	"""

	LOGGER.debug("> Current Application data directory '{0}'.".format(directory))
	if foundations.io.setDirectory(directory):
		for subDirectory in Constants.preferencesDirectories:
			if not foundations.io.setDirectory(os.path.join(directory, subDirectory)):
				raise OSError("{0} | '{1}' directory creation failed , '{2}' will now close!".format(
					__name__, os.path.join(directory, subDirectory), Constants.applicationName))
		return True
	else:
		raise OSError("{0} | '{1}' directory creation failed , '{2}' will now close!".format(__name__,
																							 directory,
																							 Constants.applicationName))

def getCommandLineParametersParser():
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
					  dest="verbosityLevel",
					  help="'Application verbosity levels: 0 = Critical | 1 = Error | 2 = Warning | 3 = Info | 4 = Debug.'")
	parser.add_option("-f",
					  "--loggingFormatter",
					  action="store",
					  type="string",
					  dest="loggingFormatter",
					  help="'Application logging formatter: '{0}'.'".format(
						  ", ".join(sorted(RuntimeGlobals.loggingFormatters))))
	parser.add_option("-u",
					  "--userApplicationDataDirectory",
					  action="store",
					  type="string",
					  dest="userApplicationDataDirectory",
					  help="'User Application data directory'.")
	parser.add_option("-s",
					  "--hideSplashScreen",
					  action="store_true",
					  default=False,
					  dest="hideSplashScreen",
					  help="'Hide splashscreen'.")
	parser.add_option("-w",
					  "--deactivateWorkerThreads",
					  action="store_true",
					  default=False,
					  dest="deactivateWorkerThreads",
					  help="'Deactivate worker threads'.")
	parser.add_option("-x",
					  "--startupScript",
					  action="store",
					  type="string",
					  dest="startupScript",
					  help="'Execute given startup script'.")
	parser.add_option("-t",
					  "--traceModules",
					  action="store",
					  default="{}",
					  type="string",
					  dest="traceModules",
					  help="'Trace given modules'.")
	return parser

@umbra.reporter.criticalExceptionHandler
def getLoggingFile(maximumLoggingFiles=10, retries=2 ^ 16):
	"""
	Returns the logging file path.

	:param maximumLoggingFiles: Maximum allowed logging files in the logging directory.
	:type maximumLoggingFiles: int
	:param retries: Number of retries to generate a unique logging file name.
	:type retries: int
	:return: Logging file path.
	:rtype: unicode
	"""

	loggingDirectory = os.path.join(RuntimeGlobals.userApplicationDataDirectory, Constants.loggingDirectory)
	for file in sorted(foundations.walkers.filesWalker(loggingDirectory),
					   key=lambda y: os.path.getmtime(os.path.abspath(y)), reverse=True)[maximumLoggingFiles:]:
		try:
			os.remove(file)
		except OSError:
			LOGGER.warning(
				"!> {0} | Cannot remove '{1}' file!".format(__name__, file, Constants.applicationName))

	path = None
	for i in range(retries):
		path = os.path.join(RuntimeGlobals.userApplicationDataDirectory,
							Constants.loggingDirectory,
							Constants.loggingFile.format(foundations.strings.getRandomSequence()))
		if not os.path.exists(path):
			break

	if path is None:
		raise umbra.exceptions.EngineConfigurationError(
			"{0} | Logging file is not available, '{1}' will now close!".format(__name__, Constants.applicationName))

	LOGGER.debug("> Current Logging file: '{0}'".format(path))

	return path

@umbra.reporter.criticalExceptionHandler
def run(engine, parameters, componentsPaths=None, requisiteComponents=None, visibleComponents=None):
	"""
	Starts the Application.

	:param engine: Engine.
	:type engine: QObject
	:param parameters: Command line parameters.
	:type parameters: tuple
	:param componentsPaths: Components componentsPaths.
	:type componentsPaths: tuple or list
	:param requisiteComponents: Requisite components names.
	:type requisiteComponents: tuple or list
	:param visibleComponents: Visible components names.
	:type visibleComponents: tuple or list
	:return: Definition success.
	:rtype: bool
	"""

	# Command line parameters handling.
	RuntimeGlobals.parameters, RuntimeGlobals.arguments = parameters

	foundations.trace.evaluateTraceRequest(RuntimeGlobals.parameters.traceModules, foundations.verbose.tracer)

	if RuntimeGlobals.parameters.about:
		for line in SESSION_HEADER_TEXT:
			sys.stdout.write("{0}\n".format(line))
		foundations.core.exit(1)

	# Redirecting standard output and error messages.
	sys.stdout = foundations.verbose.StandardOutputStreamer(LOGGER)
	sys.stderr = foundations.verbose.StandardOutputStreamer(LOGGER)

	# Setting application verbose level.
	foundations.verbose.setVerbosityLevel(4)

	# Setting user application data directory.
	if RuntimeGlobals.parameters.userApplicationDataDirectory:
		userApplicationDataDirectory = RuntimeGlobals.userApplicationDataDirectory = \
			RuntimeGlobals.parameters.userApplicationDataDirectory
	else:
		userApplicationDataDirectory = RuntimeGlobals.userApplicationDataDirectory = \
			foundations.environment.getUserApplicationDataDirectory()

	if not setUserApplicationDataDirectory(userApplicationDataDirectory):
		raise umbra.exceptions.EngineConfigurationError(
			"{0} | '{1}' user Application data directory is not available, '{2}' will now close!".format(
				__name__, RuntimeGlobals.userApplicationDataDirectory, Constants.applicationName))

	if foundations.environment.getTemporaryDirectory() in userApplicationDataDirectory:
		umbra.ui.widgets.messageBox.messageBox("Error",
											   "Error",
"{0} failed to use the default user Application data directory to store its preferences \
and has defaulted to the following directory:\n\n\t'{1}'.\n\nReasons for this are various:\n\
\t- Undefined 'APPDATA' ( Windows ) or 'HOME' ( Mac Os X, Linux ) environment variables.\n\
\t- User name with non 'UTF-8' encoding compliant characters.\n\
\t- Non 'UTF-8' encoding compliant characters in the preferences directory path.\n\n\
You will have to define your own preferences directory by launching {0} with the \
'-u \"path\\to\\the\\custom\\preferences\\directory\"' command line parameter.".format(
												   Constants.applicationName,
												   userApplicationDataDirectory))

	LOGGER.debug("> Application Python interpreter: '{0}'".format(sys.executable))
	LOGGER.debug("> Application PyQt version: '{0}'".format(PYQT_VERSION_STR))
	LOGGER.debug("> Application startup location: '{0}'".format(os.getcwd()))
	LOGGER.debug("> Session user Application data directory: '{0}'".format(RuntimeGlobals.userApplicationDataDirectory))

	LOGGER.debug("> Initializing '{0}'!".format(Constants.applicationName))

	# Getting the logging file path.
	RuntimeGlobals.loggingFile = getLoggingFile()
	RuntimeGlobals.loggingFileHandler = foundations.verbose.getLoggingFileHandler(file=RuntimeGlobals.loggingFile)

	# Getting the patches file path.
	RuntimeGlobals.patchesFile = os.path.join(RuntimeGlobals.userApplicationDataDirectory,
											  Constants.patchesDirectory,
											  Constants.patchesFile)
	# Initializing the patches manager.
	RuntimeGlobals.patchesManager = umbra.managers.patchesManager.PatchesManager(RuntimeGlobals.patchesFile,
																				 [os.path.join(path,
																							   Constants.patchesDirectory)
																				  for path in
																				  RuntimeGlobals.resourcesDirectories])
	RuntimeGlobals.patchesManager.registerPatches() and RuntimeGlobals.patchesManager.applyPatches()

	# Retrieving settings file.
	RuntimeGlobals.settingsFile = os.path.join(RuntimeGlobals.userApplicationDataDirectory,
											   Constants.settingsDirectory,
											   Constants.settingsFile)

	RuntimeGlobals.settings = Preferences(RuntimeGlobals.settingsFile)

	LOGGER.debug("> Retrieving default layouts.")
	RuntimeGlobals.settings.setDefaultLayouts(("startupCentric",))

	foundations.common.pathExists(RuntimeGlobals.settingsFile) or RuntimeGlobals.settings.setDefaultPreferences()

	LOGGER.debug("> Retrieving stored verbose level.")
	RuntimeGlobals.verbosityLevel = RuntimeGlobals.parameters.verbosityLevel \
		if RuntimeGlobals.parameters.verbosityLevel is not None else \
		foundations.common.getFirstItem(RuntimeGlobals.settings.getKey("Settings", "verbosityLevel").toInt())
	LOGGER.debug("> Setting logger verbosity level to: '{0}'.".format(RuntimeGlobals.verbosityLevel))
	foundations.verbose.setVerbosityLevel(RuntimeGlobals.verbosityLevel)
	RuntimeGlobals.settings.setKey("Settings", "verbosityLevel", RuntimeGlobals.verbosityLevel)

	LOGGER.debug("> Retrieving stored logging formatter.")
	loggingFormatter = RuntimeGlobals.parameters.loggingFormatter if RuntimeGlobals.parameters.loggingFormatter is not None else \
		foundations.strings.toString(RuntimeGlobals.settings.getKey("Settings", "loggingFormatter").toString())
	loggingFormatter = loggingFormatter if loggingFormatter in RuntimeGlobals.loggingFormatters else None
	RuntimeGlobals.loggingActiveFormatter = loggingFormatter if loggingFormatter is not None else Constants.loggingDefaultFormatter
	LOGGER.debug("> Setting logging formatter: '{0}'.".format(RuntimeGlobals.loggingActiveFormatter))
	for handler in (RuntimeGlobals.loggingConsoleHandler, RuntimeGlobals.loggingFileHandler):
		handler and handler.setFormatter(RuntimeGlobals.loggingFormatters[RuntimeGlobals.loggingActiveFormatter])

	# Starting the session handler.
	RuntimeGlobals.loggingSessionHandler = foundations.verbose.getLoggingStreamHandler()
	RuntimeGlobals.loggingSessionHandlerStream = RuntimeGlobals.loggingSessionHandler.stream

	LOGGER.info(Constants.loggingSeparators)
	for line in SESSION_HEADER_TEXT:
		LOGGER.info(line)
	LOGGER.info("{0} | Session started at: {1}".format(Constants.applicationName, time.strftime('%X - %x')))
	LOGGER.info(Constants.loggingSeparators)
	LOGGER.info("{0} | Starting Interface!".format(Constants.applicationName))

	# Initializing splashscreen.
	if RuntimeGlobals.parameters.hideSplashScreen:
		LOGGER.debug("> SplashScreen skipped by 'hideSplashScreen' command line parameter.")
	else:
		LOGGER.debug("> Initializing splashscreen.")

		RuntimeGlobals.splashscreenImage = QPixmap(umbra.ui.common.getResourcePath(UiConstants.splashScreenImage))
		RuntimeGlobals.splashscreen = Delayed_QSplashScreen(RuntimeGlobals.splashscreenImage, textColor=Qt.white)
		RuntimeGlobals.splashscreen.showMessage(
			"{0} - {1} | Initializing {0}.".format(Constants.applicationName, Constants.version))
		RuntimeGlobals.splashscreen.show()

	# Initializing requests stack.
	RuntimeGlobals.requestsStack = collections.deque()

	# Initializing engine.
	RuntimeGlobals.engine = engine(parent=None,
								   componentsPaths=componentsPaths,
								   requisiteComponents=requisiteComponents,
								   visibleComponents=visibleComponents,
								   splashscreen=RuntimeGlobals.splashscreen,
								   requestsStack=RuntimeGlobals.requestsStack,
								   patchesManager=RuntimeGlobals.patchesManager,
								   userApplicationDataDirectory=RuntimeGlobals.userApplicationDataDirectory,
								   loggingSessionHandler=RuntimeGlobals.loggingSessionHandler,
								   loggingFileHandler=RuntimeGlobals.loggingFileHandler,
								   loggingConsoleHandler=RuntimeGlobals.loggingConsoleHandler,
								   loggingSessionHandlerStream=RuntimeGlobals.loggingSessionHandlerStream,
								   loggingActiveFormatter=RuntimeGlobals.loggingActiveFormatter,
								   settings=RuntimeGlobals.settings,
								   verbosityLevel=RuntimeGlobals.verbosityLevel,
								   parameters=RuntimeGlobals.parameters,
								   arguments=RuntimeGlobals.arguments)
	RuntimeGlobals.engine.show()
	RuntimeGlobals.engine.raise_()

	return sys.exit(RuntimeGlobals.application.exec_())

def exit(exitCode=0):
	"""
	Exits the Application.

	:param exitCode: Exit code.
	:type exitCode: int
	"""

	for line in SESSION_FOOTER_TEXT:
		LOGGER.info(line)

	foundations.verbose.removeLoggingHandler(RuntimeGlobals.loggingConsoleHandler)

	RuntimeGlobals.application.exit(exitCode)
