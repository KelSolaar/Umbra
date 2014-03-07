#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tcpClientUi.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`TCPClientUi` Component Interface class.

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
import socket
from PyQt4.QtCore import QChar
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QGridLayout

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.verbose
from manager.qwidgetComponent import QWidgetComponentFactory

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "TCPClientUi"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "TCP_Client_Ui.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class TCPClientUi(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	Defines the :mod:`umbra.components.factory.tcpClientUi.tcpClientUi` Component Interface class.
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

		super(TCPClientUi, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__preferencesManager = None
		self.__scriptEditor = None

		self.__address = foundations.common.getHostAddress()
		self.__port = 16384
		self.__fileCommand = "execfile(\"{0}\")"
		self.__connectionEnd = "<!RE>"

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
	def scriptEditor(self):
		"""
		Property for **self.__scriptEditor** attribute.

		:return: self.__scriptEditor.
		:rtype: QWidget
		"""

		return self.__scriptEditor

	@scriptEditor.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def scriptEditor(self, value):
		"""
		Setter for **self.__scriptEditor** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "scriptEditor"))

	@scriptEditor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def scriptEditor(self):
		"""
		Deleter for **self.__scriptEditor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "scriptEditor"))

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
			self.Address_lineEdit.setText(value)
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
			self.Port_spinBox.setValue(value)
		self.__port = value

	@port.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def port(self):
		"""
		Deleter for **self.__port** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "port"))

	@property
	def fileCommand(self):
		"""
		Property for **self.__fileCommand** attribute.

		:return: self.__fileCommand.
		:rtype: unicode
		"""

		return self.__fileCommand

	@fileCommand.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def fileCommand(self, value):
		"""
		Setter for **self.__fileCommand** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"fileCommand", value)
		self.__fileCommand = value

	@fileCommand.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def fileCommand(self):
		"""
		Deleter for **self.__fileCommand** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "fileCommand"))

	@property
	def connectionEnd(self):
		"""
		Property for **self.__connectionEnd** attribute.

		:return: self.__connectionEnd.
		:rtype: unicode
		"""

		return self.__connectionEnd

	@connectionEnd.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def connectionEnd(self, value):
		"""
		Setter for **self.__connectionEnd** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"connectionEnd", value)
		self.__connectionEnd = value

	@connectionEnd.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def connectionEnd(self):
		"""
		Deleter for **self.__connectionEnd** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "connectionEnd"))

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
		self.__scriptEditor = self.__engine.componentsManager["factory.scriptEditor"]

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
		self.__Address_lineEdit_setUi()
		self.__File_Command_lineEdit_setUi()
		self.__Connection_End_lineEdit_setUi()

		self.__addActions()

		# Signals / Slots.
		self.Port_spinBox.valueChanged.connect(self.__Port_spinBox__valueChanged)
		self.Address_lineEdit.editingFinished.connect(self.__Address_lineEdit__editFinished)
		self.File_Command_lineEdit.editingFinished.connect(self.__File_Command_lineEdit__editFinished)
		self.Connection_End_lineEdit.editingFinished.connect(self.__Connection_End_lineEdit__editFinished)

		self.initializedUi = True
		return True

	def uninitializeUi(self):
		"""
		Uninitializes the Component ui.
		
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__removeActions()

		# Signals / Slots.
		self.Port_spinBox.valueChanged.disconnect(self.__Port_spinBox__valueChanged)
		self.Address_lineEdit.editingFinished.disconnect(self.__Address_lineEdit__editFinished)
		self.File_Command_lineEdit.editingFinished.disconnect(self.__File_Command_lineEdit__editFinished)
		self.Connection_End_lineEdit.editingFinished.disconnect(self.__Connection_End_lineEdit__editFinished)

		self.initializedUi = False
		return True

	def addWidget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferencesManager.Others_Preferences_gridLayout.addWidget(self.TCP_Client_Ui_groupBox)

		return True

	def removeWidget(self):
		"""
		Removes the Component Widget from the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferencesManager.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self)
		self.TCP_Client_Ui_groupBox.setParent(None)

		return True

	def __addActions(self):
		"""
		Sets Component actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		self.__scriptEditor.commandMenu.addSeparator()
		self.__scriptEditor.commandMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|addons.tcpServerUi|&Command|Send Selection To Server",
		shortcut=Qt.ControlModifier + Qt.AltModifier + Qt.Key_Return,
		slot=self.__sendSelectionToServerAction__triggered))
		self.__scriptEditor.commandMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|addons.tcpServerUi|&Command|&Send Current File To Server",
		shortcut=Qt.SHIFT + Qt.AltModifier + Qt.CTRL + Qt.Key_Return,
		slot=self.__sendFileToServerAction__triggered))

	def __removeActions(self):
		"""
		Removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		sendSelectionToServerAction = "Actions|Umbra|Components|addons.tcpServerUi|&Command|Send Selection To Server"
		sendFileToServerAction = "Actions|Umbra|Components|addons.tcpServerUi|&Command|&Send Current File To Server"
		for action in (sendSelectionToServerAction, sendFileToServerAction):
			self.__scriptEditor.commandMenu.removeAction(self.__engine.actionsManager.getAction(action))
			self.__engine.actionsManager.unregisterAction(action)

	def __Address_lineEdit_setUi(self):
		"""
		Fills **Address_lineEdit** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey(self.__settingsSection, "address").isNull() and \
		self.__settings.setKey(self.__settingsSection, "address", self.__address)

		address = self.__settings.getKey(self.__settingsSection, "address").toString()
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Address_lineEdit",
																address))
		self.__address = address
		self.Address_lineEdit.setText(address)

	def __Address_lineEdit__editFinished(self):
		"""
		Defines the slot triggered by **Address_lineEdit** Widget when edited.
		"""

		address = self.Address_lineEdit.text()
		self.__settings.setKey(self.__settingsSection, "address", address)
		self.__address = address

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
		self.__port = port
		self.Port_spinBox.setValue(port)

	def __Port_spinBox__valueChanged (self, value):
		"""
		Defines the slot triggered by the **Port_spinBox** Widget when value changed.

		:param value: Port value.
		:type value: int
		"""

		LOGGER.debug("> 'Port' value: '{0}'.".format(value))
		self.__port = int(value)
		self.__settings.setKey(self.__settingsSection, "port", value)

	def __File_Command_lineEdit_setUi(self):
		"""
		Fills **File_Command_lineEdit** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey(self.__settingsSection, "fileCommand").isNull() and \
		self.__settings.setKey(self.__settingsSection, "fileCommand", self.__fileCommand)

		fileCommand = self.__settings.getKey(self.__settingsSection, "fileCommand").toString()
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("File_Command_lineEdit",
																fileCommand))
		self.__fileCommand = fileCommand
		self.File_Command_lineEdit.setText(fileCommand)

	def __File_Command_lineEdit__editFinished(self):
		"""
		Defines the slot triggered by **File_Command_lineEdit** Widget when edited.
		"""

		fileCommand = self.File_Command_lineEdit.text()
		self.__settings.setKey(self.__settingsSection, "fileCommand", fileCommand)
		self.__fileCommand = fileCommand

	def __Connection_End_lineEdit_setUi(self):
		"""
		Fills **Connection_End_lineEdit** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey(self.__settingsSection, "connectionEnd").isNull() and \
		self.__settings.setKey(self.__settingsSection, "connectionEnd", self.__connectionEnd)

		connectionEnd = self.__settings.getKey(self.__settingsSection, "connectionEnd").toString()
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Connection_End_lineEdit",
																connectionEnd))
		self.__connectionEnd = connectionEnd
		self.Connection_End_lineEdit.setText(connectionEnd)

	def __Connection_End_lineEdit__editFinished(self):
		"""
		Defines the slot triggered by **Connection_End_lineEdit** Widget when edited.
		"""

		connectionEnd = self.Connection_End_lineEdit.text()
		self.__settings.setKey(self.__settingsSection, "connectionEnd", connectionEnd)
		self.__connectionEnd = connectionEnd

	def __sendSelectionToServerAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|addons.tcpServerUi|&Command|Send Selection To Server'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		editor = self.__scriptEditor.getCurrentEditor()
		if not editor:
			return False

		selectedText = foundations.strings.toString(editor.getSelectedText().replace(QChar(QChar.ParagraphSeparator),
																			QString("\n")))
		if not selectedText:
			return False

		return self.sendDataToServer(selectedText)

	def __sendFileToServerAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|addons.tcpServerUi|&Command|&Send Current File To Server'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		editor = self.__scriptEditor.getCurrentEditor()
		if not editor:
			return False

		if self.__scriptEditor.saveFile():
			return self.sendDataToServer(foundations.strings.toString(self.__fileCommand).format(editor.file))

	def sendDataToServer(self, data, timeOut=5):
		"""
		Sends given data to the Server.

		:param data: Data to send.
		:type data: unicode
		:param timeOut: Connection timeout in seconds.
		:type timeOut: float
		:return: Method success.
		:rtype: bool
		"""

		if not data.endswith(self.__connectionEnd):
			data = "{0}{1}".format(data, foundations.strings.toString(self.__connectionEnd).decode("string_escape"))

		connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connection.settimeout(timeOut)
		connection.connect((foundations.strings.toString(self.__address), int(self.__port)))
		connection.send(data)
		self.__engine.notificationsManager.notify(
		"{0} | Socket connection command dispatched!".format(self.__class__.__name__))
		connection.close()
		return True
