#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**scriptEditor.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`ScriptEditor` Component Interface class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import code
import logging
import os
import platform
import re
import sys
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import umbra.ui.common
import umbra.ui.completers
import umbra.ui.highlighters
import umbra.ui.inputAccelerators
from manager.uiComponent import UiComponent
from umbra.components.factory.scriptEditor.editor import Editor, Language, PYTHON_LANGUAGE
from umbra.components.factory.scriptEditor.searchAndReplace import SearchAndReplace
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals
from umbra.globals.uiConstants import UiConstants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Editor_Status", "ScriptEditor"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Editor_Status(QObject):
	"""
	| This class defines the **ScriptEditor** Component status bar widget. 
	"""

	@core.executionTrace
	def __init__(self, container):
		"""
		This method initializes the class.

		:param container: Container. ( Object )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QObject.__init__(self)

		# --- Setting class attributes. ---
		self.__container = container

		self.__maximumStoredPatterns = 15

		self.__uiPath = "ui/Editor_Status.ui"
		self.__uiPath = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)

		self.__ui = uic.loadUi(self.__uiPath)
		if "." in sys.path:
			sys.path.remove(".")

		Editor_Status.initializeUi(self)

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
		self.__ui.Languages_comboBox.addItems(self.__container.languages.keys())

		# Signals / Slots.
		self.__ui.Languages_comboBox.activated.connect(self.__Languages_comboBox__activated)

	@core.executionTrace
	def __Languages_comboBox_setDefaultViewState(self):
		"""
		This method sets the **Languages_comboBox** Widget default View state.
		"""

		if not self.__container.hasEditorTab():
			return

		editor = self.__container.getCurrentEditor()
		for i in range(self.__ui.Languages_comboBox.count()):
			if self.__ui.Languages_comboBox.itemText(i) == editor.language.name:
				self.__ui.Languages_comboBox.setCurrentIndex(i)
				return

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __Languages_comboBox__activated(self, index):
		"""
		This method is called when the **Languages_comboBox** Widget is activated.

		:param index: ComboBox activated item index. ( Integer )
		"""

		if not self.__container.hasEditorTab():
			return

		language = self.__container.languages[str(self.__ui.Languages_comboBox.currentText())]
		editor = self.__container.getCurrentEditor()
		return self.__container.setEditorLanguage(editor, language)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __editor__cursorPositionChanged(self):
		"""
		This method is triggered when an editor cursor position is changed.
		"""

		if not self.__container.hasEditorTab():
			return

		editor = self.__container.getCurrentEditor()
		self.__ui.Lines_Columns_label.setText("Line {0} : Column {1}".format(editor.getCursorLine(), editor.getCursorColumn()))

class ScriptEditor(UiComponent):
	"""
	| This class is the :mod:`umbra.components.addons.scriptEditor.scriptEditor` Component Interface class.
	"""

	# Custom signals definitions.
	datasChanged = pyqtSignal()
	recentFilesChanged = pyqtSignal()

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This method initializes the class.

		:param name: Component name. ( String )
		:param uiFile: Ui file. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__uiPath = "ui/Script_Editor.ui"
		self.__dockArea = 8

		self.__container = None
		self.__settings = None
		self.__settingsSection = None

		self.__languages = {"Python" : PYTHON_LANGUAGE,
							"Logging" : Language(name="Logging",
												extension="\.log",
												highlighter=umbra.ui.highlighters.LoggingHighlighter,
												completer=None,
												preInputAccelerators=(),
												postInputAccelerators=(),
												indentMarker="\t",
												commentMarker=None),
							"Text" : Language(name="Text",
												extension="\.txt",
												highlighter=None,
												completer=umbra.ui.completers.EnglishCompleter,
												preInputAccelerators=(umbra.ui.inputAccelerators.completionPreEventInputAccelerators,),
												postInputAccelerators=(),
												indentMarker="\t",
												commentMarker=None)}

		self.__defaultLanguage = "Text"
		self.__defaultScriptLanguage = "Python"

		self.__files = []
		self.__modifiedFiles = set()

		self.__defaultWindowTitle = "Script Editor"
		self.__defaultScriptEditorDirectory = "scriptEditor"
		self.__defaultScriptEditorFile = "defaultScript.py"
		self.__scriptEditorFile = None

		self.__maximumRecentFiles = 10
		self.__recentFilesActions = None

		self.__searchAndReplace = None

		self.__indentWidth = 20
		self.__defaultFontsSettings = {"Windows" : ("Consolas", 10), "Darwin" : ("Monaco", 12), "Linux" : ("Nimbus Mono L", 10)}

		self.__locals = None
		self.__memoryHandlerStackDepth = None
		self.__menuBar = None

		self.__fileSystemWatcher = None
		self.__Languages_comboBox = None

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiPath(self):
		"""
		This method is the property for ** self.__uiPath ** attribute.

		:return: self.__uiPath. ( String )
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for ** self.__uiPath ** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("uiPath"))

	@uiPath.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self):
		"""
		This method is the deleter method for ** self.__uiPath ** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("uiPath"))

	@property
	def dockArea(self):
		"""
		This method is the property for ** self.__dockArea ** attribute.

		:return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This method is the setter method for ** self.__dockArea ** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for ** self.__dockArea ** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dockArea"))

	@property
	def container(self):
		"""
		This method is the property for ** self.__container ** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for ** self.__container ** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for ** self.__container ** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This method is the deleter method for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settings"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("settingsSection"))

	@settingsSection.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settingsSection(self):
		"""
		This method is the deleter method for **self.__settingsSection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("settingsSection"))

	@property
	def languages(self):
		"""
		This method is the property for **self.__languages** attribute.

		:return: self.__languages. ( Dictionary )
		"""

		return self.__languages

	@languages.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def languages(self, value):
		"""
		This method is the setter method for **self.__languages** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("languages"))

	@languages.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def languages(self):
		"""
		This method is the deleter method for **self.__languages** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("languages"))

	@property
	def defaultLanguage(self):
		"""
		This method is the property for ** self.__defaultLanguage ** attribute.

		:return: self.__defaultLanguage. ( String )
		"""

		return self.__defaultLanguage

	@defaultLanguage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultLanguage(self, value):
		"""
		This method is the setter method for ** self.__defaultLanguage ** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("defaultLanguage"))

	@defaultLanguage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultLanguage(self):
		"""
		This method is the deleter method for ** self.__defaultLanguage ** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultLanguage"))

	@property
	def defaultScriptLanguage(self):
		"""
		This method is the property for ** self.__defaultScriptLanguage ** attribute.

		:return: self.__defaultScriptLanguage. ( String )
		"""

		return self.__defaultScriptLanguage

	@defaultScriptLanguage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultScriptLanguage(self, value):
		"""
		This method is the setter method for ** self.__defaultScriptLanguage ** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("defaultScriptLanguage"))

	@defaultScriptLanguage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultScriptLanguage(self):
		"""
		This method is the deleter method for ** self.__defaultScriptLanguage ** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultScriptLanguage"))

	@property
	def files(self):
		"""
		This method is the property for **self.__files** attribute.

		:return: self.__files. ( List )
		"""

		return self.__files

	@files.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def files(self, value):
		"""
		This method is the setter method for **self.__files** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("files"))

	@files.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def files(self):
		"""
		This method is the deleter method for **self.__files** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("files"))

	@property
	def modifiedFiles(self):
		"""
		This method is the property for **self.__modifiedFiles** attribute.

		:return: self.__modifiedFiles. ( Set )
		"""

		return self.__modifiedFiles

	@modifiedFiles.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modifiedFiles(self, value):
		"""
		This method is the setter method for **self.__modifiedFiles** attribute.

		:param value: Attribute value. ( Set )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("modifiedFiles"))

	@modifiedFiles.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modifiedFiles(self):
		"""
		This method is the deleter method for **self.__modifiedFiles** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("modifiedFiles"))

	@property
	def defaultWindowTitle(self):
		"""
		This method is the property for ** self.__defaultWindowTitle ** attribute.

		:return: self.__defaultWindowTitle. ( String )
		"""

		return self.__defaultWindowTitle

	@defaultWindowTitle.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultWindowTitle(self, value):
		"""
		This method is the setter method for ** self.__defaultWindowTitle ** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("defaultWindowTitle"))

	@defaultWindowTitle.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultWindowTitle(self):
		"""
		This method is the deleter method for ** self.__defaultWindowTitle ** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultWindowTitle"))

	@property
	def defaultScriptEditorDirectory(self):
		"""
		This method is the property for ** self.__defaultScriptEditorDirectory ** attribute.

		:return: self.__defaultScriptEditorDirectory. ( String )
		"""

		return self.__defaultScriptEditorDirectory

	@defaultScriptEditorDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultScriptEditorDirectory(self, value):
		"""
		This method is the setter method for ** self.__defaultScriptEditorDirectory ** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("defaultScriptEditorDirectory"))

	@defaultScriptEditorDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultScriptEditorDirectory(self):
		"""
		This method is the deleter method for ** self.__defaultScriptEditorDirectory ** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultScriptEditorDirectory"))

	@property
	def defaultScriptEditorFile(self):
		"""
		This method is the property for ** self.__defaultScriptEditorFile ** attribute.

		:return: self.__defaultScriptEditorFile. ( String )
		"""

		return self.__defaultScriptEditorFile

	@defaultScriptEditorFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultScriptEditorFile(self, value):
		"""
		This method is the setter method for ** self.__defaultScriptEditorFile ** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("defaultScriptEditorFile"))

	@defaultScriptEditorFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultScriptEditorFile(self):
		"""
		This method is the deleter method for ** self.__defaultScriptEditorFile ** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultScriptEditorFile"))

	@property
	def scriptEditorFile(self):
		"""
		This method is the property for ** self.__scriptEditorFile ** attribute.

		:return: self.__scriptEditorFile. ( String )
		"""

		return self.__scriptEditorFile

	@scriptEditorFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def scriptEditorFile(self, value):
		"""
		This method is the setter method for ** self.__scriptEditorFile ** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("scriptEditorFile", value)
		self.__scriptEditorFile = value

	@scriptEditorFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def scriptEditorFile(self):
		"""
		This method is the deleter method for ** self.__scriptEditorFile ** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("scriptEditorFile"))

	@property
	def maximumRecentFiles(self):
		"""
		This method is the property for ** self.__maximumRecentFiles ** attribute.

		:return: self.__maximumRecentFiles. ( Integer )
		"""

		return self.__maximumRecentFiles

	@maximumRecentFiles.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumRecentFiles(self, value):
		"""
		This method is the setter method for ** self.__maximumRecentFiles ** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("maximumRecentFiles"))

	@maximumRecentFiles.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumRecentFiles(self):
		"""
		This method is the deleter method for ** self.__maximumRecentFiles ** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("maximumRecentFiles"))

	@property
	def recentFilesActions(self):
		"""
		This method is the property for ** self.__recentFilesActions ** attribute.

		:return: self.__recentFilesActions. ( List )
		"""

		return self.__recentFilesActions

	@recentFilesActions.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def recentFilesActions(self, value):
		"""
		This method is the setter method for ** self.__recentFilesActions ** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("recentFilesActions"))

	@recentFilesActions.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def recentFilesActions(self):
		"""
		This method is the deleter method for ** self.__recentFilesActions ** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("recentFilesActions"))

	@property
	def searchAndReplace(self):
		"""
		This method is the property for ** self.__searchAndReplace ** attribute.

		:return: self.__searchAndReplace. ( SearchAndReplace )
		"""

		return self.__searchAndReplace

	@searchAndReplace.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchAndReplace(self, value):
		"""
		This method is the setter method for ** self.__searchAndReplace ** attribute.

		:param value: Attribute value. ( SearchAndReplace )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("searchAndReplace"))

	@searchAndReplace.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchAndReplace(self):
		"""
		This method is the deleter method for ** self.__searchAndReplace ** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("searchAndReplace"))

	@property
	def indentWidth(self):
		"""
		This method is the property for **self.__indentWidth** attribute.

		:return: self.__indentWidth. ( Integer )
		"""

		return self.__indentWidth

	@indentWidth.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def indentWidth(self, value):
		"""
		This method is the setter method for **self.__indentWidth** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("indentWidth"))

	@indentWidth.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def indentWidth(self):
		"""
		This method is the deleter method for **self.__indentWidth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("indentWidth"))

	@property
	def defaultFontsSettings(self):
		"""
		This method is the property for **self.__defaultFontsSettings** attribute.

		:return: self.__defaultFontsSettings. ( Dictionary )
		"""

		return self.__defaultFontsSettings

	@defaultFontsSettings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultFontsSettings(self, value):
		"""
		This method is the setter method for **self.__defaultFontsSettings** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("defaultFontsSettings"))

	@defaultFontsSettings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultFontsSettings(self):
		"""
		This method is the deleter method for **self.__defaultFontsSettings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultFontsSettings"))

	@property
	def locals(self):
		"""
		This method is the property for ** self.__locals ** attribute.

		:return: self.__locals. ( Dictionary )
		"""

		return self.__locals

	@locals.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def locals(self, value):
		"""
		This method is the setter method for ** self.__locals ** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("locals"))

	@locals.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def locals(self):
		"""
		This method is the deleter method for ** self.__locals ** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("locals"))

	@property
	def memoryHandlerStackDepth(self):
		"""
		This method is the property for ** self.__memoryHandlerStackDepth ** attribute.

		:return: self.__memoryHandlerStackDepth. ( Integer )
		"""

		return self.__memoryHandlerStackDepth

	@memoryHandlerStackDepth.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def memoryHandlerStackDepth(self, value):
		"""
		This method is the setter method for ** self.__memoryHandlerStackDepth ** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("memoryHandlerStackDepth"))

	@memoryHandlerStackDepth.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def memoryHandlerStackDepth(self):
		"""
		This method is the deleter method for ** self.__memoryHandlerStackDepth ** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("memoryHandlerStackDepth"))

	@property
	def menuBar(self):
		"""
		This method is the property for ** self.__menuBar ** attribute.

		:return: self.__menuBar. ( QToolbar )
		"""

		return self.__menuBar

	@menuBar.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def menuBar(self, value):
		"""
		This method is the setter method for ** self.__menuBar ** attribute.

		:param value: Attribute value. ( QToolbar )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("menuBar"))

	@menuBar.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def menuBar(self):
		"""
		This method is the deleter method for ** self.__menuBar ** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("menuBar"))

	@property
	def fileSystemWatcher(self):
		"""
		This method is the property for **self.__fileSystemWatcher** attribute.

		:return: self.__fileSystemWatcher. ( QFileSystemWatcher )
		"""

		return self.__fileSystemWatcher

	@fileSystemWatcher.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def fileSystemWatcher(self, value):
		"""
		This method is the setter method for **self.__fileSystemWatcher** attribute.

		:param value: Attribute value. ( QFileSystemWatcher )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("fileSystemWatcher"))

	@fileSystemWatcher.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def fileSystemWatcher(self):
		"""
		This method is the deleter method for **self.__fileSystemWatcher** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("fileSystemWatcher"))

	@property
	def Languages_comboBox(self):
		"""
		This method is the property for **self.__Languages_comboBox** attribute.

		:return: self.__Languages_comboBox. ( QLabel )
		"""

		return self.__Languages_comboBox

	@Languages_comboBox.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def Languages_comboBox(self, value):
		"""
		This method is the setter method for **self.__Languages_comboBox** attribute.

		:param value: Attribute value. ( QLabel )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("Languages_comboBox"))

	@Languages_comboBox.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def Languages_comboBox(self):
		"""
		This method is the deleter method for **self.__Languages_comboBox** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("Languages_comboBox"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		:param container: Container to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__container = container
		self.__settings = self.__container.settings
		self.__settingsSection = self.name

		self.__defaultScriptEditorDirectory = os.path.join(self.__container.userApplicationDatasDirectory, Constants.ioDirectory, self.__defaultScriptEditorDirectory)
		not os.path.exists(self.__defaultScriptEditorDirectory) and os.makedirs(self.__defaultScriptEditorDirectory)
		self.__defaultScriptEditorFile = os.path.join(self.__defaultScriptEditorDirectory, self.__defaultScriptEditorFile)

		self.__getsLocals()
		self.__console = code.InteractiveConsole(self.__locals)

		return UiComponent.activate(self)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component cannot be deactivated!".format(self.__name))

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__recentFilesActions = []
		for i in range(self.__maximumRecentFiles):
			self.__recentFilesActions.append(QAction(self.__menuBar, visible=False, triggered=self.__loadRecentFile__triggered))

		self.__menuBar = QMenuBar()
		self.__menuBar.setNativeMenuBar(False)
		self.ui.menuBar_frame_gridLayout.addWidget(self.__menuBar)
		self.__initializeMenuBar()

		self.ui.Script_Editor_Output_plainTextEdit.highlighter = umbra.ui.highlighters.LoggingHighlighter(self.ui.Script_Editor_Output_plainTextEdit.document())
		self.ui.Script_Editor_Output_plainTextEdit.setTabStopWidth(self.__indentWidth)
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			fontFamily, fontSize = self.__defaultFontsSettings["Windows"]
		elif platform.system() == "Darwin":
			fontFamily, fontSize = self.__defaultFontsSettings["Darwin"]
		elif platform.system() == "Linux":
			fontFamily, fontSize = self.__defaultFontsSettings["Linux"]
		font = QFont(fontFamily)
		font.setPointSize(fontSize)
		self.ui.Script_Editor_Output_plainTextEdit.setFont(font)

		self.__searchAndReplace = SearchAndReplace(self)

		self.__fileSystemWatcher = QFileSystemWatcher(self)

		self.Editor_Status = Editor_Status(self)

		self.__container.statusBar.addPermanentWidget(self.Editor_Status.ui)

		# Signals / Slots.
		self.__container.timer.timeout.connect(self.__Script_Editor_Output_plainTextEdit_refreshUi)
		self.__container.timer.timeout.connect(self.__reloadModifiedFiles)
		self.ui.Script_Editor_tabWidget.tabCloseRequested.connect(self.__Script_Editor_tabWidget__tabCloseRequested)
		self.ui.Script_Editor_tabWidget.currentChanged.connect(self.__Script_Editor_tabWidget__currentChanged)
		RuntimeGlobals.application.focusChanged.connect(self.__application__focusChanged)
		self.datasChanged.connect(self.__Script_Editor_Output_plainTextEdit_refreshUi)
		self.recentFilesChanged.connect(self.__setRecentFilesActions)
		self.__fileSystemWatcher.fileChanged.connect(self.__fileSystemWatcher__fileChanged)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.

		:return: Method success. ( Boolean )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component ui cannot be uninitialized!".format(self.name))

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

		return True

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.removeDockWidget(self.ui)
		self.ui.setParent(None)

		return True

	@core.executionTrace
	def onStartup(self):
		"""
		This method is called on Framework startup.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		if os.path.exists(self.__defaultScriptEditorFile):
			return self.loadFile(self.__defaultScriptEditorFile)
		else:
			return self.newFile()

	@core.executionTrace
	def onClose(self):
		"""
		This method is called on Framework close.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onClose' method.".format(self.__class__.__name__))

		return self.closeAllFiles(leaveLastEditor=False)

	@core.executionTrace
	def __initializeMenuBar(self):
		"""
		This method initializes Component menuBar.
		"""

		fileMenu = QMenu("&File", parent=self.__menuBar)
		fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|&New", shortcut=QKeySequence.New, slot=self.__newFileAction__triggered))
		fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|&Load ...", shortcut=QKeySequence.Open, slot=self.__loadFileAction__triggered))
		fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|Source ...", slot=self.__sourceFileAction__triggered))
		fileMenu.addSeparator()
		fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|&Save", shortcut=QKeySequence.Save, slot=self.__saveFileAction__triggered))
		fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|Save As ...", shortcut=QKeySequence.SaveAs, slot=self.__saveFileAsAction__triggered))
		fileMenu.addSeparator()
		fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|Close ...", shortcut=QKeySequence.Close, slot=self.__closeFileAction__triggered))
		fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|Close All ...", shortcut=Qt.SHIFT + Qt.ControlModifier + Qt.Key_W, slot=self.__closeAllFilesAction__triggered))
		fileMenu.addSeparator()
		for action in self.__recentFilesActions:
			fileMenu.addAction(action)
		self.__setRecentFilesActions()
		self.__menuBar.addMenu(fileMenu)

		self.__editMenu = QMenu("&Edit")
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|&Undo", shortcut=QKeySequence.Undo, slot=self.__undoAction__triggered))
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|&Redo", shortcut=QKeySequence.Redo, slot=self.__redoAction__triggered))
		self.__editMenu.addSeparator()
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|Cu&t", shortcut=QKeySequence.Cut, slot=self.__cutAction__triggered))
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|&Copy", shortcut=QKeySequence.Copy, slot=self.__copyAction__triggered))
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|&Paste", shortcut=QKeySequence.Paste, slot=self.__pasteAction__triggered))
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|Delete", slot=self.__deleteAction__triggered))
		self.__editMenu.addSeparator()
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|Select All", shortcut=QKeySequence.SelectAll, slot=self.__selectAllAction__triggered))
		self.__editMenu.addSeparator()
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|Goto Line ...", shortcut=Qt.ControlModifier + Qt.Key_L, slot=self.__gotoLineAction__triggered))
		self.__editMenu.addSeparator()
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|Indent Selection", shortcut=Qt.Key_Tab, slot=self.__indentSelectionAction__triggered))
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|Unindent Selection", shortcut=Qt.Key_Backtab, slot=self.__unindentSelectionAction__triggered))
		self.__editMenu.addSeparator()
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|Toggle Comments", shortcut=Qt.ControlModifier + Qt.Key_Slash, slot=self.__toggleCommentsAction__triggered))
		self.__menuBar.addMenu(self.__editMenu)

		self.__searchMenu = QMenu("&Search")
		self.__searchMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Search|Search And Replace ...", shortcut=Qt.ControlModifier + Qt.Key_F, slot=self.__searchAndReplaceAction__triggered))
		self.__searchMenu.addSeparator()
		self.__searchMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Search|Search Next", shortcut=Qt.ControlModifier + Qt.Key_K, slot=self.__searchNextAction__triggered))
		self.__searchMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Search|Search Previous", shortcut=Qt.SHIFT + Qt.ControlModifier + Qt.Key_K, slot=self.__searchPreviousAction__triggered))
		self.__menuBar.addMenu(self.__searchMenu)

		self.__commandMenu = QMenu("&Command")
		self.__commandMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Command|&Evaluate Selection", shortcut=Qt.ControlModifier + Qt.Key_Return, slot=self.__evaluateSelectionAction__triggered))
		self.__commandMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Command|Evaluate &Script", shortcut=Qt.SHIFT + Qt.CTRL + Qt.Key_Return, slot=self.__evaluateScriptAction__triggered))
		self.__menuBar.addMenu(self.__commandMenu)

		self.__viewMenu = QMenu("&View")
		self.__viewMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&View|Toggle Word Wrap", slot=self.__toggleWordWrapAction__triggered))
		self.__viewMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&View|Toggle White Spaces", slot=self.__toggleWhiteSpacesAction__triggered))
		self.__menuBar.addMenu(self.__viewMenu)

	# @core.executionTrace
	def __Script_Editor_Output_plainTextEdit_setUi(self):
		"""
		This method sets the **Script_Editor_Output_plainTextEdit** Widget.
		"""

		for line in self.__container.loggingSessionHandlerStream.stream:
			self.ui.Script_Editor_Output_plainTextEdit.moveCursor(QTextCursor.End)
			self.ui.Script_Editor_Output_plainTextEdit.insertPlainText(line)
		self.__Script_Editor_Output_plainTextEdit_setDefaultViewState()

	# @core.executionTrace
	def __Script_Editor_Output_plainTextEdit_setDefaultViewState(self):
		"""
		This method sets the **Script_Editor_Output_plainTextEdit** Widget default View state.
		"""

		self.ui.Script_Editor_Output_plainTextEdit.moveCursor(QTextCursor.End)
		self.ui.Script_Editor_Output_plainTextEdit.ensureCursorVisible()

	# @core.executionTrace
	def __Script_Editor_Output_plainTextEdit_refreshUi(self):
		"""
		This method updates the **Script_Editor_Output_plainTextEdit** Widget.
		"""

		memoryHandlerStackDepth = len(self.__container.loggingSessionHandlerStream.stream)
		if memoryHandlerStackDepth != self.__memoryHandlerStackDepth:
			for line in self.__container.loggingSessionHandlerStream.stream[self.__memoryHandlerStackDepth:memoryHandlerStackDepth]:
				self.ui.Script_Editor_Output_plainTextEdit.moveCursor(QTextCursor.End)
				self.ui.Script_Editor_Output_plainTextEdit.insertPlainText(line)
			self.__Script_Editor_Output_plainTextEdit_setDefaultViewState()
			self.__memoryHandlerStackDepth = memoryHandlerStackDepth

	@core.executionTrace
	def __Languages_comboBox_setUi(self):
		"""
		This method sets the **Languages_comboBox** Widget.
		"""

		self.__Languages_comboBox = QComboBox()
		self.__Languages_comboBox.setObjectName("Languages_comboBox")
		self.__Languages_comboBox.addItems(self.__languages.keys())

	@core.executionTrace
	def __Script_Editor_tabWidget__tabCloseRequested(self, tabIndex):
		"""
		This method is triggered by the **Script_Editor_tabWidget** Widget when a tab is requested to be closed.

		:param tabIndex: Tab index. ( Integer )
		"""

		return self.closeFile()

	@core.executionTrace
	def __Script_Editor_tabWidget__currentChanged(self, tabIndex):
		"""
		This method is triggered by the **Script_Editor_tabWidget** Widget when the current tab is changed.

		:param tabIndex: Tab index. ( Integer )
		"""

		self.Editor_Status._Editor_Status__Languages_comboBox_setDefaultViewState()
		self.__setWindowTitle()

	@core.executionTrace
	def __application__focusChanged(self, previousWidget, currentWidget):
		"""
		This method is triggered by the Application when the widget focus is changed.

		:param previousWidget: Widget that lost focus. ( QWidget )
		:param currentWidget: Widget that gained focus. ( QWidget )
		"""

		if not currentWidget:
			return

		if isinstance(currentWidget, Editor):
			self.Editor_Status.ui.show()
		else:
			for object in umbra.ui.common.parentsWalker(currentWidget):
				if object is self.__container.statusBar:
					return

			self.Editor_Status.ui.hide()

	@core.executionTrace
	def __newFileAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|&New'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.newFile()

	@core.executionTrace
	def __loadFileAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|&Load ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.loadFile_ui()

	@core.executionTrace
	def __sourceFileAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|Source ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if self.loadFile_ui():
			return self.evaluateScript()

	@core.executionTrace
	def __saveFileAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|&Save'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.saveFile()

	@core.executionTrace
	def __saveFileAsAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|Save As ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.saveFileAs()

	@core.executionTrace
	def __closeFileAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|Close ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.closeFile()

	@core.executionTrace
	def __closeAllFilesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|Close All ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.closeAllFiles()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __loadRecentFile__triggered(self, checked):
		"""
		This method is triggered by any recent file related action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		file = self.sender()._datas
		if os.path.exists(file):
			return self.loadFile(file)

	@core.executionTrace
	def __undoAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Undo'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		self.getCurrentEditor().undo()
		return True

	@core.executionTrace
	def __redoAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Redo'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		self.getCurrentEditor().redo()
		return True

	@core.executionTrace
	def __cutAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|Cu&t'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		currentWidget = QApplication.focusWidget()
		if currentWidget.objectName() == "Script_Editor_Output_plainTextEdit":
			self.ui.Script_Editor_Output_plainTextEdit.copy()
		elif isinstance(QApplication.focusWidget(), Editor):
			self.getCurrentEditor().cut()
		return True

	@core.executionTrace
	def __copyAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Copy'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		currentWidget = QApplication.focusWidget()
		if currentWidget.objectName() == "Script_Editor_Output_plainTextEdit":
			self.ui.Script_Editor_Output_plainTextEdit.copy()
		elif isinstance(QApplication.focusWidget(), Editor):
			self.getCurrentEditor().copy()
		return True

	@core.executionTrace
	def __pasteAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Paste'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		self.getCurrentEditor().paste()
		return True

	@core.executionTrace
	def __deleteAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|Delete'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		self.getCurrentEditor().delete()
		return True

	@core.executionTrace
	def __selectAllAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|Select All'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		currentWidget = QApplication.focusWidget()
		if currentWidget.objectName() == "Script_Editor_Output_plainTextEdit":
			self.ui.Script_Editor_Output_plainTextEdit.selectAll()
		elif isinstance(QApplication.focusWidget(), Editor):
			self.getCurrentEditor().selectAll()
		return True

	@core.executionTrace
	def __gotoLineAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|Goto Line ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.gotoLine()

	@core.executionTrace
	def __searchAndReplaceAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Search|Search And Replace ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.searchAndReplace_ui()

	@core.executionTrace
	def __searchNextAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Search|Search Next'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().searchNext()

	@core.executionTrace
	def __searchPreviousAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Search|Search Previous'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().searchPrevious()

	@core.executionTrace
	def __indentSelectionAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|Indent Selection'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().indent()

	@core.executionTrace
	def __unindentSelectionAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|Unindent Selection'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().unindent()

	@core.executionTrace
	def __toggleCommentsAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|Toggle Comments'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().toggleComments()

	@core.executionTrace
	def __evaluateSelectionAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Command|&Evaluate Selection'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.evaluateSelection()

	@core.executionTrace
	def __evaluateScriptAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Command|Evaluate &Script'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.evaluateScript()

	@core.executionTrace
	def __toggleWordWrapAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&View|Toggle Word Wrap'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().toggleWordWrap()

	@core.executionTrace
	def __toggleWhiteSpacesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&View|Toggle White Spaces'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().toggleWhiteSpaces()

	@core.executionTrace
	def __editor__contentChanged(self):
		"""
		This method is triggered when an editor content is changed.
		"""

		self.__setEditorTabName(self.ui.Script_Editor_tabWidget.currentIndex())
		self.__setWindowTitle()

	@core.executionTrace
	def __editor__fileChanged(self):
		"""
		This method is triggered when an editor file is changed.
		"""

		self.__setEditorTabName(self.ui.Script_Editor_tabWidget.currentIndex())

	@core.executionTrace
	def __editor__languageChanged(self):
		"""
		This method is triggered when an editor language is changed.
		"""

		self.Editor_Status._Editor_Status__Languages_comboBox_setDefaultViewState()

	@core.executionTrace
	def __fileSystemWatcher__fileChanged(self, file):
		"""
		This method is triggered by the :obj:`fileSystemWatcher` class property when a file is modified.
		
		:param file: File modified. ( String )
		"""

		self.__modifiedFiles.add(file)

	@core.executionTrace
	def __reloadModifiedFiles(self):
		"""
		This method reloads modfied files.
		"""

		while self.__modifiedFiles:
			self.reloadFile(self.__modifiedFiles.pop())

	@core.executionTrace
	def __registerFile(self, file):
		"""
		This method registers provided file in the :obj:`ScriptEditor.files` class property.
		
		:param file: File to register. ( String )
		"""

		self.__files.append(file)
		self.__fileSystemWatcher.addPath(file)

	@core.executionTrace
	def __unregisterFile(self, file):
		"""
		This method unregisters provided file in the :obj:`ScriptEditor.files` class property.
		
		:param file: File to unregister. ( String )
		"""

		if file in self.__files:
			self.__files.remove(file)
			self.__fileSystemWatcher.removePath(file)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __setRecentFilesActions(self):
		"""
		This method sets the recent files actions.
		"""

		recentFiles = self.__settings.getKey(self.__settingsSection, "recentFiles").toString().split(",")
		if not recentFiles:
			return

		numberRecentFiles = min(len(recentFiles), self.__maximumRecentFiles)

		for i in range(self.__maximumRecentFiles):
			if i >= numberRecentFiles:
				self.__recentFilesActions[i].setVisible(False)
				continue

			self.__recentFilesActions[i].setText("{0} {1}".format(i + 1, os.path.basename(str(recentFiles[i]))))
			self.__recentFilesActions[i]._datas = str(recentFiles[i])
			self.__recentFilesActions[i].setVisible(True)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __storeRecentFile(self, file):
		"""
		This method stores provided recent file into the settings.
		
		:param file: File to store. ( String )
		"""

		recentFiles = self.__settings.getKey(self.__settingsSection, "recentFiles").toString().split(",")
		if not recentFiles:
			recentFiles = QStringList()

		if file in recentFiles:
			recentFiles.removeAt(recentFiles.indexOf(file))
		recentFiles.insert(0, file)
		del recentFiles[self.__maximumRecentFiles:]
		recentFiles = self.__settings.setKey(self.__settingsSection, "recentFiles", recentFiles.join(","))
		self.emit(SIGNAL("recentFilesChanged()"))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __setWindowTitle(self):
		"""
		This method sets the **scriptEditor** Component window title.
		"""

		if self.hasEditorTab():
			self.ui.setWindowTitle("{0} - {1}".format(self.__defaultWindowTitle, self.ui.Script_Editor_tabWidget.currentWidget().file))
		else:
			self.ui.setWindowTitle("{0}".format(self.__defaultWindowTitle))

	@core.executionTrace
	def __setEditorTabName(self, tabIndex):
		"""
		This method sets the editor tab name.

		:param tabIndex: Index of the tab containing the editor. ( Integer )
		"""

		self.ui.Script_Editor_tabWidget.setTabText(tabIndex, self.ui.Script_Editor_tabWidget.widget(tabIndex).windowTitle())

	@core.executionTrace
	def __getsLocals(self):
		"""
		This method gets the locals for the interactive console.

		:return: Method success. ( Boolean )
		"""

		self.__locals = {}

		for globals in (Constants, RuntimeGlobals, UiConstants):
			self.__locals[globals.__name__] = globals

		self.__locals[Constants.applicationName] = self.__container
		self.__locals["componentsManager"] = self.__container.componentsManager

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def registerLanguage(self, language, description):
		"""
		This method registers provided language name and description in the :obj:`ScriptEditor.languages` class property.
		
		:param language: Language name to register. ( String )
		:param description: Language description. ( Language )
		:return: Method success. ( Boolean )
		"""

		self.__languages[language] = description
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, KeyError)
	def unregisterLanguage(self, language):
		"""
		This method unregisters provided language name from the :obj:`ScriptEditor.languages` class property.
		
		:param language: Language name to unregister. ( String )
		:return: Method success. ( Boolean )
		"""

		if language not in self.__languages.keys():
			raise KeyError("{0} | '{1}' language isn't registered!".format(self.__class__.__name__, language))

		del(self.__languages[language])
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, KeyError)
	def getFileLanguage(self, file):
		"""
		This method returns the language of provided file.
		
		:param file: File to get language of. ( String )
		:return: File language / description. ( Tuple )
		"""

		fileLanguage = fileDescription = None
		for language, description in self.__languages.items():
			if re.search(description.extension, file):
				fileLanguage = language
				fileDescription = description
				break
		if not fileLanguage or not fileDescription:
			fileLanguage = self.__defaultLanguage
			fileDescription = self.__languages[self.__defaultLanguage]

		LOGGER.debug("> '{0}' file detected language: '{1}'.".format(file, fileLanguage))

		return fileLanguage, fileDescription

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setEditorLanguage(self, editor, language):
		"""
		This method sets provided editor language.
		
		:param editor: Editor to set language to. ( Editor )
		:return: Method success. ( Boolean )
		"""

		return editor.setLanguage(language)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def getCurrentEditor(self):
		"""
		This method returns the current editor.

		:return: Current editor. ( Editor )
		"""

		if not self.hasEditorTab():
			return

		return self.ui.Script_Editor_tabWidget.currentWidget()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def findEditor(self, file):
		"""
		This method finds the :class:`Editor` instance associated with the provided file.

		:param file: File to search editors for. ( String )
		:return: Editor. ( Editor )
		"""

		for i in range(self.ui.Script_Editor_tabWidget.count()):
			if not self.ui.Script_Editor_tabWidget.widget(i).file == file:
				continue
			return self.ui.Script_Editor_tabWidget.widget(i)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def loadFile_ui(self):
		"""
		This method loads user chosen file into a new :class:`Editor` instance with its associated tab.

		:return: Method success. ( Boolean )
		
		:note: This method may require user interaction.
		"""

		file = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getOpenFileName(self, "Load File:", RuntimeGlobals.lastBrowsedPath)))
		if not file:
			return

		return self.loadFile(file)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def searchAndReplace_ui(self):
		"""
 		This method performs a search and replace in the current widget tab editor.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		return self.__searchAndReplace.show()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addEditorTab(self, editor):
		"""
		This method adds a new tab to the **Script_Editor_tabWidget** Widget and sets provided editor as child widget.

		:param editor: Editor. ( Editor )
		:return: New tab index. ( Integer )
		"""

		tabIndex = self.ui.Script_Editor_tabWidget.addTab(editor, editor.getFileShortName())
		self.ui.Script_Editor_tabWidget.setCurrentIndex(tabIndex)

		# Signals / Slots.
		editor.languageChanged.connect(self.__editor__languageChanged)
		editor.contentChanged.connect(self.__editor__contentChanged)
		editor.fileChanged.connect(self.__editor__fileChanged)
		editor.cursorPositionChanged.connect(self.Editor_Status._Editor_Status__editor__cursorPositionChanged)
		return tabIndex

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeEditorTab(self, tabIndex):
		"""
		This method removes the **Script_Editor_tabWidget** Widget tab with provided index.

		:param tabIndex: Tab index. ( Integer )
		:return: Method success. ( Boolean )
		"""

		self.ui.Script_Editor_tabWidget.removeTab(tabIndex)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def findEditorTab(self, file):
		"""
		This method finds the :class:`Editor` instance tab associated with the provided file.

		:param file: File to search editors for. ( String )
		:return: Tab index. ( Editor )
		"""

		for i in range(self.ui.Script_Editor_tabWidget.count()):
			if not self.ui.Script_Editor_tabWidget.widget(i).file == file:
				continue
			return i

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def hasEditorTab(self):
		"""
		This method returns if the **Script_Editor_tabWidget** Widget has at least a tab.

		:return: Has tab. ( Boolean )
		"""

		return self.ui.Script_Editor_tabWidget.count() and True or False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def newFile(self):
		"""
		This method creates a new file into a new :class:`Editor` instance with its associated tab.

		:return: Method success. ( Boolean )
		"""

		editor = Editor(parent=None, language=self.__languages[self.__defaultScriptLanguage])
		LOGGER.info("{0} | Creating '{1}' file!".format(self.__class__.__name__, editor.getNextUntitledFileName()))
		if editor.newFile():
			self.addEditorTab(editor)
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
	def loadFile(self, file):
		"""
		This method reads and loads provided file into a new :class:`Editor` instance with its associated tab or sets the focus on an existing tab if the file is already loaded.

		:param file: File to load. ( String )
		:return: Method success. ( Boolean )
		"""

		if not os.path.exists(file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(self.__class__.__name__, file))

		tabIndex = self.findEditorTab(file)
		if tabIndex >= 0:
			LOGGER.info("{0} | '{1}' is already loaded!".format(self.__class__.__name__, file))
			self.ui.Script_Editor_tabWidget.setCurrentIndex(tabIndex)
			return

		LOGGER.info("{0} | Loading '{1}' file!".format(self.__class__.__name__, file))
		language, description = self.getFileLanguage(file)
		editor = Editor(parent=None, language=description)
		if editor.loadFile(file):
			self.addEditorTab(editor)
			self.__storeRecentFile(file)
			self.__registerFile(file)
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
	def reloadFile(self, file):
		"""
		This method reloads provided file into its associated tab.

		:param file: File to reload. ( String )
		:return: Method success. ( Boolean )
		"""

		if not os.path.exists(file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(self.__class__.__name__, file))

		tabIndex = self.findEditorTab(file)
		if tabIndex >= 0:
			LOGGER.info("{0} | Reloading '{1}' file!".format(self.__class__.__name__, file))
			editor = self.ui.Script_Editor_tabWidget.widget(tabIndex)
			return editor.reloadFile()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def saveFile(self):
		"""
		This method saves current :class:`Editor` instance file.

		:return: Method success. ( Boolean )
		"""

		if self.ui.Script_Editor_tabWidget.count():
			editor = self.ui.Script_Editor_tabWidget.currentWidget()
			LOGGER.info("{0} | Saving '{1}' file!".format(self.__class__.__name__, editor.file))
			self.__fileSystemWatcher.removePaths(self.__files)
			editor.saveFile()
			self.__fileSystemWatcher.addPaths(self.__files)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def saveFileAs(self):
		"""
		This method saves current :class:`Editor` instance file as user defined file.

		:return: Method success. ( Boolean )
		"""

		editor = self.getCurrentEditor()
		if not editor:
			return

		LOGGER.info("{0} | Saving '{1}' file!".format(self.__class__.__name__, editor.file))
		if editor.saveFileAs():
			self.__storeRecentFile(editor.file)
			self.__registerFile(editor.file)
			language, description = self.getFileLanguage(editor.file)
			if editor.language.name != language:
				self.setEditorLanguage(editor, description)
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def closeFile(self):
		"""
 		This method closes current :class:`Editor` instance file and removes the associated **Script_Editor_tabWidget** Widget tab.

		:return: Method success. ( Boolean )
		"""

		editor = self.getCurrentEditor()
		if not editor:
			return

		LOGGER.info("{0} | Closing '{1}' file!".format(self.__class__.__name__, editor.file))
		if not editor.closeFile():
			return

		self.__unregisterFile(editor.file)

		if self.removeEditorTab(self.ui.Script_Editor_tabWidget.currentIndex()):
			not self.ui.Script_Editor_tabWidget.count() and self.newFile()
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def closeAllFiles(self, leaveLastEditor=True):
		"""
 		This method closes every :class:`Editor` instances and removes their associated **Script_Editor_tabWidget** Widget tabs.

		:return: Method success. ( Boolean )
		"""

		for i in range(self.ui.Script_Editor_tabWidget.count(), 0, -1):
			editor = self.ui.Script_Editor_tabWidget.widget(i - 1)
			LOGGER.info("{0} | Closing '{1}' file!".format(self.__class__.__name__, editor.file))
			if not editor.closeFile():
				return

			self.__unregisterFile(editor.file)

			if self.removeEditorTab(self.ui.Script_Editor_tabWidget.currentIndex()):
				if not self.ui.Script_Editor_tabWidget.count() and leaveLastEditor:
					self.newFile()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def gotoLine(self):
		"""
 		This method moves current widget tab editor cursor to user defined line.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		editor = self.getCurrentEditor()
		if not editor:
			return

		line, state = QInputDialog.getInt(self, "Goto Line Number", "Line number:", min=1)
		if not state:
			return

		return editor.gotoLine(line)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def evaluateSelection(self):
		"""
		This method evaluates current **Script_Editor_tabWidget** Widget tab editor selected content in the interactive console.

		:return: Method success. ( Boolean )
		"""

		editor = self.getCurrentEditor()
		if not editor:
			return

		if self.evaluateCode(str(editor.textCursor().selectedText().replace(QChar(QChar.ParagraphSeparator), QString("\n")))):
			self.emit(SIGNAL("datasChanged()"))
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def evaluateScript(self):
		"""
		This method evaluates current **Script_Editor_tabWidget** Widget tab editor content in the interactive console.

		:return: Method success. ( Boolean )
		"""

		editor = self.getCurrentEditor()
		if not editor:
			return

		if self.evaluateCode(str(editor.toPlainText())):
			self.emit(SIGNAL("datasChanged()"))
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def evaluateCode(self, code):
		"""
		This method evaluates provided code in the interactive console.

		:param code: Code to evaluate. ( String )
		:return: Method success. ( Boolean )
		"""

		if not code:
			return

		code = code.endswith("\n") and code or "{0}\n".format(code)
		sys.stdout.write(code)
		self.__console.runcode(code)

		return True
