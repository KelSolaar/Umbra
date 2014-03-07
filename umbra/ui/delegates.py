#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**delegates.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the Application Delegates classes.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QStyle
from PyQt4.QtGui import QStyledItemDelegate
from PyQt4.QtGui import QTextDocument

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.dataStructures
import foundations.exceptions
import foundations.verbose
import umbra.ui.common

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "RichText_QStyledItemDelegate"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Style(foundations.dataStructures.Structure):
	"""
	Defines a storage object for the :class:`RichText_QStyledItemDelegate` class style. 
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param \*\*kwargs: .
		:type \*\*kwargs: dict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class RichText_QStyledItemDelegate(QStyledItemDelegate):
	"""
	Defines a `QStyledItemDelegate <http://doc.qt.nokia.com/qstyleditemdelegate.html>`_ subclass used as a rich
	text Delegate for Application Views. 
	"""

	def __init__(self,
				parent=None,
				style=None,
				highlightColor=None,
				hoverColor=None,
				backgroundColor=None,
				highlightBackgroundColor=None,
				hoverBackgroundColor=None):
		"""
		Initializes the class.

		:param parent: Widget parent.
		:type parent: QObject
		:param style: Style.
		:type style: Style
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
									background-color: rgb(32, 32, 32);
									color: rgb(192, 192, 192);
								}
								""",
								hover=\
								"""
								QLabel, QLabel link {
									background-color: rgb(64, 64, 64);
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
		Property for **self.__style** attribute.

		:return: self.__style.
		:rtype: Style
		"""

		return self.__style

	@style.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def style(self, value):
		"""
		Setter for **self.__style** attribute.

		:param value: Attribute value.
		:type value: Style
		"""

		if value is not None:
			assert type(value) is Style, "'{0}' attribute: '{1}' type is not 'Style'!".format("style", value)
			style = Style()
			for item in(self.__defaultStyle, value):
				style.update(item)
			value = style
		self.__style = value

	@style.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def style(self):
		"""
		Deleter for **self.__style** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "style"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def paint(self, painter, option, index):
		"""
		Reimplements the :meth:`QStyledItemDelegate.paint` method.
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

	def sizeHint(self, option, index):
		"""
		Reimplements the :meth:`QStyledItemDelegate.sizeHint` method.
		"""

		document = QTextDocument()
		document.setDefaultFont(option.font)
		data = index.model().data(index)
		text = umbra.ui.common.getQVariantAsString(data)
		self.__label.setText(text)
		document.setHtml(text)
		return QSize(document.idealWidth() + self.__indent, option.fontMetrics.height())
