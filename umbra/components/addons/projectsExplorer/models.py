#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`umbra.components.factory.projectsExplorer.projectsExplorer.ProjectsExplorer`
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
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Defines the proxy Model used by the 
	:class:`umbra.components.factory.projectsExplorer.projectsExplorer.ProjectsExplorer` Component Interface class. 
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
		Reimplements the :meth:`QSortFilterProxyModel.filterAcceptsRow` method.
		
		:param row: Source row.
		:type row: int
		:param parent: Source parent.
		:type parent: QModelIndex
		:return: Filter result
		:rtype: bool
		"""

		child = self.sourceModel().getNode(parent).child(row)
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
		Returns the Node at given index.
		
		:param index: Index.
		:type index: QModelIndex
		:return: Node.
		:rtype: AbstractCompositeNode
		"""

		index = self.mapToSource(index)
		if not index.isValid():
			return self.sourceModel().rootNode

		return index.internalPointer() or self.sourceModel().rootNode

	def getAttribute(self, *args):
		"""
		Reimplements requisite method.
		"""

		pass
