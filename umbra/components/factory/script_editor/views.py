#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**views.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`umbra.components.factory.script_editor.script_editor.ScriptEditor`
    Component Interface class Views.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtCore import QEvent
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QAbstractItemView
from PyQt4.QtGui import QTabWidget

import foundations.exceptions
import foundations.verbose
import umbra.ui.views

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "SearchResults_QTreeView", "ScriptEditor_QTabWidget"]

LOGGER = foundations.verbose.install_logger()


class SearchResults_QTreeView(umbra.ui.views.Abstract_QTreeView):
    """
    Defines the view for Database Ibl Sets columns.
    """

    def __init__(self, parent, model=None, read_only=False, message=None):
        """
        Initializes the class.

        :param parent: Object parent.
        :type parent: QObject
        :param read_only: View is read only.
        :type read_only: bool
        :param message: View default message when Model is empty.
        :type message: unicode
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        umbra.ui.views.Abstract_QTreeView.__init__(self, parent, read_only, message)

        # --- Setting class attributes. ---
        self.setModel(model)

        self.__tree_view_indentation = 15

        SearchResults_QTreeView.__initialize_ui(self)

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
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setIndentation(self.__tree_view_indentation)
        self.setDragDropMode(QAbstractItemView.DragOnly)
        self.setHeaderHidden(True)

        self.__set_default_ui_state()

        # Signals / Slots.
        self.model().modelReset.connect(self.__set_default_ui_state)

    def __set_default_ui_state(self, *args):
        """
        Sets the Widget default ui state.

        :param \*args: Arguments.
        :type \*args: \*
        """

        LOGGER.debug("> Setting default View state!")

        if not self.model():
            return

        self.expandAll()

        for column in range(len(self.model().horizontal_headers)):
            self.resizeColumnToContents(column)


class ScriptEditor_QTabWidget(QTabWidget):
    """
    | Defines a `QTabWidget <http://doc.qt.nokia.com/qtabwidget.html>`_ subclass used
        to display :class:`umbra.components.factory.script_editor.script_editor.ScriptEditor` editors.
    | It provides support for drag'n'drop by reimplementing relevant methods.
    """

    # Custom signals definitions.
    content_dropped = pyqtSignal(QEvent)
    """
    This signal is emited by the :class:`ScriptEditor_QTabWidget` class when it receives dropped content.

    :return: Event.
    :rtype: QEvent
    """

    def __init__(self, parent):
        """
        Initializes the class.

        :param parent: Parent object.
        :type parent: QObject
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        QTabWidget.__init__(self, parent)

        self.setAcceptDrops(True)

        # --- Setting class attributes. ---
        self.__container = parent

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

    def dragEnterEvent(self, event):
        """
        Reimplements the :meth:`QTabWidget.dragEnterEvent` method.

        :param event: QEvent.
        :type event: QEvent
        """

        LOGGER.debug("> '{0}' widget drag enter event accepted!".format(self.__class__.__name__))
        event.accept()

    def dragMoveEvent(self, event):
        """
        Reimplements the :meth:`QTabWidget.dragMoveEvent` method.

        :param event: QEvent.
        :type event: QEvent
        """

        LOGGER.debug("> '{0}' widget drag move event accepted!".format(self.__class__.__name__))
        event.accept()

    def dropEvent(self, event):
        """
        Reimplements the :meth:`QTabWidget.dropEvent` method.

        :param event: QEvent.
        :type event: QEvent
        """

        LOGGER.debug("> '{0}' widget drop event accepted!".format(self.__class__.__name__))
        self.content_dropped.emit(event)
