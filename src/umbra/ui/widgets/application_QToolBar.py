#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**application_QToolBar.py.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Application_QToolBar` class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
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
import foundations.common
import foundations.core as core
import foundations.exceptions
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
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Application_QToolBar"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Application_QToolBar(QToolBar):
	"""
	This class is a `QToolBar <http://doc.qt.nokia.com/qtoolbar.html>`_ subclass providing
	the Application toolbar.
	"""

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def settings(self):
		"""
		This method is the property for **self.__settings** attribute.

		:return: self.__settings. ( Preferences )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This method is the setter method for **self.__settings** attribute.

		:param value: Attribute value. ( Preferences )
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
	def layoutsActiveLabelsCollection(self):
		"""
		This method is the property for **self.__layoutsActiveLabelsCollection** attribute.

		:return: self.__layoutsActiveLabelsCollection. ( Active_QLabelsCollection )
		"""

		return self.__layoutsActiveLabelsCollection

	@layoutsActiveLabelsCollection.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def layoutsActiveLabelsCollection(self, value):
		"""
		This method is the setter method for **self.__layoutsActiveLabelsCollection** attribute.

		:param value: Attribute value. ( Active_QLabelsCollection )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "layoutsActiveLabelsCollection"))

	@layoutsActiveLabelsCollection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def layoutsActiveLabelsCollection(self):
		"""
		This method is the deleter method for **self.__layoutsActiveLabelsCollection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "layoutsActiveLabelsCollection"))

	@property
	def customLayoutsMenu(self):
		"""
		This method is the property for **self.__customLayoutsMenu** attribute.

		:return: self.__customLayoutsMenu. ( QMenu )
		"""

		return self.__customLayoutsMenu

	@customLayoutsMenu.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def customLayoutsMenu(self, value):
		"""
		This method is the setter method for **self.__customLayoutsMenu** attribute.

		:param value: Attribute value. ( QMenu )
		"""

		if value is not None:
			assert type(value) is QMenu, "'{0}' attribute: '{1}' type is not 'QMenu'!".format("customLayoutsMenu", value)
		self.__customLayoutsMenu = value

	@customLayoutsMenu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def customLayoutsMenu(self):
		"""
		This method is the deleter method for **self.__customLayoutsMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "customLayoutsMenu"))

	@property
	def miscellaneousMenu(self):
		"""
		This method is the property for **self.__miscellaneousMenu** attribute.

		:return: self.__miscellaneousMenu. ( QMenu )
		"""

		return self.__miscellaneousMenu

	@miscellaneousMenu.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def miscellaneousMenu(self, value):
		"""
		This method is the setter method for **self.__miscellaneousMenu** attribute.

		:param value: Attribute value. ( QMenu )
		"""

		if value is not None:
			assert type(value) is QMenu, "'{0}' attribute: '{1}' type is not 'QMenu'!".format("miscellaneousMenu", value)
		self.__miscellaneousMenu = value

	@miscellaneousMenu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def miscellaneousMenu(self):
		"""
		This method is the deleter method for **self.__miscellaneousMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "miscellaneousMenu"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
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

	@core.executionTrace
	def __layoutActiveLabel__clicked(self, layout):
		"""
		This method is triggered when a **Active_QLabel** Widget is clicked.

		:param layout: Layout name. ( String )
		"""

		self.__container.layoutsManager.restoreLayout(layout)

	@core.executionTrace
	def __layoutsManager__layoutStored(self, layout):
		"""
		This method is triggered by the :class:`umbra.managers.layoutsManager.LayoutsManager` class
		when a layout is stored.

		:param layout: Layout name. ( String )
		"""

		layoutActiveLabel = self.__layoutsActiveLabelsCollection.getToggledActiveLabel()
		layoutActiveLabel and self.__settings.setKey("Layouts",
										"{0}_activeLabel".format(layout),
										self.__layoutsActiveLabelsCollection.getActiveLabelIndex(layoutActiveLabel))

	@core.executionTrace
	def __layoutsManager__layoutRestored(self, layout):
		"""
		This method is triggered by the :class:`umbra.managers.layoutsManager.LayoutsManager` class
		when a layout is restored.

		:param layout: Layout name. ( String )
		"""

		layoutActiveLabel = self.__layoutsActiveLabelsCollection.getActiveLabelFromIndex(foundations.common.getFirstItem(
							self.__settings.getKey("Layouts", "{0}_activeLabel".format(layout)).toInt()))
		layoutActiveLabel and layoutActiveLabel.setChecked(True)

	@core.executionTrace
	def __helpDisplayMiscAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|ToolBar|Miscellaneous|Help content ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Opening url: '{0}'.".format(UiConstants.helpFile))
		QDesktopServices.openUrl(QUrl(QString(UiConstants.helpFile)))
		return True

	@core.executionTrace
	def __apiDisplayMiscAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|ToolBar|Miscellaneous|Api content ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Opening url: '{0}'.".format(UiConstants.apiFile))
		QDesktopServices.openUrl(QUrl(QString(UiConstants.apiFile)))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setLayoutDefaultGeometry(self):
		"""
		This method sets the toolBar layout default geometry.

		:return: Method success. ( Boolean )
		"""

		self.layout().setSpacing(8)
		self.layout().setContentsMargins(0, 0, 0, 0)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setToolBarChildrenWidgets(self):
		"""
		This method sets the toolBar children widgets.

		:return: Method success. ( Boolean )
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

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getApplicationLogoLabel(self):
		"""
		This method provides the default **Application_Logo_label** widget.

		:return: Application logo label. ( QLabel )
		"""

		logoLabel = QLabel()
		logoLabel.setObjectName("Application_Logo_label")
		logoLabel.setPixmap(QPixmap(umbra.ui.common.getResourcePath(UiConstants.logoImage)))
		return logoLabel

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getLayoutActiveLabel(self, resources, name, title, identity, shortcut):
		"""
		This method returns a layout **Active_QLabel** widget.

		:param resources: Icons resources ( Default / Hover / Active ). ( Tuple )
		:param name: Ui object name. ( String )
		:param title: Layout registration title. ( String )
		:param identity: Layout code name. ( String )
		:param shortcut: Layout associated shortcut. ( QtCore.Key )
		:return: Layout active label. ( Active_QLabel )
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

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getLayoutsActiveLabels(self):
		"""
		This method returns the layouts **Active_QLabel** widgets.

		:return: Layouts active labels. ( List )
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

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getCustomLayoutsActiveLabel(self):
		"""
		This method provides the default **Custom_Layouts_activeLabel** widget.

		:return: Layout active label. ( Active_QLabel )
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

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getMiscellaneousActiveLabel(self):
		"""
		This method provides the default **Miscellaneous_activeLabel** widget.

		:return: Miscellaneous active label. ( Active_QLabel )
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

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getSpacerLabel(self):
		"""
		This method provides the default **Spacer_label** widget.

		:return: Logo spacer label. ( QLabel )
		"""

		spacer = QLabel()
		spacer.setObjectName("Spacer_label")
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		return spacer

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getClosureSpacerLabel(self):
		"""
		This method provides the default **Closure_Spacer_label** widget.

		:return: Closure spacer label. ( QLabel )
		"""

		spacer = QLabel()
		spacer.setObjectName("Closure_Spacer_label")
		spacer.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
		return spacer
