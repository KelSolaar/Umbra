#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**editor.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Editor class and others helper objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import inspect
import logging
import os
import platform
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QTextOption

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.io as io
import foundations.strings
import umbra.ui.common
import umbra.ui.completers
import umbra.ui.highlighters
import umbra.ui.inputAccelerators
import umbra.ui.widgets.messageBox as messageBox
from umbra.components.factory.scriptEditor.exceptions import LanguageGrammarError
from umbra.globals.constants import Constants
from umbra.globals.uiConstants import UiConstants
from umbra.ui.widgets.codeEditor_QPlainTextEdit import CodeEditor_QPlainTextEdit

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
		"PYTHON_GRAMMAR_FILE",
		"LANGUAGES_CAPABILITIES",
		"Language",
		"getObjectFromLanguageCapability",
		"getLanguageDescription",
		"getPythonLanguage",
		"PYTHON_LANGUAGE",
		"Editor"]

LOGGER = logging.getLogger(Constants.logger)

PYTHON_GRAMMAR_FILE = umbra.ui.common.getResourcePath(UiConstants.pythonGrammarFile)

LANGUAGES_ACCELERATORS = {"DefaultHighlighter" : umbra.ui.highlighters.DefaultHighlighter,
						"DefaultCompleter" : umbra.ui.completers.DefaultCompleter,
						"indentationPreEventInputAccelerators" :
						umbra.ui.inputAccelerators.indentationPreEventInputAccelerators,
						"completionPreEventInputAccelerators" :
						umbra.ui.inputAccelerators.completionPreEventInputAccelerators,
						"completionPostEventInputAccelerators" :
						umbra.ui.inputAccelerators.completionPostEventInputAccelerators,
						"symbolsExpandingPreEventInputAccelerators" :
						umbra.ui.inputAccelerators.symbolsExpandingPreEventInputAccelerators,
						"pythonPostEventInputAccelerators" :
						umbra.ui.inputAccelerators.pythonPostEventInputAccelerators,
						"DefaultTheme" : umbra.ui.highlighters.DEFAULT_THEME,
						"LoggingTheme" : umbra.ui.highlighters.LOGGING_THEME}

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Language(core.Structure):
	"""
	This class represents a storage object for the :class:`Editor` class language description. 
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: name, extensions. ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		core.Structure.__init__(self, **kwargs)

@core.executionTrace
def getObjectFromLanguageAccelerators(accelerator):
	"""
	This definition returns the object associated to given accelerator.

	:param accelerator: Accelerator. ( String )
	:return: Object. ( Object )
	"""

	return LANGUAGES_ACCELERATORS.get(accelerator)

@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, LanguageGrammarError)
def getLanguageDescription(file):
	"""
	This definition gets the language description from given language grammar file.

	:param file: Language grammar. ( String )
	:return: Language description. ( Language )
	"""

	sectionParser = umbra.ui.common.getSectionsFileParser(file)

	name = sectionParser.getValue("Name", "Language")
	if not name:
		raise LanguageGrammarError("{0} | '{1}' attribute not found in '{2}' file!".format(
			inspect.getmodulename(__file__), "Language|Name", file))

	extensions = sectionParser.getValue("Extensions", "Language")
	if not extensions:
		raise LanguageGrammarError("{0} | '{1}' attribute not found in '{2}' file!".format(
			inspect.getmodulename(__file__), "Language|Extensions", file))

	highlighter = getObjectFromLanguageAccelerators(sectionParser.getValue("Highlighter", "Accelerators"))
	completer = getObjectFromLanguageAccelerators(sectionParser.getValue("Completer", "Accelerators"))
	preInputAccelerators = sectionParser.getValue("PreInputAccelerators", "Accelerators")
	preInputAccelerators = preInputAccelerators and [getObjectFromLanguageAccelerators(accelerator)
													for accelerator in preInputAccelerators.split("|")] or ()
	postInputAccelerators = sectionParser.getValue("PostInputAccelerators", "Accelerators")
	postInputAccelerators = postInputAccelerators and [getObjectFromLanguageAccelerators(accelerator)
													for accelerator in postInputAccelerators.split("|")] or ()

	indentMarker = sectionParser.sectionExists("Syntax") and sectionParser.getValue("IndentMarker", "Syntax") or "\t"
	commentMarker = sectionParser.sectionExists("Syntax") and sectionParser.getValue("CommentMarker", "Syntax") or str()
	theme = getObjectFromLanguageAccelerators(sectionParser.getValue("Theme", "Accelerators")) or \
			umbra.ui.highlighters.DEFAULT_THEME

	return Language(name=name,
				extensions=extensions,
				highlighter=highlighter,
				completer=completer,
				preInputAccelerators=preInputAccelerators,
				postInputAccelerators=postInputAccelerators,
				indentMarker=indentMarker,
				commentMarker=commentMarker,
				parser=sectionParser,
				theme=theme)

@core.executionTrace
def getPythonLanguage():
	"""
	This definition returns the Python language description.

	:return: Python language description. ( Language )
	"""

	return getLanguageDescription(PYTHON_GRAMMAR_FILE)

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
PYTHON_LANGUAGE = getPythonLanguage()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Editor(CodeEditor_QPlainTextEdit):
	"""
	This class defines the default editor used by the: **ScriptEditor** Component. 
	"""

	__instanceId = 1

	# Custom signals definitions.
	languageChanged = pyqtSignal()
	contentChanged = pyqtSignal()
	fileChanged = pyqtSignal()

	@core.executionTrace
	def __init__(self, parent=None, file=None, language=PYTHON_LANGUAGE, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param file: File path. ( String )
		:param language: Editor language. ( Language )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		CodeEditor_QPlainTextEdit.__init__(self, parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__file = None
		self.file = file
		self.__language = language

		self.__defaultFontsSettings = {"Windows" : ("Consolas", 10),
										"Darwin" : ("Monaco", 12),
										"Linux" : ("Nimbus Mono L", 10)}
		self.__tabWidth = None

		self.__isUntitled = True
		self.__defaultFileName = "Untitled"
		self.__defaultFileExtension = "py"

		Editor.__initializeUi(self)

		file and self.loadFile(file)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "file"))

	@property
	def language(self):
		"""
		This method is the property for **self.__language** attribute.

		:return: self.__language. ( Language )
		"""

		return self.__language

	@language.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def language(self, value):
		"""
		This method is the setter method for **self.__language** attribute.

		:param value: Attribute value. ( Language )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "language"))

	@language.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def language(self):
		"""
		This method is the deleter method for **self.__language** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "language"))

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
	def tabWidth(self):
		"""
		This method is the property for **self.__tabWidth** attribute.

		:return: self.__tabWidth. ( Integer )
		"""

		return self.__tabWidth

	@tabWidth.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tabWidth(self, value):
		"""
		This method is the setter method for **self.__tabWidth** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tabWidth"))

	@tabWidth.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def tabWidth(self):
		"""
		This method is the deleter method for **self.__tabWidth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tabWidth"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "isUntitled"))

	@isUntitled.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def isUntitled(self):
		"""
		This method is the deleter method for **self.__isUntitled** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "isUntitled"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultFileName"))

	@defaultFileName.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultFileName(self):
		"""
		This method is the deleter method for **self.__defaultFileName** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultFileName"))

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultFileExtension"))

	@defaultFileExtension.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultFileExtension(self):
		"""
		This method is the deleter method for **self.__defaultFileExtension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultFileExtension"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		self.__setLanguageDescription()

		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setWordWrapMode(QTextOption.NoWrap)

		self.setAcceptDrops(True)

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			fontFamily, fontSize = self.__defaultFontsSettings["Windows"]
		elif platform.system() == "Darwin":
			fontFamily, fontSize = self.__defaultFontsSettings["Darwin"]
		elif platform.system() == "Linux":
			fontFamily, fontSize = self.__defaultFontsSettings["Linux"]
		font = QFont(fontFamily)
		font.setPointSize(fontSize)
		self.setFont(font)

		self.__tabWidth = self.fontMetrics().width(" " * self.indentWidth)
		self.setTabStopWidth(self.__tabWidth)

	@core.executionTrace
	def __setFile(self, file):
		"""
		This method sets the editor file.

		:param File: File to set. ( String )
		"""

		self.__file = file
		self.__isUntitled = False
		self.setModified(False)
		self.setWindowTitle("{0}".format(self.getFileShortName()))

		self.fileChanged.emit()

	@core.executionTrace
	def __setWindowTitle(self):
		"""
		This method sets the editor window title.
		"""

		titleTemplate = self.isModified() and "{0} *" or "{0}"
		self.setWindowTitle(titleTemplate.format(self.getFileShortName()))
		self.contentChanged.emit()

	@core.executionTrace
	def __editor__contentsChanged(self):
		"""
		This method is triggered when the editor content changes.
		"""

		self.__setWindowTitle()

	@core.executionTrace
	def __setLanguageDescription(self):
		"""
		This method sets the editor language accelerators.
		"""

		if not self.__language:
			return

		if self.__language.highlighter:
			self.setHighlighter(self.__language.highlighter(self.document(),
															self.__language.parser,
															self.__language.theme))
		else:
			self.removeHighlighter()

		if self.__language.completer:
			self.setCompleter(self.__language.completer(self.parent(), self.__language.parser))
		else:
			self.removeCompleter()

		self.indentMarker = self.__language.indentMarker
		self.commentMarker = self.__language.commentMarker
		self.preInputAccelerators = self.__language.preInputAccelerators
		self.postInputAccelerators = self.__language.postInputAccelerators

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def setLanguage(self, language, emitSignal=True):
		"""
		This method sets the editor language.

		:param language: Language to set. ( Language )
		:param emitSignal: Emit signal. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not isinstance(language, Language):
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' type is not 'Language'!".format(
			self.__class__.__name__, language))

		self.__language = language
		self.__setLanguageDescription()
		emitSignal and self.languageChanged.emit()
		return True

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
		This method reads and loads given file into the editor.

		:param File: File to load. ( String )
		:return: Method success. ( Boolean )
		"""

		if not os.path.exists(file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(self.__class__.__name__,
																									file))

		LOGGER.debug("> Loading '{0}' file.".format(file))
		reader = io.File(file)
		reader.read() and self.setPlainText("".join(reader.content))
		self.__setFile(file)

		# Signals / Slots.
		self.document().contentsChanged.connect(self.__editor__contentsChanged)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
	def reloadFile(self):
		"""
		This method reloads the current file into the editor.

		:return: Method success. ( Boolean )
		"""

		if not os.path.exists(self.__file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
			self.__class__.__name__, self.__file))

		LOGGER.debug("> Reloading '{0}' file.".format(self.__file))
		reader = io.File(self.__file)
		if reader.read():
			self.setContent(reader.content)
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
		This method writes the editor content into given file.

		:param file: File to write. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Writing '{0}' file.".format(file))
		writer = io.File(file)
		writer.content = [self.toPlainText()]
		if writer.write():
			self.setModified(False)
			self.__setWindowTitle()
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def closeFile(self):
		"""
		This method closes the editor file.

		:return: Method success. ( Boolean )
		"""

		if not self.isModified():
			LOGGER.debug("> Closing '{0}' file.".format(self.__file))
			return True

		choice = messageBox.messageBox("Warning", "Warning",
		"'{0}' document has been modified!\nWould you like to save your changes?".format(self.getFileShortName()),
		buttons=QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
		if choice == QMessageBox.Save:
			if self.saveFile():
				LOGGER.debug("> Closing '{0}' file.".format(self.__file))
				return True
		elif choice == QMessageBox.Discard:
			LOGGER.debug("> Discarding '{0}' file.".format(self.__file))
			return True
