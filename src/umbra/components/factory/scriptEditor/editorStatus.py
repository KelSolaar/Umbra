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

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.ui.common
import foundations.strings as strings
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

__all__ = ["LOGGER", "UI_FILE", "EditorStatus"]

LOGGER = logging.getLogger(Constants.logger)

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Editor_Status.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class EditorStatus(foundations.ui.common.QWidgetFactory(uiFile=UI_FILE)):
	"""
	This class defines the
	:class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor` Component Interface class status bar widget. 
	"""

	@core.executionTrace
	def __init__(self, parent, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(EditorStatus, self).__init__(parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__container = parent

		self.__Lines_Columns_label_defaultText = "Line {0} : Column {1}"

		EditorStatus.__initializeUi(self)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "Lines_Columns_label_defaultText"))

	@Lines_Columns_label_defaultText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def Lines_Columns_label_defaultText(self):
		"""
		This method is the deleter method for **self.__Lines_Columns_label_defaultText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "Lines_Columns_label_defaultText"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		self.Lines_Columns_label.setAlignment(Qt.AlignRight)
		self.Lines_Columns_label.setText(self.__Lines_Columns_label_defaultText.format(1, 1))

		self.Languages_comboBox.setModel(self.__container.languagesModel)

		# Signals / Slots.
		self.Languages_comboBox.currentIndexChanged.connect(self.__Languages_comboBox__currentIndexChanged)

	@core.executionTrace
	def __Languages_comboBox_setDefaultViewState(self):
		"""
		This method sets the **Languages_comboBox** Widget default View state.
		"""

		if not self.__container.hasEditorTab():
			return

		editor = self.__container.getCurrentEditor()
		index = self.Languages_comboBox.findText(editor.language.name)

		self.Languages_comboBox.setCurrentIndex(index)

	@core.executionTrace
	def __Languages_comboBox__currentIndexChanged(self, index):
		"""
		This method is triggered when the **Languages_comboBox** Widget current index is changed.

		:param index: ComboBox current item index. ( Integer )
		"""

		if not self.__container.hasEditorTab():
			return

		language = self.__container.languagesModel.getLanguage(strings.encode(self.Languages_comboBox.currentText()))
		if not language:
			return

		editor = self.__container.getCurrentEditor()
		editor.blockSignals(True)
		self.__container.setLanguage(editor, language)
		editor.blockSignals(False)

	@core.executionTrace
	def __editor__cursorPositionChanged(self):
		"""
		This method is triggered when a
		:class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor` Component Interface class editor
		cursor position is changed.
		"""

		if not self.__container.hasEditorTab():
			return

		editor = self.__container.getCurrentEditor()
		self.Lines_Columns_label.setText(self.__Lines_Columns_label_defaultText.format(editor.getCursorLine() + 1,
																						editor.getCursorColumn() + 1))
