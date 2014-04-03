#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the Application Views classes.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import re
from PyQt4.QtCore import QAbstractItemModel
from PyQt4.QtCore import QAbstractListModel
from PyQt4.QtCore import QAbstractTableModel
from PyQt4.QtCore import QEvent
from PyQt4.QtCore import QObject
from PyQt4.QtCore import QString
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QItemSelection
from PyQt4.QtGui import QItemSelectionModel
from PyQt4.QtGui import QListView
from PyQt4.QtGui import QTableView
from PyQt4.QtGui import QTreeView
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QTableWidget
from PyQt4.QtGui import QTreeWidget

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.walkers
import foundations.verbose
import umbra.exceptions
import umbra.ui.common
from umbra.ui.models import GraphModel
from umbra.ui.widgets.notification_QLabel import Notification_QLabel

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
		"ReadOnlyFilter",
		"Mixin_AbstractBase"
		"Mixin_AbstractView",
		"Mixin_AbstractWidget",
		"Abstract_QListView",
		"Abstract_QTableView",
		"Abstract_QTreeView",
		"Abstract_QListWidget",
		"Abstract_QTableWidget",
		"Abstract_QTreeWidget"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ReadOnlyFilter(QObject):
	"""
	Defines a `QObject <http://doc.qt.nokia.com/qobject.html>`_ subclass used as an event filter
	for the :class:`Abstract_QListView` and :class:`Abstract_QTreeView` classes.
	"""

	def eventFilter(self, object, event):
		"""
		Reimplements the **QObject.eventFilter** method.
		
		:param object: Object.
		:type object: QObject
		:param event: Event.
		:type event: QEvent
		:return: Event filtered.
		:rtype: bool
		"""

		if event.type() == QEvent.MouseButtonDblClick:
			view = object.parent()
			if view.readOnly:
				self.__raiseUserError(view)
				return True
		return False

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											foundations.exceptions.UserError)
	def __raiseUserError(self, view) :
		"""
		Raises an error if the given View has been set read only and the user attempted to edit its content.

		:param view: View.
		:type view: QWidget
		"""

		raise foundations.exceptions.UserError("{0} | Cannot perform action, '{1}' View has been set read only!".format(
		self.__class__.__name__, view.objectName() or view))

