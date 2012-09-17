#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**componentsManagerUi.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`ComponentsManagerUi` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
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

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.walkers
import foundations.strings as strings
import manager.exceptions
import umbra.engine
import umbra.ui.common
import umbra.ui.nodes
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.constants import Constants
from umbra.components.factory.componentsManagerUi.models import ComponentsModel
from umbra.components.factory.componentsManagerUi.nodes import ComponentNode
from umbra.components.factory.componentsManagerUi.nodes import PathNode
from umbra.components.factory.componentsManagerUi.views import Components_QTreeView

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "ComponentsManagerUi"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Components_Manager_Ui.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ComponentsManagerUi(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`umbra.components.factory.componentsManagerUi.componentsManagerUi` Component Interface class.
	| It defines methods to interact with
		the :class:`manager.componentsManager.Manager` class Application instance Components.
	"""

	# Custom signals definitions.
	modelRefresh = pyqtSignal()
	"""
	This signal is emited by the :class:`ComponentsManagerUi` class when :obj:`ComponentsManagerUi.model` class property
	model needs to be refreshed. ( pyqtSignal )
	"""

	activatedComponent = pyqtSignal(str)
	"""
	This signal is emited by the :class:`ComponentsManagerUi` class when a Component is activated. ( pyqtSignal )

	:return: Activated Component name. ( String )	
	"""

	deactivatedComponent = pyqtSignal(str)
	"""
	This signal is emited by the :class:`ComponentsManagerUi` class when a Component is deactivated. ( pyqtSignal )

	:return: Deactivated Component name. ( String )	
	"""

	reloadedComponent = pyqtSignal(str)
	"""
	This signal is emited by the :class:`ComponentsManagerUi` class when a Component is reloaded. ( pyqtSignal )

	:return: Reloaded Component name. ( String )	
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

		super(ComponentsManagerUi, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__uiResourcesDirectory = "resources"
		self.__uiActivatedImage = "Activated.png"
		self.__uiDeactivatedImage = "Deactivated.png"
		self.__uiCategoryAffixe = "_Category.png"
		self.__dockArea = 1

		self.__engine = None
		self.__settings = None

		self.__model = None
		self.__view = None

		self.__headers = OrderedDict([("Components", "name"),
										("Activated", "activated"),
										("Category", "category"),
										("Rank", "rank"),
										("Version", "version")])

		self.__treeViewInnerMargins = QMargins(0, 0, 0, 12)
		self.__componentsInformationsDefaultText = \
		"<center><h4>* * *</h4>Select Some Components to display related informations!<h4>* * *</h4></center>"
		self.__componentsInformationsText = """
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

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def uiResourcesDirectory(self):
		"""
		This method is the property for **self.__uiResourcesDirectory** attribute.

		:return: self.__uiResourcesDirectory. ( String )
		"""

		return self.__uiResourcesDirectory

	@uiResourcesDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self, value):
		"""
		This method is the setter method for **self.__uiResourcesDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiResourcesDirectory"))

	@uiResourcesDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiResourcesDirectory(self):
		"""
		This method is the deleter method for **self.__uiResourcesDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiResourcesDirectory"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiActivatedImage"))

	@uiActivatedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiActivatedImage(self):
		"""
		This method is the deleter method for **self.__uiActivatedImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiActivatedImage"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiDeactivatedImage"))

	@uiDeactivatedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiDeactivatedImage(self):
		"""
		This method is the deleter method for **self.__uiDeactivatedImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiDeactivatedImage"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "uiCategoryAffixe"))

	@uiCategoryAffixe.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiCategoryAffixe(self):
		"""
		This method is the deleter method for **self.__uiCategoryAffixe** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiCategoryAffixe"))

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
	def model(self):
		"""
		This method is the property for **self.__model** attribute.

		:return: self.__model. ( ComponentsModel )
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This method is the setter method for **self.__model** attribute.

		:param value: Attribute value. ( ComponentsModel )
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
	def headers(self):
		"""
		This method is the property for **self.__headers** attribute.

		:return: self.__headers. ( List )
		"""

		return self.__headers

	@headers.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def headers(self, value):
		"""
		This method is the setter method for **self.__headers** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "headers"))

	@headers.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def headers(self):
		"""
		This method is the deleter method for **self.__headers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "headers"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "treeViewInnerMargins"))

	@treeViewInnerMargins.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def treeViewInnerMargins(self):
		"""
		This method is the deleter method for **self.__treeViewInnerMargins** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "treeViewInnerMargins"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "componentsInformationsDefaultText"))

	@componentsInformationsDefaultText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsInformationsDefaultText(self):
		"""
		This method is the deleter method for **self.__componentsInformationsDefaultText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "componentsInformationsDefaultText"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "componentsInformationsText"))

	@componentsInformationsText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def componentsInformationsText(self):
		"""
		This method is the deleter method for **self.__componentsInformationsText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "componentsInformationsText"))

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

		self.__uiResourcesDirectory = os.path.join(os.path.dirname(core.getModule(self).__file__),
													self.__uiResourcesDirectory)
		self.__engine = engine

		self.__settings = self.__engine.settings

		self.activated = True
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This method deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def initializeUi(self):
		"""
		This method initializes the Component ui.
		
		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__model = ComponentsModel(self, horizontalHeaders=self.__headers)
		self.setComponents()

		self.Components_Manager_Ui_treeView.setParent(None)
		self.Components_Manager_Ui_treeView = Components_QTreeView(self, self.__model)
		self.Components_Manager_Ui_treeView.setObjectName("Components_Manager_Ui_treeView")
		self.Components_Manager_Ui_gridLayout.setContentsMargins(self.__treeViewInnerMargins)
		self.Components_Manager_Ui_gridLayout.addWidget(self.Components_Manager_Ui_treeView, 0, 0)
		self.__view = self.Components_Manager_Ui_treeView
		self.__view.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__view_addActions()

		self.Components_Informations_textBrowser.setText(self.__componentsInformationsDefaultText)

		self.Components_Manager_Ui_splitter.setSizes([ 16777215, 1 ])

		# Signals / Slots.
		self.__view.selectionModel().selectionChanged.connect(self.__view_selectionModel__selectionChanged)
		self.modelRefresh.connect(self.__componentsManagerUi__modelRefresh)

		self.initializedUi = True
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

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
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def onStartup(self):
		"""
		This method is triggered on Framework startup.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		self.modelRefresh.emit()
		return True

	@core.executionTrace
	def __componentsManagerUi__modelRefresh(self):
		"""
		This method is triggered when the Model data need refresh.
		"""

		LOGGER.debug("> Refreshing '{0}' Model!".format("Components_Manager_Ui_treeView"))

		self.setComponents()

	@core.executionTrace
	def __view_addActions(self):
		"""
		This method sets the **Components_Manager_Ui_treeView** actions.
		"""

		self.Components_Manager_Ui_treeView.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.ComponentsManagerUi|Activate Component(s)",
		slot=self.__view_activateComponentsAction__triggered))
		self.Components_Manager_Ui_treeView.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.ComponentsManagerUi|Deactivate Component(s)",
		slot=self.__view_deactivateComponentsAction__triggered))

		separatorAction = QAction(self.Components_Manager_Ui_treeView)
		separatorAction.setSeparator(True)
		self.Components_Manager_Ui_treeView.addAction(separatorAction)

		self.Components_Manager_Ui_treeView.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.ComponentsManagerUi|Reload Component(s)",
		slot=self.__view_reloadComponentsAction__triggered))

		separatorAction = QAction(self.Components_Manager_Ui_treeView)
		separatorAction.setSeparator(True)
		self.Components_Manager_Ui_treeView.addAction(separatorAction)

	@core.executionTrace
	def __view_activateComponentsAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.ComponentsManagerUi|Activate Component(s)'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.activateComponentsUi()

	@core.executionTrace
	def __view_deactivateComponentsAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|factory.ComponentsManagerUi|Deactivate Component(s)'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.deactivateComponentsUi()

	@core.executionTrace
	def __view_reloadComponentsAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.ComponentsManagerUi|Reload Component(s)'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.reloadComponentsUi()

	@core.executionTrace
	def __view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
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
		for node in foundations.walkers.nodesWalker(self.__model.rootNode):
			if node.family == "Component":
				node.component.interface.activated or deactivatedComponents.append(node.component.name)

		LOGGER.debug("> Storing '{0}' deactivated Components.".format(", ".join(deactivatedComponents)))
		self.__settings.setKey("Settings", "deactivatedComponents", ",".join(deactivatedComponents))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler,
											False,
											manager.exceptions.ComponentActivationError)
	@umbra.engine.encapsulateProcessing
	def activateComponentsUi(self):
		"""
		This method activates user selected Components.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedComponents = self.getSelectedComponents()

		self.__engine.startProcessing("Activating Components ...", len(selectedComponents))
		activationFailedComponents = []
		for component in selectedComponents:
			if not component.interface.activated:
				success = self.activateComponent(component.name) or False
				if not success:
					activationFailedComponents.append(component)
			else:
				self.__engine.notificationsManager.warnify("{0} | '{1}' Component is already activated!".format(
				self.__class__.__name__, component.name))
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

		self.__storeDeactivatedComponents()

		if not activationFailedComponents:
			return True
		else:
			raise manager.exceptions.ComponentActivationError(
			"{0} | Exception(s) raised while activating '{1}' Component(s)!".format(self.__class__.__name__,
			", ". join((activationFailedComponent.name for activationFailedComponent in activationFailedComponents))))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler,
											False,
											manager.exceptions.ComponentDeactivationError)
	@umbra.engine.encapsulateProcessing
	def deactivateComponentsUi(self):
		"""
		This method deactivates user selected Components.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedComponents = self.getSelectedComponents()

		self.__engine.startProcessing("Deactivating Components ...", len(selectedComponents))
		deactivationFailedComponents = []
		for component in selectedComponents:
			if component.interface.activated:
				if component.interface.deactivatable:
					success = self.deactivateComponent(component.name) or False
					if not success:
						deactivationFailedComponents.append(component)
				else:
					self.__engine.notificationsManager.warnify(
					"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, component.name))
			else:
				self.__engine.notificationsManager.warnify(
				"{0} | '{1}' Component is already deactivated!".format(self.__class__.__name__, component.name))
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

		self.__storeDeactivatedComponents()

		if not deactivationFailedComponents:
			return True
		else:
			raise manager.exceptions.ComponentDeactivationError(
			"{0} | Exception(s) raised while deactivating '{1}' Component(s)!".format(self.__class__.__name__,
			", ". join((deactivationFailedComponent.name
			for deactivationFailedComponent in deactivationFailedComponents))))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler,
											False,
											manager.exceptions.ComponentReloadError)
	@umbra.engine.encapsulateProcessing
	def reloadComponentsUi(self):
		"""
		This method reloads user selected Components.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		selectedComponents = self.getSelectedComponents()

		self.__engine.startProcessing("Reloading Components ...", len(selectedComponents))
		reloadFailedComponents = []
		for component in selectedComponents:
			if component.interface.deactivatable:
				success = self.reloadComponent(component.name) or False
				if not success:
					reloadFailedComponents.append(component)
			else:
				self.__engine.notificationsManager.warnify(
				"{0} | '{1}' Component cannot be deactivated and won't be reloaded!".format(self.__class__.__name__,
																							component.name))
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

		if not reloadFailedComponents:
			return True
		else:
			raise manager.exceptions.ComponentReloadError(
			"{0} | Exception(s) raised while reloading '{1}' Component(s)!".format(self.__class__.__name__,
			", ". join((reloadFailedComponent.name for reloadFailedComponent in reloadFailedComponents))))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, manager.exceptions.ComponentExistsError, Exception)
	def activateComponent(self, name):
		"""
		This method activates given Component.

		:param name: Component name. ( String )
		:return: Method success. ( Boolean )
		"""

		if not name in self.__engine.componentsManager.components:
			raise manager.exceptions.ComponentExistsError(
			"{0} | '{1}' Component isn't registered in the Components Manager!".format(self.__class__.__name__, name))

		component = self.__engine.componentsManager.components[name]
		if component.interface.activated:
			LOGGER.warning("!> {0} | '{1}' Component is already activated!".format(self.__class__.__name__, name))
			return False

		LOGGER.debug("> Attempting '{0}' Component activation.".format(component.name))
		component.interface.activate(self.__engine)
		if component.category in ("Default", "QObject"):
			component.interface.initialize()
		elif component.category == "QWidget":
			component.interface.initializeUi()
			component.interface.addWidget()
		LOGGER.info("{0} | '{1}' Component has been activated!".format(self.__class__.__name__, component.name))
		self.activatedComponent.emit(name)
		self.modelRefresh.emit()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None,
											False,
											manager.exceptions.ComponentExistsError,
											manager.exceptions.ComponentDeactivationError)
	def deactivateComponent(self, name):
		"""
		This method deactivates given Component.

		:param name: Component name. ( String )
		:return: Method success. ( Boolean )
		"""

		if not name in self.__engine.componentsManager.components:
			raise manager.exceptions.ComponentExistsError(
			"{0} | '{0}' Component isn't registered in the Components Manager!".format(self.__class__.__name__, name))

		component = self.__engine.componentsManager.components[name]
		if not component.interface.activated:
			LOGGER.warning("!> {0} | '{1}' Component is already deactivated!".format(self.__class__.__name__, name))
			return False

		LOGGER.debug("> Attempting '{0}' Component deactivation.".format(component.name))
		if component.interface.deactivatable:
			if component.category in ("Default", "QObject"):
				component.interface.uninitialize()
			elif component.category == "QWidget":
				component.interface.uninitializeUi()
				component.interface.removeWidget()
			component.interface.deactivate()
			LOGGER.info("{0} | '{1}' Component has been deactivated!".format(self.__class__.__name__, component.name))
			self.deactivatedComponent.emit(name)
			self.modelRefresh.emit()
			return True
		else:
			raise manager.exceptions.ComponentDeactivationError(
			"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, component.name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None,
											False,
											manager.exceptions.ComponentExistsError,
											manager.exceptions.ComponentReloadError)
	def reloadComponent(self, name):
		"""
		This method reloads given Component.

		:param name: Component name. ( String )
		:return: Method success. ( Boolean )
		"""

		if not name in self.__engine.componentsManager.components:
			raise manager.exceptions.ComponentExistsError(
			"{0} | '{1}' Component isn't registered in the Components Manager!".format(self.__class__.__name__, name))

		component = self.__engine.componentsManager.components[name]

		LOGGER.debug("> Attempting '{0}' Component reload.".format(component.name))
		if component.interface.deactivatable:
			if component.interface.activated:
				self.deactivateComponent(name)
			self.__engine.componentsManager.reloadComponent(component.name)
			if not component.interface.activated:
				self.activateComponent(name)
			LOGGER.info("{0} | '{1}' Component has been reloaded!".format(self.__class__.__name__, component.name))
			self.reloadedComponent.emit(name)
			self.modelRefresh.emit()
			return True
		else:
			raise manager.exceptions.ComponentReloadError(
			"{0} | '{1}' Component cannot be deactivated and won't be reloaded!".format(self.__class__.__name__,
																						component.name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getComponents(self):
		"""
		This method returns the Components.

		:return: Components. ( List )
		"""

		return self.__engine.componentsManager.components

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listComponents(self):
		"""
		This method lists the Components names.

		:return: Components names. ( List )
		"""

		return self.__engine.componentsManager.listComponents()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setComponents(self):
		"""
		This method sets the Components Model nodes.
		"""

		nodeFlags = attributesFlags = int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

		rootNode = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")

		paths = {}
		for path in self.__engine.componentsManager.paths:
			basename = os.path.basename(path)
			if not paths.get(basename):
				paths[basename] = {}

			components = {}
			for name, component in self.__engine.componentsManager.components.iteritems():
				if os.path.normpath(path) in os.path.normpath(component.directory):
					continue

				components[name] = component
			
			paths[basename].update(components)

		for path, components in paths.iteritems():
			pathNode = PathNode(name=path.title(),
								parent=rootNode,
								nodeFlags=nodeFlags,
								attributesFlags=attributesFlags,
								activated=umbra.ui.nodes.GraphModelAttribute(name="activated", flags=attributesFlags),
								category=umbra.ui.nodes.GraphModelAttribute(name="category", flags=attributesFlags),
								rank=umbra.ui.nodes.GraphModelAttribute(name="rank", flags=attributesFlags),
								version=umbra.ui.nodes.GraphModelAttribute(name="version", flags=attributesFlags))

			for component in components.itervalues():
				if not component.interface:
					continue

				componentNode = ComponentNode(component,
										name=component.title,
										parent=pathNode,
										nodeFlags=nodeFlags,
										attributesFlags=attributesFlags,
										activated=umbra.ui.nodes.GraphModelAttribute(name="activated",
										flags=attributesFlags,
										roles={Qt.DisplayRole: strings.encode(component.interface.activated),
										Qt.DecorationRole:os.path.join(self.__uiResourcesDirectory,
																component.interface.activated and \
																self.__uiActivatedImage or self.__uiDeactivatedImage)}))
				componentNode.roles[Qt.DecorationRole] = os.path.join(self.__uiResourcesDirectory,
															"{0}{1}".format(component.category, self.__uiCategoryAffixe))

		rootNode.sortChildren()

		self.__model.initializeModel(rootNode)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getSelectedNodes(self):
		"""
		This method returns the View selected nodes.

		:return: View selected nodes. ( Dictionary )
		"""

		return self.__view.getSelectedNodes()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getSelectedComponentsNodes(self):
		"""
		This method returns the View selected Components nodes.

		:return: View selected Components nodes. ( List )
		"""

		return [node for node in self.getSelectedNodes() if node.family == "Component"]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getSelectedComponents(self):
		"""
		This method gets the View selected Components.

		:return: View selected Components. ( List )
		"""

		return [node.component for node in self.getSelectedComponentsNodes()]
