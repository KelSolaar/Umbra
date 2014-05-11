#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**message_box.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :func:`message_box` and :func:`standaloneMessageBox` functions.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextEdit

import foundations.ui.common
import foundations.verbose
import umbra.ui.common
from umbra.globals.runtime_globals import RuntimeGlobals
from umbra.globals.constants import Constants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "message_box"]

LOGGER = foundations.verbose.install_logger()


def message_box(type, title, message, icon=None, buttons=QMessageBox.Ok, custom_buttons=None):
    """
    Provides a fast GUI message box.

    :param title: Current message title.
    :type title: unicode
    :param message: Message.
    :type message: unicode
    :param icon: Custom icon.
    :type icon: QConstant
    :param buttons: Standard buttons.
    :type buttons: QConstant
    :param custom_buttons: Custom buttons.
    :type custom_buttons: tuple or list
    :return: User choice.
    :rtype: int
    """

    LOGGER.debug("> Launching messagebox().")
    LOGGER.debug("> Message type: '{0}'.".format(type))
    LOGGER.debug("> Title: '{0}'.".format(title))
    LOGGER.debug("> Message: '{0}'.".format(message))

    message_box = QMessageBox()
    message_box.setWindowTitle("{0} | {1}".format(Constants.application_name, title))
    message_box.setText(message)

    for button, role in custom_buttons or ():
        message_box.addButton(button, role)
    umbra.ui.common.set_children_padding(message_box, (QPushButton,), width=12)

    message = message.split("\n")
    if type == "Critical":
        if icon:
            message_box.setIcon(icon)
        else:
            message_box.setIcon(QMessageBox.Critical)
        for line in message:
            LOGGER.critical("!> {0}".format(line))
    elif type == "Error":
        if icon:
            message_box.setIcon(icon)
        else:
            message_box.setIcon(QMessageBox.Critical)
        for line in message:
            LOGGER.error("!> {0}".format(line))
    elif type == "Detailed Error":
        if icon:
            message_box.setIcon(icon)
        else:
            message_box.setIcon(QMessageBox.Critical)
        RuntimeGlobals.logging_session_handler_stream and \
        message_box.setDetailedText("".join(RuntimeGlobals.logging_session_handler_stream.stream))
        text_edit = message_box.findChild(QTextEdit)
        if text_edit:
            text_edit.setCurrentFont(QFont("Courier"))
            text_edit.setLineWrapMode(QTextEdit.NoWrap)
            text_edit.moveCursor(QTextCursor.End)
            text_edit.ensureCursorVisible()
        for line in message:
            LOGGER.error("!> {0}".format(line))
    elif type == "Warning":
        if icon:
            message_box.setIcon(icon)
        else:
            message_box.setIcon(QMessageBox.Warning)
        for line in message:
            LOGGER.warning("{0}".format(line))
    elif type == "Information":
        if icon:
            message_box.setIcon(icon)
        else:
            message_box.setIcon(QMessageBox.Information)
        for line in message:
            LOGGER.info("{0}".format(line))
    elif type == "Question":
        if icon:
            message_box.setIcon(icon)
        else:
            message_box.setIcon(QMessageBox.Question)
        for line in message:
            LOGGER.info("{0}".format(line))

    message_box.setStandardButtons(buttons)
    message_box.setWindowFlags(Qt.WindowStaysOnTopHint)
    message_box.show()
    foundations.ui.common.center_widget_on_screen(message_box)
    return message_box.exec_()


if __name__ == "__main__":
    import sys
    from PyQt4.QtCore import QString

    application = umbra.ui.common.get_application_instance()

    message_box("Critical", "Critical", "This is a 'Critical' QMessageBox!")
    message_box("Error", "Error", "This is an 'Error' QMessageBox!")
    message_box("Warning", "Warning", "This is a 'Warning' QMessageBox!")
    message_box("Information", "Information", "This is an 'Information' QMessageBox!")
    message_box("Question", "Question", "This is a 'Question' QMessageBox!")
    message_box("Information", "Information", "This QMessageBox is using a custom button!",
                custom_buttons=((QString("Custom"), QMessageBox.RejectRole),))

    sys.exit(application.exec_())
