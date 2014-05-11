#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**languages.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines languages manipulation related objects.

**Others:**

"""

from __future__ import unicode_literals

import os
from PyQt4.QtCore import QRegExp

import foundations.data_structures
import foundations.parsers
import foundations.verbose
import umbra.ui.completers
import umbra.ui.highlighters
import umbra.ui.input_accelerators
import umbra.ui.themes
import umbra.ui.visual_accelerators
from umbra.exceptions import LanguageGrammarError
from umbra.globals.ui_constants import UiConstants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
           "get_object_from_language_accelerators",
           "get_language_description",
           "get_python_language",
           "get_logging_language",
           "PYTHON_LANGUAGE",
           "LOGGING_LANGUAGE",
           "TEXT_LANGUAGE", ]

LOGGER = foundations.verbose.install_logger()

PYTHON_GRAMMAR_FILE = umbra.ui.common.get_resource_path(UiConstants.python_grammar_file)
LOGGING_GRAMMAR_FILE = umbra.ui.common.get_resource_path(UiConstants.logging_grammar_file)
TEXT_GRAMMAR_FILE = umbra.ui.common.get_resource_path(UiConstants.text_grammar_file)

LANGUAGES_ACCELERATORS = {"DefaultHighlighter": umbra.ui.highlighters.DefaultHighlighter,
                          "DefaultCompleter": umbra.ui.completers.DefaultCompleter,
                          "indentation_pre_event_input_accelerators":
                              umbra.ui.input_accelerators.indentation_pre_event_input_accelerators,
                          "indentation_post_event_input_accelerators":
                              umbra.ui.input_accelerators.indentation_post_event_input_accelerators,
                          "completion_pre_event_input_accelerators":
                              umbra.ui.input_accelerators.completion_pre_event_input_accelerators,
                          "completion_post_event_input_accelerators":
                              umbra.ui.input_accelerators.completion_post_event_input_accelerators,
                          "symbols_expanding_pre_event_input_accelerators":
                              umbra.ui.input_accelerators.symbols_expanding_pre_event_input_accelerators,
                          "highlight_current_line":
                              umbra.ui.visual_accelerators.highlight_current_line,
                          "highlight_occurences":
                              umbra.ui.visual_accelerators.highlight_occurences,
                          "highlight_matching_symbols_pairs":
                              umbra.ui.visual_accelerators.highlight_matching_symbols_pairs,
                          "DefaultTheme": umbra.ui.themes.DEFAULT_THEME,
                          "LoggingTheme": umbra.ui.themes.LOGGING_THEME}

DEFAULT_INDENT_MARKER = "\t"


class Language(foundations.data_structures.Structure):
    """
    Defines a storage object for the :class:`Editor` class language description.
    """

    def __init__(self, **kwargs):
        """
        Initializes the class.

        :param \*\*kwargs: name, file, parser,	extensions, highlighter, completer,	pre_input_accelerators,
            post_input_accelerators, visual_accelerators, indent_marker, comment_marker, comment_block_marker_start,
            comment_block_marker_end, symbols_pairs, indentation_symbols, rules, tokens, theme.
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        foundations.data_structures.Structure.__init__(self, **kwargs)


def get_object_from_language_accelerators(accelerator):
    """
    Returns the object associated to given accelerator.

    :param accelerator: Accelerator.
    :type accelerator: unicode
    :return: Object.
    :rtype: object
    """

    return LANGUAGES_ACCELERATORS.get(accelerator)


