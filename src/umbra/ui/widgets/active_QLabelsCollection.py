#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**active_QLabel.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`Active_QLabelsCollection` class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import logging
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal

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

__all__ = ["LOGGER", "Active_QLabelsCollection"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Active_QLabelsCollection(QObject):
	"""
	This class is a `QObject <http://doc.qt.nokia.com/qobject.html>`_ subclass providing
	a group for :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` class objects.
	"""

	# Custom signals definitions.
	activeLabelclicked = pyqtSignal(Active_QLabel)
	"""
	This signal is emited by the :class:`Active_QLabelsCollection` class when it receives a mouse press event. ( pyqtSignal )

	:return: Current clicked active label. ( activeLabelclicked )	
	"""

	@core.executionTrace
	def __init__(self, parent=None):
		"""
		This method initializes the class.

		:param parent: Widget parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QObject.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__container = parent

		self.__activeLabels = []

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def activeLabels(self):
		"""
		This method is the property for **self.__activeLabels** attribute.

		:return: self.__activeLabels. ( List )
		"""

		return self.__activeLabels

	@activeLabels.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def activeLabels(self, value):
		"""
		This method is the setter method for **self.__activeLabels** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "activeLabels"))

	@activeLabels.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def activeLabels(self):
		"""
		This method is the deleter method for **self.__activeLabels** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "activeLabels"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __activeLabel__clicked(self, activeLabel):
		"""
		This method is triggered when an **Active_QLabel** Widget is clicked.
		"""

		LOGGER.debug("> Clicked 'Active_QLabel': '{0}'.".format(activeLabel))

		for item in self.__activeLabels:
			item is not activeLabel and item.setChecked(False)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addActiveLabel(self, activeLabel):
		"""
		This method adds given **Active_QLabel** Widget.

		:param activeLabel: Active label to add. ( Active_QLabel )
		:return: Method success. ( Boolean )
		"""

		if not isinstance(activeLabel, Active_QLabel):
			# TODO:
			raise

		if activeLabel not in self.__activeLabels:
			not self.__activeLabels and activeLabel.setChecked(True) or activeLabel.setChecked(False)
			print activeLabel, activeLabel.checked
			activeLabel.clicked.connect(functools.partial(self.__activeLabel__clicked, activeLabel))
			activeLabel.clicked.connect(functools.partial(self.activeLabelclicked.emit, activeLabel))
			self.__activeLabels.append(activeLabel)
		else:
			# TODO:
			raise

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeActiveLabel(self, activeLabel):
		"""
		This method removes given **Active_QLabel** Widget.

		:param activeLabel: Active label to remove. ( Active_QLabel )
		:return: Method success. ( Boolean )
		"""

		if activeLabel in self.__activeLabels:
			activeLabel.clicked.disconnect(self.__setCheckedStates)
			self.__activeLabels.remove(activeLabel)
		else:
			# TODO:
			raise

		return True
