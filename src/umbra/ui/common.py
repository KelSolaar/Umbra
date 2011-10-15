#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**common.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines common ui manipulation related objects.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import functools
import inspect
import logging
import os
import platform
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
import umbra.exceptions
import umbra.ui.widgets.messageBox as messageBox
from foundations.parsers import SectionsFileParser
from umbra.globals.constants import Constants
from umbra.globals.uiConstants import UiConstants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"LayoutActiveLabel",
			"Icon",
			"uiExtendedExceptionHandler",
			"uiStandaloneExtendedExceptionHandler",
			"uiBasicExceptionHandler",
			"uiStandaloneBasicExceptionHandler",
			"uiSystemExitExceptionHandler",
			"uiStandaloneSystemExitExceptionHandler",
			"getResourcePath",
			"setWindowDefaultIcon",
			"centerWidgetOnScreen",
			"getTokensParser",
			"storeLastBrowsedPath",
			"parentsWalker"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class LayoutActiveLabel(core.Structure):
	"""
	This class represents a storage object for layout active labels attributes.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: name, object, layout, shortcut. ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

class Icon(core.Structure):
	"""
	This class represents a storage object for icon.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param kwargs: path ( Key / Value pairs )
		"""

		core.Structure.__init__(self, **kwargs)

@core.executionTrace
def uiExtendedExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui extended exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \* )
	"""

	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	messageBox.messageBox("Detailed Error", "Exception", "Exception in '{0}': {1}".format(origin, exception))

@core.executionTrace
def uiStandaloneExtendedExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui standalone extended exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \* )
	"""

	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	messageBox.standaloneMessageBox("Detailed Error", "Exception", "Exception in '{0}': {1}".format(origin, exception))

@core.executionTrace
def uiBasicExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui basic exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \* )
	"""

	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	messageBox.messageBox("Detailed Error", "Exception", "{0}".format(exception))

@core.executionTrace
def uiStandaloneBasicExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui standalone basic exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \* )
	"""

	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	messageBox.standaloneMessageBox("Detailed Error", "Exception", "{0}".format(exception))

@core.executionTrace
def uiSystemExitExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui system exit exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \* )
	"""

	uiExtendedExceptionHandler(exception, origin, *args, **kwargs)
	foundations.common.exit(1, LOGGER, [RuntimeGlobals.loggingSessionHandler, RuntimeGlobals.loggingFileHandler, RuntimeGlobals.loggingConsoleHandler])

@core.executionTrace
def uiStandaloneSystemExitExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui standalone system exit exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \* )
	"""

	uiStandaloneExtendedExceptionHandler(exception, origin, *args, **kwargs)
	foundations.common.exit(1, LOGGER, [RuntimeGlobals.loggingSessionHandler, RuntimeGlobals.loggingFileHandler, RuntimeGlobals.loggingConsoleHandler])

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, umbra.exceptions.ResourceExistsError)
def getResourcePath(name, raiseException=False):
	"""
	This definition returns the resource file path matching the provided name.

	:param name: Resource name. ( String )
	:param raiseException: Raise the exception. ( Boolean )
	:return: Resource path. ( String )
	"""

	for path in RuntimeGlobals.resourcesPaths:
		path = os.path.join(path, name)
		if os.path.exists(path):
			LOGGER.debug("> '{0}' resource path: '{1}'.".format(name, path))
			return path

	if raiseException:
		raise umbra.exceptions.ResourceExistsError("{0} | No resource file path found for '{0}' name!".format(inspect.getmodulename(__file__), name))

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def setWindowDefaultIcon(window):
	"""
	This method sets the Application icon to the provided window.

	:param window: Window. ( QWidget )
	:return: Definition success. ( Boolean )
	"""

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		window.setWindowIcon(QIcon(getResourcePath(UiConstants.applicationWindowsIcon)))
	elif platform.system() == "Darwin":
		window.setWindowIcon(QIcon(getResourcePath(UiConstants.applicationDarwinIcon)))
	elif platform.system() == "Linux":
		pass
	return True

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def centerWidgetOnScreen(widget, screen=None):
	"""
	This definition centers the provided Widget middle of the screen.

	:param widget: Current Widget. ( QWidget )
	:param screen: Screen used for centering. ( Integer )
	:return: Definition success. ( Boolean )
	"""

	screen = screen and screen or QApplication.desktop().primaryScreen()
	desktopWidth = QApplication.desktop().screenGeometry(screen).width()
	desktopHeight = QApplication.desktop().screenGeometry(screen).height()
	widget.move(desktopWidth / 2 - widget.width() / 2, desktopHeight / 2 - widget.height() / 2)
	return True

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
def getTokensParser(tokensFile):
	"""
	This method returns a tokens sections file parser.

	:param tokensFile: Tokens file. ( String )
	:return: Tokens. ( SectionsFileParser )
	"""

	if not os.path.exists(tokensFile):
		raise foundations.exceptions.FileExistsError("{0} | '{1}' tokens file doesn't exists!".format(inspect.getmodulename(__file__), tokensFile))

	sectionsFileParser = SectionsFileParser(tokensFile)
	sectionsFileParser.read() and sectionsFileParser.parse(orderedDictionary=False)
	return sectionsFileParser

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def storeLastBrowsedPath(path):
	"""
	This definition is a wrapper method used to store the last browsed path.

	:param path: Provided path. ( QString )
	:return: Provided path. ( String )
	"""

	path = str(path)

	lastBrowsedPath = os.path.normpath(os.path.join(os.path.isfile(path) and os.path.dirname(path) or path, ".."))
	LOGGER.debug("> Storing last browsed path: '%s'.", lastBrowsedPath)

	RuntimeGlobals.lastBrowsedPath = lastBrowsedPath

	return path

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def parentsWalker(object):
	"""
	This definition is a generator used to retrieve the chain of parents of the provided :class:`QObject` instance.

	:param object: Provided path. ( QObject )
	:yield: Object parent. ( QObject )
	"""

	while object.parent():
		object = object.parent()
		yield object

def showWaitCursor(object):
	"""
	This decorator is used to show a wait cursor while processing.
	
	:param object: Object to decorate. ( Object )
	:return: Object. ( Object )
	"""

	@functools.wraps(object)
	def function(*args, **kwargs):
		"""
		This decorator is used to show a wait cursor while processing.

		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \* )
		:return: Object. ( Object )
		"""

		QApplication.setOverrideCursor(Qt.WaitCursor)
		try:
			value = object(*args, **kwargs)
		finally:
			QApplication.restoreOverrideCursor()
			return value

	return function
