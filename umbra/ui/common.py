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
import fnmatch
import functools
import inspect
import logging
import os
import platform
import re
from PyQt4.QtCore import QString
from PyQt4.QtCore import QStringList
from PyQt4.QtCore import QVariant
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
import foundations.strings as strings
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
			"Location",
			"parseLocation",
			"uiExtendedExceptionHandler",
			"uiBasicExceptionHandler",
			"uiSystemExitExceptionHandler",
			"notifyExceptionHandler",
			"getResourcePath",
			"setWindowDefaultIcon",
			"getSectionsFileParser",
			"storeLastBrowsedPath",
			"getQVariantAsString",
			"parentsWalker",
			"signalsBlocker",
			"showWaitCursor"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Location(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for the :class:`SearchInFiles` class location.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: directories, files, filtersIn, filtersOut, targets. ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

@core.executionTrace
def parseLocation(data):
	"""
	This definition parses given location data.

	:param data: Exception. ( Exception )
	:return: Location object. ( Location )
	"""

	tokens = data.split(",")
	location = Location(directories=[], files=[], filtersIn=[], filtersOut=[], targets=[])
	if not tokens:
		return location

	for token in tokens:
		token = token.strip()
		if not token:
			continue

		if foundations.common.pathExists(token):
			if os.path.isdir(token):
				location.directories.append(token)
			else:
				location.files.append(token)
		else:
			match = re.match("(?P<filterIn>\*\.\w+)", token)
			if match:
				location.filtersIn.append(fnmatch.translate(match.group("filterIn")))
				continue
			match = re.match("!(?P<filterOut>\*\.\w+)", token)
			if match:
				location.filtersOut.append(fnmatch.translate(match.group("filterOut")))
				continue
			match = re.match("\<(?P<target>[\w ]+)\>", token)
			if match:
				location.targets.append(match.group("target"))
				continue
	return location

@core.executionTrace
def uiExtendedExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui extended exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \*\* )
	:return: Definition success. ( Boolean )
	"""

	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	messageBox.messageBox("Detailed Error", "Exception", "Exception in '{0}': {1}".format(origin, exception))
	return True

@core.executionTrace
def uiBasicExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui basic exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \*\* )
	:return: Definition success. ( Boolean )
	"""

	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	messageBox.messageBox("Detailed Error", "Exception", "{0}".format(exception))
	return True

@core.executionTrace
def uiSystemExitExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a ui system exit exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \*\* )
	:return: Definition success. ( Boolean )
	"""

	uiExtendedExceptionHandler(exception, origin, *args, **kwargs)
	return core.exit(1)

@core.executionTrace
def notifyExceptionHandler(exception, origin, *args, **kwargs):
	"""
	This definition provides a notifier exception handler.

	:param exception: Exception. ( Exception )
	:param origin: Function / Method raising the exception. ( String )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \*\* )
	:return: Definition success. ( Boolean )
	"""

	callback = lambda: RuntimeGlobals.engine.layoutsManager.restoreLayout(UiConstants.developmentLayout)
	foundations.exceptions.defaultExceptionsHandler(exception, origin, *args, **kwargs)
	RuntimeGlobals.notificationsManager.exceptify(message="{0}".format(exception), notificationClickedSlot=callback)
	return True

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
		"{0} | No resource file path found for '{1}' name!".format(inspect.getmodulename(__file__), name))

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
@foundations.exceptions.exceptionsHandler(None, False, TypeError)
def storeLastBrowsedPath(data):
	"""
	This definition is a wrapper method used to store the last browsed path.

	:param data: Path data. ( QString / QList  )
	:return: Last browsed path. ( String )
	"""

	if type(data) in (tuple, list, QStringList):
		data = [strings.encode(path) for path in data]
		lastBrowsedPath = foundations.common.getFirstItem(data)
	elif type(data) in (str, unicode, QString):
		data = lastBrowsedPath = strings.encode(data)
	else:
		raise TypeError("{0} | '{1}' type is not supported!".format(
		inspect.getmodulename(__file__), type(data)))

	if foundations.common.pathExists(lastBrowsedPath):
		lastBrowsedPath = os.path.normpath(lastBrowsedPath)
		if os.path.isfile(lastBrowsedPath):
			lastBrowsedPath = os.path.dirname(lastBrowsedPath)

		LOGGER.debug("> Storing last browsed path: '%s'.", lastBrowsedPath)
		RuntimeGlobals.lastBrowsedPath = lastBrowsedPath
	return data

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getQVariantAsString(data):
	"""
	This definition returns given `QVariant <http://doc.qt.nokia.com/qvariant.html>`_ data as a string.

	:param data: Given dat. ( Object )
	:return: QVariant data as string. ( String )		
	"""

	if isinstance(data, QVariant):
		data = data.toString()

	data = QString(data)
	return strings.encode(data)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def parentsWalker(object):
	"""
	This definition is a generator used to retrieve the chain of parents of the given :class:`QObject` instance.

	:param object: Given path. ( QObject )
	:yield: Object parent. ( QObject )
	"""

	while object.parent():
		object = object.parent()
		yield object

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def signalsBlocker(instance, attribute, *args, **kwargs):
	"""
	This definition blocks given instance signals before calling the given attribute with \
	given arguments and then unblocks the signals.

	:param instance: Instance object. ( QObject )
	:param attribute: Attribute to call. ( QObject )
	:param \*args: Arguments. ( \* )
	:param \*\*kwargs: Keywords arguments. ( \*\* )
	:return: Object. ( Object )
	"""

	value = None
	try:
		hasattr(instance, "blockSignals") and instance.blockSignals(True)
		value = attribute(*args, **kwargs)
	finally:
		hasattr(instance, "blockSignals") and instance.blockSignals(False)
		return value

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
