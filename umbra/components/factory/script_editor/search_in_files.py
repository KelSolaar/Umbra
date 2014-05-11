#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**search_in_files.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`SearchInFiles` class.

**Others:**

"""

from __future__ import unicode_literals

import functools
import os
import sys
if sys.version_info[:2] <= (2, 6):
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextDocument

import foundations.cache
import foundations.exceptions
import foundations.strings
import foundations.ui.common
import foundations.verbose
import umbra.ui.common
import umbra.ui.nodes
from foundations.io import File
from umbra.components.factory.script_editor.models import SearchResultsModel
from umbra.components.factory.script_editor.nodes import ReplaceResultNode
from umbra.components.factory.script_editor.nodes import SearchFileNode
from umbra.components.factory.script_editor.nodes import SearchOccurenceNode
from umbra.components.factory.script_editor.search_and_replace import SearchAndReplace
from umbra.components.factory.script_editor.search_and_replace import ValidationFilter
from umbra.components.factory.script_editor.views import SearchResults_QTreeView
from umbra.components.factory.script_editor.workers import CacheData
from umbra.components.factory.script_editor.workers import Search_worker
from umbra.globals.runtime_globals import RuntimeGlobals
from umbra.ui.delegates import RichText_QStyledItemDelegate
from umbra.ui.widgets.search_QLineEdit import Search_QLineEdit

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "UI_FILE", "SearchInFiles"]

LOGGER = foundations.verbose.install_logger()

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Search_In_Files.ui")

class SearchInFiles(foundations.ui.common.QWidget_factory(ui_file=UI_FILE)):
    """
    Defines search and replace in files dialog used by the **ScriptEditor** Component.
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

        super(SearchInFiles, self).__init__(parent, *args, **kwargs)

        # --- Setting class attributes. ---
        self.__container = self.__script_editor = parent

        self.__files_cache = foundations.cache.Cache()

        self.__search_patterns_model = None
        self.__replace_with_patterns_model = None

        self.__model = None
        self.__view = None
        self.__delegate = None

        self.__locations = OrderedDict([("Add Directory ...", "directory"),
                                ("Add File ...", "file"),
                                ("Add Opened Files", "editors"),
                                ("Add Include Filter", "include_filter"),
                                ("Add Exclude Filter", "exclude_filter")])
        self.__locations_menu = None

        self.__default_filter_in = "*.txt"
        self.__filters_in_format = "{0}"
        self.__default_filter_out = "*.txt"
        self.__filters_out_format = "!{0}"
        self.__default_target = "Opened Files"
        self.__targets_format = "<{0}>"

        self.__default_line_number_width = 6
        self.__default_line_color = QColor(144, 144, 144)

        self.__ignore_hidden_files = True

        self.__search_worker_thread = None

        SearchInFiles.__initialize_ui(self)

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
    def script_editor(self):
        """
        Property for **self.__script_editor** attribute.

        :return: self.__script_editor.
        :rtype: QWidget
        """

        return self.__script_editor

    @script_editor.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def script_editor(self, value):
        """
        Setter for **self.__script_editor** attribute.

        :param value: Attribute value.
        :type value: QWidget
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "script_editor"))

    @script_editor.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def script_editor(self):
        """
        Deleter for **self.__script_editor** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "script_editor"))

    @property
    def files_cache(self):
        """
        Property for **self.__files_cache** attribute.

        :return: self.__files_cache.
        :rtype: Cache
        """

        return self.__files_cache

    @files_cache.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def files_cache(self, value):
        """
        Setter for **self.__files_cache** attribute.

        :param value: Attribute value.
        :type value: Cache
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "files_cache"))

    @files_cache.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def files_cache(self):
        """
        Deleter for **self.__files_cache** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "files_cache"))

    @property
    def search_patterns_model(self):
        """
        Property for **self.__search_patterns_model** attribute.

        :return: self.__search_patterns_model.
        :rtype: PatternsModel
        """

        return self.__search_patterns_model

    @search_patterns_model.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def search_patterns_model(self, value):
        """
        Setter for **self.__search_patterns_model** attribute.

        :param value: Attribute value.
        :type value: PatternsModel
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "search_patterns_model"))

    @search_patterns_model.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def search_patterns_model(self):
        """
        Deleter for **self.__search_patterns_model** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "search_patterns_model"))

    @property
    def replace_with_patterns_model(self):
        """
        Property for **self.__replace_with_patterns_model** attribute.

        :return: self.__replace_with_patterns_model.
        :rtype: PatternsModel
        """

        return self.__replace_with_patterns_model

    @replace_with_patterns_model.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def replace_with_patterns_model(self, value):
        """
        Setter for **self.__replace_with_patterns_model** attribute.

        :param value: Attribute value.
        :type value: PatternsModel
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "replace_with_patterns_model"))

    @replace_with_patterns_model.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def replace_with_patterns_model(self):
        """
        Deleter for **self.__replace_with_patterns_model** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "replace_with_patterns_model"))

    @property
    def model(self):
        """
        Property for **self.__model** attribute.

        :return: self.__model.
        :rtype: SearchResultsModel
        """

        return self.__model

    @model.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def model(self, value):
        """
        Setter for **self.__model** attribute.

        :param value: Attribute value.
        :type value: SearchResultsModel
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

    @model.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def model(self):
        """
        Deleter for **self.__model** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

    @property
    def view(self):
        """
        Property for **self.__view** attribute.

        :return: self.__view.
        :rtype: QWidget
        """

        return self.__view

    @view.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def view(self, value):
        """
        Setter for **self.__view** attribute.

        :param value: Attribute value.
        :type value: QWidget
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

    @view.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def view(self):
        """
        Deleter for **self.__view** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

    @property
    def delegate(self):
        """
        Property for **self.__delegate** attribute.

        :return: self.__delegate.
        :rtype: QItemDelegate
        """

        return self.__delegate

    @delegate.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def delegate(self, value):
        """
        Setter for **self.__delegate** attribute.

        :param value: Attribute value.
        :type value: QItemDelegate
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "delegate"))

    @delegate.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def delegate(self):
        """
        Deleter for **self.__delegate** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "delegate"))

    @property
    def locations(self):
        """
        Property for **self.__locations** attribute.

        :return: self.__locations.
        :rtype: OrderedDict
        """

        return self.__locations

    @locations.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def locations(self, value):
        """
        Setter for **self.__locations** attribute.

        :param value: Attribute value.
        :type value: OrderedDict
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "locations"))

    @locations.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def locations(self):
        """
        Deleter for **self.__locations** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "locations"))

    @property
    def locations_menu(self):
        """
        Property for **self.__locations_menu** attribute.

        :return: self.__locations_menu.
        :rtype: QMenu
        """

        return self.__locations_menu

    @locations_menu.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def locations_menu(self, value):
        """
        Setter for **self.__locations_menu** attribute.

        :param value: Attribute value.
        :type value: QMenu
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "locations_menu"))

    @locations_menu.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def locations_menu(self):
        """
        Deleter for **self.__locations_menu** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "locations_menu"))

    @property
    def default_filter_in(self):
        """
        Property for **self.__default_filter_in** attribute.

        :return: self.__default_filter_in.
        :rtype: unicode
        """

        return self.__default_filter_in

    @default_filter_in.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def default_filter_in(self, value):
        """
        Setter for **self.__default_filter_in** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
            "default_filter_in", value)
            assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("default_filter_in", value)
        self.__default_filter_in = value

    @default_filter_in.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_filter_in(self):
        """
        Deleter for **self.__default_filter_in** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_filter_in"))
    @property
    def filters_in_format(self):
        """
        Property for **self.__filters_in_format** attribute.

        :return: self.__filters_in_format.
        :rtype: unicode
        """

        return self.__filters_in_format

    @filters_in_format.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def filters_in_format(self, value):
        """
        Setter for **self.__filters_in_format** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
            "filters_in_format", value)
            assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("filters_in_format", value)
        self.__filters_in_format = value

    @filters_in_format.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def filters_in_format(self):
        """
        Deleter for **self.__filters_in_format** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "filters_in_format"))

    @property
    def default_filter_out(self):
        """
        Property for **self.__default_filter_out** attribute.

        :return: self.__default_filter_out.
        :rtype: unicode
        """

        return self.__default_filter_out

    @default_filter_out.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def default_filter_out(self, value):
        """
        Setter for **self.__default_filter_out** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
            "default_filter_out", value)
            assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("default_filter_out", value)
        self.__default_filter_out = value

    @default_filter_out.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_filter_out(self):
        """
        Deleter for **self.__default_filter_out** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_filter_out"))
    @property
    def filters_out_format(self):
        """
        Property for **self.__filters_out_format** attribute.

        :return: self.__filters_out_format.
        :rtype: unicode
        """

        return self.__filters_out_format

    @filters_out_format.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def filters_out_format(self, value):
        """
        Setter for **self.__filters_out_format** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
            "filters_out_format", value)
            assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("filters_out_format", value)
        self.__filters_out_format = value

    @filters_out_format.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def filters_out_format(self):
        """
        Deleter for **self.__filters_out_format** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "filters_out_format"))

    @property
    def default_target(self):
        """
        Property for **self.__default_target** attribute.

        :return: self.__default_target.
        :rtype: unicode
        """

        return self.__default_target

    @default_target.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def default_target(self, value):
        """
        Setter for **self.__default_target** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
            "default_target", value)
            assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("default_target", value)
        self.__default_target = value

    @default_target.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_target(self):
        """
        Deleter for **self.__default_target** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_target"))
    @property
    def targets_format(self):
        """
        Property for **self.__targets_format** attribute.

        :return: self.__targets_format.
        :rtype: unicode
        """

        return self.__targets_format

    @targets_format.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def targets_format(self, value):
        """
        Setter for **self.__targets_format** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
            "targets_format", value)
            assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("targets_format", value)
        self.__targets_format = value

    @targets_format.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def targets_format(self):
        """
        Deleter for **self.__targets_format** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "targets_format"))

    @property
    def default_line_number_width(self):
        """
        Property for **self.__default_line_number_width** attribute.

        :return: self.__default_line_number_width.
        :rtype: int
        """

        return self.__default_line_number_width

    @default_line_number_width.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def default_line_number_width(self, value):
        """
        Setter for **self.__default_line_number_width** attribute.

        :param value: Attribute value.
        :type value: int
        """

        if value is not None:
            assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format(
            "default_line_number_width", value)
            assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("default_line_number_width", value)
        self.__default_line_number_width = value

    @default_line_number_width.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_line_number_width(self):
        """
        Deleter for **self.__default_line_number_width** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_line_number_width"))

    @property
    def default_line_color(self):
        """
        Property for **self.__default_line_color** attribute.

        :return: self.__default_line_color.
        :rtype: QColor
        """

        return self.__default_line_color

    @default_line_color.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def default_line_color(self, value):
        """
        Setter for **self.__default_line_color** attribute.

        :param value: Attribute value.
        :type value: QColor
        """

        if value is not None:
            assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("default_line_color", value)
        self.__default_line_color = value

    @default_line_color.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_line_color(self):
        """
        Deleter for **self.__default_line_color** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_line_color"))

    @property
    def ignore_hidden_files(self):
        """
        Property for **self.__ignore_hidden_files** attribute.

        :return: self.__ignore_hidden_files.
        :rtype: bool
        """

        return self.__ignore_hidden_files

    @ignore_hidden_files.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ignore_hidden_files(self, value):
        """
        Setter for **self.__ignore_hidden_files** attribute.

        :param value: Attribute value.
        :type value: bool
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ignore_hidden_files"))

    @ignore_hidden_files.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ignore_hidden_files(self):
        """
        Deleter for **self.__ignore_hidden_files** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ignore_hidden_files"))

    @property
    def search_worker_thread(self):
        """
        Property for **self.__search_worker_thread** attribute.

        :return: self.__search_worker_thread.
        :rtype: QThread
        """

        return self.__search_worker_thread

    @search_worker_thread.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def search_worker_thread(self, value):
        """
        Setter for **self.__search_worker_thread** attribute.

        :param value: Attribute value.
        :type value: QThread
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "search_worker_thread"))

    @search_worker_thread.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def search_worker_thread(self):
        """
        Deleter for **self.__search_worker_thread** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "search_worker_thread"))

    def show(self):
        """
        Reimplements the :meth:`QWidget.show` method.
        """

        selected_text = self.__container.get_current_editor().get_selected_text()
        selected_text and SearchAndReplace.insert_pattern(selected_text, self.__search_patterns_model)
        self.Search_comboBox.line_edit().selectAll()
        self.Search_comboBox.setFocus()

        super(SearchInFiles, self).show()
        self.raise_()

    def closeEvent(self, event):
        """
        Reimplements the :meth:`QWidget.closeEvent` method.

        :param event: QEvent.
        :type event: QEvent
        """

        self.__interrupt_search()
        super(SearchInFiles, self).closeEvent(event)

    def __initialize_ui(self):
        """
        Initializes the Widget ui.
        """

        umbra.ui.common.set_window_default_icon(self)

        self.__model = SearchResultsModel(self)
        self.__delegate = RichText_QStyledItemDelegate(self)

        self.Search_Results_treeView.setParent(None)
        self.Search_Results_treeView = SearchResults_QTreeView(self,
                                                            self.__model,
                                                            message="No Search Result to view!")
        self.Search_Results_treeView.setItemDelegate(self.__delegate)
        self.Search_Results_treeView.setObjectName("Search_Results_treeView")
        self.Search_Results_frame_gridLayout.addWidget(self.Search_Results_treeView, 0, 0)
        self.__view = self.Search_Results_treeView
        self.__view.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.__view_add_actions()

        self.__search_patterns_model = self.__container.search_and_replace.search_patterns_model
        self.Search_comboBox.setModel(self.__container.search_and_replace.search_patterns_model)
        self.Search_comboBox.setInsertPolicy(QComboBox.InsertAtTop)
        self.Search_comboBox.completer().setCaseSensitivity(Qt.CaseSensitive)

        self.__replace_with_patterns_model = self.__container.search_and_replace.replace_with_patterns_model
        self.Replace_With_comboBox.setModel(self.__container.search_and_replace.replace_with_patterns_model)
        self.Replace_With_comboBox.setInsertPolicy(QComboBox.InsertAtTop)
        self.Replace_With_comboBox.completer().setCaseSensitivity(Qt.CaseSensitive)

        self.Where_lineEdit.setParent(None)
        self.Where_lineEdit = Search_QLineEdit(self)
        self.Where_lineEdit.setObjectName("Where_lineEdit")
        self.Where_frame_gridLayout.addWidget(self.Where_lineEdit, 0, 0)
        self.__locations_menu = QMenu()
        for title, location in self.__locations.iteritems():
            self.__locations_menu.addAction(self.__container.engine.actions_manager.register_action(
            "Actions|Umbra|Components|factory.script_editor|Search In Files|{0}".format(title),
            text="{0}".format(title),
            slot=functools.partial(self.__add_location, location)))
        self.Where_lineEdit.search_active_label.set_menu(self.__locations_menu)
        self.Where_lineEdit.setPlaceholderText("Use the magnifier to add locations!")

        self.installEventFilter(ValidationFilter(self))

        # Signals / Slots.
        self.__view.selectionModel().selectionChanged.connect(self.__view_selectionModel__selectionChanged)
        self.__view.doubleClicked.connect(self.__view__doubleClicked)
        self.__search_patterns_model.pattern_inserted.connect(functools.partial(
        self.__patterns_model__pattern_inserted, self.Search_comboBox))
        self.__replace_with_patterns_model.pattern_inserted.connect(functools.partial(
        self.__patterns_model__pattern_inserted, self.Replace_With_comboBox))
        self.Search_pushButton.clicked.connect(self.__Search_pushButton__clicked)
        self.Close_pushButton.clicked.connect(self.__Close_pushButton__clicked)

    def __view_add_actions(self):
        """
        Sets the View actions.
        """

        self.__view.addAction(self.__container.engine.actions_manager.register_action(
        "Actions|Umbra|Components|factory.script_editor|Search In Files|Replace All",
        slot=self.__view_replace_all_action__triggered))
        self.__view.addAction(self.__container.engine.actions_manager.register_action(
        "Actions|Umbra|Components|factory.script_editor|Search In Files|Replace Selected",
        slot=self.__view_replace_selected_action__triggered))
        separator_action = QAction(self.__view)
        separator_action.setSeparator(True)
        self.__view.addAction(separator_action)
        self.__view.addAction(self.__container.engine.actions_manager.register_action(
        "Actions|Umbra|Components|factory.script_editor|Search In Files|Save All",
        slot=self.__view_save_all_action__triggered))
        self.__view.addAction(self.__container.engine.actions_manager.register_action(
        "Actions|Umbra|Components|factory.script_editor|Search In Files|Save Selected",
        slot=self.__view_save_selected_action__triggered))

    def __view_replace_all_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|Search In Files|Replace All'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        all_nodes = filter(lambda x: x.family in ("SearchFile", "SearchOccurence"), self.__model.root_node.children)
        if all_nodes:
            return self.replace(all_nodes)

    def __view_replace_selected_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|Search In Files|Replace Selected'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        selected_nodes = filter(lambda x: x.family in ("SearchFile", "SearchOccurence"), self.__view.get_selected_nodes())
        if selected_nodes:
            return self.replace(filter(lambda x: x.parent not in selected_nodes, selected_nodes))

    def __view_save_all_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|Search In Files|Save All'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        all_nodes = filter(lambda x: x.family is "ReplaceResult", self.__model.root_node.children)
        if all_nodes:
            return self.save_files(all_nodes)

    def __view_save_selected_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|Search In Files|Save Selected'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        selected_nodes = filter(lambda x: x.family is "ReplaceResult", self.__view.get_selected_nodes())
        if selected_nodes:
            return self.save_files(selected_nodes)

    def __patterns_model__pattern_inserted(self, combo_box, index):
        """
        Defines the slot triggered by a pattern when inserted into a patterns Model.

        :param combo_box: Pattern Model attached combo_box.
        :type combo_box: QComboBox
        :param index: Inserted pattern index.
        :type index: QModelIndex
        """

        combo_box.setCurrentIndex(index.row())

    def __Search_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Search_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.search()

    def __Close_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Close_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.close()

    def __view__doubleClicked(self, index):
        """
        Defines the slot triggered by a View when double clicked.

        :param index: Clicked item index.
        :type index: QModelIndex
        """

        node = self.__model.get_node(index)

        if node.family == "SearchOccurence":
            file = node.parent.file
            occurence = node
        elif node.family in ("SearchFile", "ReplaceResult"):
            file = node.file
            occurence = None

        self.__highlight_occurence(file, occurence)

    def __view_selectionModel__selectionChanged(self, selected_items, deselected_items):
        """
        Defines the slot triggered by the View **selectionModel** when selection changed.

        :param selected_items: Selected items.
        :type selected_items: QItemSelection
        :param deselected_items: Deselected items.
        :type deselected_items: QItemSelection
        """

        indexes = selected_items.indexes()
        if not indexes:
            return

        node = self.__model.get_node(indexes.pop())

        if node.family == "SearchOccurence":
            file = node.parent.file
            occurence = node
        elif node.family in ("SearchFile", "ReplaceResult"):
            file = node.file
            occurence = None

        if self.__container.get_editor(file):
            self.__highlight_occurence(file, occurence)

    def __search_worker_thread__searchFinished(self, search_results):
        """
        Defines the slot triggered by :attr:`SearchInFiles.grepWorkerThread` attribute worker thread
        when the search is finished.

        :param search_results: Search results.
        :type search_results: list
        """

        self.set_search_results(search_results)

        self.__container.engine.stop_processing()
        metrics = self.__model.get_metrics()
        self.__container.engine.notifications_manager.notify(
        "{0} | '{1}' pattern occurence(s) found in '{2}' files!".format(self.__class__.__name__,
                                                                    metrics["SearchOccurence"],
                                                                    metrics["SearchFile"]))

    def __add_location(self, type, *args):
        """
        Defines the slot triggered by **Where_lineEdit** Widget when a context menu entry is clicked.

        :param type: Location type.
        :type type: unicode
        :param \*args: Arguments.
        :type \*args: \*
        """

        if type == "directory":
            location = umbra.ui.common.store_last_browsed_path((QFileDialog.getExistingDirectory(self,
                                                                                        "Add Directory:",
                                                                                        RuntimeGlobals.last_browsed_path)))
        elif type == "file":
            location = umbra.ui.common.store_last_browsed_path((QFileDialog.getOpenFileName(self,
                                                                                        "Add File:",
                                                                                        RuntimeGlobals.last_browsed_path,
                                                                                        "All Files (*)")))
        elif type == "editors":
            location = self.__targets_format.format(self.__default_target)
        elif type == "include_filter":
            location = self.__filters_in_format.format(self.__default_filter_in)
        elif type == "exclude_filter":
            location = self.__filters_out_format.format(self.__default_filter_out)

        location and self.Where_lineEdit.setText(", ".join(filter(bool, (foundations.strings.to_string(
        self.Where_lineEdit.text()), location))))

    def __format_occurence(self, occurence):
        """
        Formats the given occurence and returns the matching rich html text.

        :param occurence: Occurence to format.
        :type occurence: Occurence
        :return: Rich text.
        :rtype: unicode
        """

        color = "rgb({0}, {1}, {2})"
        span_format = "<span style=\"color: {0};\">{{0}}</span>".format(color.format(self.__default_line_color.red(),
                                                                                    self.__default_line_color.green(),
                                                                                    self.__default_line_color.blue()))
        line = foundations.strings.to_string(occurence.text)
        start = span_format.format(line[:occurence.column])
        pattern = "<b>{0}</b>".format(line[occurence.column:occurence.column + occurence.length])
        end = span_format.format(line[occurence.column + occurence.length:])
        return "".join((start, pattern, end))

    def __format_replace_metrics(self, file, metrics):
        """
        Formats the given replace metrics and returns the matching rich html text.

        :param file: File.
        :type file: unicode
        :param metrics: Replace metrics to format.
        :type metrics: unicode
        :return: Rich text.
        :rtype: unicode
        """

        color = "rgb({0}, {1}, {2})"
        span_format = "<span style=\"color: {0};\">{{0}}</span>".format(color.format(self.__default_line_color.red(),
                                                                                    self.__default_line_color.green(),
                                                                                    self.__default_line_color.blue()))
        dir_name, base_name = (os.path.dirname(file), os.path.basename(file))

        return "".join((span_format.format("'"),
                        span_format.format(dir_name),
                        span_format.format(os.path.sep),
                        base_name,
                        span_format.format("' file: '"),
                        foundations.strings.to_string(metrics),
                        span_format.format("' occurence(s) replaced!")))

    def __highlight_occurence(self, file, occurence):
        """
        Highlights given file occurence.

        :param file: File containing the occurence.
        :type file: unicode
        :param occurence: Occurence to highlight.
        :type occurence: Occurence or SearchOccurenceNode
        """

        if not self.__container.get_editor(file):
            cache_data = self.__files_cache.get_content(file)
            if cache_data:
                document = cache_data.document or self.__get_document(cache_data.content)
                self.__container.load_document(document, file)
                self.__uncache(file)
            else:
                self.__container.load_file(file)
        else:
            self.__container.set_current_editor(file)

        if not occurence:
            return

        cursor = self.__container.get_current_editor().textCursor()
        cursor.setPosition(occurence.position, QTextCursor.MoveAnchor)
        cursor.setPosition(occurence.position + occurence.length, QTextCursor.KeepAnchor)
        self.__container.get_current_editor().setTextCursor(cursor)

    def __get_document(self, content):
        """
        Returns a `QTextDocument <http://doc.qt.nokia.com/qtextdocument.html>`_ class instance
        with given content.

        :return: Document.
        :rtype: QTextDocument
        """

        document = QTextDocument(QString(content))
        document.clearUndoRedoStacks()
        document.setModified(False)
        return document

    def __replace_within_document(self, document, occurrences, replacement_pattern):
        """
        Replaces given pattern occurrences in given document using given settings.

        :param document: Document.
        :type document: QTextDocument
        :param replacement_pattern: Replacement pattern.
        :type replacement_pattern: unicode
        :return: Replaced occurrences count.
        :rtype: int
        """

        cursor = QTextCursor(document)
        cursor.beginEditBlock()
        offset = count = 0
        for occurence in sorted(occurrences, key=lambda x: x.position):
            cursor.setPosition(offset + occurence.position, QTextCursor.MoveAnchor)
            cursor.setPosition(offset + occurence.position + occurence.length, QTextCursor.KeepAnchor)
            cursor.insertText(replacement_pattern)
            offset += len(replacement_pattern) - occurence.length
            count += 1
        cursor.endEditBlock()
        return count

    def __get_settings(self):
        """
        Returns the current search and replace settings.

        :return: Settings.
        :rtype: dict
        """

        return {"case_sensitive" : self.Case_Sensitive_checkBox.isChecked(),
                "whole_word" : self.Whole_Word_checkBox.isChecked(),
                "regular_expressions" : self.Regular_Expressions_checkBox.isChecked()}

    def __interrupt_search(self):
        """
        Interrupt the current search.
        """

        if self.__search_worker_thread:
            self.__search_worker_thread.quit()
            self.__search_worker_thread.wait()
            self.__container.engine.stop_processing(warning=False)

    def __cache(self, file, content, document):
        """
        Caches given file.

        :param file: File to cache.
        :type file: unicode
        :param content: File content.
        :type content: list
        :param document: File document.
        :type document: QTextDocument
        """

        self.__files_cache.add_content(**{file : CacheData(content=content, document=document)})

    def __uncache(self, file):
        """
        Uncaches given file.

        :param file: File to uncache.
        :type file: unicode
        """

        if file in self.__files_cache:
            self.__files_cache.remove_content(file)

    def set_search_results(self, search_results):
        """
        Sets the Model Nodes using given search results.

        :param search_results: Search results.
        :type search_results: list
        :return: Method success.
        :rtype: bool
        """

        root_node = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")
        for search_result in search_results:
            search_file_node = SearchFileNode(name=search_result.file,
                                            parent=root_node)
            search_file_node.update(search_result)
            width = \
            max(self.__default_line_number_width,
            max([len(foundations.strings.to_string(occurence.line)) for occurence in search_result.occurrences]))
            for occurence in search_result.occurrences:
                formatter = "{{0:>{0}}}".format(width)
                name = "{0}:{1}".format(formatter.format(occurence.line + 1).replace(" ", "&nbsp;"),
                                        self.__format_occurence(occurence))
                search_occurence_node = SearchOccurenceNode(name=name,
                                                        parent=search_file_node)
                search_occurence_node.update(occurence)
        self.__model.initialize_model(root_node)
        return True

    def set_replace_results(self, replace_results):
        """
        Sets the Model Nodes using given replace results.

        :param replace_results: Replace results.
        :type replace_results: list
        :return: Method success.
        :rtype: bool
        """

        root_node = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")
        for file, metrics in sorted(replace_results.iteritems()):
            replace_result_node = ReplaceResultNode(name=self.__format_replace_metrics(file, metrics),
                                                parent=root_node,
                                                file=file)
        self.__model.initialize_model(root_node)
        return True

    def search(self):
        """
        Searchs user defined locations for search pattern.

        :return: Method success.
        :rtype: bool
        """

        self.__interrupt_search()

        search_pattern = self.Search_comboBox.currentText()
        replacement_pattern = self.Replace_With_comboBox.currentText()
        if not search_pattern:
            return False

        SearchAndReplace.insert_pattern(search_pattern, self.__search_patterns_model)
        SearchAndReplace.insert_pattern(replacement_pattern, self.__replace_with_patterns_model)

        location = umbra.ui.common.parse_location(
        foundations.strings.to_string(self.Where_lineEdit.text()) or \
        self.__targets_format.format(self.__default_target))
        self.__ignore_hidden_files and location.filters_out.append("\\\.|/\.")

        settings = self.__get_settings()

        self.__search_worker_thread = Search_worker(self, search_pattern, location, settings)
        # Signals / Slots.
        self.__search_worker_thread.searchFinished.connect(self.__search_worker_thread__searchFinished)

        self.__container.engine.worker_threads.append(self.__search_worker_thread)
        self.__container.engine.start_processing("Searching In Files ...")
        self.__search_worker_thread.start()
        return True

    def replace(self, nodes):
        """
        Replaces user defined files search pattern occurrences with replacement pattern using given nodes.

        :param nodes: Nodes.
        :type nodes: list
        :return: Method success.
        :rtype: bool
        """

        files = {}
        for node in nodes:
            if node.family == "SearchFile":
                files[node.file] = node.children
            elif node.family == "SearchOccurence":
                file = node.parent.file
                if not file in files:
                    files[file] = []
                files[file].append(node)

        replacement_pattern = self.Replace_With_comboBox.currentText()
        SearchAndReplace.insert_pattern(replacement_pattern, self.__replace_with_patterns_model)

        replace_results = {}
        for file, occurrences in files.iteritems():
            editor = self.__container.get_editor(file)
            if editor:
                document = editor.document()
            else:
                cache_data = self.__files_cache.get_content(file)
                if cache_data is None:
                    LOGGER.warning(
                    "!> {0} | '{1}' file doesn't exists in files cache!".format(self.__class__.__name__, file))
                    continue

                content = self.__files_cache.get_content(file).content
                document = self.__get_document(content)
                self.__cache(file, content, document)
            replace_results[file] = self.__replace_within_document(document, occurrences, replacement_pattern)

        self.set_replace_results(replace_results)
        self.__container.engine.notifications_manager.notify(
        "{0} | '{1}' pattern occurence(s) replaced in '{2}' files!".format(self.__class__.__name__,
                                                                    sum(replace_results.values()),
                                                                    len(replace_results.keys())))

    def save_files(self, nodes):
        """
        Saves user defined files using give nodes.

        :param nodes: Nodes.
        :type nodes: list
        :return: Method success.
        :rtype: bool
        """

        metrics = {"Opened" : 0, "Cached" : 0}
        for node in nodes:
            file = node.file
            if self.__container.get_editor(file):
                if self.__container.save_file(file):
                    metrics["Opened"] += 1
                    self.__uncache(file)
            else:
                cache_data = self.__files_cache.get_content(file)
                if cache_data is None:
                    LOGGER.warning(
                    "!> {0} | '{1}' file doesn't exists in files cache!".format(self.__class__.__name__, file))
                    continue

                if cache_data.document:
                    file_handle = File(file)
                    file_handle.content = [cache_data.document.toPlainText().toUtf8()]
                    if file_handle.write():
                        metrics["Cached"] += 1
                        self.__uncache(file)
                else:
                    LOGGER.warning(
                    "!> {0} | '{1}' file document doesn't exists in files cache!".format(self.__class__.__name__, file))

        self.__container.engine.notifications_manager.notify(
        "{0} | '{1}' opened file(s) and '{2}' cached file(s) saved!".format(self.__class__.__name__,
                                                                        metrics["Opened"],
                                                                        metrics["Cached"]))
