#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**delegates.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application Delegates classes.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QStyle
from PyQt4.QtGui import QStyledItemDelegate
from PyQt4.QtGui import QTextDocument

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
import umbra.ui.common
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

__all__ = ["LOGGER", "RichText_QStyledItemDelegate"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Style(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for the :class:`RichText_QStyledItemDelegate` class style. 
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: . ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class RichText_QStyledItemDelegate(QStyledItemDelegate):
	"""
	This class is a `QStyledItemDelegate <http://doc.qt.nokia.com/qstyleditemdelegate.html>`_ subclass used as a rich
	text Delegate for Application Views. 
	"""

	@core.executionTrace
	def __init__(self,
				parent=None,
				style=None,
				highlightColor=None,
				hoverColor=None,
				backgroundColor=None,
				highlightBackgroundColor=None,
				hoverBackgroundColor=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		:param style: Style. ( Style )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QStyledItemDelegate.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__indent = 5

		self.__label = QLabel()
		self.__label.setIndent(self.__indent)
		self.__label.setTextFormat(Qt.RichText)

		self.__defaultStyle = Style(default=\
								"""
								QLabel, QLabel link {
									background-color: rgb(40, 40, 40);
									color: rgb(192, 192, 192);
								}
								""",
								hover=\
								"""
								QLabel, QLabel link {
									background-color: rgb(80, 80, 80);
									color: rgb(192, 192, 192);
								}
								""",
								highlight=\
								"""
								QLabel, QLabel link {
									background-color: rgb(128, 128, 128);
									color: rgb(224, 224, 224);
								}
								""")

		self.__style = self.__defaultStyle
		self.style = style or self.__style

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def style(self):
		"""
		This method is the property for **self.__style** attribute.

		:return: self.__style. ( Style )
		"""

		return self.__style

	@style.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def style(self, value):
		"""
		This method is the setter method for **self.__style** attribute.

		:param value: Attribute value. ( Style )
		"""

		if value is not None:
			assert type(value) is Style, "'{0}' attribute: '{1}' type is not 'Style'!".format("style", value)
			style = Style()
			for item in(self.__defaultStyle, value):
				style.update(item)
			value = style
		self.__style = value

	@style.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def style(self):
		"""
		This method is the deleter method for **self.__style** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "style"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	# @core.executionTrace
	def paint(self, painter, option, index):
		"""
		This method reimplements the :meth:`QStyledItemDelegate.paint` method.
		"""

		if option.state & QStyle.State_MouseOver:
			styleSheet = self.__style.hover
		elif option.state & QStyle.State_Selected:
			styleSheet = self.__style.highlight
		else:
			styleSheet = self.__style.default

		self.__label.setStyleSheet(styleSheet)
		data = index.model().data(index, Qt.DisplayRole)
		self.__label.setText(umbra.ui.common.getQVariantAsString(data))
		self.__label.setFixedSize(option.rect.size())
		painter.save()
		painter.translate(option.rect.topLeft())
		self.__label.render(painter)
		painter.restore()

	# @core.executionTrace
	def sizeHint(self, option, index):
		"""
		This method reimplements the :meth:`QStyledItemDelegate.sizeHint` method.
		"""

		document = QTextDocument()
		document.setDefaultFont(option.font)
		data = index.model().data(index)
		text = umbra.ui.common.getQVariantAsString(data)
		self.__label.setText(text)
		document.setHtml(text)
		return QSize(document.idealWidth() + self.__indent, option.fontMetrics.height())
