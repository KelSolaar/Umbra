#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**active_QLabel.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`Active_QLabelsCollection` class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

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
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Defines a `QObject <http://doc.qt.nokia.com/qobject.html>`_ subclass providing
	a group for :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` class objects.
	"""

	# Custom signals definitions.
	activeLabelClicked = pyqtSignal(Active_QLabel)
	"""
	This signal is emited by the :class:`Active_QLabelsCollection` class
	when one of its :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` child has been clicked. ( pyqtSignal )

	:return: Current clicked active label.
	:rtype: Active_QLabel
	"""

	activeLabelPressed = pyqtSignal(Active_QLabel)
	"""
	This signal is emited by the :class:`Active_QLabelsCollection` class
	when one of its :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` child has been pressed. ( pyqtSignal )

	:return: Current clicked active label.
	:rtype: Active_QLabel
	"""

	activeLabelReleased = pyqtSignal(Active_QLabel)
	"""
	This signal is emited by the :class:`Active_QLabelsCollection` class
	when one of its :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` child has been released. ( pyqtSignal )

	:return: Current clicked active label.
	:rtype: Active_QLabel
	"""

	activeLabelToggled = pyqtSignal(Active_QLabel)
	"""
	This signal is emited by the :class:`Active_QLabelsCollection` class
	when one of its :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` child has been toggled. ( pyqtSignal )

	:return: Current checked active label.
	:rtype: Active_QLabel
	"""

	def __init__(self, parent=None):
		"""
		Initializes the class.

		:param parent: Widget parent.
		:type parent: QObject
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
		Property for **self.__container** attribute.

		:return: self.__container.
		:rtype: QObject
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		Setter for **self.__container** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		Deleter for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def activeLabels(self):
		"""
		Property for **self.__activeLabels** attribute.

		:return: self.__activeLabels.
		:rtype: list
		"""

		return self.__activeLabels

	@activeLabels.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def activeLabels(self, value):
		"""
		Setter for **self.__activeLabels** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "activeLabels"))

	@activeLabels.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def activeLabels(self):
		"""
		Deleter for **self.__activeLabels** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "activeLabels"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __activeLabel__toggled(self, activeLabel, state):
		"""
		Defines the slot triggered by an **Active_QLabel** Widget when toggled.

		:param activeLabel: Active label.
		:type activeLabel: Active_QLabel
		:param state: Active label checked state.
		:type state: bool
		"""

		LOGGER.debug("> Toggled 'Active_QLabel': '{0}'.".format(activeLabel))

		self.__updateSiblingsActiveLabelsStates(activeLabel)

	def __updateSiblingsActiveLabelsStates(self, activeLabel):
		"""
		Updates given **Active_QLabel** Widget siblings states.

		:param activeLabel: Active label.
		:type activeLabel: Active_QLabel
		"""

		LOGGER.debug("> Clicked 'Active_QLabel': '{0}'.".format(activeLabel))

		for item in self.__activeLabels:
			if item is activeLabel:
				continue

			umbra.ui.common.signalsBlocker(item, item.setChecked, False)

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def addActiveLabel(self, activeLabel):
		"""
		Adds given **Active_QLabel** Widget.

		:param activeLabel: Active label to add.
		:type activeLabel: Active_QLabel
		:return: Method success.
		:rtype: bool
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
		Removes given **Active_QLabel** Widget.

		:param activeLabel: Active label to remove.
		:type activeLabel: Active_QLabel
		:return: Method success.
		:rtype: bool
		"""

		if not activeLabel in self.__activeLabels:
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' is not in the collection!".format(
			self.__class__.__name__, activeLabel))

		self.__activeLabels.remove(activeLabel)
		return True

	def getToggledActiveLabel(self):
		"""
		Returns the toggled **Active_QLabel** Widget.

		:return: Checked active label.
		:rtype: bool
		"""

		for activeLabel in self.__activeLabels:
			if activeLabel.checked:
				return activeLabel

	def getActiveLabelIndex(self, activeLabel):
		"""
		Returns given **Active_QLabel** Widget index.

		:param activeLabel: Active label to retrieve index.
		:type activeLabel: Active_QLabel
		:return: Active label index.
		:rtype: int
		"""

		return self.__activeLabels.index(activeLabel)

	def getActiveLabelFromIndex(self, index):
		"""
		Returns the **Active_QLabel** Widget from given index.

		:param index: Index.
		:type index: int
		:return: Active label.
		:rtype: Active_QLabel
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
