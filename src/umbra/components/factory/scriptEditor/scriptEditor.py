#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**scriptEditor.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`ScriptEditor` Component Interface class and the :class:`Editor class.

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
import foundations.strings
import umbra.ui.widgets.messageBox as messageBox
import umbra.ui.common
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

__all__ = ["LOGGER", "Editor", "ScriptEditor"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Editor(CodeEditor_QPlainTextEdit):
	"""
	| This class defines the default editor used by the: class:`ScriptEditor`. 
	"""

	__instanceId = 1

	# Custom signals definitions.
	contentChanged = pyqtSignal()
	fileChanged = pyqtSignal()

	@core.executionTrace
	def __init__(self, file=None):
		"""
		This method initializes the class.

		:param file: File path. ( String )
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
		This method sets the editor file.

		:param File: File to set. ( String )
		"""

		self.__file = file
		self.__isUntitled = False
		self.document().setModified(False)
		self.setWindowTitle("{0}".format(self.getFileShortName()))

		self.emit(SIGNAL("fileChanged()"))

	@core.executionTrace
	def __editor__contentsChanged(self):
		"""
		This method is triggered when the editor content changes.
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
	def getNextUntitledFileName(self):
		"""
		This method returns the next untitled file name.

		:return: File short name. ( String )
		"""

		name = "{0} {1}.{2}".format(self.__defaultFileName, Editor._Editor__instanceId, self.defaultFileExtension)
		LOGGER.debug("> Next untitled file name: '{0}'.".format(name))
		return name

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def newFile(self):
		"""
		This method creates a new file.

		:return: Method success. ( Boolean )
		"""

		file = self.getNextUntitledFileName()
		LOGGER.debug("> Creating '{0}' file.".format(file))
		self.__file = file
		self.__isUntitled = True
		Editor._Editor__instanceId += 1
		self.setWindowTitle("{0}".format(self.__file))

		# Signals / Slots.
		self.document().contentsChanged.connect(self.__editor__contentsChanged)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
	def loadFile(self, file):
		"""
		This method reads and loads provided file into the editor.

		:param File: File to load. ( String )
		:return: Method success. ( Boolean )
		"""

		if not os.path.exists(file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(self.__class__.__name__, file))

		LOGGER.debug("> Loading '{0}' file.".format(file))
		reader = io.File(file)
		reader.read() and self.setPlainText("".join(reader.content))
		self.__setFile(file)

		# Signals / Slots.
		self.document().contentsChanged.connect(self.__editor__contentsChanged)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def saveFile(self):
		"""
		This method saves the editor content.

		:return: Method success. ( Boolean )
		"""

		if not self.__isUntitled:
			return self.writeFile(self.__file)
		else:
			return self.saveFileAs()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.uiBasicExceptionHandler, False, Exception)
	def saveFileAs(self):
		"""
		This method saves the editor content into user defined file.

		:return: Method success. ( Boolean )
		
		:note: This method may require user interaction.
		"""

		file = umbra.ui.common.storeLastBrowsedPath(QFileDialog.getSaveFileName(self, "Save As:", self.__file))
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
		This method writes the editor content into provided file.

		:param file: File to write. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Writing '{0}' file.".format(file))
		writer = io.File(file)
		writer.content = [self.toPlainText()]
		return writer.write()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def closeFile(self):
		"""
		This method close the editor file.

		:return: Method success. ( Boolean )
		"""

		if not self.document().isModified():
			LOGGER.debug("> Closing '{0}' file.".format(self.__file))
			return True

		choice = messageBox.messageBox("Warning", "Warning", "'{0}' document has been modified!\nWould you like to save your changes?".format(self.getFileShortName()), buttons=QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
		if choice == QMessageBox.Save:
			if self.saveFile():
				LOGGER.debug("> Closing '{0}' file.".format(self.__file))
				return True
		elif choice == QMessageBox.Discard:
			LOGGER.debug("> Discarding '{0}' file.".format(self.__file))
			return True

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

		self.ui.Script_Editor_Output_plainTextEdit.highlighter = LoggingHighlighter(self.ui.Script_Editor_Output_plainTextEdit.document())

		# Signals / Slots.
		self.__container.timer.timeout.connect(self.__Script_Editor_Output_plainTextEdit_refreshUi)
		self.ui.Script_Editor_tabWidget.tabCloseRequested.connect(self.__Script_Editor_tabWidget__tabCloseRequested)
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

		self.__fileMenu = QMenu("&File")
		self.__fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|&New", shortcut=QKeySequence.New, slot=self.__newFileAction__triggered))
		self.__fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|&Load ...", shortcut=QKeySequence.Open, slot=self.__loadFileAction__triggered))
#		self.__fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|Source ...", slot=self.__sourceFileAction__triggered))
		self.__fileMenu.addSeparator()
		self.__fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|&Save", shortcut=QKeySequence.Save, slot=self.__saveFileAction__triggered))
		self.__fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|Save As ...", shortcut=QKeySequence.SaveAs, slot=self.__saveFileAsAction__triggered))
		self.__fileMenu.addSeparator()
		self.__fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|Close ...", shortcut=QKeySequence.Close, slot=self.__closeFileAction__triggered))
		self.__fileMenu.addAction(self.__container.actionsManager.registerAction("Actions|Umbra|Components|factory.scriptEditor|&File|Close All ...", shortcut=Qt.SHIFT + Qt.ControlModifier + Qt.Key_W, slot=self.__closeAllFilesAction__triggered))
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
		self.__Script_Editor_Output_plainTextEdit_setDefaultViewState()

	# @core.executionTrace
	def __Script_Editor_Output_plainTextEdit_setDefaultViewState(self):
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
			self.__Script_Editor_Output_plainTextEdit_setDefaultViewState()
			self.__memoryHandlerStackDepth = memoryHandlerStackDepth

	@core.executionTrace
	def __Script_Editor_tabWidget__tabCloseRequested(self, tabIndex):
		"""
		This method is triggered by the **Script_Editor_tabWidget** widget when a tab is requested to be closed.

		:param tabIndex: Tab index. ( Integer )
		"""

		return self.closeFile()

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
	def __editor__contentChanged(self):
		"""
		This method is triggered when a editor content changes.
		"""

		self.__setEditorTabName(self.ui.Script_Editor_tabWidget.currentIndex())

	@core.executionTrace
	def __editor__fileChanged(self):
		"""
		This method is triggered when a editor file changes.
		"""

		self.__setEditorTabName(self.ui.Script_Editor_tabWidget.currentIndex())

	@core.executionTrace
	def __setEditorTabName(self, tabIndex):
		"""
		This method sets the editor tab name.

		:param tabIndex: Index of the tab containing the editor. ( Integer )
		"""

		self.ui.Script_Editor_tabWidget.setTabText(tabIndex, self.ui.Script_Editor_tabWidget.widget(tabIndex).windowTitle())

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
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addEditorTab(self, editor):
		"""
		This method adds a new tab to the **Script_Editor_tabWidget** widget and sets provided editor as child widget.

		:param editor: Editor. ( Editor )
		:return: New tab index. ( Integer )
		"""

		tabIndex = self.ui.Script_Editor_tabWidget.addTab(editor, editor.getFileShortName())
		self.ui.Script_Editor_tabWidget.setCurrentIndex(tabIndex)

		# Signals / Slots.
		editor.contentChanged.connect(self.__editor__contentChanged)
		editor.fileChanged.connect(self.__editor__fileChanged)
		return tabIndex

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeEditorTab(self, tabIndex):
		"""
		This method removes the **Script_Editor_tabWidget** widget tab with provided index.

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
	def newFile(self):
		"""
		This method creates a new file into a new :class:`Editor` instance with its associated tab.

		:return: Method success. ( Boolean )
		"""

		editor = Editor()
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
		editor = Editor()
		if editor.loadFile(file):
			self.addEditorTab(editor)
			return True

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
			return editor.saveFile()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def saveFileAs(self):
		"""
		This method saves current :class:`Editor` instance file as user defined file.

		:return: Method success. ( Boolean )
		"""

		if not self.ui.Script_Editor_tabWidget.count():
			return

		editor = self.ui.Script_Editor_tabWidget.currentWidget()
		LOGGER.info("{0} | Saving '{1}' file!".format(self.__class__.__name__, editor.file))
		return editor.saveFileAs()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def closeFile(self):
		"""
 		This method closes current :class:`Editor` instance file and removes the associated **Script_Editor_tabWidget** widget tab.

		:return: Method success. ( Boolean )
		"""

		if not self.ui.Script_Editor_tabWidget.count():
			return

		editor = self.ui.Script_Editor_tabWidget.currentWidget()
		LOGGER.info("{0} | Closing '{1}' file!".format(self.__class__.__name__, editor.file))
		if not editor.closeFile():
			return

		if self.removeEditorTab(self.ui.Script_Editor_tabWidget.currentIndex()):
			not self.ui.Script_Editor_tabWidget.count() and self.newFile()
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def closeAllFiles(self, leaveLastEditor=True):
		"""
 		This method closes every :class:`Editor` instances and removes their associated **Script_Editor_tabWidget** widget tabs.

		:return: Method success. ( Boolean )
		"""

		for i in range(self.ui.Script_Editor_tabWidget.count(), 0, -1):
			editor = self.ui.Script_Editor_tabWidget.widget(i - 1)
			LOGGER.info("{0} | Closing '{1}' file!".format(self.__class__.__name__, editor.file))
			if not editor.closeFile():
				return

			if self.removeEditorTab(self.ui.Script_Editor_tabWidget.currentIndex()):
				if not self.ui.Script_Editor_tabWidget.count() and leaveLastEditor:
					self.newFile()
		return True

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
