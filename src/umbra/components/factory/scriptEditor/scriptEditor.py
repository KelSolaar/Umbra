#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**scriptEditor.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`ScriptEditor` Component Interface class and the :class:`CodeEditor class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import code
import functools
import logging
import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.io as io
import foundations.strings
from manager.uiComponent import UiComponent
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals
from umbra.globals.uiConstants import UiConstants
from umbra.ui.completers import PythonCompleter
from umbra.ui.highlighters import LoggingHighlighter, PythonHighlighter
from umbra.ui.widgets.codeEditor_QPlainTextEdit import CodeEditor_QPlainTextEdit

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "CodeEditor", "ScriptEditor"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class CodeEditor(CodeEditor_QPlainTextEdit):
	"""
	| This class defines the default editor used by the: class:`ScriptEditor`. 
	"""

	__titleNumber = 1

	# Custom signals definitions.
	contentChanged = pyqtSignal()
	fileChanged = pyqtSignal()

	@core.executionTrace
	def __init__(self, file=None):
		"""
		This method initializes the class.

		:param script: Script path. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		CodeEditor_QPlainTextEdit.__init__(self)

		# --- Setting class attributes. ---
		self.__file = None
		self.file = file

		self.__isUntitled = True
		self.__defaultFileName = "Untitled"
		self.__defaultFileExtension = "py"

		self.setAttribute(Qt.WA_DeleteOnClose)

		self.highlighter = PythonHighlighter(self.document())
		self.setCompleter(PythonCompleter())

		file and self.loadFile(file)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def file(self):
		"""
		This method is the property for **self.__file** attribute.

		:return: self.__file. ( String )
		"""

		return self.__file

	@file.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def file(self, value):
		"""
		This method is the setter method for **self.__file** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("file", value)
		self.__file = value

	@file.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def file(self):
		"""
		This method is the deleter method for **self.__file** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("file"))

	@property
	def isUntitled(self):
		"""
		This method is the property for **self.__isUntitled** attribute.

		:return: self.__isUntitled. ( Boolean )
		"""

		return self.__isUntitled

	@isUntitled.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def isUntitled(self, value):
		"""
		This method is the setter method for **self.__isUntitled** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("isUntitled"))

	@isUntitled.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def isUntitled(self):
		"""
		This method is the deleter method for **self.__isUntitled** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("isUntitled"))

	@property
	def defaultFileName(self):
		"""
		This method is the property for **self.__defaultFileName** attribute.

		:return: self.__defaultFileName. ( String )
		"""

		return self.__defaultFileName

	@defaultFileName.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultFileName(self, value):
		"""
		This method is the setter method for **self.__defaultFileName** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("defaultFileName"))

	@defaultFileName.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultFileName(self):
		"""
		This method is the deleter method for **self.__defaultFileName** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultFileName"))

	@property
	def defaultFileExtension(self):
		"""
		This method is the property for **self.__defaultFileExtension** attribute.

		:return: self.__defaultFileExtension. ( String )
		"""

		return self.__defaultFileExtension

	@defaultFileExtension.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultFileExtension(self, value):
		"""
		This method is the setter method for **self.__defaultFileExtension** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("defaultFileExtension"))

	@defaultFileExtension.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultFileExtension(self):
		"""
		This method is the deleter method for **self.__defaultFileExtension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultFileExtension"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __setFile(self, file):
		"""
		This method sets the code editor file.

		:param File: File to set. ( String )
		"""

		self.__file = file
		self.__isUntitled = False
		self.document().setModified(False)
		self.setWindowTitle("{0}".format(self.getFileShortName()))

		self.emit(SIGNAL("fileChanged()"))

	@core.executionTrace
	def __codeEditor__contentsChanged(self):
		"""
		This method is triggered when the code editor content changes.
		"""

		titleTemplate = self.document().isModified() and "{0} *" or "{0}"
		self.setWindowTitle(titleTemplate.format(self.getFileShortName()))

		self.emit(SIGNAL("contentChanged()"))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getFileShortName(self):
		"""
		This method returns the current file short name.

		:return: File short name. ( String )
		"""

		if not self.__file:
			return

		return foundations.strings.getSplitextBasename(self.__file)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def newFile(self):
		"""
		This method creates a new file.

		:return: Method success. ( Boolean )
		"""

		self.__isUntitled = True
		self.__file = "{0}_{1}.{2}".format(self.__defaultFileName, CodeEditor._CodeEditor__titleNumber, self.defaultFileExtension)
		CodeEditor._CodeEditor__titleNumber += 1
		self.setWindowTitle("{0}".format(self.__file))

		# Signals / Slots.
		self.document().contentsChanged.connect(self.__codeEditor__contentsChanged)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
	def loadFile(self, file):
		"""
		This method reads and loads provided file into the code editor.

		:param File: File to load. ( String )
		:return: Method success. ( Boolean )
		"""

		if not os.path.exists(file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(self.__class__.__name__, file))

		LOGGER.info("{0} | Loading '{1}' file into code editor!".format(self.__class__.__name__, file))
		reader = io.File(file)
		reader.read() and self.setPlainText("".join(reader.content))
		self.__setFile(file)

		# Signals / Slots.
		self.document().contentsChanged.connect(self.__codeEditor__contentsChanged)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def saveFile(self):
		"""
		This method saves the code editor content.

		:return: Method success. ( Boolean )
		"""

		if not self.__isUntitled:
			return self.writeFile(self.__file)
		else:
			return self.saveFileAs()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def saveFileAs(self):
		"""
		This method saves the code editor content into user defined file.

		:return: Method success. ( Boolean )
		"""

		file = QFileDialog.getSaveFileName(self, "Save As", self.__file)
		if not file:
			return

		file = str(file)
		if self.writeFile(file):
			self.__setFile(file)
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def writeFile(self, file):
		"""
		This method writes the code editor content into provided file.

		:param file: File to write. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.info("{0} | Writing '{1}' file!".format(self.__class__.__name__, file))
		writer = io.File(file)
		writer.content = [self.toPlainText()]
		return writer.write()

