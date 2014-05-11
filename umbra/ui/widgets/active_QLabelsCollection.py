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

from __future__ import unicode_literals

import functools
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal

import foundations.exceptions
import foundations.verbose
import umbra.ui.common
from umbra.ui.widgets.active_QLabel import Active_QLabel

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Active_QLabelsCollection"]

LOGGER = foundations.verbose.install_logger()

class Active_QLabelsCollection(QObject):
	"""
	Defines a `QObject <http://doc.qt.nokia.com/qobject.html>`_ subclass providing
	a group for :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` class objects.
	"""

	# Custom signals definitions.
	active_label_clicked = pyqtSignal(Active_QLabel)
	"""
	This signal is emited by the :class:`Active_QLabelsCollection` class
	when one of its :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` child has been clicked.

	:return: Current clicked active label.
	:rtype: Active_QLabel
	"""

	active_label_pressed = pyqtSignal(Active_QLabel)
	"""
	This signal is emited by the :class:`Active_QLabelsCollection` class
	when one of its :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` child has been pressed.

	:return: Current clicked active label.
	:rtype: Active_QLabel
	"""

	active_label_released = pyqtSignal(Active_QLabel)
	"""
	This signal is emited by the :class:`Active_QLabelsCollection` class
	when one of its :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` child has been released.

	:return: Current clicked active label.
	:rtype: Active_QLabel
	"""

	active_label_toggled = pyqtSignal(Active_QLabel)
	"""
	This signal is emited by the :class:`Active_QLabelsCollection` class
	when one of its :class:`umbra.ui.widgets.active_QLabel.Active_QLabel` child has been toggled.

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

		self.__active_labels = []

	@property
	def container(self):
		"""
		Property for **self.__container** attribute.

		:return: self.__container.
		:rtype: QObject
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		Setter for **self.__container** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		Deleter for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def active_labels(self):
		"""
		Property for **self.__active_labels** attribute.

		:return: self.__active_labels.
		:rtype: list
		"""

		return self.__active_labels

	@active_labels.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def active_labels(self, value):
		"""
		Setter for **self.__active_labels** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "active_labels"))

	@active_labels.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def active_labels(self):
		"""
		Deleter for **self.__active_labels** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "active_labels"))

	def __active_label__toggled(self, active_label, state):
		"""
		Defines the slot triggered by an **Active_QLabel** Widget when toggled.

		:param active_label: Active label.
		:type active_label: Active_QLabel
		:param state: Active label checked state.
		:type state: bool
		"""

		LOGGER.debug("> Toggled 'Active_QLabel': '{0}'.".format(active_label))

		self.__update_siblings_active_labels_states(active_label)

	def __update_siblings_active_labels_states(self, active_label):
		"""
		Updates given **Active_QLabel** Widget siblings states.

		:param active_label: Active label.
		:type active_label: Active_QLabel
		"""

		LOGGER.debug("> Clicked 'Active_QLabel': '{0}'.".format(active_label))

		for item in self.__active_labels:
			if item is active_label:
				continue

			umbra.ui.common.signals_blocker(item, item.set_checked, False)

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def add_active_label(self, active_label):
		"""
		Adds given **Active_QLabel** Widget.

		:param active_label: Active label to add.
		:type active_label: Active_QLabel
		:return: Method success.
		:rtype: bool
		"""

		if not issubclass(active_label.__class__, Active_QLabel):
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' must be a '{2}' subclass!".format(
			self.__class__.__name__, active_label, Active_QLabel.__name__))

		if active_label in self.__active_labels:
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' is already in the collection!".format(
			self.__class__.__name__, active_label))

		active_label.checkable = True
		not self.__active_labels and active_label.set_checked(True) or active_label.set_checked(False)
		self.__active_labels.append(active_label)

		# Signals / Slots.
		active_label.toggled.connect(functools.partial(self.__active_label__toggled, active_label))

		active_label.clicked.connect(functools.partial(self.active_label_clicked.emit, active_label))
		active_label.pressed.connect(functools.partial(self.active_label_pressed.emit, active_label))
		active_label.released.connect(functools.partial(self.active_label_released.emit, active_label))
		active_label.toggled.connect(functools.partial(self.active_label_toggled.emit, active_label))

		return True

	def remove_active_label(self, active_label):
		"""
		Removes given **Active_QLabel** Widget.

		:param active_label: Active label to remove.
		:type active_label: Active_QLabel
		:return: Method success.
		:rtype: bool
		"""

		if not active_label in self.__active_labels:
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' is not in the collection!".format(
			self.__class__.__name__, active_label))

		self.__active_labels.remove(active_label)
		return True

	def get_toggled_active_label(self):
		"""
		Returns the toggled **Active_QLabel** Widget.

		:return: Checked active label.
		:rtype: bool
		"""

		for active_label in self.__active_labels:
			if active_label.checked:
				return active_label

	def get_active_label_index(self, active_label):
		"""
		Returns given **Active_QLabel** Widget index.

		:param active_label: Active label to retrieve index.
		:type active_label: Active_QLabel
		:return: Active label index.
		:rtype: int
		"""

		return self.__active_labels.index(active_label)

	def get_active_label_from_index(self, index):
		"""
		Returns the **Active_QLabel** Widget from given index.

		:param index: Index.
		:type index: int
		:return: Active label.
		:rtype: Active_QLabel
		"""

		return self.__active_labels[index]

