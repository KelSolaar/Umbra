#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**common.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines common ui manipulation related objects.

**Others:**

"""

from __future__ import unicode_literals

import fnmatch
import functools
import os
import re
import sys
from PyQt4.QtCore import QString
from PyQt4.QtCore import QStringList
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractButton
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QIcon

import foundations.common
import foundations.data_structures
import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.exceptions
from foundations.parsers import SectionsFileParser
from umbra.globals.constants import Constants
from umbra.globals.runtime_globals import RuntimeGlobals
from umbra.globals.ui_constants import UiConstants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
		"Location",
		"get_application_instance",
		"parse_location",
		"get_resource_path",
		"set_window_default_icon",
		"get_sections_file_parser",
		"store_last_browsed_path",
		"QVariant_to_string",
		"parents_walker",
		"signals_blocker",
		"show_wait_cursor",
		"set_toolBox_height",
		"set_children_padding"]

LOGGER = foundations.verbose.install_logger()

class Location(foundations.data_structures.Structure):
	"""
	Defines a storage object for the :class:`SearchInFiles` class location.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param \*\*kwargs: directories, files, filters_in, filters_out, targets.
		:type \*\*kwargs: dict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.data_structures.Structure.__init__(self, **kwargs)

def get_application_instance():
	"""
	Returns the current `QApplication <http://doc.qt.nokia.com/qapplication.html>`_ instance or
	create one if it doesn't exists.

	:return: Application instance.
	:rtype: QApplication
	"""

	instance = QApplication.instance()
	if not instance:
		instance = QApplication(sys.argv)
	return instance

def parse_location(data):
	"""
	Parses given location data.

	:param data: Exception.
	:type data: Exception
	:return: Location object.
	:rtype: Location
	"""

	tokens = data.split(",")
	location = Location(directories=[], files=[], filters_in=[], filters_out=[], targets=[])
	if not tokens:
		return location

	for token in tokens:
		token = token.strip()
		if not token:
			continue

		if foundations.common.path_exists(token):
			if os.path.isdir(token):
				location.directories.append(token)
			else:
				location.files.append(token)
		else:
			match = re.match("(?P<filterIn>\*\.\w+)", token)
			if match:
				location.filters_in.append(fnmatch.translate(match.group("filterIn")))
				continue
			match = re.match("!(?P<filterOut>\*\.\w+)", token)
			if match:
				location.filters_out.append(fnmatch.translate(match.group("filterOut")))
				continue
			match = re.match("\<(?P<target>[\w ]+)\>", token)
			if match:
				location.targets.append(match.group("target"))
				continue
	return location

@foundations.exceptions.handle_exceptions(umbra.exceptions.ResourceExistsError)
def get_resource_path(name, raise_exception=False):
	"""
	Returns the resource file path matching the given name.

	:param name: Resource name.
	:type name: unicode
	:param raise_exception: Raise the exception.
	:type raise_exception: bool
	:return: Resource path.
	:rtype: unicode
	"""

	if not RuntimeGlobals.resources_directories:
		RuntimeGlobals.resources_directories.append(
		os.path.normpath(os.path.join(umbra.__path__[0], Constants.resources_directory)))

	for path in RuntimeGlobals.resources_directories:
		path = os.path.join(path, name)
		if foundations.common.path_exists(path):
			LOGGER.debug("> '{0}' resource path: '{1}'.".format(name, path))
			return path

	if raise_exception:
		raise umbra.exceptions.ResourceExistsError(
		"{0} | No resource file path found for '{1}' name!".format(__name__, name))

def set_window_default_icon(window):
	"""
	Sets the default Application icon to the given window.

	:param window: Window.
	:type window: QWidget
	:return: Definition success.
	:rtype: bool
	"""

	window.setWindowIcon(QIcon(get_resource_path(UiConstants.application_windows_icon)))
	return True

@foundations.exceptions.handle_exceptions(foundations.exceptions.FileExistsError)
def get_sections_file_parser(file):
	"""
	Returns a sections file parser.

	:param file: File.
	:type file: unicode
	:return: Parser.
	:rtype: SectionsFileParser
	"""

	if not foundations.common.path_exists(file):
		raise foundations.exceptions.FileExistsError("{0} | '{1}' sections file doesn't exists!".format(__name__, file))

	sections_file_parser = SectionsFileParser(file)
	sections_file_parser.parse()
	return sections_file_parser

