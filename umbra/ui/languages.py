#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**languages.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines languages manipulation related objects.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
from PyQt4.QtCore import QRegExp

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.dataStructures
import foundations.parsers
import foundations.verbose
import umbra.ui.completers
import umbra.ui.highlighters
import umbra.ui.inputAccelerators
import umbra.ui.themes
import umbra.ui.visualAccelerators
from umbra.exceptions import LanguageGrammarError
from umbra.globals.uiConstants import UiConstants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
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
		"TEXT_LANGUAGE", ]

LOGGER = foundations.verbose.installLogger()

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

	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: name, file, parser,	extensions, highlighter, completer,	preInputAccelerators,
			postInputAccelerators, visualAccelerators, indentMarker, commentMarker, commentBlockMarkerStart, commentBlockMarkerEnd,
			symbolsPairs, indentationSymbols, rules, tokens, theme. ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

def getObjectFromLanguageAccelerators(accelerator):
	"""
	This definition returns the object associated to given accelerator.

	:param accelerator: Accelerator. ( String )
	:return: Object. ( Object )
	"""

	return LANGUAGES_ACCELERATORS.get(accelerator)

@foundations.exceptions.handleExceptions(LanguageGrammarError)
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
		raise LanguageGrammarError("{0} | '{1}' attribute not found in '{2}' file!".format(__name__,
																						"Language|Name",
																						grammarfile))

	extensions = sectionsParser.getValue("Extensions", "Language")
	if not extensions:
		raise LanguageGrammarError("{0} | '{1}' attribute not found in '{2}' file!".format(__name__,
																						"Language|Extensions",
																						grammarfile))

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
			LOGGER.warning(
			"!> {0} | '{1}' language dictionary file doesn't exists and will be skipped!".format(__name__,
																								dictionaryFile))

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

def getPythonLanguage():
	"""
	This definition returns the Python language description.

	:return: Python language description. ( Language )
	"""

	return getLanguageDescription(PYTHON_GRAMMAR_FILE)

def getLoggingLanguage():
	"""
	This definition returns the Logging language description.

	:return: Logging language description. ( Language )
	"""

	return getLanguageDescription(LOGGING_GRAMMAR_FILE)

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

