#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**traceUi.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`TraceUi` Component Interface class and others helper objects.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import re
import sys
if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
	from collections import OrderedDict
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import foundations.strings
import foundations.trace
import umbra.exceptions
import umbra.ui.nodes
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.components.addons.traceUi.models import ModulesModel
from umbra.components.addons.traceUi.nodes import ModuleNode
from umbra.components.addons.traceUi.views import Modules_QTreeView
from umbra.ui.widgets.search_QLineEdit import Search_QLineEdit

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "TraceUi"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Trace_Ui.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class TraceUi(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	Defines the :mod:`umbra.components.addons.traceUi.traceUi` Component Interface class.
	"""

	# Custom signals definitions.
	refreshNodes = pyqtSignal()
	"""
	This signal is emited by the :class:`TraceUi` class when :obj:`TraceUi.model` class property model
	nodes needs to be refreshed. ( pyqtSignal )
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

		self.__dockArea = 1

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__model = None
		self.__view = None
		self.__headers = OrderedDict([("Module", "name"),
										("Traced", "traced")])

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def dockArea(self):
		"""
		Property for **self.__dockArea** attribute.

		:return: self.__dockArea.
		:rtype: int
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		Setter for **self.__dockArea** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		Deleter for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

	@property
	def engine(self):
		"""
		Property for **self.__engine** attribute.

		:return: self.__engine.
		:rtype: QObject
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		Setter for **self.__engine** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		Setter for **self.__settings** attribute.

		:param value: Attribute value.
		:type value: QSettings
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		Deleter for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def settingsSection(self):
		"""
		Property for **self.__settingsSection** attribute.

		:return: self.__settingsSection.
		:rtype: unicode
		"""

		return self.__settingsSection

	@settingsSection.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settingsSection(self, value):
		"""
		Setter for **self.__settingsSection** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		Deleter for **self.__settingsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settingsSection"))

	@property
	def model(self):
		"""
		Property for **self.__model** attribute.

		:return: self.__model.
		:rtype: CollectionsModel
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		Setter for **self.__model** attribute.

		:param value: Attribute value.
		:type value: CollectionsModel
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def view(self, value):
		"""
		Setter for **self.__view** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

	@view.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def headers(self, value):
		"""
		Setter for **self.__headers** attribute.

		:param value: Attribute value.
		:type value: OrderedDict
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "headers"))

	@headers.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def headers(self):
		"""
		Deleter for **self.__headers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
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
		self.__settingsSection = self.name

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
		self.__settingsSection = None

		self.activated = False
		return True

	def initializeUi(self):
		"""
		Initializes the Component ui.
		
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.Trace_Modules_Filter_lineEdit = Search_QLineEdit(self)
		self.Trace_Modules_Filter_lineEdit.searchActiveLabel.hide()
		self.Trace_Modules_Filter_lineEdit.setPlaceholderText("Objects Trace Filter ...")
		self.Trace_Modules_Filter_horizontalLayout.addWidget(self.Trace_Modules_Filter_lineEdit)

		self.__model = ModulesModel(self, horizontalHeaders=self.__headers)

		self.Modules_treeView.setParent(None)
		self.Modules_treeView = Modules_QTreeView(self, self.__model)
		self.Modules_treeView.setObjectName("Modules_treeView")
		self.Modules_treeView.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.Trace_Ui_dockWidgetContents_gridLayout.addWidget(self.Modules_treeView, 0, 0)
		self.__view = self.Modules_treeView
		self.__view_addActions()

		self.setModules()

		# Signals / Slots.
		self.refreshNodes.connect(self.__model__refreshNodes)

		self.initializedUi = True
		return True

	def uninitializeUi(self):
		"""
		Uninitializes the Component ui.
		
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		# Signals / Slots.
		self.refreshNodes.disconnect(self.__model__refreshNodes)

		self.__view_removeActions()

		self.__model = None
		self.__view = None

		self.initializedUi = False
		return True

	def addWidget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	def removeWidget(self):
		"""
		Removes the Component Widget from the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.removeDockWidget(self)
		self.setParent(None)

		return True

	def __model__refreshNodes(self):
		"""
		Defines the slot triggered by the Model when Nodes need refresh.
		"""

		self.setModules()

	def __model__refreshAttributes(self):
		"""
		Refreshes the Model Nodes attributes.
		"""

		for node in foundations.walkers.nodesWalker(self.__model.rootNode):
			if foundations.trace.isTraced(node.module) == node.traced.value:
				continue

			node.updateNodeAttributes()

	def __view_addActions(self):
		"""
		Sets the View actions.
		"""

		self.__view.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|addons.traceUi|Trace Module(s)",
		slot=self.__view_traceModulesAction__triggered))
		self.__view.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|addons.traceUi|Untrace Module(s)",
		slot=self.__view_untraceModulesAction__triggered))

	def __view_removeActions(self):
		"""
		Removes the View actions.
		"""

		traceModulesAction = "Actions|Umbra|Components|addons.traceUi|Trace Module(s)"
		untraceModulesAction = "Actions|Umbra|Components|addons.traceUi|Untrace Module(s)"

		for action in (traceModulesAction, untraceModulesAction):
			self.__view.removeAction(self.__engine.actionsManager.getAction(action))
			self.__engine.actionsManager.unregisterAction(action)

	def __view_traceModulesAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|addons.traceUi|Trace Module(s)'** action.

		:param checked: Action checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		pattern = foundations.strings.toString(self.Trace_Modules_Filter_lineEdit.text()) or r".*"
		flags = re.IGNORECASE if self.Case_Sensitive_Matching_pushButton.isChecked() else 0
		return self.traceModules(self.getSelectedModules(), pattern, flags)

	def __view_untraceModulesAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|addons.traceUi|Untrace Module(s)'** action.

		:param checked: Action checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.untraceModules(self.getSelectedModules())

	def getSelectedNodes(self):
		"""
		Returns the View selected nodes.

		:return: View selected nodes.
		:rtype: dict
		"""

		return self.__view.getSelectedNodes()

	def getSelectedModules(self):
		"""
		Returns the View selected modules.

		:return: View selected modules.
		:rtype: list
		"""

		return [node.module for node in self.getSelectedNodes()]

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											foundations.exceptions.UserError)
	def traceModules(self, modules, pattern=r".*", flags=re.IGNORECASE):
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
			foundations.trace.traceModule(module, foundations.verbose.tracer, pattern)
		self.__model__refreshAttributes()
		return True

	def untraceModules(self, modules):
		"""
		Untraces given modules.

		:param modules: Modules to untrace.
		:type modules: list
		:return: Method success.
		:rtype: bool
		"""

		for module in modules:
			foundations.trace.untraceModule(module)
		self.__model__refreshAttributes()
		return True

	def getModules(self):
		"""
		Sets the registered Modules.
	
		:return: Registered modules.
		:rtype: list
		"""

		return foundations.trace.REGISTERED_MODULES

	def setModules(self, modules=None):
		"""
		Sets the modules Model nodes.
	
		:param modules: Modules to set.
		:type modules: list
		:return: Method success.
		:rtype: bool
		"""

		nodeFlags = int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
		modules = modules or self.getModules()
		rootNode = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")
		for module in modules:
			moduleNode = ModuleNode(module=module,
									name=foundations.strings.toString(module.__name__),
									parent=rootNode,
									nodeFlags=nodeFlags,
									attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled))

		rootNode.sortChildren()

		self.__model.initializeModel(rootNode)
		return True

