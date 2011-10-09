#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**componentsManagerUi.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`ComponentsManagerUi` Component Interface class and the :class:`CollectionsOutliner_QTreeView` class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import manager.exceptions
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "ComponentsManagerUi"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Components_Manager_Ui.ui")

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class ComponentsManagerUi(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`umbra.components.core.componentsManagerUi.componentsManagerUi` Component Interface class.
	| It defines methods to interact with the :class:`manager.componentsManager.Manager` class Application instance Components.
	"""

	# Custom signals definitions.
	modelChanged = pyqtSignal()
	modelRefresh = pyqtSignal()
	modelPartialRefresh = pyqtSignal()

	@core.executionTrace
	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param name: Component name. ( String )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(ComponentsManagerUi, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__uiResources = "resources"
		self.__uiActivatedImage = "Activated.png"
		self.__uiDeactivatedImage = "Deactivated.png"
		self.__uiCategoryAffixe = "_Category.png"
		self.__dockArea = 1

		self.__container = None
		self.__settings = None

		self.__model = None

		self.__modelHeaders = [ "Components", "Activated", "Category", "Rank", "Version" ]
		self.__treeWidgetIndentation = 15
		self.__treeViewInnerMargins = QMargins(0, 0, 0, 12)
		self.__componentsInformationsDefaultText = "<center><h4>* * *</h4>Select Some Components to display related informations!<h4>* * *</h4></center>"
		self.__componentsInformationsText = """
											<h4><center>{0}</center></h4>
											<p>
											<b>Category:</b> {1}
											<br/>
											<b>Author:</b> {2}
											<br/>
											<b>Email:</b> <a href="mailto:{3}"><span style=" text-decoration: underline; color:#e0e0e0;">{3}</span></a>
											<br/>
											<b>Url:</b> <a href="{4}"><span style=" text-decoration: underline; color:#e0e0e0;">{4}</span></a>
											<p>
											<b>Description:</b> {5}
											</p>
											</p>
											"""

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiResources(self):
		"""
		This method is the property for **self.__uiResources** attribute.

		:return: self.__uiResources. ( String )
		"""

		return self.__uiResources

	@uiResources.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self, value):
		"""
		This method is the setter method for **self.__uiResources** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiResources"))

	@uiResources.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResources(self):
		"""
		This method is the deleter method for **self.__uiResources** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiResources"))

	@property
	def uiActivatedImage(self):
		"""
		This method is the property for **self.__uiActivatedImage** attribute.

		:return: self.__uiActivatedImage. ( String )
		"""

		return self.__uiActivatedImage

	@uiActivatedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiActivatedImage(self, value):
		"""
		This method is the setter method for **self.__uiActivatedImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiActivatedImage"))

	@uiActivatedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiActivatedImage(self):
		"""
		This method is the deleter method for **self.__uiActivatedImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiActivatedImage"))

	@property
	def uiDeactivatedImage(self):
		"""
		This method is the property for **self.__uiDeactivatedImage** attribute.

		:return: self.__uiDeactivatedImage. ( String )
		"""

		return self.__uiDeactivatedImage

	@uiDeactivatedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDeactivatedImage(self, value):
		"""
		This method is the setter method for **self.__uiDeactivatedImage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiDeactivatedImage"))

	@uiDeactivatedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDeactivatedImage(self):
		"""
		This method is the deleter method for **self.__uiDeactivatedImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiDeactivatedImage"))

	@property
	def uiCategoryAffixe(self):
		"""
		This method is the property for **self.__uiCategoryAffixe** attribute.

		:return: self.__uiCategoryAffixe. ( String )
		"""

		return self.__uiCategoryAffixe

	@uiCategoryAffixe.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiCategoryAffixe(self, value):
		"""
		This method is the setter method for **self.__uiCategoryAffixe** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiCategoryAffixe"))

	@uiCategoryAffixe.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiCategoryAffixe(self):
		"""
		This method is the deleter method for **self.__uiCategoryAffixe** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiCategoryAffixe"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dockArea"))

	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This method is the deleter method for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settings"))

	@property
	def model(self):
		"""
		This method is the property for **self.__model** attribute.

		:return: self.__model. ( QStandardItemModel )
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This method is the setter method for **self.__model** attribute.

		:param value: Attribute value. ( QStandardItemModel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		This method is the deleter method for **self.__model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("model"))

	@property
	def modelHeaders(self):
		"""
		This method is the property for **self.__modelHeaders** attribute.

		:return: self.__modelHeaders. ( List )
		"""

		return self.__modelHeaders

	@modelHeaders.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelHeaders(self, value):
		"""
		This method is the setter method for **self.__modelHeaders** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("modelHeaders"))

	@modelHeaders.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modelHeaders(self):
		"""
		This method is the deleter method for **self.__modelHeaders** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("modelHeaders"))

	@property
	def treeWidgetIndentation(self):
		"""
		This method is the property for **self.__treeWidgetIndentation** attribute.

		:return: self.__treeWidgetIndentation. ( Integer )
		"""

		return self.__treeWidgetIndentation

	@treeWidgetIndentation.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeWidgetIndentation(self, value):
		"""
		This method is the setter method for **self.__treeWidgetIndentation** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("treeWidgetIndentation"))

	@treeWidgetIndentation.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeWidgetIndentation(self):
		"""
		This method is the deleter method for **self.__treeWidgetIndentation** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("treeWidgetIndentation"))

	@property
	def treeViewInnerMargins(self):
		"""
		This method is the property for **self.__treeViewInnerMargins** attribute.

		:return: self.__treeViewInnerMargins. ( Integer )
		"""

		return self.__treeViewInnerMargins

	@treeViewInnerMargins.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewInnerMargins(self, value):
		"""
		This method is the setter method for **self.__treeViewInnerMargins** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("treeViewInnerMargins"))

	@treeViewInnerMargins.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewInnerMargins(self):
		"""
		This method is the deleter method for **self.__treeViewInnerMargins** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("treeViewInnerMargins"))

	@property
	def componentsInformationsDefaultText(self):
		"""
		This method is the property for **self.__componentsInformationsDefaultText** attribute.

		:return: self.__componentsInformationsDefaultText. ( String )
		"""

		return self.__componentsInformationsDefaultText

	@componentsInformationsDefaultText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsInformationsDefaultText(self, value):
		"""
		This method is the setter method for **self.__componentsInformationsDefaultText** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("componentsInformationsDefaultText"))

	@componentsInformationsDefaultText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsInformationsDefaultText(self):
		"""
		This method is the deleter method for **self.__componentsInformationsDefaultText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("componentsInformationsDefaultText"))

	@property
	def componentsInformationsText(self):
		"""
		This method is the property for **self.__componentsInformationsText** attribute.

		:return: self.__componentsInformationsText. ( String )
		"""

		return self.__componentsInformationsText

	@componentsInformationsText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsInformationsText(self, value):
		"""
		This method is the setter method for **self.__componentsInformationsText** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("componentsInformationsText"))

	@componentsInformationsText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsInformationsText(self):
		"""
		This method is the deleter method for **self.__componentsInformationsText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("componentsInformationsText"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		:param container: Container to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__uiResources = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiResources)
		self.__container = container

		self.__settings = self.__container.settings

		self.activated = True
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component cannot be deactivated!".format(self.__name))

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__model = QStandardItemModel()

		self.__Components_Manager_Ui_treeView_setModel()

		self.Components_Manager_Ui_gridLayout.setContentsMargins(self.__treeViewInnerMargins)

		self.Components_Manager_Ui_treeView.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__Components_Manager_Ui_treeView_addActions()

		self.__Components_Manager_Ui_treeView_setView()

		self.Components_Informations_textBrowser.setText(self.__componentsInformationsDefaultText)

		self.Components_Manager_Ui_splitter.setSizes([ 16777215, 1 ])

		# Signals / Slots.
		self.Components_Manager_Ui_treeView.selectionModel().selectionChanged.connect(self.__Components_Manager_Ui_treeView_selectionModel__selectionChanged)
		self.modelChanged.connect(self.__Components_Manager_Ui_treeView_refreshView)
		self.modelRefresh.connect(self.__Components_Manager_Ui_treeView_refreshModel)
		self.modelPartialRefresh.connect(self.__Components_Manager_Ui_treeView_setActivationsStatus)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component ui cannot be uninitialized!".format(self.name))

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Widget cannot be removed!".format(self.name))

	@core.executionTrace
	def onStartup(self):
		"""
		This method is called on Framework startup.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		self.__Components_Manager_Ui_treeView_setActivationsStatus()
		return True

	@core.executionTrace
	def __Components_Manager_Ui_treeView_setModel(self):
		"""
		This method sets the **Components_Manager_Ui_treeView** Model.

		Columns:
		Collections | Activated | Category | Rank | Version

		Rows:
		* Path: { _type: "Path" }
		** Component: { _type: "Component", _datas: profile }
		"""

		LOGGER.debug("> Setting up '{0}' Model!".format("Components_Manager_Ui_treeView"))

		self.__model.clear()

		self.__model.setHorizontalHeaderLabels(self.__modelHeaders)
		self.__model.setColumnCount(len(self.__modelHeaders))

		for path in self.__container.componentsManager.paths:
			components = {name : component for name, component in self.__container.componentsManager.components.items() if os.path.normpath(path) in os.path.normpath(component.path)}
			if not components:
				break

			pathStandardItem = QStandardItem(QString(os.path.basename(path).title()))
			pathStandardItem._type = "Path"

			LOGGER.debug("> Adding '{0}' path to '{1}' Model.".format(path, "Components_Manager_Ui_treeView"))
			self.__model.appendRow(pathStandardItem)

			for name, component in components.items():
				if not component.interface:
					continue

				componentStandardItem = QStandardItem(QString(component.title))
				iconPath = os.path.join(self.__uiResources, "{0}{1}".format(component.category, self.__uiCategoryAffixe))
				componentStandardItem.setIcon(QIcon(iconPath))

				componentActivationStandardItem = QStandardItem(QString(str(component.interface.activated)))
				iconPath = component.interface.activated and os.path.join(self.__uiResources, self.__uiActivatedImage) or os.path.join(self.__uiResources, self.__uiDeactivatedImage)
				componentActivationStandardItem.setIcon(QIcon(iconPath))

				componentCategoryStandardItem = QStandardItem(QString(component.category and component.category or ""))
				componentCategoryStandardItem.setTextAlignment(Qt.AlignCenter)

				componentRankStandardItem = QStandardItem(QString(component.rank or ""))
				componentRankStandardItem.setTextAlignment(Qt.AlignCenter)

				componentVersionStandardItem = QStandardItem(QString(component.version or ""))
				componentVersionStandardItem.setTextAlignment(Qt.AlignCenter)

				componentStandardItem._datas = component
				componentStandardItem._type = "Component"

				LOGGER.debug("> Adding '{0}' Component to '{1}'.".format(name, "Components_Manager_Ui_treeView"))
				pathStandardItem.appendRow([componentStandardItem, componentActivationStandardItem, componentCategoryStandardItem, componentRankStandardItem, componentVersionStandardItem])

		self.modelChanged.emit()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_refreshModel(self):
		"""
		This method refreshes the **Components_Manager_Ui_treeView** Model.
		"""

		LOGGER.debug("> Refreshing '{0}' Model!".format("Components_Manager_Ui_treeView"))

		self.__Components_Manager_Ui_treeView_setModel()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_setView(self):
		"""
		This method sets the **Components_Manager_Ui_treeView** View.
		"""

		LOGGER.debug("> Refreshing '{0}' ui!".format(self.__class__.__name__))

		self.Components_Manager_Ui_treeView.setAutoScroll(False)
		self.Components_Manager_Ui_treeView.setDragDropMode(QAbstractItemView.NoDragDrop)
		self.Components_Manager_Ui_treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.Components_Manager_Ui_treeView.setIndentation(self.__treeWidgetIndentation)
		self.Components_Manager_Ui_treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.Components_Manager_Ui_treeView.setSortingEnabled(True)

		self.Components_Manager_Ui_treeView.setModel(self.__model)

		self.__Components_Manager_Ui_treeView_setDefaultViewState()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_setDefaultViewState(self):
		"""
		This method sets **Components_Manager_Ui_treeView** Widget default View state.
		"""

		LOGGER.debug("> Setting '{0}' default View state!".format("Components_Manager_Ui_treeView"))

		self.Components_Manager_Ui_treeView.expandAll()
		for column in range(len(self.__modelHeaders)):
			self.Components_Manager_Ui_treeView.resizeColumnToContents(column)

		self.Components_Manager_Ui_treeView.sortByColumn(0, Qt.AscendingOrder)

	@core.executionTrace
	def __Components_Manager_Ui_treeView_setActivationsStatus(self):
		"""
		This method sets the **Components_Manager_Ui_treeView** activations status.
		"""

		for i in range(self.__model.rowCount()):
			for j in range(self.__model.item(i).rowCount()):
				componentStandardItem = self.__model.item(i).child(j, 0)
				componentActivationStandardItem = self.__model.item(i).child(j, 1)
				componentActivationStandardItem.setText(str(componentStandardItem._datas.interface.activated))
				iconPath = componentStandardItem._datas.interface.activated and os.path.join(self.__uiResources, self.__uiActivatedImage) or os.path.join(self.__uiResources, self.__uiDeactivatedImage)
				componentActivationStandardItem.setIcon(QIcon(iconPath))

	@core.executionTrace
	def __Components_Manager_Ui_treeView_refreshView(self):
		"""
		This method refreshes the **Components_Manager_Ui_treeView** View.
		"""

		self.__Components_Manager_Ui_treeView_setDefaultViewState()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_addActions(self):
		"""
		This method sets the **Components_Manager_Ui_treeView** actions.
		"""

		self.Components_Manager_Ui_treeView.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.ComponentsManagerUi|Activate Component(s)", slot=self.__Components_Manager_Ui_treeView_activateComponentsAction__triggered))
		self.Components_Manager_Ui_treeView.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.ComponentsManagerUi|Deactivate Component(s)", slot=self.__Components_Manager_Ui_treeView_deactivateComponentsAction__triggered))

		separatorAction = QAction(self.Components_Manager_Ui_treeView)
		separatorAction.setSeparator(True)
		self.Components_Manager_Ui_treeView.addAction(separatorAction)

		self.Components_Manager_Ui_treeView.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.ComponentsManagerUi|Reload Component(s)", slot=self.__Components_Manager_Ui_treeView_reloadComponentsAction__triggered))

		separatorAction = QAction(self.Components_Manager_Ui_treeView)
		separatorAction.setSeparator(True)
		self.Components_Manager_Ui_treeView.addAction(separatorAction)

	@core.executionTrace
	def __Components_Manager_Ui_treeView_activateComponentsAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.ComponentsManagerUi|Activate Component(s)'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.activateComponents_ui()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_deactivateComponentsAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.ComponentsManagerUi|Deactivate Component(s)'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.deactivateComponents_ui()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_reloadComponentsAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.ComponentsManagerUi|Reload Component(s)'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.reloadComponents_ui()

	@core.executionTrace
	def __Components_Manager_Ui_treeView_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method sets the **Additional_Informations_textEdit** Widget.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""

		LOGGER.debug("> Initializing '{0}' Widget.".format("Additional_Informations_textEdit"))

		selectedComponents = self.getSelectedComponents()
		content = []
		if selectedComponents:
			for item in selectedComponents:
				content.append(self.__componentsInformationsText.format(item.name,
																		item.category,
																		item.author,
																		item.email,
																		item.url,
																		item.description))
		else:
			content.append(self.__componentsInformationsDefaultText)

		separator = len(content) == 1 and "" or "<p><center>* * *<center/></p>"
		self.Components_Informations_textBrowser.setText(separator.join(content))

	@core.executionTrace
	def __storeDeactivatedComponents(self):
		"""
		This method stores deactivated Components in settings file.
		"""

		deactivatedComponents = []
		for component in self.__model.findItems(".*", Qt.MatchRegExp | Qt.MatchRecursive, 0):
			if component._type == "Component":
				component._datas.interface.activated or deactivatedComponents.append(component._datas.name)

		LOGGER.debug("> Storing '{0}' deactivated Components.".format(", ".join(deactivatedComponents)))
		self.__settings.setKey("Settings", "deactivatedComponents", ",".join(deactivatedComponents))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, manager.exceptions.ComponentActivationError)
	def activateComponents_ui(self):
		"""
		This method activates user selected Components.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		activationFailedComponents = []
		for component in self.getSelectedComponents():
			if not component.interface.activated:
				success = self.activateComponent(component.name) or False
				if not success:
					activationFailedComponents.append(component)
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Component is already activated!".format(self.__class__.__name__, component.name))
		self.__storeDeactivatedComponents()
		if not activationFailedComponents:
			return True
		else:
			raise manager.exceptions.ComponentActivationError("{0} | Exception(s) raised while activating '{1}' Component(s)!".format(self.__class__.__name__, ", ". join(activationFailedComponents)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, manager.exceptions.ComponentDeactivationError)
	def deactivateComponents_ui(self):
		"""
		This method deactivates user selected Components.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		deactivationFailedComponents = []
		for component in self.getSelectedComponents():
			if component.interface.activated:
				if component.interface.deactivatable:
					success = self.deactivateComponent(component.name) or False
					if not success:
						deactivationFailedComponents.append(component)
				else:
					messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, component.name))
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Component is already deactivated!".format(self.__class__.__name__, component.name))
		self.__storeDeactivatedComponents()
		if not deactivationFailedComponents:
			return True
		else:
			raise manager.exceptions.ComponentDeactivationError("{0} | Exception(s) raised while deactivating '{1}' Component(s)!".format(self.__class__.__name__, ", ". join(deactivationFailedComponents)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, manager.exceptions.ComponentReloadError)
	def reloadComponents_ui(self):
		"""
		This method reloads user selected Components.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		reloadFailedComponents = []
		for component in self.getSelectedComponents():
			if component.interface.deactivatable:
				success = self.reloadComponent(component.name) or False
				if not success:
					reloadFailedComponents.append(component)
			else:
				messageBox.messageBox("Warning", "Warning", "{0} | '{1}' Component cannot be deactivated and won't be reloaded!".format(self.__class__.__name__, component.name))
		if not reloadFailedComponents:
			return True
		else:
			raise manager.exceptions.ComponentReloadError("{0} | Exception(s) raised while reloading '{1}' Component(s)!".format(self.__class__.__name__, ", ". join(reloadFailedComponents)))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, manager.exceptions.ComponentExistsError, Exception)
	def activateComponent(self, name):
		"""
		This method activates provided Component.

		:param name: Component name. ( String )
		:return: Method success. ( Boolean )
		"""

		if not name in self.__container.componentsManager.components.keys():
			raise manager.exceptions.ComponentExistsError("'{0}' Component isn't registered in the Components Manager!".format(name))

		component = self.__container.componentsManager.components[name]
		LOGGER.debug("> Attempting '{0}' Component activation.".format(component.name))
		component.interface.activate(self.__container)
		if component.category in ("Default", "QObject"):
			component.interface.initialize()
		elif component.category == "QWidget":
			component.interface.addWidget()
			component.interface.initializeUi()
		LOGGER.info("{0} | '{1}' Component has been activated!".format(self.__class__.__name__, component.name))
		self.modelPartialRefresh.emit()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, manager.exceptions.ComponentExistsError, manager.exceptions.ComponentDeactivationError)
	def deactivateComponent(self, name):
		"""
		This method deactivates provided Component.

		:param name: Component name. ( String )
		:return: Method success. ( Boolean )
		"""

		if not name in self.__container.componentsManager.components.keys():
			raise manager.exceptions.ComponentExistsError("'{0}' Component isn't registered in the Components Manager!".format(name))

		component = self.__container.componentsManager.components[name]

		LOGGER.debug("> Attempting '{0}' Component deactivation.".format(component.name))
		if component.interface.deactivatable:
			if component.category in ("Default", "QObject"):
				component.interface.uninitialize()
			elif component.category == "QWidget":
				component.interface.uninitializeUi()
				component.interface.removeWidget()
			component.interface.deactivate()
			LOGGER.info("{0} | '{1}' Component has been deactivated!".format(self.__class__.__name__, component.name))
			self.modelPartialRefresh.emit()
			return True
		else:
			raise manager.exceptions.ComponentDeactivationError("{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, component.name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, manager.exceptions.ComponentExistsError, manager.exceptions.ComponentReloadError)
	def reloadComponent(self, name):
		"""
		This method reloads provided Component.

		:param name: Component name. ( String )
		:return: Method success. ( Boolean )
		"""

		if not name in self.__container.componentsManager.components.keys():
			raise manager.exceptions.ComponentExistsError("'{0}' Component isn't registered in the Components Manager!".format(name))

		component = self.__container.componentsManager.components[name]

		LOGGER.debug("> Attempting '{0}' Component reload.".format(component.name))
		if component.interface.deactivatable:
			if component.interface.activated:
				self.deactivateComponent(name)
			self.__container.componentsManager.reloadComponent(component.name)
			if not component.interface.activated:
				self.activateComponent(name)
			LOGGER.info("{0} | '{1}' Component has been reloaded!".format(self.__class__.__name__, component.name))
			self.modelPartialRefresh.emit()
			return True
		else:
			raise manager.exceptions.ComponentReloadError("{0} | '{1}' Component cannot be deactivated and won't be reloaded!".format(self.__class__.__name__, component.name))

	@core.executionTrace
	def getSelectedItems(self, rowsRootOnly=True):
		"""
		This method returns the **Components_Manager_Ui_treeView** selected items.

		:param rowsRootOnly: Return rows roots only. ( Boolean )
		:return: View selected items. ( List )
		"""

		selectedIndexes = self.Components_Manager_Ui_treeView.selectedIndexes()
		return rowsRootOnly and [item for item in set((self.__model.itemFromIndex(self.__model.sibling(index.row(), 0, index)) for index in selectedIndexes))] or [self.__model.itemFromIndex(index) for index in selectedIndexes]

	@core.executionTrace
	def getSelectedComponents(self):
		"""
		This method returns selected Components.

		:return: View selected Components. ( List )
		"""

		selectedComponents = [item._datas for item in self.getSelectedItems() if item._type == "Component"]
		return selectedComponents and selectedComponents or []
