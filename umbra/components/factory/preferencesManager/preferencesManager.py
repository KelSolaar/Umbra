#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**preferencesManager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`PreferencesManager` Component Interface class.

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
from PyQt4.QtCore import QStringList
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
import umbra.ui.common
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "PreferencesManager"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Preferences_Manager.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class PreferencesManager(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| Defines the :mod:`umbra.components.factory.preferencesManager.preferencesManager` Component Interface class.
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

		self.__dockArea = 2

		self.__engine = None
		self.__settings = None

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

		self.activated = True
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		Deactivates the Component.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

	def initializeUi(self):
		"""
		Initializes the Component ui.
		
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		umbra.ui.common.setToolBoxHeight(self.Preferences_Manager_toolBox)

		self.__Logging_Formatters_comboBox_setUi()
		self.__Verbose_Level_comboBox_setUi()
		self.__Restore_Geometry_On_Layout_Change_checkBox_setUi()

		# Signals / Slots.
		self.__engine.verbosityLevelChanged.connect(self.__engine__verbosityLevelChanged)
		self.Logging_Formatters_comboBox.activated.connect(self.__Logging_Formatters_comboBox__activated)
		self.Verbose_Level_comboBox.activated.connect(self.__Verbose_Level_comboBox__activated)
		self.Restore_Geometry_On_Layout_Change_checkBox.stateChanged.connect(
		self.__Restore_Geometry_On_Layout_Change_checkBox__stateChanged)

		self.initializedUi = True
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		Uninitializes the Component ui.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

	def addWidget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		Removes the Component Widget from the engine.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component Widget cannot be removed!".format(self.__class__.__name__, self.name))

	def __engine__verbosityLevelChanged(self, verbosityLevel):
		"""
		Defines the slot triggered by the engine when verbosity level has changed.

		:param verbosityLevel: Current verbosity level.
		:type verbosityLevel: int
		"""

		self.Verbose_Level_comboBox.setCurrentIndex(verbosityLevel)

	def __Logging_Formatters_comboBox_setUi(self):
		"""
		Fills **Logging_Formatter_comboBox** Widget.
		"""

		self.Logging_Formatters_comboBox.clear()
		LOGGER.debug("> Available logging formatters: '{0}'.".format(", ".join(RuntimeGlobals.loggingFormatters)))
		self.Logging_Formatters_comboBox.insertItems(0, QStringList(RuntimeGlobals.loggingFormatters.keys()))
		loggingFormatter = self.__settings.getKey("Settings", "loggingFormatter").toString()
		self.__engine.loggingActiveFormatter = loggingFormatter and loggingFormatter or Constants.loggingDefaultFormatter
		self.Logging_Formatters_comboBox.setCurrentIndex(self.Logging_Formatters_comboBox.findText(
		self.__engine.loggingActiveFormatter, Qt.MatchExactly))

	def __Logging_Formatters_comboBox__activated(self, index):
		"""
		Defines the slot triggered by the **Logging_Formatter_comboBox** Widget when activated.

		:param index: ComboBox activated item index.
		:type index: int
		"""

		formatter = foundations.strings.toString(self.Logging_Formatters_comboBox.currentText())
		LOGGER.debug("> Setting logging formatter: '{0}'.".format(formatter))
		RuntimeGlobals.loggingActiveFormatter = formatter
		self.setLoggingFormatter()
		self.__settings.setKey("Settings", "loggingFormatter", self.Logging_Formatters_comboBox.currentText())

	def __Verbose_Level_comboBox_setUi(self):
		"""
		Fills **Verbose_Level_ComboBox** Widget.
		"""

		self.Verbose_Level_comboBox.clear()
		LOGGER.debug("> Available verbose levels: '{0}'.".format(Constants.verbosityLabels))
		self.Verbose_Level_comboBox.insertItems(0, QStringList (Constants.verbosityLabels))
		self.__engine.verbosityLevel = foundations.common.getFirstItem(
									self.__settings.getKey("Settings", "verbosityLevel").toInt())
		self.Verbose_Level_comboBox.setCurrentIndex(self.__engine.verbosityLevel)

	def __Verbose_Level_comboBox__activated(self, index):
		"""
		Defines the slot triggered by the **Verbose_Level_ComboBox** Widget when activated.

		:param index: ComboBox activated item index.
		:type index: int
		"""

		LOGGER.debug("> Setting verbose level: '{0}'.".format(self.Verbose_Level_comboBox.currentText()))
		self.__engine.verbosityLevel = index
		foundations.verbose.setVerbosityLevel(index)
		self.__settings.setKey("Settings", "verbosityLevel", index)

	def __Restore_Geometry_On_Layout_Change_checkBox_setUi(self):
		"""
		Sets the **Restore_Geometry_On_Layout_Change_checkBox** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey("Settings", "restoreGeometryOnLayoutChange").isNull() and \
		self.__settings.setKey("Settings", "restoreGeometryOnLayoutChange", Qt.Unchecked)

		restoreGeometryOnLayoutChange = foundations.common.getFirstItem(
										self.__settings.getKey("Settings", "restoreGeometryOnLayoutChange").toInt())
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Restore_Geometry_On_Layout_Change_checkBox",
																restoreGeometryOnLayoutChange))
		self.Restore_Geometry_On_Layout_Change_checkBox.setCheckState(restoreGeometryOnLayoutChange)
		self.__engine.layoutsManager.restoreGeometryOnLayoutChange = restoreGeometryOnLayoutChange and True or False

	def __Restore_Geometry_On_Layout_Change_checkBox__stateChanged(self, state):
		"""
		Defines the slot triggered by **Restore_Geometry_On_Layout_Change_checkBox** Widget when state changed.

		:param state: Checkbox state.
		:type state: int
		"""

		LOGGER.debug("> 'Restore Geometry On Layout Change' state: '{0}'.".format(state))
		self.__settings.setKey("Settings", "restoreGeometryOnLayoutChange", state)
		self.__engine.layoutsManager.restoreGeometryOnLayoutChange = state and True or False

	def setLoggingFormatter(self):
		"""
		Sets the logging formatter.
		"""

		for handler in (RuntimeGlobals.loggingConsoleHandler,
						RuntimeGlobals.loggingFileHandler,
						RuntimeGlobals.loggingSessionHandler):
			handler and handler.setFormatter(RuntimeGlobals.loggingFormatters[RuntimeGlobals.loggingActiveFormatter])
