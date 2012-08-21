#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tcpClientUi.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`TCPClientUi` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
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
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.globals.constants import Constants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "TCPClientUi"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "TCP_Client_Ui.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class TCPClientUi(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	This class is the :mod:`umbra.components.factory.tcpClientUi.tcpClientUi` Component Interface class.
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

		super(TCPClientUi, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = True

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__factoryPreferencesManager = None
		self.__factoryScriptEditor = None

		self.__address = socket.gethostbyname(socket.gethostname())
		self.__port = 16384
		self.__connectionEndToken = "<!RE>"

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
	def factoryPreferencesManager(self):
		"""
		This method is the property for **self.__factoryPreferencesManager** attribute.

		:return: self.__factoryPreferencesManager. ( QWidget )
		"""

		return self.__factoryPreferencesManager

	@factoryPreferencesManager.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryPreferencesManager(self, value):
		"""
		This method is the setter method for **self.__factoryPreferencesManager** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factoryPreferencesManager"))

	@factoryPreferencesManager.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryPreferencesManager(self):
		"""
		This method is the deleter method for **self.__factoryPreferencesManager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factoryPreferencesManager"))

	@property
	def factoryScriptEditor(self):
		"""
		This method is the property for **self.__factoryScriptEditor** attribute.

		:return: self.__factoryScriptEditor. ( QWidget )
		"""

		return self.__factoryScriptEditor

	@factoryScriptEditor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryScriptEditor(self, value):
		"""
		This method is the setter method for **self.__factoryScriptEditor** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factoryScriptEditor"))

	@factoryScriptEditor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryScriptEditor(self):
		"""
		This method is the deleter method for **self.__factoryScriptEditor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factoryScriptEditor"))

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

	@property
	def connectionEndToken(self):
		"""
		This method is the property for **self.__connectionEndToken** attribute.

		:return: self.__connectionEndToken. ( String )
		"""

		return self.__connectionEndToken

	@connectionEndToken.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def connectionEndToken(self, value):
		"""
		This method is the setter method for **self.__connectionEndToken** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"connectionEndToken", value)
		self.__connectionEndToken = value

	@connectionEndToken.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def connectionEndToken(self):
		"""
		This method is the deleter method for **self.__connectionEndToken** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "connectionEndToken"))

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

		self.__factoryPreferencesManager = self.__engine.componentsManager.components[
											"factory.preferencesManager"].interface
		self.__factoryScriptEditor = self.__engine.componentsManager.components["factory.scriptEditor"].interface

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

		self.__factoryPreferencesManager = None

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
		self.__Address_lineEdit_setUi()
		self.__Connection_End_Token_lineEdit_setUi()

		self.__addActions()

		# Signals / Slots.
		self.Port_spinBox.valueChanged.connect(self.__Port_spinBox__valueChanged)
		self.Address_lineEdit.editingFinished.connect(self.__Address_lineEdit__editFinished)
		self.Connection_End_Token_lineEdit.editingFinished.connect(self.__Connection_End_Token_lineEdit__editFinished)

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

		self.__removeActions()

		# Signals / Slots.
		self.Port_spinBox.valueChanged.disconnect(self.__Port_spinBox__valueChanged)
		self.Address_lineEdit.editingFinished.disconnect(self.__Address_lineEdit__editFinished)
		self.Connection_End_Token_lineEdit.editingFinished.disconnect(self.__Connection_End_Token_lineEdit__editFinished)

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

		self.__factoryPreferencesManager.Others_Preferences_gridLayout.addWidget(self.TCP_Client_Ui_groupBox)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )		
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__factoryPreferencesManager.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self)
		self.TCP_Client_Ui_groupBox.setParent(None)

		return True

	@core.executionTrace
	def __addActions(self):
		"""
		This method sets Component actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		self.__factoryScriptEditor.commandMenu.addSeparator()
		self.__factoryScriptEditor.commandMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|addins.tcpServerUi|&Command|Send Selection To Server",
		shortcut=Qt.ControlModifier + Qt.AltModifier + Qt.Key_Return,
		slot=self.__sendSelectionToServerAction__triggered))
		self.__factoryScriptEditor.commandMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|addins.tcpServerUi|&Command|&Send Current File To Server",
		shortcut=Qt.SHIFT + Qt.AltModifier + Qt.CTRL + Qt.Key_Return,
		slot=self.__sendFileToServerAction__triggered))

	@core.executionTrace
	def __removeActions(self):
		"""
		This method removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		sendSelectionToServerAction = "Actions|Umbra|Components|addins.tcpServerUi|&Command|Send Selection To Server"
		sendFileToServerAction = "Actions|Umbra|Components|addins.tcpServerUi|&Command|&Send Current File To Server"
		for action in (sendSelectionToServerAction, sendFileToServerAction):
			self.__factoryScriptEditor.commandMenu.removeAction(self.__engine.actionsManager.getAction(action))
			self.__engine.actionsManager.unregisterAction(action)

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
	def __Address_lineEdit_setUi(self):
		"""
		This method fills **Address_lineEdit** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey(self.__settingsSection, "address").isNull() and \
		self.__settings.setKey(self.__settingsSection, "address", self.__address)

		address = self.__settings.getKey(self.__settingsSection, "address").toString()
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Address_lineEdit",
																address))
		self.Address_lineEdit.setText(address)

	@core.executionTrace
	def __Address_lineEdit__editFinished(self):
		"""
		This method is triggered when **Address_lineEdit** Widget is edited.
		"""

		self.__settings.setKey(self.__settingsSection, "address", self.Address_lineEdit.text())

	@core.executionTrace
	def __Connection_End_Token_lineEdit_setUi(self):
		"""
		This method fills **Connection_End_Token_lineEdit** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.getKey(self.__settingsSection, "connectionEndToken").isNull() and \
		self.__settings.setKey(self.__settingsSection, "connectionEndToken", self.__connectionEndToken)

		connectionEndToken = self.__settings.getKey(self.__settingsSection, "connectionEndToken").toString()
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Connection_End_Token_lineEdit",
																connectionEndToken))
		self.Connection_End_Token_lineEdit.setText(connectionEndToken)

	@core.executionTrace
	def __Connection_End_Token_lineEdit__editFinished(self):
		"""
		This method is triggered when **Connection_End_Token_lineEdit** Widget is edited.
		"""

		self.__settings.setKey(self.__settingsSection, "connectionEndToken", self.Connection_End_Token_lineEdit.text())

	@core.executionTrace
	def __sendSelectionToServerAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|addins.tcpServerUi|&Command|Send Selection To Server'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		editor = self.__factoryScriptEditor.getCurrentEditor()
		if not editor:
			return

		selectedText = strings.encode(editor.getSelectedText().replace(QChar(QChar.ParagraphSeparator),
																			QString("\n")))
		if not selectedText:
			return

		return self.sendDataToServer(selectedText)

	@core.executionTrace
	def __sendFileToServerAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|addins.tcpServerUi|&Command|&Send Current File To Server'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		editor = self.__factoryScriptEditor.getCurrentEditor()
		if not editor:
			return

		if self.__factoryScriptEditor.saveFile():
			return self.sendDataToServer("execfile(\"{0}\", {{}}, {{}})".format(editor.file))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def sendDataToServer(self, data):
		"""
		This method sends given data to the Server.

		:return: Method success. ( Boolean )
		"""

		if not data.endswith(self.__connectionEndToken):
			data = "{0}{1}".format(data, self.__connectionEndToken)

		connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connection.connect((self.__address, self.__port))
		connection.send(data)
		connection.close()
		return True
