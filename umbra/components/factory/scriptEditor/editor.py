#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**editor.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Editor` class and others editing helper objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import inspect
import logging
import os
import platform
from PyQt4.QtCore import QRegExp
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPlainTextDocumentLayout
from PyQt4.QtGui import QTextOption

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
import foundations.io as io
import foundations.parsers
import foundations.strings as strings
import umbra.ui.common
import umbra.ui.completers
import umbra.ui.highlighters
import umbra.ui.inputAccelerators
import umbra.ui.themes
import umbra.ui.visualAccelerators
import umbra.ui.widgets.messageBox as messageBox
from umbra.components.factory.scriptEditor.exceptions import LanguageGrammarError
from umbra.globals.constants import Constants
from umbra.globals.uiConstants import UiConstants
from umbra.ui.widgets.codeEditor_QPlainTextEdit import CodeEditor_QPlainTextEdit

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
		"PYTHON_GRAMMAR_FILE",
		"LOGGING_GRAMMAR_FILE",
		"TEXT_GRAMMAR_FILE",
		"LANGUAGES_ACCELERATORS",
		"DEFAULT_INDENT_MARKER",
		"Language",
		"getObjectFromLanguageAccelerators",
		"getLanguageDescription",
		"getPythonLanguage",
		"getLoggingLanguage",
		"PYTHON_LANGUAGE",
		"LOGGING_LANGUAGE",
		"TEXT_LANGUAGE",
		"Editor"]

LOGGER = logging.getLogger(Constants.logger)

PYTHON_GRAMMAR_FILE = umbra.ui.common.getResourcePath(UiConstants.pythonGrammarFile)
LOGGING_GRAMMAR_FILE = umbra.ui.common.getResourcePath(UiConstants.loggingGrammarFile)
TEXT_GRAMMAR_FILE = umbra.ui.common.getResourcePath(UiConstants.textGrammarFile)

LANGUAGES_ACCELERATORS = {"DefaultHighlighter" : umbra.ui.highlighters.DefaultHighlighter,
						"DefaultCompleter" : umbra.ui.completers.DefaultCompleter,
						"indentationPreEventInputAccelerators" :
						umbra.ui.inputAccelerators.indentationPreEventInputAccelerators,
						"indentationPostEventInputAccelerators" :
						umbra.ui.inputAccelerators.indentationPostEventInputAccelerators,
						"completionPreEventInputAccelerators" :
						umbra.ui.inputAccelerators.completionPreEventInputAccelerators,
						"completionPostEventInputAccelerators" :
						umbra.ui.inputAccelerators.completionPostEventInputAccelerators,
						"symbolsExpandingPreEventInputAccelerators" :
						umbra.ui.inputAccelerators.symbolsExpandingPreEventInputAccelerators,
						"highlightCurrentLine" :
						umbra.ui.visualAccelerators.highlightCurrentLine,
						"highlightOccurences" :
						umbra.ui.visualAccelerators.highlightOccurences,
						"highlightMatchingSymbolsPairs" :
						umbra.ui.visualAccelerators.highlightMatchingSymbolsPairs,
						"DefaultTheme" : umbra.ui.themes.DEFAULT_THEME,
						"LoggingTheme" : umbra.ui.themes.LOGGING_THEME}

