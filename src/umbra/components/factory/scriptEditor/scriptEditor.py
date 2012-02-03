#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**scriptEditor.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`ScriptEditor` Component Interface class and :class:`ScriptEditor_QTabWidget` class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import code
import logging
import os
import platform
import re
import sys
import shutil
from PyQt4.QtCore import QChar
from PyQt4.QtCore import QEvent
from PyQt4.QtCore import QFileSystemWatcher
from PyQt4.QtCore import QString
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QKeySequence
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QMenuBar
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextOption

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.exceptions
import foundations.walkers
import umbra.engine
import umbra.ui.common
import umbra.ui.highlighters
from manager.qwidgetComponent import QWidgetComponentFactory
from umbra.components.factory.scriptEditor.editor import Editor
from umbra.components.factory.scriptEditor.editor import getLanguageDescription
from umbra.components.factory.scriptEditor.editor import LOGGING_LANGUAGE
from umbra.components.factory.scriptEditor.editor import PYTHON_LANGUAGE
from umbra.components.factory.scriptEditor.editor import TEXT_LANGUAGE
from umbra.components.factory.scriptEditor.editorStatus import EditorStatus
from umbra.components.factory.scriptEditor.models import LanguagesModel
from umbra.components.factory.scriptEditor.searchAndReplace import SearchAndReplace
from umbra.components.factory.scriptEditor.searchInFiles import SearchInFiles
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals
from umbra.globals.uiConstants import UiConstants
from umbra.ui.widgets.basic_QPlainTextEdit import Basic_QPlainTextEdit

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "ScriptEditor_QTabWidget", "ScriptEditor"]

