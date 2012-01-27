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
import fnmatch
import functools
import logging
import os
import re
from collections import OrderedDict
from PyQt4.QtCore import QRegExp
from PyQt4.QtCore import Qt
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
from umbra.components.factory.scriptEditor.searchAndReplace import _insertEditorSelectTextInModel
from umbra.components.factory.scriptEditor.searchAndReplace import _keyPressEvent
from umbra.components.factory.scriptEditor.workers import Grep_worker
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

__all__ = ["LOGGER", "UI_FILE", "parseLocation", "Location", "SearchInFiles"]

LOGGER = logging.getLogger(Constants.logger)

UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Search_In_Files.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
@core.executionTrace
def parseLocation(data):
	"""
	This definition parses given location data.

	:param data: Exception. ( Exception )
	:return: Location object. ( Location )
	"""

	tokens = data.split(",")
	if not tokens:
		return

	location = Location(directories=[], files=[], filtersIn=[], filtersOut=[], targets=[])
	for token in tokens:
		token = token.strip()
		if not token:
			continue

		if foundations.common.pathExists(token):
			if os.path.isdir(token):
				location.directories.append(token)
			else:
				location.files.append(token)
		else:
			match = re.match("(?P<filterIn>\*\.\w+)", token)
			if match:
				location.filtersIn.append(fnmatch.translate(match.group("filterIn")))
				continue
			match = re.match("!(?P<filterOut>\*\.\w+)", token)
			if match:
				location.filtersOut.append(fnmatch.translate(match.group("filterOut")))
				continue
			match = re.match("\<(?P<target>[\w ]+)\>", token)
			if match:
				location.targets.append(match.group("target"))
				continue
	return location

class Location(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for the :class:`SearchInFiles` class location.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: directories, files, filtersIn, filtersOut, targets. ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

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

		self.__searchPatternsModel = None
		self.__replaceWithPatternsModel = None

		self.__locations = OrderedDict([("Add Directory ...", "directory"),
								("Add File ...", "file"),
								("Add Opened Files", "editors"),
								("Add Include Filter", "includeFilter"),
								("Add Exclude Filter", "excludeFilter")])

		self.__defaultFilterIn = "*.txt"
		self.__defaultFilterOut = "!*.txt"
		self.__defaultTarget = "<Opened Files>"

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

		_insertEditorSelectTextInModel(self.__container.getCurrentEditor(), self.__searchPatternsModel)

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
			location = self.__defaultTarget
		elif type == "includeFilter":
			location = self.__defaultFilterIn
		elif type == "excludeFilter":
			location = self.__defaultFilterOut
		location and self.Where_lineEdit.setText(", ".join(filter(bool, (str(self.Where_lineEdit.text()), location))))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def search(self):
		"""
		This method searchs user defined files for search pattern.

		:return: Method success. ( Boolean )
		"""

		location = parseLocation(
		unicode(self.Where_lineEdit.text(), Constants.encodingFormat, Constants.encodingError) or self.__defaultTarget)
		settings = {"caseSensitive" : self.Case_Sensitive_checkBox.isChecked(),
					"wholeWord" : self.Whole_Word_checkBox.isChecked(),
					"regularExpressions" : self.Regular_Expressions_checkBox.isChecked()}

		self.__grepWorkerThread = Grep_worker(self, location, settings)
		self.__container.engine.workerThreads.append(self.__grepWorkerThread)
		self.__grepWorkerThread.start()

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
