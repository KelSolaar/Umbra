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
from collections import OrderedDict
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextDocument

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.cache
import foundations.core as core
import foundations.exceptions
import foundations.strings as strings
import foundations.ui.common
import umbra.ui.common
import umbra.ui.nodes
from foundations.io import File
from umbra.components.factory.scriptEditor.models import SearchResultsModel
from umbra.components.factory.scriptEditor.nodes import ReplaceResultNode
from umbra.components.factory.scriptEditor.nodes import SearchFileNode
from umbra.components.factory.scriptEditor.nodes import SearchOccurenceNode
from umbra.components.factory.scriptEditor.searchAndReplace import SearchAndReplace
from umbra.components.factory.scriptEditor.searchAndReplace import ValidationFilter
from umbra.components.factory.scriptEditor.views import SearchResults_QTreeView
from umbra.components.factory.scriptEditor.workers import CacheData
from umbra.components.factory.scriptEditor.workers import Search_worker
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals
from umbra.ui.delegates import RichText_QStyledItemDelegate
from umbra.ui.widgets.search_QLineEdit import Search_QLineEdit

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
		self.__container = self.__scriptEditor = parent

		self.__filesCache = foundations.cache.Cache()

		self.__searchPatternsModel = None
		self.__replaceWithPatternsModel = None

		self.__model = None
		self.__view = None
		self.__delegate = None

		self.__locations = OrderedDict([("Add Directory ...", "directory"),
								("Add File ...", "file"),
								("Add Opened Files", "editors"),
								("Add Include Filter", "includeFilter"),
								("Add Exclude Filter", "excludeFilter")])
		self.__locationsMenu = None

		self.__defaultFilterIn = "*.txt"
		self.__filtersInFormat = "{0}"
		self.__defaultFilterOut = "*.txt"
		self.__filtersOutFormat = "!{0}"
		self.__defaultTarget = "Opened Files"
		self.__targetsFormat = "<{0}>"

		self.__defaultLineNumberWidth = 6
		self.__defaultLineColor = QColor(144, 144, 144)

		self.__searchWorkerThread = None

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
	def scriptEditor(self):
		"""
		This method is the property for **self.__scriptEditor** attribute.

		:return: self.__scriptEditor. ( QWidget )
		"""

		return self.__scriptEditor

	@scriptEditor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def scriptEditor(self, value):
		"""
		This method is the setter method for **self.__scriptEditor** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "scriptEditor"))

	@scriptEditor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def scriptEditor(self):
		"""
		This method is the deleter method for **self.__scriptEditor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "scriptEditor"))

	@property
	def filesCache(self):
		"""
		This method is the property for **self.__filesCache** attribute.

		:return: self.__filesCache. ( Cache )
		"""

		return self.__filesCache

	@filesCache.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def filesCache(self, value):
		"""
		This method is the setter method for **self.__filesCache** attribute.

		:param value: Attribute value. ( Cache )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "filesCache"))

	@filesCache.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def filesCache(self):
		"""
		This method is the deleter method for **self.__filesCache** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "filesCache"))

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
	def model(self):
		"""
		This method is the property for **self.__model** attribute.

		:return: self.__model. ( SearchResultsModel )
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		This method is the setter method for **self.__model** attribute.

		:param value: Attribute value. ( SearchResultsModel )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		This method is the deleter method for **self.__model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

	@property
	def view(self):
		"""
		This method is the property for **self.__view** attribute.

		:return: self.__view. ( QWidget )
		"""

		return self.__view

	@view.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def view(self, value):
		"""
		This method is the setter method for **self.__view** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view"))

	@view.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def view(self):
		"""
		This method is the deleter method for **self.__view** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view"))

	@property
	def delegate(self):
		"""
		This method is the property for **self.__delegate** attribute.

		:return: self.__delegate. ( QItemDelegate )
		"""

		return self.__delegate

	@delegate.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def delegate(self, value):
		"""
		This method is the setter method for **self.__delegate** attribute.

		:param value: Attribute value. ( QItemDelegate )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "delegate"))

	@delegate.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def delegate(self):
		"""
		This method is the deleter method for **self.__delegate** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "delegate"))

	@property
	def locations(self):
		"""
		This method is the property for **self.__locations** attribute.

		:return: self.__locations. ( OrderedDict )
		"""

		return self.__locations

	@locations.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def locations(self, value):
		"""
		This method is the setter method for **self.__locations** attribute.

		:param value: Attribute value. ( OrderedDict )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "locations"))

	@locations.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def locations(self):
		"""
		This method is the deleter method for **self.__locations** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "locations"))

	@property
	def locationsMenu(self):
		"""
		This method is the property for **self.__locationsMenu** attribute.

		:return: self.__locationsMenu. ( QMenu )
		"""

		return self.__locationsMenu

	@locationsMenu.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def locationsMenu(self, value):
		"""
		This method is the setter method for **self.__locationsMenu** attribute.

		:param value: Attribute value. ( QMenu )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "locationsMenu"))

	@locationsMenu.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def locationsMenu(self):
		"""
		This method is the deleter method for **self.__locationsMenu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "locationsMenu"))

	@property
	def defaultFilterIn(self):
		"""
		This method is the property for **self.__defaultFilterIn** attribute.

		:return: self.__defaultFilterIn. ( String )
		"""

		return self.__defaultFilterIn

	@defaultFilterIn.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultFilterIn(self, value):
		"""
		This method is the setter method for **self.__defaultFilterIn** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"defaultFilterIn", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("defaultFilterIn", value)
		self.__defaultFilterIn = value

	@defaultFilterIn.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultFilterIn(self):
		"""
		This method is the deleter method for **self.__defaultFilterIn** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultFilterIn"))
	@property
	def filtersInFormat(self):
		"""
		This method is the property for **self.__filtersInFormat** attribute.

		:return: self.__filtersInFormat. ( String )
		"""

		return self.__filtersInFormat

	@filtersInFormat.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def filtersInFormat(self, value):
		"""
		This method is the setter method for **self.__filtersInFormat** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"filtersInFormat", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("filtersInFormat", value)
		self.__filtersInFormat = value

	@filtersInFormat.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def filtersInFormat(self):
		"""
		This method is the deleter method for **self.__filtersInFormat** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "filtersInFormat"))

	@property
	def defaultFilterOut(self):
		"""
		This method is the property for **self.__defaultFilterOut** attribute.

		:return: self.__defaultFilterOut. ( String )
		"""

		return self.__defaultFilterOut

	@defaultFilterOut.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultFilterOut(self, value):
		"""
		This method is the setter method for **self.__defaultFilterOut** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"defaultFilterOut", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("defaultFilterOut", value)
		self.__defaultFilterOut = value

	@defaultFilterOut.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultFilterOut(self):
		"""
		This method is the deleter method for **self.__defaultFilterOut** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultFilterOut"))
	@property
	def filtersOutFormat(self):
		"""
		This method is the property for **self.__filtersOutFormat** attribute.

		:return: self.__filtersOutFormat. ( String )
		"""

		return self.__filtersOutFormat

	@filtersOutFormat.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def filtersOutFormat(self, value):
		"""
		This method is the setter method for **self.__filtersOutFormat** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"filtersOutFormat", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("filtersOutFormat", value)
		self.__filtersOutFormat = value

	@filtersOutFormat.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def filtersOutFormat(self):
		"""
		This method is the deleter method for **self.__filtersOutFormat** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "filtersOutFormat"))

	@property
	def defaultTarget(self):
		"""
		This method is the property for **self.__defaultTarget** attribute.

		:return: self.__defaultTarget. ( String )
		"""

		return self.__defaultTarget

	@defaultTarget.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultTarget(self, value):
		"""
		This method is the setter method for **self.__defaultTarget** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"defaultTarget", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("defaultTarget", value)
		self.__defaultTarget = value

	@defaultTarget.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultTarget(self):
		"""
		This method is the deleter method for **self.__defaultTarget** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultTarget"))
	@property
	def targetsFormat(self):
		"""
		This method is the property for **self.__targetsFormat** attribute.

		:return: self.__targetsFormat. ( String )
		"""

		return self.__targetsFormat

	@targetsFormat.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def targetsFormat(self, value):
		"""
		This method is the setter method for **self.__targetsFormat** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"targetsFormat", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' file doesn't exists!".format("targetsFormat", value)
		self.__targetsFormat = value

	@targetsFormat.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def targetsFormat(self):
		"""
		This method is the deleter method for **self.__targetsFormat** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "targetsFormat"))

	@property
	def defaultLineNumberWidth(self):
		"""
		This method is the property for **self.__defaultLineNumberWidth** attribute.

		:return: self.__defaultLineNumberWidth. ( Integer )
		"""

		return self.__defaultLineNumberWidth

	@defaultLineNumberWidth.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultLineNumberWidth(self, value):
		"""
		This method is the setter method for **self.__defaultLineNumberWidth** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format(
			"defaultLineNumberWidth", value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("defaultLineNumberWidth", value)
		self.__defaultLineNumberWidth = value

	@defaultLineNumberWidth.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultLineNumberWidth(self):
		"""
		This method is the deleter method for **self.__defaultLineNumberWidth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultLineNumberWidth"))

	@property
	def defaultLineColor(self):
		"""
		This method is the property for **self.__defaultLineColor** attribute.

		:return: self.__defaultLineColor. ( QColor )
		"""

		return self.__defaultLineColor

	@defaultLineColor.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultLineColor(self, value):
		"""
		This method is the setter method for **self.__defaultLineColor** attribute.

		:param value: Attribute value. ( QColor )
		"""

		if value is not None:
			assert type(value) is QColor, "'{0}' attribute: '{1}' type is not 'QColor'!".format("defaultLineColor", value)
		self.__defaultLineColor = value

	@defaultLineColor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultLineColor(self):
		"""
		This method is the deleter method for **self.__defaultLineColor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultLineColor"))

	@property
	def searchWorkerThread(self):
		"""
		This method is the property for **self.__searchWorkerThread** attribute.

		:return: self.__searchWorkerThread. ( QThread )
		"""

		return self.__searchWorkerThread

	@searchWorkerThread.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchWorkerThread(self, value):
		"""
		This method is the setter method for **self.__searchWorkerThread** attribute.

		:param value: Attribute value. ( QThread )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "searchWorkerThread"))

	@searchWorkerThread.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchWorkerThread(self):
		"""
		This method is the deleter method for **self.__searchWorkerThread** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchWorkerThread"))

	#******************************************************************************************************************
	#***	Class methods
	#******************************************************************************************************************
	@core.executionTrace
	def show(self):
		"""
		This method reimplements the :meth:`QWidget.show` method.
		"""

		selectedText = self.__container.getCurrentEditor().getSelectedText()
		selectedText and SearchAndReplace.insertPattern(selectedText, self.__searchPatternsModel)
		self.Search_comboBox.lineEdit().selectAll()
		self.Search_comboBox.setFocus()

		super(SearchInFiles, self).show()
		self.raise_()

	@core.executionTrace
	def closeEvent(self, event):
		"""
		This method reimplements the :meth:`QWidget.closeEvent` method.

		:param event: QEvent. ( QEvent )
		"""

		self.__interruptSearch()
		super(SearchInFiles, self).closeEvent(event)

	@core.executionTrace
	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		umbra.ui.common.setWindowDefaultIcon(self)

		self.__model = SearchResultsModel(self)
		self.__delegate = RichText_QStyledItemDelegate(self)

		self.Search_Results_treeView.setParent(None)
		self.Search_Results_treeView = SearchResults_QTreeView(self, self.__model)
		self.Search_Results_treeView.setItemDelegate(self.__delegate)
		self.Search_Results_treeView.setObjectName("Search_Results_treeView")
		self.Search_Results_frame_gridLayout.addWidget(self.Search_Results_treeView, 0, 0)
		self.__view = self.Search_Results_treeView
		self.__view.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.__view_addActions()

		self.__searchPatternsModel = self.__container.searchAndReplace.searchPatternsModel
		self.Search_comboBox.setModel(self.__container.searchAndReplace.searchPatternsModel)
		self.Search_comboBox.setInsertPolicy(QComboBox.InsertAtTop)
		self.Search_comboBox.completer().setCaseSensitivity(Qt.CaseSensitive)

		self.__replaceWithPatternsModel = self.__container.searchAndReplace.replaceWithPatternsModel
		self.Replace_With_comboBox.setModel(self.__container.searchAndReplace.replaceWithPatternsModel)
		self.Replace_With_comboBox.setInsertPolicy(QComboBox.InsertAtTop)
		self.Replace_With_comboBox.completer().setCaseSensitivity(Qt.CaseSensitive)

		self.Where_lineEdit.setParent(None)
		self.Where_lineEdit = Search_QLineEdit(self)
		self.Where_lineEdit.setObjectName("Where_lineEdit")
		self.Where_frame_gridLayout.addWidget(self.Where_lineEdit, 0, 0)
		self.__locationsMenu = QMenu()
		for title, location in self.__locations.iteritems():
			self.__locationsMenu.addAction(self.__container.engine.actionsManager.registerAction(
			"Actions|Umbra|Components|factory.scriptEditor|Search In Files|{0}".format(title),
			text="{0}".format(title),
			slot=functools.partial(self.__addLocation, location)))
		self.Where_lineEdit.searchActiveLabel.setMenu(self.__locationsMenu)
		self.Where_lineEdit.setPlaceholderText("Use the magnifier to add locations!")

		self.installEventFilter(ValidationFilter(self))

		# Signals / Slots.
		self.__view.selectionModel().selectionChanged.connect(self.__view_selectionModel__selectionChanged)
		self.__view.doubleClicked.connect(self.__view__doubleClicked)
		self.__searchPatternsModel.patternInserted.connect(functools.partial(
		self.__patternsModel__patternInserted, self.Search_comboBox))
		self.__replaceWithPatternsModel.patternInserted.connect(functools.partial(
		self.__patternsModel__patternInserted, self.Replace_With_comboBox))
		self.Search_pushButton.clicked.connect(self.__Search_pushButton__clicked)
		self.Close_pushButton.clicked.connect(self.__Close_pushButton__clicked)

	@core.executionTrace
	def __view_addActions(self):
		"""
		This method sets the View actions.
		"""

		self.__view.addAction(self.__container.engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|Search In Files|Replace All",
		slot=self.__view_replaceAllAction__triggered))
		self.__view.addAction(self.__container.engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|Search In Files|Replace Selected",
		slot=self.__view_replaceSelectedAction__triggered))
		separatorAction = QAction(self.__view)
		separatorAction.setSeparator(True)
		self.__view.addAction(separatorAction)
		self.__view.addAction(self.__container.engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|Search In Files|Save All",
		slot=self.__view_saveAllAction__triggered))
		self.__view.addAction(self.__container.engine.actionsManager.registerAction(
		"Actions|Umbra|Components|factory.scriptEditor|Search In Files|Save Selected",
		slot=self.__view_saveSelectedAction__triggered))

	@core.executionTrace
	def __view_replaceAllAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|Search In Files|Replace All'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		allNodes = filter(lambda x: x.family in ("SearchFile", "SearchOccurence"), self.__model.rootNode.children)
		if allNodes:
			return self.replace(allNodes)

	@core.executionTrace
	def __view_replaceSelectedAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|Search In Files|Replace Selected'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		selectedNodes = filter(lambda x: x.family in ("SearchFile", "SearchOccurence"), self.__view.getSelectedNodes())
		if selectedNodes:
			return self.replace(filter(lambda x: x.parent not in selectedNodes, selectedNodes))

	@core.executionTrace
	def __view_saveAllAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|Search In Files|Save All'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		allNodes = filter(lambda x: x.family is "ReplaceResult", self.__model.rootNode.children)
		if allNodes:
			return self.saveFiles(allNodes)

	@core.executionTrace
	def __view_saveSelectedAction__triggered(self, checked):
		"""
		This method is triggered by **'Actions|Umbra|Components|factory.scriptEditor|Search In Files|Save Selected'** action.

		:param checked: Action checked state. ( Boolean )
		:return: Method success. ( Boolean )
		"""

		selectedNodes = filter(lambda x: x.family is "ReplaceResult", self.__view.getSelectedNodes())
		if selectedNodes:
			return self.saveFiles(selectedNodes)

	@core.executionTrace
	def __patternsModel__patternInserted(self, comboBox, index):
		"""
		This method is triggered when a pattern has been inserted into a patterns Model.

		:param comboBox: Pattern Model attached comboBox. ( QComboBox )
		:param index: Inserted pattern index. ( QModelIndex )
		"""

		comboBox.setCurrentIndex(index.row())

	@core.executionTrace
	def __Search_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Search_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.search()

	@core.executionTrace
	def __Close_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Close_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		self.close()

	@core.executionTrace
	def __view__doubleClicked(self, index):
		"""
		This method is triggered when a View Widget is double clicked.

		:param index: Clicked item index. ( QModelIndex )
		"""

		node = self.__model.getNode(index)

		if node.family == "SearchOccurence":
			file = node.parent.file
			occurence = node
		elif node.family in ("SearchFile", "ReplaceResult"):
			file = node.file
			occurence = None

		self.__highlightOccurence(file, occurence)

	@core.executionTrace
	def __view_selectionModel__selectionChanged(self, selectedItems, deselectedItems):
		"""
		This method is triggered when the View **selectionModel** has changed.

		:param selectedItems: Selected items. ( QItemSelection )
		:param deselectedItems: Deselected items. ( QItemSelection )
		"""

		indexes = selectedItems.indexes()
		if not indexes:
			return

		node = self.__model.getNode(indexes.pop())

		if node.family == "SearchOccurence":
			file = node.parent.file
			occurence = node
		elif node.family in ("SearchFile", "ReplaceResult"):
			file = node.file
			occurence = None

		if self.__container.getEditor(file):
			self.__highlightOccurence(file, occurence)

	@core.executionTrace
	def __searchWorkerThread__searchFinished(self, searchResults):
		"""
		This method is triggered by the :attr:`SearchInFiles.grepWorkerThread` attribute worker thread
		when the search is finished.
	
		:param searchResults: Search results. ( List )
		"""

		self.setSearchResults(searchResults)

		self.__container.engine.stopProcessing()
		metrics = self.__model.getMetrics()
		self.__container.engine.notificationsManager.notify(
		"{0} | '{1}' pattern occurence(s) found in '{2}' files!".format(self.__class__.__name__,
																	metrics["SearchOccurence"],
																	metrics["SearchFile"]))

	@core.executionTrace
	def __addLocation(self, type, *args):
		"""
		This method is triggered when a **Where_lineEdit** Widget context menu entry is clicked.

		:param type: Location type. ( String )
		:param \*args: Arguments. ( \* )
		"""

		if type == "directory":
			location = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getExistingDirectory(self,
																						"Add Directory:",
																						RuntimeGlobals.lastBrowsedPath)))
		elif type == "file":
			location = umbra.ui.common.storeLastBrowsedPath((QFileDialog.getOpenFileName(self,
																						"Add File:",
																						RuntimeGlobals.lastBrowsedPath,
																						"All Files (*)")))
		elif type == "editors":
			location = self.__targetsFormat.format(self.__defaultTarget)
		elif type == "includeFilter":
			location = self.__filtersInFormat.format(self.__defaultFilterIn)
		elif type == "excludeFilter":
			location = self.__filtersOutFormat.format(self.__defaultFilterOut)

		location and self.Where_lineEdit.setText(", ".join(filter(bool, (strings.encode(
		self.Where_lineEdit.text()), location))))

	@core.executionTrace
	def __formatOccurence(self, occurence):
		"""
		This method formats the given occurence and returns the matching rich html text.

		:param occurence: Occurence to format. ( Occurence )
		:return: Rich text. ( String )
		"""

		color = "rgb({0}, {1}, {2})"
		spanFormat = "<span style=\"color: {0};\">{{0}}</span>".format(color.format(self.__defaultLineColor.red(),
																					self.__defaultLineColor.green(),
																					self.__defaultLineColor.blue()))
		line = strings.encode(occurence.text)
		start = spanFormat.format(line[:occurence.column])
		pattern = "<b>{0}</b>".format(line[occurence.column:occurence.column + occurence.length])
		end = spanFormat.format(line[occurence.column + occurence.length:])
		return "".join((start, pattern, end))

	@core.executionTrace
	def __formatReplaceMetrics(self, file, metrics):
		"""
		This method formats the given replace metrics and returns the matching rich html text.

		:param file: File. ( String )
		:param metrics: Replace metrics to format. ( String )
		:return: Rich text. ( String )
		"""

		color = "rgb({0}, {1}, {2})"
		spanFormat = "<span style=\"color: {0};\">{{0}}</span>".format(color.format(self.__defaultLineColor.red(),
																					self.__defaultLineColor.green(),
																					self.__defaultLineColor.blue()))
		dirName, baseName = (os.path.dirname(file), os.path.basename(file))

		return "".join((spanFormat.format("'"),
						spanFormat.format(dirName),
						spanFormat.format(os.path.sep),
						baseName,
						spanFormat.format("' file: '"),
						strings.encode(metrics),
						spanFormat.format("' occurence(s) replaced!")))

	@core.executionTrace
	def __highlightOccurence(self, file, occurence):
		"""
		This method highlights given file occurence.
		
		:param file: File containing the occurence. ( String )
		:param occurence: Occurence to highlight. ( Occurence / SearchOccurenceNode )
		"""

		if not self.__container.getEditor(file):
			cacheData = self.__filesCache.getContent(file)
			if cacheData:
				document = cacheData.document or self.__getDocument(cacheData.content)
				self.__container.loadDocument(document, file)
				self.__uncache(file)
			else:
				self.__container.loadFile(file)
		else:
			self.__container.setCurrentEditor(file)

		if not occurence:
			return

		cursor = self.__container.getCurrentEditor().textCursor()
		cursor.setPosition(occurence.position, QTextCursor.MoveAnchor)
		cursor.setPosition(occurence.position + occurence.length, QTextCursor.KeepAnchor)
		self.__container.getCurrentEditor().setTextCursor(cursor)

	@core.executionTrace
	def __getDocument(self, content):
		"""
		This method returns a `QTextDocument <http://doc.qt.nokia.com/qtextdocument.html>`_ class instance
		with given content.

		:return: Document. ( QTextDocument )
		"""

		document = QTextDocument(QString(content))
		document.clearUndoRedoStacks()
		document.setModified(False)
		return document

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __replaceWithinDocument(self, document, occurences, replacementPattern):
		"""
		This method replaces given pattern occurences in given document using given settings.
	
		:param document: Document. ( QTextDocument )
		:param replacementPattern: Replacement pattern. ( String )
		:return: Replaced occurences count. ( Integer )
		"""

		cursor = QTextCursor(document)
		cursor.beginEditBlock()
		offset = count = 0
		for occurence in sorted(occurences, key=lambda x: x.position):
			cursor.setPosition(offset + occurence.position, QTextCursor.MoveAnchor)
			cursor.setPosition(offset + occurence.position + occurence.length, QTextCursor.KeepAnchor)
			cursor.insertText(replacementPattern)
			offset += len(replacementPattern) - occurence.length
			count += 1
		cursor.endEditBlock()
		return count

	@core.executionTrace
	def __getSettings(self):
		"""
		This method returns the current search and replace settings.

		:return: Settings. ( Dictionary )
		"""

		return {"caseSensitive" : self.Case_Sensitive_checkBox.isChecked(),
				"wholeWord" : self.Whole_Word_checkBox.isChecked(),
				"regularExpressions" : self.Regular_Expressions_checkBox.isChecked()}

	@core.executionTrace
	def __interruptSearch(self):
		"""
		This method interrupt the current search.
		"""

		if self.__searchWorkerThread:
			self.__searchWorkerThread.quit()
			self.__searchWorkerThread.wait()
			self.__container.engine.stopProcessing(warning=False)

	@core.executionTrace
	def __cache(self, file, content, document):
		"""
		This method caches given file.

		:param file: File to cache. ( String )
		:param content: File content. ( List )
		:param document: File document. ( QTextDocument )
		"""

		self.__filesCache.addContent(**{file : CacheData(content=content, document=document)})

	@core.executionTrace
	def __uncache(self, file):
		"""
		This method uncaches given file.

		:param file: File to uncache. ( String )
		"""

		if file in self.__filesCache:
			self.__filesCache.removeContent(file)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setSearchResults(self, searchResults):
		"""
		This method sets the Model nodes using given search results.
		
		:param searchResults: Search results. ( List )
		:return: Method success. ( Boolean )
		"""

		rootNode = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")
		for searchResult in searchResults:
			searchFileNode = SearchFileNode(name=searchResult.file,
											parent=rootNode)
			searchFileNode.update(searchResult)
			width = \
			max(self.__defaultLineNumberWidth,
			max([len(strings.encode(occurence.line)) for occurence in searchResult.occurences]))
			for occurence in searchResult.occurences:
				formatter = "{{:>{0}}}".format(width)
				name = "{0}:{1}".format(formatter.format(occurence.line + 1).replace(" ", "&nbsp;"),
										self.__formatOccurence(occurence))
				searchOccurenceNode = SearchOccurenceNode(name=name,
														parent=searchFileNode)
				searchOccurenceNode.update(occurence)
		self.__model.initializeModel(rootNode)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setReplaceResults(self, replaceResults):
		"""
		This method sets the Model nodes using given replace results.
		
		:param replaceResults: Replace results. ( List )
		:return: Method success. ( Boolean )
		"""

		rootNode = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")
		for file, metrics in sorted(replaceResults.iteritems()):
			replaceResultNode = ReplaceResultNode(name=self.__formatReplaceMetrics(file, metrics),
												parent=rootNode,
												file=file)
		self.__model.initializeModel(rootNode)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def search(self):
		"""
		This method searchs user defined locations for search pattern.

		:return: Method success. ( Boolean )
		"""

		self.__interruptSearch()

		searchPattern = self.Search_comboBox.currentText()
		replacementPattern = self.Replace_With_comboBox.currentText()
		if not searchPattern:
			return False

		SearchAndReplace.insertPattern(searchPattern, self.__searchPatternsModel)
		SearchAndReplace.insertPattern(replacementPattern, self.__replaceWithPatternsModel)

		location = umbra.ui.common.parseLocation(
		strings.encode(self.Where_lineEdit.text()) or \
		self.__targetsFormat.format(self.__defaultTarget))

		settings = self.__getSettings()

		self.__searchWorkerThread = Search_worker(self, searchPattern, location, settings)
		# Signals / Slots.
		self.__searchWorkerThread.searchFinished.connect(self.__searchWorkerThread__searchFinished)

		self.__container.engine.workerThreads.append(self.__searchWorkerThread)
		self.__container.engine.startProcessing("Searching In Files ...")
		self.__searchWorkerThread.start()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def replace(self, nodes):
		"""
		This method replaces user defined files search pattern occurences with replacement pattern using given nodes.
		
		:param nodes: Nodes. ( List )
		:return: Method success. ( Boolean )
		"""

		files = {}
		for node in nodes:
			if node.family == "SearchFile":
				files[node.file] = node.children
			elif node.family == "SearchOccurence":
				file = node.parent.file
				if not file in files:
					files[file] = []
				files[file].append(node)

		replacementPattern = self.Replace_With_comboBox.currentText()
		SearchAndReplace.insertPattern(replacementPattern, self.__replaceWithPatternsModel)

		replaceResults = {}
		for file, occurences in files.iteritems():
			editor = self.__container.getEditor(file)
			if editor:
				document = editor.document()
			else:
				cacheData = self.__filesCache.getContent(file)
				if cacheData is None:
					LOGGER.warning(
					"!> {0} | '{1}' file doesn't exists in files cache!".format(self.__class__.__name__, file))
					continue

				content = self.__filesCache.getContent(file).content
				document = self.__getDocument(content)
				self.__cache(file, content, document)
			replaceResults[file] = self.__replaceWithinDocument(document, occurences, replacementPattern)

		self.setReplaceResults(replaceResults)
		self.__container.engine.notificationsManager.notify(
		"{0} | '{1}' pattern occurence(s) replaced in '{2}' files!".format(self.__class__.__name__,
																	sum(replaceResults.values()),
																	len(replaceResults.keys())))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def saveFiles(self, nodes):
		"""
		This method saves user defined files using give nodes.

		:param nodes: Nodes. ( List )
		:return: Method success. ( Boolean )
		"""

		metrics = {"Opened" : 0, "Cached" : 0}
		for node in nodes:
			file = node.file
			if self.__container.getEditor(file):
				if self.__container.saveFile(file):
					metrics["Opened"] += 1
					self.__uncache(file)
			else:
				cacheData = self.__filesCache.getContent(file)
				if cacheData is None:
					LOGGER.warning(
					"!> {0} | '{1}' file doesn't exists in files cache!".format(self.__class__.__name__, file))
					continue

				if cacheData.document:
					fileHandle = File(file)
					fileHandle.content = [cacheData.document.toPlainText()]
					if fileHandle.write():
						metrics["Cached"] += 1
						self.__uncache(file)
				else:
					LOGGER.warning(
					"!> {0} | '{1}' file document doesn't exists in files cache!".format(self.__class__.__name__, file))

		self.__container.engine.notificationsManager.notify(
		"{0} | '{1}' opened file(s) and '{2}' cached file(s) saved!".format(self.__class__.__name__,
																		metrics["Opened"],
																		metrics["Cached"]))
