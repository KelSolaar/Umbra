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
import re
from PyQt4.QtCore import QEvent
from PyQt4.QtCore import QObject
from PyQt4.QtCore import QString
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QItemSelection
from PyQt4.QtGui import QItemSelectionModel
from PyQt4.QtGui import QListView
from PyQt4.QtGui import QTreeView

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.walkers
import foundations.verbose
import umbra.ui.common
from umbra.ui.widgets.notification_QLabel import Notification_QLabel

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
		"Mixin_AbstractView",
		"ReadOnlyFilter",
		"Abstract_QListView",
		"Abstract_QTreeView"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ReadOnlyFilter(QObject):
	"""
	This class is a `QObject <http://doc.qt.nokia.com/qobject.html>`_ subclass used as an event filter
	for the :class:`Abstract_QListView` and :class:`Abstract_QTreeView` classes.
	"""

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

	@foundations.exceptions.handleExceptions(umbra.ui.common.notifyExceptionHandler,
											foundations.exceptions.UserError)
	def __raiseUserError(self, view) :
		"""
		This method raises an error if the given view has been set read only and the user attempted to edit its content.

		:param view: View. ( QWidget )
		"""

		raise foundations.exceptions.UserError("{0} | Cannot perform action, '{1}' View has been set read only!".format(
		self.__class__.__name__, view.objectName() or view))

