#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tcpServerUi.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`TCPServerUi` Component Interface class and others helper objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
import socket
import SocketServer
from PyQt4.QtGui import QGridLayout
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
from foundations.tcpServer import TCPServer
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "RequestsStackDataHandler", "TCPServerUi"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "TCP_Server_Ui.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class RequestsStackDataHandler(SocketServer.BaseRequestHandler):
	"""
	This class represents the default requests handler.
	"""

	codes = foundations.dataStructures.Structure(requestEnd="<!RE>",
												serverShutdown="<!SS>")

	@core.executionTrace
	def handle(self):
		"""
		This method reimplements the :meth:`SocketServer.BaseRequestHandler.handle` method.
	
		:return: Method success. ( Boolean )
		"""

		allData = []
		while True:
			data = self.request.recv(1024)
			if not data:
				break

			if self.codes.serverShutdown in data:
				return self.__serverShutdown()

			if self.codes.requestEnd in data:
				allData.append(data[:data.find(self.codes.requestEnd)])
				break

			allData.append(data)
			if len(allData) >= 2:
				tail = allData[-2] + allData[-1]

				if self.codes.serverShutdown in tail:
					return self.__serverShutdown()

				if self.codes.requestEnd in tail:
					allData[-2] = tail[:tail.find(self.codes.requestEnd)]
					allData.pop()
					break

		RuntimeGlobals.requestsStack.append("".join(allData))
		return True

	def __serverShutdown(self):
		"""
		This method shutdowns the TCP Server.
		"""

		return self.container.stop(terminate=True)

