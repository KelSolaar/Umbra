#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**components_manager_ui.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`ComponentsManagerUi` Component Interface class.

**Others:**

"""

from __future__ import unicode_literals

import os
import sys

if sys.version_info[:2] <= (2, 6):
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict
from PyQt4.QtCore import QMargins
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QAction

import foundations.exceptions
import foundations.walkers
import foundations.strings
import foundations.verbose
import manager.exceptions
import umbra.engine
import umbra.exceptions
import umbra.ui.nodes
from manager.QWidget_component import QWidgetComponentFactory
from umbra.components.factory.components_manager_ui.models import ComponentsModel
from umbra.components.factory.components_manager_ui.nodes import ComponentNode
from umbra.components.factory.components_manager_ui.nodes import PathNode
from umbra.components.factory.components_manager_ui.views import Components_QTreeView

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "ComponentsManagerUi"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Components_Manager_Ui.ui")


class ComponentsManagerUi(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
    """
    | Defines the :mod:`umbra.components.factory.components_manager_ui.components_manager_ui` Component Interface class.
    | It defines methods to interact with
        the :class:`manager.components_manager.Manager` class Application instance Components.
    """

    # Custom signals definitions.
    refresh_nodes = pyqtSignal()
    """
    This signal is emited by the :class:`ComponentsManagerUi` class when :obj:`ComponentsManagerUi.model` class property
    model Nodes nodes needs to be refreshed.
    """

    activated_component = pyqtSignal(unicode)
    """
    This signal is emited by the :class:`ComponentsManagerUi` class when a Component is activated.

    :return: Activated Component name.
    :rtype: unicode
    """

    deactivated_component = pyqtSignal(unicode)
    """
    This signal is emited by the :class:`ComponentsManagerUi` class when a Component is deactivated.

    :return: Deactivated Component name.
    :rtype: unicode
    """

    reloaded_component = pyqtSignal(unicode)
    """
    This signal is emited by the :class:`ComponentsManagerUi` class when a Component is reloaded.

    :return: Reloaded Component name.
    :rtype: unicode
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

        super(ComponentsManagerUi, self).__init__(parent, name, *args, **kwargs)

        # --- Setting class attributes. ---
        self.deactivatable = False

        self.__ui_resources_directory = "resources"
        self.__ui_activated_image = "Activated.png"
        self.__ui_deactivated_image = "Deactivated.png"
        self.__ui_category_affixe = "_Category.png"
        self.__dock_area = 1

        self.__engine = None
        self.__settings = None

        self.__model = None
        self.__view = None

        self.__headers = OrderedDict([("Components", "name"),
                                      ("Activated", "activated"),
                                      ("Category", "category"),
                                      ("Dependencies", "require"),
                                      ("Version", "version")])

        self.__tree_view_inner_margins = QMargins(0, 0, 0, 12)
        self.__components_informations_default_text = \
            "<center><h4>* * *</h4>Select some Components to display related informations!<h4>* * *</h4></center>"
        self.__components_informations_text = """
                                            <h4><center>{0}</center></h4>
                                            <p>
                                            <b>Category:</b> {1}
                                            <br/>
                                            <b>Author:</b> {2}
                                            <br/>
                                            <b>Email:</b> <a href="mailto:{3}">
                                            <span style=" text-decoration: underline; color:#e0e0e0;">{3}</span></a>
                                            <br/>
                                            <b>Url:</b> <a href="{4}">
                                            <span style=" text-decoration: underline; color:#e0e0e0;">{4}</span></a>
                                            <p>
                                            <b>Description:</b> {5}
                                            </p>
                                            </p>
                                            """

    @property
    def ui_resources_directory(self):
        """
        Property for **self.__ui_resources_directory** attribute.

        :return: self.__ui_resources_directory.
        :rtype: unicode
        """

        return self.__ui_resources_directory

    @ui_resources_directory.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_resources_directory(self, value):
        """
        Setter for **self.__ui_resources_directory** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_resources_directory"))

    @ui_resources_directory.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_resources_directory(self):
        """
        Deleter for **self.__ui_resources_directory** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_resources_directory"))

    @property
    def ui_activated_image(self):
        """
        Property for **self.__ui_activated_image** attribute.

        :return: self.__ui_activated_image.
        :rtype: unicode
        """

        return self.__ui_activated_image

    @ui_activated_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_activated_image(self, value):
        """
        Setter for **self.__ui_activated_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_activated_image"))

    @ui_activated_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_activated_image(self):
        """
        Deleter for **self.__ui_activated_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_activated_image"))

    @property
    def ui_deactivated_image(self):
        """
        Property for **self.__ui_deactivated_image** attribute.

        :return: self.__ui_deactivated_image.
        :rtype: unicode
        """

        return self.__ui_deactivated_image

    @ui_deactivated_image.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_deactivated_image(self, value):
        """
        Setter for **self.__ui_deactivated_image** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_deactivated_image"))

    @ui_deactivated_image.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_deactivated_image(self):
        """
        Deleter for **self.__ui_deactivated_image** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_deactivated_image"))

    @property
    def ui_category_affixe(self):
        """
        Property for **self.__ui_category_affixe** attribute.

        :return: self.__ui_category_affixe.
        :rtype: unicode
        """

        return self.__ui_category_affixe

    @ui_category_affixe.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_category_affixe(self, value):
        """
        Setter for **self.__ui_category_affixe** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "ui_category_affixe"))

    @ui_category_affixe.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def ui_category_affixe(self):
        """
        Deleter for **self.__ui_category_affixe** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "ui_category_affixe"))

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
    def model(self):
        """
        Property for **self.__model** attribute.

        :return: self.__model.
        :rtype: ComponentsModel
        """

        return self.__model

    @model.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def model(self, value):
        """
        Setter for **self.__model** attribute.

        :param value: Attribute value.
        :type value: ComponentsModel
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
        :rtype: list
        """

        return self.__headers

    @headers.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def headers(self, value):
        """
        Setter for **self.__headers** attribute.

        :param value: Attribute value.
        :type value: list
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
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "headers"))

    @property
    def tree_view_inner_margins(self):
        """
        Property for **self.__tree_view_inner_margins** attribute.

        :return: self.__tree_view_inner_margins.
        :rtype: int
        """

        return self.__tree_view_inner_margins

    @tree_view_inner_margins.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def tree_view_inner_margins(self, value):
        """
        Setter for **self.__tree_view_inner_margins** attribute.

        :param value: Attribute value.
        :type value: int
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tree_view_inner_margins"))

    @tree_view_inner_margins.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def tree_view_inner_margins(self):
        """
        Deleter for **self.__tree_view_inner_margins** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tree_view_inner_margins"))

    @property
    def components_informations_default_text(self):
        """
        Property for **self.__components_informations_default_text** attribute.

        :return: self.__components_informations_default_text.
        :rtype: unicode
        """

        return self.__components_informations_default_text

    @components_informations_default_text.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def components_informations_default_text(self, value):
        """
        Setter for **self.__components_informations_default_text** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__,
                                                         "components_informations_default_text"))

    @components_informations_default_text.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def components_informations_default_text(self):
        """
        Deleter for **self.__components_informations_default_text** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__,
                                                             "components_informations_default_text"))

    @property
    def components_informations_text(self):
        """
        Property for **self.__components_informations_text** attribute.

        :return: self.__components_informations_text.
        :rtype: unicode
        """

        return self.__components_informations_text

    @components_informations_text.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def components_informations_text(self, value):
        """
        Setter for **self.__components_informations_text** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "components_informations_text"))

    @components_informations_text.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def components_informations_text(self):
        """
        Deleter for **self.__components_informations_text** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "components_informations_text"))

    def activate(self, engine):
        """
        Activates the Component.

        :param engine: Engine to attach the Component to.
        :type engine: QObject
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

        self.__ui_resources_directory = os.path.join(os.path.dirname(__file__), self.__ui_resources_directory)
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

        self.__model = ComponentsModel(self, horizontal_headers=self.__headers)
        self.set_components()

        self.Components_Manager_Ui_treeView.setParent(None)
        self.Components_Manager_Ui_treeView = Components_QTreeView(self, self.__model)
        self.Components_Manager_Ui_treeView.setObjectName("Components_Manager_Ui_treeView")
        self.Components_Manager_Ui_gridLayout.setContentsMargins(self.__tree_view_inner_margins)
        self.Components_Manager_Ui_gridLayout.addWidget(self.Components_Manager_Ui_treeView, 0, 0)
        self.__view = self.Components_Manager_Ui_treeView
        self.__view.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.__view_add_actions()

        self.Components_Informations_textBrowser.setText(self.__components_informations_default_text)

        self.Components_Manager_Ui_splitter.setSizes([16777215, 1])

        # Signals / Slots.
        self.__view.selectionModel().selectionChanged.connect(self.__view_selectionModel__selectionChanged)
        self.refresh_nodes.connect(self.__model__refresh_nodes)

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

    def on_startup(self):
        """
        Defines the slot triggered by Framework startup.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Calling '{0}' Component Framework 'on_startup' method.".format(self.__class__.__name__))

        self.refresh_nodes.emit()
        return True

    def __model__refresh_nodes(self):
        """
        Defines the slot triggered by the Model when nodes need refresh.
        """

        LOGGER.debug("> Refreshing '{0}' Model!".format("Components_Manager_Ui_treeView"))

        self.set_components()

    def __view_add_actions(self):
        """
        Sets the **Components_Manager_Ui_treeView** actions.
        """

        self.Components_Manager_Ui_treeView.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|factory.ComponentsManagerUi|Activate Component(s)",
            slot=self.__view_activate_components_action__triggered))
        self.Components_Manager_Ui_treeView.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|factory.ComponentsManagerUi|Deactivate Component(s)",
            slot=self.__view_deactivate_components_action__triggered))

        separator_action = QAction(self.Components_Manager_Ui_treeView)
        separator_action.setSeparator(True)
        self.Components_Manager_Ui_treeView.addAction(separator_action)

        self.Components_Manager_Ui_treeView.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|factory.ComponentsManagerUi|Reload Component(s)",
            slot=self.__view_reload_components_action__triggered))

        separator_action = QAction(self.Components_Manager_Ui_treeView)
        separator_action.setSeparator(True)
        self.Components_Manager_Ui_treeView.addAction(separator_action)

    def __view_activate_components_action__triggered(self, checked):
        """
        Defines the slot triggered by \*\*'Actions|Umbra|Components|factory.ComponentsManagerUi|Activate Component(s)'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.activate_components_ui()

    def __view_deactivate_components_action__triggered(self, checked):
        """
        Defines the slot triggered by
        **'Actions|Umbra|Components|factory.ComponentsManagerUi|Deactivate Component(s)'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.deactivate_components_ui()

    def __view_reload_components_action__triggered(self, checked):
        """
        Defines the slot triggered by \*\*'Actions|Umbra|Components|factory.ComponentsManagerUi|Reload Component(s)'** action.

        :param checked: Action checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.reload_components_ui()

    def __view_selectionModel__selectionChanged(self, selected_items, deselected_items):
        """
        Sets the **Additional_Informations_textEdit** Widget.

        :param selected_items: Selected items.
        :type selected_items: QItemSelection
        :param deselected_items: Deselected items.
        :type deselected_items: QItemSelection
        """

        LOGGER.debug("> Initializing '{0}' Widget.".format("Additional_Informations_textEdit"))

        selected_components = self.get_selected_components()
        content = []
        if selected_components:
            for item in selected_components:
                content.append(self.__components_informations_text.format(item.name,
                                                                          item.category,
                                                                          item.author,
                                                                          item.email,
                                                                          item.url,
                                                                          item.description))
        else:
            content.append(self.__components_informations_default_text)

        separator = "" if len(content) == 1 else "<p><center>* * *<center/></p>"
        self.Components_Informations_textBrowser.setText(separator.join(content))

    def __store_deactivated_components(self):
        """
        Stores deactivated Components in settings file.
        """

        deactivated_components = []
        for node in foundations.walkers.nodes_walker(self.__model.root_node):
            if node.family == "Component":
                node.component.interface.activated or deactivated_components.append(node.component.name)

        LOGGER.debug("> Storing '{0}' deactivated Components.".format(", ".join(deactivated_components)))
        self.__settings.set_key("Settings", "deactivated_components", ",".join(deactivated_components))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                              manager.exceptions.ComponentActivationError)
    @umbra.engine.encapsulate_processing
    def activate_components_ui(self):
        """
        Activates user selected Components.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        selected_components = self.get_selected_components()

        self.__engine.start_processing("Activating Components ...", len(selected_components))
        activation_failed_components = []
        for component in selected_components:
            if not component.interface.activated:
                success = self.activate_component(component.name) or False
                if not success:
                    activation_failed_components.append(component)
            else:
                self.__engine.notifications_manager.warnify("{0} | '{1}' Component is already activated!".format(
                    self.__class__.__name__, component.name))
            self.__engine.step_processing()
        self.__engine.stop_processing()

        self.__store_deactivated_components()

        if not activation_failed_components:
            return True
        else:
            raise manager.exceptions.ComponentActivationError(
                "{0} | Exception(s) raised while activating '{1}' Component(s)!".format(self.__class__.__name__,
                                                                                        ", ".join((
                                                                                        activation_failed_component.name
                                                                                        for activation_failed_component
                                                                                        in
                                                                                        activation_failed_components))))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                              manager.exceptions.ComponentDeactivationError)
    @umbra.engine.encapsulate_processing
    def deactivate_components_ui(self):
        """
        Deactivates user selected Components.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        selected_components = self.get_selected_components()

        self.__engine.start_processing("Deactivating Components ...", len(selected_components))
        deactivation_failed_components = []
        for component in selected_components:
            if component.interface.activated:
                if component.interface.deactivatable:
                    success = self.deactivate_component(component.name) or False
                    if not success:
                        deactivation_failed_components.append(component)
                else:
                    self.__engine.notifications_manager.warnify(
                        "{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, component.name))
            else:
                self.__engine.notifications_manager.warnify(
                    "{0} | '{1}' Component is already deactivated!".format(self.__class__.__name__, component.name))
            self.__engine.step_processing()
        self.__engine.stop_processing()

        self.__store_deactivated_components()

        if not deactivation_failed_components:
            return True
        else:
            raise manager.exceptions.ComponentDeactivationError(
                "{0} | Exception(s) raised while deactivating '{1}' Component(s)!".format(self.__class__.__name__,
                                                                                          ", ".join((
                                                                                          deactivation_failed_component.name
                                                                                          for
                                                                                          deactivation_failed_component
                                                                                          in
                                                                                          deactivation_failed_components))))

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                              manager.exceptions.ComponentReloadError)
    @umbra.engine.encapsulate_processing
    def reload_components_ui(self):
        """
        Reloads user selected Components.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        selected_components = self.get_selected_components()

        self.__engine.start_processing("Reloading Components ...", len(selected_components))
        reload_failed_components = []
        for component in selected_components:
            if component.interface.deactivatable:
                success = self.reload_component(component.name) or False
                if not success:
                    reload_failed_components.append(component)
            else:
                self.__engine.notifications_manager.warnify(
                    "{0} | '{1}' Component cannot be deactivated and won't be reloaded!".format(self.__class__.__name__,
                                                                                                component.name))
            self.__engine.step_processing()
        self.__engine.stop_processing()

        if not reload_failed_components:
            return True
        else:
            raise manager.exceptions.ComponentReloadError(
                "{0} | Exception(s) raised while reloading '{1}' Component(s)!".format(self.__class__.__name__,
                                                                                       ", ".join(
                                                                                           (reload_failed_component.name
                                                                                            for reload_failed_component
                                                                                            in
                                                                                            reload_failed_components))))

    @foundations.exceptions.handle_exceptions(manager.exceptions.ComponentExistsError, Exception)
    def activate_component(self, name):
        """
        Activates given Component.

        :param name: Component name.
        :type name: unicode
        :return: Method success.
        :rtype: bool
        """

        if not name in self.__engine.components_manager.components:
            raise manager.exceptions.ComponentExistsError(
                "{0} | '{1}' Component isn't registered in the Components Manager!".format(self.__class__.__name__,
                                                                                           name))

        component = self.__engine.components_manager.components[name]
        if component.interface.activated:
            LOGGER.warning("!> {0} | '{1}' Component is already activated!".format(self.__class__.__name__, name))
            return False

        LOGGER.debug("> Attempting '{0}' Component activation.".format(component.name))
        component.interface.activate(self.__engine)
        if component.category in ("Default", "QObject"):
            component.interface.initialize()
        elif component.category == "QWidget":
            component.interface.initialize_ui()
            component.interface.add_widget()
        LOGGER.info("{0} | '{1}' Component has been activated!".format(self.__class__.__name__, component.name))
        self.activated_component.emit(name)
        self.refresh_nodes.emit()
        return True

    @foundations.exceptions.handle_exceptions(manager.exceptions.ComponentExistsError,
                                              manager.exceptions.ComponentDeactivationError)
    def deactivate_component(self, name):
        """
        Deactivates given Component.

        :param name: Component name.
        :type name: unicode
        :return: Method success.
        :rtype: bool
        """

        if not name in self.__engine.components_manager.components:
            raise manager.exceptions.ComponentExistsError(
                "{0} | '{0}' Component isn't registered in the Components Manager!".format(self.__class__.__name__,
                                                                                           name))

        component = self.__engine.components_manager.components[name]
        if not component.interface.activated:
            LOGGER.warning("!> {0} | '{1}' Component is already deactivated!".format(self.__class__.__name__, name))
            return False

        LOGGER.debug("> Attempting '{0}' Component deactivation.".format(component.name))
        if component.interface.deactivatable:
            if component.category in ("Default", "QObject"):
                component.interface.uninitialize()
            elif component.category == "QWidget":
                component.interface.uninitialize_ui()
                component.interface.remove_widget()
            component.interface.deactivate()
            LOGGER.info("{0} | '{1}' Component has been deactivated!".format(self.__class__.__name__, component.name))
            self.deactivated_component.emit(name)
            self.refresh_nodes.emit()
            return True
        else:
            raise manager.exceptions.ComponentDeactivationError(
                "{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, component.name))

    @foundations.exceptions.handle_exceptions(manager.exceptions.ComponentExistsError,
                                              manager.exceptions.ComponentReloadError)
    def reload_component(self, name):
        """
        Reloads given Component.

        :param name: Component name.
        :type name: unicode
        :return: Method success.
        :rtype: bool
        """

        if not name in self.__engine.components_manager.components:
            raise manager.exceptions.ComponentExistsError(
                "{0} | '{1}' Component isn't registered in the Components Manager!".format(self.__class__.__name__,
                                                                                           name))

        component = self.__engine.components_manager.components[name]
        LOGGER.debug("> Attempting '{0}' Component reload.".format(component.name))
        if component.interface.deactivatable:
            dependents = list(reversed(self.__engine.components_manager.list_dependents(component.name)))

            if filter(lambda x: not self.__engine.components_manager[x].deactivatable, dependents):
                LOGGER.warning(
                    "!> {0} | '{1}' Component has non reloadable dependencies and won't be reloaded!".format(
                        self.__class__.__name__, component.name))
                return False

            LOGGER.info("{0} | '{1}' Component dependents: '{2}'.".format(self.__class__.__name__,
                                                                          component.name,
                                                                          ", ".join(dependents)))

            LOGGER.debug("> Deactivating '{0}' Component dependents.".format(component.name))
            dependents.append(component.name)
            for dependent in dependents:
                if self.__engine.components_manager[dependent].activated:
                    self.deactivate_component(dependent)
                self.__engine.process_events()

            LOGGER.debug("> Reloading '{0}' Component dependents.".format(component.name))
            self.__engine.components_manager.reload_component(component.name)

            LOGGER.debug("> Activating '{0}' Component dependents.".format(component.name))
            for dependent in reversed(dependents):
                if not self.__engine.components_manager[dependent].activated:
                    self.activate_component(dependent)
                self.__engine.process_events()

            LOGGER.info("{0} | '{1}' Component has been reloaded!".format(self.__class__.__name__, component.name))
            self.reloaded_component.emit(component.name)
            return True
        else:
            raise manager.exceptions.ComponentReloadError(
                "{0} | '{1}' Component cannot be deactivated and won't be reloaded!".format(self.__class__.__name__,
                                                                                            component.name))

    def get_components(self):
        """
        Returns the Components.

        :return: Components.
        :rtype: list
        """

        return self.__engine.components_manager.components

    def list_components(self):
        """
        Lists the Components names.

        :return: Components names.
        :rtype: list
        """

        return self.__engine.components_manager.list_components()

    def set_components(self):
        """
        Sets the Components Model nodes.
        """

        node_flags = attributes_flags = int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        root_node = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")

        paths = {}
        for path in self.__engine.components_manager.paths:
            basename = os.path.basename(path)
            if not paths.get(basename):
                paths[basename] = {}

            paths[basename].update(dict((name, component)
                                        for (name, component) in self.__engine.components_manager
                                        if basename == os.path.basename(os.path.dirname(component.directory))))

        for path, components in paths.iteritems():
            path_node = PathNode(name=path.title(),
                                 parent=root_node,
                                 node_flags=node_flags,
                                 attributes_flags=attributes_flags)

            for component in components.itervalues():
                if not component.interface:
                    continue

                component_node = ComponentNode(component,
                                               name=component.title,
                                               parent=path_node,
                                               node_flags=node_flags,
                                               attributes_flags=attributes_flags,
                                               activated=umbra.ui.nodes.GraphModelAttribute(name="activated",
                                                                                            flags=attributes_flags,
                                                                                            roles={
                                                                                            Qt.DisplayRole: foundations.strings.to_string(
                                                                                                component.interface.activated),
                                                                                            Qt.DecorationRole: os.path.join(
                                                                                                self.__ui_resources_directory,
                                                                                                component.interface.activated and
                                                                                                self.__ui_activated_image or self.__ui_deactivated_image)}))
                component_node.roles[Qt.DecorationRole] = os.path.join(self.__ui_resources_directory,
                                                                       "{0}{1}".format(component.category,
                                                                                       self.__ui_category_affixe))

        root_node.sort_children()

        self.__model.initialize_model(root_node)
        return True

    def get_selected_nodes(self):
        """
        Returns the View selected nodes.

        :return: View selected nodes.
        :rtype: dict
        """

        return self.__view.get_selected_nodes()

    def get_selected_components_nodes(self):
        """
        Returns the View selected Components nodes.

        :return: View selected Components nodes.
        :rtype: list
        """

        return [node for node in self.get_selected_nodes() if node.family == "Component"]

    def get_selected_components(self):
        """
        Returns the View selected Components.

        :return: View selected Components.
        :rtype: list
        """

        return [node.component for node in self.get_selected_components_nodes()]