class ScriptEditor(UiComponent):
	"""
	| This class is the :mod:`umbra.components.addons.scriptEditor.scriptEditor` Component Interface class.
	"""

	# Custom signals definitions.
	datasChanged = pyqtSignal()

	@core.executionTrace
	def __init__(self, name=None, uiFile=None):
		"""
		This method initializes the class.

		:param name: Component name. (String)
		:param uiFile: Ui file. (String)
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		UiComponent.__init__(self, name=name, uiFile=uiFile)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__uiPath = "ui/Script_Editor.ui"
		self.__dockArea = 8

		self.__container = None

		self.__defaultWindowTitle = "Script Editor"
		self.__defaultScriptEditorDirectory = "scriptEditor"
		self.__defaultScriptEditorFile = "defaultScript.py"
		self.__scriptEditorFile = None

		self.__locals = None
		self.__memoryHandlerStackDepth = None
		self.__menuBar = None

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiPath(self):
		"""
		This method is the property for ** self.__uiPath ** attribute.

		:return: self.__uiPath. (String)
		"""

		return self.__uiPath

	@uiPath.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiPath(self, value):
		"""
		This method is the setter method for ** self.__uiPath ** attribute.

		:param value: Attribute value. (String)
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

		:return: self.__dockArea. (Integer)
		"""

		return self.__dockArea

	@dockArea.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self, value):
		"""
		This method is the setter method for ** self.__dockArea ** attribute.

		:param value: Attribute value. (Integer)
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

		:return: self.__container. (QObject)
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for ** self.__container ** attribute.

		:param value: Attribute value. (QObject)
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
	def defaultWindowTitle(self):
		"""
		This method is the property for ** self.__defaultWindowTitle ** attribute.

		:return: self.__defaultWindowTitle. (String)
		"""

		return self.__defaultWindowTitle

	@defaultWindowTitle.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultWindowTitle(self, value):
		"""
		This method is the setter method for ** self.__defaultWindowTitle ** attribute.

		:param value: Attribute value. (String)
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

		:return: self.__defaultScriptEditorDirectory. (String)
		"""

		return self.__defaultScriptEditorDirectory

	@defaultScriptEditorDirectory.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultScriptEditorDirectory(self, value):
		"""
		This method is the setter method for ** self.__defaultScriptEditorDirectory ** attribute.

		:param value: Attribute value. (String)
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

		:return: self.__defaultScriptEditorFile. (String)
		"""

		return self.__defaultScriptEditorFile

	@defaultScriptEditorFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultScriptEditorFile(self, value):
		"""
		This method is the setter method for ** self.__defaultScriptEditorFile ** attribute.

		:param value: Attribute value. (String)
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

		:return: self.__scriptEditorFile. (String)
		"""

		return self.__scriptEditorFile

	@scriptEditorFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def scriptEditorFile(self, value):
		"""
		This method is the setter method for ** self.__scriptEditorFile ** attribute.

		:param value: Attribute value. (String)
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
	def locals(self):
		"""
		This method is the property for ** self.__locals ** attribute.

		:return: self.__locals. (Dictionary)
		"""

		return self.__locals

	@locals.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def locals(self, value):
		"""
		This method is the setter method for ** self.__locals ** attribute.

		:param value: Attribute value. (Dictionary)
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

		:return: self.__memoryHandlerStackDepth. (Integer)
		"""

		return self.__memoryHandlerStackDepth

	@memoryHandlerStackDepth.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def memoryHandlerStackDepth(self, value):
		"""
		This method is the setter method for ** self.__memoryHandlerStackDepth ** attribute.

		:param value: Attribute value. (Integer)
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

		:return: self.__menuBar. (QToolbar)
		"""

		return self.__menuBar

	@menuBar.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def menuBar(self, value):
		"""
		This method is the setter method for ** self.__menuBar ** attribute.

		:param value: Attribute value. (QToolbar)
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("menuBar"))

	@menuBar.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def menuBar(self):
		"""
		This method is the deleter method for ** self.__menuBar ** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("menuBar"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def activate(self, container):
		"""
		This method activates the Component.

		:param container: Container to attach the Component to. (QObject)
		:return: Method success. (Boolean)
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.uiFile = os.path.join(os.path.dirname(core.getModule(self).__file__), self.__uiPath)
		self.__container = container

		self.__defaultScriptEditorDirectory = os.path.join(self.__container.userApplicationDatasDirectory, Constants.ioDirectory, self.__defaultScriptEditorDirectory)
		not os.path.exists(self.__defaultScriptEditorDirectory) and os.makedirs(self.__defaultScriptEditorDirectory)
		self.__defaultScriptEditorFile = os.path.join(self.__defaultScriptEditorDirectory, self.__defaultScriptEditorFile)

