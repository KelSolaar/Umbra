#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the Application Models classes.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import pickle
import sys
import weakref
if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
	from collections import OrderedDict
from PyQt4.QtCore import QAbstractItemModel
from PyQt4.QtCore import QMimeData
from PyQt4.QtCore import QModelIndex
from PyQt4.QtCore import QStringList
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QIcon

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.ui.nodes
from foundations.nodes import AbstractCompositeNode

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "GraphModel"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class GraphModel(QAbstractItemModel):
	"""
	| Defines a `QAbstractItemModel <http://doc.qt.nokia.com/qabstractitemmodel.html>`_ subclass
		providing a graph model.
	| The Model provided by this object is very generic and abstract making it compatible with major Qt Views
		( `QListView <http://doc.qt.nokia.com/qlistview.html>`_,
		`QTreeView <http://doc.qt.nokia.com/QTreeView.html>`_,
		`QTableView <http://doc.qt.nokia.com/qtableview.html>`_,
		`QComboBox <http://doc.qt.nokia.com/qcombobox.html>`_ ).
	"""

	__modelsInstances = weakref.WeakValueDictionary()
	"""
	:param __modelsInstances: Models instances.
	:type __modelsInstances: dict
	"""

	def __new__(cls, *args, **kwargs):
		"""
		Constructor of the class.
		
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Class instance.
		:rtype: AbstractNode
		"""

		instance = super(GraphModel, cls).__new__(cls)

		GraphModel._GraphModel__modelsInstances[id(instance)] = instance
		return instance

	def __init__(self,
				parent=None,
				rootNode=None,
				horizontalHeaders=None,
				verticalHeaders=None,
				defaultNode=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param rootNode: Root node.
		:type rootNode: AbstractCompositeNode or GraphModelNode
		:param horizontalHeaders: Headers.
		:type horizontalHeaders: OrderedDict
		:param verticalHeaders: Headers.
		:type verticalHeaders: OrderedDict
		:param defaultNode: Default node.
		:type defaultNode: AbstractCompositeNode or GraphModelNode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QAbstractItemModel.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__rootNode = None
		self.rootNode = rootNode or umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")
		self.__horizontalHeaders = None
		self.horizontalHeaders = horizontalHeaders or OrderedDict([("Graph Model", "graphModel")])
		self.__verticalHeaders = None
		self.verticalHeaders = verticalHeaders or OrderedDict()
		self.__defaultNode = None
		self.defaultNode = defaultNode or umbra.ui.nodes.GraphModelNode

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def rootNode(self):
		"""
		Property for **self.__rootNode** attribute.

		:return: self.__rootNode.
		:rtype: AbstractCompositeNode or GraphModelNode
		"""

		return self.__rootNode

	@rootNode.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def rootNode(self, value):
		"""
		Setter for **self.__rootNode** attribute.

		:param value: Attribute value.
		:type value: AbstractCompositeNode or GraphModelNode
		"""

		if value is not None:
			assert issubclass(value.__class__, AbstractCompositeNode), \
			"'{0}' attribute: '{1}' is not a '{2}' subclass!".format("rootNode", value, AbstractCompositeNode.__name__)
		self.__rootNode = value

	@rootNode.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def rootNode(self):
		"""
		Deleter for **self.__rootNode** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "rootNode"))

	@property
	def horizontalHeaders(self):
		"""
		Property for **self.__horizontalHeaders** attribute.

		:return: self.__horizontalHeaders.
		:rtype: OrderedDict
		"""

		return self.__horizontalHeaders

	@horizontalHeaders.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def horizontalHeaders(self, value):
		"""
		Setter for **self.__horizontalHeaders** attribute.

		:param value: Attribute value.
		:type value: OrderedDict
		"""

		if value is not None:
			assert type(value) is OrderedDict, "'{0}' attribute: '{1}' type is not 'OrderedDict'!".format(
			"horizontalHeaders", value)
		self.__horizontalHeaders = value

	@horizontalHeaders.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def horizontalHeaders(self):
		"""
		Deleter for **self.__horizontalHeaders** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "horizontalHeaders"))

	@property
	def verticalHeaders(self):
		"""
		Property for **self.__verticalHeaders** attribute.

		:return: self.__verticalHeaders.
		:rtype: OrderedDict
		"""

		return self.__verticalHeaders

	@verticalHeaders.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def verticalHeaders(self, value):
		"""
		Setter for **self.__verticalHeaders** attribute.

		:param value: Attribute value.
		:type value: OrderedDict
		"""

		if value is not None:
			assert type(value) is OrderedDict, "'{0}' attribute: '{1}' type is not 'OrderedDict'!".format(
			"verticalHeaders", value)
		self.__verticalHeaders = value

	@verticalHeaders.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def verticalHeaders(self):
		"""
		Deleter for **self.__verticalHeaders** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "verticalHeaders"))

	@property
	def defaultNode(self):
		"""
		Property for **self.__defaultNode** attribute.

		:return: self.__defaultNode.
		:rtype: AbstractCompositeNode or GraphModelNode
		"""

		return self.__defaultNode

	@defaultNode.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def defaultNode(self, value):
		"""
		Setter for **self.__defaultNode** attribute.

		:param value: Attribute value.
		:type value: AbstractCompositeNode or GraphModelNode
		"""

		if value is not None:
			assert issubclass(value, AbstractCompositeNode), \
			"'{0}' attribute: '{1}' is not a '{2}' subclass!".format("defaultNode", value, AbstractCompositeNode.__name__)
		self.__defaultNode = value

	@defaultNode.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultNode(self):
		"""
		Deleter for **self.__defaultNode** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultNode"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def rowCount(self, parent=QModelIndex()):
		"""
		Reimplements the :meth:`QAbstractItemModel.rowCount` method.
		
		:param parent: Parent node.
		:type parent: AbstractCompositeNode or GraphModelNode
		:return: Row count.
		:rtype: int
		"""

		if not parent.isValid():
			parentNode = self.__rootNode
		else:
			parentNode = parent.internalPointer()
		return parentNode.childrenCount()

	def columnCount(self, parent=QModelIndex()):
		"""
		Reimplements the :meth:`QAbstractItemModel.columnCount` method.
		
		:param parent: Parent node.
		:type parent: AbstractCompositeNode or GraphModelNode
		:return: Column count.
		:rtype: int
		"""

		return len(self.__horizontalHeaders)

	def data(self, index, role=Qt.DisplayRole):
		"""
		Reimplements the :meth:`QAbstractItemModel.data` method.
		
		:param index: Index.
		:type index: QModelIndex
		:param role: Role.
		:type role: int
		:return: Data.
		:rtype: QVariant
		"""

		if not index.isValid():
			return QVariant()

		node = self.getNode(index)
		if index.column() == 0:
			if hasattr(node, "roles"):
				if role == Qt.DecorationRole:
					return QIcon(node.roles.get(role, ""))
				else:
					return node.roles.get(role, QVariant())
		else:
			attribute = self.getAttribute(node, index.column())
			if attribute:
				if hasattr(attribute, "roles"):
					if role == Qt.DecorationRole:
						return QIcon(attribute.roles.get(role, ""))
					else:
						return attribute.roles.get(role, QVariant())
		return QVariant()

	def setData(self, index, value, role=Qt.EditRole):
		"""
		Reimplements the :meth:`QAbstractItemModel.setData` method.
		
		:param index: Index.
		:type index: QModelIndex
		:param value: Value.
		:type value: QVariant
		:param role: Role.
		:type role: int
		:return: Method success.
		:rtype: bool
		"""

		if not index.isValid():
			return False

		node = self.getNode(index)
		if role == Qt.DisplayRole or role == Qt.EditRole:
			value = foundations.strings.toString(value.toString())
			roles = {Qt.DisplayRole : value, Qt.EditRole : value}
		else:
			roles = {role : value}

		if index.column() == 0:
			if (node and hasattr(node, "roles")):
				node.roles.update(roles)
				node.name = value
		else:
			attribute = self.getAttribute(node, index.column())
			if (attribute and hasattr(attribute, "roles")):
				attribute.roles.update(roles)
				attribute.value = value

		self.dataChanged.emit(index, index)
		return True

	def headerData(self, section, orientation, role=Qt.DisplayRole):
		"""
		Reimplements the :meth:`QAbstractItemModel.headerData` method.
		
		:param section: Section.
		:type section: int
		:param orientation: Orientation. ( Qt.Orientation )
		:param role: Role.
		:type role: int
		:return: Header data.
		:rtype: QVariant
		"""

		if role == Qt.DisplayRole:
			if orientation == Qt.Horizontal:
				if section < len(self.__horizontalHeaders):
					return self.__horizontalHeaders.keys()[section]
			elif orientation == Qt.Vertical:
				if section < len(self.__verticalHeaders):
					return self.__verticalHeaders.keys()[section]
		return QVariant()

	def flags(self, index):
		"""
		Reimplements the :meth:`QAbstractItemModel.flags` method.
		
		:param index: Index.
		:type index: QModelIndex
		:return: Flags. ( Qt.ItemFlags )
		"""

		if not index.isValid():
			return Qt.NoItemFlags

		node = self.getNode(index)
		if index.column() == 0:
			return hasattr(node, "flags") and Qt.ItemFlags(node.flags) or Qt.NoItemFlags
		else:
			attribute = self.getAttribute(node, index.column())
			return attribute and hasattr(attribute, "flags") and Qt.ItemFlags(attribute.flags) or Qt.NoItemFlags

	def parent(self, index):
		"""
		Reimplements the :meth:`QAbstractItemModel.parent` method.
		
		:param index: Index.
		:type index: QModelIndex
		:return: Parent.
		:rtype: QModelIndex
		"""

		if not index.isValid():
			return QModelIndex()

		node = self.getNode(index)
		parentNode = node.parent
		if not parentNode:
			return QModelIndex()

		if parentNode == self.__rootNode:
			return QModelIndex()

		row = parentNode.row()
		return self.createIndex(row, 0, parentNode) if row is not None else QModelIndex()

	def index(self, row, column=0, parent=QModelIndex()):
		"""
		Reimplements the :meth:`QAbstractItemModel.index` method.
		
		:param row: Row.
		:type row: int
		:param column: Column.
		:type column: int
		:param parent: Parent.
		:type parent: QModelIndex
		:return: Index.
		:rtype: QModelIndex
		"""

		parentNode = self.getNode(parent)
		child = parentNode.child(row)
		if child:
			return self.createIndex(row, column, child)
		else:
			return QModelIndex()

	def sort(self, column, order=Qt.AscendingOrder):
		"""
		Reimplements the :meth:`QAbstractItemModel.sort` method.
		
		:param column: Column.
		:type column: int
		:param order: Order. ( Qt.SortOrder )
		"""

		if column > self.columnCount():
			return

		self.beginResetModel()
		if column == 0:
			self.__rootNode.sortChildren(reverseOrder=order)
		else:
			self.__rootNode.sortChildren(attribute=self.__horizontalHeaders[self.__horizontalHeaders.keys()[column]],
										reverseOrder=order)
		self.endResetModel()

	def insertRows(self, row, count, parent=QModelIndex()):
		"""
		Reimplements the :meth:`QAbstractItemModel.insertRows` method.
		
		:param row: Row.
		:type row: int
		:param count: Count.
		:type count: int
		:param parent: Parent.
		:type parent: QModelIndex
		:return: Method success.
		:rtype: bool
		"""

		parentNode = self.getNode(parent)
		self.beginInsertRows(parent, row, row + count - 1)
		success = True
		for i in range(count):
			childNode = self.__defaultNode()
			success *= True if parentNode.insertChild(childNode, row) else False
		self.endInsertRows()
		return success

	def removeRows(self, row, count, parent=QModelIndex()):
		"""
		Reimplements the :meth:`QAbstractItemModel.removeRows` method.
		
		:param row: Row.
		:type row: int
		:param count: Count.
		:type count: int
		:param parent: Parent.
		:type parent: QModelIndex
		:return: Method success.
		:rtype: bool
		"""

		parentNode = self.getNode(parent)
		self.beginRemoveRows(parent, row, row + count - 1)
		success = True
		for i in range(count):
			success *= True if parentNode.removeChild(row) else False
		self.endRemoveRows()
		return success

	def movesRows(self, fromParent, fromFirstRow, fromLastRow, toParent, toRow):
		"""
		Moves given rows from parent to parent row.
		"""

		return True

	def mimeTypes(self):
		"""
		Reimplements the :meth:`QAbstractItemModel.mimeTypes` method.
		
		:return: Mime types.
		:rtype: QStringList
		"""

		types = QStringList()
		types.append("application/x-umbragraphmodeldatalist")
		return types

	def mimeData(self, indexes):
		"""
		Reimplements the :meth:`QAbstractItemModel.mimeData` method.
		
		:param indexes: Indexes.
		:type indexes: QModelIndexList
		:return: MimeData.
		:rtype: QMimeData
		"""

		byteStream = pickle.dumps([self.getNode(index) for index in indexes], pickle.HIGHEST_PROTOCOL)
		mimeData = QMimeData()
		mimeData.setData("application/x-umbragraphmodeldatalist", byteStream)
		return mimeData

	def clear(self):
		"""
		Clears the Model.
		
		:return: Method success.
		:rtype: bool
		"""

		self.beginResetModel()
		self.rootNode.children = []
		self.endResetModel()

	def hasNodes(self):
		"""
		Returns if Model has nodes.
		
		:return: Has children.
		:rtype: bool
		"""

		return True if self.__rootNode.children else False

	def getNode(self, index):
		"""
		Returns the Node at given index.
		
		:param index: Index.
		:type index: QModelIndex
		:return: Node.
		:rtype: AbstractCompositeNode or GraphModelNode
		"""

		if not index.isValid():
			return self.__rootNode
		return index.internalPointer() or self.__rootNode

	def getAttribute(self, node, column):
		"""
		Returns the given Node attribute associated to the given column.
		
		:param node: Node.
		:type node: AbstractCompositeNode or GraphModelNode
		:param column: Column.
		:type column: int
		:return: Attribute.
		:rtype: Attribute
		"""

		if column > 0 and column < len(self.__horizontalHeaders):
			return node.get(self.__horizontalHeaders[self.__horizontalHeaders.keys()[column]], None)

	def getNodeIndex(self, node):
		"""
		Returns given Node index.
		
		:param node: Node.
		:type node: AbstractCompositeNode or GraphModelNode
		:return: Index.
		:rtype: QModelIndex
		"""

		if node == self.__rootNode:
			return QModelIndex()
		else:
			row = node.row()
			return self.createIndex(row, 0, node) if row is not None else QModelIndex()

	def getAttributeIndex(self, node, column):
		"""
		Returns given Node attribute index at given column.
		
		:param node: Node.
		:type node: AbstractCompositeNode or GraphModelNode
		:param column: Attribute column.
		:type column: int
		:return: Index.
		:rtype: QModelIndex
		"""

		if column > 0 and column < len(self.__horizontalHeaders):
			row = node.row()
			return self.createIndex(row, column, node) if row is not None else QModelIndex()

	def findChildren(self, pattern=".*", flags=0):
		"""
		Finds the children matching the given patten.
		
		:param pattern: Matching pattern.
		:type pattern: unicode
		:param flags: Matching regex flags.
		:type flags: int
		:return: Matching children.
		:rtype: list
		"""

		return self.__rootNode.findChildren(pattern, flags)

	def findFamily(self, pattern=r".*", flags=0, node=None):
		"""
		Returns the Nodes from given family.
		
		:param pattern: Matching pattern.
		:type pattern: unicode
		:param flags: Matching regex flags.
		:type flags: int
		:param node: Node to start walking from.
		:type node: AbstractNode or AbstractCompositeNode or GraphModelNode
		:return: Family nodes.
		:rtype: list
		"""

		return self.__rootNode.findFamily(pattern, flags, node or self.__rootNode)

