#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**searchInFiles.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`SearchInFiles` class.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import logging
import os
from PyQt4.QtCore import QRegExp
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QWidget

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.ui.common
import umbra.components.factory.scriptEditor.searchAndReplace
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

__all__ = ["LOGGER", "UI_FILE", "SearchInFiles"]

LOGGER = logging.getLogger(Constants.logger)

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Search_In_Files.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class SearchInFiles(foundations.ui.common.QWidgetFactory(uiFile=UI_FILE)):
	"""
	This class defines search and replace in files dialog used by the **ScriptEditor** Component. 
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

		super(SearchInFiles, self).__init__(parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__container = parent

		SearchInFiles.__initializeUi(self)

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
	def searchPatternsModel(self):
		"""
		This method is the property for **self.__searchPatternsModel** attribute.

		:return: self.__searchPatternsModel. ( PatternsModel )
		"""

		return self.__searchPatternsModel

	@searchPatternsModel.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchPatternsModel(self, value):
		"""
		This method is the setter method for **self.__searchPatternsModel** attribute.

		:param value: Attribute value. ( PatternsModel )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "searchPatternsModel"))

	@searchPatternsModel.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchPatternsModel(self):
		"""
		This method is the deleter method for **self.__searchPatternsModel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchPatternsModel"))

	@property
	def replaceWithPatternsModel(self):
		"""
		This method is the property for **self.__replaceWithPatternsModel** attribute.

		:return: self.__replaceWithPatternsModel. ( PatternsModel )
		"""

		return self.__replaceWithPatternsModel

	@replaceWithPatternsModel.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def replaceWithPatternsModel(self, value):
		"""
		This method is the setter method for **self.__replaceWithPatternsModel** attribute.

		:param value: Attribute value. ( PatternsModel )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "replaceWithPatternsModel"))

	@replaceWithPatternsModel.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def replaceWithPatternsModel(self):
		"""
		This method is the deleter method for **self.__replaceWithPatternsModel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "replaceWithPatternsModel"))

	#******************************************************************************************************************
	#***	Class methods
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def show(self):
		"""
		This method reimplements the :meth:`QWidget.show` method.

		:return: Method success. ( Boolean )
		"""

		umbra.components.factory.scriptEditor.searchAndReplace._insertEditorSelectTextInModel(
		self.__container.getCurrentEditor(), self.__searchPatternsModel)

		super(SearchInFiles, self).show()
		self.raise_()
		self.Search_comboBox.setFocus()

		return True

	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		umbra.ui.common.setWindowDefaultIcon(self)

		self.__searchPatternsModel = self.__container.searchAndReplace.searchPatternsModel
		self.Search_comboBox.setModel(self.__container.searchAndReplace.searchPatternsModel)
		self.Search_comboBox.setInsertPolicy(QComboBox.InsertAtTop)

		self.__replaceWithPatternsModel = self.__container.searchAndReplace.replaceWithPatternsModel
		self.Replace_With_comboBox.setModel(self.__container.searchAndReplace.replaceWithPatternsModel)
		self.Replace_With_comboBox.setInsertPolicy(QComboBox.InsertAtTop)

		for widget in self.findChildren(QWidget, QRegExp(".*")):
			widget.keyPressEvent = functools.partial(
			umbra.components.factory.scriptEditor.searchAndReplace._keyPressEvent, widget, self)

		# Signals / Slots.
		self.__searchPatternsModel.dataChanged.connect(self.__searchPatternsModel__dataChanged)
		self.Search_pushButton.clicked.connect(self.__Search_pushButton__clicked)
		self.Replace_pushButton.clicked.connect(self.__Replace_pushButton__clicked)
		self.Close_pushButton.clicked.connect(self.__Close_pushButton__clicked)

	@core.executionTrace
	def __searchPatternsModel__dataChanged(self, startIndex, endIndex):
		"""
		This method is triggered when the **searchPatternsModel** Model data has changed.

		:param startIndex: Edited item starting QModelIndex. ( QModelIndex )
		:param endIndex: Edited item ending QModelIndex. ( QModelIndex )
		"""

		self.Search_comboBox.setCurrentIndex(endIndex.row())

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
	def __Close_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Close_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.close()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def search(self):
		"""
		This method searchs user defined files for search pattern.

		:return: Method success. ( Boolean )
		"""

		print "Search!"
#		self.__storeRecentSearchPatternsSettings()
#
#		editor = self.__container.getCurrentEditor()
#		searchPattern = self.Search_comboBox.currentText()
#
#		if not editor or not searchPattern:
#			return
#
#		settings = {"caseSensitive" : self.Case_Sensitive_checkBox.isChecked(),
#					"wholeWord" : self.Whole_Word_checkBox.isChecked(),
#					"regularExpressions" : self.Regular_Expressions_checkBox.isChecked(),
#					"backwardSearch" : self.Backward_Search_checkBox.isChecked(),
#					"wrapAround" : self.Wrap_Around_checkBox.isChecked()}
#
#		LOGGER.debug("> 'Search' on '{0}' search pattern with '{1}' settings.".format(searchPattern, settings))
#
#		return editor.search(searchPattern, **settings)
#
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def replace(self):
		"""
		This method replaces user defined files earch pattern occurences with replacement pattern.
		
		:return: Method success. ( Boolean )
		"""

		print "Replace!"
#		self.__storeRecentReplaceWithPatternsSettings()
#
#		editor = self.__container.getCurrentEditor()
#		searchPattern = self.Search_comboBox.currentText()
#		replacementPattern = self.Replace_With_comboBox.currentText()
#
#		if not editor or not searchPattern:
#			return
#
#		settings = {"caseSensitive" : self.Case_Sensitive_checkBox.isChecked(),
#					"wholeWord" : self.Whole_Word_checkBox.isChecked(),
#					"regularExpressions" : self.Regular_Expressions_checkBox.isChecked(),
#					"backwardSearch" : self.Backward_Search_checkBox.isChecked(),
#					"wrapAround" : self.Wrap_Around_checkBox.isChecked()}
#
#
#		LOGGER.debug("> 'Replace' on search '{0}' pattern, '{1}' replacement pattern with '{2}' settings.".format(
#		searchPattern, replacementPattern, settings))
#
#		return editor.replace(searchPattern, replacementPattern, **settings)
#
