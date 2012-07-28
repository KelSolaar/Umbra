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
#***	External imports.
#**********************************************************************************************************************
import logging
from PyQt4.QtGui import QSortFilterProxyModel

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
from umbra.components.factory.scriptEditor.nodes import EditorNode
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

__all__ = ["LOGGER", "ProjectsProxyModel"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ProjectsProxyModel(QSortFilterProxyModel):
	"""
	This class defines the proxy Model used the by 
	:class:`umbra.components.factory.projectsExplorer.projectsExplorer.ProjectsExplorer` Component Interface class. 
	"""

	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
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

	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getNode(self, index):
		"""
		This method returns the node at given index.
		
		:param index: Index. ( QModelIndex )
		:return: Node. ( AbstractCompositeNode )
		"""

		index = self.mapToSource(index)
		if not index.isValid():
			return self.sourceModel().rootNode

		return index.internalPointer() or self.sourceModel().rootNode

	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getAttribute(self, *args):
		"""
		This method is an implementation requisite method.
		"""

		pass
