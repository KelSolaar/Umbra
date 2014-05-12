#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**editor_status.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`EditorStatus` class.

**Others:**

"""

from __future__ import unicode_literals

import os
from PyQt4.QtCore import Qt

import foundations.exceptions
import foundations.ui.common
import foundations.strings
import foundations.verbose

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "UI_FILE", "EditorStatus"]

LOGGER = foundations.verbose.install_logger()

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Editor_Status.ui")


class EditorStatus(foundations.ui.common.QWidget_factory(ui_file=UI_FILE)):
    """
    Defines the
    :class:`umbra.components.factory.script_editor.script_editor.ScriptEditor` Component Interface class status bar widget.
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

        super(EditorStatus, self).__init__(parent, *args, **kwargs)

        # --- Setting class attributes. ---
        self.__container = parent

        self.__Lines_Columns_label_default_text = "Line {0} : Column {1}"

        EditorStatus.__initialize_ui(self)

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
    def Lines_Columns_label_default_text(self):
        """
        Property for **self.__Lines_Columns_label_default_text** attribute.

        :return: self.__Lines_Columns_label_default_text.
        :rtype: unicode
        """

        return self.__Lines_Columns_label_default_text

    @Lines_Columns_label_default_text.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def Lines_Columns_label_default_text(self, value):
        """
        Setter for **self.__Lines_Columns_label_default_text** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "Lines_Columns_label_default_text"))

    @Lines_Columns_label_default_text.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def Lines_Columns_label_default_text(self):
        """
        Deleter for **self.__Lines_Columns_label_default_text** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__,
                                                             "Lines_Columns_label_default_text"))

    def __initialize_ui(self):
        """
        Initializes the Widget ui.
        """

        self.Lines_Columns_label.setAlignment(Qt.AlignRight)
        self.Lines_Columns_label.setText(self.__Lines_Columns_label_default_text.format(1, 1))

        self.Languages_comboBox.setModel(self.__container.languages_model)

        # Signals / Slots.
        self.Languages_comboBox.currentIndexChanged.connect(self.__Languages_comboBox__currentIndexChanged)

    def __Languages_comboBox_set_default_view_state(self):
        """
        Sets the **Languages_comboBox** Widget default View state.
        """

        if not self.__container.has_editor_tab():
            return

        editor = self.__container.get_current_editor()
        index = self.Languages_comboBox.findText(editor.language.name)

        self.Languages_comboBox.setCurrentIndex(index)

    def __Languages_comboBox__currentIndexChanged(self, index):
        """
        Defines the slot triggered by the **Languages_comboBox** Widget when current index is changed.

        :param index: ComboBox current item index.
        :type index: int
        """

        if not self.__container.has_editor_tab():
            return

        language = self.__container.languages_model.get_language(foundations.strings.to_string(
            self.Languages_comboBox.currentText()))
        if not language:
            return

        editor = self.__container.get_current_editor()
        if editor.language == language:
            return

        editor.blockSignals(True)
        self.__container.set_language(editor, language)
        editor.blockSignals(False)

    def __editor__cursorPositionChanged(self):
        """
        Defines the slot triggered by :class:`umbra.components.factory.script_editor.script_editor.ScriptEditor`
        Component Interface class editor when cursor position is changed.
        """

        if not self.__container.has_editor_tab():
            return

        editor = self.__container.get_current_editor()
        self.Lines_Columns_label.setText(self.__Lines_Columns_label_default_text.format(editor.get_cursor_line() + 1,
                                                                                        editor.get_cursor_column() + 1))
