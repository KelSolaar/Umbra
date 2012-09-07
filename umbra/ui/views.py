#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application Views classes.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import inspect
import logging
import re
from PyQt4.QtCore import QEvent
from PyQt4.QtCore import QObject
from PyQt4.QtGui import QItemSelection
from PyQt4.QtGui import QItemSelectionModel
from PyQt4.QtGui import QListView
from PyQt4.QtGui import QTreeView

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.walkers
import umbra.ui.common
from umbra.globals.constants import Constants

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
		"getNodes",
		"filterNodes",
		"getViewNodesFromIndexes",
		"getViewSelectedNodes",
		"ReadOnlyFilter",
		"selectViewIndexes",
		"Abstract_QListView",
		"Abstract_QTreeView"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getNodes(view):
	"""
	This method returns the given View nodes.

	:param view: View. ( QWidget )
	:return: View nodes. ( List )
	"""

	return [node for node in foundations.walkers.nodesWalker(view.model().rootNode)]

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def filterNodes(view, pattern, attribute, flags=re.IGNORECASE):
	"""
	This method filters the given View nodes on given attribute using given pattern.

	:param view: View. ( QWidget )
	:param pattern: Filtering pattern. ( String )
	:param attribute: Filtering attribute. ( String )
	:param flags: Regex filtering flags. ( Integer )
	:return: View filtered nodes. ( List )
	"""

	return [node for node in getNodes(view) if re.search(pattern, getattr(node, attribute), flags)]

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, NotImplementedError)
# TODO: Implement a way to invalidate indexes in the cache, disabling the cache until yet.
# @core.memoize(None)
def getViewNodesFromIndexes(view, *indexes):
	"""
	This method returns the given View nodes from given indexes.

	:param view: View. ( QWidget )
	:param \*indexes: Indexes. ( List )
	:return: View nodes. ( Dictionary )
	"""

	nodes = {}
	model = view.model()
	if not model:
		return nodes

	if not hasattr(model, "getNode"):
		raise NotImplementedError(
		"{0} | '{1}' Model doesn't implement a 'getNode' method!".format(inspect.getmodulename(__file__), model))

	if not hasattr(model, "getAttribute"):
		raise NotImplementedError(
		"{0} | '{1}' Model doesn't implement a 'getAttribute' method!".format(inspect.getmodulename(__file__), model))

	for index in indexes:
		node = view.model().getNode(index)
		if not node in nodes:
			nodes[node] = []
		attribute = view.model().getAttribute(node, index.column())
		attribute and nodes[node].append(attribute)
	return nodes

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getViewSelectedNodes(view):
	"""
	This method returns the given View selected nodes.

	:param view: View. ( QWidget )
	:return: View selected nodes. ( Dictionary )
	"""

	return getViewNodesFromIndexes(view, *view.selectedIndexes())

class ReadOnlyFilter(QObject):
	"""
	This class is a `QObject <http://doc.qt.nokia.com/qobject.html>`_ subclass used as an event filter
	for the :class:`Abstract_QListView` and :class:`Abstract_QTreeView` classes.
	"""

	# @core.executionTrace
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
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler,
											False,
											foundations.exceptions.UserError)
	def __raiseUserError(self, view) :
		"""
		This method raises an error if the given view has been set read only and the user attempted to edit its content.

		:param view: View. ( QWidget )
		"""

		raise foundations.exceptions.UserError("{0} | Cannot perform action, '{1}' View has been set read only!".format(
		self.__class__.__name__, view.objectName() or view))

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def selectViewIndexes(view, indexes, flags=QItemSelectionModel.Select | QItemSelectionModel.Rows):
	"""
	This method selects given view indexes.

	:param view: View. ( QWidget )
	:param indexes: Indexes to select. ( List )
	:param flags: Selection flags. ( QItemSelectionModel.SelectionFlags )
	:return: Definition success. ( Boolean )
	"""

	if view.selectionModel():
		selection = QItemSelection()
		for index in indexes:
			selection.merge(QItemSelection(index, index), flags)
		view.selectionModel().select(selection, flags)
	return True

