#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class Views.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractItemView

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import umbra.ui.views
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

__all__ = ["LOGGER", "SearchResults_QTreeView"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class SearchResults_QTreeView(umbra.ui.views.Abstract_QTreeView):
	"""
	This class is used to display Database Ibl Sets columns.
	"""

	@core.executionTrace
	def __init__(self, parent, model=None, readOnly=False):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param readOnly: View is read only. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.views.Abstract_QTreeView.__init__(self, parent, readOnly)

		# --- Setting class attributes. ---
		self.setModel(model)

		self.__treeViewIndentation = 15

		SearchResults_QTreeView.__initializeUi(self)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def treeViewIndentation(self):
		"""
		This method is the property for **self.__treeViewIndentation** attribute.

		:return: self.__treeViewIndentation. ( Integer )
		"""

		return self.__treeViewIndentation

	@treeViewIndentation.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewIndentation(self, value):
		"""
		This method is the setter method for **self.__treeViewIndentation** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "treeViewIndentation"))

	@treeViewIndentation.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewIndentation(self):
		"""
		This method is the deleter method for **self.__treeViewIndentation** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "treeViewIndentation"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		self.setAutoScroll(True)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.setIndentation(self.__treeViewIndentation)
		self.setDragDropMode(QAbstractItemView.DragOnly)
		self.setHeaderHidden(True)

		self.__setDefaultUiState()

	@core.executionTrace
	def __setDefaultUiState(self, *args):
		"""
		This method sets the Widget default ui state.
		
		:param \*args: Arguments. ( \* )
		"""

		LOGGER.debug("> Setting default View state!")

		if not self.model():
			return

		self.expandAll()

		for column in range(len(self.model().horizontalHeaders)):
			self.resizeColumnToContents(column)

	@core.executionTrace
	def blockUpdates(self, state):
		"""
		This method blocks the Widget updates.
		
		:param state: Widget updates state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Setting View state updates state: '{0}'!".format(state))

		if state:
			self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
			self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
			self.viewport().setUpdatesEnabled(False)
		else:
			self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
			self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
			self.viewport().setUpdatesEnabled(True)
			self.__setDefaultUiState()
