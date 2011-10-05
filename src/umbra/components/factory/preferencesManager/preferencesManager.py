#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**preferencesManager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`PreferencesManager` Component Interface class.

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
from manager.qwidgetComponent import QWidgetComponent
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "PreferencesManager"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class PreferencesManager(QWidgetComponent):
	"""
	| This class is the :mod:`umbra.components.core.preferencesManager.preferencesManager` Component Interface class.
	| It exposes Application preferences inside a dedicated `QDockWidget <http://doc.qt.nokia.com/4.7/qdockwidget.html>`_ window.
	"""

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This method initializes the class.

		:param name: Component name. ( String )
		:param uiFile: Ui file. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QWidgetComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__uiPath = "ui/Preferences_Manager.ui"
		self.__dockArea = 2

		self.__container = None
		self.__settings = None

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiPath(self):
		"""
		This method is the property for **self.__uiPath** attribute.

		:return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for **self.__uiPath** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This method is the deleter method for **self.__uiPath** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPath"))

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

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__container = container

		self.__settings = self.__container.settings

		return QWidgetComponent.activate(self)

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

		self.__Logging_Formatters_comboBox_setUi()
		self.__Verbose_Level_comboBox_setUi()
		self.__Restore_Geometry_On_Layout_Change_checkBox_setUi()

		# Signals / Slots.
		self.ui.Logging_Formatters_comboBox.activated.connect(self.__Logging_Formatters_comboBox__activated)
		self.ui.Verbose_Level_comboBox.activated.connect(self.__Verbose_Level_comboBox__activated)
		self.ui.Restore_Geometry_On_Layout_Change_checkBox.stateChanged.connect(self.__Restore_Geometry_On_Layout_Change_checkBox__stateChanged)

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

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component Widget cannot be removed!".format(self.name))

	@core.executionTrace
	def __Logging_Formatters_comboBox_setUi(self):
		"""
		This method fills **Logging_Formatter_comboBox** Widget.
		"""

		self.ui.Logging_Formatters_comboBox.clear()
		LOGGER.debug("> Available logging formatters: '{0}'.".format(", ".join(RuntimeGlobals.loggingFormatters.keys())))
		self.ui.Logging_Formatters_comboBox.insertItems(0, QStringList (RuntimeGlobals.loggingFormatters.keys()))
		loggingFormatter = self.__settings.getKey("Settings", "loggingFormatter").toString()
		self.__container.loggingActiveFormatter = loggingFormatter and loggingFormatter or Constants.loggingDefaultFormatter
		self.ui.Logging_Formatters_comboBox.setCurrentIndex(self.ui.Logging_Formatters_comboBox.findText(self.__container.loggingActiveFormatter, Qt.MatchExactly))

	@core.executionTrace
	def __Logging_Formatters_comboBox__activated(self, index):
		"""
		This method is called when the **Logging_Formatter_comboBox** Widget is activated.

		:param index: ComboBox activated item index. ( Integer )
		"""

		formatter = str(self.ui.Logging_Formatters_comboBox.currentText())
		LOGGER.debug("> Setting logging formatter: '{0}'.".format(formatter))
		RuntimeGlobals.loggingActiveFormatter = formatter
		self.setLoggingFormatter()
		self.__settings.setKey("Settings", "loggingFormatter", self.ui.Logging_Formatters_comboBox.currentText())

	@core.executionTrace
	def __Verbose_Level_comboBox_setUi(self):
		"""
		This method fills **Verbose_Level_ComboBox** Widget.
		"""

		self.ui.Verbose_Level_comboBox.clear()
		LOGGER.debug("> Available verbose levels: '{0}'.".format(Constants.verbosityLabels))
		self.ui.Verbose_Level_comboBox.insertItems(0, QStringList (Constants.verbosityLabels))
		self.__container.verbosityLevel = self.__settings.getKey("Settings", "verbosityLevel").toInt()[0]
		self.ui.Verbose_Level_comboBox.setCurrentIndex(self.__container.verbosityLevel)

	@core.executionTrace
	def __Verbose_Level_comboBox__activated(self, index):
		"""
		This method is called when the **Verbose_Level_ComboBox** Widget is triggered.

		:param index: ComboBox activated item index. ( Integer )
		"""

		LOGGER.debug("> Setting verbose level: '{0}'.".format(self.ui.Verbose_Level_comboBox.currentText()))
		self.__container.verbosityLevel = int(self.ui.Verbose_Level_comboBox.currentIndex())
		core.setVerbosityLevel(int(self.ui.Verbose_Level_comboBox.currentIndex()))
		self.__settings.setKey("Settings", "verbosityLevel", self.ui.Verbose_Level_comboBox.currentIndex())

	@core.executionTrace
	def __Restore_Geometry_On_Layout_Change_checkBox_setUi(self):
		"""
		This method sets the **Restore_Geometry_On_Layout_Change_checkBox** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey("Settings", "restoreGeometryOnLayoutChange").isNull() and self.__settings.setKey("Settings", "restoreGeometryOnLayoutChange", Qt.Unchecked)

		restoreGeometryOnLayoutChange = self.__settings.getKey("Settings", "restoreGeometryOnLayoutChange").toInt()[0]
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Restore_Geometry_On_Layout_Change_checkBox", restoreGeometryOnLayoutChange))
		self.ui.Restore_Geometry_On_Layout_Change_checkBox.setCheckState(restoreGeometryOnLayoutChange)
		self.__container.settings._datas.restoreGeometryOnLayoutChange = restoreGeometryOnLayoutChange and True or False

	@core.executionTrace
	def __Restore_Geometry_On_Layout_Change_checkBox__stateChanged(self, state):
		"""
		This method is called when **Restore_Geometry_On_Layout_Change_checkBox** state changes.

		:param state: Checkbox state. ( Integer )
		"""

		restoreGeometryOnLayoutChange = self.ui.Restore_Geometry_On_Layout_Change_checkBox.checkState()
		LOGGER.debug("> Restore geometry on layout change state: '{0}'.".format(restoreGeometryOnLayoutChange))
		self.__settings.setKey("Settings", "restoreGeometryOnLayoutChange", restoreGeometryOnLayoutChange)
		self.__container.settings._datas.restoreGeometryOnLayoutChange = restoreGeometryOnLayoutChange and True or False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setLoggingFormatter(self):
		"""
		This method sets the logging formatter.
		"""

		for handler in (RuntimeGlobals.loggingConsoleHandler, RuntimeGlobals.loggingFileHandler, RuntimeGlobals.loggingSessionHandler):
			handler and handler.setFormatter(RuntimeGlobals.loggingFormatters[RuntimeGlobals.loggingActiveFormatter])
