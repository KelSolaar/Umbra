#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class Workers.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
from PyQt4.QtCore import QMutex
from PyQt4.QtCore import QRegExp
from PyQt4.QtCore import QString
from PyQt4.QtCore import QThread
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextDocument

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
import foundations.io as io
import foundations.walkers
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

__all__ = ["LOGGER", "Occurence", "SearchResult", "CacheData", "Search_worker"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Occurence(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for the :class:`Search_worker` class search occurence.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: line, column, length, text. ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class SearchResult(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for the :class:`Search_worker` class search result.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: file, pattern, settings, occurences. ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class CacheData(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for the :class:`Search_worker` class cache data.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: content, document. ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class Search_worker(QThread):
	"""
	This class is a `QThread <http://doc.qt.nokia.com/qthread.html>`_ subclass used
	to search for a pattern in a directory files.
	"""

	# Custom signals definitions.
	searchFinished = pyqtSignal(list)
	"""
	This signal is emited by the :class:`Search_worker` class when the search is finished. ( pyqtSignal )

	:return: Search results. ( List )
	"""

	@core.executionTrace
	def __init__(self, parent, pattern=None, location=None, settings=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QThread.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__container = parent

		self.__pattern = None
		self.pattern = pattern
		self.__location = None
		self.location = location
		self.__settings = None
		self.settings = settings

		self.__searchResults = None

		self.__interrupt = False
		self.__lock = QMutex()

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
	def pattern(self):
		"""
		This method is the property for **self.__pattern** attribute.

		:return: self.__pattern. ( String )
		"""

		return self.__pattern

	@pattern.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def pattern(self, value):
		"""
		This method is the setter method for **self.__pattern** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode, QString), \
			"'{0}' attribute: '{1}' type is not 'str', 'unicode' or 'QString'!".format("pattern", value)
		self.__pattern = value

	@pattern.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def pattern(self):
		"""
		This method is the deleter method for **self.__pattern** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "pattern"))

	@property
	def location(self):
		"""
		This method is the property for **self.__location** attribute.

		:return: self.__location. ( Location )
		"""

		return self.__location

	@location.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def location(self, value):
		"""
		This method is the setter method for **self.__location** attribute.

		:param value: Attribute value. ( Location )
		"""

		if value is not None:
			assert type(value) is umbra.ui.common.Location, \
			"'{0}' attribute: '{1}' type is not 'umbra.ui.common.Location'!".format("location", value)
		self.__location = value

	@location.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def location(self):
		"""
		This method is the deleter method for **self.__location** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "location"))

	@property
	def settings(self):
		"""
		This method is the property for **self.__settings** attribute.

		:return: self.__settings. ( Location )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def settings(self, value):
		"""
		This method is the setter method for **self.__settings** attribute.

		:param value: Attribute value. ( Location )
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("settings", value)
		self.__settings = foundations.dataStructures.Structure(**{"caseSensitive" : False,
																"wholeWord" : False,
																"regularExpressions" : False})
		self.__settings.update(value)

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This method is the deleter method for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def searchResults(self):
		"""
		This method is the property for **self.__searchResults** attribute.

		:return: self.__searchResults. ( List )
		"""

		return self.__searchResults

	@searchResults.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchResults(self, value):
		"""
		This method is the setter method for **self.__searchResults** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "searchResults"))

	@searchResults.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def searchResults(self):
		"""
		This method is the deleter method for **self.__searchResults** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchResults"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def run(self):
		"""
		This method reimplements the :meth:`QThread.run` method.
		"""

		self.__search()

	@core.executionTrace
	def quit(self):
		"""
		This method reimplements the :meth:`QThread.quit` method.
		"""

		self.__interrupt = True

		QThread.quit(self)

	@core.executionTrace
	def __search(self):
		"""
		This method performs the search.
		"""

		editorsFiles = self.__container.defaultTarget in self.__location.targets and \
		[editor.file for editor in self.__container.scriptEditor.listEditors()] or []

		files = self.__location.files
		for directory in self.__location.directories:
			if self.__interrupt:
				return

			walkerFiles = foundations.walkers.filesWalker(directory,
														self.__location.filtersIn,
														self.__location.filtersOut)
			files.extend(filter(foundations.common.isBinaryFile, walkerFiles))
		files = filter(lambda x: x not in editorsFiles, foundations.common.orderedUniqify(files))

		self.__searchResults = []
		self.__searchEditorsFiles(editorsFiles)
		self.__searchFiles(files)
		not self.__interrupt and self.searchFinished.emit(self.__searchResults)

	@core.executionTrace
	def __searchEditorsFiles(self, files):
		"""
		This method searches in :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor` class editors files.

		:param files: Editor files. ( List )
		"""

		for file in files:
			if self.__interrupt:
				return

			editor = self.__container.scriptEditor.getEditor(file)
			if not editor:
				continue

			self.__lock.lock()
			occurences = self.__searchDocument(editor.document(), self.__pattern, self.__settings)
			self.__lock.unlock()
			occurences and self.__searchResults.append(SearchResult(file=file,
																	pattern=self.__pattern,
																	settings=self.__settings,
																	occurences=occurences))

	@core.executionTrace
	def __searchFiles(self, files):
		"""
		This method searches in given files.

		:param files: Files. ( List )
		"""

		for file in files:
			if self.__interrupt:
				return

			if not foundations.common.pathExists(file):
				continue

			cacheData = self.__container.filesCache.getContent(file)
			if not cacheData:
				reader = io.File(file)
				content = reader.readAll()
				if content is None:
					LOGGER.warning("!> Error occured while reading '{0}' file proceeding to next one!".format(file))
					continue
				self.__container.filesCache.addContent(**{file : CacheData(content=content, document=None)})
			else:
				content = cacheData.content
			occurences = self.__searchDocument(QTextDocument(QString(content)), self.__pattern, self.__settings)
			occurences and self.__searchResults.append(SearchResult(file=file,
																	pattern=self.__pattern,
																	settings=self.__settings,
																	occurences=occurences))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __searchDocument(self, document, pattern, settings):
		"""
		This method searches for given pattern occurences in given document using given settings.
	
		:param document: Document. ( QTextDocument )
		:param pattern: Pattern. ( String )
		:param settings: Search settings. ( Structure )
		:return: Matched occurences. ( List )
		"""

		pattern = settings.regularExpressions and QRegExp(pattern) or pattern

		flags = QTextDocument.FindFlags()
		if settings.caseSensitive:
			flags = flags | QTextDocument.FindCaseSensitively
		if settings.wholeWord:
			flags = flags | QTextDocument.FindWholeWords

		occurences = []
		block = document.findBlock(0)
		cursor = document.find(pattern, block.position(), flags)
		while block.isValid() and cursor.position() != -1:
			if self.__interrupt:
				return

			blockCursor = QTextCursor(cursor)
			blockCursor.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
			blockCursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
			length = cursor.selectionEnd() - cursor.selectionStart()
			occurences.append(Occurence(line=cursor.blockNumber(),
										column=cursor.columnNumber() - length,
										length=length,
										position=cursor.position() - length,
										text=blockCursor.selectedText()))
			cursor = document.find(pattern, cursor.position(), flags)
			block = block.next()
		return occurences
