#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application views classes.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import umbra.ui.common
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "getViewSelectedNodes", "ReadOnlyFilter", "Abstract_QListView", "Abstract_QTreeView"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getViewSelectedNodes(view):
	"""
	This method returns the given View selected nodes.

	:param view: View. ( QWidget )
	:return: View selected nodes. ( Dictionary )
	"""

	nodes = {}
	for index in view.selectedIndexes():
		node = view.model().getNode(index)
		if not node in nodes.keys():
			nodes[node] = []
		attribute = view.model().getAttribute(node, index.column())
		attribute and nodes[node].append(attribute)
	return nodes

class ReadOnlyFilter(QObject):
	"""
	This class is a `QObject <http://doc.qt.nokia.com/4.7/qobject.html>`_ subclass used as an event filter for the :class:`Abstract_QListView` and :class:`Abstract_QTreeView` classes.
	"""

	@core.executionTrace
	def eventFilter(self, object, event):
		"""
		This method reimplements the **QObject.eventFilter** method.
		
		:param object: Object. ( QObject )
		:param event: Event. ( QEvent )
		:return: Event filtered. ( Boolean )
		"""

		if event.type() == QEvent.MouseButtonDblClick:
			view = object.parent()
			if view.readOnly:
				self.__raiseUserError(view)
				return True
		return False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, foundations.exceptions.UserError)
	def __raiseUserError(self, view) :
		"""
		This method raises an error if the given view has been set read only and the user attempted to edit its content.

		:param view: View. ( QWidget )
		"""

		raise foundations.exceptions.UserError("{0} | Cannot perform action, '{1}' View has been set read only!".format(self.__class__.__name__, view.objectName() or view))

class Abstract_QListView(QListView):
	"""
	This class is a `QListView <http://doc.qt.nokia.com/4.7/qlistview.html>`_ subclass used as base by others Application views classes.
	"""

	@core.executionTrace
	def __init__(self, parent=None, readOnly=False):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param readOnly: View is read only. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QListView.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__readOnly = readOnly

		Abstract_QListView.__initializeUi(self)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def readOnly(self):
		"""
		This method is the property for **self.__readOnly** attribute.

		:return: self.__readOnly. ( Boolean )
		"""

		return self.__readOnly

	@readOnly.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def readOnly(self, value):
		"""
		This method is the setter method for **self.__readOnly** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		if value:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("readOnly", value)
		self.__readOnly = value

	@readOnly.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def readOnly(self):
		"""
		This method is the deleter method for **self.__readOnly** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "readOnly"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the View ui.
		"""

		self.viewport().installEventFilter(ReadOnlyFilter(self))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getSelectedNodes(self):
		"""
		This method returns the selected nodes.

		:return: View selected nodes. ( Dictionary )
		"""

		return getViewSelectedNodes(self)

class Abstract_QTreeView(QTreeView):
	"""
	This class is a `QTreeView <http://doc.qt.nokia.com/4.7/qtreeview.html>`_ subclass used as base by others Application views classes.
	"""

	@core.executionTrace
	def __init__(self, parent=None, readOnly=False):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param readOnly: View is read only. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QTreeView.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__readOnly = readOnly

		Abstract_QTreeView.__initializeUi(self)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def readOnly(self):
		"""
		This method is the property for **self.__readOnly** attribute.

		:return: self.__readOnly. ( Boolean )
		"""

		return self.__readOnly

	@readOnly.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def readOnly(self, value):
		"""
		This method is the setter method for **self.__readOnly** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		if value:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("readOnly", value)
		self.__readOnly = value

	@readOnly.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def readOnly(self):
		"""
		This method is the deleter method for **self.__readOnly** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "readOnly"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		self.viewport().installEventFilter(ReadOnlyFilter(self))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getSelectedNodes(self):
		"""
		This method returns the selected nodes.

		:return: View selected nodes. ( Dictionary )
		"""

		return getViewSelectedNodes(self)
