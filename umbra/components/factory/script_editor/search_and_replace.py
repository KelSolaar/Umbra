#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**search_and_replace.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`SearchAndReplace` class.

**Others:**

"""

from __future__ import unicode_literals

import functools
import os
from PyQt4.QtCore import QChar
from PyQt4.QtCore import QObject
from PyQt4.QtCore import QEvent
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QComboBox

import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.ui.common
import foundations.verbose
import umbra.ui.common
from umbra.components.factory.script_editor.models import PatternsModel
from umbra.components.factory.script_editor.nodes import PatternNode

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "UI_FILE", "SearchAndReplace"]

LOGGER = foundations.verbose.install_logger()

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Search_And_Replace.ui")

class ValidationFilter(QObject):
    """
    Defines a `QObject <http://doc.qt.nokia.com/qobject.html>`_ subclass used as an event filter
    for the :class:`SearchAndReplace` class.
    """

    def eventFilter(self, object, event):
        """
        Reimplements the **QObject.eventFilter** method.

        :param object: Object.
        :type object: QObject
        :param event: Event.
        :type event: QEvent
        :return: Event filtered.
        :rtype: bool
        """

        if event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Enter, Qt.Key_Return):
                object.search()
            elif event.key() in (Qt.Key_Escape,):
                object.close()
            return True
        else:
            return QObject.eventFilter(self, object, event)

class SearchAndReplace(foundations.ui.common.QWidget_factory(ui_file=UI_FILE)):
    """
    Defines the default search and replace dialog used by the **ScriptEditor** Component.
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

        super(SearchAndReplace, self).__init__(parent, *args, **kwargs)

        # --- Setting class attributes. ---
        self.__container = parent

        self.__search_patterns_model = None
        self.__replace_with_patterns_model = None

        self.__maximum_stored_patterns = 15

        SearchAndReplace.__initialize_ui(self)

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
    def maximum_stored_patterns(self):
        """
        Property for **self.__maximum_stored_patterns** attribute.

        :return: self.__maximum_stored_patterns.
        :rtype: int
        """

        return self.__maximum_stored_patterns

    @maximum_stored_patterns.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def maximum_stored_patterns(self, value):
        """
        Setter for **self.__maximum_stored_patterns** attribute.

        :param value: Attribute value.
        :type value: int
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "maximum_stored_patterns"))

    @maximum_stored_patterns.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def maximum_stored_patterns(self):
        """
        Deleter for **self.__maximum_stored_patterns** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "maximum_stored_patterns"))

    def show(self):
        """
        Reimplements the :meth:`QWidget.show` method.
        """

        selected_text = self.__container.get_current_editor().get_selected_text()
        selected_text and self.insert_pattern(selected_text, self.__search_patterns_model)
        self.Search_comboBox.line_edit().selectAll()
        self.Search_comboBox.setFocus()

        super(SearchAndReplace, self).show()
        self.raise_()

    def __initialize_ui(self):
        """
        Initializes the Widget ui.
        """

        umbra.ui.common.set_window_default_icon(self)

        for model, settings_key, combo_box in \
        (("_SearchAndReplace__search_patterns_model", "recent_search_patterns", self.Search_comboBox),
        ("_SearchAndReplace__replace_with_patterns_model", "recent_replace_with_patterns", self.Replace_With_comboBox)):
            self.__dict__[model] = PatternsModel()
            patterns = foundations.common.ordered_uniqify([foundations.strings.to_string(pattern) for pattern in \
                                                        self.__container.settings.get_key(self.__container.settings_section,
                                                                                        settings_key).toStringList()])
            [PatternNode(parent=self.__dict__[model].root_node, name=pattern) \
            for pattern in patterns[:self.__maximum_stored_patterns]]
            combo_box.setInsertPolicy(QComboBox.InsertAtTop)
            combo_box.setModel(self.__dict__[model])

            combo_box.completer().setCaseSensitivity(Qt.CaseSensitive)

            # Signals / Slots.
            self.__dict__[model].pattern_inserted.connect(
            functools.partial(self.__patterns_model__pattern_inserted, settings_key, combo_box))

        self.Wrap_Around_checkBox.setChecked(True)

        self.installEventFilter(ValidationFilter(self))

        # Signals / Slots.
        self.Search_pushButton.clicked.connect(self.__Search_pushButton__clicked)
        self.Replace_pushButton.clicked.connect(self.__Replace_pushButton__clicked)
        self.Replace_All_pushButton.clicked.connect(self.__Replace_All_pushButton__clicked)
        self.Close_pushButton.clicked.connect(self.__Close_pushButton__clicked)

    def __patterns_model__pattern_inserted(self, settings_key, combo_box, index):
        """
        Defines the slot triggered by a pattern when inserted into a patterns Model.

        :param settings_key: Pattern Model settings key.
        :type settings_key: unicode
        :param combo_box: Pattern Model attached combo_box.
        :type combo_box: QComboBox
        :param index: Inserted pattern index.
        :type index: QModelIndex
        """

        patterns_model = self.sender()

        LOGGER.debug("> Storing '{0}' model patterns in '{1}' settings key.".format(patterns_model, settings_key))

        self.__container.settings.set_key(self.__container.settings_section,
                                        settings_key,
                                        [pattern_node.name for pattern_node in \
                                        patterns_model.root_node.children[:self.maximum_stored_patterns]])
        combo_box.setCurrentIndex(index.row())

    def __Search_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Search_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.search()

    def __Replace_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Replace_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.replace()

    def __Replace_All_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Replace_All_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.replace_all()

    def __Close_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Close_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.close()

    def __get_settings(self):
        """
        Returns the current search and replace settings.

        :return: Settings.
        :rtype: dict
        """

        return {"case_sensitive" : self.Case_Sensitive_checkBox.isChecked(),
                "whole_word" : self.Whole_Word_checkBox.isChecked(),
                "regular_expressions" : self.Regular_Expressions_checkBox.isChecked(),
                "backward_search" : self.Backward_Search_checkBox.isChecked(),
                "wrap_around" : self.Wrap_Around_checkBox.isChecked()}

    @staticmethod
    def insert_pattern(pattern, model, index=0):
        """
        Inserts given pattern into given Model.

        :param pattern: Pattern.
        :type pattern: unicode
        :param model: Model.
        :type model: PatternsModel
        :param index: Insertion indes.
        :type index: int
        :return: Method success.
        :rtype: bool
        """

        if not pattern:
            return False

        pattern = pattern.replace(QChar(QChar.ParagraphSeparator), QString("\n"))
        pattern = foundations.common.get_first_item(foundations.strings.to_string(pattern).split("\n"))

        model.insert_pattern(foundations.strings.to_string(pattern), index)

        return True

    def search(self):
        """
        Searchs current editor Widget for search pattern.

        :return: Method success.
        :rtype: bool
        """

        editor = self.__container.get_current_editor()
        search_pattern = self.Search_comboBox.currentText()
        replacement_pattern = self.Replace_With_comboBox.currentText()

        if not editor or not search_pattern:
            return False

        self.insert_pattern(search_pattern, self.__search_patterns_model)
        self.insert_pattern(replacement_pattern, self.__replace_with_patterns_model)

        settings = self.__get_settings()

        LOGGER.debug("> 'Search' on '{0}' search pattern with '{1}' settings.".format(search_pattern, settings))

        return editor.search(search_pattern, **settings)

    def replace(self):
        """
        Replaces current editor Widget current search pattern occurence with replacement pattern.

        :return: Method success.
        :rtype: bool
        """

        editor = self.__container.get_current_editor()
        search_pattern = self.Search_comboBox.currentText()
        replacement_pattern = self.Replace_With_comboBox.currentText()

        if not editor or not search_pattern:
            return False

        self.insert_pattern(search_pattern, self.__search_patterns_model)
        self.insert_pattern(replacement_pattern, self.__replace_with_patterns_model)

        settings = self.__get_settings()

        LOGGER.debug("> 'Replace' on search '{0}' pattern, '{1}' replacement pattern with '{2}' settings.".format(
        search_pattern, replacement_pattern, settings))

        return editor.replace(search_pattern, replacement_pattern, **settings)

    def replace_all(self):
        """
        Replaces current editor Widget search pattern occurrences with replacement pattern.

        :return: Method success.
        :rtype: bool
        """

        editor = self.__container.get_current_editor()
        search_pattern = self.Search_comboBox.currentText()
        replacement_pattern = self.Replace_With_comboBox.currentText()

        if not editor or not search_pattern:
            return False

        self.insert_pattern(search_pattern, self.__search_patterns_model)
        self.insert_pattern(replacement_pattern, self.__replace_with_patterns_model)

        settings = self.__get_settings()
        settings.update({"backward_search" : False,
                        "wrap_around" : False})

        LOGGER.debug("> 'Replace All' on search '{0}' pattern, '{1}' replacement pattern with '{2}' settings.".format(
        search_pattern, replacement_pattern, settings))

        return editor.replace_all(search_pattern, replacement_pattern, **settings)
