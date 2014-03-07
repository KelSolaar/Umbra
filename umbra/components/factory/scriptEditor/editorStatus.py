#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**editorStatus.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`EditorStatus` class.

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
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.ui.common
import foundations.strings
import foundations.verbose

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "UI_FILE", "EditorStatus"]

LOGGER = foundations.verbose.installLogger()

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Editor_Status.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class EditorStatus(foundations.ui.common.QWidgetFactory(uiFile=UI_FILE)):
	"""
	Defines the
	:class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor` Component Interface class status bar widget. 
	"""

	def __init__(self, parent, *args, **kwargs):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
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
		Property for **self.__container** attribute.

		:return: self.__container.
		:rtype: QObject
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		Setter for **self.__container** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		Deleter for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def Lines_Columns_label_defaultText(self):
		"""
		Property for **self.__Lines_Columns_label_defaultText** attribute.

		:return: self.__Lines_Columns_label_defaultText.
		:rtype: unicode
		"""

		return self.__Lines_Columns_label_defaultText

	@Lines_Columns_label_defaultText.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def Lines_Columns_label_defaultText(self, value):
		"""
		Setter for **self.__Lines_Columns_label_defaultText** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "Lines_Columns_label_defaultText"))

	@Lines_Columns_label_defaultText.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def Lines_Columns_label_defaultText(self):
		"""
		Deleter for **self.__Lines_Columns_label_defaultText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "Lines_Columns_label_defaultText"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeUi(self):
		"""
		Initializes the Widget ui.
		"""

		self.Lines_Columns_label.setAlignment(Qt.AlignRight)
		self.Lines_Columns_label.setText(self.__Lines_Columns_label_defaultText.format(1, 1))

		self.Languages_comboBox.setModel(self.__container.languagesModel)

		# Signals / Slots.
		self.Languages_comboBox.currentIndexChanged.connect(self.__Languages_comboBox__currentIndexChanged)

	def __Languages_comboBox_setDefaultViewState(self):
		"""
		Sets the **Languages_comboBox** Widget default View state.
		"""

		if not self.__container.hasEditorTab():
			return

		editor = self.__container.getCurrentEditor()
		index = self.Languages_comboBox.findText(editor.language.name)

		self.Languages_comboBox.setCurrentIndex(index)

	def __Languages_comboBox__currentIndexChanged(self, index):
		"""
		Defines the slot triggered by the **Languages_comboBox** Widget when current index is changed.

		:param index: ComboBox current item index.
		:type index: int
		"""

		if not self.__container.hasEditorTab():
			return

		language = self.__container.languagesModel.getLanguage(foundations.strings.toString(
		self.Languages_comboBox.currentText()))
		if not language:
			return

		editor = self.__container.getCurrentEditor()
		if editor.language == language:
			return

		editor.blockSignals(True)
		self.__container.setLanguage(editor, language)
		editor.blockSignals(False)

	def __editor__cursorPositionChanged(self):
		"""
		Defines the slot triggered by :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor`
		Component Interface class editor when cursor position is changed.
		"""

		if not self.__container.hasEditorTab():
			return

		editor = self.__container.getCurrentEditor()
		self.Lines_Columns_label.setText(self.__Lines_Columns_label_defaultText.format(editor.getCursorLine() + 1,
																						editor.getCursorColumn() + 1))