class TCPServerUi(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| This class is the :mod:`umbra.components.factory.tcpServerUi.tcpServerUi` Component Interface class.
	| It provides various methods to operate the TCP Server.
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

		super(TCPServerUi, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__preferencesManager = None

		self.__tcpServer = None
		self.__address = socket.gethostbyname(socket.gethostname())
		self.__port = 16384

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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
	def preferencesManager(self):
		"""
		This method is the property for **self.__preferencesManager** attribute.

		:return: self.__preferencesManager. ( QWidget )
		"""

		return self.__preferencesManager

	@preferencesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def preferencesManager(self, value):
		"""
		This method is the setter method for **self.__preferencesManager** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "preferencesManager"))

	@preferencesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def preferencesManager(self):
		"""
		This method is the deleter method for **self.__preferencesManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "preferencesManager"))

	@property
	def tcpServer(self):
		"""
		This method is the property for **self.__tcpServer** attribute.

		:return: self.__tcpServer. ( QWidget )
		"""

		return self.__tcpServer

	@tcpServer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tcpServer(self, value):
		"""
		This method is the setter method for **self.__tcpServer** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tcpServer"))

	@tcpServer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tcpServer(self):
		"""
		This method is the deleter method for **self.__tcpServer** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tcpServer"))

	@property
	def address(self):
		"""
		This method is the property for **self.__address** attribute.

		:return: self.__address. ( String )
		"""

		return self.__address

	@address.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def address(self, value):
		"""
		This method is the setter method for **self.__address** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"address", value)
		self.__address = value

	@address.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def address(self):
		"""
		This method is the deleter method for **self.__address** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "address"))

	@property
	def port(self):
		"""
		This method is the property for **self.__port** attribute.

		:return: self.__port. ( Integer )
		"""

		return self.__port

	@port.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def port(self, value):
		"""
		This method is the setter method for **self.__port** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format(
			"port", value)
			assert type(value) >= 0 and type(value) >= 65535, \
			"'{0}' attribute: '{1}' value must be in 0-65535 range!".format("port", value)
		self.__port = value

	@port.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def port(self):
		"""
		This method is the deleter method for **self.__port** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "port"))


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

		self.__preferencesManager = self.__engine.componentsManager["factory.preferencesManager"]

		self.__tcpServer = TCPServer(self.__address, self.__port, RequestsStackDataHandler)

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

		self.__preferencesManager = None

		self.__tcpServer.online and self.__tcpServer.stop()
		self.__tcpServer = None

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

		self.__Port_spinBox_setUi()
		self.__Autostart_TCP_Server_checkBox_setUi()

		# Signals / Slots.
		self.Port_spinBox.valueChanged.connect(self.__Port_spinBox__valueChanged)
		self.Autostart_TCP_Server_checkBox.stateChanged.connect(
		self.__Autostart_TCP_Server_checkBox__stateChanged)
		self.Start_TCP_Server_pushButton.clicked.connect(self.__Start_TCP_Server_pushButton__clicked)
		self.Stop_TCP_Server_pushButton.clicked.connect(self.__Stop_TCP_Server_pushButton__clicked)

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
		self.Port_spinBox.valueChanged.disconnect(self.__Port_spinBox__valueChanged)
		self.Autostart_TCP_Server_checkBox.stateChanged.disconnect(
		self.__Autostart_TCP_Server_checkBox__stateChanged)
		self.Start_TCP_Server_pushButton.clicked.disconnect(self.__Start_TCP_Server_pushButton__clicked)
		self.Stop_TCP_Server_pushButton.clicked.disconnect(self.__Stop_TCP_Server_pushButton__clicked)

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

		self.__preferencesManager.Others_Preferences_gridLayout.addWidget(self.TCP_Server_Ui_groupBox)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferencesManager.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self)
		self.TCP_Server_Ui_groupBox.setParent(None)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def onStartup(self):
		"""
		This method is triggered on Framework startup.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		if self.Autostart_TCP_Server_checkBox.isChecked():
			if not self.__tcpServer.online:
				self.__tcpServer.port = self.Port_spinBox.value()
				self.__tcpServer.start()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def onClose(self):
		"""
		This method is triggered on Framework close.
		"""

		self.__tcpServer.online and self.__tcpServer.stop()
		return True

	@core.executionTrace
	def __Port_spinBox_setUi(self):
		"""
		This method sets the **Port_spinBox** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey(self.__settingsSection, "port").isNull() and \
		self.__settings.setKey(self.__settingsSection, "port", self.__port)

		port = foundations.common.getFirstItem(self.__settings.getKey(self.__settingsSection, "port").toInt())
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Port_spinBox",
																port))
		self.Port_spinBox.setValue(port)
		self.__port = port

	@core.executionTrace
	def __Port_spinBox__valueChanged (self, value):
		"""
		This method is triggered when the **Port_spinBox** Widget value is changed.

		:param value: Port value. ( Integer )
		"""

		LOGGER.debug("> 'Port' value: '{0}'.".format(value))
		self.__settings.setKey(self.__settingsSection, "port", value)
		self.__port = value

	@core.executionTrace
	def __Autostart_TCP_Server_checkBox_setUi(self):
		"""
		This method sets the **Autostart_TCP_Server_checkBox** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey(self.__settingsSection, "autostartTcpServer").isNull() and \
		self.__settings.setKey(self.__settingsSection, "autostartTcpServer", Qt.Checked)

		autostartTcpServer = foundations.common.getFirstItem(
							self.__settings.getKey(self.__settingsSection, "autostartTcpServer").toInt())
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Autostart_TCP_Server_checkBox",
																autostartTcpServer))
		self.Autostart_TCP_Server_checkBox.setCheckState(autostartTcpServer)

	@core.executionTrace
	def __Autostart_TCP_Server_checkBox__stateChanged(self, state):
		"""
		This method is triggered when **Autostart_TCP_Server_checkBox** state changes.

		:param state: Checkbox state. ( Integer )
		"""

		autostartTcpServer = self.Autostart_TCP_Server_checkBox.checkState()
		LOGGER.debug("> 'Autostart TCP Server' state: '{0}'.".format(autostartTcpServer))
		self.__settings.setKey(self.__settingsSection, "autostartTcpServer", autostartTcpServer)

	@core.executionTrace
	def __Start_TCP_Server_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Start_TCP_Server_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.startTcpServer(self.Port_spinBox.value())

	@core.executionTrace
	def __Stop_TCP_Server_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Stop_TCP_Server_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.stopTcpServer()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def startTcpServer(self, port):
		"""
		This method starts the TCP server using given port.

		:param port: Port. ( Integer )
		:return: Method success. ( Boolean )
		"""

		self.__tcpServer.port = port
		if not self.__tcpServer.online:
			if self.__tcpServer.start():
				self.__engine.notificationsManager.notify(
				"{0} | TCP Server has started with '{1}' address on '{2}' port!".format(
																						self.__class__.__name__,
																						self.__address,
																						self.__port))
				return True
		else:
			self.__engine.notificationsManager.warnify(
			"{0} | TCP Server is already online!".format(self.__class__.__name__))
			return False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def stopTcpServer(self):
		"""
		This method stops the TCP server.

		:return: Method success. ( Boolean )
		"""

		if self.__tcpServer.online:
			if self.__tcpServer.stop():
				self.__engine.notificationsManager.notify(
				"{0} | TCP Server has stopped!".format(self.__class__.__name__))
				return True
		else:
			self.__engine.notificationsManager.warnify(
			"{0} | TCP Server is not online!".format(self.__class__.__name__))
			return False
