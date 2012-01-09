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

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import inspect
import logging
import os
import platform
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QIcon

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
import umbra.exceptions
import umbra.ui.widgets.messageBox as messageBox
from foundations.parsers import SectionsFileParser
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals
from umbra.globals.uiConstants import UiConstants

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
			"Icon",
			"uiExtendedExceptionHandler",
			"uiBasicExceptionHandler",
			"uiSystemExitExceptionHandler",
			"notifyExceptionHandler",
			"getResourcePath",
			"setWindowDefaultIcon",
			"centerWidgetOnScreen",
			"getSectionsFileParser",
			"storeLastBrowsedPath",
			"parentsWalker"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Icon(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for icon.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param kwargs: path ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

@core.executionTrace
def uiExtendedExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui extended exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \*\* )
	"""

	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	messageBox.messageBox("Detailed Error", "Exception", "Exception in '{0}': {1}".format(origin, exception))

@core.executionTrace
def uiBasicExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui basic exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \*\* )
	"""

	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	messageBox.messageBox("Detailed Error", "Exception", "{0}".format(exception))

@core.executionTrace
def uiSystemExitExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui system exit exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \*\* )
	"""

	uiExtendedExceptionHandler(exception, origin, *args, **kwargs)
	foundations.common.exit(1)

@core.executionTrace
def notifyExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a notifier exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \*\* )
	"""

	callback = lambda: RuntimeGlobals.engine.restoreLayout(UiConstants.developmentLayout)
	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	RuntimeGlobals.notificationsManager.exceptify(message="{0}".format(exception), notificationClickedSlot=callback)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, umbra.exceptions.ResourceExistsError)
def getResourcePath(name, raiseException=False):
	"""
	This definition returns the resource file path matching the given name.

	:param name: Resource name. ( String )
	:param raiseException: Raise the exception. ( Boolean )
	:return: Resource path. ( String )
	"""

	for path in RuntimeGlobals.resourcesDirectories:
		path = os.path.join(path, name)
		if foundations.common.pathExists(path):
			LOGGER.debug("> '{0}' resource path: '{1}'.".format(name, path))
			return path

	if raiseException:
		raise umbra.exceptions.ResourceExistsError(
		"{0} | No resource file path found for '{0}' name!".format(inspect.getmodulename(__file__), name))

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def setWindowDefaultIcon(window):
	"""
	This method sets the default Application icon to the given window.

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
	This definition centers the given Widget on the screen.

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
def getSectionsFileParser(file):
	"""
	This method returns a sections file parser.

	:param file: File. ( String )
	:return: Parser. ( SectionsFileParser )
	"""

	if not foundations.common.pathExists(file):
		raise foundations.exceptions.FileExistsError("{0} | '{1}' sections file doesn't exists!".format(
		inspect.getmodulename(__file__), file))

	sectionsFileParser = SectionsFileParser(file)
	sectionsFileParser.read() and sectionsFileParser.parse()
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
	This definition is a generator used to retrieve the chain of parents of the given :class:`QObject` instance.

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
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		:return: Object. ( Object )
		"""

		QApplication.setOverrideCursor(Qt.WaitCursor)
		value = None
		try:
			value = object(*args, **kwargs)
		finally:
			QApplication.restoreOverrideCursor()
			return value

	return function
