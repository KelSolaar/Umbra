#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class Workers.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import itertools
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
import foundations.dataStructures
import foundations.exceptions
import foundations.io
import foundations.verbose
import foundations.walkers
import umbra.ui.common

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Occurence", "SearchResult", "CacheData", "Search_worker"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Occurence(foundations.dataStructures.Structure):
	"""
	Defines a storage object for the :class:`Search_worker` class search occurence.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param \*\*kwargs: line, column, length, text.
		:type \*\*kwargs: dict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class SearchResult(foundations.dataStructures.Structure):
	"""
	Defines a storage object for the :class:`Search_worker` class search result.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param \*\*kwargs: file, pattern, settings, occurrences.
		:type \*\*kwargs: dict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class CacheData(foundations.dataStructures.Structure):
	"""
	Defines a storage object for the :class:`Search_worker` class cache data.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param \*\*kwargs: content, document.
		:type \*\*kwargs: dict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class Search_worker(QThread):
	"""
	Defines a `QThread <http://doc.qt.nokia.com/qthread.html>`_ subclass used
	to search for a pattern in a directory files.
	"""

	# Custom signals definitions.
	searchFinished = pyqtSignal(list)
	"""
	This signal is emited by the :class:`Search_worker` class when the search is finished. ( pyqtSignal )

	:return: Search results.
	:rtype: list
	"""

	def __init__(self, parent, pattern=None, location=None, settings=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
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
	def pattern(self):
		"""
		Property for **self.__pattern** attribute.

		:return: self.__pattern.
		:rtype: unicode
		"""

		return self.__pattern

	@pattern.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def pattern(self, value):
		"""
		Setter for **self.__pattern** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) in (unicode, QString), \
			"'{0}' attribute: '{1}' type is not 'unicode' or 'QString'!".format("pattern", value)
		self.__pattern = value

	@pattern.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def pattern(self):
		"""
		Deleter for **self.__pattern** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "pattern"))

	@property
	def location(self):
		"""
		Property for **self.__location** attribute.

		:return: self.__location.
		:rtype: Location
		"""

		return self.__location

	@location.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def location(self, value):
		"""
		Setter for **self.__location** attribute.

		:param value: Attribute value.
		:type value: Location
		"""

		if value is not None:
			assert type(value) is umbra.ui.common.Location, \
			"'{0}' attribute: '{1}' type is not 'umbra.ui.common.Location'!".format("location", value)
		self.__location = value

	@location.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def location(self):
		"""
		Deleter for **self.__location** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "location"))

	@property
	def settings(self):
		"""
		Property for **self.__settings** attribute.

		:return: self.__settings.
		:rtype: Location
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def settings(self, value):
		"""
		Setter for **self.__settings** attribute.

		:param value: Attribute value.
		:type value: Location
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("settings", value)
		self.__settings = foundations.dataStructures.Structure(**{"caseSensitive" : False,
																"wholeWord" : False,
																"regularExpressions" : False})
		self.__settings.update(value)

	@settings.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		Deleter for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def searchResults(self):
		"""
		Property for **self.__searchResults** attribute.

		:return: self.__searchResults.
		:rtype: list
		"""

		return self.__searchResults

	@searchResults.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def searchResults(self, value):
		"""
		Setter for **self.__searchResults** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "searchResults"))

	@searchResults.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def searchResults(self):
		"""
		Deleter for **self.__searchResults** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "searchResults"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def run(self):
		"""
		Reimplements the :meth:`QThread.run` method.
		"""

		self.__search()

	def quit(self):
		"""
		Reimplements the :meth:`QThread.quit` method.
		"""

		self.__interrupt = True

		QThread.quit(self)

	def __search(self):
		"""
		Performs the search.
		"""

		self.__searchResults = []

		editorsFiles = self.__container.defaultTarget in self.__location.targets and \
		[editor.file for editor in self.__container.scriptEditor.listEditors()] or []
		self.__searchEditorsFiles(editorsFiles)

		self.__searchFiles(self.__location.files)

		for directory in self.__location.directories:
			if self.__interrupt:
				return

			filesWalker = foundations.walkers.filesWalker(directory,
														self.__location.filtersIn,
														list(itertools.chain(self.__location.filtersOut,
																			self.__location.files,
																			editorsFiles)))
			self.__searchFiles(filesWalker)

		not self.__interrupt and self.searchFinished.emit(self.__searchResults)

	def __searchEditorsFiles(self, files):
		"""
		Searches in :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor` class editors files.

		:param files: Editor files.
		:type files: list
		"""

		for file in files:
			if self.__interrupt:
				return

			if foundations.io.isReadable(file):
				if foundations.io.isBinaryFile(file):
					continue

			LOGGER.info("{0} | Searching '{1}' file!".format(self.__class__.__name__, file))
			editor = self.__container.scriptEditor.getEditor(file)
			if not editor:
				continue

			self.__lock.lock()
			occurrences = self.__searchDocument(editor.document(), self.__pattern, self.__settings)
			self.__lock.unlock()
			occurrences and self.__searchResults.append(SearchResult(file=file,
																	pattern=self.__pattern,
																	settings=self.__settings,
																	occurrences=occurrences))

	def __searchFiles(self, files):
		"""
		Searches in given files.

		:param files: Files.
		:type files: list
		"""

		for file in files:
			if self.__interrupt:
				return

			if not foundations.common.pathExists(file):
				continue

			if foundations.io.isReadable(file):
				if foundations.io.isBinaryFile(file):
					continue

			LOGGER.info("{0} | Searching '{1}' file!".format(self.__class__.__name__, file))
			cacheData = self.__container.filesCache.getContent(file)
			if not cacheData:
				reader = foundations.io.File(file)
				content = reader.read()
				if content is None:
					LOGGER.warning("!> Error occured while reading '{0}' file proceeding to next one!".format(file))
					continue
				self.__container.filesCache.addContent(**{file : CacheData(content=content, document=None)})
			else:
				content = cacheData.content
			occurrences = self.__searchDocument(QTextDocument(QString(content)), self.__pattern, self.__settings)
			occurrences and self.__searchResults.append(SearchResult(file=file,
																	pattern=self.__pattern,
																	settings=self.__settings,
																	occurrences=occurrences))

	def __searchDocument(self, document, pattern, settings):
		"""
		Searches for given pattern occurrences in given document using given settings.

		:param document: Document.
		:type document: QTextDocument
		:param pattern: Pattern.
		:type pattern: unicode
		:param settings: Search settings.
		:type settings: Structure
		:return: Matched occurrences.
		:rtype: list
		"""

		pattern = settings.regularExpressions and QRegExp(pattern) or pattern

		flags = QTextDocument.FindFlags()
		if settings.caseSensitive:
			flags = flags | QTextDocument.FindCaseSensitively
		if settings.wholeWord:
			flags = flags | QTextDocument.FindWholeWords

		occurrences = []
		block = document.findBlock(0)
		cursor = document.find(pattern, block.position(), flags)
		while block.isValid() and cursor.position() != -1:
			if self.__interrupt:
				return

			blockCursor = QTextCursor(cursor)
			blockCursor.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
			blockCursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
			length = cursor.selectionEnd() - cursor.selectionStart()
			occurrences.append(Occurence(line=cursor.blockNumber(),
										column=cursor.columnNumber() - length,
										length=length,
										position=cursor.position() - length,
										text=blockCursor.selectedText()))
			cursor = document.find(pattern, cursor.position(), flags)
			block = block.next()
		return occurrences
