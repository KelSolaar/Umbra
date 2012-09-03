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
import logging
import os
from PyQt4.QtCore import QChar
from PyQt4.QtCore import QObject
from PyQt4.QtCore import QEvent
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QComboBox

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.common
import foundations.exceptions
import foundations.ui.common
import foundations.strings as strings
import umbra.ui.common
from umbra.components.factory.scriptEditor.models import PatternsModel
from umbra.components.factory.scriptEditor.nodes import PatternNode
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
class ValidationFilter(QObject):
	"""
	This class is a `QObject <http://doc.qt.nokia.com/qobject.html>`_ subclass used as an event filter
	for the :class:`SearchAndReplace` class.
	"""

	# @core.executionTrace
	def eventFilter(self, object, event):
		"""
		This method reimplements the **QObject.eventFilter** method.
		
		:param object: Object. ( QObject )
		:param event: Event. ( QEvent )
		:return: Event filtered. ( Boolean )
		"""

		if event.type() == QEvent.KeyPress:
			if event.key() in (Qt.Key_Enter, Qt.Key_Return):
				object.search()
			elif event.key() in (Qt.Key_Escape,):
				object.close()
			return True
		else:
			return QObject.eventFilter(self, object, event)

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

		self.__searchPatternsModel = None
		self.__replaceWithPatternsModel = None

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
	def show(self):
		"""
		This method reimplements the :meth:`QWidget.show` method.
		"""

		selectedText = self.__container.getCurrentEditor().getSelectedText()
		selectedText and self.insertPattern(selectedText, self.__searchPatternsModel)
		self.Search_comboBox.lineEdit().selectAll()
		self.Search_comboBox.setFocus()

		super(SearchAndReplace, self).show()
		self.raise_()

	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		umbra.ui.common.setWindowDefaultIcon(self)

		for model, settingsKey, comboBox in \
		(("_SearchAndReplace__searchPatternsModel", "recentSearchPatterns", self.Search_comboBox),
		("_SearchAndReplace__replaceWithPatternsModel", "recentReplaceWithPatterns", self.Replace_With_comboBox)):
			self.__dict__[model] = PatternsModel(defaultNode=PatternNode)
			patterns = foundations.common.orderedUniqify([strings.encode(pattern) for pattern in \
														self.__container.settings.getKey(self.__container.settingsSection,
																						settingsKey).toStringList()])
			[PatternNode(parent=self.__dict__[model].rootNode, name=pattern) \
			for pattern in patterns[:self.__maximumStoredPatterns]]
			comboBox.setInsertPolicy(QComboBox.InsertAtTop)
			comboBox.setModel(self.__dict__[model])

			comboBox.completer().setCaseSensitivity(Qt.CaseSensitive)

			# Signals / Slots.
			self.__dict__[model].patternInserted.connect(
			functools.partial(self.__patternsModel__patternInserted, settingsKey, comboBox))

		self.Wrap_Around_checkBox.setChecked(True)

		self.installEventFilter(ValidationFilter(self))

		# Signals / Slots.
		self.Search_pushButton.clicked.connect(self.__Search_pushButton__clicked)
		self.Replace_pushButton.clicked.connect(self.__Replace_pushButton__clicked)
		self.Replace_All_pushButton.clicked.connect(self.__Replace_All_pushButton__clicked)
		self.Close_pushButton.clicked.connect(self.__Close_pushButton__clicked)

	@core.executionTrace
	def __patternsModel__patternInserted(self, settingsKey, comboBox, index):
		"""
		This method is triggered when a pattern has been inserted into a patterns Model.

		:param settingsKey: Pattern Model settings key. ( String )
		:param comboBox: Pattern Model attached comboBox. ( QComboBox )
		:param index: Inserted pattern index. ( QModelIndex )
		"""

		patternsModel = self.sender()

		LOGGER.debug("> Storing '{0}' model patterns in '{1}' settings key.".format(patternsModel, settingsKey))

		self.__container.settings.setKey(self.__container.settingsSection,
										settingsKey,
										[patternNode.name for patternNode in \
										patternsModel.rootNode.children[:self.maximumStoredPatterns]])
		comboBox.setCurrentIndex(index.row())

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
	def __getSettings(self):
		"""
		This method returns the current search and replace settings.

		:return: Settings. ( Dictionary )
		"""

		return {"caseSensitive" : self.Case_Sensitive_checkBox.isChecked(),
				"wholeWord" : self.Whole_Word_checkBox.isChecked(),
				"regularExpressions" : self.Regular_Expressions_checkBox.isChecked(),
				"backwardSearch" : self.Backward_Search_checkBox.isChecked(),
				"wrapAround" : self.Wrap_Around_checkBox.isChecked()}

	@staticmethod
	@core.executionTrace
	def insertPattern(pattern, model, index=0):
		"""
		This definition inserts given pattern into given Model.
	
		:param pattern: Pattern. ( String )
		:param model: Model. ( PatternsModel )
		:param index: Insertion indes. ( Integer )
		:return: Method success. ( Boolean )
		"""

		if not pattern:
			return False

		pattern = pattern.replace(QChar(QChar.ParagraphSeparator), QString("\n"))
		pattern = foundations.common.getFirstItem(strings.encode(pattern).split("\n"))

		model.insertPattern(strings.encode(pattern), index)

		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def search(self):
		"""
		This method searchs current editor Widget for search pattern.

		:return: Method success. ( Boolean )
		"""

		editor = self.__container.getCurrentEditor()
		searchPattern = self.Search_comboBox.currentText()
		replacementPattern = self.Replace_With_comboBox.currentText()

		if not editor or not searchPattern:
			return False

		self.insertPattern(searchPattern, self.__searchPatternsModel)
		self.insertPattern(replacementPattern, self.__replaceWithPatternsModel)

		settings = self.__getSettings()

		LOGGER.debug("> 'Search' on '{0}' search pattern with '{1}' settings.".format(searchPattern, settings))

		return editor.search(searchPattern, **settings)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def replace(self):
		"""
		This method replaces current editor Widget current search pattern occurence with replacement pattern.

		:return: Method success. ( Boolean )
		"""

		editor = self.__container.getCurrentEditor()
		searchPattern = self.Search_comboBox.currentText()
		replacementPattern = self.Replace_With_comboBox.currentText()

		if not editor or not searchPattern:
			return False

		self.insertPattern(searchPattern, self.__searchPatternsModel)
		self.insertPattern(replacementPattern, self.__replaceWithPatternsModel)

		settings = self.__getSettings()

		LOGGER.debug("> 'Replace' on search '{0}' pattern, '{1}' replacement pattern with '{2}' settings.".format(
		searchPattern, replacementPattern, settings))

		return editor.replace(searchPattern, replacementPattern, **settings)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def replaceAll(self):
		"""
		This method replaces current editor Widget search pattern occurences with replacement pattern.

		:return: Method success. ( Boolean )
		"""

		editor = self.__container.getCurrentEditor()
		searchPattern = self.Search_comboBox.currentText()
		replacementPattern = self.Replace_With_comboBox.currentText()

		if not editor or not searchPattern:
			return False

		self.insertPattern(searchPattern, self.__searchPatternsModel)
		self.insertPattern(replacementPattern, self.__replaceWithPatternsModel)

		settings = self.__getSettings()
		settings.update({"backwardSearch" : False,
						"wrapAround" : False})

		LOGGER.debug("> 'Replace All' on search '{0}' pattern, '{1}' replacement pattern with '{2}' settings.".format(
		searchPattern, replacementPattern, settings))

		return editor.replaceAll(searchPattern, replacementPattern, **settings)
