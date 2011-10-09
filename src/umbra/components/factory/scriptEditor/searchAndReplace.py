#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**searchAndReplace.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`SearchAndReplace` class.

**Others:**

"""

#***********************************************************************************************
#***	External imports.
#***********************************************************************************************
import functools
import logging
import os
import sys
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.ui.common
import umbra.ui.common
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

__all__ = ["LOGGER", "UI_FILE", "SearchAndReplace"]

LOGGER = logging.getLogger(Constants.logger)

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Search_And_Replace.ui")

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
def _keyPressEvent(self, container, event):
	"""
	This definition reimplements the :class:`SearchAndReplace` widgets **keyPressEvent** method.

	:param container: Container. ( QObject )
	:param event: Event. ( QEvent )
	"""

	self.__class__.keyPressEvent(self, event)
	if event.key() in (Qt.Key_Enter, Qt.Key_Return):
		container.search()
	elif event.key() in (Qt.Key_Escape,):
		container.close()

class SearchAndReplace(foundations.ui.common.QWidgetFactory(uiFile=UI_FILE)):
	"""
	This class defines the default search and replace dialog used by the **ScriptEditor** Component. 
	"""

	@core.executionTrace
	def __init__(self, parent=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Arguments. ( \* )
		"""

		if not parent:
			raise umbra.exceptions.WidgetInitializationError("'{0}' Widget initialization requires a parent Widget!".format(self.__class__.__name__))

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(SearchAndReplace, self).__init__(parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__container = parent

		self.__maximumStoredPatterns = 15

		SearchAndReplace.__initializeUi(self)

	#***********************************************************************************************
	#***	Attributes properties.
	#***********************************************************************************************
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

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("container"))

	@container.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("container"))

	@property
	def maximumStoredPatterns(self):
		"""
		This method is the property for **self.__maximumStoredPatterns** attribute.

		:return: self.__maximumStoredPatterns. ( Integer )
		"""

		return self.__maximumStoredPatterns

	@maximumStoredPatterns.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumStoredPatterns(self, value):
		"""
		This method is the setter method for **self.__maximumStoredPatterns** attribute.

		:param value: Attribute value. ( Integer )
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is read only!".format("maximumStoredPatterns"))

	@maximumStoredPatterns.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumStoredPatterns(self):
		"""
		This method is the deleter method for **self.__maximumStoredPatterns** attribute.
		"""

		raise foundations.exceptions.ProgrammingError("'{0}' attribute is not deletable!".format("maximumStoredPatterns"))

	#***********************************************************************************************
	#***	Class methods.
	#***********************************************************************************************
	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		umbra.ui.common.setWindowDefaultIcon(self)

		self.Wrap_Around_checkBox.setChecked(True)

		for widget in self.findChildren(QWidget, QRegExp(".*")):
			widget.keyPressEvent = functools.partial(_keyPressEvent, widget, self)

		recentSearchPatterns = self.__container.settings.getKey(self.__container.settingsSection, "recentSearchPatterns").toString().split(",")
		if recentSearchPatterns:
			for i in range(min(self.__maximumStoredPatterns, len(recentSearchPatterns))):
				self.Search_comboBox.addItem(recentSearchPatterns[i])

		recentReplaceWithPatterns = self.__container.settings.getKey(self.__container.settingsSection, "recentReplaceWithPatterns").toString().split(",")
		if recentReplaceWithPatterns:
			for i in range(min(self.__maximumStoredPatterns, len(recentReplaceWithPatterns))):
				self.Search_comboBox.addItem(recentReplaceWithPatterns[i])

		# Signals / Slots.
		self.Search_pushButton.clicked.connect(self.__Search_pushButton__clicked)
		self.Replace_pushButton.clicked.connect(self.__Replace_pushButton__clicked)
		self.Replace_All_pushButton.clicked.connect(self.__Replace_All_pushButton__clicked)
		self.Close_pushButton.clicked.connect(self.__Close_pushButton__clicked)

	@core.executionTrace
	def __storeRecentPatterns(self, comboBox, settingsKey):
		"""
		This method stores provided :class:`QComboBox` patterns.
		
		:param comboBox: QComboBox. ( QComboBox )
		:param settingsKey: Associated settings key. ( String )
		"""

		currentText = comboBox.currentText()
		if currentText:
			isNotRegistered = True
			for i in range(comboBox.count()):
				if comboBox.itemText(i) == currentText:
					isNotRegistered = False
					break
			isNotRegistered and comboBox.insertItem(0, currentText)

		self.__container.settings.setKey(self.__container.settingsSection, settingsKey, ",".join((str(comboBox.itemText(i)) for i in range(min(self.__maximumStoredPatterns, comboBox.count())) if comboBox.itemText(i))))

	@core.executionTrace
	def __storeRecentSearchPatterns(self):
		"""
		This method stores recent **Search_comboBox** Widget patterns.
		"""

		self.__storeRecentPatterns(self.Search_comboBox, "recentSearchPatterns")

	@core.executionTrace
	def __storeRecentReplaceWithPatterns(self):
		"""
		This method stores recent **Replace_With_comboBox** Widget patterns.
		"""

		self.__storeRecentPatterns(self.Replace_With_comboBox, "recentReplaceWithPatterns")

	@core.executionTrace
	def __Search_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Search_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.search()

	@core.executionTrace
	def __Replace_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Replace_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.replace()

	@core.executionTrace
	def __Replace_All_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Replace_All_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.replaceAll()

	@core.executionTrace
	def __Close_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Close_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.close()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def show(self):
		"""
		This method shows the Widget.

		:return: Method success. ( Boolean )
		"""

		super(SearchAndReplace, self).show()
		self.raise_()
		self.Search_comboBox.setFocus()

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def search(self):
		"""
		This method searchs current widget tab editor for search pattern.

		:return: Method success. ( Boolean )
		"""

		self.__storeRecentSearchPatterns()

		editor = self.__container.getCurrentEditor()
		searchPattern = self.Search_comboBox.currentText()

		if not editor or not searchPattern:
			return

		return editor.search(searchPattern, **{"caseSensitive" : self.Case_Sensitive_checkBox.isChecked(),
												"wholeWord" : self.Whole_Word_checkBox.isChecked(),
												"regularExpressions" : self.Regular_Expressions_checkBox.isChecked(),
												"backwardSearch" : self.Backward_Search_checkBox.isChecked(),
												"wrapAround" : self.Wrap_Around_checkBox.isChecked()})

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def replace(self):
		"""
		This method replaces current widget tab editor current search pattern occurence with replacement pattern.

		:return: Method success. ( Boolean )
		"""

		self.__storeRecentReplaceWithPatterns()

		editor = self.__container.getCurrentEditor()
		searchPattern = self.Search_comboBox.currentText()
		replacementPattern = self.Replace_With_comboBox.currentText()

		if not editor or not searchPattern:
			return

		return editor.replace(searchPattern, replacementPattern, **{"caseSensitive" : self.Case_Sensitive_checkBox.isChecked(),
																	"wholeWord" : self.Whole_Word_checkBox.isChecked(),
																	"regularExpressions" : self.Regular_Expressions_checkBox.isChecked(),
																	"backwardSearch" : self.Backward_Search_checkBox.isChecked(),
																	"wrapAround" : self.Wrap_Around_checkBox.isChecked()})

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def replaceAll(self):
		"""
		This method replaces current widget tab editor search pattern occurences with replacement pattern.

		:return: Method success. ( Boolean )
		"""

		self.__storeRecentReplaceWithPatterns()

		editor = self.__container.getCurrentEditor()
		searchPattern = self.Search_comboBox.currentText()
		replacementPattern = self.Replace_With_comboBox.currentText()

		if not editor or not searchPattern:
			return

		return editor.replaceAll(searchPattern, replacementPattern, **{"caseSensitive" : self.Case_Sensitive_checkBox.isChecked(),
																		"wholeWord" : self.Whole_Word_checkBox.isChecked(),
																		"regularExpressions" : self.Regular_Expressions_checkBox.isChecked(),
																		"backwardSearch" : False,
																		"wrapAround" : True})
