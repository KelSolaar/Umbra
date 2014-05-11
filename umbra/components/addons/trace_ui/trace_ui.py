#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**trace_ui.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`TraceUi` Component Interface class and others helper objects.

**Others:**

"""

from __future__ import unicode_literals

import os
import re
import sys
if sys.version_info[:2] <= (2, 6):
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal

import foundations.exceptions
import foundations.verbose
import foundations.strings
import foundations.trace
import umbra.exceptions
import umbra.ui.nodes
from manager.QWidget_component import QWidgetComponentFactory
from umbra.components.addons.trace_ui.models import ModulesModel
from umbra.components.addons.trace_ui.nodes import ModuleNode
from umbra.components.addons.trace_ui.views import Modules_QTreeView
from umbra.ui.widgets.search_QLineEdit import Search_QLineEdit

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "TraceUi"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Trace_Ui.ui")

class TraceUi(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
    """
    Defines the :mod:`umbra.components.addons.trace_ui.trace_ui` Component Interface class.
    """

    # Custom signals definitions.
    refresh_nodes = pyqtSignal()
    """
    This signal is emited by the :class:`TraceUi` class when :obj:`TraceUi.model` class property model
    nodes needs to be refreshed.
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

        super(TraceUi, self).__init__(parent, name, *args, **kwargs)

        # --- Setting class attributes. ---
        self.deactivatable = True

        self.__dock_area = 1

        self.__engine = None
        self.__settings = None
        self.__settings_section = None

        self.__model = None
        self.__view = None
        self.__headers = OrderedDict([("Module", "name"),
                                        ("Traced", "traced")])

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

    @property
    def settings_section(self):
        """
        Property for **self.__settings_section** attribute.

        :return: self.__settings_section.
        :rtype: unicode
        """

        return self.__settings_section

    @settings_section.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def settings_section(self, value):
        """
        Setter for **self.__settings_section** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings_section"))

    @settings_section.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def settings_section(self):
        """
        Deleter for **self.__settings_section** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings_section"))

    @property
    def model(self):
        """
        Property for **self.__model** attribute.

        :return: self.__model.
        :rtype: CollectionsModel
        """

        return self.__model

    @model.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def model(self, value):
        """
        Setter for **self.__model** attribute.

        :param value: Attribute value.
        :type value: CollectionsModel
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
    def headers(self):
        """
        Property for **self.__headers** attribute.

        :return: self.__headers.
        :rtype: OrderedDict
        """

        return self.__headers

    @headers.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def headers(self, value):
        """
        Setter for **self.__headers** attribute.

        :param value: Attribute value.
        :type value: OrderedDict
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "headers"))

    @headers.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def headers(self):
        """
        Deleter for **self.__headers** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

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
        self.__settings_section = self.name

        self.activated = True
        return True

    def deactivate(self):
        """
        Deactivates the Component.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

        self.__engine = None
        self.__settings = None
        self.__settings_section = None

        self.activated = False
        return True

    def initialize_ui(self):
        """
        Initializes the Component ui.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

        self.Trace_Modules_Filter_lineEdit = Search_QLineEdit(self)
        self.Trace_Modules_Filter_lineEdit.search_active_label.hide()
        self.Trace_Modules_Filter_lineEdit.setPlaceholderText("Objects Trace Filter ...")
        self.Trace_Modules_Filter_horizontalLayout.addWidget(self.Trace_Modules_Filter_lineEdit)

        self.__model = ModulesModel(self, horizontal_headers=self.__headers)

        self.Modules_treeView.setParent(None)
        self.Modules_treeView = Modules_QTreeView(self, self.__model)
        self.Modules_treeView.setObjectName("Modules_treeView")
        self.Modules_treeView.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.Trace_Ui_dockWidgetContents_gridLayout.addWidget(self.Modules_treeView, 0, 0)
        self.__view = self.Modules_treeView
        self.__view_add_actions()

        self.set_modules()

        # Signals / Slots.
        self.refresh_nodes.connect(self.__model__refresh_nodes)

        self.initialized_ui = True
        return True

    def uninitialize_ui(self):
        """
        Uninitializes the Component ui.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

        # Signals / Slots.
        self.refresh_nodes.disconnect(self.__model__refresh_nodes)

        self.__view_remove_actions()

        self.__model = None
        self.__view = None

        self.initialized_ui = False
        return True

    def add_widget(self):
        """
        Adds the Component Widget to the engine.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

        self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dock_area), self)

        return True

    def remove_widget(self):
        """
        Removes the Component Widget from the engine.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

        self.__engine.removeDockWidget(self)
        self.setParent(None)

        return True

    def __model__refresh_nodes(self):
        """
        Defines the slot triggered by the Model when Nodes need refresh.
        """

        self.set_modules()

    def __model__refresh_attributes(self):
        """
        Refreshes the Model Nodes attributes.
        """

        for node in foundations.walkers.nodes_walker(self.__model.root_node):
            if foundations.trace.is_traced(node.module) == node.traced.value:
                continue

            node.update_node_attributes()

    def __view_add_actions(self):
        """
        Sets the View actions.
        """

        self.__view.addAction(self.__engine.actions_manager.register_action(
        "Actions|Umbra|Components|addons.trace_ui|Trace Module(s)",
        slot=self.__view_trace_modules_action__triggered))
        self.__view.addAction(self.__engine.actions_manager.register_action(
        "Actions|Umbra|Components|addons.trace_ui|Untrace Module(s)",
        slot=self.__view_untrace_modules_action__triggered))

    def __view_remove_actions(self):
        """
        Removes the View actions.
        """

        trace_modules_action = "Actions|Umbra|Components|addons.trace_ui|Trace Module(s)"
        untrace_modules_action = "Actions|Umbra|Components|addons.trace_ui|Untrace Module(s)"

        for action in (trace_modules_action, untrace_modules_action):
            self.__view.removeAction(self.__engine.actions_manager.get_action(action))
            self.__engine.actions_manager.unregister_action(action)

    def __view_trace_modules_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|addons.trace_ui|Trace Module(s)'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        pattern = foundations.strings.to_string(self.Trace_Modules_Filter_lineEdit.text()) or r".*"
        flags = re.IGNORECASE if self.Case_Sensitive_Matching_pushButton.isChecked() else 0
        return self.trace_modules(self.get_selected_modules(), pattern, flags)

    def __view_untrace_modules_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|addons.trace_ui|Untrace Module(s)'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.untrace_modules(self.get_selected_modules())

    def get_selected_nodes(self):
        """
        Returns the View selected nodes.

        :return: View selected nodes.
        :rtype: dict
        """

        return self.__view.get_selected_nodes()

    def get_selected_modules(self):
        """
        Returns the View selected modules.

        :return: View selected modules.
        :rtype: list
        """

        return [node.module for node in self.get_selected_nodes()]

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                            foundations.exceptions.UserError)
    def trace_modules(self, modules, pattern=r".*", flags=re.IGNORECASE):
        """
        Traces given modules using given filter pattern.

        :param modules: Modules to trace.
        :type modules: list
        :param pattern: Matching pattern.
        :type pattern: unicode
        :param flags: Matching regex flags.
        :type flags: int
        :return: Method success.
        :rtype: bool
        """

        try:
            pattern = re.compile(pattern, flags)
        except Exception:
            raise foundations.exceptions.UserError(
            "{0} | Invalid objects trace filter pattern: Regex compilation failed!".format(self.__class__.__name__))

        for module in modules:
            foundations.trace.trace_module(module, foundations.verbose.tracer, pattern)
        self.__model__refresh_attributes()
        return True

    def untrace_modules(self, modules):
        """
        Untraces given modules.

        :param modules: Modules to untrace.
        :type modules: list
        :return: Method success.
        :rtype: bool
        """

        for module in modules:
            foundations.trace.untrace_module(module)
        self.__model__refresh_attributes()
        return True

    def get_modules(self):
        """
        Sets the registered Modules.

        :return: Registered modules.
        :rtype: list
        """

        return foundations.trace.REGISTERED_MODULES

    def set_modules(self, modules=None):
        """
        Sets the modules Model nodes.

        :param modules: Modules to set.
        :type modules: list
        :return: Method success.
        :rtype: bool
        """

        node_flags = int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        modules = modules or self.get_modules()
        root_node = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")
        for module in modules:
            module_node = ModuleNode(module=module,
                                    name=foundations.strings.to_string(module.__name__),
                                    parent=root_node,
                                    node_flags=node_flags,
                                    attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))

        root_node.sort_children()

        self.__model.initialize_model(root_node)
        return True
