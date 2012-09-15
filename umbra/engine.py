#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**engine.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	| This module is the main **Umbra** package module.
	| It defines various classes, methods and definitions to run, maintain and exit the Application.
	| The main Application object is the :class:`Umbra` class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import collections
import functools
import gc
import inspect
import logging
import os
import optparse
import platform
import re
import sys
import time
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
def _setApplicationPackageDirectory():
	"""
	This definition sets the Application package directory in the path.
	"""

	applicationPackageDirectory = os.path.normpath(os.path.join(sys.path[0], "../"))
	applicationPackageDirectory not in sys.path and sys.path.append(applicationPackageDirectory)

_setApplicationPackageDirectory()

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
	This definition overrides dependencies globals.
	"""

	foundations.globals.constants.Constants.logger = manager.globals.constants.Constants.logger = Constants.logger
	foundations.globals.constants.Constants.applicationDirectory = \
	manager.globals.constants.Constants.applicationDirectory = Constants.applicationDirectory

_overrideDependenciesGlobals()

import foundations.common

def _extendResourcesPaths():
	"""
	This definition extend resources paths.
	"""

	for path in (os.path.join(umbra.__path__[0], Constants.resourcesDirectory),
				os.path.join(os.getcwd(), umbra.__name__, Constants.resourcesDirectory)):
		(foundations.common.pathExists(path) and not path in RuntimeGlobals.resourcesDirectories) and \
		RuntimeGlobals.resourcesDirectories.append(path)

_extendResourcesPaths()

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.environment
import foundations.io as io
import foundations.namespace
import foundations.strings as strings
import foundations.ui.common
import manager.exceptions
import umbra.exceptions
import umbra.managers.actionsManager
import umbra.managers.fileSystemEventsManager
import umbra.managers.notificationsManager
import umbra.managers.patchesManager
import umbra.managers.layoutsManager
import umbra.ui.common
from foundations.streamObject import StreamObject
from manager.componentsManager import Manager
from umbra.preferences import Preferences
from umbra.processing import Processing
from umbra.ui.widgets.application_QToolBar import Application_QToolBar
from umbra.ui.widgets.delayed_QSplashScreen import Delayed_QSplashScreen

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
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
			"run",
			"exit"]

LOGGER = logging.getLogger(Constants.logger)

def _initializeLogging():
	"""
	This definition initializes the Application logging.
	"""

	# Starting the console handler.
	if not hasattr(sys, "frozen") or not (platform.system() == "Windows" or platform.system() == "Microsoft"):
		RuntimeGlobals.loggingConsoleHandler = logging.StreamHandler(sys.__stdout__)
		RuntimeGlobals.loggingConsoleHandler.setFormatter(core.LOGGING_DEFAULT_FORMATTER)
		LOGGER.addHandler(RuntimeGlobals.loggingConsoleHandler)

	# Defining logging formatters.
	RuntimeGlobals.loggingFormatters = {"Default" :core.LOGGING_DEFAULT_FORMATTER,
										"Extended" : core.LOGGING_EXTENDED_FORMATTER,
										"Standard" : core.LOGGING_STANDARD_FORMATTER}

_initializeLogging()

def _initializeApplication():
	"""
	This definition initializes the Application.
	"""

	RuntimeGlobals.application = QApplication(sys.argv)

_initializeApplication()

def _initializeApplicationUiFile():
	"""
	This definition initializes the Application ui file.
	"""

	RuntimeGlobals.uiFile = umbra.ui.common.getResourcePath(UiConstants.uiFile)
	if not foundations.common.pathExists(RuntimeGlobals.uiFile):
		umbra.ui.common.uiSystemExitExceptionHandler(
		foundations.exceptions.FileExistsError("'{0}' ui file is not available, {1} will now close!".format(
		UiConstants.uiFile, Constants.applicationName)), Constants.applicationName)

_initializeApplicationUiFile()

SESSION_HEADER_TEXT = ("{0} | Copyright ( C ) 2008 - 2012 Thomas Mansencal - thomas.mansencal@gmail.com".format(
					Constants.applicationName),
				"{0} | This software is released under terms of GNU GPL V3 license.".format(Constants.applicationName),
				"{0} | http://www.gnu.org/licenses/ ".format(Constants.applicationName),
				"{0} | Version: {1}".format(Constants.applicationName, Constants.releaseVersion))

SESSION_FOOTER_TEXT = ("{0} | Closing interface! ".format(Constants.applicationName),
				Constants.loggingSeparators,
				"{0} | Session ended at: {1}".format(Constants.applicationName, time.strftime('%X - %x')),
				Constants.loggingSeparators)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def showProcessing(message=unicode()):
	"""
	This decorator is used for a processing operation.
	
	:param message: Operation description. ( String )
	:return: Object. ( Object )
	"""

	def wrapper(object):
		"""
		This decorator is used for a processing operation.

		:param object: Object to decorate. ( Object )
		:return: Object. ( Object )
		"""

		@functools.wraps(object)
		def function(*args, **kwargs):
			"""
			This decorator is used for a processing operation.

			:param \*args: Arguments. ( \* )
			:param \*\*kwargs: Keywords arguments. ( \*\* )
			"""

			RuntimeGlobals.engine.startProcessing(message, warning=False)
			try:
				return object(*args, **kwargs)
			finally:
				RuntimeGlobals.engine.stopProcessing(warning=False)
		return function
	return wrapper

def encapsulateProcessing(object):
	"""
	This decorator is used to encapsulate a processing operation.

	:param object: Object to decorate. ( Object )
	:return: Object. ( Object )
	"""

	@functools.wraps(object)
	def function(*args, **kwargs):
		"""
		This decorator is used to encapsulate a processing operation.

		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		RuntimeGlobals.engine._Umbra__storeProcessingState()
		RuntimeGlobals.engine.stopProcessing(warning=False)
		try:
			return object(*args, **kwargs)
		finally:
			RuntimeGlobals.engine.stopProcessing(warning=False)
			RuntimeGlobals.engine._Umbra__restoreProcessingState()
	return function