class Abstract_QListView(QListView):
	"""
	This class is a `QListView <http://doc.qt.nokia.com/qlistview.html>`_ subclass used as base
	by others Application views classes.
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

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def readOnly(self):
		"""
		This method is the property for **self.__readOnly** attribute.

		:return: self.__readOnly. ( Boolean )
		"""

		return self.__readOnly

	@readOnly.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def readOnly(self, value):
		"""
		This method is the setter method for **self.__readOnly** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		if value is not None:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("readOnly", value)
		self.__readOnly = value

	@readOnly.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def readOnly(self):
		"""
		This method is the deleter method for **self.__readOnly** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "readOnly"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the View ui.
		"""

		self.viewport().installEventFilter(ReadOnlyFilter(self))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getNodes(self):
		"""
		This method returns the View nodes.

		:return: View nodes. ( List )
		"""

		return getNodes(self)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def filterNodes(self, pattern, attribute, flags=re.IGNORECASE):
		"""
		This method filters the View nodes on given attribute using given pattern.
	
		:param pattern: Filtering pattern. ( String )
		:param attribute: Filtering attribute. ( String )
		:param flags: Regex filtering flags. ( Integer )
		:return: View filtered nodes. ( List )
		"""

		return filterNodes(self, pattern, attribute, flags)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getSelectedNodes(self):
		"""
		This method returns the View selected nodes.

		:return: View selected nodes. ( Dictionary )
		"""

		return getViewSelectedNodes(self)

	@core.executionTrace
	def selectIndexes(self, indexes, flags=QItemSelectionModel.Select | QItemSelectionModel.Rows):
		"""
		This method selects given indexes.

		:param indexes: Indexes to select. ( List )
		:param flags: Selection flags. ( QItemSelectionModel.SelectionFlags )
		:return: Method success. ( Boolean )
		"""

		return selectViewIndexes(self, indexes, flags)

class Abstract_QTreeView(QTreeView):
	"""
	This class is a `QTreeView <http://doc.qt.nokia.com/qtreeview.html>`_ subclass used as base
	by others Application views classes.
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

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def readOnly(self):
		"""
		This method is the property for **self.__readOnly** attribute.

		:return: self.__readOnly. ( Boolean )
		"""

		return self.__readOnly

	@readOnly.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def readOnly(self, value):
		"""
		This method is the setter method for **self.__readOnly** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		if value is not None:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("readOnly", value)
		self.__readOnly = value

	@readOnly.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def readOnly(self):
		"""
		This method is the deleter method for **self.__readOnly** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "readOnly"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		self.viewport().installEventFilter(ReadOnlyFilter(self))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getNodes(self):
		"""
		This method returns the View nodes.

		:return: View nodes. ( List )
		"""

		return getNodes(self)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def filterNodes(self, pattern, attribute, flags=re.IGNORECASE):
		"""
		This method filters the View nodes on given attribute using given pattern.
	
		:param pattern: Filtering pattern. ( String )
		:param attribute: Filtering attribute. ( String )
		:param flags: Regex filtering flags. ( Integer )
		:return: View filtered nodes. ( List )
		"""

		return filterNodes(self, pattern, attribute, flags)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getSelectedNodes(self):
		"""
		This method returns the View selected nodes.

		:return: View selected nodes. ( Dictionary )
		"""

		return getViewSelectedNodes(self)

	@core.executionTrace
	def selectIndexes(self, indexes, flags=QItemSelectionModel.Select | QItemSelectionModel.Rows):
		"""
		This method selects given indexes.

		:param indexes: Indexes to select. ( List )
		:param flags: Selection flags. ( QItemSelectionModel.SelectionFlags )
		:return: Method success. ( Boolean )
		"""

		return selectViewIndexes(self, indexes, flags)