DEFAULT_INDENT_MARKER = "\t"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Language(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for the :class:`Editor` class language description. 
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: name, file, parser,	extensions, highlighter, completer,	preInputAccelerators,
			postInputAccelerators, visualAccelerators, indentMarker, commentMarker, commentBlockMarkerStart, commentBlockMarkerEnd,
			symbolsPairs, indentationSymbols, rules, tokens, theme. ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

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
def getLanguageDescription(grammarfile):
	"""
	This definition gets the language description from given language grammar file.

	:param grammarfile: Language grammar. ( String )
	:return: Language description. ( Language )
	"""

	LOGGER.debug("> Processing '{0}' grammar file.".format(grammarfile))

	sectionsParser = foundations.parsers.SectionsFileParser(grammarfile)
	sectionsParser.read() and sectionsParser.parse(stripQuotationMarkers=False)

	name = sectionsParser.getValue("Name", "Language")
	if not name:
		raise LanguageGrammarError("{0} | '{1}' attribute not found in '{2}' file!".format(
			inspect.getmodulename(__file__), "Language|Name", grammarfile))

	extensions = sectionsParser.getValue("Extensions", "Language")
	if not extensions:
		raise LanguageGrammarError("{0} | '{1}' attribute not found in '{2}' file!".format(
			inspect.getmodulename(__file__), "Language|Extensions", grammarfile))

	highlighter = getObjectFromLanguageAccelerators(sectionsParser.getValue("Highlighter", "Accelerators"))
	completer = getObjectFromLanguageAccelerators(sectionsParser.getValue("Completer", "Accelerators"))
	preInputAccelerators = sectionsParser.getValue("PreInputAccelerators", "Accelerators")
	preInputAccelerators = preInputAccelerators and [getObjectFromLanguageAccelerators(accelerator)
													for accelerator in preInputAccelerators.split("|")] or ()
	postInputAccelerators = sectionsParser.getValue("PostInputAccelerators", "Accelerators")
	postInputAccelerators = postInputAccelerators and [getObjectFromLanguageAccelerators(accelerator)
													for accelerator in postInputAccelerators.split("|")] or ()

	visualAccelerators = sectionsParser.getValue("VisualAccelerators", "Accelerators")
	visualAccelerators = visualAccelerators and [getObjectFromLanguageAccelerators(accelerator)
													for accelerator in visualAccelerators.split("|")] or ()

	indentMarker = sectionsParser.sectionExists("Syntax") and sectionsParser.getValue("IndentMarker", "Syntax") or \
					DEFAULT_INDENT_MARKER
	commentMarker = sectionsParser.sectionExists("Syntax") and \
					sectionsParser.getValue("CommentMarker", "Syntax") or unicode()
	commentBlockMarkerStart = sectionsParser.sectionExists("Syntax") and \
							sectionsParser.getValue("CommentBlockMarkerStart", "Syntax") or unicode()
	commentBlockMarkerEnd = sectionsParser.sectionExists("Syntax") and \
							sectionsParser.getValue("CommentBlockMarkerEnd", "Syntax") or unicode()
	symbolsPairs = sectionsParser.sectionExists("Syntax") and \
							sectionsParser.getValue("SymbolsPairs", "Syntax") or {}

	if symbolsPairs:
		associatedPairs = foundations.dataStructures.Lookup()
		for pair in symbolsPairs.split("|"):
			associatedPairs[pair[0]] = pair[1]
		symbolsPairs = associatedPairs

	indentationSymbols = sectionsParser.sectionExists("Syntax") and \
						sectionsParser.getValue("IndentationSymbols", "Syntax")
	indentationSymbols = indentationSymbols and indentationSymbols.split("|") or ()

	rules = []
	attributes = sectionsParser.sections.get("Rules")
	if attributes:
		for attribute in sectionsParser.sections["Rules"]:
			pattern = sectionsParser.getValue(attribute, "Rules")
			rules.append(umbra.ui.highlighters.Rule(name=foundations.namespace.removeNamespace(attribute),
								pattern=QRegExp(pattern)))

	tokens = []
	dictionary = sectionsParser.getValue("Dictionary", "Accelerators")
	if dictionary:
		dictionaryFile = os.path.join(os.path.dirname(grammarfile), dictionary)
		if foundations.common.pathExists(dictionaryFile):
			with open(dictionaryFile, "r") as file:
				for line in iter(file):
					line = line.strip()
					line and tokens.append(line)
		else:
			LOGGER.warning("!> {0} | '{1}' language dictionary file doesn't exists and will be skipped!".format(
				inspect.getmodulename(__file__), dictionaryFile))

	theme = getObjectFromLanguageAccelerators(sectionsParser.getValue("Theme", "Accelerators")) or \
			umbra.ui.highlighters.DEFAULT_THEME

	attributes = {"name" : name,
				"file" : grammarfile,
				"parser" : sectionsParser,
				"extensions" : extensions,
				"highlighter" : highlighter,
				"completer" : completer,
				"preInputAccelerators" : preInputAccelerators,
				"postInputAccelerators" : postInputAccelerators,
				"visualAccelerators" : visualAccelerators,
				"indentMarker" : indentMarker,
				"commentMarker" : commentMarker,
				"commentBlockMarkerStart" : commentBlockMarkerStart,
				"commentBlockMarkerEnd" : commentBlockMarkerEnd,
				"symbolsPairs" : symbolsPairs,
				"indentationSymbols" : indentationSymbols,
				"rules" : rules,
				"tokens" : tokens,
				"theme" : theme}

	for attribute, value in sorted(attributes.iteritems()):
		if attribute == "rules":
			LOGGER.debug("> Registered '{0}' syntax rules.".format(len(value)))
		elif attribute == "tokens":
			LOGGER.debug("> Registered '{0}' completion tokens.".format(len(value)))
		else:
			LOGGER.debug("> Attribute: '{0}', Value: '{1}'.".format(attribute, value))

	return Language(**attributes)

@core.executionTrace
def getPythonLanguage():
	"""
	This definition returns the Python language description.

	:return: Python language description. ( Language )
	"""

	return getLanguageDescription(PYTHON_GRAMMAR_FILE)

@core.executionTrace
def getLoggingLanguage():
	"""
	This definition returns the Logging language description.

	:return: Logging language description. ( Language )
	"""

	return getLanguageDescription(LOGGING_GRAMMAR_FILE)

@core.executionTrace
def getTextLanguage():
	"""
	This definition returns the Text language description.

	:return: Text language description. ( Language )
	"""

	return getLanguageDescription(TEXT_GRAMMAR_FILE)

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
PYTHON_LANGUAGE = getPythonLanguage()
LOGGING_LANGUAGE = getLoggingLanguage()
TEXT_LANGUAGE = getTextLanguage()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Editor(CodeEditor_QPlainTextEdit):
	"""
	This class defines the default editor used by
	the :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor` Component Interface class. 
	"""

	__untitledNameId = 1
	"""Editor untitled name id. ( Integer )"""

	# Custom signals definitions.
	languageChanged = pyqtSignal()
	"""
	This signal is emited by the :class:`Editor` class when :obj:`ComponentsManagerUi.language` class property language
	is changed. ( pyqtSignal )
	"""

	titleChanged = pyqtSignal()
	"""
	This signal is emited by the :class:`Editor` class when the current title is changed. ( pyqtSignal )
	"""

	fileLoaded = pyqtSignal()
	"""
	This signal is emited by the :class:`Editor` class when the current file is loaded. ( pyqtSignal )
	"""

	fileSaved = pyqtSignal()
	"""
	This signal is emited by the :class:`Editor` class when the current file is saved. ( pyqtSignal )
	"""

	fileReloaded = pyqtSignal()
	"""
	This signal is emited by the :class:`Editor` class when the current file is reloaded. ( pyqtSignal )
	"""

	fileClosed = pyqtSignal()
	"""
	This signal is emited by the :class:`Editor` class when the current file is closed. ( pyqtSignal )
	"""

	contentsChanged = pyqtSignal()
	"""
	This signal is emited by the :class:`Editor` class when the current editor document content has changed. ( pyqtSignal )
	"""

	modificationChanged = pyqtSignal(bool)
	"""
	This signal is emited by the :class:`Editor` class when the current editor doucment content has been modified. ( pyqtSignal )
	"""

	@core.executionTrace
	def __init__(self, parent=None, file=None, language=PYTHON_LANGUAGE, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param file: File path. ( String )
		:param language: Editor language. ( Language )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		CodeEditor_QPlainTextEdit.__init__(self, parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__file = None
		self.file = file
		self.__language = language

		self.__defaultFontsSettings = {"Windows" : ("Consolas", 10),
										"Darwin" : ("Monaco", 12),
										"Linux" : ("Monospace", 10)}
		self.__tabWidth = None

		self.__title = None
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

		if value is not None:
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
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
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
	def title(self):
		"""
		This method is the property for **self.__title** attribute.

		:return: self.__title. ( String )
		"""

		return self.__title

	@title.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def title(self, value):
		"""
		This method is the setter method for **self.__title** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "title"))

	@title.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def title(self):
		"""
		This method is the deleter method for **self.__title** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "title"))

	@property
	def isUntitled(self):
		"""
		This method is the property for **self.__isUntitled** attribute.

		:return: self.__isUntitled. ( Boolean )
		"""

		return self.__isUntitled

	@isUntitled.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
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

		self.__setLanguageDescription()

	@core.executionTrace
	def __document__contentsChanged(self):
		"""
		This method is triggered when the editor document content changes.
		"""

		self.setTitle()

	@core.executionTrace
	def __document__modificationChanged(self, changed):
		"""
		This method is triggered when the editor document is modified.
		
		:param changed: File modification state. ( Boolean )
		"""

		self.setTitle()

	@core.executionTrace
	def __setLanguageDescription(self):
		"""
		This method sets the editor language accelerators.
		"""

		LOGGER.debug("> Setting editor language description.")

		if not self.__language:
			return

		if self.__language.highlighter:
			self.setHighlighter(self.__language.highlighter(self.document(),
															self.__language.rules,
															self.__language.theme))
			self.highlighter.rehighlight()
		else:
			self.removeHighlighter()

		if self.__language.completer:
			self.setCompleter(self.__language.completer(self.parent(), self.__language.name, self.__language.tokens))
		else:
			self.removeCompleter()

		self.indentMarker = self.__language.indentMarker
		self.commentMarker = self.__language.commentMarker
		self.preInputAccelerators = self.__language.preInputAccelerators
		self.postInputAccelerators = self.__language.postInputAccelerators
		self.visualAccelerators = self.__language.visualAccelerators

		color = "rgb({0}, {1}, {2})"
		background = self.__language.theme.get("default").background()
		foreground = self.__language.theme.get("default").foreground()
		self.setStyleSheet(
		"QPlainTextEdit{{ background-color: {0}; color: {1}; }}".format(color.format(background.color().red(),
																								background.color().green(),
																								background.color().blue()),
																				color.format(foreground.color().red(),
																							foreground.color().green(),
																							foreground.color().blue())))

		self.__tabWidth = self.fontMetrics().width(" " * self.indentWidth)
		self.setTabStopWidth(self.__tabWidth)

	@core.executionTrace
	def __setDocumentSignals(self):
		"""
		This method connects the editor document signals.
		"""

		# Signals / Slots.
		self.document().contentsChanged.connect(self.contentsChanged.emit)
		self.document().contentsChanged.connect(self.__document__contentsChanged)
		self.document().modificationChanged.connect(self.modificationChanged.emit)
		self.document().modificationChanged.connect(self.__document__modificationChanged)

	@core.executionTrace
	def setTitle(self, title=None):
		"""
		This method sets the editor title.

		:param title: Editor title. ( String )
		:return: Method success. ( Boolean )
		"""

		if not title:
			# TODO: https://bugreports.qt-project.org/browse/QTBUG-27084
			# titleTemplate = self.isModified() and "{0} *" or "{0}"
			# title = titleTemplate.format(self.getFileShortName())
			title = self.getFileShortName()

		LOGGER.debug("> Setting editor title to '{0}'.".format(title))
		self.__title = title
		self.setWindowTitle(title)

		self.titleChanged.emit()
		return True

	@core.executionTrace
	def setFile(self, file=None, isModified=False, isUntitled=False):
		"""
		This method sets the editor file.

		:param File: File to set. ( String )
		:param isModified: File modified state. ( Boolean )
		:param isUntitled: File untitled state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Setting '{0}' editor file.".format(file))
		self.__file = file
		self.__isUntitled = isUntitled
		self.setModified(isModified)
		self.setTitle()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setLanguage(self, language):
		"""
		This method sets the editor language.

		:param language: Language to set. ( Language )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Setting editor language to '{0}'.".format(language.name))
		self.__language = language or PYTHON_LANGUAGE
		self.__setLanguageDescription()
		self.languageChanged.emit()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getFileShortName(self):
		"""
		This method returns the current editor file short name.

		:return: File short name. ( String )
		"""

		if not self.__file:
			return str()

		return os.path.basename(self.__file)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getUntitledFileName(self):
		"""
		This method returns an untitled editor file name.

		:return: Untitled file name. ( String )
		"""

		name = "{0} {1}.{2}".format(self.__defaultFileName, Editor._Editor__untitledNameId, self.defaultFileExtension)
		Editor._Editor__untitledNameId += 1
		LOGGER.debug("> Next untitled file name: '{0}'.".format(name))
		return name

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def loadDocument(self, document, file=None, language=None):
		"""
		This method loads given document into the editor.

		:param document: Document to load. ( QTextDocument )
		:param file: File. ( String )
		:param language: Editor language. ( String )
		:return: Method success. ( Boolean )
		"""

		document.setDocumentLayout(QPlainTextDocumentLayout(document))
		self.setDocument(document)
		self.setFile(file)
		self.setLanguage(language)
		self.__setDocumentSignals()

		self.fileLoaded.emit()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def newFile(self):
		"""
		This method creates a new editor file.

		:return: File name. ( String )
		"""

		file = self.getUntitledFileName()
		LOGGER.debug("> Creating '{0}' file.".format(file))
		self.setFile(file, isModified=False, isUntitled=True)
		self.__setDocumentSignals()
		return file

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
	def loadFile(self, file):
		"""
		This method reads and loads given file into the editor.

		:param File: File to load. ( String )
		:return: Method success. ( Boolean )
		"""

		if not foundations.common.pathExists(file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(self.__class__.__name__,
																									file))

		LOGGER.debug("> Loading '{0}' file.".format(file))
		reader = io.File(file)
		self.setPlainText(reader.readAll())
		self.setFile(file)
		self.__setDocumentSignals()
		self.fileLoaded.emit()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.FileExistsError)
	def reloadFile(self, isModified=True):
		"""
		This method reloads the current editor file.

		:param isModified: File modified state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		if not foundations.common.pathExists(self.__file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
			self.__class__.__name__, self.__file))

		LOGGER.debug("> Reloading '{0}' file.".format(self.__file))
		reader = io.File(self.__file)
		if reader.read():
			self.setContent(reader.content)
			self.setFile(self.__file, isModified=isModified)

			self.fileReloaded.emit()
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def saveFile(self):
		"""
		This method saves the editor file content.

		:return: Method success. ( Boolean )
		"""

		if not self.__isUntitled and foundations.common.pathExists(self.__file):
			return self.writeFile(self.__file)
		else:
			return self.saveFileAs()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(umbra.ui.common.notifyExceptionHandler, False, Exception)
	def saveFileAs(self, file=None):
		"""
		This method saves the editor file content either using given file or user chosen file.

		:return: Method success. ( Boolean )
		
		:note: This method may require user interaction.
		"""

		file = file or umbra.ui.common.storeLastBrowsedPath(QFileDialog.getSaveFileName(self, "Save As:", self.__file))
		if not file:
			return False

		return self.writeFile(strings.encode(file))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def writeFile(self, file):
		"""
		This method writes the editor file content into given file.

		:param file: File to write. ( String )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Writing '{0}' file.".format(file))
		writer = io.File(file)
		writer.content = [self.toPlainText()]
		if writer.write():
			self.setFile(file)

			self.fileSaved.emit()
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

			self.fileClosed.emit()
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

			self.fileClosed.emit()
			return True
