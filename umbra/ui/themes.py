#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**highlighters.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the Application themes classes.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QTextCharFormat

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.data_structures
import foundations.exceptions
import foundations.verbose

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "get_format",
			"DEFAULT_FORMAT",
			"DEFAULT_THEME",
			"LOGGING_THEME"]

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def get_format(**kwargs):
	"""
	Returns a `QTextCharFormat <http://doc.qt.nokia.com/qtextcharformat.html>`_ format.
	
	:param \*\*kwargs: Format settings.
	:type \*\*kwargs: dict
	:return: Format.
	:rtype: QTextCharFormat
	"""

	settings = foundations.data_structures.Structure(**{"format" : QTextCharFormat(),
								"background_color" : None,
								"color" : None,
								"font_weight" : None,
								"font_point_size" : None,
								"italic" : False})
	settings.update(kwargs)

	format = QTextCharFormat(settings.format)

	settings.background_color and format.setBackground(settings.background_color)
	settings.color and format.setForeground(settings.color)
	settings.font_weight and format.setFontWeight(settings.font_weight)
	settings.font_point_size and format.setFontPointSize(settings.font_point_size)
	settings.italic and	format.setFontItalic(True)

	return format

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
DEFAULT_FORMAT = get_format(color=QColor(192, 192, 192))

DEFAULT_THEME = {"default" : get_format(format=DEFAULT_FORMAT, background_color=QColor(32, 32, 32)),
			"comment" : get_format(format=DEFAULT_FORMAT, color=QColor(96, 96, 96)),
			"comment.line" : None,
			"comment.line.double-slash" : None,
			"comment.line.double-dash" : None,
			"comment.line.number-sign" : None,
			"comment.line.percentage" : None,
			"comment.line.character" : None,
			"comment.block" : get_format(format=DEFAULT_FORMAT, color=QColor(128, 128, 128)),
			"comment.block.documentation" : None,
			"constant" : get_format(format=DEFAULT_FORMAT, color=QColor(205, 105, 75)),
			"constant.numeric" : None,
			"constant.character" : None,
			"constant.character.escape" : None,
			"constant.language" : None,
			"constant.other" : None,
			"entity" : get_format(format=DEFAULT_FORMAT, color=QColor(115, 135, 175)),
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
			"keyword" : get_format(format=DEFAULT_FORMAT, color=QColor(205, 170, 105), font_weight=75),
			"keyword.control" : None,
			"keyword.operator" : get_format(format=DEFAULT_FORMAT, color=QColor(205, 170, 105)),
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
			"storage.type" : get_format(format=DEFAULT_FORMAT, color=QColor(205, 170, 105), font_weight=75),
			"storage.modifier" : get_format(format=DEFAULT_FORMAT, italic=True),
			"string" : get_format(format=DEFAULT_FORMAT, color=QColor(145, 160, 105), italic=True),
			"string.quoted" : None,
			"string.quoted.single" : None,
			"string.quoted.double" : None,
			"string.quoted.triple" : None,
			"string.quoted.other" : None,
			"string.unquoted" : None,
			"string.interpolated" : None,
			"string.regexp" : None,
			"string.other" : None,
			"support" : get_format(format=DEFAULT_FORMAT, color=QColor(115, 135, 175)),
			"support.function" : None,
			"support.class" : None,
			"support.type" : None,
			"support.constant" : None,
			"support.variable" : None,
			"support.other" : None,
			"variable" : get_format(format=DEFAULT_FORMAT, italic=True),
			"variable.parameter" : None,
			"variable.language" : None,
			"variable.language.other" : None,
			"accelerator.line": get_format(format=DEFAULT_FORMAT, background_color=QColor(48, 48, 48)),
			"accelerator.occurence": get_format(format=DEFAULT_FORMAT, background_color=QColor(64, 64, 64)),
			"accelerator.pair": get_format(format=DEFAULT_FORMAT, background_color=QColor(64, 64, 64))}

LOGGING_THEME = {"default" : get_format(format=DEFAULT_FORMAT, background_color=QColor(32, 32, 32)),
			"logging.message" : get_format(format=DEFAULT_FORMAT),
			"logging.message.critical" : get_format(format=DEFAULT_FORMAT, color=QColor(48, 48, 48),
										background_color=QColor(255, 64, 64)),
			"logging.message.error" : get_format(format=DEFAULT_FORMAT, color=QColor(255, 64, 64)),
			"logging.message.warning" : get_format(format=DEFAULT_FORMAT, color=QColor(255, 128, 0)),
			"logging.message.debug" : get_format(format=DEFAULT_FORMAT, italic=True),
			"logging.message.debug.trace.in" : get_format(format=DEFAULT_FORMAT, color=QColor(128, 160, 192), italic=True),
			"logging.message.debug.trace.out" : get_format(format=DEFAULT_FORMAT, color=QColor(192, 160, 128), italic=True)}
