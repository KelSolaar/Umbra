#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**application_QToolBar.py.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`Application_QToolBar` class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
from PyQt4.QtCore import QSize
from PyQt4.QtCore import QString
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QToolBar

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import umbra.managers.layoutsManager
import umbra.ui.common
from umbra.globals.constants import Constants
from umbra.globals.uiConstants import UiConstants
from umbra.ui.widgets.active_QLabel import Active_QLabel
from umbra.ui.widgets.active_QLabelsCollection import Active_QLabelsCollection

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Application_QToolBar"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Application_QToolBar(QToolBar):
	"""
	Defines a `QToolBar <http://doc.qt.nokia.com/qtoolbar.html>`_ subclass providing
	the Application toolbar.
	"""

	def __init__(self, parent=None):
		"""
		Initializes the class.

		:param parent: Widget parent.
		:type parent: QObject
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QToolBar.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__container = parent
		self.__settings = self.__container.settings

		self.__layoutsActiveLabelsCollection = None
		self.__customLayoutsMenu = None
		self.__miscellaneousMenu = None

		self.__userLayouts = (umbra.managers.layoutsManager.Layout(name="1", identity="one", shortcut=Qt.Key_1),
							umbra.managers.layoutsManager.Layout(name="2", identity="two", shortcut=Qt.Key_2),
							umbra.managers.layoutsManager.Layout(name="3", identity="three", shortcut=Qt.Key_3),
							umbra.managers.layoutsManager.Layout(name="4", identity="four", shortcut=Qt.Key_4),
							umbra.managers.layoutsManager.Layout(name="5", identity="five", shortcut=Qt.Key_5))

		Application_QToolBar.__initializeUi(self)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def container(self):
		"""
		Property for **self.__container** attribute.

		:return: self.__container.
		:rtype: QObject
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		Setter for **self.__container** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		Deleter for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def settings(self):
		"""
		Property for **self.__settings** attribute.

		:return: self.__settings.
		:rtype: Preferences
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		Setter for **self.__settings** attribute.

		:param value: Attribute value.
		:type value: Preferences
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
	def layoutsActiveLabelsCollection(self):
		"""
		Property for **self.__layoutsActiveLabelsCollection** attribute.

		:return: self.__layoutsActiveLabelsCollection.
		:rtype: Active_QLabelsCollection
		"""

		return self.__layoutsActiveLabelsCollection

	@layoutsActiveLabelsCollection.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def layoutsActiveLabelsCollection(self, value):
		"""
		Setter for **self.__layoutsActiveLabelsCollection** attribute.

		:param value: Attribute value.
		:type value: Active_QLabelsCollection
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "layoutsActiveLabelsCollection"))

	@layoutsActiveLabelsCollection.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def layoutsActiveLabelsCollection(self):
		"""
		Deleter for **self.__layoutsActiveLabelsCollection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "layoutsActiveLabelsCollection"))

	@property
	def customLayoutsMenu(self):
		"""
		Property for **self.__customLayoutsMenu** attribute.

		:return: self.__customLayoutsMenu.
		:rtype: QMenu
		"""

		return self.__customLayoutsMenu

	@customLayoutsMenu.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def customLayoutsMenu(self, value):
		"""
		Setter for **self.__customLayoutsMenu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		if value is not None:
			assert type(value) is QMenu, "'{0}' attribute: '{1}' type is not 'QMenu'!".format("customLayoutsMenu", value)
		self.__customLayoutsMenu = value

	@customLayoutsMenu.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def customLayoutsMenu(self):
		"""
		Deleter for **self.__customLayoutsMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "customLayoutsMenu"))

	@property
	def miscellaneousMenu(self):
		"""
		Property for **self.__miscellaneousMenu** attribute.

		:return: self.__miscellaneousMenu.
		:rtype: QMenu
		"""

		return self.__miscellaneousMenu

	@miscellaneousMenu.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def miscellaneousMenu(self, value):
		"""
		Setter for **self.__miscellaneousMenu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		if value is not None:
			assert type(value) is QMenu, "'{0}' attribute: '{1}' type is not 'QMenu'!".format("miscellaneousMenu", value)
		self.__miscellaneousMenu = value

	@miscellaneousMenu.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def miscellaneousMenu(self):
		"""
		Deleter for **self.__miscellaneousMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "miscellaneousMenu"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeUi(self):
		"""
		Initializes the Widget ui.
		"""

		LOGGER.debug("> Initializing Application toolBar!")

		self.setIconSize(QSize(UiConstants.defaultToolbarIconSize, UiConstants.defaultToolbarIconSize))
		self.setAllowedAreas(Qt.TopToolBarArea)
		self.setFloatable(False)
		self.setMovable(False)
		self.setLayoutDefaultGeometry()

		self.setObjectName("toolBar")
		self.setWindowTitle("{0} - toolBar".format(Constants.applicationName))

		self.setToolBarChildrenWidgets()

		# Signals / Slots.
		self.__container.layoutsManager.layoutStored.connect(self.__layoutsManager__layoutStored)
		self.__container.layoutsManager.layoutRestored.connect(self.__layoutsManager__layoutRestored)

	def __layoutActiveLabel__clicked(self, layout):
		"""
		Defines the slot triggered by a **Active_QLabel** Widget when clicked.

		:param layout: Layout name.
		:type layout: unicode
		"""

		self.__container.layoutsManager.restoreLayout(layout)

	def __layoutsManager__layoutStored(self, layout):
		"""
		Defines the slot triggered by :class:`umbra.managers.layoutsManager.LayoutsManager` class
		when a layout is stored.

		:param layout: Layout name.
		:type layout: unicode
		"""

		layoutActiveLabel = self.__layoutsActiveLabelsCollection.getToggledActiveLabel()
		layoutActiveLabel and self.__settings.setKey("Layouts",
										"{0}_activeLabel".format(layout),
										layoutActiveLabel.objectName())

	def __layoutsManager__layoutRestored(self, layout):
		"""
		Defines the slot triggered by :class:`umbra.managers.layoutsManager.LayoutsManager` class
		when a layout is restored.

		:param layout: Layout name.
		:type layout: unicode
		"""

		layoutActiveLabel = self.__settings.getKey("Layouts", "{0}_activeLabel".format(layout)).toString()
		for activeLabel in self.__layoutsActiveLabelsCollection.activeLabels:
			if not activeLabel.objectName() == layoutActiveLabel:
				continue

			activeLabel.setChecked(True)

	def __helpDisplayMiscAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|ToolBar|Miscellaneous|Help content ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Opening url: '{0}'.".format(UiConstants.helpFile))
		QDesktopServices.openUrl(QUrl(QString(UiConstants.helpFile)))
		return True

	def __apiDisplayMiscAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|ToolBar|Miscellaneous|Api content ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Opening url: '{0}'.".format(UiConstants.apiFile))
		QDesktopServices.openUrl(QUrl(QString(UiConstants.apiFile)))
		return True

	def setLayoutDefaultGeometry(self):
		"""
		Sets the toolBar layout default geometry.

		:return: Method success.
		:rtype: bool
		"""

		self.layout().setSpacing(8)
		self.layout().setContentsMargins(0, 0, 0, 0)
		return True

	def setToolBarChildrenWidgets(self):
		"""
		Sets the toolBar children widgets.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding 'Application_Logo_label' widget!")
		self.addWidget(self.getApplicationLogoLabel())

		LOGGER.debug("> Adding 'Spacer_label' widget!")
		self.addWidget(self.getSpacerLabel())

		LOGGER.debug("> Adding 'Development_activeLabel', 'Preferences_activeLabel' widgets!")
		for layoutActiveLabel in self.getLayoutsActiveLabels():
			self.addWidget(layoutActiveLabel)

		LOGGER.debug("> Adding 'Custom_Layouts_activeLabel' widget!")
		self.addWidget(self.getCustomLayoutsActiveLabel())

		LOGGER.debug("> Adding 'Miscellaneous_activeLabel' widget!")
		self.addWidget(self.getMiscellaneousActiveLabel())

		LOGGER.debug("> Adding 'Closure_Spacer_label' widget!")
		self.addWidget(self.getClosureSpacerLabel())

		return True

	def getApplicationLogoLabel(self):
		"""
		Provides the default **Application_Logo_label** widget.

		:return: Application logo label.
		:rtype: QLabel
		"""

		logoLabel = QLabel()
		logoLabel.setObjectName("Application_Logo_label")
		logoLabel.setPixmap(QPixmap(umbra.ui.common.getResourcePath(UiConstants.logoImage)))
		return logoLabel

	def getLayoutActiveLabel(self, resources, name, title, identity, shortcut):
		"""
		Returns a layout **Active_QLabel** widget.

		:param resources: Icons resources ( Default / Hover / Active ).
		:type resources: tuple
		:param name: Ui object name.
		:type name: unicode
		:param title: Layout registration title.
		:type title: unicode
		:param identity: Layout code name.
		:type identity: unicode
		:param shortcut: Layout associated shortcut. ( QtCore.Key )
		:return: Layout active label.
		:rtype: Active_QLabel
		"""

		defaultIcon, hoverIcon, activeIcon = resources
		layoutActiveLabel = Active_QLabel(self,
										QPixmap(umbra.ui.common.getResourcePath(defaultIcon)),
										QPixmap(umbra.ui.common.getResourcePath(hoverIcon)),
										QPixmap(umbra.ui.common.getResourcePath(activeIcon)),
										True)
		self.__container.layoutsManager.registerLayout(identity, umbra.managers.layoutsManager.Layout(name=title,
																								identity=identity,
																								shortcut=shortcut))
		self.__container.addAction(
		self.__container.actionsManager.registerAction("Actions|Umbra|ToolBar|Layouts|Restore layout {0}".format(title),
														shortcut=shortcut,
														shortcutContext=Qt.ApplicationShortcut,
														slot=functools.partial(
														self.__container.layoutsManager.restoreLayout, identity)))

		layoutActiveLabel.setObjectName(name)

		# Signals / Slots.
		layoutActiveLabel.clicked.connect(functools.partial(self.__layoutActiveLabel__clicked, identity))

		return layoutActiveLabel

	def getLayoutsActiveLabels(self):
		"""
		Returns the layouts **Active_QLabel** widgets.

		:return: Layouts active labels.
		:rtype: list
		"""

		self.__layoutsActiveLabelsCollection = Active_QLabelsCollection(self)

		self.__layoutsActiveLabelsCollection.addActiveLabel(self.getLayoutActiveLabel((UiConstants.developmentIcon,
																					UiConstants.developmentHoverIcon,
																					UiConstants.developmentActiveIcon),
																					"Development_activeLabel",
																					"Development",
																					"developmentCentric",
																					Qt.Key_9))

		self.__layoutsActiveLabelsCollection.addActiveLabel(self.getLayoutActiveLabel((UiConstants.preferencesIcon,
																					UiConstants.preferencesHoverIcon,
																					UiConstants.preferencesActiveIcon),
																					"Preferences_activeLabel",
																					"Preferences",
																					"preferencesCentric",
																					Qt.Key_0))
		return self.__layoutsActiveLabelsCollection.activeLabels

	def getCustomLayoutsActiveLabel(self):
		"""
		Provides the default **Custom_Layouts_activeLabel** widget.

		:return: Layout active label.
		:rtype: Active_QLabel
		"""

		layoutActiveLabel = Active_QLabel(self, QPixmap(umbra.ui.common.getResourcePath(UiConstants.customLayoutsIcon)),
									QPixmap(umbra.ui.common.getResourcePath(UiConstants.customLayoutsHoverIcon)),
									QPixmap(umbra.ui.common.getResourcePath(UiConstants.customLayoutsActiveIcon)))
		layoutActiveLabel.setObjectName("Custom_Layouts_activeLabel")

		self.__customLayoutsMenu = QMenu("Layouts", layoutActiveLabel)

		for layout in self.__userLayouts:
			self.__container.layoutsManager.registerLayout(layout.identity, layout)
			self.__customLayoutsMenu.addAction(self.__container.actionsManager.registerAction(
			"Actions|Umbra|ToolBar|Layouts|Restore layout {0}".format(layout.name),
			shortcut=layout.shortcut,
			slot=functools.partial(self.__container.layoutsManager.restoreLayout, layout.identity)))

		self.__customLayoutsMenu.addSeparator()

		for layout in self.__userLayouts:
			self.__customLayoutsMenu.addAction(self.__container.actionsManager.registerAction(
			"Actions|Umbra|ToolBar|Layouts|Store layout {0}".format(layout.name),
			shortcut=Qt.CTRL + layout.shortcut,
			slot=functools.partial(self.__container.layoutsManager.storeLayout, layout.identity)))

		self.__customLayoutsMenu.addSeparator()

		self.__customLayoutsMenu.addAction(self.__container.actionsManager.registerAction(
		"Actions|Umbra|ToolBar|Layouts|Toggle FullScreen",
		shortcut=Qt.ControlModifier + Qt.SHIFT + Qt.Key_F,
		slot=self.__container.toggleFullScreen))

		layoutActiveLabel.setMenu(self.__customLayoutsMenu)
		return layoutActiveLabel

	def getMiscellaneousActiveLabel(self):
		"""
		Provides the default **Miscellaneous_activeLabel** widget.

		:return: Miscellaneous active label.
		:rtype: Active_QLabel
		"""

		miscellaneousActiveLabel = Active_QLabel(self,
											QPixmap(umbra.ui.common.getResourcePath(UiConstants.miscellaneousIcon)),
											QPixmap(umbra.ui.common.getResourcePath(UiConstants.miscellaneousHoverIcon)),
											QPixmap(umbra.ui.common.getResourcePath(UiConstants.miscellaneousActiveIcon)))
		miscellaneousActiveLabel.setObjectName("Miscellaneous_activeLabel")

		self.__miscellaneousMenu = QMenu("Miscellaneous", miscellaneousActiveLabel)

		self.__miscellaneousMenu.addAction(self.__container.actionsManager.registerAction(
											"Actions|Umbra|ToolBar|Miscellaneous|Help content ...",
											shortcut="F1",
											slot=self.__helpDisplayMiscAction__triggered))
		self.__miscellaneousMenu.addAction(self.__container.actionsManager.registerAction(
											"Actions|Umbra|ToolBar|Miscellaneous|Api content ...",
											slot=self.__apiDisplayMiscAction__triggered))
		self.__miscellaneousMenu.addSeparator()

		miscellaneousActiveLabel.setMenu(self.__miscellaneousMenu)
		return miscellaneousActiveLabel

	def getSpacerLabel(self):
		"""
		Provides the default **Spacer_label** widget.

		:return: Logo spacer label.
		:rtype: QLabel
		"""

		spacer = QLabel()
		spacer.setObjectName("Spacer_label")
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		return spacer

	def getClosureSpacerLabel(self):
		"""
		Provides the default **Closure_Spacer_label** widget.

		:return: Closure spacer label.
		:rtype: QLabel
		"""

		spacer = QLabel()
		spacer.setObjectName("Closure_Spacer_label")
		spacer.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
		return spacer

if __name__ == "__main__":
	import sys
	from PyQt4.QtGui import QMainWindow

	from manager.componentsManager import Manager
	from umbra.managers.actionsManager import ActionsManager
	from umbra.managers.layoutsManager import LayoutsManager
	from umbra.preferences import Preferences

	application = umbra.ui.common.getApplicationInstance()

	mainWindow = QMainWindow()

	mainWindow.settings = Preferences()
	mainWindow.actionsManager = ActionsManager(mainWindow)
	mainWindow.layoutsManager = LayoutsManager(mainWindow)
	mainWindow.componentsManager = Manager()
	mainWindow.toggleFullScreen = lambda: sys.stdout.write("toggleFullScreen()\n")

	mainWindow.setCentralWidget(QLabel())

	application_QToolBar = Application_QToolBar(mainWindow)
	mainWindow.addToolBar(application_QToolBar)

	mainWindow.show()
	mainWindow.raise_()

	sys.exit(application.exec_())
