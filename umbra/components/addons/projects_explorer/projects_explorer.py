#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**projects_explorer.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`ProjectsExplorer` Component Interface class and others helper objects.

**Others:**

"""

from __future__ import unicode_literals

import itertools
import os
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QMessageBox

import foundations.exceptions
import foundations.io
import foundations.strings
import foundations.verbose
import umbra.exceptions
import umbra.ui.widgets.message_box as message_box
from manager.QWidget_component import QWidgetComponentFactory
from umbra.components.addons.projects_explorer.models import ProjectsProxyModel
from umbra.components.addons.projects_explorer.views import Projects_QTreeView
from umbra.ui.delegates import RichText_QStyledItemDelegate
from umbra.ui.delegates import Style

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "ProjectsExplorer"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Projects_Explorer.ui")


class ProjectsExplorer(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
    """
    Defines the :mod:`sibl_gui.components.addons.projects_explorer.projects_explorer` Component Interface class.
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

        super(ProjectsExplorer, self).__init__(parent, name, *args, **kwargs)

        # --- Setting class attributes. ---
        self.deactivatable = True

        self.__dock_area = 1

        self.__engine = None
        self.__settings = None
        self.__settings_section = None

        self.__script_editor = None

        self.__model = None
        self.__view = None
        self.__delegate = None
        self.__style = Style(default="""
                                QLabel, QLabel link {
                                    background-color: rgb(32, 32, 32);
                                    color: rgb(192, 192, 192);
                                }
                                """,
                             hover="""
                                QLabel, QLabel link {
                                    background-color: rgb(64, 64, 64);
                                    color: rgb(192, 192, 192);
                                }
                                """,
                             highlight="""
                                QLabel, QLabel link {
                                    background-color: rgb(128, 128, 128);
                                    color: rgb(224, 224, 224);
                                }
                                """)

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
    def model(self):
        """
        Property for **self.__model** attribute.

        :return: self.__model.
        :rtype: ProjectsProxyModel
        """

        return self.__model

    @model.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def model(self, value):
        """
        Setter for **self.__model** attribute.

        :param value: Attribute value.
        :type value: ProjectsProxyModel
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
    def style(self):
        """
        Property for **self.__style** attribute.

        :return: self.__style.
        :rtype: Style
        """

        return self.__style

    @style.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def style(self, value):
        """
        Setter for **self.__style** attribute.

        :param value: Attribute value.
        :type value: Style
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "style"))

    @style.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def style(self):
        """
        Deleter for **self.__style** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "style"))

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

        self.__script_editor = self.__engine.components_manager["factory.script_editor"]

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

        self.__script_editor = None

        self.activated = False
        return True

    def initialize_ui(self):
        """
        Initializes the Component ui.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))
        self.__model = ProjectsProxyModel(self)
        self.__model.setSourceModel(self.__script_editor.model)
        self.__delegate = RichText_QStyledItemDelegate(self, self.__style)

        self.Projects_Explorer_treeView.setParent(None)
        self.Projects_Explorer_treeView = Projects_QTreeView(self, self.__model)
        self.Projects_Explorer_treeView.setItemDelegate(self.__delegate)
        self.Projects_Explorer_treeView.setObjectName("Projects_Explorer_treeView")
        self.Projects_Explorer_treeView.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.Projects_Explorer_dockWidgetContents_gridLayout.addWidget(self.Projects_Explorer_treeView, 0, 0)
        self.__view = self.Projects_Explorer_treeView
        self.__view_add_actions()

        self.__add_actions()

        # Signals / Slots.
        self.__view.expanded.connect(self.__view__expanded)
        self.__view.doubleClicked.connect(self.__view__doubleClicked)
        self.__view.selectionModel().selectionChanged.connect(self.__view_selectionModel__selectionChanged)
        self.__script_editor.Script_Editor_tabWidget.currentChanged.connect(
            self.__script_editor_Script_Editor_tabWidget__currentChanged)
        self.__script_editor.model.project_registered.connect(self.__script_editor_model__project_registered)

        self.initialized_ui = True
        return True

    def uninitialize_ui(self):
        """
        Uninitializes the Component ui.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

        self.__remove_actions()

        # Signals / Slots.
        self.__view.expanded.disconnect(self.__view__expanded)
        self.__view.doubleClicked.disconnect(self.__view__doubleClicked)
        self.__view.selectionModel().selectionChanged.disconnect(self.__view_selectionModel__selectionChanged)
        self.__script_editor.Script_Editor_tabWidget.currentChanged.disconnect(
            self.__script_editor_Script_Editor_tabWidget__currentChanged)
        self.__script_editor.model.project_registered.disconnect(self.__script_editor_model__project_registered)

        self.__view_remove_actions()

        self.__model = None
        self.__delegate = None
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

    def __add_actions(self):
        """
        Sets Component actions.
        """

        LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

        add_project_action = self.__engine.actions_manager.get_action(
            "Actions|Umbra|Components|factory.script_editor|&File|Add Project ...")
        remove_project_action = self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|factory.script_editor|&File|Remove Project",
            slot=self.__view_remove_project_action__triggered)
        self.__script_editor.file_menu.insertAction(add_project_action, remove_project_action)
        self.__script_editor.file_menu.removeAction(add_project_action)
        self.__script_editor.file_menu.insertAction(remove_project_action, add_project_action)

    def __remove_actions(self):
        """
        Removes actions.
        """

        LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

        remove_project_action = "Actions|Umbra|Components|factory.script_editor|&File|Remove Project"
        self.__script_editor.command_menu.removeAction(self.__engine.actions_manager.get_action(remove_project_action))
        self.__engine.actions_manager.unregister_action(remove_project_action)

    def __view_add_actions(self):
        """
        Sets the View actions.
        """

        self.__view.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|addons.projects_explorer|Add Project ...",
            slot=self.__view_add_project_action__triggered))
        self.__view.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|addons.projects_explorer|Remove Project",
            slot=self.__view_remove_project_action__triggered))

        separator_action = QAction(self.__view)
        separator_action.setSeparator(True)
        self.__view.addAction(separator_action)

        self.__view.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|addons.projects_explorer|Add New File ...",
            slot=self.__view_add_new_file_action__triggered))
        self.__view.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|addons.projects_explorer|Add New Directory ...",
            slot=self.__view_add_new_directory_action__triggered))

        separator_action = QAction(self.__view)
        separator_action.setSeparator(True)
        self.__view.addAction(separator_action)

        self.__view.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|addons.projects_explorer|Rename ...",
            slot=self.__view_rename_action__triggered))
        # self.__view.addAction(self.__engine.actions_manager.register_action(
        # "Actions|Umbra|Components|addons.projects_explorer|Copy ...",
        # slot=self.__view_copy_action__triggered))
        # self.__view.addAction(self.__engine.actions_manager.register_action(
        # "Actions|Umbra|Components|addons.projects_explorer|Move ...",
        # slot=self.__view_move_action__triggered))

        separator_action = QAction(self.__view)
        separator_action.setSeparator(True)
        self.__view.addAction(separator_action)

        self.__view.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|addons.projects_explorer|Delete ...",
            slot=self.__view_delete_action__triggered))

        separator_action = QAction(self.__view)
        separator_action.setSeparator(True)
        self.__view.addAction(separator_action)

        self.__view.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|addons.projects_explorer|Find In Files ...",
            slot=self.__view_find_in_files_action__triggered))

        separator_action = QAction(self.__view)
        separator_action.setSeparator(True)
        self.__view.addAction(separator_action)

        self.__view.addAction(self.__engine.actions_manager.register_action(
            "Actions|Umbra|Components|addons.projects_explorer|Output Selected Path",
            slot=self.__view_output_selected_path_action__triggered))

    def __view_remove_actions(self):
        """
        Removes the View actions.
        """

        add_project_action = "Actions|Umbra|Components|addons.projects_explorer|Add Project ..."
        remove_project_action = "Actions|Umbra|Components|addons.projects_explorer|Remove Project"
        add_new_file_action = "Actions|Umbra|Components|addons.projects_explorer|Add New File ..."
        add_new_directory_action = "Actions|Umbra|Components|addons.projects_explorer|Add New Directory ..."
        rename_action = "Actions|Umbra|Components|addons.projects_explorer|Rename ..."
        # copy_action = "Actions|Umbra|Components|addons.projects_explorer|Copy ..."
        # move_action = "Actions|Umbra|Components|addons.projects_explorer|Move ..."
        delete_action = "Actions|Umbra|Components|addons.projects_explorer|Delete ..."
        find_in_files_action = "Actions|Umbra|Components|addons.projects_explorer|Find In Files ..."
        output_selected_path_action = "Actions|Umbra|Components|addons.projects_explorer|Output Selected Path"

        for action in (add_project_action,
                       remove_project_action,
                       add_new_file_action,
                       add_new_directory_action,
                       rename_action,
                       # copy_action,
                       # move_action,
                       delete_action,
                       output_selected_path_action):
            self.__view.removeAction(self.__engine.actions_manager.get_action(action))
            self.__engine.actions_manager.unregister_action(action)

    def __view__expanded(self, index):
        """
        Defines the slot triggered by a View when an item is expanded.

        :param index: Expdanded item.
        :type index: QModelIndex
        """

        node = self.__model.get_node(index)
        if node.family != "Directory":
            return

        self.__script_editor.model.set_project_nodes(node)

    def __view__doubleClicked(self, index):
        """
        Defines the slot triggered by a View when double clicked.

        :param index: Clicked item index.
        :type index: QModelIndex
        """

        node = self.__model.get_node(index)
        if not node.family == "File":
            return

        foundations.common.path_exists(node.path) and self.__script_editor.load_file(node.path)

    def __view_selectionModel__selectionChanged(self, selected_items, deselected_items):
        """
        Defines the slot triggered by the View **selectionModel** when selection changed.

        :param selected_items: Selected items.
        :type selected_items: QItemSelection
        :param deselected_items: Deselected items.
        :type deselected_items: QItemSelection
        """

        for node in self.__view.get_selected_nodes():
            if node.family == "File":
                self.__script_editor.set_current_editor(node.path)

    def __script_editor_Script_Editor_tabWidget__currentChanged(self, index):
        """
        Defines the slot triggered by :class:`umbra.components.factory.script_editor.script_editor.ScriptEditor`
        Component Interface class when the current tab is changed.

        :param index: Tab index.
        :type index: int
        """

        editor = self.__script_editor.get_current_editor()
        if not editor:
            return

        editor_node = foundations.common.get_first_item(self.__script_editor.model.get_editor_nodes(editor))
        if not editor_node:
            return

        indexes = [self.__model.mapFromSource(self.__model.sourceModel().get_node_index(editor_node.parent))]
        self.__view.clearSelection()
        self.__view.select_indexes(indexes)

    def __script_editor_model__project_registered(self, project_node):
        """
        Defines the slot triggered by :class:`umbra.components.factory.script_editor.script_editor` class
        Model when a project is registered.

        :param project_node: Registered project ProjectNode.
        :type project_node: ProjectNode
        """

        index = self.__model.mapFromSource(self.__script_editor.model.get_node_index(project_node))
        self.__view.setExpanded(index, True)

    def __view_add_project_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|addons.projects_explorer|Add Project ...'** action.

        :param checked: Checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        return self.__script_editor.add_project_ui()

    def __view_remove_project_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|addons.projects_explorer|Remove Project'** action.

        :param checked: Checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        node = foundations.common.get_first_item(self.get_selected_nodes())
        if not node:
            return False

        return self.remove_project(node)

    def __view_add_new_file_action__triggered(self, checked):
        """
        Defines the slot triggered by **'"Actions|Umbra|Components|addons.projects_explorer|Add New File ..."'** action.

        :param checked: Checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        node = foundations.common.get_first_item(self.get_selected_nodes())
        if not node:
            return False

        return self.add_new_file(node)

    def __view_add_new_directory_action__triggered(self, checked):
        """
        Defines the slot triggered by **'"Actions|Umbra|Components|addons.projects_explorer|Add New Directory ..."'** action.

        :param checked: Checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        node = foundations.common.get_first_item(self.get_selected_nodes())
        if not node:
            return False

        return self.add_new_directory(node)

    def __view_rename_action__triggered(self, checked):
        """
        Defines the slot triggered by **'"Actions|Umbra|Components|addons.projects_explorer|Rename ..."'** action.

        :param checked: Checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        node = foundations.common.get_first_item(self.get_selected_nodes())
        if not node:
            return False

        return self.rename(node)

    # def __view_copy_action__triggered(self, checked):
    # 	"""
    # 	Defines the slot triggered by \*\*'"Actions|Umbra|Components|addons.projects_explorer|Copy ..."'** action.
    #
    # 	:param checked: Checked state.
    # 	:type :param: bool
    # 	:return: Method success.
    # 	:rtype: bool
    # 	"""
    #
    # 	print "Actions|Umbra|Components|addons.projects_explorer|Copy ..."

    # def __view_move_action__triggered(self, checked):
    # 	"""
    # 	Defines the slot triggered by \*\*'"Actions|Umbra|Components|addons.projects_explorer|Move ..."'** action.
    #
    # 	:param checked: Checked state.
    # 	:type :param: bool
    # 	:return: Method success.
    # 	:rtype: bool
    # 	"""
    #
    # 	print "Actions|Umbra|Components|addons.projects_explorer|Move ..."

    def __view_delete_action__triggered(self, checked):
        """
        Defines the slot triggered by **'"Actions|Umbra|Components|addons.projects_explorer|Delete ..."'** action.

        :param checked: Checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        node = foundations.common.get_first_item(self.get_selected_nodes())
        if not node:
            return False

        return self.delete(node)

    def __view_find_in_files_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|addons.projects_explorer|Find In Files ...'** action.

        :param checked: Checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        node = foundations.common.get_first_item(self.__view.get_selected_nodes().iterkeys())
        if not node:
            return False

        self.__script_editor.search_in_files.Where_lineEdit.setText(node.path)
        self.__script_editor.search_in_files.show()
        return True

    def __view_output_selected_path_action__triggered(self, checked):
        """
        Defines the slot triggered by **'Actions|Umbra|Components|addons.projects_explorer|Output Selected Path'** action.

        :param checked: Checked state.
        :type checked: bool
        :return: Method success.
        :rtype: bool
        """

        node = foundations.common.get_first_item(self.__view.get_selected_nodes().iterkeys())
        if not node:
            return False

        LOGGER.info("{0} | '{1}'.".format(self.__class__.__name__, node.path))
        return True

    @foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
                                              foundations.exceptions.FileExistsError,
                                              foundations.exceptions.DirectoryExistsError,
                                              Exception)
    def __raise_file_system_exception(self, item, directory):
        """
        Raises a common fileSystem exception.

        :param item: Name of the item generating the exception.
        :type item: unicode
        :param directory: Name of the target directory.
        :type directory: unicode
        """

        path = os.path.join(directory, item)
        if os.path.isfile(path):
            raise foundations.exceptions.FileExistsError(
                "{0} | A file with '{1}' name already exists in '{2}' directory!".format(self.__class__.__name__,
                                                                                         item,
                                                                                         directory))
        else:
            raise foundations.exceptions.DirectoryExistsError(
                "{0} | A directory with '{1}' name already exists in '{2}' directory!".format(self.__class__.__name__,
                                                                                              item,
                                                                                              directory))

    def __set_authoring_nodes(self, source, target):
        """
        Sets given editor authoring nodes.

        :param source: Source file.
        :type source: unicode
        :param target: Target file.
        :type target: unicode
        """

        editor = self.__script_editor.get_editor(source)
        editor.set_file(target)
        self.__script_editor.model.update_authoring_nodes(editor)

    def __rename_path(self, source, target):
        """
        Renames given source with given target name.

        :param source: Source file.
        :type source: unicode
        :param target: Target file.
        :type target: unicode
        """

        if not foundations.common.path_exists(source):
            return

        parent_directory = os.path.dirname(source)
        is_path_registered = self.__engine.file_system_events_manager.is_path_registered(parent_directory)
        is_path_registered and self.__engine.file_system_events_manager.unregister_path(parent_directory)
        os.rename(source, target)
        is_path_registered and self.__engine.file_system_events_manager.register_path(parent_directory)

    def __delete_path(self, path):
        """
        Deletes given path.

        :param path: Path to delete.
        :type path: unicode
        """

        if not foundations.common.path_exists(path):
            return

        parent_directory = os.path.dirname(path)
        is_path_registered = self.__engine.file_system_events_manager.is_path_registered(parent_directory)
        is_path_registered and self.__engine.file_system_events_manager.unregister_path(parent_directory)
        foundations.io.remove(path)
        is_path_registered and self.__engine.file_system_events_manager.register_path(parent_directory)

    def __rename_file(self, source, target):
        """
        Renames a file using given source and target names.

        :param source: Source file.
        :type source: unicode
        :param target: Target file.
        :type target: unicode
        """

        for file_node in self.__script_editor.model.get_file_nodes(source, self.__script_editor.model.root_node):
            self.__script_editor.unregister_node_path(file_node)
            self.__rename_path(source, target)
            self.__script_editor.register_node_path(file_node)
            if self.__script_editor.model.is_authoring_node(file_node):
                self.__set_authoring_nodes(source, target)
            else:
                self.__script_editor.model.update_project_nodes(file_node.parent)

    def __rename_directory(self, source, target):
        """
        Renames a directory using given source and target names.

        :param source: Source file.
        :type source: unicode
        :param target: Target file.
        :type target: unicode
        """

        for node in itertools.chain(self.__script_editor.model.get_project_nodes(source),
                                    self.__script_editor.model.get_directory_nodes(source)):
            self.__script_editor.model.unregister_project_nodes(node)
            self.__script_editor.unregister_node_path(node)
            self.__rename_path(source, target)
            node.name = os.path.basename(target)
            node.path = target
            self.__script_editor.model.node_changed(node)
            self.__script_editor.register_node_path(node)
            self.__script_editor.model.set_project_nodes(node)

    def __rename_project(self, source, target):
        """
        Renames a project using given source and target names.

        :param source: Source project.
        :type source: unicode
        :param target: Target project.
        :type target: unicode
        """

        self.__rename_directory(source, target)

    def __delete_file(self, file):
        """
        Deletes given file.

        :param file: File to delete.
        :type file: unicode
        """

        for file_node in self.__script_editor.model.get_file_nodes(file, self.__script_editor.model.root_node):
            self.__script_editor.unregister_node_path(file_node)
            self.__delete_path(file)
            if self.__script_editor.model.is_authoring_node(file_node):
                self.__script_editor.get_editor(file).set_modified(True)
            else:
                self.__script_editor.model.unregister_file(file_node)

    def __delete_directory(self, directory):
        """
        Deletes given directory.

        :param directory: Directory to delete.
        :type directory: unicode
        """

        for node in itertools.chain(self.__script_editor.model.get_project_nodes(directory),
                                    self.__script_editor.model.get_directory_nodes(directory)):
            self.__script_editor.model.unregister_project_nodes(node)
            if node.family == "Directory":
                self.__script_editor.model.unregister_project_nodes(node)
                self.__script_editor.model.unregister_directory(node)
            elif node.family == "Project":
                self.__script_editor.remove_project(directory)
            self.__delete_path(directory)

    def get_selected_nodes(self):
        """
        Returns the View selected nodes.

        :return: View selected nodes.
        :rtype: dict
        """

        return self.__view.get_selected_nodes()

    def remove_project(self, node):
        """
        Removes the project associated with given node.

        :param node: Node.
        :type node: ProjectNode or DirectoryNode or FileNode
        :return: Method success.
        :rtype: bool
        """

        if node.family == "Project":
            self.__script_editor.remove_project(node.path)
            return True

        for node in foundations.walkers.nodes_walker(node, ascendants=True):
            if node.family == "Project" and not node is self.__script_editor.model.default_project_node:
                self.__script_editor.remove_project(node.path)
                return True

    def add_new_file(self, node):
        """
        Adds a new file next to given Node associated path.

        :param node: Node.
        :type node: ProjectNode or DirectoryNode or FileNode
        :return: Method success.
        :rtype: bool
        """

        if self.__script_editor.model.is_authoring_node(node):
            return self.__script_editor.new_file()

        file, state = QInputDialog.getText(self, "Add File", "Enter your new file name:")
        if not state:
            return False

        if node.family in ("Project", "Directory"):
            directory = node.path
        elif node.family == "File":
            directory = os.path.dirname(node.path)

        # file = foundations.strings.to_string(file)
        if not file in os.listdir(directory):
            file = os.path.join(directory, file)
            LOGGER.info("{0} | Adding '{1}' file!".format(self.__class__.__name__, file))
            open(file, "w").close()
        else:
            self.__raise_file_system_exception(file, directory)
        return True

    def add_new_directory(self, node):
        """
        Adds a new directory next to given Node associated path.

        :param node: Node.
        :type node: ProjectNode or DirectoryNode or FileNode
        :return: Method success.
        :rtype: bool
        """

        if self.__script_editor.model.is_authoring_node(node):
            return False

        directory, state = QInputDialog.getText(self, "Add Directory", "Enter your new directory name:")
        if not state:
            return False

        if node.family in ("Project", "Directory"):
            parent_directory = node.path
        elif node.family == "File":
            parent_directory = os.path.dirname(node.path)

        directory = foundations.strings.to_string(directory)
        if not directory in os.listdir(parent_directory):
            directory = os.path.join(parent_directory, directory)
            LOGGER.info("{0} | Adding '{1}' directory!".format(self.__class__.__name__, directory))
            os.makedirs(directory)
        else:
            self.__raise_file_system_exception(file, parent_directory)
        return True

    def rename(self, node):
        """
        Renames given Node associated path.

        :param node: Node.
        :type node: ProjectNode or DirectoryNode or FileNode
        :return: Method success.
        :rtype: bool
        """

        source = node.path
        base_name, state = QInputDialog.getText(self, "Rename", "Enter your new name:", text=os.path.basename(source))
        if not state:
            return False

        base_name = foundations.strings.to_string(base_name)
        if base_name == os.path.basename(source):
            return False

        parent_directory = os.path.dirname(source)
        target = os.path.join(parent_directory, base_name)

        if self.__script_editor.model.is_authoring_node(node):
            if not foundations.common.path_exists(source):
                LOGGER.info("{0} | Renaming '{1}' untitled file to '{2}'!".format(
                    self.__class__.__name__, source, target))
                self.__set_authoring_nodes(source, target)
                return True

        if not base_name in os.listdir(parent_directory):
            if node.family == "File":
                LOGGER.info("{0} | Renaming '{1}' file to '{2}'!".format(self.__class__.__name__, source, target))
                self.__rename_file(source, target)
            elif node.family == "Directory":
                LOGGER.info("{0} | Renaming '{1}' directory to '{2}'!".format(self.__class__.__name__, source, target))
                self.__rename_directory(source, target)
            elif node.family == "Project":
                LOGGER.info("{0} | Renaming '{1}' project to '{2}'!".format(self.__class__.__name__, source, target))
                self.__rename_project(source, target)
        else:
            self.__raise_file_system_exception(base_name, parent_directory)

        return True

    def delete(self, node):
        """
        Deletes given Node associated path.

        :param node: Node.
        :type node: ProjectNode or DirectoryNode or FileNode
        :return: Method success.
        :rtype: bool
        """

        path = node.path
        if self.__script_editor.model.is_authoring_node(node):
            if not foundations.common.path_exists(path):
                return False

        if message_box.message_box("Question", "Question",
                                   "Are you sure you want to delete '{0}' {1}?".format(
                                           path, "file" if os.path.isfile(path) else "directory"),
                                   buttons=QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            if os.path.isfile(path):
                LOGGER.info("{0} | Deleting '{1}' file!".format(self.__class__.__name__, path))
                self.__delete_file(path)
            else:
                LOGGER.info("{0} | Deleting '{1}' directory!".format(self.__class__.__name__, path))
                self.__delete_directory(path)
        return True
