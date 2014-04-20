#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tcp_client_ui.py**

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
from manager.QWidget_component import QWidgetComponentFactory

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

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "TCP_Client_Ui.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class TCPClientUi(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
	"""
	Defines the :mod:`umbra.components.factory.tcp_client_ui.tcp_client_ui` Component Interface class.
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
		self.__settings_section = None

		self.__preferences_manager = None
		self.__script_editor = None

		self.__address = foundations.common.get_host_address()
		self.__port = 16384
		self.__file_command = "execfile(\"{0}\")"
		self.__connection_end = "<!RE>"

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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		Setter for **self.__engine** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		Setter for **self.__settings** attribute.

		:param value: Attribute value.
		:type value: QSettings
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		Deleter for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def settings_section(self):
		"""
		Property for **self.__settings_section** attribute.

		:return: self.__settings_section.
		:rtype: unicode
		"""

		return self.__settings_section

	@settings_section.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings_section(self, value):
		"""
		Setter for **self.__settings_section** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings_section"))

	@settings_section.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings_section(self):
		"""
		Deleter for **self.__settings_section** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings_section"))

	@property
	def preferences_manager(self):
		"""
		Property for **self.__preferences_manager** attribute.

		:return: self.__preferences_manager.
		:rtype: QWidget
		"""

		return self.__preferences_manager

	@preferences_manager.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def preferences_manager(self, value):
		"""
		Setter for **self.__preferences_manager** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "preferences_manager"))

	@preferences_manager.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def preferences_manager(self):
		"""
		Deleter for **self.__preferences_manager** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "preferences_manager"))

	@property
	def script_editor(self):
		"""
		Property for **self.__script_editor** attribute.

		:return: self.__script_editor.
		:rtype: QWidget
		"""

		return self.__script_editor

	@script_editor.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def script_editor(self, value):
		"""
		Setter for **self.__script_editor** attribute.

		:param value: Attribute value.
		:type value: QWidget
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "script_editor"))

	@script_editor.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def script_editor(self):
		"""
		Deleter for **self.__script_editor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "script_editor"))

	@property
	def address(self):
		"""
		Property for **self.__address** attribute.

		:return: self.__address.
		:rtype: unicode
		"""

		return self.__address

	@address.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def port(self):
		"""
		Deleter for **self.__port** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "port"))

	@property
	def file_command(self):
		"""
		Property for **self.__file_command** attribute.

		:return: self.__file_command.
		:rtype: unicode
		"""

		return self.__file_command

	@file_command.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def file_command(self, value):
		"""
		Setter for **self.__file_command** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"file_command", value)
		self.__file_command = value

	@file_command.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def file_command(self):
		"""
		Deleter for **self.__file_command** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "file_command"))

	@property
	def connection_end(self):
		"""
		Property for **self.__connection_end** attribute.

		:return: self.__connection_end.
		:rtype: unicode
		"""

		return self.__connection_end

	@connection_end.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def connection_end(self, value):
		"""
		Setter for **self.__connection_end** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"connection_end", value)
		self.__connection_end = value

	@connection_end.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def connection_end(self):
		"""
		Deleter for **self.__connection_end** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "connection_end"))

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
		self.__settings_section = self.name

		self.__preferences_manager = self.__engine.components_manager["factory.preferences_manager"]
		self.__script_editor = self.__engine.components_manager["factory.script_editor"]

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
		self.__settings_section = None

		self.__preferences_manager = None

		self.activated = False
		return True

	def initialize_ui(self):
		"""
		Initializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__Port_spinBox_set_ui()
		self.__Address_lineEdit_set_ui()
		self.__File_Command_lineEdit_set_ui()
		self.__Connection_End_lineEdit_set_ui()

		self.__add_actions()

		# Signals / Slots.
		self.Port_spinBox.valueChanged.connect(self.__Port_spinBox__valueChanged)
		self.Address_lineEdit.editingFinished.connect(self.__Address_lineEdit__editFinished)
		self.File_Command_lineEdit.editingFinished.connect(self.__File_Command_lineEdit__editFinished)
		self.Connection_End_lineEdit.editingFinished.connect(self.__Connection_End_lineEdit__editFinished)

		self.initialized_ui = True
		return True

	def uninitialize_ui(self):
		"""
		Uninitializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Uninitializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__remove_actions()

		# Signals / Slots.
		self.Port_spinBox.valueChanged.disconnect(self.__Port_spinBox__valueChanged)
		self.Address_lineEdit.editingFinished.disconnect(self.__Address_lineEdit__editFinished)
		self.File_Command_lineEdit.editingFinished.disconnect(self.__File_Command_lineEdit__editFinished)
		self.Connection_End_lineEdit.editingFinished.disconnect(self.__Connection_End_lineEdit__editFinished)

		self.initialized_ui = False
		return True

	def add_widget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferences_manager.Others_Preferences_gridLayout.addWidget(self.TCP_Client_Ui_groupBox)

		return True

	def remove_widget(self):
		"""
		Removes the Component Widget from the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__preferences_manager.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self)
		self.TCP_Client_Ui_groupBox.setParent(None)

		return True

	def __add_actions(self):
		"""
		Sets Component actions.
		"""

		LOGGER.debug("> Adding '{0}' Component actions.".format(self.__class__.__name__))

		self.__script_editor.command_menu.addSeparator()
		self.__script_editor.command_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|addons.tcp_serverUi|&Command|Send Selection To Server",
		shortcut=Qt.ControlModifier + Qt.AltModifier + Qt.Key_Return,
		slot=self.__send_selection_to_server_action__triggered))
		self.__script_editor.command_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|addons.tcp_serverUi|&Command|&Send Current File To Server",
		shortcut=Qt.SHIFT + Qt.AltModifier + Qt.CTRL + Qt.Key_Return,
		slot=self.__send_file_to_server_action__triggered))

	def __remove_actions(self):
		"""
		Removes actions.
		"""

		LOGGER.debug("> Removing '{0}' Component actions.".format(self.__class__.__name__))

		send_selection_to_server_action = "Actions|Umbra|Components|addons.tcp_serverUi|&Command|Send Selection To Server"
		send_file_to_server_action = "Actions|Umbra|Components|addons.tcp_serverUi|&Command|&Send Current File To Server"
		for action in (send_selection_to_server_action, send_file_to_server_action):
			self.__script_editor.command_menu.removeAction(self.__engine.actions_manager.get_action(action))
			self.__engine.actions_manager.unregister_action(action)

	def __Address_lineEdit_set_ui(self):
		"""
		Fills **Address_lineEdit** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.get_key(self.__settings_section, "address").isNull() and \
		self.__settings.set_key(self.__settings_section, "address", self.__address)

		address = self.__settings.get_key(self.__settings_section, "address").toString()
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Address_lineEdit",
																address))
		self.__address = address
		self.Address_lineEdit.setText(address)

	def __Address_lineEdit__editFinished(self):
		"""
		Defines the slot triggered by **Address_lineEdit** Widget when edited.
		"""

		address = self.Address_lineEdit.text()
		self.__settings.set_key(self.__settings_section, "address", address)
		self.__address = address

	def __Port_spinBox_set_ui(self):
		"""
		Sets the **Port_spinBox** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.get_key(self.__settings_section, "port").isNull() and \
		self.__settings.set_key(self.__settings_section, "port", self.__port)

		port = foundations.common.get_first_item(self.__settings.get_key(self.__settings_section, "port").toInt())
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
		self.__settings.set_key(self.__settings_section, "port", value)

	def __File_Command_lineEdit_set_ui(self):
		"""
		Fills **File_Command_lineEdit** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.get_key(self.__settings_section, "file_command").isNull() and \
		self.__settings.set_key(self.__settings_section, "file_command", self.__file_command)

		file_command = self.__settings.get_key(self.__settings_section, "file_command").toString()
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("File_Command_lineEdit",
																file_command))
		self.__file_command = file_command
		self.File_Command_lineEdit.setText(file_command)

	def __File_Command_lineEdit__editFinished(self):
		"""
		Defines the slot triggered by **File_Command_lineEdit** Widget when edited.
		"""

		file_command = self.File_Command_lineEdit.text()
		self.__settings.set_key(self.__settings_section, "file_command", file_command)
		self.__file_command = file_command

	def __Connection_End_lineEdit_set_ui(self):
		"""
		Fills **Connection_End_lineEdit** Widget.
		"""

		# Adding settings key if it doesn't exists.
		self.__settings.get_key(self.__settings_section, "connection_end").isNull() and \
		self.__settings.set_key(self.__settings_section, "connection_end", self.__connection_end)

		connection_end = self.__settings.get_key(self.__settings_section, "connection_end").toString()
		LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Connection_End_lineEdit",
																connection_end))
		self.__connection_end = connection_end
		self.Connection_End_lineEdit.setText(connection_end)

	def __Connection_End_lineEdit__editFinished(self):
		"""
		Defines the slot triggered by **Connection_End_lineEdit** Widget when edited.
		"""

		connection_end = self.Connection_End_lineEdit.text()
		self.__settings.set_key(self.__settings_section, "connection_end", connection_end)
		self.__connection_end = connection_end

	def __send_selection_to_server_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|addons.tcp_serverUi|&Command|Send Selection To Server'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		editor = self.__script_editor.get_current_editor()
		if not editor:
			return False

		selected_text = foundations.strings.to_string(editor.get_selected_text().replace(QChar(QChar.ParagraphSeparator),
																			QString("\n")))
		if not selected_text:
			return False

		return self.send_data_to_server(selected_text)

	def __send_file_to_server_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|addons.tcp_serverUi|&Command|&Send Current File To Server'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		editor = self.__script_editor.get_current_editor()
		if not editor:
			return False

		if self.__script_editor.save_file():
			return self.send_data_to_server(foundations.strings.to_string(self.__file_command).format(editor.file))

	def send_data_to_server(self, data, time_out=5):
		"""
		Sends given data to the Server.

		:param data: Data to send.
		:type data: unicode
		:param time_out: Connection timeout in seconds.
		:type time_out: float
		:return: Method success.
		:rtype: bool
		"""

		if not data.endswith(self.__connection_end):
			data = "{0}{1}".format(data, foundations.strings.to_string(self.__connection_end).decode("string_escape"))

		connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connection.settimeout(time_out)
		connection.connect((foundations.strings.to_string(self.__address), int(self.__port)))
		connection.send(data)
		self.__engine.notifications_manager.notify(
		"{0} | Socket connection command dispatched!".format(self.__class__.__name__))
		connection.close()
		return True
