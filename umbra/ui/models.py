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

from __future__ import unicode_literals

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

import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.ui.nodes
from foundations.nodes import AbstractCompositeNode

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "GraphModel"]

LOGGER = foundations.verbose.install_logger()


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

    __models_instances = weakref.WeakValueDictionary()
    """
    :param __models_instances: Models instances.
    :type __models_instances: dict
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

        GraphModel._GraphModel__models_instances[id(instance)] = instance
        return instance

    def __init__(self,
                 parent=None,
                 root_node=None,
                 horizontal_headers=None,
                 vertical_headers=None,
                 default_node=None):
        """
        Initializes the class.

        :param parent: Object parent.
        :type parent: QObject
        :param root_node: Root node.
        :type root_node: AbstractCompositeNode or GraphModelNode
        :param horizontal_headers: Headers.
        :type horizontal_headers: OrderedDict
        :param vertical_headers: Headers.
        :type vertical_headers: OrderedDict
        :param default_node: Default node.
        :type default_node: AbstractCompositeNode or GraphModelNode
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        QAbstractItemModel.__init__(self, parent)

        # --- Setting class attributes. ---
        self.__root_node = None
        self.root_node = root_node or umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")
        self.__horizontal_headers = None
        self.horizontal_headers = horizontal_headers or OrderedDict([("Graph Model", "graphModel")])
        self.__vertical_headers = None
        self.vertical_headers = vertical_headers or OrderedDict()
        self.__default_node = None
        self.default_node = default_node or umbra.ui.nodes.GraphModelNode

    @property
    def root_node(self):
        """
        Property for **self.__root_node** attribute.

        :return: self.__root_node.
        :rtype: AbstractCompositeNode or GraphModelNode
        """

        return self.__root_node

    @root_node.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def root_node(self, value):
        """
        Setter for **self.__root_node** attribute.

        :param value: Attribute value.
        :type value: AbstractCompositeNode or GraphModelNode
        """

        if value is not None:
            assert issubclass(value.__class__, AbstractCompositeNode), \
                "'{0}' attribute: '{1}' is not a '{2}' subclass!".format(
                    "root_node", value, AbstractCompositeNode.__name__)
        self.__root_node = value

    @root_node.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def root_node(self):
        """
        Deleter for **self.__root_node** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "root_node"))

    @property
    def horizontal_headers(self):
        """
        Property for **self.__horizontal_headers** attribute.

        :return: self.__horizontal_headers.
        :rtype: OrderedDict
        """

        return self.__horizontal_headers

    @horizontal_headers.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def horizontal_headers(self, value):
        """
        Setter for **self.__horizontal_headers** attribute.

        :param value: Attribute value.
        :type value: OrderedDict
        """

        if value is not None:
            assert type(value) is OrderedDict, "'{0}' attribute: '{1}' type is not 'OrderedDict'!".format(
                "horizontal_headers", value)
        self.__horizontal_headers = value

    @horizontal_headers.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def horizontal_headers(self):
        """
        Deleter for **self.__horizontal_headers** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "horizontal_headers"))

    @property
    def vertical_headers(self):
        """
        Property for **self.__vertical_headers** attribute.

        :return: self.__vertical_headers.
        :rtype: OrderedDict
        """

        return self.__vertical_headers

    @vertical_headers.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def vertical_headers(self, value):
        """
        Setter for **self.__vertical_headers** attribute.

        :param value: Attribute value.
        :type value: OrderedDict
        """

        if value is not None:
            assert type(value) is OrderedDict, "'{0}' attribute: '{1}' type is not 'OrderedDict'!".format(
                "vertical_headers", value)
        self.__vertical_headers = value

    @vertical_headers.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def vertical_headers(self):
        """
        Deleter for **self.__vertical_headers** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "vertical_headers"))

    @property
    def default_node(self):
        """
        Property for **self.__default_node** attribute.

        :return: self.__default_node.
        :rtype: AbstractCompositeNode or GraphModelNode
        """

        return self.__default_node

    @default_node.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def default_node(self, value):
        """
        Setter for **self.__default_node** attribute.

        :param value: Attribute value.
        :type value: AbstractCompositeNode or GraphModelNode
        """

        if value is not None:
            assert issubclass(value, AbstractCompositeNode), \
                "'{0}' attribute: '{1}' is not a '{2}' subclass!".format(
                    "default_node", value, AbstractCompositeNode.__name__)
        self.__default_node = value

    @default_node.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_node(self):
        """
        Deleter for **self.__default_node** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_node"))

    def rowCount(self, parent=QModelIndex()):
        """
        Reimplements the :meth:`QAbstractItemModel.rowCount` method.

        :param parent: Parent node.
        :type parent: AbstractCompositeNode or GraphModelNode
        :return: Row count.
        :rtype: int
        """

        if not parent.isValid():
            parent_node = self.__root_node
        else:
            parent_node = parent.internalPointer()
        return parent_node.children_count()

    def columnCount(self, parent=QModelIndex()):
        """
        Reimplements the :meth:`QAbstractItemModel.columnCount` method.

        :param parent: Parent node.
        :type parent: AbstractCompositeNode or GraphModelNode
        :return: Column count.
        :rtype: int
        """

        return len(self.__horizontal_headers)

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

        node = self.get_node(index)
        if index.column() == 0:
            if hasattr(node, "roles"):
                if role == Qt.DecorationRole:
                    return QIcon(node.roles.get(role, ""))
                else:
                    return node.roles.get(role, QVariant())
        else:
            attribute = self.get_attribute(node, index.column())
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

        node = self.get_node(index)
        if role == Qt.DisplayRole or role == Qt.EditRole:
            value = foundations.strings.to_string(value.toString())
            roles = {Qt.DisplayRole: value, Qt.EditRole: value}
        else:
            roles = {role: value}

        if index.column() == 0:
            if (node and hasattr(node, "roles")):
                node.roles.update(roles)
                node.name = value
        else:
            attribute = self.get_attribute(node, index.column())
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
                if section < len(self.__horizontal_headers):
                    return self.__horizontal_headers.keys()[section]
            elif orientation == Qt.Vertical:
                if section < len(self.__vertical_headers):
                    return self.__vertical_headers.keys()[section]
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

        node = self.get_node(index)
        if index.column() == 0:
            return hasattr(node, "flags") and Qt.ItemFlags(node.flags) or Qt.NoItemFlags
        else:
            attribute = self.get_attribute(node, index.column())
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

        node = self.get_node(index)
        parent_node = node.parent
        if not parent_node:
            return QModelIndex()

        if parent_node == self.__root_node:
            return QModelIndex()

        row = parent_node.row()
        return self.createIndex(row, 0, parent_node) if row is not None else QModelIndex()

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

        parent_node = self.get_node(parent)
        child = parent_node.child(row)
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
            self.__root_node.sort_children(reverse_order=order)
        else:
            self.__root_node.sort_children(
                attribute=self.__horizontal_headers[self.__horizontal_headers.keys()[column]],
                reverse_order=order)
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

        parent_node = self.get_node(parent)
        self.beginInsertRows(parent, row, row + count - 1)
        success = True
        for i in range(count):
            childNode = self.__default_node()
            success *= True if parent_node.insert_child(childNode, row) else False
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

        parent_node = self.get_node(parent)
        self.beginRemoveRows(parent, row, row + count - 1)
        success = True
        for i in range(count):
            success *= True if parent_node.remove_child(row) else False
        self.endRemoveRows()
        return success

    def movesRows(self, from_parent, from_first_row, from_last_row, to_parent, to_row):
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

        byte_stream = pickle.dumps([self.get_node(index) for index in indexes], pickle.HIGHEST_PROTOCOL)
        mime_data = QMimeData()
        mime_data.setData("application/x-umbragraphmodeldatalist", byte_stream)
        return mime_data

    def clear(self):
        """
        Clears the Model.

        :return: Method success.
        :rtype: bool
        """

        self.beginResetModel()
        self.root_node.children = []
        self.endResetModel()

    def has_nodes(self):
        """
        Returns if Model has nodes.

        :return: Has children.
        :rtype: bool
        """

        return True if self.__root_node.children else False

    def get_node(self, index):
        """
        Returns the Node at given index.

        :param index: Index.
        :type index: QModelIndex
        :return: Node.
        :rtype: AbstractCompositeNode or GraphModelNode
        """

        if not index.isValid():
            return self.__root_node
        return index.internalPointer() or self.__root_node

    def get_attribute(self, node, column):
        """
        Returns the given Node attribute associated to the given column.

        :param node: Node.
        :type node: AbstractCompositeNode or GraphModelNode
        :param column: Column.
        :type column: int
        :return: Attribute.
        :rtype: Attribute
        """

        if column > 0 and column < len(self.__horizontal_headers):
            return node.get(self.__horizontal_headers[self.__horizontal_headers.keys()[column]], None)

    def get_node_index(self, node):
        """
        Returns given Node index.

        :param node: Node.
        :type node: AbstractCompositeNode or GraphModelNode
        :return: Index.
        :rtype: QModelIndex
        """

        if node == self.__root_node:
            return QModelIndex()
        else:
            row = node.row()
            return self.createIndex(row, 0, node) if row is not None else QModelIndex()

    def get_attribute_index(self, node, column):
        """
        Returns given Node attribute index at given column.

        :param node: Node.
        :type node: AbstractCompositeNode or GraphModelNode
        :param column: Attribute column.
        :type column: int
        :return: Index.
        :rtype: QModelIndex
        """

        if column > 0 and column < len(self.__horizontal_headers):
            row = node.row()
            return self.createIndex(row, column, node) if row is not None else QModelIndex()

    def find_children(self, pattern=".*", flags=0):
        """
        Finds the children matching the given patten.

        :param pattern: Matching pattern.
        :type pattern: unicode
        :param flags: Matching regex flags.
        :type flags: int
        :return: Matching children.
        :rtype: list
        """

        return self.__root_node.find_children(pattern, flags)

    def find_family(self, pattern=r".*", flags=0, node=None):
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

        return self.__root_node.find_family(pattern, flags, node or self.__root_node)

    # @foundations.decorators.memoize(cache=None)
    def find_node(self, attribute):
        """
        Returns the Node with given attribute.

        :param attribute: Attribute.
        :type attribute: GraphModelAttribute
        :return: Node.
        :rtype: GraphModelNode
        """

        for model in GraphModel._GraphModel__models_instances.itervalues():
            for node in foundations.walkers.nodes_walker(model.root_node):
                if attribute in node.get_attributes():
                    return node

    @staticmethod
    # @foundations.decorators.memoize(cache=None)
    def find_model(object):
        """
        Returns the model(s) associated with given object.

        :param object: Node / Attribute.
        :type object: GraphModelNode or GraphModelAttribute
        :return: Model(s).
        :rtype: list
        """

        models = []
        for model in GraphModel._GraphModel__models_instances.itervalues():
            for node in foundations.walkers.nodes_walker(model.root_node):
                if node is object:
                    models.append(model)

                for attribute in node.get_attributes():
                    if attribute is object:
                        models.append(model)
        return models

    def enable_model_triggers(self, state):
        """
        Enables Model Nodes and attributes triggers.

        :param state: Inform model state.
        :type state: bool
        :return: Method success.
        :rtype: bool
        """

        for node in foundations.walkers.nodes_walker(self.root_node):
            node.trigger_model = state

            for attribute in node.get_attributes():
                attribute.trigger_model = state

    def node_changed(self, node):
        """
        Calls :meth:`QAbstractItemModel.dataChanged` with given Node index.

        :param node: Node.
        :type node: AbstractCompositeNode or GraphModelNode
        :return: Method success.
        :rtype: bool
        """

        index = self.get_node_index(node)
        if index is not None:
            self.dataChanged.emit(index, index)
            return True
        else:
            return False

    def attribute_changed(self, node, column):
        """
        Calls :meth:`QAbstractItemModel.dataChanged` with given Node attribute index.

        :param node: Node.
        :type node: AbstractCompositeNode or GraphModelNode
        :param column: Attribute column.
        :type column: int
        :return: Method success.
        :rtype: bool
        """

        index = self.get_attribute_index(node, column)
        if index is not None:
            self.dataChanged.emit(index, index)
            return True
        else:
            return False