class Mixin_AbstractBase(object):
	"""
	Defines the base mixin used to bring common capabilities in Application Views classes.
	"""

	def __init__(self, message=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param message: View default message when Model is empty.
		:type message: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__message = None
		self.message = message or "No Item to view!"

		self.__notifier = Notification_QLabel(self,
											color=QColor(192, 192, 192),
											backgroundColor=QColor(24, 24, 24),
											borderColor=QColor(32, 32, 32),
											anchor=8)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def message(self):
		"""
		Property for **self.__message** attribute.

		:return: self.__message.
		:rtype: unicode
		"""

		return self.__message

	@message.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def message(self, value):
		"""
		Setter for **self.__message** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) in (unicode, QString), \
			"'{0}' attribute: '{1}' type is not 'unicode' or 'QString'!".format("message", value)
		self.__message = value

	@message.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def message(self):
		"""
		Deleter for **self.__message** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "message"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def resizeEvent(self, event):
		"""
		Reimplements the :meth:`*.resizeEvent` method.
	
		:param event: QEvent.
		:type event: QEvent
		"""

		super(type(self), self).resizeEvent(event)

		self.__notifier.refreshPosition()

	def paintEvent(self, event):
		"""
		Reimplements the :meth:`*.paintEvent` method.
	
		:param event: QEvent.
		:type event: QEvent
		"""

		super(type(self), self).paintEvent(event)

		showMessage = True
		model = self.model()
		if issubclass(type(model), GraphModel):
			if model.hasNodes():
				showMessage = False
		elif issubclass(type(model), QAbstractItemModel) or \
		issubclass(type(model), QAbstractListModel) or \
		issubclass(type(model), QAbstractTableModel):
			if model.rowCount():
				showMessage = False

		if showMessage:
			self.__notifier.showMessage(self.__message, 0)
		else:
			self.__notifier.hideMessage()

class Mixin_AbstractView(Mixin_AbstractBase):
	"""
	Defines a mixin used to bring common capabilities in Application Views classes.
	"""

	def __init__(self, readOnly=None, message=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param readOnly: View is read only.
		:type readOnly: bool
		:param message: View default message when Model is empty.
		:type message: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		Mixin_AbstractBase.__init__(self, message or "No Node to view!")

		# --- Setting class attributes. ---
		self.__readOnly = readOnly

		Mixin_AbstractView.__initializeUi(self)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def readOnly(self):
		"""
		Property for **self.__readOnly** attribute.

		:return: self.__readOnly.
		:rtype: bool
		"""

		return self.__readOnly

	@readOnly.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def readOnly(self, value):
		"""
		Setter for **self.__readOnly** attribute.

		:param value: Attribute value.
		:type value: bool
		"""

		if value is not None:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("readOnly", value)
		self.__readOnly = value

	@readOnly.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def readOnly(self):
		"""
		Deleter for **self.__readOnly** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "readOnly"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeUi(self):
		"""
		Initializes the View ui.
		"""

		self.viewport().installEventFilter(ReadOnlyFilter(self))

		if issubclass(type(self), QListView):
			super(type(self), self).setUniformItemSizes(True)
		elif issubclass(type(self), QTreeView):
			super(type(self), self).setUniformRowHeights(True)

	def getNodes(self):
		"""
		Returns the View nodes.

		:return: View nodes.
		:rtype: list
		"""

		return [node for node in foundations.walkers.nodesWalker(self.model().rootNode)]

	def filterNodes(self, pattern, attribute, flags=re.IGNORECASE):
		"""
		Filters the View Nodes on given attribute using given pattern.
	
		:param pattern: Filtering pattern.
		:type pattern: unicode
		:param attribute: Filtering attribute.
		:type attribute: unicode
		:param flags: Regex filtering flags.
		:type flags: int
		:return: View filtered nodes.
		:rtype: list
		"""

		return [node for node in self.getNodes() if re.search(pattern, getattr(node, attribute), flags)]

	@foundations.exceptions.handleExceptions(NotImplementedError)
	# TODO: Implement a way to invalidate indexes in the cache, disabling the cache until yet.
	# @foundations.decorators.memoize(None)
	def getViewNodesFromIndexes(self, *indexes):
		"""
		Returns the View Nodes from given indexes.
	
		:param view: View.
		:type view: QWidget
		:param \*indexes: Indexes.
		:type \*indexes: list
		:return: View nodes.
		:rtype: dict
		"""

		nodes = {}
		model = self.model()
		if not model:
			return nodes

		if not hasattr(model, "getNode"):
			raise NotImplementedError(
			"{0} | '{1}' Model doesn't implement a 'getNode' method!".format(__name__, model))

		if not hasattr(model, "getAttribute"):
			raise NotImplementedError(
			"{0} | '{1}' Model doesn't implement a 'getAttribute' method!".format(__name__, model))

		for index in indexes:
			node = model.getNode(index)
			if not node in nodes:
				nodes[node] = []
			attribute = model.getAttribute(node, index.column())
			attribute and nodes[node].append(attribute)
		return nodes

	def getViewSelectedNodes(self):
		"""
		Returns the View selected nodes.
	
		:param view: View.
		:type view: QWidget
		:return: View selected nodes.
		:rtype: dict
		"""

		return self.getViewNodesFromIndexes(*self.selectedIndexes())

	def getSelectedNodes(self):
		"""
		Returns the View selected nodes.

		:return: View selected nodes.
		:rtype: dict
		"""

		return self.getViewSelectedNodes()

	def selectViewIndexes(self, indexes, flags=QItemSelectionModel.Select | QItemSelectionModel.Rows):
		"""
		Selects the View given indexes.
	
		:param view: View.
		:type view: QWidget
		:param indexes: Indexes to select.
		:type indexes: list
		:param flags: Selection flags. ( QItemSelectionModel.SelectionFlags )
		:return: Definition success.
		:rtype: bool
		"""

		if self.selectionModel():
			selection = QItemSelection()
			for index in indexes:
				selection.merge(QItemSelection(index, index), flags)
			self.selectionModel().select(selection, flags)
		return True

	def selectIndexes(self, indexes, flags=QItemSelectionModel.Select | QItemSelectionModel.Rows):
		"""
		Selects given indexes.

		:param indexes: Indexes to select.
		:type indexes: list
		:param flags: Selection flags. ( QItemSelectionModel.SelectionFlags )
		:return: Method success.
		:rtype: bool
		"""

		return self.selectViewIndexes(indexes, flags)

class Mixin_AbstractWidget(Mixin_AbstractBase):
	"""
	Defines a mixin used to bring common capabilities in Application Widgets Views classes.
	"""

	pass

class Abstract_QListView(QListView, Mixin_AbstractView):
	"""
	Defines a `QListView <http://doc.qt.nokia.com/qlistview.html>`_ subclass used as base
	by others Application Views classes.
	"""

	def __init__(self, parent=None, readOnly=False, message=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param readOnly: View is read only.
		:type readOnly: bool
		:param message: View default message when Model is empty.
		:type message: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QListView.__init__(self, parent)
		Mixin_AbstractView.__init__(self, readOnly, message)

class Abstract_QTableView(QTableView, Mixin_AbstractView):
	"""
	Defines a `QTableView <http://doc.qt.nokia.com/qtableview.html>`_ subclass used as base
	by others Application Views classes.
	"""

	def __init__(self, parent=None, readOnly=False, message=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param readOnly: View is read only.
		:type readOnly: bool
		:param message: View default message when Model is empty.
		:type message: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QTableView.__init__(self, parent)
		Mixin_AbstractView.__init__(self, readOnly, message)

class Abstract_QTreeView(QTreeView, Mixin_AbstractView):
	"""
	Defines a `QTreeView <http://doc.qt.nokia.com/qtreeview.html>`_ subclass used as base
	by others Application Views classes.
	"""

	def __init__(self, parent=None, readOnly=False, message=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param readOnly: View is read only.
		:type readOnly: bool
		:param message: View default message when Model is empty.
		:type message: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QTreeView.__init__(self, parent)
		Mixin_AbstractView.__init__(self, readOnly, message)

class Abstract_QListWidget(QListWidget, Mixin_AbstractWidget):
	"""
	Defines a `QListWidget <http://doc.qt.nokia.com/qlistwidget.html>`_ subclass used as base
	by others Application Widgets Views classes.
	"""

	def __init__(self, parent=None, message=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param message: View default message when Model is empty.
		:type message: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QListWidget.__init__(self, parent)
		Mixin_AbstractWidget.__init__(self, message)

class Abstract_QTableWidget(QTableWidget, Mixin_AbstractWidget):
	"""
	Defines a `QTableWidget <http://doc.qt.nokia.com/qtablewidget.html>`_ subclass used as base
	by others Application Widgets Views classes.
	"""

	def __init__(self, parent=None, readOnly=False, message=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param message: View default message when Model is empty.
		:type message: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QTableWidget.__init__(self, parent)
		Mixin_AbstractWidget.__init__(self, message)

class Abstract_QTreeWidget(QTreeWidget, Mixin_AbstractWidget):
	"""
	Defines a `QTreeWidget <http://doc.qt.nokia.com/qtreewidget.html>`_ subclass used as base
	by others Application Widgets Views classes.
	"""

	def __init__(self, parent=None, message=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param message: View default message when Model is empty.
		:type message: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QTreeWidget.__init__(self, parent)
		Mixin_AbstractWidget.__init__(self, message)
