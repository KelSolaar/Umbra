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
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.io as io

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

__all__ = ["LOGGER", "ScriptEditor"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("dockArea"))

	@dockArea.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def dockArea(self):
		"""
		This method is the deleter method for **self.__dockArea** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("dockArea"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("defaultWindowTitle"))

	@defaultWindowTitle.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultWindowTitle(self):
		"""
		This method is the deleter method for **self.__defaultWindowTitle** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultWindowTitle"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("defaultScriptEditorDirectory"))

	@defaultScriptEditorDirectory.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultScriptEditorDirectory(self):
		"""
		This method is the deleter method for **self.__defaultScriptEditorDirectory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultScriptEditorDirectory"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("defaultScriptEditorFile"))

	@defaultScriptEditorFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultScriptEditorFile(self):
		"""
		This method is the deleter method for **self.__defaultScriptEditorFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("defaultScriptEditorFile"))

	@property
	def scriptEditorFile(self):
		"""
		This method is the property for **self.__scriptEditorFile** attribute.

		:return: self.__scriptEditorFile. ( String )
		"""

		return self.__scriptEditorFile

	@scriptEditorFile.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def scriptEditorFile(self, value):
		"""
		This method is the setter method for **self.__scriptEditorFile** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("scriptEditorFile", value)
		self.__scriptEditorFile = value

	@scriptEditorFile.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def scriptEditorFile(self):
		"""
		This method is the deleter method for **self.__scriptEditorFile** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("scriptEditorFile"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("locals"))

	@locals.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def locals(self):
		"""
		This method is the deleter method for **self.__locals** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("locals"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("memoryHandlerStackDepth"))

	@memoryHandlerStackDepth.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def memoryHandlerStackDepth(self):
		"""
		This method is the deleter method for **self.__memoryHandlerStackDepth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("memoryHandlerStackDepth"))

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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("menuBar"))

	@menuBar.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def menuBar(self):
		"""
		This method is the deleter method for **self.__menuBar** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("menuBar"))

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

		self.__menuBar = QMenuBar()
		self.__menuBar.setNativeMenuBar(False)
		self.ui.menuBar_frame_gridLayout.addWidget(self.__menuBar)
		self.__initializeMenuBar()

		self.ui.Script_Editor_Input_plainTextEdit = CodeEditor_QPlainTextEdit(self)
		self.ui.Script_Editor_gridLayout.addWidget(self.ui.Script_Editor_Input_plainTextEdit, 0, 0)

		self.ui.Script_Editor_Input_plainTextEdit.highlighter = PythonHighlighter(self.ui.Script_Editor_Input_plainTextEdit.document())
		self.ui.Script_Editor_Input_plainTextEdit.setCompleter(PythonCompleter())
		self.ui.Script_Editor_Output_plainTextEdit.highlighter = LoggingHighlighter(self.ui.Script_Editor_Output_plainTextEdit.document())

		# Signals / Slots.
		self.__container.timer.timeout.connect(self.__Script_Editor_Output_plainTextEdit_refreshUi)
		self.ui.Evaluate_Script_pushButton.clicked.connect(self.__Evaluate_Script_pushButton__clicked)
		self.datasChanged.connect(self.__Script_Editor_Output_plainTextEdit_refreshUi)

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

		LOGGER.debug("> Calling '{0}' Component Framework startup method.".format(self.__class__.__name__))

		os.path.exists(self.__defaultScriptEditorFile) and self.loadScript(self.__defaultScriptEditorFile)

	@core.executionTrace
	def __initializeMenuBar(self):
		"""
		This method initializes Component menuBar.
		"""

		self.__fileMenu = QMenu("&File")
		self.__fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|&Load script ...", shortcut=QKeySequence.Open, slot=self.__loadScriptAction__triggered))
		self.__fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|Source script ...", slot=self.__sourceScriptAction__triggered))
		self.__fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|&Save script ...", shortcut=QKeySequence.Save, slot=self.__saveScriptAction__triggered))
		self.__menuBar.addMenu(self.__fileMenu)

		self.__editMenu = QMenu("&Edit")
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|&Undo", shortcut=QKeySequence.Undo, slot=self.__undoAction__triggered))
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|&Redo", shortcut=QKeySequence.Redo, slot=self.__redoAction__triggered))
		self.__editMenu.addSeparator()
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|Cu&t", shortcut=QKeySequence.Cut, slot=self.__cutAction__triggered))
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|&Copy", shortcut=QKeySequence.Copy, slot=self.__copyAction__triggered))
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|&Paste", shortcut=QKeySequence.Paste, slot=self.__pasteAction__triggered))
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|Delete", slot=self.__deleteAction__triggered))
		self.__editMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Edit|Select All", shortcut=QKeySequence.SelectAll, slot=self.__selectAllAction__triggered))
		self.__menuBar.addMenu(self.__editMenu)

		self.__commandMenu = QMenu("&Command")
		self.__commandMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Command|&Evaluate Selection", shortcut=Qt.ControlModifier + Qt.Key_Return, slot=self.__evaluateSelectionAction__triggered))
		self.__commandMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&Command|Evaluate &Script", shortcut=Qt.SHIFT + Qt.CTRL + Qt.Key_Return, slot=self.__evaluateScriptAction__triggered))
		self.__menuBar.addMenu(self.__commandMenu)

	# @core.executionTrace
	def __Script_Editor_Output_plainTextEdit_setUi(self):
		"""
		This method sets the **Script_Editor_Output_plainTextEdit** Widget.
		"""

		for line in self.__container.loggingSessionHandlerStream.stream:
			self.ui.Script_Editor_Output_plainTextEdit.moveCursor(QTextCursor.End)
			self.ui.Script_Editor_Output_plainTextEdit.insertPlainText(line)
		self.__Script_Editor_Output_plainTextEdit__setDefaultViewState()

	# @core.executionTrace
	def __Script_Editor_Output_plainTextEdit__setDefaultViewState(self):
		"""
		This method sets the **Script_Editor_Output_plainTextEdit** Widget.
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
			self.__Script_Editor_Output_plainTextEdit__setDefaultViewState()
			self.__memoryHandlerStackDepth = memoryHandlerStackDepth

	@core.executionTrace
	def __loadScriptAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|&Load script ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		return self.loadScript(self.__defaultScriptEditorFile)

	@core.executionTrace
	def __sourceScriptAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|Source script ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		print "sourceScriptAction"

	@core.executionTrace
	def __saveScriptAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&File|&Save script ...'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		print "saveScriptAction"

	@core.executionTrace
	def __undoAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Undo'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		print "undoAction"

	@core.executionTrace
	def __redoAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Redo'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		print "redoAction"

	@core.executionTrace
	def __cutAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|Cu&t'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		print "cutAction"

	@core.executionTrace
	def __copyAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Copy'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		print "copyAction"

	@core.executionTrace
	def __pasteAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|&Paste'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		print "pasteAction"

	@core.executionTrace
	def __deleteAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|Delete'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		print "deleteAction"

	@core.executionTrace
	def __selectAllAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|&Edit|Select All'** action.

		:param checked: Checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		print "selectAllAction"

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
	def __Evaluate_Script_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Evaluate_Script_pushButton** is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.evaluateScript()

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
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
	def loadScript(self, path):
		"""
		This method reads and loads provided script file path into the **Script_Editor_Input_plainTextEdit** widget.

		:param path: Script to load. ( String )
		:return: Method success. ( Boolean )
		"""

		if not os.path.exists(path):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' script file doesn't exists!".format(self.__class__.__name__, path))

		LOGGER.info("{0} | Loading '{1}' script!".format(self.__class__.__name__, path))
		file = io.File(path)
		file.read() and self.ui.Script_Editor_Input_plainTextEdit.setPlainText("".join(file.content))
		self.ui.setWindowTitle("{0} - {1}".format(self.__defaultWindowTitle, self.__defaultScriptEditorFile))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def evaluateSelection(self):
		"""
		This method evaluates **Script_Editor_Input_plainTextEdit** widget selected content in the interactive console.

		:return: Method success. ( Boolean )
		"""

		if self.evaluateCode(str(self.ui.Script_Editor_Input_plainTextEdit.textCursor().selectedText().replace(QChar(QChar.ParagraphSeparator), QString("\n")))):
			self.emit(SIGNAL("datasChanged()"))
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def evaluateScript(self):
		"""
		This method evaluates **Script_Editor_Input_plainTextEdit** widget content in the interactive console.

		:return: Method success. ( Boolean )
		"""

		if self.evaluateCode(str(self.ui.Script_Editor_Input_plainTextEdit.toPlainText())):
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

		sys.stdout.write(code)
		self.__console.runcode(code)

		return True
