#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`umbra.components.factory.components_manager_ui.components_manager_ui.ComponentsManagerUi`
    Component Interface class Views.

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

__all__ = ["LOGGER", "Components_QTreeView"]

LOGGER = foundations.verbose.install_logger()

class Components_QTreeView(umbra.ui.views.Abstract_QTreeView):
    """
    Defines the view for Components.
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
        self.__container = parent

        self.__tree_view_indentation = 15

        self.setModel(model)

        Components_QTreeView.__initialize_ui(self)

    @property
    def container(self):
        """
        Property for **self.__container** attribute.

        :return: self.__container.
        :rtype: QObject
        """

        return self.__container

    @container.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def container(self, value):
        """
        Setter for **self.__container** attribute.

        :param value: Attribute value.
        :type value: QObject
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

    @container.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def container(self):
        """
        Deleter for **self.__container** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

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

    def setModel(self, model):
        """
        Reimplements the **umbra.ui.views.Abstract_QTreeView.setModel** method.

        :param model: Model to set.
        :type model: QObject
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
        Defines the slot triggered by the Model when about to be reset.
        """

        pass

    def __model__modelReset(self):
        """
        Defines the slot triggered by the Model when reset.
        """

        pass

    def __initialize_ui(self):
        """
        Initializes the Widget ui.
        """

        self.setAutoScroll(False)
        self.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setIndentation(self.__tree_view_indentation)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

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

        for column in range(len(self.model().horizontal_headers)):
            self.resizeColumnToContents(column)