#		self.__getsLocals()
#		self.__console = code.InteractiveConsole(self.__locals)

		return UiComponent.activate(self)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		This method deactivates the Component.

		:return: Method success. (Boolean)
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component cannot be deactivated!".format(self.__name))

	@core.executionTrace
	def initializeUi(self):
		"""
		This method initializes the Component ui.

		:return: Method success. (Boolean)
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__menuBar = QMenuBar()
		self.__menuBar.setNativeMenuBar(False)
		self.ui.menuBar_frame_gridLayout.addWidget(self.__menuBar)
		self.__initializeMenuBar()

#		self.ui.Script_Editor_Input_plainTextEdit = CodeEditor_QPlainTextEdit(self)
#		self.ui.Script_Editor_gridLayout.addWidget(self.ui.Script_Editor_Input_plainTextEdit, 0, 0)

#		self.ui.Script_Editor_Input_plainTextEdit.highlighter = PythonHighlighter(self.ui.Script_Editor_Input_plainTextEdit.document())
#		self.ui.Script_Editor_Input_plainTextEdit.setCompleter(PythonCompleter())
		self.ui.Script_Editor_Output_plainTextEdit.highlighter = LoggingHighlighter(self.ui.Script_Editor_Output_plainTextEdit.document())

		# Signals / Slots.
		self.__container.timer.timeout.connect(self.__Script_Editor_Output_plainTextEdit_refreshUi)
#		self.ui.Evaluate_Script_pushButton.clicked.connect(self.__Evaluate_Script_pushButton__clicked)
#		self.datasChanged.connect(self.__Script_Editor_Output_plainTextEdit_refreshUi)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uninitializeUi(self):
		"""
		This method uninitializes the Component ui.

		:return: Method success. (Boolean)
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' Component ui cannot be uninitialized!".format(self.name))

	@core.executionTrace
	def addWidget(self):
		"""
		This method adds the Component Widget to the container.

		:return: Method success. (Boolean)
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__container.addDockWidget(Qt.DockWidgetArea(self.__dockArea), self.ui)

		return True

	@core.executionTrace
	def removeWidget(self):
		"""
		This method removes the Component Widget from the container.

		:return: Method success. (Boolean)
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

		LOGGER.debug("> Calling '{0}' Component Framework startup method.".format(self.__class__.__name__))

		os.path.exists(self.__defaultScriptEditorFile) and self.loadFile(self.__defaultScriptEditorFile)

	@core.executionTrace
	def __initializeMenuBar(self):
		"""
		This method initializes Component menuBar.
		"""

		self.__fileMenu = QMenu("&File")
		self.__fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|&New file ...", shortcut=QKeySequence.New, slot=self.__newFileAction__triggered))
