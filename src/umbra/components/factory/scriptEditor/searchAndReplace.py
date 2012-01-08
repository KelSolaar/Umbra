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

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import itertools
import logging
import os
from PyQt4.QtCore import QRegExp
from PyQt4.QtCore import QStringList
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QWidget

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.common
import foundations.exceptions
import foundations.ui.common
import umbra.ui.common
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

__all__ = ["LOGGER", "UI_FILE", "SearchAndReplace"]

LOGGER = logging.getLogger(Constants.logger)

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Search_And_Replace.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
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
	def __init__(self, parent, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(SearchAndReplace, self).__init__(parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__container = parent

		self.__maximumStoredPatterns = 15

		SearchAndReplace.__initializeUi(self)

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

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "maximumStoredPatterns"))

	@maximumStoredPatterns.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def maximumStoredPatterns(self):
		"""
		This method is the deleter method for **self.__maximumStoredPatterns** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "maximumStoredPatterns"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def show(self):
		"""
		This method reimplements the :meth:`QWidget.show` method.

		:return: Method success. ( Boolean )
		"""

		editor = self.__container.getCurrentEditor()
		if editor:
			selectedText = editor.textCursor().selectedText()
			selectedText and self.insertSearchPattern(selectedText)

		super(SearchAndReplace, self).show()
		self.raise_()
		self.Search_comboBox.setFocus()

		return True

	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		umbra.ui.common.setWindowDefaultIcon(self)

		self.Search_comboBox.setInsertPolicy(QComboBox.InsertAtTop)
		self.Replace_With_comboBox.setInsertPolicy(QComboBox.InsertAtTop)

		self.Wrap_Around_checkBox.setChecked(True)

		for widget in self.findChildren(QWidget, QRegExp(".*")):
			widget.keyPressEvent = functools.partial(_keyPressEvent, widget, self)

		recentSearchPatterns = self.__container.settings.getKey(self.__container.settingsSection,
																"recentSearchPatterns").toString().split(",")
		if recentSearchPatterns:
			for i in range(min(self.__maximumStoredPatterns, len(recentSearchPatterns))):
				self.Search_comboBox.addItem(recentSearchPatterns[i])

		recentReplaceWithPatterns = self.__container.settings.getKey(self.__container.settingsSection,
																	"recentReplaceWithPatterns").toString().split(",")
		if recentReplaceWithPatterns:
			for i in range(min(self.__maximumStoredPatterns, len(recentReplaceWithPatterns))):
				self.Replace_With_comboBox.addItem(recentReplaceWithPatterns[i])

		# Signals / Slots.
		self.Search_pushButton.clicked.connect(self.__Search_pushButton__clicked)
		self.Replace_pushButton.clicked.connect(self.__Replace_pushButton__clicked)
		self.Replace_All_pushButton.clicked.connect(self.__Replace_All_pushButton__clicked)
		self.Close_pushButton.clicked.connect(self.__Close_pushButton__clicked)

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
	def __storeRecentPatternsSettings(self, comboBox, settingsKey):
		"""
		This method stores given `QComboBox <http://doc.qt.nokia.com/qcombox.html>`_ class patterns.
		
		:param comboBox: QComboBox. ( QComboBox )
		:param settingsKey: Associated settings key. ( String )
		"""

		LOGGER.debug("> Storing '{0}' comboBox patterns in '{1}' settings key.".format(comboBox, settingsKey))
		self.__container.settings.setKey(self.__container.settingsSection,
										settingsKey,
										",".join((unicode(comboBox.itemText(i),
														Constants.encodingFormat,
														Constants.encodingError)
										for i in range(min(self.__maximumStoredPatterns, comboBox.count()))
										if comboBox.itemText(i))))

	@core.executionTrace
	def __storeRecentSearchPatternsSettings(self):
		"""
		This method stores recent **Search_comboBox** Widget patterns.
		"""

		self.__storeRecentPatternsSettings(self.Search_comboBox, "recentSearchPatterns")

	@core.executionTrace
	def __storeRecentReplaceWithPatternsSettings(self):
		"""
		This method stores recent **Replace_With_comboBox** Widget patterns.
		"""

		self.__storeRecentPatternsSettings(self.Replace_With_comboBox, "recentReplaceWithPatterns")

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __insertPattern(self, pattern, comboBox, settingsStorageMethod):
		"""
		This method inserts given pattern in the given :class:`QComboBox` class Widget.

		:param pattern: Search pattern. ( String )
		:param comboBox: Target comboBox. ( QComboBox )
		:param settingsStorageMethod: Patterns settings storage method. ( Object )
		"""

		if not pattern:
			return

		LOGGER.debug("> Inserting pattern '{0}' in '{1}' comboBox.".format(pattern, comboBox))

		patterns = itertools.chain([pattern], [comboBox.itemText(i) for i in range(comboBox.count())])
		comboBox.clear()
		comboBox.addItems(QStringList(foundations.common.orderedUniqify(patterns)))

		settingsStorageMethod()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def insertSearchPattern(self, pattern):
		"""
		This method inserts given pattern in the **Search_comboBox** Widget.

		:param pattern: Search pattern. ( String )
		:return: Method success. ( Boolean )
		"""

		self.__insertPattern(pattern, self.Search_comboBox, self.__storeRecentSearchPatternsSettings)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def insertReplaceWithPattern(self, pattern):
		"""
		This method inserts given pattern in the **Replace_With_comboBox** Widget.

		:param pattern: Search pattern. ( String )
		:return: Method success. ( Boolean )
		"""

		self.__insertPattern(pattern, self.Search_comboBox, self.__storeRecentReplaceWithPatternsSettings)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def search(self):
		"""
		This method searchs current Widget tab editor for search pattern.

		:return: Method success. ( Boolean )
		"""

		self.__storeRecentSearchPatternsSettings()

		editor = self.__container.getCurrentEditor()
		searchPattern = self.Search_comboBox.currentText()

		if not editor or not searchPattern:
			return

		settings = {"caseSensitive" : self.Case_Sensitive_checkBox.isChecked(),
					"wholeWord" : self.Whole_Word_checkBox.isChecked(),
					"regularExpressions" : self.Regular_Expressions_checkBox.isChecked(),
					"backwardSearch" : self.Backward_Search_checkBox.isChecked(),
					"wrapAround" : self.Wrap_Around_checkBox.isChecked()}

		LOGGER.debug("> 'Search' on '{0}' search pattern with '{1}' settings.".format(searchPattern, settings))

		return editor.search(searchPattern, **settings)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def replace(self):
		"""
		This method replaces current Widget tab editor current search pattern occurence with replacement pattern.

		:return: Method success. ( Boolean )
		"""

		self.__storeRecentReplaceWithPatternsSettings()

		editor = self.__container.getCurrentEditor()
		searchPattern = self.Search_comboBox.currentText()
		replacementPattern = self.Replace_With_comboBox.currentText()

		if not editor or not searchPattern:
			return

		settings = {"caseSensitive" : self.Case_Sensitive_checkBox.isChecked(),
					"wholeWord" : self.Whole_Word_checkBox.isChecked(),
					"regularExpressions" : self.Regular_Expressions_checkBox.isChecked(),
					"backwardSearch" : self.Backward_Search_checkBox.isChecked(),
					"wrapAround" : self.Wrap_Around_checkBox.isChecked()}


		LOGGER.debug("> 'Replace' on search '{0}' pattern, '{1}' replacement pattern with '{2}' settings.".format(
		searchPattern, replacementPattern, settings))

		return editor.replace(searchPattern, replacementPattern, **settings)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def replaceAll(self):
		"""
		This method replaces current Widget tab editor search pattern occurences with replacement pattern.

		:return: Method success. ( Boolean )
		"""

		self.__storeRecentReplaceWithPatternsSettings()

		editor = self.__container.getCurrentEditor()
		searchPattern = self.Search_comboBox.currentText()
		replacementPattern = self.Replace_With_comboBox.currentText()

		if not editor or not searchPattern:
			return

		settings = {"caseSensitive" : self.Case_Sensitive_checkBox.isChecked(),
					"wholeWord" : self.Whole_Word_checkBox.isChecked(),
					"regularExpressions" : self.Regular_Expressions_checkBox.isChecked(),
					"backwardSearch" : False,
					"wrapAround" : False}

		LOGGER.debug("> 'Replace All' on search '{0}' pattern, '{1}' replacement pattern with '{2}' settings.".format(
		searchPattern, replacementPattern, settings))

		return editor.replaceAll(searchPattern, replacementPattern, **settings)
