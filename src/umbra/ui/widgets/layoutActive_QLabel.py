#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**layoutActive_QLabel.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`LayoutActive_QLabel` class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
from umbra.globals.constants import Constants
from umbra.ui.widgets.active_QLabel import Active_QLabel

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "LayoutActiveLabel"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class LayoutActiveLabel(Active_QLabel):
	"""
	This class defines an advanced :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` subclass
	used by the :class:`umbra.managers.layoutsManager.LayoutsManager`. 
	"""

	@core.executionTrace
	def __init__(self,
				parent=None,
				title=None,
				layout=None,
				shortcut=None,
				defaultPixmap=None,
				hoverPixmap=None,
				activePixmap=None,
				checkable=False,
				checked=False):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		:param title: Widget title. ( String )
		:param layout: Associated layout name. ( String )
		:param shortcut: Associated shortcut. ( Integer )
		:param defaultPixmap: Label default pixmap. ( QPixmap )
		:param hoverPixmap: Label hover pixmap. ( QPixmap )
		:param activePixmap: Label active pixmap. ( QPixmap )
		:param checkable: Checkable state. ( Boolean )
		:param checked: Checked state. ( Boolean )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		Active_QLabel.__init__(self, parent, defaultPixmap, hoverPixmap, activePixmap, checkable, checked)

		# --- Setting class attributes. ---
		self.__title = None
		self.title = title
		self.__layout = None
		self.layout = layout
		self.__shortcut = None
		self.shortcut = shortcut

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************	@property
	@property
	def title(self):
		"""
		This method is the property for **self.__title** attribute.

		:return: self.__title. ( String )
		"""

		return self.__title

	@title.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def title(self, value):
		"""
		This method is the setter method for **self.__title** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("title", value)
		self.__title = value

	@title.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def title(self):
		"""
		This method is the deleter method for **self.__title** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "title"))

	@property
	def layout(self):
		"""
		This method is the property for **self.__layout** attribute.

		:return: self.__layout. ( String )
		"""

		return self.__layout

	@layout.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def layout(self, value):
		"""
		This method is the setter method for **self.__layout** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("layout", value)
		self.__layout = value

	@layout.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def layout(self):
		"""
		This method is the deleter method for **self.__layout** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "layout"))

	@property
	def shortcut(self):
		"""
		This method is the property for **self.__shortcut** attribute.

		:return: self.__shortcut. ( Integer )
		"""

		return self.__shortcut

	@shortcut.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def shortcut(self, value):
		"""
		This method is the setter method for **self.__shortcut** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert hasattr(value, "__int__"), "'{0}' attribute: '{1}' cannot be converted to 'int'!".format("shortcut", value)
		self.__shortcut = value

	@shortcut.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def shortcut(self):
		"""
		This method is the deleter method for **self.__shortcut** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "shortcut"))