class Mixin_AbstractView(object):
	"""
	This class is a mixin used to bring common capabilities in Application views classes.
	"""

	def __init__(self, readOnly=None, message=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param readOnly: View is read only. ( Boolean )
		:param message: View default message when Model is empty. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__readOnly = readOnly

		self.__message = None
		self.message = message or "No Nodes to view!"

		self.__notifier = Notification_QLabel(self,
											color=QColor(192, 192, 192),
											borderColor=QColor(32, 32, 32),
											anchor=8)

		Mixin_AbstractView.__initializeUi(self)

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
	@foundations.exceptions.handleExceptions(AssertionError)
	def readOnly(self, value):
		"""
		This method is the setter method for **self.__readOnly** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		if value is not None:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("readOnly", value)
		self.__readOnly = value

	@readOnly.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def readOnly(self):
		"""
		This method is the deleter method for **self.__readOnly** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "readOnly"))

	@property
	def message(self):
		"""
		This method is the property for **self.__message** attribute.

		:return: self.__message. ( String )
		"""

		return self.__message

	@message.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def message(self, value):
		"""
		This method is the setter method for **self.__message** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode, QString), \
			"'{0}' attribute: '{1}' type is not 'str', 'unicode' or 'QString'!".format("message", value)
		self.__message = value

	@message.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def message(self):
		"""
		This method is the deleter method for **self.__message** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "message"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def resizeEvent(self, event):
		"""
		This method reimplements the :meth:`*.resizeEvent` method.
	
		:param event: QEvent. ( QEvent )
		"""

		super(type(self), self).resizeEvent(event)

		self.__notifier.refreshPosition()

	def paintEvent(self, event):
		"""
		This method reimplements the :meth:`*.paintEvent` method.
	
		:param event: QEvent. ( QEvent )
		"""

		super(type(self), self).paintEvent(event)

		model = self.model()
		if not model:
			return

		if not hasattr(model, "rootNode"):
			return

		if not model.rootNode.children:
			self.__notifier.showMessage(self.__message, 0)
		else:
			self.__notifier.hideMessage()

	def __initializeUi(self):
		"""
		This method initializes the View ui.
		"""

		self.viewport().installEventFilter(ReadOnlyFilter(self))

		if issubclass(type(self), QListView):
			super(type(self), self).setUniformItemSizes(True)
		elif issubclass(type(self), QTreeView):
			super(type(self), self).setUniformRowHeights(True)

	def getNodes(self):
		"""
		This method returns the View nodes.

		:return: View nodes. ( List )
		"""

		return [node for node in foundations.walkers.nodesWalker(self.model().rootNode)]

	def filterNodes(self, pattern, attribute, flags=re.IGNORECASE):
		"""
		This method filters the View nodes on given attribute using given pattern.
	
		:param pattern: Filtering pattern. ( String )
		:param attribute: Filtering attribute. ( String )
		:param flags: Regex filtering flags. ( Integer )
		:return: View filtered nodes. ( List )
		"""

		return [node for node in self.getNodes() if re.search(pattern, getattr(node, attribute), flags)]

	@foundations.exceptions.handleExceptions(NotImplementedError)
	# TODO: Implement a way to invalidate indexes in the cache, disabling the cache until yet.
	# @core.memoize(None)
	def getViewNodesFromIndexes(self, *indexes):
		"""
		This method returns the View nodes from given indexes.
	
		:param view: View. ( QWidget )
		:param \*indexes: Indexes. ( List )
		:return: View nodes. ( Dictionary )
		"""

		nodes = {}
		model = self.model()
		if not model:
			return nodes

		if not hasattr(model, "getNode"):
			raise NotImplementedError(
			"{0} | '{1}' Model doesn't implement a 'getNode' method!".format(inspect.getmodulename(__file__), model))

		if not hasattr(model, "getAttribute"):
			raise NotImplementedError(
			"{0} | '{1}' Model doesn't implement a 'getAttribute' method!".format(inspect.getmodulename(__file__), model))

		for index in indexes:
			node = model.getNode(index)
			if not node in nodes:
				nodes[node] = []
			attribute = model.getAttribute(node, index.column())
			attribute and nodes[node].append(attribute)
		return nodes

	def getViewSelectedNodes(self):
		"""
		This method returns the View selected nodes.
	
		:param view: View. ( QWidget )
		:return: View selected nodes. ( Dictionary )
		"""

		return self.getViewNodesFromIndexes(*self.selectedIndexes())

	def getSelectedNodes(self):
		"""
		This method returns the View selected nodes.

		:return: View selected nodes. ( Dictionary )
		"""

		return self.getViewSelectedNodes()

	def selectViewIndexes(self, indexes, flags=QItemSelectionModel.Select | QItemSelectionModel.Rows):
		"""
		This method selects the View given indexes.
	
		:param view: View. ( QWidget )
		:param indexes: Indexes to select. ( List )
		:param flags: Selection flags. ( QItemSelectionModel.SelectionFlags )
		:return: Definition success. ( Boolean )
		"""

		if self.selectionModel():
			selection = QItemSelection()
			for index in indexes:
				selection.merge(QItemSelection(index, index), flags)
			self.selectionModel().select(selection, flags)
		return True

	def selectIndexes(self, indexes, flags=QItemSelectionModel.Select | QItemSelectionModel.Rows):
		"""
		This method selects given indexes.

		:param indexes: Indexes to select. ( List )
		:param flags: Selection flags. ( QItemSelectionModel.SelectionFlags )
		:return: Method success. ( Boolean )
		"""

		return self.selectViewIndexes(indexes, flags)

class Abstract_QListView(QListView, Mixin_AbstractView):
	"""
	This class is a `QListView <http://doc.qt.nokia.com/qlistview.html>`_ subclass used as base
	by others Application views classes.
	"""

	def __init__(self, parent=None, readOnly=False, message=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param readOnly: View is read only. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QListView.__init__(self, parent)
		Mixin_AbstractView.__init__(self, readOnly, message)

class Abstract_QTreeView(QTreeView, Mixin_AbstractView):
	"""
	This class is a `QTreeView <http://doc.qt.nokia.com/qtreeview.html>`_ subclass used as base
	by others Application views classes.
	"""

	def __init__(self, parent=None, readOnly=False, message=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param readOnly: View is read only. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QTreeView.__init__(self, parent)
		Mixin_AbstractView.__init__(self, readOnly, message)
