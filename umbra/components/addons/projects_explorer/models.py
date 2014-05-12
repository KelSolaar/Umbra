#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`umbra.components.factory.projects_explorer.projects_explorer.ProjectsExplorer`
    Component Interface class Models.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QSortFilterProxyModel

import foundations.verbose
from umbra.components.factory.script_editor.nodes import EditorNode

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "ProjectsProxyModel"]

LOGGER = foundations.verbose.install_logger()


class ProjectsProxyModel(QSortFilterProxyModel):
    """
    Defines the proxy Model used by the
    :class:`umbra.components.factory.projects_explorer.projects_explorer.ProjectsExplorer` Component Interface class.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initializes the class.

        :param parent: Object parent.
        :type parent: QObject
        :param \*args: Arguments.
        :type \*args: \*
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        QSortFilterProxyModel.__init__(self, parent, *args, **kwargs)

        # --- Setting class attributes. ---
        color = "rgb({0}, {1}, {2})"
        self.__editor_node_format = "<span>{0}</span>"
        self.__file_node_format = "<span style=\"color: {0};\">{{0}}</span>".format(color.format(160, 160, 160))
        self.__directory_node_format = "{0}"
        self.__project_node_format = "<b>{0}</b>"
        self.__default_project_node_format = "<b>Open Files</b>"

    def filterAcceptsRow(self, row, parent):
        """
        Reimplements the :meth:`QSortFilterProxyModel.filterAcceptsRow` method.

        :param row: Source row.
        :type row: int
        :param parent: Source parent.
        :type parent: QModelIndex
        :return: Filter result
        :rtype: bool
        """

        child = self.sourceModel().get_node(parent).child(row)
        if isinstance(child, EditorNode):
            return False

        return True

    def data(self, index, role=Qt.DisplayRole):
        """
        Reimplements the :meth:`QSortFilterProxyModel.data` method.

        :param index: Index.
        :type index: QModelIndex
        :param role: Role.
        :type role: int
        :return: Data.
        :rtype: QVariant
        """

        if role == Qt.DisplayRole:
            node = self.get_node(index)
            if node.family == "Editor":
                data = self.__editor_node_format.format(node.name)
            elif node.family == "File":
                data = self.__file_node_format.format(node.name)
            elif node.family == "Directory":
                data = self.__directory_node_format.format(node.name)
            elif node.family == "Project":
                if node is self.sourceModel().default_project_node:
                    data = self.__default_project_node_format.format(node.name)
                else:
                    data = self.__project_node_format.format(node.name)
            else:
                data = QVariant()
            return data
        else:
            return QSortFilterProxyModel.data(self, index, role)

    def get_node(self, index):
        """
        Returns the Node at given index.

        :param index: Index.
        :type index: QModelIndex
        :return: Node.
        :rtype: AbstractCompositeNode
        """

        index = self.mapToSource(index)
        if not index.isValid():
            return self.sourceModel().root_node

        return index.internalPointer() or self.sourceModel().root_node

    def get_attribute(self, *args):
        """
        Reimplements requisite method.
        """

        pass