#		self.__fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|&Load file ...", shortcut=QKeySequence.Open, slot=self.__loadFileAction__triggered))
#		self.__fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|Source file ...", slot=self.__sourceFileAction__triggered))
		self.__fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|&Save file ...", shortcut=QKeySequence.Save, slot=self.__saveFileAction__triggered))
		self.__menuBar.addMenu(self.__fileMenu)
#
#		self.__editMenu = QMenu("&Edit")
#		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|&Undo", shortcut=QKeySequence.Undo, slot=self.__undoAction__triggered))
#		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|&Redo", shortcut=QKeySequence.Redo, slot=self.__redoAction__triggered))
#		self.__editMenu.addSeparator()
#		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|Cu&t", shortcut=QKeySequence.Cut, slot=self.__cutAction__triggered))
#		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|&Copy", shortcut=QKeySequence.Copy, slot=self.__copyAction__triggered))
#		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|&Paste", shortcut=QKeySequence.Paste, slot=self.__pasteAction__triggered))
#		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|Delete", slot=self.__deleteAction__triggered))
#		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|Select All", shortcut=QKeySequence.SelectAll, slot=self.__selectAllAction__triggered))
#		self.__menuBar.addMenu(self.__editMenu)
#
#		self.__commandMenu = QMenu("&Command")
#		self.__commandMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Command|&Evaluate Selection", shortcut=Qt.ControlModifier + Qt.Key_Return, slot=self.__evaluateSelectionAction__triggered))
#		self.__commandMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Command|Evaluate &Script", shortcut=Qt.SHIFT + Qt.CTRL + Qt.Key_Return, slot=self.__evaluateScriptAction__triggered))
#		self.__menuBar.addMenu(self.__commandMenu)

	# @core.executionTrace
	def __Script_Editor_Output_plainTextEdit_setUi(self):
		"""
		This method sets the ** Script_Editor_Output_plainTextEdit ** Widget.
		"""

		for line in self.__container.loggingSessionHandlerStream.stream:
			self.ui.Script_Editor_Output_plainTextEdit.moveCursor(QTextCursor.End)
			self.ui.Script_Editor_Output_plainTextEdit.insertPlainText(line)
		self.__Script_Editor_Output_plainTextEdit__setDefaultViewState()

	# @core.executionTrace
	def __Script_Editor_Output_plainTextEdit__setDefaultViewState(self):
		"""
		This method sets the ** Script_Editor_Output_plainTextEdit ** Widget.
		"""

		self.ui.Script_Editor_Output_plainTextEdit.moveCursor(QTextCursor.End)
		self.ui.Script_Editor_Output_plainTextEdit.ensureCursorVisible()

	# @core.executionTrace
	def __Script_Editor_Output_plainTextEdit_refreshUi(self):
		"""
		This method updates the ** Script_Editor_Output_plainTextEdit ** Widget.
		"""

		memoryHandlerStackDepth = len(self.__container.loggingSessionHandlerStream.stream)
		if memoryHandlerStackDepth != self.__memoryHandlerStackDepth:
			for line in self.__container.loggingSessionHandlerStream.stream[self.__memoryHandlerStackDepth:memoryHandlerStackDepth]:
				self.ui.Script_Editor_Output_plainTextEdit.moveCursor(QTextCursor.End)
				self.ui.Script_Editor_Output_plainTextEdit.insertPlainText(line)
			self.__Script_Editor_Output_plainTextEdit__setDefaultViewState()
			self.__memoryHandlerStackDepth = memoryHandlerStackDepth

	@core.executionTrace
	def __newFileAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|&New file ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.newFile()

	@core.executionTrace
	def __saveFileAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|&Save file ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.saveFile()

