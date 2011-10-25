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
from foundations.dag import Attribute, AbstractCompositeNode
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

__all__ = ["LOGGER", "GraphModelAttribute", "getGraphModelNode", "DefaultNode", "GraphModel"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class GraphModelAttribute(Attribute):
	"""
	This class represents a storage object for the :class:`GraphModelNode` class attributes.
	"""

	@core.executionTrace
	def __init__(self, name=None, value=None, roles=None, flags=None, **kwargs):
		"""
		This method initializes the class.

		:param name: Attribute name. ( String )
		:param value: Attribute value. ( Object )
		:param roles: Roles. ( Dictionary )
		:param flags: Flags. ( Qt.ItemFlag )
		:param \*\*kwargs: Keywords arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		Attribute.__init__(self, name, value, **kwargs)

		# --- Setting class attributes. ---
		self.__roles = None
		self.roles = roles or {Qt.DisplayRole : value, Qt.EditRole : value}
		self.__flags = None
		self.flags = flags or Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def roles(self):
		"""
		This method is the property for **self.__roles** attribute.
	
		:return: self.__roles. ( Dictionary )
		"""

		return self.__roles

	@roles.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def roles(self, value):
		"""
		This method is the setter method for **self.__roles** attribute.
	
		:param value: Attribute value. ( Dictionary )
		"""

		if value:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("roles", value)
		self.__roles = value

	@roles.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def roles(self):
		"""
		This method is the deleter method for **self.__roles** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "roles"))

	@property
	def flags(self):
		"""
		This method is the property for **self.__flags** attribute.
	
		:return: self.__flags. ( Integer )
		"""

		return self.__flags

	@flags.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def flags(self, value):
		"""
		This method is the setter method for **self.__flags** attribute.
	
		:param value: Attribute value. ( Integer )
		"""

		if value:
			assert hasattr(value, "__int__"), "'{0}' attribute: '{1}' type is not 'int'!".format("flags", value)
		self.__flags = value

	@flags.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def flags(self):
		"""
		This method is the deleter method for **self.__flags** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "flags"))

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getGraphModelNode(dbItem):
	"""
	This definition is a class factory creating :class:`GraphModelNode` classes using given database object.

	:param dbItem: Database item. ( Object )
	:return: GraphModelNode class. ( GraphModelNode )
	"""

	class GraphModelNode(AbstractCompositeNode):
		"""
		This class is built by the :def:`getGraphModelNode` definition.
		"""

		__family = "GraphModelNode"

		@core.executionTrace
		def __init__(self, name=None, parent=None, children=None, roles=None, flags=None, ** kwargs):
			"""
			This method initializes the class.
	
			:param name: Node name.  ( String )
			:param parent: Node parent. ( AbstractNode / AbstractCompositeNode )
			:param children: Children. ( List )
			:param roles: Roles. ( Dictionary )
			:param flags: Flags. ( Qt.ItemFlag )
			:param \*\*kwargs: Keywords arguments. ( \* )
			"""

			LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

			AbstractCompositeNode.__init__(self, name, parent, children, **kwargs)

			# --- Setting class attributes. ---
			self.__roles = None
			self.roles = roles or {Qt.DisplayRole : name, Qt.EditRole : name}
			self.__flags = None
			self.flags = flags or Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled

			self.__dbItem = dbItem

		#***********************************************************************************************
		#***	Attributes properties.
		#***********************************************************************************************
		@property
		def name(self):
			"""
			This method is the property for **self.__name** attribute.
	
			:return: self.__name. ( String )
			"""

			return self.__name

		@name.setter
		@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
		def name(self, value):
			"""
			This method is the setter method for **self.__name** attribute.
	
			:param value: Attribute value. ( String )
			"""

			if value:
				assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("name", value)
			self.__name = value

		@name.deleter
		@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
		def name(self):
			"""
			This method is the deleter method for **self.__name** attribute.
			"""

			raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "name"))

		@property
		def roles(self):
			"""
			This method is the property for **self.__roles** attribute.
	
			:return: self.__roles. ( Dictionary )
			"""

			return self.__roles

		@roles.setter
		@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
		def roles(self, value):
			"""
			This method is the setter method for **self.__roles** attribute.
	
			:param value: Attribute value. ( Dictionary )
			"""

			if value:
				assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("roles", value)
			self.__roles = value

		@roles.deleter
		@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
		def roles(self):
			"""
			This method is the deleter method for **self.__roles** attribute.
			"""

			raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "roles"))

		@property
		def flags(self):
			"""
			This method is the property for **self.__flags** attribute.
		
			:return: self.__flags. ( Integer )
			"""

			return self.__flags

		@flags.setter
		@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
		def flags(self, value):
			"""
			This method is the setter method for **self.__flags** attribute.
		
			:param value: Attribute value. ( Integer )
			"""

			if value:
				assert hasattr(value, "__int__"), "'{0}' attribute: '{1}' type is not 'int'!".format("flags", value)
			self.__flags = value

		@flags.deleter
		@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
		def flags(self):
			"""
			This method is the deleter method for **self.__flags** attribute.
			"""

			raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "flags"))

		@property
		def dbItem(self):
			"""
			This method is the property for **self.__dbItem** attribute.
	
			:return: self.__dbItem. ( Object )
			"""

			return self.__dbItem

		@dbItem.setter
		@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
		def dbItem(self, value):
			"""
			This method is the setter method for **self.__dbItem** attribute.
	
			:param value: Attribute value. ( Object )
			"""

			raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dbItem"))

		@dbItem.deleter
		@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
		def dbItem(self):
			"""
			This method is the deleter method for **self.__dbItem** attribute.
			"""

			raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dbItem"))

		#***********************************************************************************************
		#***	Class methods.
		#***********************************************************************************************
		@core.executionTrace
		@foundations.exceptions.exceptionsHandler(None, False, Exception)
		def synchronizeNodeAttributes(self):
			"""
			This method synchronizes the node attributes from the dbItem.
			
			:return: Method success. ( Boolean )
			"""

			for column in self.__dbItem.__table__.columns:
				attribute = column.key
				value = getattr(dbItem, attribute)
				if not attribute in self.keys():
					break

				if issubclass(self[attribute].__class__, GraphModelAttribute):
						self[attribute] = value
			return True

		@core.executionTrace
		@foundations.exceptions.exceptionsHandler(None, False, Exception)
		def synchronizeDbItem(self):
			"""
			This method synchronizes the dbItem from the node attributes.

			:return: Method success. ( Boolean )
			"""

			for column in self.__dbItem.__table__.columns:
				attribute = column.key
				if not attribute in self.keys():
					break

				if issubclass(self[attribute].__class__, GraphModelAttribute):
						setattr(self.__dbItem, attribute, self[attribute].value)
			return True

	attributes = {}
	for column in dbItem.__table__.columns:
		attribute = column.key
		value = getattr(dbItem, attribute)
		roles = {Qt.DisplayRole : value,
				Qt.EditRole : value}
		flags = {}
		attributes[attribute] = GraphModelAttribute(attribute, value, roles, flags)

	return GraphModelNode, attributes

class DefaultNode(AbstractCompositeNode):
	"""
	| This class defines the default node used in :class:`GraphModel` class model.
	| Usually this node is used as an invisible root for graphs.
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
	def __init__(self, parent=None, rootNode=None, horizontalHeaders=None, verticalHeaders=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param rootNode: Root node. ( AbstractCompositeNode )
		:param horizontalHeaders: Headers. ( OrderedDict )
		:param verticalHeaders: Headers. ( OrderedDict )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QAbstractItemModel.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__rootNode = None
		self.rootNode = rootNode or DefaultNode(name="InvisibleRootNode")
		self.__horizontalHeaders = None
		self.horizontalHeaders = horizontalHeaders or OrderedDict([("Graph Model", "graphModel")])
		self.__verticalHeaders = None
		self.verticalHeaders = verticalHeaders or OrderedDict()

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
			assert issubclass(value.__class__, AbstractCompositeNode), "'{0}' attribute: '{1}' is not a '{2}' subclass!".format("rootNode", value, AbstractCompositeNode.__name__)
		self.__rootNode = value

	@rootNode.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def rootNode(self):
		"""
		This method is the deleter method for **self.__rootNode** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "rootNode"))

	@property
	def horizontalHeaders(self):
		"""
		This method is the property for **self.__horizontalHeaders** attribute.

		:return: self.__horizontalHeaders. ( OrderedDict )
		"""

		return self.__horizontalHeaders

	@horizontalHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def horizontalHeaders(self, value):
		"""
		This method is the setter method for **self.__horizontalHeaders** attribute.

		:param value: Attribute value. ( OrderedDict )
		"""

		if value:
			assert type(value) is OrderedDict, "'{0}' attribute: '{1}' type is not 'OrderedDict'!".format("horizontalHeaders", value)
		self.__horizontalHeaders = value

	@horizontalHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def horizontalHeaders(self):
		"""
		This method is the deleter method for **self.__horizontalHeaders** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "horizontalHeaders"))

	@property
	def verticalHeaders(self):
		"""
		This method is the property for **self.__verticalHeaders** attribute.

		:return: self.__verticalHeaders. ( OrderedDict )
		"""

		return self.__verticalHeaders

	@verticalHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def verticalHeaders(self, value):
		"""
		This method is the setter method for **self.__verticalHeaders** attribute.

		:param value: Attribute value. ( OrderedDict )
		"""

		if value:
			assert type(value) is OrderedDict, "'{0}' attribute: '{1}' type is not 'OrderedDict'!".format("verticalHeaders", value)
		self.__verticalHeaders = value

	@verticalHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def verticalHeaders(self):
		"""
		This method is the deleter method for **self.__verticalHeaders** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "verticalHeaders"))

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

		return len(self.__horizontalHeaders.keys())

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

		node = self.getNode(index)
		if index.column() == 0:
			return node.roles.get(role, None) or QVariant()
		else:
			attribute = self.getAttribute(node, index.column())
			return attribute.roles.get(role, None) or QVariant()

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

		if not index.isValid():
			return False

		node = self.getNode(index)
		if role == Qt.DisplayRole or role == Qt.EditRole:
			value = unicode(value.toString(), Constants.encodingFormat, Constants.encodingError)
			roles = {Qt.DisplayRole : value, Qt.EditRole : value}
		else:
			roles = {role : value}

		if index.column() == 0:
			node.roles.update(roles)
			node.name = value
		else:
			attribute = self.getAttribute(node, index.column())
			attribute.roles.update(roles)
			attribute.value = value

		self.dataChanged.emit(index, index)
		return True

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
				if section < len(self.__horizontalHeaders.keys()):
					return self.__horizontalHeaders.keys()[section]
			elif orientation == Qt.Vertical:
				if section < len(self.__verticalHeaders.keys()):
					return self.__verticalHeaders.keys()[section]
		return QVariant()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def flags(self, index):
		"""
		This method reimplements the :meth:`QAbstractItemModel.flags` method.
		
		:param index: Index. ( QModelIndex )
		:return: Flags. ( Qt.ItemFlags )
		"""

		if not index.isValid():
			return Qt.NoItemFlags

		node = self.getNode(index)
		if index.column() == 0:
			return node.flags
		else:
			attribute = self.getAttribute(node, index.column())
			return attribute.flags

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def parent(self, index):
		"""
		This method reimplements the :meth:`QAbstractItemModel.parent` method.
		
		:param index: Index. ( QModelIndex )
		:return: Parent. ( QModelIndex )
		"""

		if not index.isValid():
			return QModelIndex()

		node = self.getNode(index)
		parentNode = node.parent
		if parentNode == self.__rootNode:
			return QModelIndex()
		return self.createIndex(parentNode.row(), 0, parentNode)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def index(self, row, column=0, parent=QModelIndex()):
		"""
		This method reimplements the :meth:`QAbstractItemModel.index` method.
		
		:param row: Row. ( Integer )
		:param column: Column. ( Integer )
		:param parent: Parent. ( QModelIndex )
		:return: Index. ( QModelIndex )
		"""

		parentNode = self.getNode(parent)
		child = parentNode.child(row)
		if child:
			return self.createIndex(row, column, child)
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

		if not index.isValid():
			return self.__rootNode
		return index.internalPointer() or self.__rootNode

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getAttribute(self, node, column):
		"""
		This method returns the given node attribute associated to the given column.
		
		:param node: Node. ( AbstractCompositeNode )
		:param column: Column. ( Integer )
		:return: Attribute. ( Attribute )
		"""

		if column > 0 and column < len(self.__horizontalHeaders.keys()):
			return node.get(self.__horizontalHeaders[self.__horizontalHeaders.keys()[column]], None)
