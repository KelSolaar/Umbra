#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**scriptEditor.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`ScriptEditor` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import code
import os
import platform
import re
import sys
import shutil
from PyQt4.QtCore import QChar
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QKeySequence
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QMenuBar
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextOption

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.trace
import foundations.verbose
import foundations.walkers
import umbra.engine
import umbra.exceptions
import umbra.ui.common
import umbra.ui.highlighters
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.components.factory.scriptEditor.editor import Editor
from umbra.components.factory.scriptEditor.editorStatus import EditorStatus
from umbra.components.factory.scriptEditor.models import LanguagesModel
from umbra.components.factory.scriptEditor.models import ProjectsModel
from umbra.components.factory.scriptEditor.searchAndReplace import SearchAndReplace
from umbra.components.factory.scriptEditor.searchInFiles import SearchInFiles
from umbra.components.factory.scriptEditor.views import ScriptEditor_QTabWidget
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals
from umbra.globals.uiConstants import UiConstants
from umbra.ui.languages import getLanguageDescription
from umbra.ui.languages import LOGGING_LANGUAGE
from umbra.ui.languages import PYTHON_LANGUAGE
from umbra.ui.languages import TEXT_LANGUAGE
from umbra.ui.widgets.basic_QPlainTextEdit import Basic_QPlainTextEdit

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "ScriptEditor"]

