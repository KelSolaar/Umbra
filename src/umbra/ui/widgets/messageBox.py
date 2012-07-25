#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**messageBox.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :func:`messageBox` and :func:`standaloneMessageBox` functions.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextEdit

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.ui.common
from umbra.globals.runtimeGlobals import RuntimeGlobals
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

__all__ = ["LOGGER", "messageBox"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
@core.executionTrace
def messageBox(type, title, message, icon=None, buttons=QMessageBox.Ok, customButtons=None):
	"""
	This definition provides a fast GUI message box.

	:param title: Current message title. ( String )
	:param message: Message. ( String )
	:param icon: Custom icon. ( QConstant )
	:param buttons: Standard buttons. ( QConstant )
	:param customButtons: Custom buttons. ( Tuple / List )
	:return: User choice. ( Integer )
	"""

	LOGGER.debug("> Launching messagebox().")
	LOGGER.debug("> Message type: '{0}'.".format(type))
	LOGGER.debug("> Title: '{0}'.".format(title))
	LOGGER.debug("> Message: '{0}'.".format(message))

	messageBox = QMessageBox()
	messageBox.setWindowTitle("{0} | {1}".format(Constants.applicationName, title))
	messageBox.setText(message)

	for button, role in customButtons or ():
		messageBox.addButton(button, role)

	message = message.split("\n")
	if type == "Critical":
		if icon:
			messageBox.setIcon(icon)
		else:
			messageBox.setIcon(QMessageBox.Critical)
		for line in message:
			LOGGER.critical("!> {0}".format(line))
	elif type == "Error":
		if icon:
			messageBox.setIcon(icon)
		else:
			messageBox.setIcon(QMessageBox.Critical)
		for line in message:
			LOGGER.error("!> {0}".format(line))
	elif type == "Detailed Error":
		if icon:
			messageBox.setIcon(icon)
		else:
			messageBox.setIcon(QMessageBox.Critical)
		RuntimeGlobals.loggingSessionHandlerStream and \
		messageBox.setDetailedText("".join(RuntimeGlobals.loggingSessionHandlerStream.stream))
		textEdit = messageBox.findChild(QTextEdit)
		if textEdit:
			textEdit.setCurrentFont(QFont("Courier"))
			textEdit.setLineWrapMode(QTextEdit.NoWrap)
			textEdit.moveCursor(QTextCursor.End)
			textEdit.ensureCursorVisible()
		for line in message:
			LOGGER.error("!> {0}".format(line))
	elif type == "Warning":
		if icon:
			messageBox.setIcon(icon)
		else:
			messageBox.setIcon(QMessageBox.Warning)
		for line in message:
			LOGGER.warning("{0}".format(line))
	elif type == "Information":
		if icon:
			messageBox.setIcon(icon)
		else:
			messageBox.setIcon(QMessageBox.Information)
		for line in message:
			LOGGER.info("{0}".format(line))
	elif type == "Question":
		if icon:
			messageBox.setIcon(icon)
		else:
			messageBox.setIcon(QMessageBox.Question)
		for line in message:
			LOGGER.info("{0}".format(line))

	messageBox.setStandardButtons(buttons)
	messageBox.setWindowFlags(Qt.WindowStaysOnTopHint)
	messageBox.show()
	foundations.ui.common.centerWidgetOnScreen(messageBox)
	return messageBox.exec_()
