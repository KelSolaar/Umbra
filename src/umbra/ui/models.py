#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application models classes.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
from collections import OrderedDict
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from foundations.dag import AbstractCompositeNode
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

__all__ = ["LOGGER", "DefaultNode", "GraphModel"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class DefaultNode(AbstractCompositeNode):
	"""
	This class defines the default node used in :class:`GraphModel` class model.
	"""

	__family = "Default"

	@core.executionTrace
	def __init__(self, name=None, parent=None, children=None, **kwargs):
		"""
		This method initializes the class.

		:param name: Node name.  ( String )
		:param parent: Node parent. ( AbstractCompositeNode )
		:param children: Children. ( List )
		:param \*\*kwargs: Keywords arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractCompositeNode.__init__(self, name, parent, children, **kwargs)

class GraphModel(QAbstractItemModel):
	"""
	This class is a `QAbstractItemModel <http://doc.qt.nokia.com/4.7/qabstractitemmodel.html>`_ subclass providing a graph model.
	"""

	@core.executionTrace
	def __init__(self, parent=None, rootNode=None, headers=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param rootNode: Root node. ( AbstractCompositeNode )
		:param headers: Headers. ( OrderedDict )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QAbstractItemModel.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__rootNode = None
		self.rootNode = rootNode or DefaultNode(name="InvisibleRootNode")
		self.__headers = None
		self.headers = headers or OrderedDict([("Graph Model", "graphModel")])

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def rootNode(self):
		"""
		This method is the property for **self.__rootNode** attribute.

		:return: self.__rootNode. ( AbstractCompositeNode )
		"""

		return self.__rootNode

	@rootNode.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def rootNode(self, value):
		"""
		This method is the setter method for **self.__rootNode** attribute.

		:param value: Attribute value. ( AbstractCompositeNode )
		"""

		if value:
			assert issubclass(value.__class__, AbstractCompositeNode), "'{0}' attribute: '{1}' is not a '{2}' subclass!".format("rootNode", value, AbstractCompositeNode.__class__.__name__)
		self.__rootNode = value

	@rootNode.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def rootNode(self):
		"""
		This method is the deleter method for **self.__rootNode** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "rootNode"))

	@property
	def headers(self):
		"""
		This method is the property for **self.__headers** attribute.

		:return: self.__headers. ( OrderedDict )
		"""

		return self.__headers

	@headers.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def headers(self, value):
		"""
		This method is the setter method for **self.__headers** attribute.

		:param value: Attribute value. ( OrderedDict )
		"""

		if value:
			assert type(value) is OrderedDict, "'{0}' attribute: '{1}' type is not 'OrderedDict'!".format("headers", value)
		self.__headers = value

	@headers.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def headers(self):
		"""
		This method is the deleter method for **self.__headers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "headers"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def rowCount(self, parent=QModelIndex()):
		"""
		This method reimplements the :meth:`QAbstractItemModel.rowCount` method.
		
		:param parent: Parent node. ( AbstractCompositeNode )
		:return: Row count. ( Integer )
		"""

		if not parent.isValid():
			parentNode = self.__rootNode
		else:
			parentNode = parent.internalPointer()
		return parentNode.childrenCount()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def columnCount(self, parent=QModelIndex()):
		"""
		This method reimplements the :meth:`QAbstractItemModel.columnCount` method.
		
		:param parent: Parent node. ( AbstractCompositeNode )
		:return: Column count. ( Integer )
		"""

		return len(self.__headers.keys())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def data(self, index, role=Qt.DisplayRole):
		"""
		This method reimplements the :meth:`QAbstractItemModel.data` method.
		
		:param index: Index. ( QModelIndex )
		:param role: Role. ( Integer )
		:return: Data. ( QVariant )
		"""

		if not index.isValid():
			return QVariant()

		node = index.internalPointer()
		if role == Qt.DisplayRole or role == Qt.EditRole:
			if index.column() == 0:
				return node.name
			else:
				attribute = self.getAttribute(node, index.column())
				if attribute:
					return attribute.value

		if role == Qt.DecorationRole:
			if index.column() == 0:
				family = node.family

				if family == "":
					return QIcon(QPixmap(""))
		return QVariant()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setData(self, index, value, role=Qt.EditRole):
		"""
		This method reimplements the :meth:`QAbstractItemModel.setData` method.
		
		:param index: Index. ( QModelIndex )
		:param value: Value. ( QVariant )
		:param role: Role. ( Integer )
		:return: Method success. ( Boolean )
		"""

		if index.isValid():
			if role == Qt.EditRole:
				value = str(value.toString())
				node = index.internalPointer()
				if index.column() == 0:
					node.name = value
					self.dataChanged.emit(index, index)
					return True
				else:
					attribute = self.getAttribute(node, index.column())
					if attribute:
						attribute.value = value
						self.dataChanged.emit(index, index)
						return True
		return False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def headerData(self, section, orientation, role=Qt.DisplayRole):
		"""
		This method reimplements the :meth:`QAbstractItemModel.headerData` method.
		
		:param section: Section. ( Integer )
		:param orientation: Orientation. ( Qt.Orientation )
		:param role: Role. ( Integer )
		:return: Header data. ( QVariant )
		"""

		if role == Qt.DisplayRole:
			if orientation == Qt.Horizontal:
				if section < len(self.__headers.keys()):
					return self.__headers.keys()[section]
		return QVariant()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def flags(self, index):
		"""
		This method reimplements the :meth:`QAbstractItemModel.flags` method.
		
		:param index: Index. ( QModelIndex )
		:return: Flags. ( Qt.ItemFlags )
		"""

		return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def parent(self, index):
		"""
		This method reimplements the :meth:`QAbstractItemModel.parent` method.
		
		:param index: Index. ( QModelIndex )
		:return: Parent. ( QModelIndex )
		"""

		node = self.getNode(index)
		parentNode = node.parent
		if parentNode == self.__rootNode:
			return QModelIndex()
		return self.createIndex(parentNode.row(), 0, parentNode)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def index(self, row, column, parent=QModelIndex()):
		"""
		This method reimplements the :meth:`QAbstractItemModel.index` method.
		
		:param row: Row. ( Integer )
		:param column: Column. ( Integer )
		:param parent: Parent. ( QModelIndex )
		:return: Index. ( QModelIndex )
		"""

		parentNode = self.getNode(parent)
		childItem = parentNode.child(row)
		if childItem:
			return self.createIndex(row, column, childItem)
		else:
			return QModelIndex()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def insertRows(self, row, count, parent=QModelIndex()):
		"""
		This method reimplements the :meth:`QAbstractItemModel.insertRows` method.
		
		:param row: Row. ( Integer )
		:param count: Count. ( Integer )
		:param parent: Parent. ( QModelIndex )
		:return: Method success. ( Boolean )
		"""

		parentNode = self.getNode(parent)
		self.beginInsertRows(parent, row, row + count - 1)
		success = True
		for i in range(count):
			childNode = DefaultNode()
			success *= parentNode.insertChild(childNode, row)
		self.endInsertRows()
		return success

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeRows(self, row, count, parent=QModelIndex()):
		"""
		This method reimplements the :meth:`QAbstractItemModel.removeRows` method.
		
		:param row: Row. ( Integer )
		:param count: Count. ( Integer )
		:param parent: Parent. ( QModelIndex )
		:return: Method success. ( Boolean )
		"""

		parentNode = self.getNode(parent)
		self.beginRemoveRows(parent, row, row + count - 1)
		success = True
		for i in range(count):
			success *= parentNode.removeChild(row)
		self.endRemoveRows()
		return success

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getNode(self, index):
		"""
		This method returns the node at given index.
		
		:param index: Index. ( QModelIndex )
		:return: Node. ( AbstractCompositeNode )
		"""

		if index.isValid():
			node = index.internalPointer()
			if node:
				return node
		return self.__rootNode

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getAttribute(self, node, column):
		"""
		This method returns the given node attribute associated to the given column.
		
		:param node: Node. ( AbstractCompositeNode )
		:param column: Column. ( Integer )
		:return: Attribute. ( Attribute )
		"""

		if column > 0 and column < len(self.__headers.keys()):
			return node.get(self.__headers[self.__headers.keys()[column]], None)