LOGGER = foundations.verbose.installLogger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Script_Editor.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ScriptEditor(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	Defines the :mod:`sibl_gui.components.addons.scriptEditor.scriptEditor` Component Interface class.
	"""

	# Custom signals definitions.
	uiRefresh = pyqtSignal()
	"""
	This signal is emited by the :class:`ScriptEditor` class when the Ui needs to be refreshed. ( pyqtSignal )
	"""

	recentFilesChanged = pyqtSignal()
	"""
	This signal is emited by the :class:`ScriptEditor` class when the recent files list has changed. ( pyqtSignal )
	"""

	fileLoaded = pyqtSignal(unicode)
	"""
	This signal is emited by the :class:`ScriptEditor` class when a file is loaded. ( pyqtSignal )

	:return: Loaded file.
	:rtype: unicode
	"""

	fileClosed = pyqtSignal(unicode)
	"""
	This signal is emited by the :class:`ScriptEditor` class when a file is closed. ( pyqtSignal )

	:return: Closed file.
	:rtype: unicode
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

		super(ScriptEditor, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__dockArea = 1

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__developmentLayout = UiConstants.developmentLayout

		self.__grammarsDirectory = "grammars"
		self.__extension = "grc"

		self.__model = None
		self.__languagesModel = None

		self.__defaultProject = "defaultProject"
		self.__defaultLanguage = "Text"
		self.__defaultScriptLanguage = "Python"
		self.__defaultFileName = "Untitled"
		self.__defaultFileExtension = "py"

		self.__defaultWindowTitle = "Script Editor"

		self.__defaultScriptEditorDirectory = "scriptEditor"
		self.__defaultSessionDirectory = "session"
		self.__defaultScriptEditorFile = "defaultScript.py"
		self.__factoryDefaultScriptEditorFile = "others/defaultScript.py"
		self.__scriptEditorFile = None

		self.__maximumRecentFiles = 10
		self.__recentFilesActions = None

		self.__searchAndReplace = None
		self.__searchInFiles = None

		self.__indentWidth = 20
		self.__defaultFontsSettings = {"Windows" : ("Consolas", 10),
										"Darwin" : ("Monaco", 12),
										"Linux" : ("Monospace", 10)}

		self.__console = None
		self.__memoryHandlerStackDepth = None

		self.__menuBar = None
		self.__fileMenu = None
		self.__editMenu = None
		self.__sourceMenu = None
		self.__navigateMenu = None
		self.__searchMenu = None
		self.__commandMenu = None
		self.__viewMenu = None

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def dockArea(self):
		"""
		Property for **self.__dockArea** attribute.

		:return: self.__dockArea.
		:rtype: int
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		Setter for **self.__dockArea** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		Deleter for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

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
	def developmentLayout(self):
		"""
		Property for **self.__developmentLayout** attribute.

		:return: self.__developmentLayout.
		:rtype: unicode
		"""

		return self.__developmentLayout

	@developmentLayout.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def developmentLayout(self, value):
		"""
		Setter for **self.__developmentLayout** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "developmentLayout"))

	@developmentLayout.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def developmentLayout(self):
		"""
		Deleter for **self.__developmentLayout** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "developmentLayout"))

	@property
	def grammarsDirectory(self):
		"""
		Property for **self.__grammarsDirectory** attribute.

		:return: self.__grammarsDirectory.
		:rtype: unicode
		"""

		return self.__grammarsDirectory

	@grammarsDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def grammarsDirectory(self, value):
		"""
		Setter for **self.__grammarsDirectory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "grammarsDirectory"))

	@grammarsDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def grammarsDirectory(self):
		"""
		Deleter for **self.__grammarsDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "grammarsDirectory"))

	@property
	def extension(self):
		"""
		Property for **self.__extension** attribute.

		:return: self.__extension.
		:rtype: unicode
		"""

		return self.__extension

	@extension.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def extension(self, value):
		"""
		Setter for **self.__extension** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "extension"))

	@extension.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def extension(self):
		"""
		Deleter for **self.__extension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "extension"))

	@property
	def model(self):
		"""
		Property for **self.__model** attribute.

		:return: self.__model.
		:rtype: ProjectsModel
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		Setter for **self.__model** attribute.

		:param value: Attribute value.
		:type value: ProjectsModel
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		Deleter for **self.__model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

	@property
	def languagesModel(self):
		"""
		Property for **self.__languagesModel** attribute.

		:return: self.__languagesModel.
		:rtype: LanguagesModel
		"""

		return self.__languagesModel

	@languagesModel.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def languagesModel(self, value):
		"""
		Setter for **self.__languagesModel** attribute.

		:param value: Attribute value.
		:type value: LanguagesModel
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "languagesModel"))

	@languagesModel.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def languagesModel(self):
		"""
		Deleter for **self.__languagesModel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "languagesModel"))

	@property
	def defaultProject(self):
		"""
		Property for **self.__defaultProject** attribute.

		:return: self.__defaultProject.
		:rtype: unicode
		"""

		return self.__defaultProject

	@defaultProject.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultProject(self, value):
		"""
		Setter for **self.__defaultProject** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultProject"))

	@defaultProject.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultProject(self):
		"""
		Deleter for **self.__defaultProject** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultProject"))

	@property
	def defaultLanguage(self):
		"""
		Property for **self.__defaultLanguage** attribute.

		:return: self.__defaultLanguage.
		:rtype: unicode
		"""

		return self.__defaultLanguage

	@defaultLanguage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultLanguage(self, value):
		"""
		Setter for **self.__defaultLanguage** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultLanguage"))

	@defaultLanguage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultLanguage(self):
		"""
		Deleter for **self.__defaultLanguage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultLanguage"))

	@property
	def defaultScriptLanguage(self):
		"""
		Property for **self.__defaultScriptLanguage** attribute.

		:return: self.__defaultScriptLanguage.
		:rtype: unicode
		"""

		return self.__defaultScriptLanguage

	@defaultScriptLanguage.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultScriptLanguage(self, value):
		"""
		Setter for **self.__defaultScriptLanguage** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultScriptLanguage"))

	@defaultScriptLanguage.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultScriptLanguage(self):
		"""
		Deleter for **self.__defaultScriptLanguage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultScriptLanguage"))

	@property
	def defaultFileName(self):
		"""
		Property for **self.__defaultFileName** attribute.

		:return: self.__defaultFileName.
		:rtype: unicode
		"""

		return self.__defaultFileName

	@defaultFileName.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultFileName(self, value):
		"""
		Setter for **self.__defaultFileName** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultFileName"))

	@defaultFileName.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultFileName(self):
		"""
		Deleter for **self.__defaultFileName** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultFileName"))

	@property
	def defaultFileExtension(self):
		"""
		Property for **self.__defaultFileExtension** attribute.

		:return: self.__defaultFileExtension.
		:rtype: unicode
		"""

		return self.__defaultFileExtension

	@defaultFileExtension.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultFileExtension(self, value):
		"""
		Setter for **self.__defaultFileExtension** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultFileExtension"))

	@defaultFileExtension.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultFileExtension(self):
		"""
		Deleter for **self.__defaultFileExtension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultFileExtension"))

	@property
	def defaultWindowTitle(self):
		"""
		Property for **self.__defaultWindowTitle** attribute.

		:return: self.__defaultWindowTitle.
		:rtype: unicode
		"""

		return self.__defaultWindowTitle

	@defaultWindowTitle.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultWindowTitle(self, value):
		"""
		Setter for **self.__defaultWindowTitle** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultWindowTitle"))

	@defaultWindowTitle.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultWindowTitle(self):
		"""
		Deleter for **self.__defaultWindowTitle** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultWindowTitle"))

	@property
	def defaultScriptEditorDirectory(self):
		"""
		Property for **self.__defaultScriptEditorDirectory** attribute.

		:return: self.__defaultScriptEditorDirectory.
		:rtype: unicode
		"""

		return self.__defaultScriptEditorDirectory

	@defaultScriptEditorDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultScriptEditorDirectory(self, value):
		"""
		Setter for **self.__defaultScriptEditorDirectory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultScriptEditorDirectory"))

	@defaultScriptEditorDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultScriptEditorDirectory(self):
		"""
		Deleter for **self.__defaultScriptEditorDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultScriptEditorDirectory"))

	@property
	def defaultSessionDirectory(self):
		"""
		Property for **self.__defaultSessionDirectory** attribute.

		:return: self.__defaultSessionDirectory.
		:rtype: unicode
		"""

		return self.__defaultSessionDirectory

	@defaultSessionDirectory.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultSessionDirectory(self, value):
		"""
		Setter for **self.__defaultSessionDirectory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultSessionDirectory"))

	@defaultSessionDirectory.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultSessionDirectory(self):
		"""
		Deleter for **self.__defaultSessionDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultSessionDirectory"))

	@property
	def defaultScriptEditorFile(self):
		"""
		Property for **self.__defaultScriptEditorFile** attribute.

		:return: self.__defaultScriptEditorFile.
		:rtype: unicode
		"""

		return self.__defaultScriptEditorFile

	@defaultScriptEditorFile.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultScriptEditorFile(self, value):
		"""
		Setter for **self.__defaultScriptEditorFile** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultScriptEditorFile"))

	@defaultScriptEditorFile.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultScriptEditorFile(self):
		"""
		Deleter for **self.__defaultScriptEditorFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultScriptEditorFile"))

	@property
	def factoryDefaultScriptEditorFile(self):
		"""
		Property for **self.__factoryDefaultScriptEditorFile** attribute.

		:return: self.__factoryDefaultScriptEditorFile.
		:rtype: unicode
		"""

		return self.__factoryDefaultScriptEditorFile

	@factoryDefaultScriptEditorFile.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def factoryDefaultScriptEditorFile(self, value):
		"""
		Setter for **self.__factoryDefaultScriptEditorFile** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factoryDefaultScriptEditorFile"))

	@factoryDefaultScriptEditorFile.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def factoryDefaultScriptEditorFile(self):
		"""
		Deleter for **self.__factoryDefaultScriptEditorFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factoryDefaultScriptEditorFile"))

	@property
	def scriptEditorFile(self):
		"""
		Property for **self.__scriptEditorFile** attribute.

		:return: self.__scriptEditorFile.
		:rtype: unicode
		"""

		return self.__scriptEditorFile

	@scriptEditorFile.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def scriptEditorFile(self, value):
		"""
		Setter for **self.__scriptEditorFile** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"scriptEditorFile", value)
		self.__scriptEditorFile = value

	@scriptEditorFile.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def scriptEditorFile(self):
		"""
		Deleter for **self.__scriptEditorFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "scriptEditorFile"))

	@property
	def maximumRecentFiles(self):
		"""
		Property for **self.__maximumRecentFiles** attribute.

		:return: self.__maximumRecentFiles.
		:rtype: int
		"""

		return self.__maximumRecentFiles

	@maximumRecentFiles.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def maximumRecentFiles(self, value):
		"""
		Setter for **self.__maximumRecentFiles** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "maximumRecentFiles"))

	@maximumRecentFiles.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def maximumRecentFiles(self):
		"""
		Deleter for **self.__maximumRecentFiles** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "maximumRecentFiles"))

	@property
	def recentFilesActions(self):
		"""
		Property for **self.__recentFilesActions** attribute.

		:return: self.__recentFilesActions.
		:rtype: list
		"""

		return self.__recentFilesActions

	@recentFilesActions.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def recentFilesActions(self, value):
		"""
		Setter for **self.__recentFilesActions** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "recentFilesActions"))

	@recentFilesActions.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def recentFilesActions(self):
		"""
		Deleter for **self.__recentFilesActions** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "recentFilesActions"))

	@property
	def searchAndReplace(self):
		"""
		Property for **self.__searchAndReplace** attribute.

		:return: self.__searchAndReplace.
		:rtype: SearchAndReplace
		"""

		return self.__searchAndReplace

	@searchAndReplace.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def searchAndReplace(self, value):
		"""
		Setter for **self.__searchAndReplace** attribute.

		:param value: Attribute value.
		:type value: SearchAndReplace
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "searchAndReplace"))

	@searchAndReplace.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def searchAndReplace(self):
		"""
		Deleter for **self.__searchAndReplace** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchAndReplace"))

	@property
	def searchInFiles(self):
		"""
		Property for **self.__searchInFiles** attribute.

		:return: self.__searchInFiles.
		:rtype: SearchInFiles
		"""

		return self.__searchInFiles

	@searchInFiles.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def searchInFiles(self, value):
		"""
		Setter for **self.__searchInFiles** attribute.

		:param value: Attribute value.
		:type value: SearchInFiles
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "searchInFiles"))

	@searchInFiles.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def searchInFiles(self):
		"""
		Deleter for **self.__searchInFiles** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchInFiles"))

	@property
	def indentWidth(self):
		"""
		Property for **self.__indentWidth** attribute.

		:return: self.__indentWidth.
		:rtype: int
		"""

		return self.__indentWidth

	@indentWidth.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def indentWidth(self, value):
		"""
		Setter for **self.__indentWidth** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "indentWidth"))

	@indentWidth.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def indentWidth(self):
		"""
		Deleter for **self.__indentWidth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "indentWidth"))

	@property
	def defaultFontsSettings(self):
		"""
		Property for **self.__defaultFontsSettings** attribute.

		:return: self.__defaultFontsSettings.
		:rtype: dict
		"""

		return self.__defaultFontsSettings

	@defaultFontsSettings.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultFontsSettings(self, value):
		"""
		Setter for **self.__defaultFontsSettings** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultFontsSettings"))

	@defaultFontsSettings.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultFontsSettings(self):
		"""
		Deleter for **self.__defaultFontsSettings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultFontsSettings"))

	@property
	def console(self):
		"""
		Property for **self.__console** attribute.

		:return: self.__console.
		:rtype: dict
		"""

		return self.__console

	@console.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def console(self, value):
		"""
		Setter for **self.__console** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "console"))

	@console.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def console(self):
		"""
		Deleter for **self.__console** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "console"))

	@property
	def memoryHandlerStackDepth(self):
		"""
		Property for **self.__memoryHandlerStackDepth** attribute.

		:return: self.__memoryHandlerStackDepth.
		:rtype: int
		"""

		return self.__memoryHandlerStackDepth

	@memoryHandlerStackDepth.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def memoryHandlerStackDepth(self, value):
		"""
		Setter for **self.__memoryHandlerStackDepth** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "memoryHandlerStackDepth"))

	@memoryHandlerStackDepth.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def memoryHandlerStackDepth(self):
		"""
		Deleter for **self.__memoryHandlerStackDepth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "memoryHandlerStackDepth"))

	@property
	def menuBar(self):
		"""
		Property for **self.__menuBar** attribute.

		:return: self.__menuBar.
		:rtype: QToolbar
		"""

		return self.__menuBar

	@menuBar.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def menuBar(self, value):
		"""
		Setter for **self.__menuBar** attribute.

		:param value: Attribute value.
		:type value: QToolbar
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "menuBar"))

	@menuBar.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def menuBar(self):
		"""
		Deleter for **self.__menuBar** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "menuBar"))

	@property
	def fileMenu(self):
		"""
		Property for **self.__fileMenu** attribute.

		:return: self.__fileMenu.
		:rtype: QMenu
		"""

		return self.__fileMenu

	@fileMenu.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def fileMenu(self, value):
		"""
		Setter for **self.__fileMenu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "fileMenu"))

	@fileMenu.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def fileMenu(self):
		"""
		Deleter for **self.__fileMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "fileMenu"))

	@property
	def editMenu(self):
		"""
		Property for **self.__editMenu** attribute.

		:return: self.__editMenu.
		:rtype: QMenu
		"""

		return self.__editMenu

	@editMenu.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def editMenu(self, value):
		"""
		Setter for **self.__editMenu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "editMenu"))

	@editMenu.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def editMenu(self):
		"""
		Deleter for **self.__editMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "editMenu"))

	@property
	def sourceMenu(self):
		"""
		Property for **self.__sourceMenu** attribute.

		:return: self.__sourceMenu.
		:rtype: QMenu
		"""

		return self.__sourceMenu

	@sourceMenu.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def sourceMenu(self, value):
		"""
		Setter for **self.__sourceMenu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "sourceMenu"))

	@sourceMenu.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def sourceMenu(self):
		"""
		Deleter for **self.__sourceMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "sourceMenu"))

	@property
	def navigateMenu(self):
		"""
		Property for **self.__navigateMenu** attribute.

		:return: self.__navigateMenu.
		:rtype: QMenu
		"""

		return self.__navigateMenu

	@navigateMenu.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def navigateMenu(self, value):
		"""
		Setter for **self.__navigateMenu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "navigateMenu"))

	@navigateMenu.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def navigateMenu(self):
		"""
		Deleter for **self.__navigateMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "navigateMenu"))

	@property
	def searchMenu(self):
		"""
		Property for **self.__searchMenu** attribute.

		:return: self.__searchMenu.
		:rtype: QMenu
		"""

		return self.__searchMenu

	@searchMenu.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def searchMenu(self, value):
		"""
		Setter for **self.__searchMenu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "searchMenu"))

	@searchMenu.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def searchMenu(self):
		"""
		Deleter for **self.__searchMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchMenu"))

	@property
	def commandMenu(self):
		"""
		Property for **self.__commandMenu** attribute.

		:return: self.__commandMenu.
		:rtype: QMenu
		"""

		return self.__commandMenu

	@commandMenu.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def commandMenu(self, value):
		"""
		Setter for **self.__commandMenu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "commandMenu"))

	@commandMenu.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def commandMenu(self):
		"""
		Deleter for **self.__commandMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "commandMenu"))

	@property
	def viewMenu(self):
		"""
		Property for **self.__viewMenu** attribute.

		:return: self.__viewMenu.
		:rtype: QMenu
		"""

		return self.__viewMenu

	@viewMenu.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def viewMenu(self, value):
		"""
		Setter for **self.__viewMenu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "viewMenu"))

	@viewMenu.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def viewMenu(self):
		"""
		Deleter for **self.__viewMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "viewMenu"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def activate(self, engine):
		"""
		Activates the Component.

		:param engine: Container to attach the Component to.
		:type engine: QObject
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = engine
		self.__settings = self.__engine.settings
		self.__settingsSection = self.name

		self.__defaultScriptEditorDirectory = os.path.join(self.__engine.userApplicationDataDirectory,
															Constants.ioDirectory,
															self.__defaultScriptEditorDirectory)
		not foundations.common.pathExists(self.__defaultScriptEditorDirectory) and \
		os.makedirs(self.__defaultScriptEditorDirectory)
		self.__defaultSessionDirectory = os.path.join(self.__defaultScriptEditorDirectory, self.__defaultSessionDirectory)
		not foundations.common.pathExists(self.__defaultSessionDirectory) and os.makedirs(self.__defaultSessionDirectory)
		self.__defaultScriptEditorFile = os.path.join(self.__defaultScriptEditorDirectory,
													self.__defaultScriptEditorFile)

		self.__console = code.InteractiveConsole(self.__engine.locals)

		self.activated = True
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		Deactivates the Component.

		:return: Method success.
		:rtype: bool
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

	def initializeUi(self):
		"""
		Initializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__model = ProjectsModel(self, defaultProject=self.__defaultProject)

		self.Script_Editor_tabWidget = ScriptEditor_QTabWidget(self.__engine)
		self.Script_Editor_tabWidget_frame_gridLayout.addWidget(self.Script_Editor_tabWidget, 0, 0)
		self.__Script_Editor_tabWidget_setUi()

		self.__recentFilesActions = []
		for i in range(self.__maximumRecentFiles):
			self.__recentFilesActions.append(QAction(self.__menuBar,
													visible=False,
													triggered=self.__loadRecentFile__triggered))

		self.__menuBar = QMenuBar()
		self.__menuBar.setNativeMenuBar(False)
		self.menuBar_frame_gridLayout.addWidget(self.__menuBar)
		# Qt 4.8.4: Needs to show the menuBar, otherwise it doesn't appear.
		self.__menuBar.show()
		self.__initializeMenuBar()

		self.Script_Editor_Output_plainTextEdit.setParent(None)
		self.Script_Editor_Output_plainTextEdit = Basic_QPlainTextEdit(self)
		self.Script_Editor_Output_plainTextEdit_frame_gridLayout.addWidget(
		self.Script_Editor_Output_plainTextEdit, 0, 0)
		self.Script_Editor_Output_plainTextEdit.setObjectName("Script_Editor_Output_plainTextEdit")
		self.__Script_Editor_Output_plainTextEdit_setUi()

		self.__searchAndReplace = SearchAndReplace(self, Qt.Window)
		self.__searchInFiles = SearchInFiles(self, Qt.Window)

		self.__initializeLanguagesModel()

		self.Editor_Status_editorStatus = EditorStatus(self)
		self.__engine.statusBar.insertPermanentWidget(0, self.Editor_Status_editorStatus)

		Editor.getUntitledFileName = self.__getUntitledFileName

		# Signals / Slots.
		self.__engine.timer.timeout.connect(self.__Script_Editor_Output_plainTextEdit_refreshUi)
		self.__engine.contentDropped.connect(self.__engine__contentDropped)
		self.__engine.layoutsManager.layoutRestored.connect(self.__engine_layoutsManager__layoutRestored)
		self.__engine.fileSystemEventsManager.fileChanged.connect(self.__engine_fileSystemEventsManager__fileChanged)
		self.__engine.fileSystemEventsManager.fileInvalidated.connect(
		self.__engine_fileSystemEventsManager__fileInvalidated)
		self.__engine.fileSystemEventsManager.directoryChanged.connect(
		self.__engine_fileSystemEventsManager__directoryChanged)
		self.__engine.fileSystemEventsManager.directoryInvalidated.connect(
		self.__engine_fileSystemEventsManager__directoryInvalidated)
		self.Script_Editor_tabWidget.tabCloseRequested.connect(self.__Script_Editor_tabWidget__tabCloseRequested)
		self.Script_Editor_tabWidget.currentChanged.connect(self.__Script_Editor_tabWidget__currentChanged)
		self.Script_Editor_tabWidget.contentDropped.connect(self.__Script_Editor_tabWidget__contentDropped)
		self.Script_Editor_tabWidget.tabBar().tabMoved.connect(self.__Script_Editor_tabWidget_tabBar__tabMoved)
		self.visibilityChanged.connect(self.__scriptEditor__visibilityChanged)
		self.uiRefresh.connect(self.__Script_Editor_Output_plainTextEdit_refreshUi)
		self.recentFilesChanged.connect(self.__setRecentFilesActions)
		self.__model.fileRegistered.connect(self.__model__fileRegistered)
		self.__model.fileUnregistered.connect(self.__model__fileUnregistered)
		self.__model.directoryRegistered.connect(self.__model__directoryRegistered)
		self.__model.directoryUnregistered.connect(self.__model__directoryUnregistered)
		self.__model.projectRegistered.connect(self.__model__projectRegistered)
		self.__model.projectUnregistered.connect(self.__model__projectUnregistered)
		self.__model.editorRegistered.connect(self.__model__editorRegistered)
		self.__model.editorUnregistered.connect(self.__model__editorUnregistered)

		self.initializedUi = True
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		Uninitializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

	def addWidget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	def removeWidget(self):
		"""
		Removes the Component Widget from the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.removeDockWidget(self)
		self.setParent(None)

		return True

	def onStartup(self):
		"""
		Defines the slot triggered on Framework startup.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onStartup' method.".format(self.__class__.__name__))

		factoryDefaultScriptEditorFile = umbra.ui.common.getResourcePath(self.__factoryDefaultScriptEditorFile)
		if foundations.common.pathExists(factoryDefaultScriptEditorFile) and \
		not foundations.common.pathExists(self.__defaultScriptEditorFile):
			shutil.copyfile(factoryDefaultScriptEditorFile, self.__defaultScriptEditorFile)

		if foundations.common.pathExists(self.__defaultScriptEditorFile):
			self.loadFile(self.__defaultScriptEditorFile)
		else:
			self.newFile()

		startupScript = self.__engine.parameters.startupScript
		if foundations.common.pathExists(startupScript):
			self.loadFile(startupScript) and self.evaluateScript()

		self.restoreSession()

		for argument in self.__engine.arguments[1:]:
			file = os.path.abspath(argument)
			if foundations.common.pathExists(file):
				os.path.isfile(file) and self.loadFile(file)

		return True

	def onClose(self):
		"""
		Defines the slot triggered on Framework close.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onClose' method.".format(self.__class__.__name__))

		map(self.unregisterFile, self.listFiles())

		if self.storeSession() and self.closeAllFiles(leaveFirstEditor=False):
			return True

	def __initializeMenuBar(self):
		"""
		Initializes Component menuBar.
		"""

		self.__fileMenu = QMenu("&File", parent=self.__menuBar)
		self.__fileMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&File|&New",
		shortcut=QKeySequence.New,
		slot=self.__newFileAction__triggered))
		self.__fileMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&File|&Load ...",
		shortcut=QKeySequence.Open,
		slot=self.__loadFileAction__triggered))
		self.__fileMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&File|Source ...",
		slot=self.__sourceFileAction__triggered))
		self.__fileMenu.addSeparator()
		self.__fileMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&File|Add Project ...",
		slot=self.__addProjectAction__triggered))
		self.__fileMenu.addSeparator()
		self.__fileMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&File|&Save",
		shortcut=QKeySequence.Save,
		slot=self.__saveFileAction__triggered))
		self.__fileMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&File|Save As ...",
		shortcut=QKeySequence.SaveAs,
		slot=self.__saveFileAsAction__triggered))
		self.__fileMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&File|Save All",
		slot=self.__saveAllFilesAction__triggered))
		self.__fileMenu.addSeparator()
		self.__fileMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&File|Revert",
		slot=self.__revertFileAction__triggered))
		self.__fileMenu.addSeparator()
		self.__fileMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&File|Close ...",
		shortcut=QKeySequence.Close,
		slot=self.__closeFileAction__triggered))
		self.__fileMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&File|Close All ...",
		shortcut=Qt.SHIFT + Qt.ControlModifier + Qt.Key_W,
		slot=self.__closeAllFilesAction__triggered))
		self.__fileMenu.addSeparator()
		for action in self.__recentFilesActions:
			self.__fileMenu.addAction(action)
		self.__setRecentFilesActions()
		self.__menuBar.addMenu(self.__fileMenu)

		self.__editMenu = QMenu("&Edit", parent=self.__menuBar)
		self.__editMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Edit|&Undo",
		shortcut=QKeySequence.Undo,
		slot=self.__undoAction__triggered))
		self.__editMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Edit|&Redo",
		shortcut=QKeySequence.Redo,
		slot=self.__redoAction__triggered))
		self.__editMenu.addSeparator()
		self.__editMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Edit|Cu&t",
		shortcut=QKeySequence.Cut,
		slot=self.__cutAction__triggered))
		self.__editMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Edit|&Copy",
		shortcut=QKeySequence.Copy,
		slot=self.__copyAction__triggered))
		self.__editMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Edit|&Paste",
		shortcut=QKeySequence.Paste,
		slot=self.__pasteAction__triggered))
		self.__editMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Edit|Delete",
		slot=self.__deleteAction__triggered))
		self.__editMenu.addSeparator()
		self.__editMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Edit|Select All",
		shortcut=QKeySequence.SelectAll,
		slot=self.__selectAllAction__triggered))
		self.__menuBar.addMenu(self.__editMenu)

		self.__sourceMenu = QMenu("&Source", parent=self.__menuBar)
		self.__sourceMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Source|Delete Line(s)",
		shortcut=Qt.ControlModifier + Qt.Key_D,
		slot=self.__deleteLinesAction__triggered))
		self.__sourceMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Source|Duplicate Line(s)",
		shortcut=Qt.SHIFT + Qt.ControlModifier + Qt.Key_D,
		slot=self.__duplicateLinesAction__triggered))
		self.__sourceMenu.addSeparator()
		self.__sourceMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Source|Move Up",
		shortcut=Qt.SHIFT + Qt.ControlModifier + Qt.ALT + Qt.Key_Up,
		slot=self.__moveUpAction__triggered))
		self.__sourceMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Source|Move Down",
		shortcut=Qt.SHIFT + Qt.ControlModifier + Qt.ALT + Qt.Key_Down,
		slot=self.__moveDownAction__triggered))
		self.__sourceMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Source|Indent Selection",
		shortcut=Qt.Key_Tab,
		slot=self.__indentSelectionAction__triggered))
		self.__sourceMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Source|Unindent Selection",
		shortcut=Qt.Key_Backtab,
		slot=self.__unindentSelectionAction__triggered))
		self.__sourceMenu.addSeparator()
		self.__sourceMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Source|Convert Indentation To Tabs",
		slot=self.__convertIndentationToTabsAction__triggered))
		self.__sourceMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Source|Convert Indentation To Spaces",
		slot=self.__convertIndentationToSpacesAction__triggered))
		self.__sourceMenu.addSeparator()
		self.__sourceMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Source|Remove Trailing WhiteSpaces",
		slot=self.__removeTrailingWhiteSpacesAction__triggered))
		self.__sourceMenu.addSeparator()
		self.__sourceMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Source|Toggle Comments",
		shortcut=Qt.ControlModifier + Qt.Key_Slash,
		slot=self.__toggleCommentsAction__triggered))
		self.__menuBar.addMenu(self.__sourceMenu)

		self.__navigateMenu = QMenu("&Navigate", parent=self.__menuBar)
		self.__navigateMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Navigate|Goto Line ...",
		shortcut=Qt.ControlModifier + Qt.Key_L,
		slot=self.__gotoLineAction__triggered))
		self.__navigateMenu.addSeparator()
		self.__menuBar.addMenu(self.__navigateMenu)

		self.__searchMenu = QMenu("&Search", parent=self.__menuBar)
		self.__searchMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Search|Search And Replace ...",
		shortcut=Qt.ControlModifier + Qt.Key_F,
		slot=self.__searchAndReplaceAction__triggered))
		self.__searchMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Search|Search In Files ...",
		shortcut=Qt.ALT + Qt.ControlModifier + Qt.Key_F,
		slot=self.__searchInFilesAction__triggered))
		self.__searchMenu.addSeparator()
		self.__searchMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Search|Search Next",
		shortcut=Qt.ControlModifier + Qt.Key_K,
		slot=self.__searchNextAction__triggered))
		self.__searchMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Search|Search Previous",
		shortcut=Qt.SHIFT + Qt.ControlModifier + Qt.Key_K,
		slot=self.__searchPreviousAction__triggered))
		self.__menuBar.addMenu(self.__searchMenu)

		self.__commandMenu = QMenu("&Command", parent=self.__menuBar)
		self.__commandMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Command|&Evaluate Selection",
		shortcut=Qt.ControlModifier + Qt.Key_Return,
		slot=self.__evaluateSelectionAction__triggered))
		self.__commandMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&Command|Evaluate &Script",
		shortcut=Qt.SHIFT + Qt.CTRL + Qt.Key_Return,
		slot=self.__evaluateScriptAction__triggered))
		self.__menuBar.addMenu(self.__commandMenu)

		self.__viewMenu = QMenu("&View", parent=self.__menuBar)
		self.__viewMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&View|Increase Font Size",
		shortcut=Qt.ControlModifier + Qt.Key_Plus,
		slot=self.__increaseFontSizeAction__triggered))
		self.__viewMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&View|Decrease Font Size",
		shortcut=Qt.ControlModifier + Qt.Key_Minus,
		slot=self.__decreaseFontSizeAction__triggered))
		self.__viewMenu.addSeparator()
		self.__viewMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&View|Toggle Word Wrap",
		slot=self.__toggleWordWrapAction__triggered))
		self.__viewMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&View|Toggle White Spaces",
		slot=self.__toggleWhiteSpacesAction__triggered))
		self.__viewMenu.addSeparator()
		self.__viewMenu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|&View|Loop Through Editors",
		shortcut=Qt.AltModifier + Qt.SHIFT + Qt.Key_Tab,
		slot=self.__loopThroughEditorsAction__triggered))
		self.__menuBar.addMenu(self.__viewMenu)

	@foundations.trace.untracable
	def __Script_Editor_Output_plainTextEdit_setUi(self):
		"""
		Sets the **Script_Editor_Output_plainTextEdit** Widget.
		"""

		self.Script_Editor_Output_plainTextEdit.setReadOnly(True)
		self.Script_Editor_Output_plainTextEdit.highlighter = umbra.ui.highlighters.DefaultHighlighter(
																 self.Script_Editor_Output_plainTextEdit.document(),
																 LOGGING_LANGUAGE.rules,
																 LOGGING_LANGUAGE.theme)

		self.Script_Editor_Output_plainTextEdit.setTabStopWidth(self.__indentWidth)
		self.Script_Editor_Output_plainTextEdit.setWordWrapMode(QTextOption.NoWrap)
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			fontFamily, fontSize = self.__defaultFontsSettings["Windows"]
		elif platform.system() == "Darwin":
			fontFamily, fontSize = self.__defaultFontsSettings["Darwin"]
		elif platform.system() == "Linux":
			fontFamily, fontSize = self.__defaultFontsSettings["Linux"]
		font = QFont(fontFamily)
		font.setPointSize(fontSize)
		self.Script_Editor_Output_plainTextEdit.setFont(font)
		self.Script_Editor_Output_plainTextEdit.contextMenuEvent = \
		self.__Script_Editor_Output_plainTextEdit_contextMenuEvent
		self.__Script_Editor_Output_plainTextEdit_setDefaultViewState()

	@foundations.trace.untracable
	def __Script_Editor_Output_plainTextEdit_setDefaultViewState(self):
		"""
		Sets the **Script_Editor_Output_plainTextEdit** Widget default View state.
		"""

		self.Script_Editor_Output_plainTextEdit.moveCursor(QTextCursor.End)
		self.Script_Editor_Output_plainTextEdit.ensureCursorVisible()

	@foundations.trace.untracable
	def __Script_Editor_Output_plainTextEdit_refreshUi(self):
		"""
		Updates the **Script_Editor_Output_plainTextEdit** Widget.
		"""

		memoryHandlerStackDepth = len(self.__engine.loggingSessionHandlerStream.stream)
		if memoryHandlerStackDepth != self.__memoryHandlerStackDepth:
			for line in self.__engine.loggingSessionHandlerStream.stream[
			self.__memoryHandlerStackDepth:memoryHandlerStackDepth]:
				self.Script_Editor_Output_plainTextEdit.moveCursor(QTextCursor.End)
				self.Script_Editor_Output_plainTextEdit.insertPlainText(line)
			self.__Script_Editor_Output_plainTextEdit_setDefaultViewState()
			self.__memoryHandlerStackDepth = memoryHandlerStackDepth

	def __Script_Editor_Output_plainTextEdit_contextMenuEvent(self, event):
		"""
		Reimplements the :meth:`QPlainTextEdit.contextMenuEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		menu = self.Script_Editor_Output_plainTextEdit.createStandardContextMenu()
		menu.addSeparator()
		menu.addAction(self.__engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|Edit Selected Path",
		slot=self.__editSelectedPathAction__triggered))
		menu.exec_(event.globalPos())

	def __Script_Editor_tabWidget_setUi(self):
		"""
		Sets the **Script_Editor_tabWidget** Widget.
		"""

		self.Script_Editor_tabWidget.setTabsClosable(True)
		self.Script_Editor_tabWidget.setMovable(True)

	def __Script_Editor_tabWidget__tabCloseRequested(self, index):
		"""
		Defines the slot triggered by **Script_Editor_tabWidget** Widget when a tab is requested to be closed.

		:param index: Tab index.
		:type index: int
		"""

		LOGGER.debug("> Closing tab with index '{0}'.".format(index))

		self.Script_Editor_tabWidget.setCurrentIndex(index)
		return self.closeFile()

	def __Script_Editor_tabWidget__currentChanged(self, index):
		"""
		Defines the slot triggered by **Script_Editor_tabWidget** Widget when the current tab is changed.

		:param index: Tab index.
		:type index: int
		"""

		LOGGER.debug("> Current tab changed to '{0}' index.".format(index))

		self.Editor_Status_editorStatus._EditorStatus__Languages_comboBox_setDefaultViewState()
		self.__setWindowTitle()

	def __Script_Editor_tabWidget__contentDropped(self, event):
		"""
		Defines the slot triggered by content when dropped in the **Script_Editor_tabWidget** Widget.

		:param event: Event.
		:type event: QEvent
		"""

		self.__handleDroppedContent(event)

	def __Script_Editor_tabWidget_tabBar__tabMoved(self, toIndex, fromIndex):
		"""
		Defines the slot triggered by a **Script_Editor_tabWidget** Widget tab when moved.

		:param toIndex: Index to.
		:type toIndex: int
		:param fromIndex: Index from.
		:type fromIndex: int
		"""

		editor = self.getCurrentEditor()
		if not editor:
			return

		editorNode = foundations.common.getFirstItem(self.__model.getEditorNodes(editor))
		fileNode = editorNode.parent
		projectNode = fileNode.parent

		self.__model.moveNode(projectNode, fromIndex, toIndex)

	def __engine__contentDropped(self, event):
		"""
		Defines the slot triggered by content when dropped into the engine.

		:param event: Event.
		:type event: QEvent
		"""

		self.__handleDroppedContent(event)

	def __engine_layoutsManager__layoutRestored(self, currentLayout):
		"""
		Defines the slot triggered by the engine layout when changed.

		:param currentLayout: Current layout.
		:type currentLayout: unicode
		"""

		self.Editor_Status_editorStatus.setVisible(not self.isHidden())

	def __engine_fileSystemEventsManager__fileChanged(self, file):
		"""
		Defines the slot triggered by the **fileSystemEventsManager** when a file is changed.

		:param file: File changed.
		:type file: unicode
		"""

		file = foundations.strings.toString(file)
		self.searchInFiles._SearchInFiles__uncache(file)
		self.reloadFile(file)

	def __engine_fileSystemEventsManager__fileInvalidated(self, file):
		"""
		Defines the slot triggered by the **fileSystemEventsManager** when a file is invalidated.

		:param file: File changed.
		:type file: unicode
		"""

		file = foundations.strings.toString(file)
		self.searchInFiles._SearchInFiles__uncache(file)
		editor = self.getEditor(file)
		editor and	editor.setModified(True)

	def __engine_fileSystemEventsManager__directoryChanged(self, directory):
		"""
		Defines the slot triggered by the **fileSystemEventsManager** when a directory is changed.

		:param directory: Directory changed.
		:type directory: unicode
		"""

		for projectNode in self.__model.listProjectNodes():
			if projectNode.path == directory:
				self.__model.updateProjectNodes(projectNode)
			else:
				for node in foundations.walkers.nodesWalker(projectNode):
					if node.path == directory:
						self.__model.updateProjectNodes(node)
						break

	def __engine_fileSystemEventsManager__directoryInvalidated(self, directory):
		"""
		Defines the slot triggered by the **fileSystemEventsManager** when a directory is invalidated.

		:param directory: Directory invalidated.
		:type directory: unicode
		"""

		for projectNode in self.__model.listProjectNodes():
			if projectNode.path == directory:
				self.__model.unregisterProject(projectNode)
				break

	def __scriptEditor__visibilityChanged(self, visibility):
		"""
		Defines the slot triggered by the **scriptEditor** Component when visibility changed.

		:param visibility: Widget visibility.
		:type visibility: bool
		"""

		self.Editor_Status_editorStatus.setVisible(visibility)

	def __newFileAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|&New'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.newFile()

	def __model__fileRegistered(self, fileNode):
		"""
		Defines the slot triggered by Model when a file is registered.

		:param fileNode: Registered file FileNode.
		:type fileNode: FileNode
		"""

		self.registerNodePath(fileNode)

	def __model__fileUnregistered(self, fileNode):
		"""
		Defines the slot triggered by Model when a file is unregistered.

		:param fileNode: Unregistered file FileNode.
		:type fileNode: FileNode
		"""

		self.unregisterNodePath(fileNode)

	def __model__directoryRegistered(self, directoryNode):
		"""
		Defines the slot triggered by Model when a directory is registered.

		:param directoryNode: Registered directory DirectoryNode.
		:type directoryNode: DirectoryNode
		"""

		self.registerNodePath(directoryNode)

	def __model__directoryUnregistered(self, directoryNode):
		"""
		Defines the slot triggered by Model when a directory is unregistered.

		:param directoryNode: Unregistered directory DirectoryNode.
		:type directoryNode: DirectoryNode
		"""

		self.unregisterNodePath(directoryNode)

	def __model__projectRegistered(self, projectNode):
		"""
		Defines the slot triggered by Model when a project is registered.

		:param projectNode: Registered project ProjectNode.
		:type projectNode: ProjectNode
		"""

		self.registerNodePath(projectNode)

	def __model__projectUnregistered(self, projectNode):
		"""
		Defines the slot triggered by Model when a project is unregistered.

		:param projectNode: Unregistered project ProjectNode.
		:type projectNode: ProjectNode
		"""

		self.unregisterNodePath(projectNode)

	def __model__editorRegistered(self, editorNode):
		"""
		Defines the slot triggered by Model when an editor is registered.

		:param editorNode: Registered editor EditorNode.
		:type editorNode: EditorNode
		"""

		self.addEditorTab(editorNode.editor)

	def __model__editorUnregistered(self, editorNode):
		"""
		Defines the slot triggered by Model when an editor is unregistered.

		:param editorNode: Unregistered editor EditorNode.
		:type editorNode: EditorNode
		"""

		self.removeEditorTab(editorNode.editor)

	def __loadFileAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|&Load ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.loadFileUi()

	def __sourceFileAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|Source ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if self.loadFileUi():
			return self.evaluateScript()

	def __addProjectAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|Add Project ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.addProjectUi()

	def __saveFileAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|&Save'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.saveFile()

	def __saveFileAsAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|Save As ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.saveFileAs()

	def __saveAllFilesAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|Save All'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.saveAllFiles()

	def __revertFileAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|Revert'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.revertFile()

	def __closeFileAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|Close ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.closeFile()

	def __closeAllFilesAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|Close All ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.closeAllFiles()

	def __loadRecentFile__triggered(self, checked):
		"""
		Defines the slot triggered by any recent file related action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		file = self.sender().data
		if foundations.common.pathExists(file):
			return self.loadFile(file)

	def __undoAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Undo'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.hasEditorTab():
			return False

		self.getCurrentEditor().undo()
		return True

	def __redoAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Redo'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.hasEditorTab():
			return False

		self.getCurrentEditor().redo()
		return True

	def __cutAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|Cu&t'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		currentWidget = self.getFocusWidget()
		if not currentWidget:
			return False

		if currentWidget.objectName() == "Script_Editor_Output_plainTextEdit":
			currentWidget.copy()
		else:
			currentWidget.cut()
		return True

	def __copyAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Copy'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		currentWidget = self.getFocusWidget()
		if not currentWidget:
			return False

		currentWidget.copy()
		return True

	def __pasteAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Paste'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.hasEditorTab():
			return False

		self.getCurrentEditor().paste()
		return True

	def __deleteAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|Delete'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.hasEditorTab():
			return False

		self.getCurrentEditor().delete()
		return True

	def __selectAllAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|Select All'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		currentWidget = self.getFocusWidget()
		if not currentWidget:
			return False

		currentWidget.selectAll()
		return True

	def __deleteLinesAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Source|Delete Line(s)'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.hasEditorTab():
			return False

		return self.getCurrentEditor().deleteLines()

	def __duplicateLinesAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Source|Duplicate Line(s)'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.hasEditorTab():
			return False

		return self.getCurrentEditor().duplicateLines()

	def __moveUpAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Source|Move Up'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.hasEditorTab():
			return False

		return self.getCurrentEditor().moveLinesUp()

	def __moveDownAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Source|Move Down'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.hasEditorTab():
			return False

		return self.getCurrentEditor().moveLinesDown()

	def __indentSelectionAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Source|Indent Selection'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.hasEditorTab():
			return False

		return self.getCurrentEditor().indent()

	def __unindentSelectionAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Source|Unindent Selection'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.hasEditorTab():
			return False

		return self.getCurrentEditor().unindent()

	def __convertIndentationToTabsAction__triggered(self, checked):
		"""
		Defines the slot triggered by
		**'Actions|Umbra|Components|factory.scriptEditor|&Source|Convert Identation To Tabs'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.hasEditorTab():
			return False

		return self.getCurrentEditor().convertIndentationToTabs()

	def __convertIndentationToSpacesAction__triggered(self, checked):
		"""
		Defines the slot triggered by
		**'Actions|Umbra|Components|factory.scriptEditor|&Source|Convert Identation To Spaces'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.hasEditorTab():
			return False

		return self.getCurrentEditor().convertIndentationToSpaces()

	def __removeTrailingWhiteSpacesAction__triggered(self, checked):
		"""
		Defines the slot triggered by
		**'Actions|Umbra|Components|factory.scriptEditor|&Source|Remove Trailing WhiteSpaces'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.hasEditorTab():
			return False

		return self.getCurrentEditor().removeTrailingWhiteSpaces()

	def __toggleCommentsAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Source|Toggle Comments'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.hasEditorTab():
			return False

		return self.getCurrentEditor().toggleComments()

	def __gotoLineAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Navigate|Goto Line ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.gotoLine()

	def __searchAndReplaceAction__triggered(self, checked):
		"""
		Defines the slot triggered by
		**'Actions|Umbra|Components|factory.scriptEditor|&Search|Search And Replace ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.searchAndReplaceUi()

	def __searchInFilesAction__triggered(self, checked):
		"""
		Defines the slot triggered by
		**'Actions|Umbra|Components|factory.scriptEditor|&Search|Search In Files ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.searchInFilesUi()

	def __searchNextAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Search|Search Next'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.hasEditorTab():
			return False

		return self.getCurrentEditor().searchNext()

	def __searchPreviousAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Search|Search Previous'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.hasEditorTab():
			return False

		return self.getCurrentEditor().searchPrevious()

	def __evaluateSelectionAction__triggered(self, checked):
		"""
		Defines the slot triggered by
		**'Actions|Umbra|Components|factory.scriptEditor|&Command|&Evaluate Selection'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.evaluateSelection()

	def __evaluateScriptAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Command|Evaluate &Script'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.evaluateScript()

	def __increaseFontSizeAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&View|Increase Font Size'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		currentWidget = self.getFocusWidget()
		if not currentWidget:
			return False

		return currentWidget.zoomIn()

	def __decreaseFontSizeAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&View|Decrease Font Size'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		currentWidget = self.getFocusWidget()
		if not currentWidget:
			return False

		return currentWidget.zoomOut()

	def __toggleWordWrapAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&View|Toggle Word Wrap'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		currentWidget = self.getFocusWidget()
		if not currentWidget:
			return False

		return currentWidget.toggleWordWrap()

	def __toggleWhiteSpacesAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&View|Toggle White Spaces'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		currentWidget = self.getFocusWidget()
		if not currentWidget:
			return False

		return currentWidget.toggleWhiteSpaces()

	def __loopThroughEditorsAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|&View|Loop Through Editors'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.loopThroughEditors()

	def __editSelectedPathAction__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.scriptEditor|Edit Selected Path'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.loadPath(foundations.strings.toString(self.Script_Editor_Output_plainTextEdit.getSelectedText()))

	def __editor__patternsReplaced(self, patterns):
		"""
		Defines the slot triggered by an editor when patterns have been replaced.
		"""

		replacedPatternsCount = len(patterns)
		replacedPatternsCount and self.__engine.notificationsManager.notify(
		"{0} | '{1}' pattern(s) replaced!".format(self.__class__.__name__, replacedPatternsCount))

	def __editor__titleChanged(self):
		"""
		Defines the slot triggered by an editor when title is changed.
		"""

		self.__setTabTitle(self.getEditorTab(self.sender()))
		self.__setWindowTitle()

	def __editor__fileLoaded(self):
		"""
		Defines the slot triggered by an editor when file is loaded.
		"""

		self.registerNodePath(self.sender())

	def __editor__fileSaved(self):
		"""
		Defines the slot triggered by an editor when file is saved.
		"""

		self.registerNodePath(self.sender())

	def __editor__languageChanged(self):
		"""
		Defines the slot triggered by an editor when language is changed.
		"""

		self.Editor_Status_editorStatus._EditorStatus__Languages_comboBox_setDefaultViewState()

	def __editor__modificationChanged(self, changed):
		"""
		Defines the slot triggered by an editor when document is modified.

		:param changed: File modification state.
		:type changed: bool
		"""

		if self.sender() is not None:
			self.searchInFiles._SearchInFiles__uncache(self.sender().file)

	def __initializeLanguagesModel(self):
		"""
		Initializes the languages Model.
		"""

		languages = [PYTHON_LANGUAGE, LOGGING_LANGUAGE, TEXT_LANGUAGE]
		existingGrammarFiles = [os.path.normpath(language.file) for language in languages]

		for directory in RuntimeGlobals.resourcesDirectories:
			for file in foundations.walkers.filesWalker(directory, ("\.{0}$".format(self.__extension),), ("\._",)):
				if os.path.normpath(file) in existingGrammarFiles:
					continue

				languageDescription = getLanguageDescription(file)
				if not languageDescription:
					continue

				LOGGER.debug("> Adding '{0}' language to model.".format(languageDescription))
				languages.append(languageDescription)

		self.__languagesModel = LanguagesModel(self, sorted(languages, key=lambda x: (x.name)))
		self.__getSupportedFileTypesString()

	@umbra.engine.encapsulateProcessing
	def __handleDroppedContent(self, event):
		"""
		Handles dopped content event.

		:param event: Content dropped event.
		:type event: QEvent
		"""

		if not event.mimeData().hasUrls():
			return

		urls = event.mimeData().urls()

		self.__engine.startProcessing("Loading Files ...", len(urls))
		for url in event.mimeData().urls():
			path = foundations.strings.toString(url.path())
			LOGGER.debug("> Handling dropped '{0}' file.".format(path))
			path = (platform.system() == "Windows" or platform.system() == "Microsoft") and \
			re.search(r"^\/[A-Z]:", path) and path[1:] or path
			self.loadPath(path) and self.restoreDevelopmentLayout()
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

	def __getSupportedFileTypesString(self):
		"""
		Returns the supported file types dialog string.
		"""

		languages = ["All Files (*)"]
		for language in self.__languagesModel.languages:
			languages.append("{0} Files ({1})".format(language.name,
													" ".join(language.extensions.split("|")).replace("\\", "*")))
		return ";;".join(languages)

	def __setRecentFilesActions(self):
		"""
		Sets the recent files actions.
		"""

		recentFiles = [foundations.strings.toString(file)
					for file in self.__settings.getKey(self.__settingsSection, "recentFiles").toStringList()
					if foundations.common.pathExists(file)]
		if not recentFiles:
			return

		numberRecentFiles = min(len(recentFiles), self.__maximumRecentFiles)

		for i in range(self.__maximumRecentFiles):
			if i >= numberRecentFiles:
				self.__recentFilesActions[i].setVisible(False)
				continue

			LOGGER.debug("> Adding '{0}' file to recent files actions.".format(recentFiles[i]))

			self.__recentFilesActions[i].setText("{0} {1}".format(i + 1, os.path.basename(
			foundations.strings.toString(recentFiles[i]))))
			self.__recentFilesActions[i].data = foundations.strings.toString(recentFiles[i])
			self.__recentFilesActions[i].setVisible(True)

	def __storeRecentFile(self, file):
		"""
		Stores given recent file into the settings.

		:param file: File to store.
		:type file: unicode
		"""

		LOGGER.debug("> Storing '{0}' file in recent files.".format(file))

		recentFiles = [foundations.strings.toString(recentFile)
					for recentFile in self.__settings.getKey(self.__settingsSection, "recentFiles").toStringList()
					if foundations.common.pathExists(recentFile)]
		if not recentFiles:
			recentFiles = []

		if file in recentFiles:
			recentFiles.pop(recentFiles.index(file))
		recentFiles.insert(0, file)
		del recentFiles[self.__maximumRecentFiles:]
		recentFiles = self.__settings.setKey(self.__settingsSection, "recentFiles", recentFiles)
		self.recentFilesChanged.emit()

	def __setWindowTitle(self):
		"""
		Sets the Component window title.
		"""

		if self.hasEditorTab():
			windowTitle = "{0} - {1}".format(self.__defaultWindowTitle, self.getCurrentEditor().file)
		else:
			windowTitle = "{0}".format(self.__defaultWindowTitle)

		LOGGER.debug("> Setting 'Script Editor' window title to '{0}'.".format(windowTitle))
		self.setWindowTitle(windowTitle)

	def __setTabTitle(self, index):
		"""
		Sets the name and toolTip of the **Script_Editor_tabWidget** Widget tab with given index.

		:param index: Index of the tab containing the Model editor.
		:type index: int
		"""

		editor = self.getWidget(index)
		if not editor:
			return

		title, toolTip = foundations.strings.toString(editor.title), foundations.strings.toString(editor.file)
		LOGGER.debug("> Setting '{0}' window title and '{1}' toolTip to tab with '{2}' index.".format(title, toolTip, index))
		# TODO: https://bugreports.qt-project.org/browse/QTBUG-27084
		color = QColor(224, 224, 224) if editor.isModified() else QColor(160, 160, 160)
		self.Script_Editor_tabWidget.tabBar().setTabTextColor(index, color)
		tabText = self.Script_Editor_tabWidget.tabText(index)
		tabText != title and self.Script_Editor_tabWidget.setTabText(index, title)
		self.Script_Editor_tabWidget.setTabToolTip(index, toolTip)

	def __hasEditorLock(self, editor):
		"""
		Returns if given editor has a lock.

		:param editor: Editor.
		:type editor: Editor
		:return: Has editor lock.
		:rtype: bool
		"""

		return hasattr(editor, "__lock")

	def __lockEditor(self, editor):
		"""
		Locks given editor.

		:param editor: Editor.
		:type editor: Editor
		"""

		setattr(editor, "__lock", True)

	def __unlockEditor(self, editor):
		"""
		Locks given editor.

		:param editor: Editor.
		:type editor: Editor
		"""

		delattr(editor, "__lock")

	def __getUntitledFileName(self):
		"""
		Returns an untitled file name.

		:return: Untitled file name.
		:rtype: unicode
		"""

		untitledNameId = Editor._Editor__untitledNameId
		for file in self.listFiles():
			if not os.path.dirname(file) == self.__defaultSessionDirectory:
				continue

			search = re.search(r"\d+", os.path.basename(file))
			if not search:
				continue

			untitledNameId = max(int(search.group(0)), untitledNameId) + 1

		name = "{0} {1}.{2}".format(self.__defaultFileName, untitledNameId, self.__defaultFileExtension)
		Editor._Editor__untitledNameId += 1
		LOGGER.debug("> Next untitled file name: '{0}'.".format(name))
		return name

	def registerFile(self, file):
		"""
		Registers given file in the **fileSystemEventsManager**.

		:param file: File.
		:type file: unicode
		:return: Method success.
		:rtype: bool
		"""

		not self.__engine.fileSystemEventsManager.isPathRegistered(file) and \
		self.__engine.fileSystemEventsManager.registerPath(file)
		return True

	def unregisterFile(self, file):
		"""
		Unregisters given file in the **fileSystemEventsManager**.

		:param file: File.
		:type file: unicode
		:return: Method success.
		:rtype: bool
		"""

		self.__engine.fileSystemEventsManager.isPathRegistered(file) and \
		self.__engine.fileSystemEventsManager.unregisterPath(file)
		return True

	def registerNodePath(self, node):
		"""
		Registers given Node path in the **fileSystemEventsManager**.

		:param node: Node.
		:type node: FileNode or DirectoryNode or ProjectNode
		:return: Method success.
		:rtype: bool
		"""

		path = node.file if hasattr(node, "file") else node.path
		path = foundations.strings.toString(path)
		if not foundations.common.pathExists(path):
			return False

		return self.registerFile(path)

	def unregisterNodePath(self, node):
		"""
		Unregisters given Node path from the **fileSystemEventsManager**.

		:param node: Node.
		:type node: FileNode or DirectoryNode or ProjectNode
		:return: Method success.
		:rtype: bool
		"""

		path = node.file if hasattr(node, "file") else node.path
		path = foundations.strings.toString(path)

		return self.unregisterFile(path)

	def loadFileUi(self):
		"""
		Loads user chosen file(s) into **Script_Editor_tabWidget** Widget tab Model editor(s).

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		editor = self.getCurrentEditor()
		file = editor and editor.file or None

		browsedPath = os.path.dirname(file) if foundations.common.pathExists(file) else RuntimeGlobals.lastBrowsedPath
		files = umbra.ui.common.storeLastBrowsedPath(QFileDialog.getOpenFileNames(self,
																				"Load File(s):",
																				browsedPath,
																				self.__getSupportedFileTypesString()))
		if not files:
			return False

		success = True
		for file in files:
			success *= self.loadFile(file)
		return success

	def addProjectUi(self):
		"""
		Adds user chosen project **Script_Editor_tabWidget** Widget tab Model.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		directory = umbra.ui.common.storeLastBrowsedPath(QFileDialog.getExistingDirectory(self,
																				"Add Project:",
																				RuntimeGlobals.lastBrowsedPath))
		if not directory:
			return False

		return self.addProject(directory)

	def searchAndReplaceUi(self):
		"""
		Performs a search and replace in the current **Script_Editor_tabWidget** Widget tab Model editor.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		self.__searchAndReplace.show()
		return True

	def searchInFilesUi(self):
		"""
		Performs a search in the current user chosen files.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		self.__searchInFiles.show()
		return True

	def getWidget(self, index):
		"""
		Returns the **Script_Editor_tabWidget** Widget associated with given index.

		:param index: Tab index.
		:type index: int
		:return: Widget.
		:rtype: QWidget
		"""

		if index is not None:
			return self.Script_Editor_tabWidget.widget(index)

	def getFocusWidget(self):
		"""
		Returns the Widget with focus.

		:return: Widget with focus.
		:rtype: QWidget
		"""

		currentWidget = QApplication.focusWidget()
		if currentWidget is None:
			return False

		if currentWidget.objectName() == "Script_Editor_Output_plainTextEdit" or \
			isinstance(currentWidget, Editor):
			return currentWidget

	def getEditorTab(self, editor):
		"""
		Returns the **Script_Editor_tabWidget** Widget tab associated with the given editor.

		:param editor: Editor to search tab for.
		:type editor: Editor
		:return: Tab index.
		:rtype: Editor
		"""

		for i in range(self.Script_Editor_tabWidget.count()):
			if not self.getWidget(i) == editor:
				continue

			LOGGER.debug("> Editor '{0}': Tab index '{1}'.".format(editor, i))
			return i

	def addEditorTab(self, editor):
		"""
		Adds a new tab to the **Script_Editor_tabWidget** Widget and sets the given editor as child widget.

		:param editor: Editor.
		:type editor: Editor
		:return: New tab index.
		:rtype: int
		"""

		index = self.Script_Editor_tabWidget.addTab(editor, editor.getFileShortName())
		LOGGER.debug("> Assigning '{0}' editor to '{1}' tab index.".format(editor, index))
		self.Script_Editor_tabWidget.setCurrentIndex(index)
		self.__setTabTitle(index)

		# Signals / Slots.
		editor.patternsReplaced.connect(self.__editor__patternsReplaced)
		editor.titleChanged.connect(self.__editor__titleChanged)
		editor.fileLoaded.connect(self.__editor__fileLoaded)
		editor.fileSaved.connect(self.__editor__fileSaved)
		editor.languageChanged.connect(self.__editor__languageChanged)
		editor.modificationChanged.connect(self.__editor__modificationChanged)
		editor.cursorPositionChanged.connect(self.Editor_Status_editorStatus._EditorStatus__editor__cursorPositionChanged)
		return index

	def removeEditorTab(self, editor):
		"""
		Removes the **Script_Editor_tabWidget** Widget tab with given editor.

		:param editor: Editor.
		:type editor: Editor
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing tab with Editor '{0}'.".format(editor))
		self.Script_Editor_tabWidget.removeTab(self.getEditorTab(editor))
		return True

	def findEditorTab(self, file):
		"""
		Finds the **Script_Editor_tabWidget** Widget tab associated to the given file.

		:param file: File to search tab for.
		:type file: unicode
		:return: Tab index.
		:rtype: Editor
		"""

		for i in range(self.Script_Editor_tabWidget.count()):
			if not self.getWidget(i).file == file:
				continue

			LOGGER.debug("> File '{0}': Tab index '{1}'.".format(file, i))
			return i

	def hasEditorTab(self):
		"""
		Returns if the **Script_Editor_tabWidget** Widget has at least one tab.

		:return: Has tab.
		:rtype: bool
		"""

		return self.Script_Editor_tabWidget.count() and True or False

	def getCurrentEditor(self):
		"""
		Returns the current **Script_Editor_tabWidget** Widget tab Model editor.

		:return: Current editor.
		:rtype: Editor
		"""

		if not self.hasEditorTab():
			return

		return self.Script_Editor_tabWidget.currentWidget()

	def setCurrentEditor(self, file):
		"""
		Focus the **Script_Editor_tabWidget** Widget tab Model editor with given file.

		:param file: File.
		:type file: unicode
		:return: Method success.
		:rtype: bool
		"""

		index = self.findEditorTab(file)
		if index is not None:
			self.Script_Editor_tabWidget.setCurrentIndex(index)
			return True

	def loadPath(self, path):
		"""
		Loads given path.

		:param path: Path to load.
		:type path: unicode
		:return: Method success.
		:rtype: bool
		"""

		if not foundations.common.pathExists(path):
			return False

		if os.path.isfile(path):
			if path in self.listFiles():
				self.setCurrentEditor(path)
			else:
				self.loadFile(path)
		else:
			if not path in self.listProjects():
				self.addProject(path)
		return True

	def loadDocument(self, document, file):
		"""
		Loads given document into a new **Script_Editor_tabWidget** Widget tab Model editor.

		:param document: Document to load.
		:type document: QTextDocument
		:param file: Document file.
		:type file: unicode
		:return: Method success.
		:rtype: bool
		"""

		if not foundations.common.pathExists(file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
			self.__class__.__name__, file))

		if self.getEditor(file):
			LOGGER.info("{0} | '{1}' is already loaded!".format(self.__class__.__name__, file))
			return True

		self.closeFirstFile()
		language = self.__languagesModel.getLanguage(self.__defaultLanguage)
		editor = Editor(parent=self, language=language)
		if not editor.newFile():
			return False

		LOGGER.info("{0} | Loading '{1}' file document!".format(self.__class__.__name__, file))
		language = self.__languagesModel.getFileLanguage(file) or self.__languagesModel.getLanguage(self.__defaultLanguage)
		if not editor.loadDocument(document, file, language):
			return False

		if self.__model.setAuthoringNodes(editor):
			self.__storeRecentFile(file)
			self.fileLoaded.emit(file)
			return True

	def addProject(self, path):
		"""
		Adds a project.

		:param path: Project path.
		:type path: unicode
		:return: Method success.
		:rtype: bool
		"""

		if not foundations.common.pathExists(path):
			return False

		path = os.path.normpath(path)
		if self.__model.getProjectNodes(path):
			self.__engine.notificationsManager.warnify(
			"{0} | '{1}' project is already opened!".format(self.__class__.__name__, path))
			return False

		LOGGER.info("{0} | Adding '{1}' project!".format(self.__class__.__name__, path))
		projectNode = self.__model.registerProject(path)
		if not projectNode:
			return False

		self.__model.setProjectNodes(projectNode)
		return True

	def removeProject(self, path):
		"""
		Removes a project.

		:param path: Project path.
		:type path: unicode
		:return: Method success.
		:rtype: bool
		"""

		projectNode = foundations.common.getFirstItem(self.__model.getProjectNodes(path))
		if not projectNode:
			self.__engine.notificationsManager.warnify(
			"{0} | '{1}' project is not opened!".format(self.__class__.__name__, path))
			return False

		LOGGER.info("{0} | Removing '{1}' project!".format(self.__class__.__name__, path))
		self.__model.deleteProjectNodes(projectNode)
		return True

	def newFile(self):
		"""
		Creates a new file into a new **Script_Editor_tabWidget** Widget tab.

		:return: Method success.
		:rtype: bool
		"""

		language = self.__languagesModel.getLanguage(self.__defaultScriptLanguage)
		editor = Editor(parent=self, language=language)

		file = editor.newFile()
		if not file:
			return False

		LOGGER.info("{0} | Creating '{1}' file!".format(self.__class__.__name__, file))

		if self.__model.setAuthoringNodes(editor):
			self.__storeRecentFile(file)
			self.fileLoaded.emit(file)
			return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.FileExistsError)
	def loadFile(self, file):
		"""
		Loads user chosen file in a new **Script_Editor_tabWidget** Widget tab Model editor.

		:param file: File to load.
		:type file: unicode
		:return: Method success.
		:rtype: bool
		"""

		if not foundations.common.pathExists(file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
			self.__class__.__name__, file))

		if self.getEditor(file):
			LOGGER.info("{0} | '{1}' is already loaded!".format(self.__class__.__name__, file))
			return True

		self.closeFirstFile()

		LOGGER.info("{0} | Loading '{1}' file!".format(self.__class__.__name__, file))
		language = self.__languagesModel.getFileLanguage(file) or self.__languagesModel.getLanguage(self.__defaultLanguage)
		editor = Editor(parent=self, language=language)

		if not editor.loadFile(file):
			return False

		if self.__model.setAuthoringNodes(editor):
			self.__storeRecentFile(file)
			self.fileLoaded.emit(file)
			return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.FileExistsError)
	def reloadFile(self, file, isModified=True):
		"""
		Reloads given file **Script_Editor_tabWidget** Widget tab Model editor content.

		:param file: File to reload.
		:type file: unicode
		:param isModified: File modified state.
		:type isModified: bool
		:return: Method success.
		:rtype: bool
		"""

		if not foundations.common.pathExists(file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
			self.__class__.__name__, file))

		editor = self.getEditor(file)
		if not editor:
			return False

		if self.__hasEditorLock(editor):
			self.__unlockEditor(editor)
			return True

		LOGGER.info("{0} | Reloading '{1}' file!".format(self.__class__.__name__, file))
		return editor.reloadFile(isModified)

	def saveFile(self, file=None):
		"""
		Saves either given file or current **Script_Editor_tabWidget** Widget tab Model editor file.

		:param file: File to save.
		:type file: unicode
		:return: Method success.
		:rtype: bool
		"""

		editor = file and self.getEditor(file) or self.getCurrentEditor()
		if not editor:
			return False

		LOGGER.info("{0} | Saving '{1}' file!".format(self.__class__.__name__, editor.file))
		self.__lockEditor(editor)
		if not editor.isUntitled and foundations.common.pathExists(editor.file):
			return editor.saveFile()
		else:
			return self.saveFileAs()

	@foundations.exceptions.handleExceptions(umbra.exceptions.notifyExceptionHandler,
											foundations.exceptions.UserError)
	def saveFileAs(self):
		"""
		Saves current **Script_Editor_tabWidget** Widget tab Model editor file as user chosen file.

		:return: Method success.
		:rtype: bool
		"""

		editor = self.getCurrentEditor()
		if not editor:
			return False

		file = umbra.ui.common.storeLastBrowsedPath(QFileDialog.getSaveFileName(self, "Save As:", editor.file))
		if not file:
			return False

		candidateEditor = self.getEditor(file)
		if candidateEditor:
			if not candidateEditor is editor:
				raise foundations.exceptions.UserError("{0} | '{1}' file is already opened!".format(
				self.__class__.__name__, file))
			else:
				return self.saveFile(file)

		LOGGER.info("{0} | Saving '{1}' file!".format(self.__class__.__name__, file))
		self.__lockEditor(editor)
		self.unregisterNodePath(editor)
		if editor.saveFileAs(file):
			self.__model.updateAuthoringNodes(editor)
			language = self.__languagesModel.getFileLanguage(file) or self.__languagesModel.getLanguage(self.__defaultLanguage)
			if editor.language.name != language.name:
				self.setLanguage(editor, language)
			return True

	@umbra.engine.encapsulateProcessing
	def saveAllFiles(self):
		"""
		Saves all **Script_Editor_tabWidget** Widget tab Model editor files.

		:return: Method success.
		:rtype: bool
		"""

		self.__engine.startProcessing("Saving All Files ...", len(self.listEditors()))
		success = True
		for file in self.listFiles():
			success *= self.saveFile(file)
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()
		return success

	@umbra.engine.encapsulateProcessing
	def revertFile(self, file=None):
		"""
		Reverts either given file or current **Script_Editor_tabWidget** Widget tab Model editor file.

		:param file: File to revert.
		:type file: unicode
		:return: Method success.
		:rtype: bool
		"""

		editor = file and self.getEditor(file) or self.getCurrentEditor()
		if not editor:
			return False

		file = editor.file
		LOGGER.info("{0} | Reverting '{1}' file!".format(self.__class__.__name__, file))
		if self.reloadFile(file, isModified=False):
			return True

	def closeFile(self, file=None, leaveFirstEditor=True):
		"""
		Closes either given file or current **Script_Editor_tabWidget** Widget tab Model editor file.

		:param file: File to save.
		:type file: unicode
		:param leaveFirstEditor: Leave first editor.
		:type leaveFirstEditor: bool
		:return: Method success.
		:rtype: bool
		"""

		editor = file and self.getEditor(file) or self.getCurrentEditor()
		if not editor:
			return False

		file = editor.file
		LOGGER.info("{0} | Closing '{1}' file!".format(self.__class__.__name__, file))
		if not editor.closeFile():
			return False

		if self.__model.deleteAuthoringNodes(editor):
			if not self.hasEditorTab() and leaveFirstEditor:
				self.newFile()
			self.fileClosed.emit(file)
			return True

	# @umbra.engine.encapsulateProcessing
	def closeAllFiles(self, leaveFirstEditor=True):
		"""
		Closes every opened files and removes their associated **Script_Editor_tabWidget** Widget tabs.

		:return: Method success.
		:rtype: bool
		"""

		# self.__engine.startProcessing("Closing All Files ...", len(self.listEditors()))
		success = True
		for file in self.listFiles():
			success *= True if self.closeFile(file, leaveFirstEditor) else False
			if not success:
				break

			# self.__engine.stepProcessing()
		# self.__engine.stopProcessing()
		return success

	def closeFirstFile(self):
		"""
		Attemtps to close the first **Script_Editor_tabWidget** Widget tab Model editor file.

		:return: Method success.
		:rtype: bool
		"""

		editor = self.getCurrentEditor()
		if len(self.__model.listEditors()) == 1 and editor.isUntitled and not editor.isModified():
			self.closeFile(leaveFirstEditor=False)
			return True

	def listEditors(self):
		"""
		Returns the Model editors.

		:return: Editors.
		:rtype: list
		"""

		return self.__model.listEditors()

	def listFiles(self):
		"""
		Returns the Model files.

		:return: FileNode nodes.
		:rtype: list
		"""

		return self.__model.listFiles()

	def listDirectories(self):
		"""
		Returns the Model directories.

		:return: DirectoryNode nodes.
		:rtype: list
		"""

		return self.__model.listDirectories()

	def listProjects(self, ignoreDefaultProject=True):
		"""
		Returns the Model projects.

		:return: ProjectNode nodes.
		:rtype: list
		"""

		return self.__model.listProjects()

	def getEditor(self, file):
		"""
		Returns the Model editor associated with given file.

		:param file: File to search editors for.
		:type file: unicode
		:return: Editor.
		:rtype: Editor
		"""

		for editor in self.__model.listEditors():
			if editor.file == file:
				return editor

	def setLanguage(self, editor, language):
		"""
		Sets given language to given Model editor.

		:param editor: Editor to set language to.
		:type editor: Editor
		:param language: Language to set.
		:type language: Language
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Setting '{0}' language to '{1}' editor.".format(language.name, editor))

		return editor.setLanguage(language)

	def gotoLine(self):
		"""
		Moves current **Script_Editor_tabWidget** Widget tab Model editor cursor to user defined line.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		editor = self.getCurrentEditor()
		if not editor:
			return False

		line, state = QInputDialog.getInt(self, "Goto Line Number", "Line number:", min=1)
		if not state:
			return False

		LOGGER.debug("> Chosen line number: '{0}'.".format(line))
		return editor.gotoLine(line)

	def evaluateSelection(self):
		"""
		Evaluates current **Script_Editor_tabWidget** Widget tab Model editor
		selected content in the interactive console.

		:return: Method success.
		:rtype: bool
		"""

		editor = self.getCurrentEditor()
		if not editor:
			return False

		LOGGER.debug("> Evaluating 'Script Editor' selected content.")
		if self.evaluateCode(foundations.strings.toString(editor.getSelectedText().replace(QChar(QChar.ParagraphSeparator),
																			QString("\n")))):
			self.uiRefresh.emit()
			return True

	def evaluateScript(self):
		"""
		Evaluates current **Script_Editor_tabWidget** Widget tab Model editor content
		into the interactive console.

		:return: Method success.
		:rtype: bool
		"""

		editor = self.getCurrentEditor()
		if not editor:
			return False

		LOGGER.debug("> Evaluating 'Script Editor' content.")
		if self.evaluateCode(foundations.strings.toString(editor.toPlainText().toUtf8())):
			self.uiRefresh.emit()
			return True

	def evaluateCode(self, code):
		"""
		Evaluates given code into the interactive console.

		:param code: Code to evaluate.
		:type code: unicode
		:return: Method success.
		:rtype: bool
		"""

		if not code:
			return False

		LOGGER.debug("> Evaluating given code.")

		code = code.endswith("\n") and code or "{0}\n".format(code)

		code = code.split("\n", 3)
		for i, line in enumerate(code[:-2]):
			if "coding" in line:
				code[i] = line.replace("=", "\=").replace(":", "\:")
				break
		code = "\n".join(code)

		sys.stdout.write(code)
		self.__console.runcode(code)
		return True

	def storeSession(self):
		"""
		Stores the current session.

		:return: Method success.
		:rtype: bool
		"""

		session = []
		for editor in self.listEditors():
			file = editor.file
			ignoreFile = True
			if editor.isUntitled and not editor.isEmpty():
				file = os.path.join(self.__defaultSessionDirectory, file)
				editor.writeFile(file)
			elif os.path.dirname(file) == self.__defaultSessionDirectory:
				editor.saveFile()
			session.append(file)

		for directory in self.listProjects():
			if not os.path.exists(directory):
				continue

			session.append(directory)

		LOGGER.debug("> Storing session :'{0}'.".format(session))
		self.__settings.setKey(self.__settingsSection, "session", session)
		return True

	def restoreSession(self):
		"""
		Restores the stored session.

		:return: Method success.
		:rtype: bool
		"""

		session = [foundations.strings.toString(path)
					for path in self.__settings.getKey(self.__settingsSection, "session").toStringList()
					if foundations.common.pathExists(path)]

		LOGGER.debug("> Restoring session :'{0}'.".format(session))
		success = True
		for path in session:
			if os.path.isfile(path):
				success *= self.loadFile(path)
			else:
				success *= self.addProject(path)
		return success


	def loopThroughEditors(self, backward=False):
		"""
		Loops through the editor tabs.

		:param backward: Looping backward.
		:type backward: bool
		:return: Method success.
		:rtype: bool
		"""

		step = not backward and 1 or -1
		idx = self.Script_Editor_tabWidget.currentIndex() + step
		if idx < 0:
			idx = self.Script_Editor_tabWidget.count() - 1
		elif idx > self.Script_Editor_tabWidget.count() - 1:
			idx = 0
		self.Script_Editor_tabWidget.setCurrentIndex(idx)
		return True

	def restoreDevelopmentLayout(self):
		"""
		Restores the development layout.

		:return: Definition success.
		:rtype: bool
		"""

		if self.__engine.layoutsManager.currentLayout != self.__developmentLayout and not self.isVisible():
			self.__engine.layoutsManager.restoreLayout(self.__developmentLayout)
		return True