@foundations.exceptions.handle_exceptions(LanguageGrammarError)
def get_language_description(grammarfile):
    """
    Gets the language description from given language grammar file.

    :param grammarfile: Language grammar.
    :type grammarfile: unicode
    :return: Language description.
    :rtype: Language
    """

    LOGGER.debug("> Processing '{0}' grammar file.".format(grammarfile))

    sections_file_parser = foundations.parsers.SectionsFileParser(grammarfile)
    sections_file_parser.parse(strip_quotation_markers=False)

    name = sections_file_parser.get_value("Name", "Language")
    if not name:
        raise LanguageGrammarError("{0} | '{1}' attribute not found in '{2}' file!".format(__name__,
                                                                                           "Language|Name",
                                                                                           grammarfile))

    extensions = sections_file_parser.get_value("Extensions", "Language")
    if not extensions:
        raise LanguageGrammarError("{0} | '{1}' attribute not found in '{2}' file!".format(__name__,
                                                                                           "Language|Extensions",
                                                                                           grammarfile))

    highlighter = get_object_from_language_accelerators(sections_file_parser.get_value("Highlighter", "Accelerators"))
    completer = get_object_from_language_accelerators(sections_file_parser.get_value("Completer", "Accelerators"))
    pre_input_accelerators = sections_file_parser.get_value("PreInputAccelerators", "Accelerators")
    pre_input_accelerators = pre_input_accelerators and [get_object_from_language_accelerators(accelerator)
                                                         for accelerator in pre_input_accelerators.split("|")] or ()
    post_input_accelerators = sections_file_parser.get_value("PostInputAccelerators", "Accelerators")
    post_input_accelerators = post_input_accelerators and [get_object_from_language_accelerators(accelerator)
                                                           for accelerator in post_input_accelerators.split("|")] or ()

    visual_accelerators = sections_file_parser.get_value("VisualAccelerators", "Accelerators")
    visual_accelerators = visual_accelerators and [get_object_from_language_accelerators(accelerator)
                                                   for accelerator in visual_accelerators.split("|")] or ()

    indent_marker = sections_file_parser.section_exists("Syntax") and sections_file_parser.get_value("IndentMarker",
                                                                                                     "Syntax") or \
                    DEFAULT_INDENT_MARKER
    comment_marker = sections_file_parser.section_exists("Syntax") and \
                     sections_file_parser.get_value("CommentMarker", "Syntax") or ""
    comment_block_marker_start = sections_file_parser.section_exists("Syntax") and \
                                 sections_file_parser.get_value("CommentBlockMarkerStart", "Syntax") or ""
    comment_block_marker_end = sections_file_parser.section_exists("Syntax") and \
                               sections_file_parser.get_value("CommentBlockMarkerEnd", "Syntax") or ""
    symbols_pairs = sections_file_parser.section_exists("Syntax") and \
                    sections_file_parser.get_value("SymbolsPairs", "Syntax") or {}

    if symbols_pairs:
        associated_pairs = foundations.data_structures.Lookup()
        for pair in symbols_pairs.split("|"):
            associated_pairs[pair[0]] = pair[1]
        symbols_pairs = associated_pairs

    indentation_symbols = sections_file_parser.section_exists("Syntax") and \
                          sections_file_parser.get_value("IndentationSymbols", "Syntax")
    indentation_symbols = indentation_symbols and indentation_symbols.split("|") or ()

    rules = []
    attributes = sections_file_parser.sections.get("Rules")
    if attributes:
        for attribute in sections_file_parser.sections["Rules"]:
            pattern = sections_file_parser.get_value(attribute, "Rules")
            rules.append(umbra.ui.highlighters.Rule(name=foundations.namespace.remove_namespace(attribute),
                                                    pattern=QRegExp(pattern)))

    tokens = []
    dictionary = sections_file_parser.get_value("Dictionary", "Accelerators")
    if dictionary:
        dictionary_file = os.path.join(os.path.dirname(grammarfile), dictionary)
        if foundations.common.path_exists(dictionary_file):
            with open(dictionary_file, "r") as file:
                for line in iter(file):
                    line = line.strip()
                    line and tokens.append(line)
        else:
            LOGGER.warning(
                "!> {0} | '{1}' language dictionary file doesn't exists and will be skipped!".format(__name__,
                                                                                                     dictionary_file))

    theme = get_object_from_language_accelerators(sections_file_parser.get_value("Theme", "Accelerators")) or \
            umbra.ui.highlighters.DEFAULT_THEME

    attributes = {"name": name,
                  "file": grammarfile,
                  "parser": sections_file_parser,
                  "extensions": extensions,
                  "highlighter": highlighter,
                  "completer": completer,
                  "pre_input_accelerators": pre_input_accelerators,
                  "post_input_accelerators": post_input_accelerators,
                  "visual_accelerators": visual_accelerators,
                  "indent_marker": indent_marker,
                  "comment_marker": comment_marker,
                  "comment_block_marker_start": comment_block_marker_start,
                  "comment_block_marker_end": comment_block_marker_end,
                  "symbols_pairs": symbols_pairs,
                  "indentation_symbols": indentation_symbols,
                  "rules": rules,
                  "tokens": tokens,
                  "theme": theme}

    for attribute, value in sorted(attributes.iteritems()):
        if attribute == "rules":
            LOGGER.debug("> Registered '{0}' syntax rules.".format(len(value)))
        elif attribute == "tokens":
            LOGGER.debug("> Registered '{0}' completion tokens.".format(len(value)))
        else:
            LOGGER.debug("> Attribute: '{0}', Value: '{1}'.".format(attribute, value))

    return Language(**attributes)


def get_python_language():
    """
    Returns the Python language description.

    :return: Python language description.
    :rtype: Language
    """

    return get_language_description(PYTHON_GRAMMAR_FILE)


def get_logging_language():
    """
    Returns the Logging language description.

    :return: Logging language description.
    :rtype: Language
    """

    return get_language_description(LOGGING_GRAMMAR_FILE)


def get_text_language():
    """
    Returns the Text language description.

    :return: Text language description.
    :rtype: Language
    """

    return get_language_description(TEXT_GRAMMAR_FILE)


PYTHON_LANGUAGE = get_python_language()
LOGGING_LANGUAGE = get_logging_language()
TEXT_LANGUAGE = get_text_language()
