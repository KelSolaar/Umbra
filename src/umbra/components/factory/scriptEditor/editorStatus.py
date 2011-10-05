#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**editorStatus.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`EditorStatus` class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import logging
import os
import sys
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "EditorStatus"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class EditorStatus(QObject):
	"""
	This class defines the **ScriptEditor** Component status bar widget. 
	"""

	@core.executionTrace
	def __init__(self, parent):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QObject.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__container = parent

		self.__Lines_Columns_label_defaultText = "Line {0} : Column {1}"

		self.__uiPath = "ui/Editor_Status.ui"
		self.__uiPath = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)

		self.__ui = uic.loadUi(self.__uiPath)
		if "." in sys.path:
			sys.path.remove(".")

		EditorStatus.initializeUi(self)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
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
	def ui(self):
		"""
		This method is the property for **self.__ui** attribute.

		:return: self.__ui. ( Object )
		"""

		return self.__ui

	@ui.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ui(self, value):
		"""
		This method is the setter method for **self.__ui** attribute.

		:param value: Attribute value. ( Object )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("ui"))

	@ui.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def ui(self):
		"""
		This method is the deleter method for **self.__ui** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("ui"))

	@property
	def Lines_Columns_label_defaultText(self):
		"""
		This method is the property for **self.__Lines_Columns_label_defaultText** attribute.

		:return: self.__Lines_Columns_label_defaultText. ( String )
		"""

		return self.__Lines_Columns_label_defaultText

	@Lines_Columns_label_defaultText.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def Lines_Columns_label_defaultText(self, value):
		"""
		This method is the setter method for **self.__Lines_Columns_label_defaultText** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("Lines_Columns_label_defaultText"))

	@Lines_Columns_label_defaultText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def Lines_Columns_label_defaultText(self):
		"""
		This method is the deleter method for **self.__Lines_Columns_label_defaultText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("Lines_Columns_label_defaultText"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def initializeUi(self):
		"""
		This method initializes the Widget ui.

		:return: Method success. ( Boolean )		
		"""

		self.__ui.Lines_Columns_label.setAlignment(Qt.AlignRight)
		self.__ui.Lines_Columns_label.setText(self.__Lines_Columns_label_defaultText.format(1, 1))

		self.__ui.Languages_comboBox.setModel(self.__container.languagesModel)

		# Signals / Slots.
		self.__ui.Languages_comboBox.currentIndexChanged.connect(self.__Languages_comboBox__currentIndexChanged)

	@core.executionTrace
	def __Languages_comboBox_setDefaultViewState(self):
		"""
		This method sets the **Languages_comboBox** Widget default View state.
		"""

		if not self.__container.hasEditorTab():
			return

		editor = self.__container.getCurrentEditor()
		index = self.__ui.Languages_comboBox.findText(editor.language.name)

		if not index:
			return

		self.__ui.Languages_comboBox.setCurrentIndex(index)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __Languages_comboBox__currentIndexChanged(self, index):
		"""
		This method is called when the **Languages_comboBox** Widget current index is changed.

		:param index: ComboBox current item index. ( Integer )
		"""

		if not self.__container.hasEditorTab():
			return

		language = self.__container.languagesModel.getLanguage(str(self.__ui.Languages_comboBox.currentText()))
		if not language:
			return

		editor = self.__container.getCurrentEditor()
		return self.__container.setEditorLanguage(editor, language, emitSignal=False)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __editor__cursorPositionChanged(self):
		"""
		This method is triggered when an editor cursor position is changed.
		"""

		if not self.__container.hasEditorTab():
			return

		editor = self.__container.getCurrentEditor()
		self.__ui.Lines_Columns_label.setText(self.__Lines_Columns_label_defaultText.format(editor.getCursorLine() + 1, editor.getCursorColumn() + 1))