LOGGER = logging.getLogger(Constants.logger)

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Script_Editor.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ScriptEditor_QTabWidget(QTabWidget):
	"""
	| This class is a `QTabWidget <http://doc.qt.nokia.com/qtabwidget.html>`_ subclass used
		to display **ScriptEditor** editors.
	| It provides support for drag'n'drop by reimplementing relevant methods.
	"""

	# Custom signals definitions.
	contentDropped = pyqtSignal(QEvent)
	"""
	This signal is emited by the :class:`ScriptEditor_QTabWidget` class when it receives dropped content. ( pyqtSignal )

	:return: Event. ( QEvent )	
	"""

	@core.executionTrace
	def __init__(self, parent):
		"""
		This method initializes the class.

		:param parent: Parent object. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QTabWidget.__init__(self, parent)

		self.setAcceptDrops(True)

		# --- Setting class attributes. ---
		self.__container = parent

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

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def dragEnterEvent(self, event):
		"""
		This method reimplements the :meth:`QTabWidget.dragEnterEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		LOGGER.debug("> '{0}' widget drag enter event accepted!".format(self.__class__.__name__))
		event.accept()

	@core.executionTrace
	def dragMoveEvent(self, event):
		"""
		This method reimplements the :meth:`QTabWidget.dragMoveEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		LOGGER.debug("> '{0}' widget drag move event accepted!".format(self.__class__.__name__))
		event.accept()

	@core.executionTrace
	def dropEvent(self, event):
		"""
		This method reimplements the :meth:`QTabWidget.dropEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		LOGGER.debug("> '{0}' widget drop event accepted!".format(self.__class__.__name__))
		self.contentDropped.emit(event)

class ScriptEditor(QWidgetComponentFactory(uiFile=COMPONENT_UI_FILE)):
	"""
	This class is the :mod:`umbra.components.addons.scriptEditor.scriptEditor` Component Interface class.
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

		super(ScriptEditor, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__dockArea = 8

		self.__engine = None
		self.__settings = None
		self.__settingsSection = None

		self.__developmentLayout = UiConstants.developmentLayout

		self.__grammarsDirectory = "grammars"
		self.__extension = "grc"

		self.__languagesModel = None

		self.__defaultLanguage = "Text"
		self.__defaultScriptLanguage = "Python"

		self.__files = []
		self.__modifiedFiles = set()

		self.__defaultWindowTitle = "Script Editor"
		self.__defaultScriptEditorDirectory = "scriptEditor"
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
										"Linux" : ("Nimbus Mono L", 10)}

		self.__console = None
		self.__locals = None
		self.__memoryHandlerStackDepth = None

		self.__menuBar = None
		self.__fileMenu = None
		self.__editMenu = None
		self.__sourceMenu = None
		self.__navigateMenu = None
		self.__searchMenu = None
		self.__commandMenu = None
		self.__viewMenu = None

		self.__fileSystemWatcher = None
		self.__timer = None
		self.__timerCycleMultiplier = 10

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def dockArea(self):
		"""
		This method is the property for **self.__dockArea** attribute.

		:return: self.__dockArea. ( Integer )
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This method is the setter method for **self.__dockArea** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dockArea"))

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
	def developmentLayout(self):
		"""
		This method is the property for **self.__developmentLayout** attribute.

		:return: self.__developmentLayout. ( String )
		"""

		return self.__developmentLayout

	@developmentLayout.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def developmentLayout(self, value):
		"""
		This method is the setter method for **self.__developmentLayout** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "developmentLayout"))

	@developmentLayout.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def developmentLayout(self):
		"""
		This method is the deleter method for **self.__developmentLayout** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "developmentLayout"))

	@property
	def grammarsDirectory(self):
		"""
		This method is the property for **self.__grammarsDirectory** attribute.

		:return: self.__grammarsDirectory. ( String )
		"""

		return self.__grammarsDirectory

	@grammarsDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def grammarsDirectory(self, value):
		"""
		This method is the setter method for **self.__grammarsDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "grammarsDirectory"))

	@grammarsDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def grammarsDirectory(self):
		"""
		This method is the deleter method for **self.__grammarsDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "grammarsDirectory"))

	@property
	def extension(self):
		"""
		This method is the property for **self.__extension** attribute.

		:return: self.__extension. ( String )
		"""

		return self.__extension

	@extension.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def extension(self, value):
		"""
		This method is the setter method for **self.__extension** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "extension"))

	@extension.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def extension(self):
		"""
		This method is the deleter method for **self.__extension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "extension"))

	@property
	def languagesModel(self):
		"""
		This method is the property for **self.__languagesModel** attribute.

		:return: self.__languagesModel. ( LanguagesModel )
		"""

		return self.__languagesModel

	@languagesModel.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def languagesModel(self, value):
		"""
		This method is the setter method for **self.__languagesModel** attribute.

		:param value: Attribute value. ( LanguagesModel )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "languagesModel"))

	@languagesModel.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def languagesModel(self):
		"""
		This method is the deleter method for **self.__languagesModel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "languagesModel"))

	@property
	def defaultLanguage(self):
		"""
		This method is the property for **self.__defaultLanguage** attribute.

		:return: self.__defaultLanguage. ( String )
		"""

		return self.__defaultLanguage

	@defaultLanguage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultLanguage(self, value):
		"""
		This method is the setter method for **self.__defaultLanguage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultLanguage"))

	@defaultLanguage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultLanguage(self):
		"""
		This method is the deleter method for **self.__defaultLanguage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultLanguage"))

	@property
	def defaultScriptLanguage(self):
		"""
		This method is the property for **self.__defaultScriptLanguage** attribute.

		:return: self.__defaultScriptLanguage. ( String )
		"""

		return self.__defaultScriptLanguage

	@defaultScriptLanguage.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultScriptLanguage(self, value):
		"""
		This method is the setter method for **self.__defaultScriptLanguage** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultScriptLanguage"))

	@defaultScriptLanguage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultScriptLanguage(self):
		"""
		This method is the deleter method for **self.__defaultScriptLanguage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultScriptLanguage"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "files"))

	@files.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def files(self):
		"""
		This method is the deleter method for **self.__files** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "files"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "modifiedFiles"))

	@modifiedFiles.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def modifiedFiles(self):
		"""
		This method is the deleter method for **self.__modifiedFiles** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "modifiedFiles"))

	@property
	def defaultWindowTitle(self):
		"""
		This method is the property for **self.__defaultWindowTitle** attribute.

		:return: self.__defaultWindowTitle. ( String )
		"""

		return self.__defaultWindowTitle

	@defaultWindowTitle.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultWindowTitle(self, value):
		"""
		This method is the setter method for **self.__defaultWindowTitle** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultWindowTitle"))

	@defaultWindowTitle.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultWindowTitle(self):
		"""
		This method is the deleter method for **self.__defaultWindowTitle** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultWindowTitle"))

	@property
	def defaultScriptEditorDirectory(self):
		"""
		This method is the property for **self.__defaultScriptEditorDirectory** attribute.

		:return: self.__defaultScriptEditorDirectory. ( String )
		"""

		return self.__defaultScriptEditorDirectory

	@defaultScriptEditorDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultScriptEditorDirectory(self, value):
		"""
		This method is the setter method for **self.__defaultScriptEditorDirectory** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultScriptEditorDirectory"))

	@defaultScriptEditorDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultScriptEditorDirectory(self):
		"""
		This method is the deleter method for **self.__defaultScriptEditorDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultScriptEditorDirectory"))

	@property
	def defaultScriptEditorFile(self):
		"""
		This method is the property for **self.__defaultScriptEditorFile** attribute.

		:return: self.__defaultScriptEditorFile. ( String )
		"""

		return self.__defaultScriptEditorFile

	@defaultScriptEditorFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultScriptEditorFile(self, value):
		"""
		This method is the setter method for **self.__defaultScriptEditorFile** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultScriptEditorFile"))

	@defaultScriptEditorFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultScriptEditorFile(self):
		"""
		This method is the deleter method for **self.__defaultScriptEditorFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultScriptEditorFile"))

	@property
	def factoryDefaultScriptEditorFile(self):
		"""
		This method is the property for **self.__factoryDefaultScriptEditorFile** attribute.

		:return: self.__factoryDefaultScriptEditorFile. ( String )
		"""

		return self.__factoryDefaultScriptEditorFile

	@factoryDefaultScriptEditorFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryDefaultScriptEditorFile(self, value):
		"""
		This method is the setter method for **self.__factoryDefaultScriptEditorFile** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factoryDefaultScriptEditorFile"))

	@factoryDefaultScriptEditorFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryDefaultScriptEditorFile(self):
		"""
		This method is the deleter method for **self.__factoryDefaultScriptEditorFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factoryDefaultScriptEditorFile"))

	@property
	def scriptEditorFile(self):
		"""
		This method is the property for **self.__scriptEditorFile** attribute.

		:return: self.__scriptEditorFile. ( String )
		"""

		return self.__scriptEditorFile

	@scriptEditorFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def scriptEditorFile(self, value):
		"""
		This method is the setter method for **self.__scriptEditorFile** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"scriptEditorFile", value)
		self.__scriptEditorFile = value

	@scriptEditorFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def scriptEditorFile(self):
		"""
		This method is the deleter method for **self.__scriptEditorFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "scriptEditorFile"))

	@property
	def maximumRecentFiles(self):
		"""
		This method is the property for **self.__maximumRecentFiles** attribute.

		:return: self.__maximumRecentFiles. ( Integer )
		"""

		return self.__maximumRecentFiles

	@maximumRecentFiles.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumRecentFiles(self, value):
		"""
		This method is the setter method for **self.__maximumRecentFiles** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "maximumRecentFiles"))

	@maximumRecentFiles.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumRecentFiles(self):
		"""
		This method is the deleter method for **self.__maximumRecentFiles** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "maximumRecentFiles"))

	@property
	def recentFilesActions(self):
		"""
		This method is the property for **self.__recentFilesActions** attribute.

		:return: self.__recentFilesActions. ( List )
		"""

		return self.__recentFilesActions

	@recentFilesActions.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def recentFilesActions(self, value):
		"""
		This method is the setter method for **self.__recentFilesActions** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "recentFilesActions"))

	@recentFilesActions.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def recentFilesActions(self):
		"""
		This method is the deleter method for **self.__recentFilesActions** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "recentFilesActions"))

	@property
	def searchAndReplace(self):
		"""
		This method is the property for **self.__searchAndReplace** attribute.

		:return: self.__searchAndReplace. ( SearchAndReplace )
		"""

		return self.__searchAndReplace

	@searchAndReplace.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchAndReplace(self, value):
		"""
		This method is the setter method for **self.__searchAndReplace** attribute.

		:param value: Attribute value. ( SearchAndReplace )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "searchAndReplace"))

	@searchAndReplace.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchAndReplace(self):
		"""
		This method is the deleter method for **self.__searchAndReplace** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchAndReplace"))

	@property
	def searchInFiles(self):
		"""
		This method is the property for **self.__searchInFiles** attribute.

		:return: self.__searchInFiles. ( SearchInFiles )
		"""

		return self.__searchInFiles

	@searchInFiles.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchInFiles(self, value):
		"""
		This method is the setter method for **self.__searchInFiles** attribute.

		:param value: Attribute value. ( SearchInFiles )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "searchInFiles"))

	@searchInFiles.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchInFiles(self):
		"""
		This method is the deleter method for **self.__searchInFiles** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchInFiles"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "indentWidth"))

	@indentWidth.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def indentWidth(self):
		"""
		This method is the deleter method for **self.__indentWidth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "indentWidth"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultFontsSettings"))

	@defaultFontsSettings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultFontsSettings(self):
		"""
		This method is the deleter method for **self.__defaultFontsSettings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultFontsSettings"))

	@property
	def console(self):
		"""
		This method is the property for **self.__console** attribute.

		:return: self.__console. ( Dictionary )
		"""

		return self.__console

	@console.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def console(self, value):
		"""
		This method is the setter method for **self.__console** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "console"))

	@console.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def console(self):
		"""
		This method is the deleter method for **self.__console** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "console"))

	@property
	def locals(self):
		"""
		This method is the property for **self.__locals** attribute.

		:return: self.__locals. ( Dictionary )
		"""

		return self.__locals

	@locals.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def locals(self, value):
		"""
		This method is the setter method for **self.__locals** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "locals"))

	@locals.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def locals(self):
		"""
		This method is the deleter method for **self.__locals** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "locals"))

	@property
	def memoryHandlerStackDepth(self):
		"""
		This method is the property for **self.__memoryHandlerStackDepth** attribute.

		:return: self.__memoryHandlerStackDepth. ( Integer )
		"""

		return self.__memoryHandlerStackDepth

	@memoryHandlerStackDepth.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def memoryHandlerStackDepth(self, value):
		"""
		This method is the setter method for **self.__memoryHandlerStackDepth** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "memoryHandlerStackDepth"))

	@memoryHandlerStackDepth.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def memoryHandlerStackDepth(self):
		"""
		This method is the deleter method for **self.__memoryHandlerStackDepth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "memoryHandlerStackDepth"))

	@property
	def menuBar(self):
		"""
		This method is the property for **self.__menuBar** attribute.

		:return: self.__menuBar. ( QToolbar )
		"""

		return self.__menuBar

	@menuBar.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def menuBar(self, value):
		"""
		This method is the setter method for **self.__menuBar** attribute.

		:param value: Attribute value. ( QToolbar )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "menuBar"))

	@menuBar.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def menuBar(self):
		"""
		This method is the deleter method for **self.__menuBar** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "menuBar"))

	@property
	def fileMenu(self):
		"""
		This method is the property for **self.__fileMenu** attribute.

		:return: self.__fileMenu. ( QMenu )
		"""

		return self.__fileMenu

	@fileMenu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def fileMenu(self, value):
		"""
		This method is the setter method for **self.__fileMenu** attribute.

		:param value: Attribute value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "fileMenu"))

	@fileMenu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def fileMenu(self):
		"""
		This method is the deleter method for **self.__fileMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "fileMenu"))

	@property
	def editMenu(self):
		"""
		This method is the property for **self.__editMenu** attribute.

		:return: self.__editMenu. ( QMenu )
		"""

		return self.__editMenu

	@editMenu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editMenu(self, value):
		"""
		This method is the setter method for **self.__editMenu** attribute.

		:param value: Attribute value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "editMenu"))

	@editMenu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editMenu(self):
		"""
		This method is the deleter method for **self.__editMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "editMenu"))

	@property
	def sourceMenu(self):
		"""
		This method is the property for **self.__sourceMenu** attribute.

		:return: self.__sourceMenu. ( QMenu )
		"""

		return self.__sourceMenu

	@sourceMenu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def sourceMenu(self, value):
		"""
		This method is the setter method for **self.__sourceMenu** attribute.

		:param value: Attribute value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "sourceMenu"))

	@sourceMenu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def sourceMenu(self):
		"""
		This method is the deleter method for **self.__sourceMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "sourceMenu"))

	@property
	def navigateMenu(self):
		"""
		This method is the property for **self.__navigateMenu** attribute.

		:return: self.__navigateMenu. ( QMenu )
		"""

		return self.__navigateMenu

	@navigateMenu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def navigateMenu(self, value):
		"""
		This method is the setter method for **self.__navigateMenu** attribute.

		:param value: Attribute value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "navigateMenu"))

	@navigateMenu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def navigateMenu(self):
		"""
		This method is the deleter method for **self.__navigateMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "navigateMenu"))

	@property
	def searchMenu(self):
		"""
		This method is the property for **self.__searchMenu** attribute.

		:return: self.__searchMenu. ( QMenu )
		"""

		return self.__searchMenu

	@searchMenu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchMenu(self, value):
		"""
		This method is the setter method for **self.__searchMenu** attribute.

		:param value: Attribute value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "searchMenu"))

	@searchMenu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchMenu(self):
		"""
		This method is the deleter method for **self.__searchMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchMenu"))

	@property
	def commandMenu(self):
		"""
		This method is the property for **self.__commandMenu** attribute.

		:return: self.__commandMenu. ( QMenu )
		"""

		return self.__commandMenu

	@commandMenu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def commandMenu(self, value):
		"""
		This method is the setter method for **self.__commandMenu** attribute.

		:param value: Attribute value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "commandMenu"))

	@commandMenu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def commandMenu(self):
		"""
		This method is the deleter method for **self.__commandMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "commandMenu"))

	@property
	def viewMenu(self):
		"""
		This method is the property for **self.__viewMenu** attribute.

		:return: self.__viewMenu. ( QMenu )
		"""

		return self.__viewMenu

	@viewMenu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewMenu(self, value):
		"""
		This method is the setter method for **self.__viewMenu** attribute.

		:param value: Attribute value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "viewMenu"))

	@viewMenu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def viewMenu(self):
		"""
		This method is the deleter method for **self.__viewMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "viewMenu"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "fileSystemWatcher"))

	@fileSystemWatcher.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def fileSystemWatcher(self):
		"""
		This method is the deleter method for **self.__fileSystemWatcher** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "fileSystemWatcher"))

	@property
	def timer(self):
		"""
		This method is the property for **self.__timer** attribute.

		:return: self.__timer. ( QTimer )
		"""

		return self.__timer

	@timer.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self, value):
		"""
		This method is the setter method for **self.__timer** attribute.

		:param value: Attribute value. ( QTimer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "timer"))

	@timer.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timer(self):
		"""
		This method is the deleter method for **self.__timer** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "timer"))

	@property
	def timerCycleMultiplier(self):
		"""
		This method is the property for **self.__timerCycleMultiplier** attribute.

		:return: self.__timerCycleMultiplier. ( Float )
		"""

		return self.__timerCycleMultiplier

	@timerCycleMultiplier.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timerCycleMultiplier(self, value):
		"""
		This method is the setter method for **self.__timerCycleMultiplier** attribute.

		:param value: Attribute value. ( Float )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "timerCycleMultiplier"))

	@timerCycleMultiplier.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def timerCycleMultiplier(self):
		"""
		This method is the deleter method for **self.__timerCycleMultiplier** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "timerCycleMultiplier"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def activate(self, engine):
		"""
		This method activates the Component.

		:param engine: Container to attach the Component to. ( QObject )
		:return: Method success. ( Boolean )
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
		self.__defaultScriptEditorFile = os.path.join(self.__defaultScriptEditorDirectory,
													self.__defaultScriptEditorFile)

		self.__setLocals()
		self.__console = code.InteractiveConsole(self.__locals)

		self.activated = True
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. ( Boolean )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def initializeUi(self):
		"""
		This method initializes the Component ui.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

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
		self.__initializeMenuBar()

		self.Script_Editor_Output_plainTextEdit.setParent(None)
		self.Script_Editor_Output_plainTextEdit = Basic_QPlainTextEdit(self)
		self.Script_Editor_Output_plainTextEdit_frame_gridLayout.addWidget(
		self.Script_Editor_Output_plainTextEdit, 0, 0)
		self.Script_Editor_Output_plainTextEdit.setObjectName("Script_Editor_Output_plainTextEdit")

		self.__Script_Editor_Output_plainTextEdit_setUi()

		self.__searchAndReplace = SearchAndReplace(self, Qt.Window)
		self.__searchInFiles = SearchInFiles(self, Qt.Window)

		self.__fileSystemWatcher = QFileSystemWatcher(self)
		self.__timer = QTimer(self)
		self.__timer.start(Constants.defaultTimerCycle * self.__timerCycleMultiplier)

		self.__initializeLanguagesModel()

		self.Editor_Status_editorStatus = EditorStatus(self)
		self.__engine.statusBar.insertPermanentWidget(0, self.Editor_Status_editorStatus)

		# Signals / Slots.
		self.__engine.timer.timeout.connect(self.__Script_Editor_Output_plainTextEdit_refreshUi)
		self.__engine.layoutsManager.layoutRestored.connect(self.__engine__layoutRestored)
		self.__engine.contentDropped.connect(self.__engine__contentDropped)
		self.Script_Editor_tabWidget.tabCloseRequested.connect(self.__Script_Editor_tabWidget__tabCloseRequested)
		self.Script_Editor_tabWidget.currentChanged.connect(self.__Script_Editor_tabWidget__currentChanged)
		self.Script_Editor_tabWidget.contentDropped.connect(self.__Script_Editor_tabWidget__contentDropped)
		self.visibilityChanged.connect(self.__scriptEditor__visibilityChanged)
		self.uiRefresh.connect(self.__Script_Editor_Output_plainTextEdit_refreshUi)
		self.recentFilesChanged.connect(self.__setRecentFilesActions)
		self.__fileSystemWatcher.fileChanged.connect(self.__fileSystemWatcher__fileChanged)
		self.__timer.timeout.connect(self.__reloadModifiedFiles)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.

		:return: Method success. ( Boolean )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addWidget(self):
		"""
		This method adds the Component Widget to the engine.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeWidget(self):
		"""
		This method removes the Component Widget from the engine.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.removeDockWidget(self)
		self.setParent(None)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def onStartup(self):
		"""
		This method is triggered on Framework startup.
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
		if startupScript:
			if foundations.common.pathExists(startupScript):
				self.loadFile(startupScript) and self.evaluateScript()

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def onClose(self):
		"""
		This method is triggered on Framework close.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'onClose' method.".format(self.__class__.__name__))

		if self.closeAllFiles(leaveLastEditor=False):
			self.__timer.stop()
			self.__timer = None
			return True

	@core.executionTrace
	def __initializeMenuBar(self):
		"""
		This method initializes Component menuBar.
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
		self.__menuBar.addMenu(self.__viewMenu)

	# @core.executionTrace
	def __Script_Editor_Output_plainTextEdit_setUi(self):
		"""
		This method sets the **Script_Editor_Output_plainTextEdit** Widget.
		"""

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
		self.__Script_Editor_Output_plainTextEdit_setDefaultViewState()

	# @core.executionTrace
	def __Script_Editor_Output_plainTextEdit_setDefaultViewState(self):
		"""
		This method sets the **Script_Editor_Output_plainTextEdit** Widget default View state.
		"""

		self.Script_Editor_Output_plainTextEdit.moveCursor(QTextCursor.End)
		self.Script_Editor_Output_plainTextEdit.ensureCursorVisible()

	# @core.executionTrace
	def __Script_Editor_Output_plainTextEdit_refreshUi(self):
		"""
		This method updates the **Script_Editor_Output_plainTextEdit** Widget.
		"""

		memoryHandlerStackDepth = len(self.__engine.loggingSessionHandlerStream.stream)
		if memoryHandlerStackDepth != self.__memoryHandlerStackDepth:
			for line in self.__engine.loggingSessionHandlerStream.stream[
			self.__memoryHandlerStackDepth:memoryHandlerStackDepth]:
				self.Script_Editor_Output_plainTextEdit.moveCursor(QTextCursor.End)
				self.Script_Editor_Output_plainTextEdit.insertPlainText(line)
			self.__Script_Editor_Output_plainTextEdit_setDefaultViewState()
			self.__memoryHandlerStackDepth = memoryHandlerStackDepth

	@core.executionTrace
	def __Script_Editor_tabWidget_setUi(self):
		"""
		This method sets the **Script_Editor_tabWidget** Widget.
		"""

		self.Script_Editor_tabWidget.setTabsClosable(True)
		self.Script_Editor_tabWidget.setMovable(True)

	@core.executionTrace
	def __Script_Editor_tabWidget__tabCloseRequested(self, index):
		"""
		This method is triggered by the **Script_Editor_tabWidget** Widget when a tab is requested to be closed.

		:param index: Tab index. ( Integer )
		"""

		LOGGER.debug("> Closing tab with index '{0}'.".format(index))

		self.Script_Editor_tabWidget.setCurrentIndex(index)
		return self.closeFile()

	@core.executionTrace
	def __Script_Editor_tabWidget__currentChanged(self, index):
		"""
		This method is triggered by the **Script_Editor_tabWidget** Widget when the current tab is changed.

		:param index: Tab index. ( Integer )
		"""

		LOGGER.debug("> Current tab changed to '{0}' index.".format(index))

		self.Editor_Status_editorStatus._EditorStatus__Languages_comboBox_setDefaultViewState()
		self.__setWindowTitle()

	@core.executionTrace
	def __Script_Editor_tabWidget__contentDropped(self, event):
		"""
		This method is triggered when content is dropped in the **Script_Editor_tabWidget** Widget.

		:param event: Event. ( QEvent )
		"""

		self.__handleContentDroppedEvent(event)

	@core.executionTrace
	def __engine__layoutRestored(self, currentLayout):
		"""
		This method is triggered when the engine layout is changed.

		:param currentLayout: Current layout. ( String )
		"""

		self.Editor_Status_editorStatus.setVisible(not self.isHidden())

	@core.executionTrace
	def __engine__contentDropped(self, event):
		"""
		This method is triggered when content is dropped into the engine.
		
		:param event: Event. ( QEvent )
		"""

		self.__handleContentDroppedEvent(event)

	@core.executionTrace
	def __scriptEditor__visibilityChanged(self, visibility):
		"""
		This method is triggered when the **scriptEditor** Component visibility changed.

		:param visibility: Widget visibility. ( Boolean )
		"""

		self.Editor_Status_editorStatus.setVisible(visibility)

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

		return self.loadFileUi()

	@core.executionTrace
	def __sourceFileAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|Source ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if self.loadFileUi():
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
	def __saveAllFilesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|Save All'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.saveAllFiles()

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
	def __loadRecentFile__triggered(self, checked):
		"""
		This method is triggered by any recent file related action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		file = self.sender().data
		if foundations.common.pathExists(file):
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

		currentWidget = self.getFocusWidget()
		if not currentWidget:
			return

		if currentWidget.objectName() == "Script_Editor_Output_plainTextEdit":
			currentWidget.copy()
		else:
			currentWidget.cut()
		return True

	@core.executionTrace
	def __copyAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Copy'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		currentWidget = self.getFocusWidget()
		if not currentWidget:
			return

		currentWidget.copy()
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

		currentWidget = self.getFocusWidget()
		if not currentWidget:
			return

		currentWidget.selectAll()
		return True

	@core.executionTrace
	def __deleteLinesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Source|Delete Line(s)'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().deleteLines()

	@core.executionTrace
	def __duplicateLinesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Source|Duplicate Line(s)'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().duplicateLines()

	@core.executionTrace
	def __moveUpAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Source|Move Up'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().moveLinesUp()

	@core.executionTrace
	def __moveDownAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Source|Move Down'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().moveLinesDown()

	@core.executionTrace
	def __indentSelectionAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Source|Indent Selection'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().indent()

	@core.executionTrace
	def __unindentSelectionAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Source|Unindent Selection'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().unindent()

	@core.executionTrace
	def __convertIndentationToTabsAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|factory.scriptEditor|&Source|Convert Identation To Tabs'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().convertIndentationToTabs()

	@core.executionTrace
	def __convertIndentationToSpacesAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|factory.scriptEditor|&Source|Convert Identation To Spaces'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().convertIndentationToSpaces()

	@core.executionTrace
	def __removeTrailingWhiteSpacesAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|factory.scriptEditor|&Source|Remove Trailing WhiteSpaces'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().removeTrailingWhiteSpaces()

	@core.executionTrace
	def __toggleCommentsAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Source|Toggle Comments'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not self.hasEditorTab():
			return

		return self.getCurrentEditor().toggleComments()

	@core.executionTrace
	def __gotoLineAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Navigate|Goto Line ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.gotoLine()

	@core.executionTrace
	def __searchAndReplaceAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|factory.scriptEditor|&Search|Search And Replace ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.searchAndReplaceUi()

	@core.executionTrace
	def __searchInFilesAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|factory.scriptEditor|&Search|Search In Files ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.searchInFilesUi()

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
	def __evaluateSelectionAction__triggered(self, checked):
		"""
		This method is triggered by
		**'Actions|Umbra|Components|factory.scriptEditor|&Command|&Evaluate Selection'** action.

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
	def __increaseFontSizeAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&View|Increase Font Size'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		currentWidget = self.getFocusWidget()
		if not currentWidget:
			return

		return currentWidget.zoomIn()

	@core.executionTrace
	def __decreaseFontSizeAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&View|Decrease Font Size'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		currentWidget = self.getFocusWidget()
		if not currentWidget:
			return

		return currentWidget.zoomOut()

	@core.executionTrace
	def __toggleWordWrapAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&View|Toggle Word Wrap'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		currentWidget = self.getFocusWidget()
		if not currentWidget:
			return

		return currentWidget.toggleWordWrap()

	@core.executionTrace
	def __toggleWhiteSpacesAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&View|Toggle White Spaces'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		currentWidget = self.getFocusWidget()
		if not currentWidget:
			return

		return currentWidget.toggleWhiteSpaces()

	@core.executionTrace
	def __editor__patternsReplaced(self, patterns):
		"""
		This method is triggered when an editor patterns have been replaced.
		"""

		replacedPatternsCount = len(patterns)
		replacedPatternsCount and self.__engine.notificationsManager.notify(
		"{0} | '{1}' pattern(s) replaced!".format(self.__class__.__name__, replacedPatternsCount))

	@core.executionTrace
	def __editor__titleChanged(self):
		"""
		This method is triggered when an editor content is changed.
		"""

		self.__setEditorTabName(self.getEditorTab(self.sender()))
		self.__setWindowTitle()

	@core.executionTrace
	def __editor__fileChanged(self):
		"""
		This method is triggered when an editor file is changed.
		"""

		self.__setEditorTabName(self.getEditorTab(self.sender()))

	@core.executionTrace
	def __editor__languageChanged(self):
		"""
		This method is triggered when an editor language is changed.
		"""

		self.Editor_Status_editorStatus._EditorStatus__Languages_comboBox_setDefaultViewState()

	@core.executionTrace
	def __fileSystemWatcher__fileChanged(self, file):
		"""
		This method is triggered by the :obj:`ScriptEditor.fileSystemWatcher` class property when a file is modified.
		
		:param file: File modified. ( String )
		"""

		LOGGER.debug("> Adding '{0}' file **modifiedFiles** stack.".format(file))

		self.__modifiedFiles.add(file)

	@core.executionTrace
	def __startfileSystemWatcher(self):
		"""
		This method starts the :obj:`ScriptEditor.fileSystemWatcher` class property bound instance.
		"""

		self.__files and self.__fileSystemWatcher.addPaths(self.__files)

	@core.executionTrace
	def __stopfileSystemWatcher(self):
		"""
		This method stops the :obj:`ScriptEditor.fileSystemWatcher` class property bound instance.
		"""

		self.__files and self.__fileSystemWatcher.removePaths(self.__files)

	@core.executionTrace
	def __reloadModifiedFiles(self):
		"""
		This method reloads modfied files.
		"""

		while self.__modifiedFiles:
			self.reloadFile(self.__modifiedFiles.pop())

	@core.executionTrace
	def __initializeLanguagesModel(self):
		"""
		This method initializes given file in the :obj:`ScriptEditor.languagesModel` class property.
		"""

		languages = [PYTHON_LANGUAGE, LOGGING_LANGUAGE, TEXT_LANGUAGE]
		existingGrammarFiles = [os.path.normpath(language.file) for language in languages]

		for directory in RuntimeGlobals.resourcesDirectories:
			osWalker = foundations.walkers.OsWalker(directory)
			osWalker.walk(("\.{0}$".format(self.__extension),), ("\._",))
			for file in osWalker.files.itervalues():
				if os.path.normpath(file) in existingGrammarFiles:
					continue

				languageDescription = getLanguageDescription(file)
				if not languageDescription:
					continue

				LOGGER.debug("> Adding '{0}' language to model.".format(languageDescription))
				languages.append(languageDescription)

		self.__languagesModel = LanguagesModel(self, sorted(languages, key=lambda x: (x.name)))

	@core.executionTrace
	def __registerFile(self, file):
		"""
		This method registers given file in the :obj:`ScriptEditor.files` class property.
		
		:param file: File to register. ( String )
		"""

		LOGGER.debug("> Registering '{0}' file.".format(file))

		self.__files.append(file)
		self.__fileSystemWatcher.addPath(file)

	@core.executionTrace
	def __unregisterFile(self, file):
		"""
		This method unregisters given file in the :obj:`ScriptEditor.files` class property.
		
		:param file: File to unregister. ( String )
		"""

		if file in self.__files:
			LOGGER.debug("> Unregistering '{0}' file.".format(file))
			self.__files.remove(file)
			self.__fileSystemWatcher.removePath(file)

	@core.executionTrace
	def __setRecentFilesActions(self):
		"""
		This method sets the recent files actions.
		"""

		recentFiles = [str(recentFile)
					for recentFile in self.__settings.getKey(self.__settingsSection, "recentFiles").toString().split(",")
					if foundations.common.pathExists(recentFile)]
		if not recentFiles:
			return

		numberRecentFiles = min(len(recentFiles), self.__maximumRecentFiles)

		for i in range(self.__maximumRecentFiles):
			if i >= numberRecentFiles:
				self.__recentFilesActions[i].setVisible(False)
				continue

			LOGGER.debug("> Adding '{0}' file to recent files actions.".format(recentFiles[i]))

			self.__recentFilesActions[i].setText("{0} {1}".format(i + 1, os.path.basename(str(recentFiles[i]))))
			self.__recentFilesActions[i].data = str(recentFiles[i])
			self.__recentFilesActions[i].setVisible(True)

	@core.executionTrace
	def __storeRecentFile(self, file):
		"""
		This method stores given recent file into the settings.
		
		:param file: File to store. ( String )
		"""

		LOGGER.debug("> Storing '{0}' file in recent files.".format(file))

		recentFiles = [str(recentFile)
					for recentFile in self.__settings.getKey(self.__settingsSection, "recentFiles").toString().split(",")
					if foundations.common.pathExists(recentFile)]
		if not recentFiles:
			recentFiles = []

		if file in recentFiles:
			recentFiles.pop(recentFiles.index(file))
		recentFiles.insert(0, file)
		del recentFiles[self.__maximumRecentFiles:]
		recentFiles = self.__settings.setKey(self.__settingsSection, "recentFiles", ",".join(recentFiles))
		self.recentFilesChanged.emit()

	@core.executionTrace
	@umbra.engine.encapsulateProcessing
	def __handleContentDroppedEvent(self, event):
		"""
		This method handles dopped content event.
		
		:param event: Content dropped event. ( QEvent )
		"""

		if not event.mimeData().hasUrls():
			return

		urls = event.mimeData().urls()

		self.__engine.startProcessing("Loading Files ...", len(urls))
		for url in event.mimeData().urls():
			LOGGER.debug("> Handling dropped '{0}' file.".format(url.path()))
			path = (platform.system() == "Windows" or platform.system() == "Microsoft") and \
			re.search(r"^\/[A-Z]:", str(url.path())) and str(url.path())[1:] or str(url.path())
			if os.path.isdir(path):
				continue

			if self.loadFile(path):
				self.__engine.layoutsManager.currentLayout != self.__developmentLayout and \
				self.__engine.layoutsManager.restoreLayout(self.__developmentLayout)
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

	@core.executionTrace
	def __setWindowTitle(self):
		"""
		This method sets the Component window title.
		"""

		if self.hasEditorTab():
			windowTitle = "{0} - {1}".format(self.__defaultWindowTitle, self.getCurrentEditor().file)
		else:
			windowTitle = "{0}".format(self.__defaultWindowTitle)

		LOGGER.debug("> Setting 'Script Editor' window title to '{0}'.".format(windowTitle))
		self.setWindowTitle(windowTitle)

	@core.executionTrace
	def __setEditorTabName(self, index):
		"""
		This method sets the name of the **Script_Editor_tabWidget** Widget tab with given index.

		:param index: Index of the tab containing the editor. ( Integer )
		"""

		editor = self.Script_Editor_tabWidget.widget(index)
		if not editor:
			return

		windowTitle = editor.windowTitle()
		LOGGER.debug("> Setting '{0}' window title to tab with '{1}' index.".format(windowTitle, index))
		self.Script_Editor_tabWidget.setTabText(index, windowTitle)

	@core.executionTrace
	def __setLocals(self):
		"""
		This method sets the locals for the interactive console.

		:return: Method success. ( Boolean )
		"""

		self.__locals = {}

		for globals in (Constants, RuntimeGlobals, UiConstants):
			self.__locals[globals.__name__] = globals

		self.__locals[Constants.applicationName] = self.__engine
		self.__locals["application"] = self.__engine
		self.__locals["patchesManager"] = self.__engine.patchesManager
		self.__locals["componentsManager"] = self.__engine.componentsManager
		self.__locals["actionsManager"] = self.__engine.actionsManager
		self.__locals["notificationsManager"] = self.__engine.notificationsManager
		self.__locals["layoutsManager"] = self.__engine.layoutsManager
		self.__locals["LOGGER"] = LOGGER

		LOGGER.debug("> Defined locals: '{0}'.".format(self.__locals))

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler, False, Exception)
	def loadFileUi(self):
		"""
		This method loads user chosen file into in the current **Script_Editor_tabWidget** Widget tab editor.

		:return: Method success. ( Boolean )
		
		:note: This method may require user interaction.
		"""

		file = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getOpenFileName(self,
																				"Load File:",
																				RuntimeGlobals.lastBrowsedPath)))
		if not file:
			return

		return self.loadFile(file)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler, False, Exception)
	def searchAndReplaceUi(self):
		"""
		This method performs a search and replace in the current **Script_Editor_tabWidget** Widget tab editor.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		self.__searchAndReplace.show()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler, False, Exception)
	def searchInFilesUi(self):
		"""
		This method performs a search in files in the current user chosen files.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		self.__searchInFiles.show()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getFocusWidget(self):
		"""
		This method returns the Widget with focus.

		:return: Widget with focus. ( QWidget )
		"""

		currentWidget = QApplication.focusWidget()
		if currentWidget.objectName() == "Script_Editor_Output_plainTextEdit" or \
			isinstance(currentWidget, Editor):
			return currentWidget

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addEditorTab(self, editor):
		"""
		This method adds a new tab to the **Script_Editor_tabWidget** Widget and sets given editor as child widget.

		:param editor: Editor. ( Editor )
		:return: New tab index. ( Integer )
		"""

		index = self.Script_Editor_tabWidget.addTab(editor, editor.getFileShortName())
		LOGGER.debug("> Assigning '{0}' editor to '{1}' tab index.".format(editor, index))
		self.Script_Editor_tabWidget.setCurrentIndex(index)

		# Signals / Slots.
		editor.patternsReplaced.connect(self.__editor__patternsReplaced)
		editor.languageChanged.connect(self.__editor__languageChanged)
		editor.titleChanged.connect(self.__editor__titleChanged)
		editor.fileChanged.connect(self.__editor__fileChanged)
		editor.cursorPositionChanged.connect(self.Editor_Status_editorStatus._EditorStatus__editor__cursorPositionChanged)
		return index

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeEditorTab(self, index):
		"""
		This method removes the **Script_Editor_tabWidget** Widget tab with given index.

		:param index: Tab index. ( Integer )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Removing tab with index '{0}'.".format(index))
		self.Script_Editor_tabWidget.widget(index).setParent(None)
		self.Script_Editor_tabWidget.removeTab(index)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getEditorTab(self, editor):
		"""
		This method returns the **Script_Editor_tabWidget** Widget tab associated with the given editor.

		:param Editor: Editor to search tab for. ( Editor )
		:return: Tab index. ( Editor )
		"""

		for i in range(self.Script_Editor_tabWidget.count()):
			if not self.Script_Editor_tabWidget.widget(i) == editor:
				continue
			LOGGER.debug("> Editor '{0}': Tab index '{1}'.".format(editor, i))
			return i

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def findEditorTab(self, file):
		"""
		This method finds the **Script_Editor_tabWidget** Widget tab associated with the given file.

		:param file: File to search tab for. ( String )
		:return: Tab index. ( Editor )
		"""

		for i in range(self.Script_Editor_tabWidget.count()):
			if not self.Script_Editor_tabWidget.widget(i).file == file:
				continue
			LOGGER.debug("> File '{0}': Tab index '{1}'.".format(file, i))
			return i

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def hasEditorTab(self):
		"""
		This method returns if the **Script_Editor_tabWidget** Widget has at least one tab.

		:return: Has tab. ( Boolean )
		"""

		return self.Script_Editor_tabWidget.count() and True or False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listEditors(self):
		"""
		This method lists the **Script_Editor_tabWidget** Widget tab editors.

		:return: Editors. ( List )
		"""

		return [self.Script_Editor_tabWidget.widget(i) for i in range(self.Script_Editor_tabWidget.count())]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setEditorLanguage(self, editor, language, emitSignal=True):
		"""
		This method sets given language to given **Script_Editor_tabWidget** Widget tab editor.
		
		:param editor: Editor to set language to. ( Editor )
		:param language: Language to set. ( Language )
		:param emitSignal: Emit signal. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Setting '{0}' language to '{1}' editor.".format(language.name, editor))

		return editor.setLanguage(language, emitSignal)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getCurrentEditor(self):
		"""
		This method returns the current **Script_Editor_tabWidget** Widget tab editor.

		:return: Current editor. ( Editor )
		"""

		if not self.hasEditorTab():
			return

		return self.Script_Editor_tabWidget.currentWidget()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def focusEditor(self, file):
		"""
		This method focus the **Script_Editor_tabWidget** Widget tab editor with given file.

		:param file: File. ( String )
		:return: Method success. ( Boolean )
		"""

		index = self.findEditorTab(file)
		if index is not None:
			self.Script_Editor_tabWidget.setCurrentIndex(index)
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def findEditor(self, file):
		"""
		This method finds the **Script_Editor_tabWidget** Widget tab editor associated to given file.

		:param file: File to search editors for. ( String )
		:return: Editor. ( Editor )
		"""

		for i in range(self.Script_Editor_tabWidget.count()):
			if not self.Script_Editor_tabWidget.widget(i).file == file:
				continue

			LOGGER.debug("> File '{0}: Editor index '{1}'.".format(file, i))
			return self.Script_Editor_tabWidget.widget(i)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def hasFile(self, file):
		"""
		This method returns if given file is loaded in any of the **Script_Editor_tabWidget** Widget tab editors.

		:param file: File. ( String )
		:return: Is file loaded. ( Boolean )
		"""

		return self.findEditor(file) and True or False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, 	Exception)
	def loadDocument(self, document, file):
		"""
		This method loads given document into a new **Script_Editor_tabWidget** Widget tab editor.

		:param document: Document to load. ( QTextDocument )
		:param file: Document file. ( String )
		:return: Method success. ( Boolean )
		"""

		editor = Editor(parent=self, language=self.__languagesModel.getLanguage(self.__defaultLanguage))
		if not editor.newFile():
			return

		LOGGER.info("{0} | Loading '{1}' file!".format(self.__class__.__name__, file))
		if not editor.loadDocument(document, file, self.__languagesModel.getFileLanguage(file)):
			return

		index = self.addEditorTab(editor)
		self.__setEditorTabName(index)
		self.__setWindowTitle()
		self.__storeRecentFile(file)
		self.__registerFile(file)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def newFile(self):
		"""
		This method creates a new file into a new **Script_Editor_tabWidget** Widget tab.

		:return: Method success. ( Boolean )
		"""

		editor = Editor(parent=self, language=self.__languagesModel.getLanguage(self.__defaultScriptLanguage))
		LOGGER.info("{0} | Creating '{1}' file!".format(self.__class__.__name__, editor.getNextUntitledFileName()))
		if editor.newFile():
			self.addEditorTab(editor)
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
	def loadFile(self, file):
		"""
		This method loads user chosen file in a new **Script_Editor_tabWidget** Widget tab editor.

		:param file: File to load. ( String )
		:return: Method success. ( Boolean )
		"""

		if not foundations.common.pathExists(file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
			self.__class__.__name__, file))

		if self.focusEditor(file):
			LOGGER.info("{0} | '{1}' is already loaded!".format(self.__class__.__name__, file))
			return True

		currentEditor = self.getCurrentEditor()
		if self.Script_Editor_tabWidget.count() == 1 and currentEditor.isUntitled and \
		not currentEditor.isModified():
			self.__unregisterFile(currentEditor.file)
			self.removeEditorTab(self.Script_Editor_tabWidget.currentIndex())

		LOGGER.info("{0} | Loading '{1}' file!".format(self.__class__.__name__, file))
		editor = Editor(parent=self, language=self.__languagesModel.getFileLanguage(file) or \
		self.__languagesModel.getLanguage(self.__defaultLanguage))

		if editor.loadFile(file):
			self.addEditorTab(editor)
			self.__storeRecentFile(file)
			self.__registerFile(file)
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
	def reloadFile(self, file):
		"""
		This method reloads current **Script_Editor_tabWidget** Widget tab editor file content.

		:param file: File to reload. ( String )
		:return: Method success. ( Boolean )
		"""

		if not foundations.common.pathExists(file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
			self.__class__.__name__, file))

		index = self.findEditorTab(file)
		if index >= 0:
			LOGGER.info("{0} | Reloading '{1}' file!".format(self.__class__.__name__, file))
			editor = self.Script_Editor_tabWidget.widget(index)
			return editor.reloadFile()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def saveFile(self, file=None):
		"""
		This method saves either given file or current **Script_Editor_tabWidget** Widget tab editor file.

		:param file: File to save. ( String )
		:return: Method success. ( Boolean )
		"""

		if self.hasEditorTab():
			editor = file and self.findEditor(file) or self.getCurrentEditor()
			LOGGER.info("{0} | Saving '{1}' file!".format(self.__class__.__name__, editor.file))
			self.__stopfileSystemWatcher()
			editor.saveFile()
			self.__startfileSystemWatcher()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def saveFileAs(self):
		"""
		This method saves current **Script_Editor_tabWidget** Widget tab editor file as user chosen file.

		:return: Method success. ( Boolean )
		"""

		editor = self.getCurrentEditor()
		if not editor:
			return

		LOGGER.info("{0} | Saving '{1}' file!".format(self.__class__.__name__, editor.file))
		if editor.saveFileAs():
			self.__storeRecentFile(editor.file)
			self.__registerFile(editor.file)
			language = self.__languagesModel.getFileLanguage(editor.file) or \
					self.__languagesModel.getLanguage(self.__defaultLanguage)
			if editor.language.name != language.name:
				self.setEditorLanguage(editor, language)
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	@umbra.engine.encapsulateProcessing
	def saveAllFiles(self):
		"""
		This method saves all **Script_Editor_tabWidget** Widget tab editor files.

		:return: Method success. ( Boolean )
		"""

		self.__stopfileSystemWatcher()

		editorsCount = self.Script_Editor_tabWidget.count()

		self.__engine.startProcessing("Saving All Files ...", editorsCount)
		success = True
		for i in range(editorsCount):
			editor = self.Script_Editor_tabWidget.widget(i)
			if editor.isModified():
				LOGGER.info("{0} | Saving '{1}' file!".format(self.__class__.__name__, editor.file))
				success *= editor.saveFile()
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()

		self.__startfileSystemWatcher()
		return success

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def closeFile(self, file=None):
		"""
		This method closes either given file or current **Script_Editor_tabWidget** Widget tab editor file.

		:param file: File to save. ( String )
		:return: Method success. ( Boolean )
		"""

		editor = file and self.findEditor(file) or self.getCurrentEditor()
		if not editor:
			return

		LOGGER.info("{0} | Closing '{1}' file!".format(self.__class__.__name__, editor.file))
		if not editor.closeFile():
			return

		self.__unregisterFile(editor.file)

		if self.removeEditorTab(self.Script_Editor_tabWidget.currentIndex()):
			not self.hasEditorTab() and self.newFile()
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	@umbra.engine.encapsulateProcessing
	def closeAllFiles(self, leaveLastEditor=True):
		"""
		This method closes every opened files and removes their associated **Script_Editor_tabWidget** Widget tabs.

		:return: Method success. ( Boolean )
		"""

		editorsCount = self.Script_Editor_tabWidget.count()
		self.__engine.startProcessing("Closing All Files ...", editorsCount)
		for editor in self.listEditors():
			LOGGER.info("{0} | Closing '{1}' file!".format(self.__class__.__name__, editor.file))
			if not editor.closeFile():
				return

			self.__unregisterFile(editor.file)

			if self.removeEditorTab(self.Script_Editor_tabWidget.currentIndex()):
				if not self.hasEditorTab() and leaveLastEditor:
					self.newFile()
			self.__engine.stepProcessing()
		self.__engine.stopProcessing()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler, False, Exception)
	def gotoLine(self):
		"""
		This method moves current **Script_Editor_tabWidget** Widget tab editor cursor to user defined line.

		:return: Method success. ( Boolean )

		:note: This method may require user interaction.
		"""

		editor = self.getCurrentEditor()
		if not editor:
			return

		line, state = QInputDialog.getInt(self, "Goto Line Number", "Line number:", min=1)
		if not state:
			return

		LOGGER.debug("> Chosen line number: '{0}'.".format(line))
		return editor.gotoLine(line)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def evaluateSelection(self):
		"""
		This method evaluates current **Script_Editor_tabWidget** Widget tab editor
		selected content in the interactive console.

		:return: Method success. ( Boolean )
		"""

		editor = self.getCurrentEditor()
		if not editor:
			return

		LOGGER.debug("> Evaluating 'Script Editor' selected content.")
		if self.evaluateCode(str(editor.textCursor().selectedText().replace(QChar(QChar.ParagraphSeparator),
																			QString("\n")))):
			self.uiRefresh.emit()
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def evaluateScript(self):
		"""
		This method evaluates current **Script_Editor_tabWidget** Widget tab editor content into the interactive console.

		:return: Method success. ( Boolean )
		"""

		editor = self.getCurrentEditor()
		if not editor:
			return

		LOGGER.debug("> Evaluating 'Script Editor' content.")
		if self.evaluateCode(str(editor.toPlainText())):
			self.uiRefresh.emit()
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def evaluateCode(self, code):
		"""
		This method evaluates given code into the interactive console.

		:param code: Code to evaluate. ( String )
		:return: Method success. ( Boolean )
		"""

		if not code:
			return

		LOGGER.debug("> Evaluating provided code.")

		code = code.endswith("\n") and code or "{0}\n".format(code)
		sys.stdout.write(code)
		self.__console.runcode(code)

		return True