#	@foundations.decorators.memoize(cache=None)
	def findNode(self, attribute):
		"""
		Returns the Node with given attribute.
		
		:param attribute: Attribute.
		:type attribute: GraphModelAttribute
		:return: Node.
		:rtype: GraphModelNode
		"""

		for model in GraphModel._GraphModel__modelsInstances.itervalues():
			for node in foundations.walkers.nodesWalker(model.rootNode):
				if attribute in node.getAttributes():
					return node

	@staticmethod
#	@foundations.decorators.memoize(cache=None)
	def findModel(object):
		"""
		Returns the model(s) associated with given object.
		
		:param object: Node / Attribute.
		:type object: GraphModelNode or GraphModelAttribute
		:return: Model(s).
		:rtype: list
		"""

		models = []
		for model in GraphModel._GraphModel__modelsInstances.itervalues():
			for node in foundations.walkers.nodesWalker(model.rootNode):
				if node is object:
					models.append(model)

				for attribute in node.getAttributes():
					if attribute is object:
						models.append(model)
		return models

	def enableModelTriggers(self, state):
		"""
		Enables Model Nodes and attributes triggers.
		
		:param state: Inform model state.
		:type state: bool
		:return: Method success.
		:rtype: bool
		"""

		for node in foundations.walkers.nodesWalker(self.rootNode):
			node.triggerModel = state

			for attribute in node.getAttributes():
				attribute.triggerModel = state

	def nodeChanged(self, node):
		"""
		Calls :meth:`QAbstractItemModel.dataChanged` with given Node index.
		
		:param node: Node.
		:type node: AbstractCompositeNode or GraphModelNode
		:return: Method success.
		:rtype: bool
		"""

		index = self.getNodeIndex(node)
		if index is not None:
			self.dataChanged.emit(index, index)
			return True
		else:
			return False

	def attributeChanged(self, node, column):
		"""
		Calls :meth:`QAbstractItemModel.dataChanged` with given Node attribute index.
		
		:param node: Node.
		:type node: AbstractCompositeNode or GraphModelNode
		:param column: Attribute column.
		:type column: int
		:return: Method success.
		:rtype: bool
		"""

		index = self.getAttributeIndex(node, column)
		if index is not None:
			self.dataChanged.emit(index, index)
			return True
		else:
			return False
