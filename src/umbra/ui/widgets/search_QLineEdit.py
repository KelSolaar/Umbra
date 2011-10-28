#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**search_QLineEdit.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Search_QLineEdit` class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import functools
import logging
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
from umbra.globals.constants import Constants

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Search_QLineEdit"]

LOGGER = logging.getLogger(Constants.logger)

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class Search_QLineEdit(QLineEdit):
	"""
	This class is a `QLineEdit <http://doc.qt.nokia.com/4.7/qlinedit.html>`_ subclass providing a search field with clearing capabilities.
	"""

	@core.executionTrace
	def __init__(self, parent=None, uiSearchImage=None, uiSearchClickedImage=None, uiClearImage=None, uiClearClickedImage=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		:param uiSearchImage: Search button image path. ( String )
		:param uiSearchClickedImage: Search button clicked image path. ( String )
		:param uiClearImage: Clear button image path. ( String )
		:param uiClearClickedImage: Clear button clicked image path. ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QLineEdit.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__uiSearchImage = None
		self.uiSearchImage = uiSearchImage
		self.__uiSearchClickedImage = None
		self.uiSearchClickedImage = uiSearchClickedImage
		self.__uiClearImage = None
		self.uiClearImage = uiClearImage
		self.__uiClearClickedImage = None
		self.uiClearClickedImage = uiClearClickedImage
		self.__parent = None
		self.parent = parent

		self.__searchButton = QToolButton(self)
		self.__searchButton.setObjectName("Search_Field_button")

		self.__clearButton = QToolButton(self)
		self.__clearButton.setObjectName("Clear_Field_button")

		Search_QLineEdit.__initializeUi(self)
		self.__setClearButtonVisibility(self.text())

		# Signals / Slots.
		self.__clearButton.clicked.connect(self.clear)
		self.textChanged.connect(self.__setClearButtonVisibility)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
	@property
	def uiSearchImage(self):
		"""
		This method is the property for **self.__uiSearchImage** attribute.

		:return: self.__uiSearchImage. ( String )
		"""

		return self.__uiSearchImage

	@uiSearchImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def uiSearchImage(self, value):
		"""
		This method is the setter method for **self.__uiSearchImage** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("uiSearchImage", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("uiSearchImage", value)
		self.__uiSearchImage = value

	@uiSearchImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSearchImage(self):
		"""
		This method is the deleter method for **self.__uiSearchImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiSearchImage"))

	@property
	def uiSearchClickedImage(self):
		"""
		This method is the property for **self.__uiSearchClickedImage** attribute.

		:return: self.__uiSearchClickedImage. ( String )
		"""

		return self.__uiSearchClickedImage

	@uiSearchClickedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def uiSearchClickedImage(self, value):
		"""
		This method is the setter method for **self.__uiSearchClickedImage** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("uiSearchClickedImage", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("uiSearchClickedImage", value)
		self.__uiSearchClickedImage = value

	@uiSearchClickedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiSearchClickedImage(self):
		"""
		This method is the deleter method for **self.__uiSearchClickedImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiSearchClickedImage"))

	@property
	def uiClearImage(self):
		"""
		This method is the property for **self.__uiClearImage** attribute.

		:return: self.__uiClearImage. ( String )
		"""

		return self.__uiClearImage

	@uiClearImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def uiClearImage(self, value):
		"""
		This method is the setter method for **self.__uiClearImage** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("uiClearImage", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("uiClearImage", value)
		self.__uiClearImage = value

	@uiClearImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearImage(self):
		"""
		This method is the deleter method for **self.__uiClearImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiClearImage"))

	@property
	def uiClearClickedImage(self):
		"""
		This method is the property for **self.__uiClearClickedImage** attribute.

		:return: self.__uiClearClickedImage. ( String )
		"""

		return self.__uiClearClickedImage

	@uiClearClickedImage.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def uiClearClickedImage(self, value):
		"""
		This method is the setter method for **self.__uiClearClickedImage** attribute.

		:param value: Attribute value. ( String )
		"""

		if value:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("uiClearClickedImage", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("uiClearClickedImage", value)
		self.__uiClearClickedImage = value

	@uiClearClickedImage.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def uiClearClickedImage(self):
		"""
		This method is the deleter method for **self.__uiClearClickedImage** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "uiClearClickedImage"))

	@property
	def parent(self):
		"""
		This method is the property for **self.__parent** attribute.

		:return: self.__parent. ( QObject )
		"""

		return self.__parent

	@parent.setter
	def parent(self, value):
		"""
		This method is the setter method for **self.__parent** attribute.

		:param value: Attribute value. ( QObject )
		"""

		self.__parent = value

	@parent.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def parent(self):
		"""
		This method is the deleter method for **self.__parent** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "parent"))

	@property
	def searchButton(self):
		"""
		This method is the property for **self.__searchButton** attribute.

		:return: self.__searchButton. ( QPushButton )
		"""

		return self.__searchButton

	@searchButton.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchButton(self, value):
		"""
		This method is the setter method for **self.__searchButton** attribute.

		:param value: Attribute value. ( QPushButton )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "searchButton"))

	@searchButton.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchButton(self):
		"""
		This method is the deleter method for **self.__searchButton** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchButton"))

	@property
	def clearButton(self):
		"""
		This method is the property for **self.__clearButton** attribute.

		:return: self.__clearButton. ( QPushButton )
		"""

		return self.__clearButton

	@clearButton.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def clearButton(self, value):
		"""
		This method is the setter method for **self.__clearButton** attribute.

		:param value: Attribute value. ( QPushButton )
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "clearButton"))

	@clearButton.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def clearButton(self):
		"""
		This method is the deleter method for **self.__clearButton** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "clearButton"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def resizeEvent(self, event):
		"""
		This method overloads the **Search_QLineEdit** Widget resize event.

		:param event: Resize event. ( QResizeEvent )
		"""

		size = self.__clearButton.sizeHint()
		frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
		self.__searchButton.move(self.rect().left() + frameWidth, (self.rect().bottom() - size.height()) / 2 + frameWidth / 2);
		self.__clearButton.move(self.rect().right() - frameWidth - size.width(), (self.rect().bottom() - size.height()) / 2 + frameWidth / 2);

	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		buttons = {self.__searchButton : (self.__uiSearchImage, self.__uiSearchClickedImage, "Search"),
					self.__clearButton : (self.__uiClearImage, self.__uiClearClickedImage, "Clear")}
		for button, data in buttons.items():
			image, clickedImage, text = data
			if image and clickedImage:
				pixmap = QPixmap(image)
				clickedPixmap = QPixmap(clickedImage)
				button.setStyleSheet("QToolButton { border: none; padding: 0px; }");
				button.setIcon(QIcon(pixmap))
				button.setMaximumSize(pixmap.size())

				# Signals / Slots.
				button.pressed.connect(functools.partial(button.setIcon, QIcon(clickedPixmap)))
				button.released.connect(functools.partial(button.setIcon, QIcon(pixmap)))
			else:
				button.setText(text)

		frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
		self.setStyleSheet(QString("QLineEdit { padding-left: " + str(self.__searchButton.sizeHint().width() + frameWidth) + "px; padding-right: " + str(self.__clearButton.sizeHint().width() + frameWidth)) + "px; }")
		self.setMinimumSize(max(self.minimumSizeHint().width(), self.__clearButton.sizeHint().height() + frameWidth * 2), max(self.minimumSizeHint().height(), self.__clearButton.sizeHint().height() + frameWidth * 2));

	@core.executionTrace
	def __setClearButtonVisibility(self, text):
		"""
		This method sets the clear button visibility.

		:param text: Current field text. ( QString )
		"""

		if text:
			self.__clearButton.show()
		else:
			self.__clearButton.hide()
