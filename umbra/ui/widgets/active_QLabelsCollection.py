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
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import umbra.ui.common
from umbra.ui.widgets.active_QLabel import Active_QLabel

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Active_QLabelsCollection"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Active_QLabelsCollection(QObject):
	"""
	This class is a `QObject <http://doc.qt.nokia.com/qobject.html>`_ subclass providing
	a group for :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` class objects.
	"""

	# Custom signals definitions.
	activeLabelClicked = pyqtSignal(Active_QLabel)
	"""
	This signal is emited by the :class:`Active_QLabelsCollection` class
	when one of its :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` child has been clicked. ( pyqtSignal )

	:return: Current clicked active label. ( Active_QLabel )	
	"""

	activeLabelPressed = pyqtSignal(Active_QLabel)
	"""
	This signal is emited by the :class:`Active_QLabelsCollection` class
	when one of its :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` child has been pressed. ( pyqtSignal )

	:return: Current clicked active label. ( Active_QLabel )	
	"""

	activeLabelReleased = pyqtSignal(Active_QLabel)
	"""
	This signal is emited by the :class:`Active_QLabelsCollection` class
	when one of its :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` child has been released. ( pyqtSignal )

	:return: Current clicked active label. ( Active_QLabel )	
	"""

	activeLabelToggled = pyqtSignal(Active_QLabel)
	"""
	This signal is emited by the :class:`Active_QLabelsCollection` class
	when one of its :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` child has been toggled. ( pyqtSignal )

	:return: Current checked active label. ( Active_QLabel )	
	"""

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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def activeLabels(self, value):
		"""
		This method is the setter method for **self.__activeLabels** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "activeLabels"))

	@activeLabels.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def activeLabels(self):
		"""
		This method is the deleter method for **self.__activeLabels** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "activeLabels"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __activeLabel__toggled(self, activeLabel, state):
		"""
		This method is triggered when an **Active_QLabel** Widget is toggled.

		:param activeLabel: Active label. ( Active_QLabel )
		:param state: Active label checked state. ( Boolean )
		"""

		LOGGER.debug("> Toggled 'Active_QLabel': '{0}'.".format(activeLabel))

		self.__updateSiblingsActiveLabelsStates(activeLabel)

	def __updateSiblingsActiveLabelsStates(self, activeLabel):
		"""
		This method updates given **Active_QLabel** widget siblings states.

		:param activeLabel: Active label. ( Active_QLabel )
		"""

		LOGGER.debug("> Clicked 'Active_QLabel': '{0}'.".format(activeLabel))

		for item in self.__activeLabels:
			if item is activeLabel:
				continue

			umbra.ui.common.signalsBlocker(item, item.setChecked, False)

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def addActiveLabel(self, activeLabel):
		"""
		This method adds given **Active_QLabel** Widget.

		:param activeLabel: Active label to add. ( Active_QLabel )
		:return: Method success. ( Boolean )
		"""

		if not issubclass(activeLabel.__class__, Active_QLabel):
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' must be a '{2}' subclass!".format(
			self.__class__.__name__, activeLabel, Active_QLabel.__name__))

		if activeLabel in self.__activeLabels:
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' is already in the collection!".format(
			self.__class__.__name__, activeLabel))

		activeLabel.checkable = True
		not self.__activeLabels and activeLabel.setChecked(True) or activeLabel.setChecked(False)
		self.__activeLabels.append(activeLabel)

		# Signals / Slots.
		activeLabel.toggled.connect(functools.partial(self.__activeLabel__toggled, activeLabel))

		activeLabel.clicked.connect(functools.partial(self.activeLabelClicked.emit, activeLabel))
		activeLabel.pressed.connect(functools.partial(self.activeLabelPressed.emit, activeLabel))
		activeLabel.released.connect(functools.partial(self.activeLabelReleased.emit, activeLabel))
		activeLabel.toggled.connect(functools.partial(self.activeLabelToggled.emit, activeLabel))

		return True

	def removeActiveLabel(self, activeLabel):
		"""
		This method removes given **Active_QLabel** Widget.

		:param activeLabel: Active label to remove. ( Active_QLabel )
		:return: Method success. ( Boolean )
		"""

		if not activeLabel in self.__activeLabels:
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' is not in the collection!".format(
			self.__class__.__name__, activeLabel))

		self.__activeLabels.remove(activeLabel)
		return True

	def getToggledActiveLabel(self):
		"""
		This method returns the toggled **Active_QLabel** Widget.

		:return: Checked active label. ( Boolean )
		"""

		for activeLabel in self.__activeLabels:
			if activeLabel.checked:
				return activeLabel

	def getActiveLabelIndex(self, activeLabel):
		"""
		This method returns given **Active_QLabel** Widget index.

		:param activeLabel: Active label to retrieve index. ( Active_QLabel )
		:return: Active label index. ( Integer )
		"""

		return self.__activeLabels.index(activeLabel)

	def getActiveLabelFromIndex(self, index):
		"""
		This method returns the **Active_QLabel** Widget from given index.

		:param index: Index. ( Integer )
		:return: Active label. ( Active_QLabel )
		"""

		return self.__activeLabels[index]

if __name__ == "__main__":
	import sys
	from PyQt4.QtGui import QGridLayout
	from PyQt4.QtGui import QPixmap
	from PyQt4.QtGui import QWidget

	from umbra.globals.uiConstants import UiConstants

	application = umbra.ui.common.getApplicationInstance()

	widget = QWidget()

	gridLayout = QGridLayout()
	widget.setLayout(gridLayout)

	activeLabelA = Active_QLabel(widget, QPixmap(umbra.ui.common.getResourcePath(UiConstants.developmentIcon)),
									QPixmap(umbra.ui.common.getResourcePath(UiConstants.developmentHoverIcon)),
									QPixmap(umbra.ui.common.getResourcePath(UiConstants.developmentActiveIcon)),
									checkable=True,
									checked=True)
	activeLabelB = Active_QLabel(widget, QPixmap(umbra.ui.common.getResourcePath(UiConstants.preferencesIcon)),
									QPixmap(umbra.ui.common.getResourcePath(UiConstants.preferencesHoverIcon)),
									QPixmap(umbra.ui.common.getResourcePath(UiConstants.preferencesActiveIcon)),
									checkable=True,
									checked=False)
	activeLabelC = Active_QLabel(widget, QPixmap(umbra.ui.common.getResourcePath(UiConstants.customLayoutsIcon)),
									QPixmap(umbra.ui.common.getResourcePath(UiConstants.customLayoutsHoverIcon)),
									QPixmap(umbra.ui.common.getResourcePath(UiConstants.customLayoutsActiveIcon)),
									checkable=True,
									checked=False)
	activeLabelD = Active_QLabel(widget, QPixmap(umbra.ui.common.getResourcePath(UiConstants.miscellaneousIcon)),
									QPixmap(umbra.ui.common.getResourcePath(UiConstants.miscellaneousHoverIcon)),
									QPixmap(umbra.ui.common.getResourcePath(UiConstants.miscellaneousActiveIcon)),
									checkable=True,
									checked=False)
	for activeLabel in (activeLabelA, activeLabelB, activeLabelC, activeLabelD):
		gridLayout.addWidget(activeLabel)

	active_QLabelsCollection = Active_QLabelsCollection()
	for activeLabel in (activeLabelA, activeLabelB, activeLabelC, activeLabelD):
		active_QLabelsCollection.addActiveLabel(activeLabel)

	widget.show()
	widget.raise_()

	sys.exit(application.exec_())
