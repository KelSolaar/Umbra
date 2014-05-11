#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**tcp_serverUi.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`TCPServerUi` Component Interface class and others helper objects.

**Others:**

"""

from __future__ import unicode_literals

import os
import SocketServer
from PyQt4.QtGui import QGridLayout
from PyQt4.QtCore import Qt

import foundations.common
import foundations.data_structures
import foundations.exceptions
import foundations.verbose
from foundations.tcp_server import TCPServer
from manager.QWidget_component import QWidgetComponentFactory
from umbra.globals.runtime_globals import RuntimeGlobals

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "RequestsStackDataHandler", "TCPServerUi"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "TCP_Server_Ui.ui")

class RequestsStackDataHandler(SocketServer.BaseRequestHandler):
    """
    Defines the default requests handler.
    """

    codes = foundations.data_structures.Structure(request_end="<!RE>",
                                                server_shutdown="<!SS>")

    def handle(self):
        """
        Reimplements the :meth:`SocketServer.BaseRequestHandler.handle` method.

        :return: Method success.
        :rtype: bool
        """

        all_data = []
        while True:
            data = self.request.recv(1024)
            if not data:
                break

            if self.codes.server_shutdown in data:
                return self.__server_shutdown()

            if self.codes.request_end in data:
                all_data.append(data[:data.find(self.codes.request_end)])
                break

            all_data.append(data)
            if len(all_data) >= 2:
                tail = all_data[-2] + all_data[-1]

                if self.codes.server_shutdown in tail:
                    return self.__server_shutdown()

                if self.codes.request_end in tail:
                    all_data[-2] = tail[:tail.find(self.codes.request_end)]
                    all_data.pop()
                    break

        RuntimeGlobals.requests_stack.append("".join(all_data))
        return True

    def __server_shutdown(self):
        """
        Shutdowns the TCP Server.
        """

        return self.container.stop(terminate=True)

class TCPServerUi(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
    """
    | Defines the :mod:`umbra.components.factory.tcp_serverUi.tcp_serverUi` Component Interface class.
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
        self.__settings_section = None

        self.__preferences_manager = None

        self.__tcp_server = None
        self.__address = foundations.common.get_host_address()
        self.__port = 16384

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
    def tcp_server(self):
        """
        Property for **self.__tcp_server** attribute.

        :return: self.__tcp_server.
        :rtype: QWidget
        """

        return self.__tcp_server

    @tcp_server.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def tcp_server(self, value):
        """
        Setter for **self.__tcp_server** attribute.

        :param value: Attribute value.
        :type value: QWidget
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tcp_server"))

    @tcp_server.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def tcp_server(self):
        """
        Deleter for **self.__tcp_server** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tcp_server"))

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
        self.__port = value

    @port.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def port(self):
        """
        Deleter for **self.__port** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
        "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "port"))


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

        self.__tcp_server = TCPServer(self.__address, self.__port, RequestsStackDataHandler)

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

        self.__tcp_server.online and self.__tcp_server.stop()
        self.__tcp_server = None

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
        self.__Autostart_TCP_Server_checkBox_set_ui()

        # Signals / Slots.
        self.Port_spinBox.valueChanged.connect(self.__Port_spinBox__valueChanged)
        self.Autostart_TCP_Server_checkBox.stateChanged.connect(
        self.__Autostart_TCP_Server_checkBox__stateChanged)
        self.Start_TCP_Server_pushButton.clicked.connect(self.__Start_TCP_Server_pushButton__clicked)
        self.Stop_TCP_Server_pushButton.clicked.connect(self.__Stop_TCP_Server_pushButton__clicked)

        self.initialized_ui = True
        return True

    def uninitialize_ui(self):
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

        self.initialized_ui = False
        return True

    def add_widget(self):
        """
        Adds the Component Widget to the engine.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

        self.__preferences_manager.Others_Preferences_gridLayout.addWidget(self.TCP_Server_Ui_groupBox)

        return True

    def remove_widget(self):
        """
        Removes the Component Widget from the engine.

        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

        self.__preferences_manager.findChild(QGridLayout, "Others_Preferences_gridLayout").removeWidget(self)
        self.TCP_Server_Ui_groupBox.setParent(None)

        return True

    def on_startup(self):
        """
        Defines the slot triggered on Framework startup.
        """

        LOGGER.debug("> Calling '{0}' Component Framework 'on_startup' method.".format(self.__class__.__name__))

        if self.Autostart_TCP_Server_checkBox.isChecked():
            if not self.__tcp_server.online:
                self.__tcp_server.port = self.Port_spinBox.value()
                self.__tcp_server.start()
        return True

    def on_close(self):
        """
        Defines the slot triggered on Framework close.
        """

        self.__tcp_server.online and self.__tcp_server.stop()
        return True

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
        self.Port_spinBox.setValue(port)
        self.__port = port

    def __Port_spinBox__valueChanged (self, value):
        """
        Defines the slot triggered by the **Port_spinBox** Widget when value changed.

        :param value: Port value.
        :type value: int
        """

        LOGGER.debug("> 'Port' value: '{0}'.".format(value))
        self.__settings.set_key(self.__settings_section, "port", value)
        self.__port = value

    def __Autostart_TCP_Server_checkBox_set_ui(self):
        """
        Sets the **Autostart_TCP_Server_checkBox** Widget.
        """

        # Adding settings key if it doesn't exists.
        self.__settings.get_key(self.__settings_section, "autostart_tcp_server").isNull() and \
        self.__settings.set_key(self.__settings_section, "autostart_tcp_server", Qt.Checked)

        autostart_tcp_server = foundations.common.get_first_item(
                            self.__settings.get_key(self.__settings_section, "autostart_tcp_server").toInt())
        LOGGER.debug("> Setting '{0}' with value '{1}'.".format("Autostart_TCP_Server_checkBox",
                                                                autostart_tcp_server))
        self.Autostart_TCP_Server_checkBox.setCheckState(autostart_tcp_server)

    def __Autostart_TCP_Server_checkBox__stateChanged(self, state):
        """
        Defines the slot triggered by **Autostart_TCP_Server_checkBox** Widged when state changed.

        :param state: Checkbox state.
        :type state: int
        """

        autostart_tcp_server = self.Autostart_TCP_Server_checkBox.checkState()
        LOGGER.debug("> 'Autostart TCP Server' state: '{0}'.".format(autostart_tcp_server))
        self.__settings.set_key(self.__settings_section, "autostart_tcp_server", autostart_tcp_server)

    def __Start_TCP_Server_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Start_TCP_Server_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.start_tcp_server(self.Port_spinBox.value())

    def __Stop_TCP_Server_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Stop_TCP_Server_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        self.stop_tcp_server()

    def start_tcp_server(self, port):
        """
        Starts the TCP server using given port.

        :param port: Port.
        :type port: int
        :return: Method success.
        :rtype: bool
        """

        self.__tcp_server.port = port
        if not self.__tcp_server.online:
            if self.__tcp_server.start():
                self.__engine.notifications_manager.notify(
                "{0} | TCP Server has started with '{1}' address on '{2}' port!".format(
                                                                                        self.__class__.__name__,
                                                                                        self.__address,
                                                                                        self.__port))
                return True
        else:
            self.__engine.notifications_manager.warnify(
            "{0} | TCP Server is already online!".format(self.__class__.__name__))
            return False

    def stop_tcp_server(self):
        """
        Stops the TCP server.

        :return: Method success.
        :rtype: bool
        """

        if self.__tcp_server.online:
            if self.__tcp_server.stop():
                self.__engine.notifications_manager.notify(
                "{0} | TCP Server has stopped!".format(self.__class__.__name__))
                return True
        else:
            self.__engine.notifications_manager.warnify(
            "{0} | TCP Server is not online!".format(self.__class__.__name__))
            return False
