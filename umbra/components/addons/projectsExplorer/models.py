#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`umbra.components.factory.projectsExplorer.projectsExplorer.ProjectsExplorer`
	Component Interface class Models.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QSortFilterProxyModel

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.verbose
from umbra.components.factory.scriptEditor.nodes import EditorNode

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "ProjectsProxyModel"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ProjectsProxyModel(QSortFilterProxyModel):
	"""
	This class defines the proxy Model used the by 
	:class:`umbra.components.factory.projectsExplorer.projectsExplorer.ProjectsExplorer` Component Interface class. 
	"""

	def __init__(self, parent, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QSortFilterProxyModel.__init__(self, parent, *args, **kwargs)

		# --- Setting class attributes. ---
		color = "rgb({0}, {1}, {2})"
		self.__editorNodeFormat = "<span>{0}</span>"
		self.__fileNodeFormat = "<span style=\"color: {0};\">{{0}}</span>".format(color.format(160, 160, 160))
		self.__directoryNodeFormat = "{0}"
		self.__projectNodeFormat = "<b>{0}</b>"
		self.__defaultProjectNodeFormat = "<b>Open Files</b>"

	#******************************************************************************************************************
	#***	Class methods
	#******************************************************************************************************************
	def filterAcceptsRow(self, row, parent):
		"""
		This method reimplements the :meth:`QSortFilterProxyModel.filterAcceptsRow` method.
		
		:param row: Source row. ( Integer )
		:param parent: Source parent. ( QModelIndex )
		:return: Filter result ( Boolean )
		"""

		child = self.sourceModel().getNode(parent).child(row)
		if isinstance(child, EditorNode):
			return False

		return True

	def data(self, index, role=Qt.DisplayRole):
		"""
		This method reimplements the :meth:`QSortFilterProxyModel.data` method.
		
		:param index: Index. ( QModelIndex )
		:param role: Role. ( Integer )
		:return: Data. ( QVariant )
		"""

		if role == Qt.DisplayRole:
			node = self.getNode(index)
			if node.family == "Editor":
				data = self.__editorNodeFormat.format(node.name)
			elif node.family == "File":
				data = self.__fileNodeFormat.format(node.name)
			elif node.family == "Directory":
				data = self.__directoryNodeFormat.format(node.name)
			elif node.family == "Project":
				if node is self.sourceModel().defaultProjectNode:
					data = self.__defaultProjectNodeFormat.format(node.name)
				else:
					data = self.__projectNodeFormat.format(node.name)
			else:
				data = QVariant()
			return data
		else:
			return QSortFilterProxyModel.data(self, index, role)

	def getNode(self, index):
		"""
		This method returns the Node at given index.
		
		:param index: Index. ( QModelIndex )
		:return: Node. ( AbstractCompositeNode )
		"""

		index = self.mapToSource(index)
		if not index.isValid():
			return self.sourceModel().rootNode

		return index.internalPointer() or self.sourceModel().rootNode

	def getAttribute(self, *args):
		"""
		This method reimplements requisite method.
		"""

		pass