@foundations.exceptions.handle_exceptions(TypeError)
def store_last_browsed_path(data):
	"""
	Defines a wrapper method used to store the last browsed path.

	:param data: Path data.
	:type data: QString or QList
	:return: Last browsed path.
	:rtype: unicode
	"""

	if type(data) in (tuple, list, QStringList):
		data = [foundations.strings.to_string(path) for path in data]
		last_browsed_path = foundations.common.get_first_item(data)
	elif type(data) in (unicode, QString):
		data = last_browsed_path = foundations.strings.to_string(data)
	else:
		raise TypeError("{0} | '{1}' type is not supported!".format(__name__, type(data)))

	if foundations.common.path_exists(last_browsed_path):
		last_browsed_path = os.path.normpath(last_browsed_path)
		if os.path.isfile(last_browsed_path):
			last_browsed_path = os.path.dirname(last_browsed_path)

		LOGGER.debug("> Storing last browsed path: '%s'.", last_browsed_path)
		RuntimeGlobals.last_browsed_path = last_browsed_path
	return data

def QVariant_to_string(data):
	"""
	Returns given `QVariant <http://doc.qt.nokia.com/qvariant.html>`_ data as a string.

	:param data: Given data.
	:type data: object
	:return: QVariant data as string.
	:rtype: unicode
	"""

	if isinstance(data, QVariant):
		data = data.toString()

	data = QString(data)
	return foundations.strings.to_string(data)

def parents_walker(object):
	"""
	Defines a generator used to retrieve the chain of parents of the given :class:`QObject` instance.

	:param object: Given path.
	:type object: QObject
	:yield: Object parent. ( QObject )
	"""

	while object.parent():
		object = object.parent()
		yield object

def signals_blocker(instance, attribute, *args, **kwargs):
	"""
	Blocks given instance signals before calling the given attribute with \
	given arguments and then unblocks the signals.

	:param instance: Instance object.
	:type instance: QObject
	:param attribute: Attribute to call.
	:type attribute: QObject
	:param \*args: Arguments.
	:type \*args: \*
	:param \*\*kwargs: Keywords arguments.
	:type \*\*kwargs: \*\*
	:return: Object.
	:rtype: object
	"""

	value = None
	try:
		hasattr(instance, "blockSignals") and instance.blockSignals(True)
		value = attribute(*args, **kwargs)
	finally:
		hasattr(instance, "blockSignals") and instance.blockSignals(False)
		return value

def show_wait_cursor(object):
	"""
	Shows a wait cursor while processing.
	
	:param object: Object to decorate.
	:type object: object
	:return: Object.
	:rtype: object
	"""

	@functools.wraps(object)
	def show_wait_cursorWrapper(*args, **kwargs):
		"""
		Shows a wait cursor while processing.

		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Object.
		:rtype: object
		"""

		QApplication.setOverrideCursor(Qt.WaitCursor)
		value = None
		try:
			value = object(*args, **kwargs)
		finally:
			QApplication.restoreOverrideCursor()
			return value

	return show_wait_cursorWrapper

def set_toolBox_height(tool_box, height=32):
	"""
	Sets given height to given QToolBox widget.

	:param toolbox: ToolBox.
	:type toolbox: QToolBox
	:param height: Height.
	:type height: int
	:return: Definition success.
	:rtype: bool
	"""

	for button in tool_box.findChildren(QAbstractButton):
		button.setMinimumHeight(height)
	return True

def set_children_padding(widget, types, height=None, width=None):
	"""
	Sets given Widget children padding.

	:param widget: Widget to sets the children padding.
	:type widget: QWidget
	:param types: Children types.
	:type types: tuple or list
	:param height: Height padding.
	:type height: int
	:param width: Width padding.
	:type width: int
	:return: Definition success.
	:rtype: bool
	"""

	for type in types:
		for child in widget.findChildren(type):
			child.setStyleSheet("{0}{{height: {1}px; width: {2}px;}}".format(
									type.__name__,
									child.fontMetrics().height() + (height if height is not None else 0) * 2,
									child.fontMetrics().width(child.text()) + (width if width is not None else 0) * 2))
	return True