#	@core.executionTrace
#	def __loadFileAction__triggered(self, checked):
#		"""
#		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|&Load file ...'** action.
#
#		:param checked: Checked state. ( Boolean )
#		:return: Method success. ( Boolean )
#		"""
#
#		return self.loadFile(self.__defaultScriptEditorFile)
#
#	@core.executionTrace
#	def __sourceScriptAction__triggered(self, checked):
#		"""
#		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|Source file ...'** action.
#
#		:param checked: Checked state. ( Boolean )
#		:return: Method success. ( Boolean )
#		"""
#
#		print "sourceScriptAction"
#
#	@core.executionTrace
#	def __saveScriptAction__triggered(self, checked):
#		"""
#		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|&Save file ...'** action.
#
#		:param checked: Checked state. ( Boolean )
#		:return: Method success. ( Boolean )
#		"""
#
#		print "saveScriptAction"
#
#	@core.executionTrace
#	def __undoAction__triggered(self, checked):
#		"""
#		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Undo'** action.
#
#		:param checked: Checked state. ( Boolean )
#		:return: Method success. ( Boolean )
#		"""
#
#		print "undoAction"
#
#	@core.executionTrace
#	def __redoAction__triggered(self, checked):
#		"""
#		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Redo'** action.
#
#		:param checked: Checked state. ( Boolean )
#		:return: Method success. ( Boolean )
#		"""
#
#		print "redoAction"
#
#	@core.executionTrace
#	def __cutAction__triggered(self, checked):
#		"""
#		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|Cu&t'** action.
#
#		:param checked: Checked state. ( Boolean )
#		:return: Method success. ( Boolean )
#		"""
#
#		print "cutAction"
#
#	@core.executionTrace
#	def __copyAction__triggered(self, checked):
#		"""
#		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Copy'** action.
#
#		:param checked: Checked state. ( Boolean )
#		:return: Method success. ( Boolean )
#		"""
#
#		print "copyAction"
#
#	@core.executionTrace
#	def __pasteAction__triggered(self, checked):
#		"""
#		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Paste'** action.
#
#		:param checked: Checked state. ( Boolean )
#		:return: Method success. ( Boolean )
#		"""
#
#		print "pasteAction"
#
#	@core.executionTrace
#	def __deleteAction__triggered(self, checked):
#		"""
#		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|Delete'** action.
#
#		:param checked: Checked state. ( Boolean )
#		:return: Method success. ( Boolean )
#		"""
#
#		print "deleteAction"
#
#	@core.executionTrace
#	def __selectAllAction__triggered(self, checked):
#		"""
#		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|Select All'** action.
#
#		:param checked: Checked state. ( Boolean )
#		:return: Method success. ( Boolean )
#		"""
#
#		print "selectAllAction"
#
#	@core.executionTrace
#	def __evaluateSelectionAction__triggered(self, checked):
#		"""
#		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Command|&Evaluate Selection'** action.
#
#		:param checked: Checked state. ( Boolean )
#		:return: Method success. ( Boolean )
#		"""
#
#		return self.evaluateSelection()
#
#	@core.executionTrace
#	def __evaluateScriptAction__triggered(self, checked):
#		"""
#		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Command|Evaluate &Script'** action.
#
#		:param checked: Checked state. ( Boolean )
#		:return: Method success. ( Boolean )
#		"""
#
#		return self.evaluateScript()
#
#	@core.executionTrace
#	def __Evaluate_Script_pushButton__clicked(self, checked):
#		"""
#		This method is triggered when **Evaluate_Script_pushButton** is clicked.
#
#		:param checked: Checked state. ( Boolean )
#		"""
#
#		self.evaluateScript()
#
#	@core.executionTrace
#	def __getsLocals(self):
#		"""
#		This method gets the locals for the interactive console.
#
#		:return: Method success. ( Boolean )
#		"""
#
#		self.__locals = {}
#
#		for globals in (Constants, RuntimeGlobals, UiConstants):
#			self.__locals[globals.__name__] = globals
#
#		self.__locals[Constants.applicationName] = self.__container
#		self.__locals["componentsManager"] = self.__container.componentsManager
#
#		return True
#
	@core.executionTrace
	def __codeEditor__contentChanged(self, tabIndex):
		"""
		This method is triggered when a code editor content changes.

		:param tabIndex: Index of the tab containing the code editor. ( Integer )
		"""
		self.__setCodeEditorTabName(tabIndex)

	@core.executionTrace
	def __codeEditor__fileChanged(self, tabIndex):
		"""
		This method is triggered when a code editor file changes.

		:param tabIndex: Index of the tab containing the code editor. ( Integer )
		"""

		self.__setCodeEditorTabName(tabIndex)

	@core.executionTrace
	def __setCodeEditorTabName(self, tabIndex):
		"""
		This method sets the code editor tab name.

		:param tabIndex: Index of the tab containing the code editor. ( Integer )
		"""

		self.ui.Script_Editor_tabWidget.setTabText(tabIndex, self.ui.Script_Editor_tabWidget.widget(tabIndex).windowTitle())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addCodeEditorTab(self, codeEditor):
		"""
		This method adds a new tab to the **Script_Editor_tabWidget** widget and sets provided code editor as child widget.

		:param codeEditor: Code editor. ( CodeEditor )
		:return: New tab index. ( Integer )
		"""

		tabIndex = self.ui.Script_Editor_tabWidget.addTab(codeEditor, codeEditor.getFileShortName())
		self.ui.Script_Editor_tabWidget.setCurrentIndex(tabIndex)

		# Signals / Slots.
		codeEditor.contentChanged.connect(functools.partial(self.__codeEditor__contentChanged, tabIndex))
		codeEditor.fileChanged.connect(functools.partial(self.__codeEditor__fileChanged, tabIndex))
		return tabIndex

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def createCodeEditor(self):
		"""
		This method creates a new :class:`CodeEditor` instance and add it to the **Script_Editor_tabWidget** widget.

		:param file: File to load. ( String )
		:return: Code editor. ( CodeEditor )
		"""

		codeEditor = CodeEditor()
		return codeEditor

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def newFile(self):
		"""
		This method creates new file into a new :class:`CodeEditor` instance.

		:return: Method success. ( Boolean )
		"""

		codeEditor = self.createCodeEditor()
		if codeEditor.newFile():
			self.addCodeEditorTab(codeEditor)
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
	def loadFile(self, file):
		"""
		This method reads and loads provided file into a new or already existing :class:`CodeEditor` instance.

		:param file: File to load. ( String )
		:return: Method success. ( Boolean )
		"""

		if not os.path.exists(file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(self.__class__.__name__, file))

		existingCodeEditor = self.findCodeEditor(file)
		if existingCodeEditor:
			# Set active tab to document.			
			return

		LOGGER.info("{0} | Loading '{1}' file into 'Script_Editor_tabWidget'!".format(self.__class__.__name__, file))
		codeEditor = self.createCodeEditor()
		if codeEditor.loadFile(file):
			self.addCodeEditorTab(codeEditor)
			return True

	@core.executionTrace
	def saveFile(self):
		"""
		This method saves current :class:`CodeEditor` instance file.

		:return: Method success. ( Boolean )
		"""

		if self.ui.Script_Editor_tabWidget.count():
			return self.ui.Script_Editor_tabWidget.currentWidget().saveFile()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def findCodeEditor(self, file):
		"""
		This method finds the :class:`CodeEditor` instance associated to the provided file.

		:param file: File to search code editors for. ( String )
		:return: Code editor. ( CodeEditor )
		"""

		pass