if __name__ == "__main__":
	import sys
	from PyQt4.QtGui import QGridLayout
	from PyQt4.QtGui import QPixmap
	from PyQt4.QtGui import QWidget

	from umbra.globals.ui_constants import UiConstants

	application = umbra.ui.common.get_application_instance()

	widget = QWidget()

	grid_layout = QGridLayout()
	widget.setLayout(grid_layout)

	active_label_a = Active_QLabel(widget, QPixmap(umbra.ui.common.get_resource_path(UiConstants.development_icon)),
									QPixmap(umbra.ui.common.get_resource_path(UiConstants.development_hover_icon)),
									QPixmap(umbra.ui.common.get_resource_path(UiConstants.development_active_icon)),
									checkable=True,
									checked=True)
	active_label_b = Active_QLabel(widget, QPixmap(umbra.ui.common.get_resource_path(UiConstants.preferences_icon)),
									QPixmap(umbra.ui.common.get_resource_path(UiConstants.preferences_hover_icon)),
									QPixmap(umbra.ui.common.get_resource_path(UiConstants.preferences_active_icon)),
									checkable=True,
									checked=False)
	active_label_c = Active_QLabel(widget, QPixmap(umbra.ui.common.get_resource_path(UiConstants.custom_layouts_icon)),
									QPixmap(umbra.ui.common.get_resource_path(UiConstants.custom_layouts_hover_icon)),
									QPixmap(umbra.ui.common.get_resource_path(UiConstants.custom_layouts_active_icon)),
									checkable=True,
									checked=False)
	active_label_d = Active_QLabel(widget, QPixmap(umbra.ui.common.get_resource_path(UiConstants.miscellaneous_icon)),
									QPixmap(umbra.ui.common.get_resource_path(UiConstants.miscellaneous_hover_icon)),
									QPixmap(umbra.ui.common.get_resource_path(UiConstants.miscellaneous_active_icon)),
									checkable=True,
									checked=False)
	for active_label in (active_label_a, active_label_b, active_label_c, active_label_d):
		grid_layout.addWidget(active_label)

	active_QLabelsCollection = Active_QLabelsCollection()
	for active_label in (active_label_a, active_label_b, active_label_c, active_label_d):
		active_QLabelsCollection.add_active_label(active_label)

	widget.show()
	widget.raise_()

	sys.exit(application.exec_())
