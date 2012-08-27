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
from PyQt4.QtCore import QEvent
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QTabWidget

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

__all__ = ["LOGGER", "SearchResults_QTreeView", "ScriptEditor_QTabWidget"]

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

		# Signals / Slots.
		self.model().modelReset.connect(self.__setDefaultUiState)

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

class ScriptEditor_QTabWidget(QTabWidget):
	"""
	| This class is a `QTabWidget <http://doc.qt.nokia.com/qtabwidget.html>`_ subclass used
		to display :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor` editors.
	| It provides support for drag'n'drop by reimplementing relevant methods.
	"""

	# Custom signals definitions.
	contentDropped = pyqtSignal(QEvent)
	"""
	This signal is emited by the :class:`ScriptEditor_QTabWidget` class when it receives dropped content. ( pyqtSignal )

	:return: Event. ( QEvent )	
	"""

	@core.executionTrace
	def __init__(self, parent):
		"""
		This method initializes the class.

		:param parent: Parent object. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QTabWidget.__init__(self, parent)

		self.setAcceptDrops(True)

		# --- Setting class attributes. ---
		self.__container = parent

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
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def dragEnterEvent(self, event):
		"""
		This method reimplements the :meth:`QTabWidget.dragEnterEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		LOGGER.debug("> '{0}' widget drag enter event accepted!".format(self.__class__.__name__))
		event.accept()

	@core.executionTrace
	def dragMoveEvent(self, event):
		"""
		This method reimplements the :meth:`QTabWidget.dragMoveEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		LOGGER.debug("> '{0}' widget drag move event accepted!".format(self.__class__.__name__))
		event.accept()

	@core.executionTrace
	def dropEvent(self, event):
		"""
		This method reimplements the :meth:`QTabWidget.dropEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		LOGGER.debug("> '{0}' widget drop event accepted!".format(self.__class__.__name__))
		self.contentDropped.emit(event)

