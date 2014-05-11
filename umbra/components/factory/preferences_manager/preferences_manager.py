#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**preferences_manager.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`PreferencesManager` Component Interface class.

**Others:**

"""

from __future__ import unicode_literals

import os
from PyQt4.QtCore import QStringList
from PyQt4.QtCore import Qt

import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.ui.common
from manager.QWidget_component import QWidgetComponentFactory
from umbra.globals.constants import Constants
from umbra.globals.runtime_globals import RuntimeGlobals

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "PreferencesManager"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Preferences_Manager.ui")

class PreferencesManager(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
    """
    | Defines the :mod:`umbra.components.factory.preferences_manager.preferences_manager` Component Interface class.
    | It exposes Application preferences inside
        a dedicated `QDockWidget <http://doc.qt.nokia.com/qdockwidget.html>`_ window.
    """

    def __init__(self, parent=None, name=None, *args, **kwargs):
        """
        Initializes the class.

        :param parent: Object parent.
        :type parent: QObject
        :param name: Component name.
        :type name: unicode
        :param \*args: Arguments.
        :type \*args: \*
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        super(PreferencesManager, self).__init__(parent, name, *args, **kwargs)

        # --- Setting class attributes. ---
        self.deactivatable = False

        self.__dock_area = 2

        self.__engine = None
        self.__settings = None

    @property
    def dock_area(self):
        """
        Property for **self.__dock_area** attribute.

        :return: self.__dock_area.
        :rtype: int
        """

        return self.__dock_area

    @dock_area.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def dock_area(self, value):
        """
        Setter for **self.__dock_area** attribute.

        :param value: Attribute value.
        :type value: int
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dock_area"))

    @dock_area.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def dock_area(self):
        """
        Deleter for **self.__dock_area** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dock_area"))

    @property
    def engine(self):
        """
        Property for **self.__engine** attribute.

        :return: self.__engine.
        :rtype: QObject
        """

        return self.__engine

    @engine.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def engine(self, value):
        """
        Setter for **self.__engine** attribute.

        :param value: Attribute value.
        :type value: QObject
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

    @engine.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def engine(self):
        """
        Deleter for **self.__engine** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

    @property
    def settings(self):
        """
        Property for **self.__settings** attribute.

        :return: self.__settings.
        :rtype: QSettings
        """

        return self.__settings

    @settings.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def settings(self, value):
        """
        Setter for **self.__settings** attribute.

        :param value: Attribute value.
        :type value: QSettings
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

    @settings.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def settings(self):
        """
        Deleter for **self.__settings** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

    def activate(self, engine):
        """
        Activates the Component.

        :param engine: Engine to attach the Component to.
        :type engine: QObject
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

        self.__engine = engine

        self.__settings = self.__engine.settings

        self.activated = True
        return True

    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def deactivate(self):
        """
        Deactivates the Component.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

    def initialize_ui(self):
        """
        Initializes the Component ui.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

        umbra.ui.common.set_toolBox_height(self.Preferences_Manager_toolBox)

        self.__Logging_Formatters_comboBox_set_ui()
        self.__Verbose_Level_comboBox_set_ui()
        self.__Restore_Geometry_On_Layout_Change_checkBox_set_ui()

        # Signals / Slots.
        self.__engine.verbosity_level_changed.connect(self.__engine__verbosity_level_changed)
        self.Logging_Formatters_comboBox.activated.connect(self.__Logging_Formatters_comboBox__activated)
        self.Verbose_Level_comboBox.activated.connect(self.__Verbose_Level_comboBox__activated)
        self.Restore_Geometry_On_Layout_Change_checkBox.stateChanged.connect(
        self.__Restore_Geometry_On_Layout_Change_checkBox__stateChanged)

        self.initialized_ui = True
        return True

    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def uninitialize_ui(self):
        """
        Uninitializes the Component ui.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

    def add_widget(self):
        """
        Adds the Component Widget to the engine.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

        self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dock_area), self)

        return True

    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def remove_widget(self):
        """
        Removes the Component Widget from the engine.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

    def __engine__verbosity_level_changed(self, verbosity_level):
        """
        Defines the slot triggered by the engine when verbosity level has changed.

        :param verbosity_level: Current verbosity level.
        :type verbosity_level: int
        """

        self.Verbose_Level_comboBox.setCurrentIndex(verbosity_level)

    def __Logging_Formatters_comboBox_set_ui(self):
        """
        Fills **Logging_Formatter_comboBox** Widget.
        """

        self.Logging_Formatters_comboBox.clear()
        LOGGER.debug("> Available logging formatters: '{0}'.".format(", ".join(RuntimeGlobals.logging_formatters)))
        self.Logging_Formatters_comboBox.insertItems(0, QStringList(RuntimeGlobals.logging_formatters.keys()))
        logging_formatter = self.__settings.get_key("Settings", "logging_formatter").toString()
        self.__engine.logging_active_formatter = logging_formatter and logging_formatter or Constants.logging_default_formatter
        self.Logging_Formatters_comboBox.setCurrentIndex(self.Logging_Formatters_comboBox.findText(
        self.__engine.logging_active_formatter, Qt.MatchExactly))

    def __Logging_Formatters_comboBox__activated(self, index):
        """
        Defines the slot triggered by the **Logging_Formatter_comboBox** Widget when activated.

        :param index: ComboBox activated item index.
        :type index: int
        """

        formatter = foundations.strings.to_string(self.Logging_Formatters_comboBox.currentText())
        LOGGER.debug("> Setting logging formatter: '{0}'.".format(formatter))
        RuntimeGlobals.logging_active_formatter = formatter
        self.set_logging_formatter()
        self.__settings.set_key("Settings", "logging_formatter", self.Logging_Formatters_comboBox.currentText())

    def __Verbose_Level_comboBox_set_ui(self):
        """
        Fills **Verbose_Level_ComboBox** Widget.
        """

        self.Verbose_Level_comboBox.clear()
        LOGGER.debug("> Available verbose levels: '{0}'.".format(Constants.verbosity_labels))
        self.Verbose_Level_comboBox.insertItems(0, QStringList (Constants.verbosity_labels))
        self.__engine.verbosity_level = foundations.common.get_first_item(
                                    self.__settings.get_key("Settings", "verbosity_level").toInt())
        self.Verbose_Level_comboBox.setCurrentIndex(self.__engine.verbosity_level)

    def __Verbose_Level_comboBox__activated(self, index):
        """
        Defines the slot triggered by the **Verbose_Level_ComboBox** Widget when activated.

        :param index: ComboBox activated item index.
        :type index: int
        """

        LOGGER.debug("> Setting verbose level: '{0}'.".format(self.Verbose_Level_comboBox.currentText()))
        self.__engine.verbosity_level = index
        foundations.verbose.set_verbosity_level(index)
        self.__settings.set_key("Settings", "verbosity_level", index)

    def __Restore_Geometry_On_Layout_Change_checkBox_set_ui(self):
        """
        Sets the **Restore_Geometry_On_Layout_Change_checkBox** Widget.
        """

        # Adding settings key if it doesn't exists.
        self.__settings.get_key("Settings", "restore_geometry_on_layout_change").isNull() and \
        self.__settings.set_key("Settings", "restore_geometry_on_layout_change", Qt.Unchecked)

        restore_geometry_on_layout_change = foundations.common.get_first_item(
                                        self.__settings.get_key("Settings", "restore_geometry_on_layout_change").toInt())
        LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Restore_Geometry_On_Layout_Change_checkBox",
                                                                restore_geometry_on_layout_change))
        self.Restore_Geometry_On_Layout_Change_checkBox.setCheckState(restore_geometry_on_layout_change)
        self.__engine.layouts_manager.restore_geometry_on_layout_change = True if restore_geometry_on_layout_change else False

    def __Restore_Geometry_On_Layout_Change_checkBox__stateChanged(self, state):
        """
        Defines the slot triggered by **Restore_Geometry_On_Layout_Change_checkBox** Widget when state changed.

        :param state: Checkbox state.
        :type state: int
        """

        LOGGER.debug("> 'Restore Geometry On Layout Change' state: '{0}'.".format(state))
        self.__settings.set_key("Settings", "restore_geometry_on_layout_change", state)
        self.__engine.layouts_manager.restore_geometry_on_layout_change = state and True or False

    def set_logging_formatter(self):
        """
        Sets the logging formatter.
        """

        for handler in (RuntimeGlobals.logging_console_handler,
                        RuntimeGlobals.logging_file_handler,
                        RuntimeGlobals.logging_session_handler):
            handler and handler.setFormatter(RuntimeGlobals.logging_formatters[RuntimeGlobals.logging_active_formatter])
