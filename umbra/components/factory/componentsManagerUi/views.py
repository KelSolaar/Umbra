#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`umbra.components.factory.componentsManagerUi.componentsManagerUi.ComponentsManagerUi`
	Component Interface class Views.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractItemView

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import umbra.ui.views

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Components_QTreeView"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Components_QTreeView(umbra.ui.views.Abstract_QTreeView):
	"""
	This class is used to display Database Collections.
	"""

	def __init__(self, parent, model=None, readOnly=False, message=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param model: Model. ( QObject )
		:param readOnly: View is read only. ( Boolean )
		:param message: View default message when Model is empty. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.views.Abstract_QTreeView.__init__(self, parent, readOnly, message)

		# --- Setting class attributes. ---
		self.__container = parent

		self.__treeViewIndentation = 15

		self.setModel(model)

		Components_QTreeView.__initializeUi(self)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def treeViewIndentation(self):
		"""
		This method is the property for **self.__treeViewIndentation** attribute.

		:return: self.__treeViewIndentation. ( Integer )
		"""

		return self.__treeViewIndentation

	@treeViewIndentation.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def treeViewIndentation(self, value):
		"""
		This method is the setter method for **self.__treeViewIndentation** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "treeViewIndentation"))

	@treeViewIndentation.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def treeViewIndentation(self):
		"""
		This method is the deleter method for **self.__treeViewIndentation** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "treeViewIndentation"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def setModel(self, model):
		"""
		This method reimplements the **umbra.ui.views.Abstract_QTreeView.setModel** method.
		
		:param model: Model to set. ( QObject )
		"""

		if not model:
			return

		LOGGER.debug("> Setting '{0}' model.".format(model))

		umbra.ui.views.Abstract_QTreeView.setModel(self, model)

		# Signals / Slots.
		self.model().modelAboutToBeReset.connect(self.__model__modelAboutToBeReset)
		self.model().modelReset.connect(self.__model__modelReset)

	def __model__modelAboutToBeReset(self):
		"""
		This method is triggered when the Model is about to be reset.
		"""

		pass

	def __model__modelReset(self):
		"""
		This method is triggered when the Model is changed.
		"""

		pass

	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		self.setAutoScroll(False)
		self.setDragDropMode(QAbstractItemView.NoDragDrop)
		self.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.setIndentation(self.__treeViewIndentation)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)

		self.setSortingEnabled(True)
		self.sortByColumn(0, Qt.AscendingOrder)

		self.__setDefaultUiState()

		# Signals / Slots.
		self.model().modelReset.connect(self.__setDefaultUiState)

	def __setDefaultUiState(self):
		"""
		This method sets the Widget default ui state.
		"""

		LOGGER.debug("> Setting default View state!")

		if not self.model():
			return

		self.expandAll()

		for column in range(len(self.model().horizontalHeaders)):
			self.resizeColumnToContents(column)
