#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tcpServerUi.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`TCPServerUi` Component Interface class and others helper objects.

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
import SocketServer
from PyQt4.QtGui import QGridLayout
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.dataStructures
import foundations.exceptions
import foundations.verbose
from foundations.tcpServer import TCPServer
from manager.qwidgetComponent import QWidgetComponentFactory
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

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "RequestsStackDataHandler", "TCPServerUi"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "TCP_Server_Ui.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class RequestsStackDataHandler(SocketServer.BaseRequestHandler):
	"""
	Defines the default requests handler.
	"""

	codes = foundations.dataStructures.Structure(requestEnd="<!RE>",
												serverShutdown="<!SS>")

	def handle(self):
		"""
		Reimplements the :meth:`SocketServer.BaseRequestHandler.handle` method.
	
		:return: Method success.
		:rtype: bool
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
		Shutdowns the TCP Server.
		"""

		return self.container.stop(terminate=True)

class TCPServerUi(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	| Defines the :mod:`umbra.components.factory.tcpServerUi.tcpServerUi` Component Interface class.
	| It provides various methods to operate the TCP Server.
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

		super(TCPServerUi, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__preferencesManager = None

		self.__tcpServer = None
		self.__address = foundations.common.getHostAddress()
		self.__port = 16384

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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
	def preferencesManager(self):
		"""
		Property for **self.__preferencesManager** attribute.

		:return: self.__preferencesManager.
		:rtype: QWidget
		"""

		return self.__preferencesManager

	@preferencesManager.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def preferencesManager(self, value):
		"""
		Setter for **self.__preferencesManager** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "preferencesManager"))

	@preferencesManager.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def preferencesManager(self):
		"""
		Deleter for **self.__preferencesManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "preferencesManager"))

	@property
	def tcpServer(self):
		"""
		Property for **self.__tcpServer** attribute.

		:return: self.__tcpServer.
		:rtype: QWidget
		"""

		return self.__tcpServer

	@tcpServer.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def tcpServer(self, value):
		"""
		Setter for **self.__tcpServer** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tcpServer"))

	@tcpServer.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def tcpServer(self):
		"""
		Deleter for **self.__tcpServer** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tcpServer"))

	@property
	def address(self):
		"""
		Property for **self.__address** attribute.

		:return: self.__address.
		:rtype: unicode
		"""

		return self.__address

	@address.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def address(self, value):
		"""
		Setter for **self.__address** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"address", value)
		self.__address = value

	@address.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def address(self):
		"""
		Deleter for **self.__address** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "address"))

	@property
	def port(self):
		"""
		Property for **self.__port** attribute.

		:return: self.__port.
		:rtype: int
		"""

		return self.__port

	@port.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def port(self, value):
		"""
		Setter for **self.__port** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format(
			"port", value)
			assert type(value) >= 0 and type(value) >= 65535, \
			"'{0}' attribute: '{1}' value must be in 0-65535 range!".format("port", value)
		self.__port = value

	@port.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def port(self):
		"""
		Deleter for **self.__port** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "port"))


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

		self.__preferencesManager = self.__engine.componentsManager["factory.preferencesManager"]

		self.__tcpServer = TCPServer(self.__address, self.__port, RequestsStackDataHandler)

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

		self.__preferencesManager = None

		self.__tcpServer.online and self.__tcpServer.stop()
		self.__tcpServer = None

		self.activated = False
		return True

	def initializeUi(self):
		"""
		Initializes the Component ui.
		
		:return: Method success.
		:rtype: bool
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

	def uninitializeUi(self):
		"""
		Uninitializes the Component ui.
		
		:return: Method success.
		:rtype: bool
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

	def addWidget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferencesManager.Others_Preferences_gridLayout.addWidget(self.TCP_Server_Ui_groupBox)

		return True

	def removeWidget(self):
		"""
		Removes the Component Widget from the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferencesManager.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self)
		self.TCP_Server_Ui_groupBox.setParent(None)

		return True

	def onStartup(self):
		"""
		Defines the slot triggered on Framework startup.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		if self.Autostart_TCP_Server_checkBox.isChecked():
			if not self.__tcpServer.online:
				self.__tcpServer.port = self.Port_spinBox.value()
				self.__tcpServer.start()
		return True

	def onClose(self):
		"""
		Defines the slot triggered on Framework close.
		"""

		self.__tcpServer.online and self.__tcpServer.stop()
		return True

	def __Port_spinBox_setUi(self):
		"""
		Sets the **Port_spinBox** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey(self.__settingsSection, "port").isNull() and \
		self.__settings.setKey(self.__settingsSection, "port", self.__port)

		port = foundations.common.getFirstItem(self.__settings.getKey(self.__settingsSection, "port").toInt())
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Port_spinBox",
																port))
		self.Port_spinBox.setValue(port)
		self.__port = port

	def __Port_spinBox__valueChanged (self, value):
		"""
		Defines the slot triggered by the **Port_spinBox** Widget when value changed.

		:param value: Port value.
		:type value: int
		"""

		LOGGER.debug("> 'Port' value: '{0}'.".format(value))
		self.__settings.setKey(self.__settingsSection, "port", value)
		self.__port = value

	def __Autostart_TCP_Server_checkBox_setUi(self):
		"""
		Sets the **Autostart_TCP_Server_checkBox** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey(self.__settingsSection, "autostartTcpServer").isNull() and \
		self.__settings.setKey(self.__settingsSection, "autostartTcpServer", Qt.Checked)

		autostartTcpServer = foundations.common.getFirstItem(
							self.__settings.getKey(self.__settingsSection, "autostartTcpServer").toInt())
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Autostart_TCP_Server_checkBox",
																autostartTcpServer))
		self.Autostart_TCP_Server_checkBox.setCheckState(autostartTcpServer)

	def __Autostart_TCP_Server_checkBox__stateChanged(self, state):
		"""
		Defines the slot triggered by **Autostart_TCP_Server_checkBox** Widged when state changed.

		:param state: Checkbox state.
		:type state: int
		"""

		autostartTcpServer = self.Autostart_TCP_Server_checkBox.checkState()
		LOGGER.debug("> 'Autostart TCP Server' state: '{0}'.".format(autostartTcpServer))
		self.__settings.setKey(self.__settingsSection, "autostartTcpServer", autostartTcpServer)

	def __Start_TCP_Server_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Start_TCP_Server_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.startTcpServer(self.Port_spinBox.value())

	def __Stop_TCP_Server_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Stop_TCP_Server_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.stopTcpServer()

	def startTcpServer(self, port):
		"""
		Starts the TCP server using given port.

		:param port: Port.
		:type port: int
		:return: Method success.
		:rtype: bool
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

	def stopTcpServer(self):
		"""
		Stops the TCP server.

		:return: Method success.
		:rtype: bool
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
