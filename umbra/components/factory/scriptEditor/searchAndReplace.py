#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**searchAndReplace.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`SearchAndReplace` class.

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
import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.ui.common
import foundations.verbose
import umbra.ui.common
from umbra.components.factory.scriptEditor.models import PatternsModel
from umbra.components.factory.scriptEditor.nodes import PatternNode

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "UI_FILE", "SearchAndReplace"]

LOGGER = foundations.verbose.installLogger()

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Search_And_Replace.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ValidationFilter(QObject):
	"""
	Defines a `QObject <http://doc.qt.nokia.com/qobject.html>`_ subclass used as an event filter
	for the :class:`SearchAndReplace` class.
	"""

	def eventFilter(self, object, event):
		"""
		Reimplements the **QObject.eventFilter** method.

		:param object: Object.
		:type object: QObject
		:param event: Event.
		:type event: QEvent
		:return: Event filtered.
		:rtype: bool
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
	Defines the default search and replace dialog used by the **ScriptEditor** Component.
	"""

	def __init__(self, parent, *args, **kwargs):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
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
	def searchPatternsModel(self):
		"""
		Property for **self.__searchPatternsModel** attribute.

		:return: self.__searchPatternsModel.
		:rtype: PatternsModel
		"""

		return self.__searchPatternsModel

	@searchPatternsModel.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def searchPatternsModel(self, value):
		"""
		Setter for **self.__searchPatternsModel** attribute.

		:param value: Attribute value.
		:type value: PatternsModel
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "searchPatternsModel"))

	@searchPatternsModel.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def searchPatternsModel(self):
		"""
		Deleter for **self.__searchPatternsModel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchPatternsModel"))

	@property
	def replaceWithPatternsModel(self):
		"""
		Property for **self.__replaceWithPatternsModel** attribute.

		:return: self.__replaceWithPatternsModel.
		:rtype: PatternsModel
		"""

		return self.__replaceWithPatternsModel

	@replaceWithPatternsModel.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def replaceWithPatternsModel(self, value):
		"""
		Setter for **self.__replaceWithPatternsModel** attribute.

		:param value: Attribute value.
		:type value: PatternsModel
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "replaceWithPatternsModel"))

	@replaceWithPatternsModel.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def replaceWithPatternsModel(self):
		"""
		Deleter for **self.__replaceWithPatternsModel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "replaceWithPatternsModel"))

	@property
	def maximumStoredPatterns(self):
		"""
		Property for **self.__maximumStoredPatterns** attribute.

		:return: self.__maximumStoredPatterns.
		:rtype: int
		"""

		return self.__maximumStoredPatterns

	@maximumStoredPatterns.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def maximumStoredPatterns(self, value):
		"""
		Setter for **self.__maximumStoredPatterns** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "maximumStoredPatterns"))

	@maximumStoredPatterns.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def maximumStoredPatterns(self):
		"""
		Deleter for **self.__maximumStoredPatterns** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "maximumStoredPatterns"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def show(self):
		"""
		Reimplements the :meth:`QWidget.show` method.
		"""

		selectedText = self.__container.getCurrentEditor().getSelectedText()
		selectedText and self.insertPattern(selectedText, self.__searchPatternsModel)
		self.Search_comboBox.lineEdit().selectAll()
		self.Search_comboBox.setFocus()

		super(SearchAndReplace, self).show()
		self.raise_()

	def __initializeUi(self):
		"""
		Initializes the Widget ui.
		"""

		umbra.ui.common.setWindowDefaultIcon(self)

		for model, settingsKey, comboBox in \
		(("_SearchAndReplace__searchPatternsModel", "recentSearchPatterns", self.Search_comboBox),
		("_SearchAndReplace__replaceWithPatternsModel", "recentReplaceWithPatterns", self.Replace_With_comboBox)):
			self.__dict__[model] = PatternsModel()
			patterns = foundations.common.orderedUniqify([foundations.strings.toString(pattern) for pattern in \
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

	def __patternsModel__patternInserted(self, settingsKey, comboBox, index):
		"""
		Defines the slot triggered by a pattern when inserted into a patterns Model.

		:param settingsKey: Pattern Model settings key.
		:type settingsKey: unicode
		:param comboBox: Pattern Model attached comboBox.
		:type comboBox: QComboBox
		:param index: Inserted pattern index.
		:type index: QModelIndex
		"""

		patternsModel = self.sender()

		LOGGER.debug("> Storing '{0}' model patterns in '{1}' settings key.".format(patternsModel, settingsKey))

		self.__container.settings.setKey(self.__container.settingsSection,
										settingsKey,
										[patternNode.name for patternNode in \
										patternsModel.rootNode.children[:self.maximumStoredPatterns]])
		comboBox.setCurrentIndex(index.row())

	def __Search_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Search_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.search()

	def __Replace_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Replace_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.replace()

	def __Replace_All_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Replace_All_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.replaceAll()

	def __Close_pushButton__clicked(self, checked):
		"""
		Defines the slot triggered by **Close_pushButton** Widget when clicked.

		:param checked: Checked state.
		:type checked: bool
		"""

		self.close()

	def __getSettings(self):
		"""
		Returns the current search and replace settings.

		:return: Settings.
		:rtype: dict
		"""

		return {"caseSensitive" : self.Case_Sensitive_checkBox.isChecked(),
				"wholeWord" : self.Whole_Word_checkBox.isChecked(),
				"regularExpressions" : self.Regular_Expressions_checkBox.isChecked(),
				"backwardSearch" : self.Backward_Search_checkBox.isChecked(),
				"wrapAround" : self.Wrap_Around_checkBox.isChecked()}

	@staticmethod
	def insertPattern(pattern, model, index=0):
		"""
		Inserts given pattern into given Model.

		:param pattern: Pattern.
		:type pattern: unicode
		:param model: Model.
		:type model: PatternsModel
		:param index: Insertion indes.
		:type index: int
		:return: Method success.
		:rtype: bool
		"""

		if not pattern:
			return False

		pattern = pattern.replace(QChar(QChar.ParagraphSeparator), QString("\n"))
		pattern = foundations.common.getFirstItem(foundations.strings.toString(pattern).split("\n"))

		model.insertPattern(foundations.strings.toString(pattern), index)

		return True

	def search(self):
		"""
		Searchs current editor Widget for search pattern.

		:return: Method success.
		:rtype: bool
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

	def replace(self):
		"""
		Replaces current editor Widget current search pattern occurence with replacement pattern.

		:return: Method success.
		:rtype: bool
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

	def replaceAll(self):
		"""
		Replaces current editor Widget search pattern occurrences with replacement pattern.

		:return: Method success.
		:rtype: bool
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
