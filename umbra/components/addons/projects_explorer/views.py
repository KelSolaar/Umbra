#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`umbra.components.factory.projects_explorer.projects_explorer.ProjectsExplorer`
	Component Interface class View.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAbstractItemView

import foundations.exceptions
import foundations.verbose
import umbra.ui.views

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Projects_QTreeView"]

LOGGER = foundations.verbose.install_logger()

class Projects_QTreeView(umbra.ui.views.Abstract_QTreeView):
	"""
	Defines the view for Projects.
	"""

	def __init__(self, parent, model=None, read_only=False, message=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param model: Model.
		:type model: QObject
		:param read_only: View is read only.
		:type read_only: bool
		:param message: View default message when Model is empty.
		:type message: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.views.Abstract_QTreeView.__init__(self, parent, read_only, message)

		# --- Setting class attributes. ---
		self.__tree_view_indentation = 15

		self.setModel(model)

		Projects_QTreeView.__initialize_ui(self)

	@property
	def tree_view_indentation(self):
		"""
		Property for **self.__tree_view_indentation** attribute.

		:return: self.__tree_view_indentation.
		:rtype: int
		"""

		return self.__tree_view_indentation

	@tree_view_indentation.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def tree_view_indentation(self, value):
		"""
		Setter for **self.__tree_view_indentation** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tree_view_indentation"))

	@tree_view_indentation.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def tree_view_indentation(self):
		"""
		Deleter for **self.__tree_view_indentation** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tree_view_indentation"))

	def __initialize_ui(self):
		"""
		Initializes the Widget ui.
		"""

		self.setAutoScroll(True)
		self.setIndentation(self.__tree_view_indentation)
		self.setRootIsDecorated(False)
		self.setDragDropMode(QAbstractItemView.DragOnly)

		self.header().hide()

		self.setSortingEnabled(True)
		self.sortByColumn(0, Qt.AscendingOrder)

		self.__set_default_ui_state()

		# Signals / Slots.
		self.model().modelReset.connect(self.__set_default_ui_state)

	def __set_default_ui_state(self):
		"""
		Sets the Widget default ui state.
		"""

		LOGGER.debug("> Setting default View state!")

		if not self.model():
			return

		self.expandAll()

	def setModel(self, model):
		"""
		Reimplements the **umbra.ui.views.Abstract_QTreeView.setModel** method.

		:param model: Model to set.
		:type model: QObject
		"""

		LOGGER.debug("> Setting '{0}' model.".format(model))

		if not model:
			return

		umbra.ui.views.Abstract_QTreeView.setModel(self, model)
