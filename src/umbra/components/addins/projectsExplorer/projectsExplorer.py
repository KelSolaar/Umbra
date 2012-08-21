#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**projectsExplorer.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`ProjectsExplorer` Component Interface class and others helper objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAction

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.constants import Constants
from umbra.components.addins.projectsExplorer.models import ProjectsProxyModel
from umbra.components.addins.projectsExplorer.views import Projects_QTreeView
from umbra.ui.delegates import RichText_QStyledItemDelegate
from umbra.ui.delegates import Style

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "ProjectsExplorer"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Projects_Explorer.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ProjectsExplorer(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	This class is the :mod:`sibl_gui.components.addons.projectsExplorer.projectsExplorer` Component Interface class.
	"""

	@core.executionTrace
	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param name: Component name. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(ProjectsExplorer, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__dockArea = 1

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__factoryScriptEditor = None

		self.__model = None
		self.__view = None
		self.__delegate = None
		self.__style = Style(default=\
								"""
								QLabel, QLabel link {
									background-color: rgb(40, 40, 40);
									color: rgb(192, 192, 192);
								}
								""",
								hover=\
								"""
								QLabel, QLabel link {
									background-color: rgb(80, 80, 80);
									color: rgb(192, 192, 192);
								}
								""",
								highlight=\
								"""
								QLabel, QLabel link {
									background-color: rgb(128, 128, 128);
									color: rgb(224, 224, 224);
								}
								""")

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def dockArea(self):
		"""
		This method is the property for **self.__dockArea** attribute.

		:return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This method is the setter method for **self.__dockArea** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

	@property
	def engine(self):
		"""
		This method is the property for **self.__engine** attribute.

		:return: self.__engine. ( QObject )
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		This method is the setter method for **self.__engine** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		This method is the deleter method for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

	@property
	def settings(self):
		"""
		This method is the property for **self.__settings** attribute.

		:return: self.__settings. ( QSettings )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This method is the setter method for **self.__settings** attribute.

		:param value: Attribute value. ( QSettings )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This method is the deleter method for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def settingsSection(self):
		"""
		This method is the property for **self.__settingsSection** attribute.

		:return: self.__settingsSection. ( String )
		"""

		return self.__settingsSection

	@settingsSection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		This method is the setter method for **self.__settingsSection** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This method is the deleter method for **self.__settingsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settingsSection"))

	@property
	def factoryScriptEditor(self):
		"""
		This method is the property for **self.__factoryScriptEditor** attribute.

		:return: self.__factoryScriptEditor. ( QWidget )
		"""

		return self.__factoryScriptEditor

	@factoryScriptEditor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryScriptEditor(self, value):
		"""
		This method is the setter method for **self.__factoryScriptEditor** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factoryScriptEditor"))

	@factoryScriptEditor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryScriptEditor(self):
		"""
		This method is the deleter method for **self.__factoryScriptEditor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factoryScriptEditor"))

	@property
	def model(self):
		"""
		This method is the property for **self.__model** attribute.

		:return: self.__model. ( CollectionsModel )
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This method is the setter method for **self.__model** attribute.

		:param value: Attribute value. ( CollectionsModel )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		This method is the deleter method for **self.__model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

	@property
	def view(self):
		"""
		This method is the property for **self.__view** attribute.

		:return: self.__view. ( QWidget )
		"""

		return self.__view

	@view.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def view(self, value):
		"""
		This method is the setter method for **self.__view** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

	@view.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def view(self):
		"""
		This method is the deleter method for **self.__view** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def delegate(self):
		"""
		This method is the property for **self.__delegate** attribute.

		:return: self.__delegate. ( QItemDelegate )
		"""

		return self.__delegate

	@delegate.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def delegate(self, value):
		"""
		This method is the setter method for **self.__delegate** attribute.

		:param value: Attribute value. ( QItemDelegate )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "delegate"))

	@delegate.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def delegate(self):
		"""
		This method is the deleter method for **self.__delegate** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "delegate"))

	@property
	def style(self):
		"""
		This method is the property for **self.__style** attribute.

		:return: self.__style. ( Style )
		"""

		return self.__style

	@style.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def style(self, value):
		"""
		This method is the setter method for **self.__style** attribute.

		:param value: Attribute value. ( Style )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "style"))

	@style.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def style(self):
		"""
		This method is the deleter method for **self.__style** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "style"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def activate(self, engine):
		"""
		This method activates the Component.

		:param engine: Engine to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = engine
		self.__settings = self.__engine.settings
		self.__settingsSection = self.name

		self.__factoryScriptEditor = self.__engine.componentsManager["factory.scriptEditor"]

		self.activated = True
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Deactivating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__factoryScriptEditor = None

		self.activated = False
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))
		self.__model = ProjectsProxyModel(self)
		self.__model.setSourceModel(self.__factoryScriptEditor.model)
		projectNode = self.__factoryScriptEditor.model.defaultProjectNode
		projectNode.roles.update({Qt.DisplayRole : "<b>Open Files</b>",
										Qt.EditRole : projectNode.name})
		self.__delegate = RichText_QStyledItemDelegate(self, self.__style)

		self.Projects_Explorer_treeView.setParent(None)
		self.Projects_Explorer_treeView = Projects_QTreeView(self, self.__model)
		self.Projects_Explorer_treeView.setItemDelegate(self.__delegate)
		self.Projects_Explorer_treeView.setObjectName("Projects_Explorer_treeView")
		self.Projects_Explorer_treeView.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.Projects_Explorer_dockWidgetContents_gridLayout.addWidget(self.Projects_Explorer_treeView, 0, 0)
		self.__view = self.Projects_Explorer_treeView
		self.__view_addActions()

		# Signals / Slots.
		self.__view.expanded.connect(self.__view__expanded)
		self.__view.doubleClicked.connect(self.__view__doubleClicked)
		self.__view.selectionModel().selectionChanged.connect(self.__view_selectionModel__selectionChanged)
		self.__factoryScriptEditor.Script_Editor_tabWidget.currentChanged.connect(
		self.__factoryScriptEditor_Script_Editor_tabWidget__currentChanged)
		self.__factoryScriptEditor.model.fileRegistered.connect(self.__factoryScriptEditor_model__fileRegistered)
		self.__factoryScriptEditor.model.editorRegistered.connect(self.__factoryScriptEditor_model__editorRegistered)
		self.__factoryScriptEditor.model.projectRegistered.connect(self.__factoryScriptEditor_model_projectRegistered)

		self.initializedUi = True
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.__view.expanded.disconnect(self.__view__expanded)
		self.__view.doubleClicked.disconnect(self.__view__doubleClicked)
		self.__view.selectionModel().selectionChanged.disconnect(self.__view_selectionModel__selectionChanged)
		self.__factoryScriptEditor.Script_Editor_tabWidget.currentChanged.disconnect(
		self.__factoryScriptEditor_Script_Editor_tabWidget__currentChanged)
		self.__factoryScriptEditor.model.fileRegistered.disconnect(self.__factoryScriptEditor_model__fileRegistered)
		self.__factoryScriptEditor.model.editorRegistered.disconnect(self.__factoryScriptEditor_model__editorRegistered)
		self.__factoryScriptEditor.model.projectRegistered.disconnect(self.__factoryScriptEditor_model_projectRegistered)

		self.__view_removeActions()

		self.__model = None
		self.__delegate = None
		self.__view = None

		self.initializedUi = False
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.removeDockWidget(self)
		self.setParent(None)

		return True

	@core.executionTrace
	def __view_addActions(self):
		"""
		This method sets the View actions.
		"""

		self.__view.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|addins.projectsExplorer|Add Project ...",
		slot=self.__view_addProjectAction__triggered))
		self.__view.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|addins.projectsExplorer|Remove Project",
		slot=self.__view_removeProjectAction__triggered))

		separatorAction = QAction(self.__view)
		separatorAction.setSeparator(True)
		self.__view.addAction(separatorAction)

		self.__view.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|addins.projectsExplorer|Add New File ...",
		slot=self.__view_addNewFileAction__triggered))
		self.__view.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|addins.projectsExplorer|Add New Directory ...",
		slot=self.__view_addNewDirectoryAction__triggered))

		separatorAction = QAction(self.__view)
		separatorAction.setSeparator(True)
		self.__view.addAction(separatorAction)

		self.__view.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|addins.projectsExplorer|Rename ...",
		slot=self.__view_renameAction__triggered))
		self.__view.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|addins.projectsExplorer|Copy ...",
		slot=self.__view_copyAction__triggered))
		self.__view.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|addins.projectsExplorer|Move ...",
		slot=self.__view_moveAction__triggered))

		separatorAction = QAction(self.__view)
		separatorAction.setSeparator(True)
		self.__view.addAction(separatorAction)

		self.__view.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|addins.projectsExplorer|Delete ...",
		slot=self.__view_deleteAction__triggered))

		separatorAction = QAction(self.__view)
		separatorAction.setSeparator(True)
		self.__view.addAction(separatorAction)

		self.__view.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|addins.projectsExplorer|Output Selected Path",
		slot=self.__view_outputSelectedPathAction__triggered))

	@core.executionTrace
	def __view_removeActions(self):
		"""
		This method removes the View actions.
		"""

		addProjectAction = "Actions|Umbra|Components|addins.projectsExplorer|Add Project ..."
		removeProjectAction = "Actions|Umbra|Components|addins.projectsExplorer|Remove Project"
		addNewFileAction = "Actions|Umbra|Components|addins.projectsExplorer|Add New File ..."
		addNewDirectoryAction = "Actions|Umbra|Components|addins.projectsExplorer|Add New Directory ..."
		renameAction = "Actions|Umbra|Components|addins.projectsExplorer|Rename ..."
		copyAction = "Actions|Umbra|Components|addins.projectsExplorer|Copy ..."
		moveAction = "Actions|Umbra|Components|addins.projectsExplorer|Move ..."
		deleteAction = "Actions|Umbra|Components|addins.projectsExplorer|Delete ..."
		outputSelectedPathAction = "Actions|Umbra|Components|addins.projectsExplorer|Output Selected Path"

		for action in (addProjectAction,
						removeProjectAction,
						addNewFileAction,
						addNewDirectoryAction,
						renameAction,
						copyAction,
						moveAction,
						deleteAction,
						outputSelectedPathAction):
			self.__view.removeAction(self.__engine.actionsManager.getAction(action))
			self.__engine.actionsManager.unregisterAction(action)

	@core.executionTrace
	def __view__expanded(self, index):
		"""
		This method is triggered when a View item is expanded.

		:param index: Expdanded item. ( QModelIndex )
		"""

		node = self.__model.getNode(index)
		if node.family != "DirectoryNode":
			return

		self.__factoryScriptEditor._ScriptEditor__setProjectNodes(node)

	@core.executionTrace
	def __view__doubleClicked(self, index):
		"""
		This method is triggered when a View Widget is double clicked.

		:param index: Clicked item index. ( QModelIndex )
		"""

		node = self.__model.getNode(index)
		if not node.family == "FileNode":
			return

		self.__factoryScriptEditor.loadFile(node.path)

	@core.executionTrace
	def __view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method is triggered when the View **selectionModel** has changed.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""

		for node in self.__view.getSelectedNodes():
			if node.family == "FileNode":
				self.__factoryScriptEditor.setCurrentEditor(node.path)

	@core.executionTrace
	def __factoryScriptEditor_Script_Editor_tabWidget__currentChanged(self, index):
		"""
		This method is triggered by the :class:`umbra.languages.factory.scriptEditor.scriptEditor.ScriptEditor`
		Component Interface class when the current tab is changed.

		:param index: Tab index. ( Integer )
		"""

		editor = self.__factoryScriptEditor.getCurrentEditor()
		if not editor:
			return

		editorNode = foundations.common.getFirstItem(self.__factoryScriptEditor.model.getEditorNodes(editor))
		if not editorNode:
			return

		indexes = [self.__model.mapFromSource(self.__model.sourceModel().getNodeIndex(editorNode.parent))]
		self.__view.clearSelection()
		self.__view.selectIndexes(indexes)

	@core.executionTrace
	def __factoryScriptEditor_model__fileRegistered(self, fileNode):
		"""
		This method is triggered by the:class:`umbra.components.factory.scriptEditor.scriptEditor` class
		Model when a file is registered.
		
		:param fileNode: Registered file FileNode. ( FileNode )
		"""

		fileNode.roles.update({Qt.DisplayRole : "<span>{0}</span>".format(fileNode.name),
								Qt.EditRole : fileNode.name})

	@core.executionTrace
	def __factoryScriptEditor_model__editorRegistered(self, editorNode):
		"""
		This method is triggered by the:class:`umbra.components.factory.scriptEditor.scriptEditor` class
		Model when an editor is registered
		
		:param editorNode: Registered editor EditorNode. ( EditorNode )
		"""

		editorNode.roles.update({Qt.DisplayRole : editorNode.name,
								Qt.EditRole : editorNode.name})

	@core.executionTrace
	def __factoryScriptEditor_model_projectRegistered(self, projectNode):
		"""
		This method is triggered by the:class:`umbra.components.factory.scriptEditor.scriptEditor` class
		Model when a project is registered
		
		:param projectNode: Registered project ProjectNode. ( ProjectNode )
		"""

		projectNode.roles.update({Qt.DisplayRole : "<b>{0}</b>".format(projectNode.name),
										Qt.EditRole : projectNode.name})

		index = self.__model.mapFromSource(self.__factoryScriptEditor.model.getNodeIndex(projectNode))
		self.__view.setExpanded(index, True)

	@core.executionTrace
	def __view_addProjectAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|addins.projectsExplorer|Add Project ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.__factoryScriptEditor.addProjectUi()

	@core.executionTrace
	def __view_removeProjectAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|addins.projectsExplorer|Remove Project'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		node = foundations.common.getFirstItem(self.__view.getSelectedNodes().iterkeys())
		if not node:
			return

		if node.family == "ProjectNode":
			self.__factoryScriptEditor.removeProject(node.path)
			return

		for node in foundations.walkers.nodesWalker(node, ascendants=True):
			if node.family == "ProjectNode" and not node is self.__factoryScriptEditor.model.defaultProjectNode:
				self.__factoryScriptEditor.removeProject(node.path)
				return True

	@core.executionTrace
	def __view_addNewFileAction__triggered(self, checked):
		"""
		This method is triggered by **'"Actions|Umbra|Components|addins.projectsExplorer|Add New File ..."'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		print "Actions|Umbra|Components|addins.projectsExplorer|Add New File ..."

	@core.executionTrace
	def __view_addNewDirectoryAction__triggered(self, checked):
		"""
		This method is triggered by **'"Actions|Umbra|Components|addins.projectsExplorer|Add New Directory ..."'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		print "Actions|Umbra|Components|addins.projectsExplorer|Add New Directory ..."

	@core.executionTrace
	def __view_renameAction__triggered(self, checked):
		"""
		This method is triggered by **'"Actions|Umbra|Components|addins.projectsExplorer|Rename ..."'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		print "Actions|Umbra|Components|addins.projectsExplorer|Rename ..."

	@core.executionTrace
	def __view_copyAction__triggered(self, checked):
		"""
		This method is triggered by **'"Actions|Umbra|Components|addins.projectsExplorer|Copy ..."'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		print "Actions|Umbra|Components|addins.projectsExplorer|Copy ..."

	@core.executionTrace
	def __view_moveAction__triggered(self, checked):
		"""
		This method is triggered by **'"Actions|Umbra|Components|addins.projectsExplorer|Move ..."'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		print "Actions|Umbra|Components|addins.projectsExplorer|Move ..."

	@core.executionTrace
	def __view_deleteAction__triggered(self, checked):
		"""
		This method is triggered by **'"Actions|Umbra|Components|addins.projectsExplorer|Delete ..."'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		print "Actions|Umbra|Components|addins.projectsExplorer|Delete ..."

	@core.executionTrace
	def __view_outputSelectedPathAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|addins.projectsExplorer|Output Selected Path'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		node = foundations.common.getFirstItem(self.__view.getSelectedNodes().iterkeys())
		if not node:
			return

		LOGGER.info("{0} | '{1}'.".format(self.__class__.__name__, node.path))
		return True
