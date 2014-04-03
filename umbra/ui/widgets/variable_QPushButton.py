#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**variable_QPushButton.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`Variable_QPushButton` class.

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
from PyQt4.QtGui import QPalette
from PyQt4.QtGui import QPushButton

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
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

__all__ = ["LOGGER", "Variable_QPushButton"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Variable_QPushButton(QPushButton):
	"""
	Defines a `QPushButton <http://doc.qt.nokia.com/qpushbutton.html>`_ subclass providing
	a button with different colors and labels depending on its clicked state.
	"""

	def __init__(self,
				parent=None,
				state=True,
				colors=(QColor(240, 240, 240),
				QColor(160, 160, 160)),
				labels=("Yes", "No")):
		"""
		Initializes the class.

		:param parent: Widget parent.
		:type parent: QObject
		:param state: Current button state.
		:type state: bool
		:param colors: Button colors.
		:type colors: tuple
		:param labels: Button texts.
		:type labels: tuple
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QPushButton.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__state = None
		self.state = state

		self.__colors = None
		self.colors = colors

		self.__labels = None
		self.labels = labels

		# Initializing the button
		self.setCheckable(True)
		if self.__state:
			self.__setTrueState()
		else:
			self.__setFalseState()

		# Signals / Slots.
		self.clicked.connect(self.__variable_QPushButton__clicked)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def state(self):
		"""
		Property for **self.__state** attribute.

		:return: self.__state.
		:rtype: bool
		"""

		return self.__state

	@state.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def state(self, value):
		"""
		Setter for **self.__state** attribute.

		:param value: Attribute value.
		:type value: bool
		"""

		if value is not None:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("state", value)
		self.__state = value

	@state.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def state(self):
		"""
		Deleter for **self.__state** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "state"))

	@property
	def colors(self):
		"""
		Property for **self.__colors** attribute.

		:return: self.__colors.
		:rtype: tuple
		"""

		return self.__colors

	@colors.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def colors(self, value):
		"""
		Setter for **self.__colors** attribute.

		:param value: Attribute value.
		:type value: tuple
		"""
		if value is not None:
			assert type(value) is tuple, "'{0}' attribute: '{1}' type is not 'tuple'!".format("colors", value)
			assert len(value) == 2, "'{0}' attribute: '{1}' length should be '2'!".format("colors", value)
			for index in range(len(value)):
				assert type(value[index]) is QColor, "'{0}' attribute element '{1}': '{2}' type is not 'QColor'!".format(
				"colors", index, value)
		self.__colors = value

	@colors.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def colors(self):
		"""
		Deleter for **self.__colors** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "colors"))

	@property
	def labels(self):
		"""
		Property for **self.__labels** attribute.

		:return: self.__labels.
		:rtype: tuple
		"""

		return self.__labels

	@labels.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def labels(self, value):
		"""
		Setter for **self.__labels** attribute.

		:param value: Attribute value.
		:type value: tuple
		"""
		if value is not None:
			assert type(value) is tuple, "'{0}' attribute: '{1}' type is not 'tuple'!".format("labels", value)
			assert len(value) == 2, "'{0}' attribute: '{1}' length should be '2'!".format("labels", value)
			for index in range(len(value)):
				assert type(value[index]) is unicode, \
				"'{0}' attribute element '{1}': '{2}' type is not 'unicode'!".format("labels", index, value)
		self.__labels = value

	@labels.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def labels(self):
		"""
		Deleter for **self.__labels** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "labels"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __variable_QPushButton__clicked(self, checked):
		"""
		Defines the slot triggered by a **Variable_QPushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		if self.__state:
			self.__setFalseState()
		else:
			self.__setTrueState()

	def __setTrueState(self):
		"""
		Sets the variable button true state.
		"""

		LOGGER.debug("> Setting variable QPushButton() to 'True' state.")
		self.__state = True

		palette = QPalette()
		palette.setColor(QPalette.Button, foundations.common.getFirstItem(self.__colors))
		self.setPalette(palette)

		self.setChecked(True)
		self.setText(foundations.common.getFirstItem(self.__labels))

	def __setFalseState(self):
		"""
		Sets the variable QPushButton true state.
		"""

		LOGGER.debug("> Setting variable QPushButton() to 'False' state.")

		self.__state = False

		palette = QPalette()
		palette.setColor(QPalette.Button, self.__colors[1])
		self.setPalette(palette)

		self.setChecked(False)
		self.setText(self.__labels[1])

if __name__ == "__main__":
	import sys
	from PyQt4.QtGui import QGridLayout
	from PyQt4.QtGui import QWidget

	import umbra.ui.common

	application = umbra.ui.common.getApplicationInstance()

	widget = QWidget()

	gridLayout = QGridLayout()
	widget.setLayout(gridLayout)

	variable_QPushButtonA = Variable_QPushButton()
	variable_QPushButtonB = Variable_QPushButton(labels=("-", "+"))
	variable_QPushButtonC = Variable_QPushButton(colors=(QColor(120, 240, 120), QColor(240, 120, 120)))

	for variable_QPushButton in (variable_QPushButtonA, variable_QPushButtonB, variable_QPushButtonC):
		gridLayout.addWidget(variable_QPushButton)

	widget.show()
	widget.raise_()

	sys.exit(application.exec_())

