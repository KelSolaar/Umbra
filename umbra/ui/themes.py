#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**highlighters.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application themes classes.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QTextCharFormat

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
from umbra.globals.constants import Constants

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
			"getFormat",
			"DEFAULT_FORMAT",
			"DEFAULT_THEME",
			"LOGGING_THEME"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
@core.executionTrace
@foundations.exceptions.exceptionsHandler(None, False, Exception)
def getFormat(**kwargs):
	"""
	This definition returns a `QTextCharFormat <http://doc.qt.nokia.com/qtextcharformat.html>`_ format.
	
	:param \*\*kwargs: Format settings. ( Key / Value pairs )
	:return: Format. ( QTextCharFormat )
	"""

	settings = foundations.dataStructures.Structure(**{"format" : QTextCharFormat(),
								"backgroundColor" : None,
								"color" : None,
								"fontWeight" : None,
								"fontPointSize" : None,
								"italic" : False})
	settings.update(kwargs)

	format = QTextCharFormat(settings.format)

	settings.backgroundColor and format.setBackground(settings.backgroundColor)
	settings.color and format.setForeground(settings.color)
	settings.fontWeight and format.setFontWeight(settings.fontWeight)
	settings.fontPointSize and format.setFontPointSize(settings.fontPointSize)
	settings.italic and	format.setFontItalic(True)

	return format

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
DEFAULT_FORMAT = getFormat(color=QColor(192, 192, 192))

DEFAULT_THEME = {"default" : getFormat(format=DEFAULT_FORMAT, backgroundColor=QColor(40, 40, 40)),
			"comment" : getFormat(format=DEFAULT_FORMAT, color=QColor(96, 96, 96)),
			"comment.line" : None,
			"comment.line.double-slash" : None,
			"comment.line.double-dash" : None,
			"comment.line.number-sign" : None,
			"comment.line.percentage" : None,
			"comment.line.character" : None,
			"comment.block" : getFormat(format=DEFAULT_FORMAT, color=QColor(128, 128, 128)),
			"comment.block.documentation" : None,
			"constant" : getFormat(format=DEFAULT_FORMAT, color=QColor(205, 105, 75)),
			"constant.numeric" : None,
			"constant.character" : None,
			"constant.character.escape" : None,
			"constant.language" : None,
			"constant.other" : None,
			"entity" : getFormat(format=DEFAULT_FORMAT, color=QColor(115, 135, 175)),
			"entity.name" : None,
			"entity.name.function" : None,
			"entity.name.type" : None,
			"entity.name.tag" : None,
			"entity.name.section" : None,
			"entity.other" : None,
			"entity.inherited-class" : None,
			"entity.attribute-name" : None,
			"invalid" : None,
			"invalid.illegal" : None,
			"invalid.deprecated" : None,
			"keyword" : getFormat(format=DEFAULT_FORMAT, color=QColor(205, 170, 105), fontWeight=75),
			"keyword.control" : None,
			"keyword.operator" : getFormat(format=DEFAULT_FORMAT, color=QColor(205, 170, 105)),
			"keyword.other" : None,
			"markup" : None,
			"markup.underline" : None,
			"markup.underline.link" : None,
			"markup.bold" : None,
			"markup.heading" : None,
			"markup.italic" : None,
			"markup.list" : None,
			"markup.list.numbered" : None,
			"markup.list.unnumbered" : None,
			"markup.quote" : None,
			"markup.raw" : None,
			"markup.other" : None,
			"meta" : None,
			"storage" : None,
			"storage.type" : getFormat(format=DEFAULT_FORMAT, color=QColor(205, 170, 105), fontWeight=75),
			"storage.modifier" : getFormat(format=DEFAULT_FORMAT, italic=True),
			"string" : getFormat(format=DEFAULT_FORMAT, color=QColor(145, 160, 105), italic=True),
			"string.quoted" : None,
			"string.quoted.single" : None,
			"string.quoted.double" : None,
			"string.quoted.triple" : None,
			"string.quoted.other" : None,
			"string.unquoted" : None,
			"string.interpolated" : None,
			"string.regexp" : None,
			"string.other" : None,
			"support" : getFormat(format=DEFAULT_FORMAT, color=QColor(115, 135, 175)),
			"support.function" : None,
			"support.class" : None,
			"support.type" : None,
			"support.constant" : None,
			"support.variable" : None,
			"support.other" : None,
			"variable" : getFormat(format=DEFAULT_FORMAT, italic=True),
			"variable.parameter" : None,
			"variable.language" : None,
			"variable.language.other" : None,
			"accelerator.line": getFormat(format=DEFAULT_FORMAT, backgroundColor=QColor(48, 48, 48)),
			"accelerator.occurence": getFormat(format=DEFAULT_FORMAT, backgroundColor=QColor(64, 64, 64)),
			"accelerator.pair": getFormat(format=DEFAULT_FORMAT, backgroundColor=QColor(64, 64, 64))}

LOGGING_THEME = {"default" : getFormat(format=DEFAULT_FORMAT, backgroundColor=QColor(40, 40, 40)),
			"logging.message" : getFormat(format=DEFAULT_FORMAT),
			"logging.message.critical" : getFormat(format=DEFAULT_FORMAT, color=QColor(48, 48, 48),
										backgroundColor=QColor(255, 64, 64)),
			"logging.message.error" : getFormat(format=DEFAULT_FORMAT, color=QColor(255, 64, 64)),
			"logging.message.warning" : getFormat(format=DEFAULT_FORMAT, color=QColor(255, 128, 0)),
			"logging.message.debug" : getFormat(format=DEFAULT_FORMAT, italic=True),
			"logging.message.debug.trace.in" : getFormat(format=DEFAULT_FORMAT, color=QColor(128, 160, 192), italic=True),
			"logging.message.debug.trace.out" : getFormat(format=DEFAULT_FORMAT, color=QColor(192, 160, 128), italic=True)}