class Umbra(foundations.ui.common.QWidgetFactory(uiFile=RuntimeGlobals.uiFile)):
	"""
	This class is the main class of the **Umbra** package.
	"""

	# Custom signals definitions.
	verbosityLevelChanged = pyqtSignal(int)
	"""
	This signal is emited by the :class:`Umbra` class when the current verbosity level has changed. ( pyqtSignal )

	:return: Current verbosity level. ( Integer )	
	"""

	contentDropped = pyqtSignal(QEvent)
	"""
	This signal is emited by the :class:`Umbra` class when it receives dropped content. ( pyqtSignal )

	:return: Event. ( QEvent )	
	"""

	sizeChanged = pyqtSignal(QEvent)
	"""
	This signal is emited by the :class:`Umbra` class when its size changes. ( pyqtSignal )

	:return: Event. ( QEvent )	
	"""

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiSystemExitExceptionHandler, False, Exception)
	def __init__(self,
				parent=None,
				componentsPaths=None,
				requisiteComponents=None,
				visibleComponents=None,
				*args,
				**kwargs):
		"""
		This method initializes the class.

		:param componentsPaths: Components componentsPaths. ( Tuple / List )
		:param requisiteComponents: Requisite components names. ( Tuple / List )
		:param visibleComponents: Visible components names. ( Tuple / List )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Running pre initialisation method. ---
		hasattr(self, "onPreInitialisation") and self.onPreInitialisation()

		super(Umbra, self).__init__(parent, *args, **kwargs)

		# Engine binding to global variable.
		RuntimeGlobals.engine = self

		# --- Setting class attributes. ---
		self.__componentsPaths = componentsPaths or []
		self.__requisiteComponents = requisiteComponents or []
		self.__visibleComponents = visibleComponents or []

		self.__timer = None
		self.__requestsStack = RuntimeGlobals.requestsStack
		self.__patchesManager = RuntimeGlobals.patchesManager
		self.__componentsManager = None
		self.__actionsManager = None
		self.__fileSystemEventsManager = None
		self.__notificationsManager = None
		self.__layoutsManager = None
		self.__userApplicationDataDirectory = RuntimeGlobals.userApplicationDataDirectory
		self.__loggingSessionHandler = RuntimeGlobals.loggingSessionHandler
		self.__loggingFileHandler = RuntimeGlobals.loggingFileHandler
		self.__loggingConsoleHandler = RuntimeGlobals.loggingConsoleHandler
		self.__loggingSessionHandlerStream = RuntimeGlobals.loggingSessionHandlerStream
		self.__loggingActiveFormatter = RuntimeGlobals.loggingActiveFormatter
		self.__settings = RuntimeGlobals.settings
		self.__verbosityLevel = RuntimeGlobals.verbosityLevel
		self.__parameters = RuntimeGlobals.parameters
		self.__arguments = RuntimeGlobals.arguments
		self.__workerThreads = []
		self.__isProcessing = False
		self.__locals = {}

		self.__processingState = None

		# --- Initializing Application timer. ---
		self.__timer = QTimer(self)
		self.__timer.start(Constants.defaultTimerCycle)

		# --- Initializing Application. ---
		RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.setMessage(
		"{0} - {1} | Initializing interface.".format(self.__class__.__name__, Constants.releaseVersion),
		textColor=Qt.white,
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
		self.setWindowTitle("{0} - {1}".format(Constants.applicationName, Constants.releaseVersion))
		self.toolBar = Application_QToolBar(self)
		self.addToolBar(self.toolBar)

		# Setting processing widget.
		self.Application_Progress_Status_processing = Processing(self, Qt.Window)
		self.statusBar.addPermanentWidget(self.Application_Progress_Status_processing)
		self.Application_Progress_Status_processing.hide()

		# --- Initializing the Components Manager. ---
		RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.setMessage(
		"{0} - {1} | Initializing Components manager.".format(self.__class__.__name__, Constants.releaseVersion),
		textColor=Qt.white,
		waitTime=0.25)

		self.__componentsManager = RuntimeGlobals.componentsManager = Manager(componentsPaths)
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
		if RuntimeGlobals.splashscreen:
			RuntimeGlobals.splashscreen.setMessage("{0} - {1} | Initialization done.".format(
			self.__class__.__name__, Constants.releaseVersion),
			textColor=Qt.white)
			RuntimeGlobals.splashscreen.hide()

		# --- Running onStartup components methods. ---
		for component in self.__componentsManager.listComponents():
			try:
				interface = self.__componentsManager.getInterface(component)
				if not interface:
					continue

				if interface.activated:
					hasattr(interface, "onStartup") and interface.onStartup()
			except Exception as error:
				RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.hide()
				umbra.ui.common.uiExtendedExceptionHandler(
				Exception("'{0}' Component 'onStartup' method raised an exception, unexpected behavior may occur!\n\
Exception raised: {1}".format(component, error)), self.__class__.__name__)

		self.__layoutsManager.restoreStartupLayout()

		# --- Running post initialisation method. ---
		hasattr(self, "onPostInitialisation") and self.onPostInitialisation()

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def timer(self):
		"""
		This method is the property for **self.__timer** attribute.

		:return: self.__timer. ( QTimer )
		"""

		return self.__timer

	@timer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self, value):
		"""
		This method is the setter method for **self.__timer** attribute.

		:param value: Attribute value. ( QTimer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "timer"))

	@timer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self):
		"""
		This method is the deleter method for **self.__timer** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "timer"))

	@property
	def requestsStack(self):
		"""
		This method is the property for **self.__requestsStack** attribute.

		:return: self.__requestsStack. ( collections.deque )
		"""

		return self.__requestsStack

	@requestsStack.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def requestsStack(self, value):
		"""
		This method is the setter method for **self.__requestsStack** attribute.

		:param value: Attribute value. ( collections.deque )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "requestsStack"))

	@requestsStack.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def requestsStack(self):
		"""
		This method is the deleter method for **self.__requestsStack** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "requestsStack"))

	@property
	def componentsPaths(self):
		"""
		This method is the property for **self.__componentsPaths** attribute.

		:return: self.__componentsPaths. ( Tuple / List )
		"""

		return self.__componentsPaths

	@componentsPaths.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsPaths(self, value):
		"""
		This method is the setter method for **self.__componentsPaths** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "componentsPaths"))

	@componentsPaths.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsPaths(self):
		"""
		This method is the deleter method for **self.__componentsPaths** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "componentsPaths"))

	@property
	def requisiteComponents(self):
		"""
		This method is the property for **self.__requisiteComponents** attribute.

		:return: self.__requisiteComponents. ( Tuple / List )
		"""

		return self.__requisiteComponents

	@requisiteComponents.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def requisiteComponents(self, value):
		"""
		This method is the setter method for **self.__requisiteComponents** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "requisiteComponents"))

	@requisiteComponents.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def requisiteComponents(self):
		"""
		This method is the deleter method for **self.__requisiteComponents** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "requisiteComponents"))

	@property
	def visibleComponents(self):
		"""
		This method is the property for **self.__visibleComponents** attribute.

		:return: self.__visibleComponents. ( Tuple / List )
		"""

		return self.__visibleComponents

	@visibleComponents.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def visibleComponents(self, value):
		"""
		This method is the setter method for **self.__visibleComponents** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		if value is not None:
			assert type(value) in (tuple, list), "'{0}' attribute: '{1}' type is not 'tuple' or 'list'!".format(
			"visibleComponents", value)
			for element in value:
				assert type(element) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
				"visibleComponents", element)
		self.__visibleComponents = value

	@visibleComponents.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def visibleComponents(self):
		"""
		This method is the deleter method for **self.__visibleComponents** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "visibleComponents"))

	@property
	def patchesManager(self):
		"""
		This method is the property for **self.__patchesManager** attribute.

		:return: self.__patchesManager. ( ActionsManager )
		"""

		return self.__patchesManager

	@patchesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def patchesManager(self, value):
		"""
		This method is the setter method for **self.__patchesManager** attribute.

		:param value: Attribute value. ( ActionsManager )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "patchesManager"))

	@patchesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def patchesManager(self):
		"""
		This method is the deleter method for **self.__patchesManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "patchesManager"))

	@property
	def componentsManager(self):
		"""
		This method is the property for **self.__componentsManager** attribute.

		:return: self.__componentsManager. ( ComponentsManager )
		"""

		return self.__componentsManager

	@componentsManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsManager(self, value):
		"""
		This method is the setter method for **self.__componentsManager** attribute.

		:param value: Attribute value. ( ComponentsManager )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "componentsManager"))

	@componentsManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsManager(self):
		"""
		This method is the deleter method for **self.__componentsManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "componentsManager"))

	@property
	def notificationsManager(self):
		"""
		This method is the property for **self.__notificationsManager** attribute.

		:return: self.__notificationsManager. ( NotificationsManager )
		"""

		return self.__notificationsManager

	@notificationsManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def notificationsManager(self, value):
		"""
		This method is the setter method for **self.__notificationsManager** attribute.

		:param value: Attribute value. ( NotificationsManager )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "notificationsManager"))

	@notificationsManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def notificationsManager(self):
		"""
		This method is the deleter method for **self.__notificationsManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "notificationsManager"))

	@property
	def actionsManager(self):
		"""
		This method is the property for **self.__actionsManager** attribute.

		:return: self.__actionsManager. ( ActionsManager )
		"""

		return self.__actionsManager

	@actionsManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def actionsManager(self, value):
		"""
		This method is the setter method for **self.__actionsManager** attribute.

		:param value: Attribute value. ( ActionsManager )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "actionsManager"))

	@actionsManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def actionsManager(self):
		"""
		This method is the deleter method for **self.__actionsManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "actionsManager"))
	@property
	def fileSystemEventsManager(self):
		"""
		This method is the property for **self.__fileSystemEventsManager** attribute.

		:return: self.__fileSystemEventsManager. ( FileSystemEventsManager )
		"""

		return self.__fileSystemEventsManager

	@fileSystemEventsManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def fileSystemEventsManager(self, value):
		"""
		This method is the setter method for **self.__fileSystemEventsManager** attribute.

		:param value: Attribute value. ( FileSystemEventsManager )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "fileSystemEventsManager"))

	@fileSystemEventsManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def fileSystemEventsManager(self):
		"""
		This method is the deleter method for **self.__fileSystemEventsManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "fileSystemEventsManager"))

	@property
	def layoutsManager(self):
		"""
		This method is the property for **self.__layoutsManager** attribute.

		:return: self.__layoutsManager. ( LayoutsManager )
		"""

		return self.__layoutsManager

	@layoutsManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def layoutsManager(self, value):
		"""
		This method is the setter method for **self.__layoutsManager** attribute.

		:param value: Attribute value. ( LayoutsManager )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "layoutsManager"))

	@layoutsManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def layoutsManager(self):
		"""
		This method is the deleter method for **self.__layoutsManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "layoutsManager"))

	@property
	def userApplicationDataDirectory(self):
		"""
		This method is the property for **self.__userApplicationDataDirectory** attribute.

		:return: self.__userApplicationDataDirectory. ( String )
		"""

		return self.__userApplicationDataDirectory

	@userApplicationDataDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def userApplicationDataDirectory(self, value):
		"""
		This method is the setter method for **self.__userApplicationDataDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "userApplicationDataDirectory"))

	@userApplicationDataDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def userApplicationDataDirectory(self):
		"""
		This method is the deleter method for **self.__userApplicationDataDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "userApplicationDataDirectory"))

	@property
	def loggingSessionHandler(self):
		"""
		This method is the property for **self.__loggingSessionHandler** attribute.

		:return: self.__loggingSessionHandler. ( Handler )
		"""

		return self.__loggingSessionHandler

	@loggingSessionHandler.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingSessionHandler(self, value):
		"""
		This method is the setter method for **self.__loggingSessionHandler** attribute.

		:param value: Attribute value. ( Handler )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "loggingSessionHandler"))

	@loggingSessionHandler.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingSessionHandler(self):
		"""
		This method is the deleter method for **self.__loggingSessionHandler** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "loggingSessionHandler"))

	@property
	def loggingFileHandler(self):
		"""
		This method is the property for **self.__loggingFileHandler** attribute.

		:return: self.__loggingFileHandler. ( Handler )
		"""

		return self.__loggingFileHandler

	@loggingFileHandler.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingFileHandler(self, value):
		"""
		This method is the setter method for **self.__loggingFileHandler** attribute.

		:param value: Attribute value. ( Handler )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "loggingFileHandler"))

	@loggingFileHandler.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingFileHandler(self):
		"""
		This method is the deleter method for **self.__loggingFileHandler** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "loggingFileHandler"))

	@property
	def loggingConsoleHandler(self):
		"""
		This method is the property for **self.__loggingConsoleHandler** attribute.

		:return: self.__loggingConsoleHandler. ( Handler )
		"""

		return self.__loggingConsoleHandler

	@loggingConsoleHandler.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingConsoleHandler(self, value):
		"""
		This method is the setter method for **self.__loggingConsoleHandler** attribute.

		:param value: Attribute value. ( Handler )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "loggingConsoleHandler"))

	@loggingConsoleHandler.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingConsoleHandler(self):
		"""
		This method is the deleter method for **self.__loggingConsoleHandler** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "loggingConsoleHandler"))

	@property
	def loggingSessionHandlerStream(self):
		"""
		This method is the property for **self.__loggingSessionHandlerStream** attribute.

		:return: self.__loggingSessionHandlerStream. ( StreamObject )
		"""

		return self.__loggingSessionHandlerStream

	@loggingSessionHandlerStream.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingSessionHandlerStream(self, value):
		"""
		This method is the setter method for **self.__loggingSessionHandlerStream** attribute.

		:param value: Attribute value. ( StreamObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "loggingSessionHandlerStream"))

	@loggingSessionHandlerStream.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def loggingSessionHandlerStream(self):
		"""
		This method is the deleter method for **self.__loggingSessionHandlerStream** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "loggingSessionHandlerStream"))

	@property
	def settings(self):
		"""
		This method is the property for **self.__settings** attribute.

		:return: self.__settings. ( QSettings )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This method is the setter method for **self.__settings** attribute.

		:param value: Attribute value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This method is the deleter method for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def verbosityLevel(self):
		"""
		This method is the property for **self.__verbosityLevel** attribute.

		:return: self.__verbosityLevel. ( Integer )
		"""

		return self.__verbosityLevel

	@verbosityLevel.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def verbosityLevel(self, value):
		"""
		This method is the setter method for **self.__verbosityLevel** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("verbosityLevel", value)
			assert value >= 0 and value <= 4, "'{0}' attribute: Value need to be exactly beetween 0 and 4!".format(
			"verbosityLevel")
		self.__verbosityLevel = value

	@verbosityLevel.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def verbosityLevel(self):
		"""
		This method is the deleter method for **self.__verbosityLevel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "verbosityLevel"))

	@property
	def parameters(self):
		"""
		This method is the property for **self.__parameters** attribute.

		:return: self.__parameters. ( Object )
		"""

		return self.__parameters

	@parameters.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def parameters(self, value):
		"""
		This method is the setter method for **self.__parameters** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "parameters"))

	@parameters.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def parameters(self):
		"""
		This method is the deleter method for **self.__parameters** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "parameters"))

	@property
	def arguments(self):
		"""
		This method is the property for **self.__arguments** attribute.

		:return: self.__arguments. ( List )
		"""

		return self.__arguments

	@arguments.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def arguments(self, value):
		"""
		This method is the setter method for **self.__arguments** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "arguments"))

	@arguments.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def arguments(self):
		"""
		This method is the deleter method for **self.__arguments** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "arguments"))

	@property
	def workerThreads(self):
		"""
		This method is the property for **self.__workerThreads** attribute.

		:return: self.__workerThreads. ( List )
		"""

		return self.__workerThreads

	@workerThreads.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def workerThreads(self, value):
		"""
		This method is the setter method for **self.__workerThreads** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "workerThreads"))

	@workerThreads.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def workerThreads(self):
		"""
		This method is the deleter method for **self.__workerThreads** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "workerThreads"))

	@property
	def isProcessing(self):
		"""
		This method is the property for **self.__isProcessing** attribute.

		:return: self.__isProcessing. ( Boolean )
		"""

		return self.__isProcessing

	@isProcessing.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def isProcessing(self, value):
		"""
		This method is the setter method for **self.__isProcessing** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "isProcessing"))

	@isProcessing.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def isProcessing(self):
		"""
		This method is the deleter method for **self.__isProcessing** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "isProcessing"))

	@property
	def locals(self):
		"""
		This method is the property for **self.__locals** attribute.

		:return: self.__locals. ( Dictionary )
		"""

		return self.__locals

	@locals.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def locals(self, value):
		"""
		This method is the setter method for **self.__locals** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "locals"))

	@locals.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def locals(self):
		"""
		This method is the deleter method for **self.__locals** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "locals"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def dragEnterEvent(self, event):
		"""
		This method reimplements the :meth:`QWidget.dragEnterEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		LOGGER.debug("> Application drag enter event accepted!")
		event.accept()

	@core.executionTrace
	def dragMoveEvent(self, event):
		"""
		This method reimplements the :meth:`QWidget.dragMoveEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		LOGGER.debug("> Application drag move event accepted!")
		event.accept()

	@core.executionTrace
	def dropEvent(self, event):
		"""
		This method reimplements the :meth:`QWidget.dropEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		LOGGER.debug("> Application drop event accepted!")
		self.contentDropped.emit(event)

	@core.executionTrace
	def show(self):
		"""
		This method reimplements the :meth:`QWidget.show` method.
		"""

		super(Umbra, self).show(setGeometry=False)

	@core.executionTrace
	def closeEvent(self, event):
		"""
		This method reimplements the :meth:`QWidget.closeEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		self.quit(event=event)

	@core.executionTrace
	def resizeEvent(self, event):
		"""
		This method reimplements the :meth:`QWidget.resizeEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		LOGGER.debug("> Application resize event accepted!")
		self.sizeChanged.emit(event)
		event.accept()

	@core.executionTrace
	def __setComponents(self, requisite=True):
		"""
		This method sets the Components.

		:param requisite: Set only requisite Components. ( Boolean )
		"""

		attribute = "intersection" if requisite else "difference"
		components = list(getattr(set(self.__componentsManager.listComponents()), attribute)(self.__requisiteComponents))
		deactivatedComponents = self.__settings.getKey("Settings", "deactivatedComponents").toString().split(",")
		components = filter(lambda x: x not in deactivatedComponents, components)

		for component in components:
			try:
				profile = self.__componentsManager.components[component]
				interface = self.__componentsManager.getInterface(component)

				setattr(self, "_{0}__{1}".format(self.__class__.__name__, foundations.namespace.getLeaf(component, ".")),
																											interface)

				RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.setMessage(
				"{0} - {1} | Activating {2}.".format(self.__class__.__name__, Constants.releaseVersion, component),
				textColor=Qt.white)
				interface.activate(self)
				if profile.category in ("Default", "QObject"):
					interface.initialize()
				elif profile.category == "QWidget":
					interface.addWidget()
					interface.initializeUi()
			except Exception as error:
				RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.hide()

				exceptionHandler = umbra.ui.common.uiSystemExitExceptionHandler if requisite else \
				umbra.ui.common.uiExtendedExceptionHandler

				message = "'{0}' Component failed to activate!\nException raised: {1}" if requisite else \
				"'{0}' Component failed to activate, unexpected behavior may occur!\nException raised: {1}"

				exceptionHandler(manager.exceptions.ComponentActivationError(message.format(component, error)),
																							self.__class__.__name__)

	@core.executionTrace
	def __setLocals(self):
		"""
		This method sets the locals for the requestsStack.
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

	# @core.executionTrace
	def __processRequestsStack(self):
		"""
		This method process the requests stack.
		"""

		while self.__requestsStack:
			try:
				exec self.__requestsStack.popleft() in self.__locals
			except Exception as error:
				umbra.ui.common.notifyExceptionHandler(error, core.getTraceName(self.__processRequestsStack))

	@core.executionTrace
	def __componentsInstantiationCallback(self, profile):
		"""
		This method is a callback for Components instantiation.

		:param profile: Component Profile. ( Profile )
		"""

		RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.setMessage(
		"{0} - {1} | Instantiating {2} Component.".format(self.__class__.__name__, Constants.releaseVersion, profile.name),
		textColor=Qt.white)

	def __storeProcessingState(self):
		"""
		This method stores the processing state.
		"""

		steps = self.Application_Progress_Status_processing.Processing_progressBar.maximum()
		value = self.Application_Progress_Status_processing.Processing_progressBar.value()
		message = self.Application_Progress_Status_processing.Processing_label.text()
		state = self.__isProcessing

		self.__processingState = steps, value, message, state

	def __restoreProcessingState(self):
		"""
		This method restores the processing state.
		"""

		steps, value, message, state = self.__processingState

		self.Application_Progress_Status_processing.Processing_progressBar.setRange(0, steps)
		self.Application_Progress_Status_processing.Processing_progressBar.setValue(value)
		self.setProcessingMessage(message, warning=False)
		self.__isProcessing = state
		state and self.Application_Progress_Status_processing.show()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def setVerbosityLevel(self, verbosityLevel):
		"""
		This method sets the Application verbosity level.
		
		:param verbosityLevel: Verbosity level. ( Integer )
		:return: Method success. ( Boolean )
		
		:note: The expected verbosity level value is an integer between 0 to 4.
		"""

		self.__verbosityLevel = verbosityLevel
		core.setVerbosityLevel(verbosityLevel)
		self.__settings.setKey("Settings", "verbosityLevel", verbosityLevel)
		self.verbosityLevelChanged.emit(verbosityLevel)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
	def setVisualStyle(self, fullScreenStyle=False):
		"""
		This method sets the Application visual style.
		
		:param fullScreenStyle: Use fullscreen stylesheet file. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Setting Application visual style.")
		platformStyles = {"Windows":(("Windows", "Microsoft"),
		 							UiConstants.windowsStyle,
									UiConstants.windowsStylesheetFile,
									UiConstants.windowsFullScreenStylesheetFile),
						"Darwin":(("Darwin",),
								UiConstants.darwinStyle,
								UiConstants.darwinStylesheetFile,
								UiConstants.darwinFullScreenStylesheetFile),
						"Linux":(("Linux",),
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
				styleSheetFile = io.File(styleSheetPath)
				break

		if not styleSheetFile:
			raise foundations.exceptions.FileExistsError(
			"{0} | No stylesheet file found, visual style will not be applied!".format(self.__class__.__name__))

		if foundations.common.pathExists(styleSheetFile.file):
			LOGGER.debug("> Reading style sheet file: '{0}'.".format(styleSheetFile.file))
			styleSheetFile.read()
			for i, line in enumerate(styleSheetFile.content):
				search = re.search(r"url\((?P<url>.*)\)", line)
				if not search:
					continue

				styleSheetFile.content[i] = line.replace(search.group("url"),
				strings.toForwardSlashes(umbra.ui.common.getResourcePath(search.group("url"))))
			RuntimeGlobals.application.setStyleSheet(QString("".join(styleSheetFile.content)))
			return True
		else:
			raise foundations.exceptions.FileExistsError(
			"{0} | '{1}' stylesheet file is not available, visual style will not be applied!".format(
			self.__class__.__name__, styleSheetFile.file))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def isFullScreen(self):
		"""
		This method returns if Application is in fullscreen state.

		:return: FullScreen state. ( Boolean )
		"""

		return self.windowState().__int__() == 4 and True or False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def toggleFullScreen(self, *args):
		"""
		This method toggles Application fullscreen state.

		:param \*args: Arguments. ( \* )
		:return: Method success. ( Boolean )
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

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def processEvents(self, flags=QEventLoop.AllEvents):
		"""
		This method process Application events.

		:param flags: Events flags. ( Integer )
		:return: Method success. ( Boolean )
		"""

		QApplication.processEvents(flags)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setProcessingMessage(self, message, warning=True):
		"""
		This method sets the processing operation message.

		:param message: Operation description. ( String )
		:param warning: Emit warning message. ( Integer )
		:return: Method success. ( Boolean )
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

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def startProcessing(self, message, steps=0, warning=True):
		"""
		This method registers the start of a processing operation.

		:param message: Operation description. ( String )
		:param steps: Operation steps. ( Integer )
		:param warning: Emit warning message. ( Integer )
		:return: Method success. ( Boolean )
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

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def stepProcessing(self, warning=True):
		"""
		This method steps the processing operation progress indicator.

		:param warning: Emit warning message. ( Integer )
		:return: Method success. ( Boolean )
		"""

		if not self.__isProcessing:
			warning and	LOGGER.warning(
			"!> {0} | Engine is not processing, 'stepProcessing' request has been ignored!".format(
			self.__class__.__name__))
			return False

		LOGGER.debug("> Stepping processing operation!")

		self.Application_Progress_Status_processing.Processing_progressBar.setValue(
		self.Application_Progress_Status_processing.Processing_progressBar.value() + 1)
		self.processEvents()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def stopProcessing(self, warning=True):
		"""
		This method registers the end of a processing operation.

		:param warning: Emit warning message. ( Integer )
		:return: Method success. ( Boolean )
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
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def garbageCollect(self):
		"""
		This method triggers the garbage collecting.

		:return: Number of unreachable objects found. ( Integer )
		"""

		LOGGER.debug("> Garbage collecting!")

		return gc.collect()

	@core.executionTrace
	def quit(self, exitCode=0, event=None):
		"""
		This method quits the Application.

		:param exitCode: Exit code. ( Integer )
		:param event: QEvent. ( QEvent )
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

		core.removeLoggingHandler(LOGGER, self.__loggingFileHandler)
		core.removeLoggingHandler(LOGGER, self.__loggingSessionHandler)
		# core.removeLoggingHandler(LOGGER, self.__loggingConsoleHandler)

		# Stopping the Application timer.
		self.__timer.stop()
		self.__timer = None

		self.deleteLater()
		event and event.accept()

		exit(exitCode)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiSystemExitExceptionHandler, False, OSError)
def setUserApplicationDataDirectory(path):
	"""
	This definition sets the Application data directory.

	:param path: Starting point for the directories tree creation. ( String )
	:return: Definition success. ( Boolean )
	"""

	userApplicationDataDirectory = RuntimeGlobals.userApplicationDataDirectory

	LOGGER.debug("> Current Application data directory '{0}'.".format(userApplicationDataDirectory))
	if io.setDirectory(userApplicationDataDirectory):
		for directory in Constants.preferencesDirectories:
			if not io.setDirectory(os.path.join(userApplicationDataDirectory, directory)):
				raise OSError("{0} | '{1}' directory creation failed , '{2}' will now close!".format(
				inspect.getmodulename(__file__), os.path.join(userApplicationDataDirectory, directory),
															Constants.applicationName))
		return True
	else:
		raise OSError("{0} | '{1}' directory creation failed , '{2}' will now close!".format(
		inspect.getmodulename(__file__), userApplicationDataDirectory, Constants.applicationName))

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getCommandLineParametersParser():
	"""
	This definition returns the command line parameters parser.

	:return: Parser. ( Parser )
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
					dest="loggingFormater",
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
	parser.add_option("-t",
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
					help="'Execute provided startup script'.")
	return parser

@core.executionTrace
@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiSystemExitExceptionHandler,
										False,
										umbra.exceptions.EngineConfigurationError)
def run(engine, parameters, componentsPaths=None, requisiteComponents=None, visibleComponents=None):
	"""
	This definition starts the Application.

	:param engine: Engine. ( QObject )
	:param parameters: Command line parameters. ( Tuple )
	:param componentsPaths: Components componentsPaths. ( Tuple / List )
	:param requisiteComponents: Requisite components names. ( Tuple / List )
	:param visibleComponents: Visible components names. ( Tuple / List )
	:return: Definition success. ( Boolean )
	"""

	# Command line parameters handling.
	RuntimeGlobals.parameters, RuntimeGlobals.arguments = parameters

	if RuntimeGlobals.parameters.about:
		for line in SESSION_HEADER_TEXT:
			sys.stdout.write("{0}\n".format(line))
		core.exit(1)

	# Redirecting standard output and error messages.
	sys.stdout = core.StandardMessageHook(LOGGER)
	sys.stderr = core.StandardMessageHook(LOGGER)

	# Setting application verbose level.
	LOGGER.setLevel(logging.DEBUG)

	# Setting user application data directory.
	if RuntimeGlobals.parameters.userApplicationDataDirectory:
		RuntimeGlobals.userApplicationDataDirectory = RuntimeGlobals.parameters.userApplicationDataDirectory
	else:
		RuntimeGlobals.userApplicationDataDirectory = foundations.environment.getUserApplicationDataDirectory()

	if not setUserApplicationDataDirectory(RuntimeGlobals.userApplicationDataDirectory):
		raise umbra.exceptions.EngineConfigurationError(
		"{0} | '{1}' user Application data directory is not available, '{2}' will now close!".format(
		inspect.getmodulename(__file__), RuntimeGlobals.userApplicationDataDirectory, Constants.applicationName))

	LOGGER.debug("> Application Python interpreter: '{0}'".format(sys.executable))
	LOGGER.debug("> Application startup location: '{0}'".format(os.getcwd()))
	LOGGER.debug("> Session user Application data directory: '{0}'".format(RuntimeGlobals.userApplicationDataDirectory))

	# Getting the logging file path.
	RuntimeGlobals.loggingFile = os.path.join(RuntimeGlobals.userApplicationDataDirectory,
											Constants.loggingDirectory,
											Constants.loggingFile)

	try:
		foundations.common.pathExists(RuntimeGlobals.loggingFile) and os.remove(RuntimeGlobals.loggingFile)
	except:
		raise umbra.exceptions.EngineConfigurationError(
		"{0} | '{1}' Logging file is currently locked by another process, '{2}' will now close!".format(
		inspect.getmodulename(__file__), RuntimeGlobals.loggingFile, Constants.applicationName))

	try:
		RuntimeGlobals.loggingFileHandler = logging.FileHandler(RuntimeGlobals.loggingFile)
		RuntimeGlobals.loggingFileHandler.setFormatter(RuntimeGlobals.loggingFormatters[Constants.loggingDefaultFormatter])
		LOGGER.addHandler(RuntimeGlobals.loggingFileHandler)
	except:
		raise umbra.exceptions.EngineConfigurationError(
		"{0} | '{1}' Logging file is not available, '{2}' will now close!".format(inspect.getmodulename(__file__),
																				RuntimeGlobals.loggingFile,
																				Constants.applicationName))

	# Getting the patches file path.
	RuntimeGlobals.patchesFile = os.path.join(RuntimeGlobals.userApplicationDataDirectory,
											Constants.patchesDirectory,
											Constants.patchesFile)
	# Initializing the patches manager.
	RuntimeGlobals.patchesManager = umbra.managers.patchesManager.PatchesManager(RuntimeGlobals.patchesFile,
																		[os.path.join(path, Constants.patchesDirectory)
																		for path in RuntimeGlobals.resourcesDirectories])
	RuntimeGlobals.patchesManager.registerPatches() and RuntimeGlobals.patchesManager.applyPatches()

	# Retrieving settings file.
	LOGGER.debug("> Initializing '{0}'!".format(Constants.applicationName))
	RuntimeGlobals.settingsFile = os.path.join(RuntimeGlobals.userApplicationDataDirectory,
												Constants.settingsDirectory,
												Constants.settingsFile)

	RuntimeGlobals.settings = Preferences(RuntimeGlobals.settingsFile)

	LOGGER.debug("> Retrieving default layouts.")
	RuntimeGlobals.settings.setDefaultLayouts(("startupCentric",))

	foundations.common.pathExists(RuntimeGlobals.settingsFile) or RuntimeGlobals.settings.setDefaultPreferences()

	LOGGER.debug("> Retrieving stored verbose level.")
	RuntimeGlobals.verbosityLevel = RuntimeGlobals.parameters.verbosityLevel and \
	RuntimeGlobals.parameters.verbosityLevel or \
	foundations.common.getFirstItem(RuntimeGlobals.settings.getKey("Settings", "verbosityLevel").toInt())
	LOGGER.debug("> Setting logger verbosity level to: '{0}'.".format(RuntimeGlobals.verbosityLevel))
	core.setVerbosityLevel(RuntimeGlobals.verbosityLevel)

	LOGGER.debug("> Retrieving stored logging formatter.")
	loggingFormatter = RuntimeGlobals.parameters.loggingFormater and RuntimeGlobals.parameters.loggingFormater or \
	strings.encode(RuntimeGlobals.settings.getKey("Settings", "loggingFormatter").toString())
	loggingFormatter = loggingFormatter in RuntimeGlobals.loggingFormatters and loggingFormatter or None
	RuntimeGlobals.loggingActiveFormatter = loggingFormatter and loggingFormatter or Constants.loggingDefaultFormatter
	LOGGER.debug("> Setting logging formatter: '{0}'.".format(RuntimeGlobals.loggingActiveFormatter))
	for handler in (RuntimeGlobals.loggingConsoleHandler, RuntimeGlobals.loggingFileHandler):
		handler and handler.setFormatter(RuntimeGlobals.loggingFormatters[RuntimeGlobals.loggingActiveFormatter])

	# Starting the session handler.
	RuntimeGlobals.loggingSessionHandlerStream = StreamObject()
	RuntimeGlobals.loggingSessionHandler = logging.StreamHandler(RuntimeGlobals.loggingSessionHandlerStream)
	RuntimeGlobals.loggingSessionHandler.setFormatter(
	RuntimeGlobals.loggingFormatters[RuntimeGlobals.loggingActiveFormatter])
	LOGGER.addHandler(RuntimeGlobals.loggingSessionHandler)

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
		RuntimeGlobals.splashscreen = Delayed_QSplashScreen(RuntimeGlobals.splashscreenImage)
		RuntimeGlobals.splashscreen.setMessage(
		"{0} - {1} | Initializing {0}.".format(Constants.applicationName, Constants.releaseVersion),
		textColor=Qt.white)
		RuntimeGlobals.splashscreen.show()

	# Initializing requests stack.
	RuntimeGlobals.requestsStack = collections.deque()

	# Initializing engine.
	RuntimeGlobals.engine = engine(None, componentsPaths, requisiteComponents, visibleComponents)
	RuntimeGlobals.engine.show()
	RuntimeGlobals.engine.raise_()

	return sys.exit(RuntimeGlobals.application.exec_())

@core.executionTrace
def exit(exitCode=0):
	"""
	This definition exits the Application.
	
	:param exitCode: Exit code. ( Integer )
	"""

	for line in SESSION_FOOTER_TEXT:
		LOGGER.info(line)

	core.removeLoggingHandler(LOGGER, RuntimeGlobals.loggingConsoleHandler)

	RuntimeGlobals.application.exit(exitCode)
