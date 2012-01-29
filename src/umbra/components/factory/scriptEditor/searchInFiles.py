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
from PyQt4.QtCore import QRegExp
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QWidget

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.ui.common
import umbra.ui.common
from umbra.ui.delegates import RichText_QStyledItemDelegate
from umbra.components.factory.scriptEditor.models import SearchFileNode
from umbra.components.factory.scriptEditor.models import SearchOccurenceNode
from umbra.components.factory.scriptEditor.models import SearchResultsModel
from umbra.components.factory.scriptEditor.searchAndReplace import _insertEditorSelectTextInModel
from umbra.components.factory.scriptEditor.searchAndReplace import _keyPressEvent
from umbra.components.factory.scriptEditor.views import SearchResults_QTreeView
from umbra.components.factory.scriptEditor.workers import Search_worker
from umbra.globals.constants import Constants
from umbra.globals.runtimeGlobals import RuntimeGlobals
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
		self.__container = self.__factoryScriptEditor = parent

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
	def factoryScriptEditor(self):
		"""
		This method is the property for **self.__factoryScriptEditor** attribute.

		:return: self.__factoryScriptEditor. ( QWidget )
		"""

		return self.__factoryScriptEditor

	@factoryScriptEditor.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryScriptEditor(self, value):
		"""
		This method is the setter method for **self.__factoryScriptEditor** attribute.

		:param value: Attribute value. ( QWidget )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factoryScriptEditor"))

	@factoryScriptEditor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def factoryScriptEditor(self):
		"""
		This method is the deleter method for **self.__factoryScriptEditor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factoryScriptEditor"))

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

		_insertEditorSelectTextInModel(self.__container.getCurrentEditor(), self.__searchPatternsModel)

		super(SearchInFiles, self).show()
		self.raise_()
		self.Search_comboBox.setFocus()

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

		self.__searchPatternsModel = self.__container.searchAndReplace.searchPatternsModel
		self.Search_comboBox.setModel(self.__container.searchAndReplace.searchPatternsModel)
		self.Search_comboBox.setInsertPolicy(QComboBox.InsertAtTop)

		self.__replaceWithPatternsModel = self.__container.searchAndReplace.replaceWithPatternsModel
		self.Replace_With_comboBox.setModel(self.__container.searchAndReplace.replaceWithPatternsModel)
		self.Replace_With_comboBox.setInsertPolicy(QComboBox.InsertAtTop)

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

		for widget in self.findChildren(QWidget, QRegExp(".*")):
			widget.keyPressEvent = functools.partial(_keyPressEvent, widget, self)

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
		location and self.Where_lineEdit.setText(", ".join(filter(bool, (str(self.Where_lineEdit.text()), location))))

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
		line = unicode(occurence.text, Constants.encodingFormat, Constants.encodingError)
		start = spanFormat.format(line[:occurence.column])
		pattern = "<b>{0}</b>".format(line[occurence.column:occurence.column + occurence.length])
		end = spanFormat.format(line[:occurence.column + occurence.length])
		return "".join((start, pattern, end))

	@core.executionTrace
	def __searchWorkerThread__occurencesMatched(self, searchResult):
		"""
		This method is triggered by the :attr:`SearchInFiles.grepWorkerThread` attribute worker thread
		when a pattern occurences have been matched in a file.

		:param searchResult: Search result. ( SearchResult )
		"""

		searchFileNode = SearchFileNode(searchResult.file)
		searchFileNode.update(searchResult)
		width = \
		max(self.__defaultLineNumberWidth, max([len(str(occurence.line)) for occurence in searchResult.occurences]))
		for occurence in searchResult.occurences:
			formatter = "{{:>{0}}}".format(width)
			name = "{0}:{1}".format(formatter.format(occurence.line + 1).replace(" ", "&nbsp;"),
									self.__formatOccurence(occurence))
			searchOccurenceNode = SearchOccurenceNode(name, searchFileNode)
			searchOccurenceNode.update(occurence)
		self.__model.appendSearchFileNode(searchFileNode)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def search(self):
		"""
		This method searchs user defined files for search pattern.

		:return: Method success. ( Boolean )
		"""

		searchPattern = self.Search_comboBox.currentText()
		if not searchPattern:
			return

		self.__model.clear()

		location = umbra.ui.common.parseLocation(
		unicode(self.Where_lineEdit.text(), Constants.encodingFormat, Constants.encodingError) or \
		self.__targetsFormat.format(self.__defaultTarget))
		settings = {"caseSensitive" : self.Case_Sensitive_checkBox.isChecked(),
					"wholeWord" : self.Whole_Word_checkBox.isChecked(),
					"regularExpressions" : self.Regular_Expressions_checkBox.isChecked()}

		self.__searchWorkerThread = Search_worker(self, searchPattern, location, settings)
		# Signals / Slots.
		self.__searchWorkerThread.occurencesMatched.connect(self.__searchWorkerThread__occurencesMatched)

		self.__container.engine.workerThreads.append(self.__searchWorkerThread)
		self.__searchWorkerThread.start()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def replace(self):
		"""
		This method replaces user defined files earch pattern occurences with replacement pattern.
		
		:return: Method success. ( Boolean )
		"""

		print "Replace!"