#		for codeEditor in self.ui.Script_Editor_mdiArea.subWindowList():
#			if codeEditor.widget().currentFile() == file:
#				return codeEditor

#	@core.executionTrace
#	@foundations.exceptions.exceptionsHandler(None, False, Exception)
#	def evaluateSelection(self):
#		"""
#		This method evaluates **Script_Editor_Input_plainTextEdit** widget selected content in the interactive console.
#
#		:return: Method success. ( Boolean )
#		"""
#
#		if self.evaluateCode(str(self.ui.Script_Editor_Input_plainTextEdit.textCursor().selectedText().replace(QChar(QChar.ParagraphSeparator), QString("\n")))):
#			self.emit(SIGNAL("datasChanged()"))
#			return True
#
#	@core.executionTrace
#	@foundations.exceptions.exceptionsHandler(None, False, Exception)
#	def evaluateScript(self):
#		"""
#		This method evaluates **Script_Editor_Input_plainTextEdit** widget content in the interactive console.
#
#		:return: Method success. ( Boolean )
#		"""
#
#		if self.evaluateCode(str(self.ui.Script_Editor_Input_plainTextEdit.toPlainText())):
#			self.emit(SIGNAL("datasChanged()"))
#			return True
#
#	@core.executionTrace
#	@foundations.exceptions.exceptionsHandler(None, False, Exception)
#	def evaluateCode(self, code):
#		"""
#		This method evaluates provided code in the interactive console.
#
#		:param code: Code to evaluate. ( String )
#		:return: Method success. ( Boolean )
#		"""
#
#		sys.stdout.write(code)
#		self.__console.runcode(code)
#
#		return True
