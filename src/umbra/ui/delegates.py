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

__all__ = ["LOGGER", "RichText_QStyledItemDelegate"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class RichText_QStyledItemDelegate(QStyledItemDelegate):
	"""
	This class is a `QStyledItemDelegate <http://doc.qt.nokia.com/qstyleditemdelegate.html>`_ subclass used as a rich
	text Delegate for Application Views. 
	"""

	@core.executionTrace
	def __init__(self,
				parent=None,
				backgroundColor=None,
				selectedBackgroundColor=None,
				hoverBackgroundColor=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		:param backgroundColor: Default background color. ( QColor )
		:param selectedBackgroundColor: Selected background color. ( QColor )
		:param hoverBackgroundColor: Hover border color. ( QColor )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QStyledItemDelegate.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__indent = 5
		self.__style = """
						QLabel, QLabel link {{
							background-color: {0};
						}}
						"""

		self.__backgroundColor = QColor(40, 40, 40)
		self.__selectedBackgroundColor = QColor(96, 96, 96)
		self.__hoverBackgroundColor = QColor(80, 80, 80)
		self.backgroundColor = backgroundColor or self.__backgroundColor
		self.selectedBackgroundColor = selectedBackgroundColor or self.__selectedBackgroundColor
		self.hoverBackgroundColor = hoverBackgroundColor or self.__hoverBackgroundColor

		self.__label = QLabel()
		self.__label.setIndent(self.__indent)
		self.__label.setTextFormat(Qt.RichText)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def backgroundColor(self):
		"""
		This method is the property for **self.__backgroundColor** attribute.

		:return: self.__backgroundColor. ( QColor )
		"""

		return self.__backgroundColor

	@backgroundColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def backgroundColor(self, value):
		"""
		This method is the setter method for **self.__backgroundColor** attribute.

		:param value: Attribute value. ( QColor )
		"""

		if value is not None:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("backgroundColor", value)
		self.__backgroundColor = value

	@backgroundColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def backgroundColor(self):
		"""
		This method is the deleter method for **self.__backgroundColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "backgroundColor"))

	@property
	def selectedBackgroundColor(self):
		"""
		This method is the property for **self.__selectedBackgroundColor** attribute.

		:return: self.__selectedBackgroundColor. ( QColor )
		"""

		return self.__selectedBackgroundColor

	@selectedBackgroundColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def selectedBackgroundColor(self, value):
		"""
		This method is the setter method for **self.__selectedBackgroundColor** attribute.

		:param value: Attribute value. ( QColor )
		"""

		if value is not None:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("selectedBackgroundColor", value)
		self.__selectedBackgroundColor = value

	@selectedBackgroundColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def selectedBackgroundColor(self):
		"""
		This method is the deleter method for **self.__selectedBackgroundColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "selectedBackgroundColor"))

	@property
	def hoverBackgroundColor(self):
		"""
		This method is the property for **self.__hoverBackgroundColor** attribute.

		:return: self.__hoverBackgroundColor. ( QColor )
		"""

		return self.__hoverBackgroundColor

	@hoverBackgroundColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def hoverBackgroundColor(self, value):
		"""
		This method is the setter method for **self.__hoverBackgroundColor** attribute.

		:param value: Attribute value. ( QColor )
		"""

		if value is not None:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("hoverBackgroundColor", value)
		self.__hoverBackgroundColor = value

	@hoverBackgroundColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def hoverBackgroundColor(self):
		"""
		This method is the deleter method for **self.__hoverBackgroundColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "hoverBackgroundColor"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	# @core.executionTrace
	def paint(self, painter, option, index):
		"""
		This method reimplements the :meth:`QStyledItemDelegate.paint` method.
		"""

		color = "rgb({0}, {1}, {2})"
		if option.state & QStyle.State_MouseOver:
			syleSheet = self.__style.format(color.format(self.__hoverBackgroundColor.red(),
														self.__hoverBackgroundColor.green(),
														self.__hoverBackgroundColor.blue()))
		elif option.state & QStyle.State_Selected:
			syleSheet = self.__style.format(color.format(self.__selectedBackgroundColor.red(),
														self.__selectedBackgroundColor.green(),
														self.__selectedBackgroundColor.blue()))
		else:
			syleSheet = self.__style.format(color.format(self.__backgroundColor.red(),
														self.__backgroundColor.green(),
														self.__backgroundColor.blue()))
		self.__label.setStyleSheet(syleSheet)
		text = index.model().data(index, Qt.DisplayRole)
		self.__label.setText(text)
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
		text = index.model().data(index)
		text and document.setHtml(text)
		return QSize(document.idealWidth() + self.__indent, option.fontMetrics.height())
