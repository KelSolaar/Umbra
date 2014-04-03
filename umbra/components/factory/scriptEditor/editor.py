#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**editor.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`Editor` class and others editing helper objects.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import platform
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPlainTextDocumentLayout
from PyQt4.QtGui import QTextOption

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.io
import foundations.strings
import foundations.verbose
import umbra.ui.common
import umbra.ui.widgets.messageBox as messageBox
from umbra.ui.languages import PYTHON_LANGUAGE
from umbra.ui.widgets.codeEditor_QPlainTextEdit import CodeEditor_QPlainTextEdit

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Editor"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Editor(CodeEditor_QPlainTextEdit):
	"""
	Defines the default editor used by
	the :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor` Component Interface class.
	"""

	__untitledNameId = 1
	"""
	:param __untitledNameId: Editor untitled name id.
	:type __untitledNameId: int
	"""

	# Custom signals definitions.
	titleChanged = pyqtSignal()
	"""
	This signal is emited by the :class:`Editor` class when the current title is changed. ( pyqtSignal )
	"""

	fileLoaded = pyqtSignal()
	"""
	This signal is emited by the :class:`Editor` class when the current file is loaded. ( pyqtSignal )
	"""

	fileSaved = pyqtSignal()
	"""
	This signal is emited by the :class:`Editor` class when the current file is saved. ( pyqtSignal )
	"""

	fileReloaded = pyqtSignal()
	"""
	This signal is emited by the :class:`Editor` class when the current file is reloaded. ( pyqtSignal )
	"""

	fileClosed = pyqtSignal()
	"""
	This signal is emited by the :class:`Editor` class when the current file is closed. ( pyqtSignal )
	"""

	contentsChanged = pyqtSignal()
	"""
	This signal is emited by the :class:`Editor` class
	when the current editor document content has changed. ( pyqtSignal )
	"""

	modificationChanged = pyqtSignal(bool)
	"""
	This signal is emited by the :class:`Editor` class
	when the current editor document content has been modified. ( pyqtSignal )
	"""

	def __init__(self, parent=None, file=None, language=PYTHON_LANGUAGE, *args, **kwargs):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param file: File path.
		:type file: unicode
		:param language: Editor language.
		:type language: Language
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		CodeEditor_QPlainTextEdit.__init__(self, parent, language, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__file = None
		self.file = file

		self.__defaultFontsSettings = {"Windows" : ("Consolas", 10),
										"Darwin" : ("Monaco", 12),
										"Linux" : ("Monospace", 10)}
		self.__tabWidth = None

		self.__title = None
		self.__isUntitled = True
		self.__defaultFileName = "Untitled"
		self.__defaultFileExtension = "py"

		Editor.__initializeUi(self)

		file and self.loadFile(file)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def file(self):
		"""
		Property for **self.__file** attribute.

		:return: self.__file.
		:rtype: unicode
		"""

		return self.__file

	@file.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def file(self, value):
		"""
		Setter for **self.__file** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format("file", value)
		self.__file = value

	@file.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def file(self):
		"""
		Deleter for **self.__file** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "file"))

	@property
	def defaultFontsSettings(self):
		"""
		Property for **self.__defaultFontsSettings** attribute.

		:return: self.__defaultFontsSettings.
		:rtype: dict
		"""

		return self.__defaultFontsSettings

	@defaultFontsSettings.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultFontsSettings(self, value):
		"""
		Setter for **self.__defaultFontsSettings** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultFontsSettings"))

	@defaultFontsSettings.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultFontsSettings(self):
		"""
		Deleter for **self.__defaultFontsSettings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultFontsSettings"))

	@property
	def tabWidth(self):
		"""
		Property for **self.__tabWidth** attribute.

		:return: self.__tabWidth.
		:rtype: int
		"""

		return self.__tabWidth

	@tabWidth.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def tabWidth(self, value):
		"""
		Setter for **self.__tabWidth** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tabWidth"))

	@tabWidth.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def tabWidth(self):
		"""
		Deleter for **self.__tabWidth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tabWidth"))

	@property
	def title(self):
		"""
		Property for **self.__title** attribute.

		:return: self.__title.
		:rtype: unicode
		"""

		return self.__title

	@title.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def title(self, value):
		"""
		Setter for **self.__title** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "title"))

	@title.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def title(self):
		"""
		Deleter for **self.__title** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "title"))

	@property
	def isUntitled(self):
		"""
		Property for **self.__isUntitled** attribute.

		:return: self.__isUntitled.
		:rtype: bool
		"""

		return self.__isUntitled

	@isUntitled.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def isUntitled(self, value):
		"""
		Setter for **self.__isUntitled** attribute.

		:param value: Attribute value.
		:type value: bool
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "isUntitled"))

	@isUntitled.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def isUntitled(self):
		"""
		Deleter for **self.__isUntitled** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "isUntitled"))

	@property
	def defaultFileName(self):
		"""
		Property for **self.__defaultFileName** attribute.

		:return: self.__defaultFileName.
		:rtype: unicode
		"""

		return self.__defaultFileName

	@defaultFileName.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultFileName(self, value):
		"""
		Setter for **self.__defaultFileName** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultFileName"))

	@defaultFileName.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultFileName(self):
		"""
		Deleter for **self.__defaultFileName** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultFileName"))

	@property
	def defaultFileExtension(self):
		"""
		Property for **self.__defaultFileExtension** attribute.

		:return: self.__defaultFileExtension.
		:rtype: unicode
		"""

		return self.__defaultFileExtension

	@defaultFileExtension.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultFileExtension(self, value):
		"""
		Setter for **self.__defaultFileExtension** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultFileExtension"))

	@defaultFileExtension.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultFileExtension(self):
		"""
		Deleter for **self.__defaultFileExtension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultFileExtension"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeUi(self):
		"""
		Initializes the Widget ui.
		"""

		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setWordWrapMode(QTextOption.NoWrap)

		self.setAcceptDrops(True)

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			fontFamily, fontSize = self.__defaultFontsSettings["Windows"]
		elif platform.system() == "Darwin":
			fontFamily, fontSize = self.__defaultFontsSettings["Darwin"]
		elif platform.system() == "Linux":
			fontFamily, fontSize = self.__defaultFontsSettings["Linux"]
		font = QFont(fontFamily)
		font.setPointSize(fontSize)
		self.setFont(font)

	def __document__contentsChanged(self):
		"""
		Defines the slot triggered by the editor when document content changes.
		"""

		self.setTitle()

	def __document__modificationChanged(self, changed):
		"""
		Defines the slot triggered by the editor when document is modified.

		:param changed: File modification state.
		:type changed: bool
		"""

		self.setTitle()

	def __setDocumentSignals(self):
		"""
		Connects the editor document signals.
		"""

		# Signals / Slots.
		self.document().contentsChanged.connect(self.contentsChanged.emit)
		self.document().contentsChanged.connect(self.__document__contentsChanged)
		self.document().modificationChanged.connect(self.modificationChanged.emit)
		self.document().modificationChanged.connect(self.__document__modificationChanged)

	def setTitle(self, title=None):
		"""
		Sets the editor title.

		:param title: Editor title.
		:type title: unicode
		:return: Method success.
		:rtype: bool
		"""

		if not title:
			# TODO: https://bugreports.qt-project.org/browse/QTBUG-27084
			# titleTemplate = self.isModified() and "{0} *" or "{0}"
			# title = titleTemplate.format(self.getFileShortName())
			title = self.getFileShortName()

		LOGGER.debug("> Setting editor title to '{0}'.".format(title))
		self.__title = title
		self.setWindowTitle(title)

		self.titleChanged.emit()
		return True

	def setFile(self, file=None, isModified=False, isUntitled=False):
		"""
		Sets the editor file.

		:param File: File to set.
		:type File: unicode
		:param isModified: File modified state.
		:type isModified: bool
		:param isUntitled: File untitled state.
		:type isUntitled: bool
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Setting '{0}' editor file.".format(file))
		self.__file = file
		self.__isUntitled = isUntitled
		self.setModified(isModified)
		self.setTitle()
		return True

	def getFileShortName(self):
		"""
		Returns the current editor file short name.

		:return: File short name.
		:rtype: unicode
		"""

		if not self.__file:
			return ""

		return os.path.basename(self.__file)

	def getUntitledFileName(self):
		"""
		Returns an untitled editor file name.

		:return: Untitled file name.
		:rtype: unicode
		"""

		name = "{0} {1}.{2}".format(self.__defaultFileName, Editor._Editor__untitledNameId, self.defaultFileExtension)
		Editor._Editor__untitledNameId += 1
		LOGGER.debug("> Next untitled file name: '{0}'.".format(name))
		return name

	def loadDocument(self, document, file=None, language=None):
		"""
		Loads given document into the editor.

		:param document: Document to load.
		:type document: QTextDocument
		:param file: File.
		:type file: unicode
		:param language: Editor language.
		:type language: unicode
		:return: Method success.
		:rtype: bool
		"""

		document.setDocumentLayout(QPlainTextDocumentLayout(document))
		self.setDocument(document)
		self.setFile(file)
		self.setLanguage(language)
		self.__setDocumentSignals()

		self.fileLoaded.emit()
		return True

	def newFile(self):
		"""
		Creates a new editor file.

		:return: File name.
		:rtype: unicode
		"""

		file = self.getUntitledFileName()
		LOGGER.debug("> Creating '{0}' file.".format(file))
		self.setFile(file, isModified=False, isUntitled=True)
		self.__setDocumentSignals()
		return file

	@foundations.exceptions.handleExceptions(foundations.exceptions.FileExistsError)
	def loadFile(self, file):
		"""
		Reads and loads given file into the editor.

		:param File: File to load.
		:type File: unicode
		:return: Method success.
		:rtype: bool
		"""

		if not foundations.common.pathExists(file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(self.__class__.__name__,
																									file))

		LOGGER.debug("> Loading '{0}' file.".format(file))
		reader = foundations.io.File(file)
		self.setPlainText(reader.read())
		self.setFile(file)
		self.__setDocumentSignals()
		self.fileLoaded.emit()
		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.FileExistsError)
	def reloadFile(self, isModified=True):
		"""
		Reloads the current editor file.

		:param isModified: File modified state.
		:type isModified: bool
		:return: Method success.
		:rtype: bool
		"""

		if not foundations.common.pathExists(self.__file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
			self.__class__.__name__, self.__file))

		LOGGER.debug("> Reloading '{0}' file.".format(self.__file))
		reader = foundations.io.File(self.__file)
		if reader.cache():
			self.setContent(reader.content)
			self.setFile(self.__file, isModified=isModified)

			self.fileReloaded.emit()
			return True

	def saveFile(self):
		"""
		Saves the editor file content.

		:return: Method success.
		:rtype: bool
		"""

		if not self.__isUntitled and foundations.common.pathExists(self.__file):
			return self.writeFile(self.__file)
		else:
			return self.saveFileAs()

	def saveFileAs(self, file=None):
		"""
		Saves the editor file content either using given file or user chosen file.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		file = file or umbra.ui.common.storeLastBrowsedPath(QFileDialog.getSaveFileName(self, "Save As:", self.__file))
		if not file:
			return False

		return self.writeFile(foundations.strings.toString(file))

	def writeFile(self, file):
		"""
		Writes the editor file content into given file.

		:param file: File to write.
		:type file: unicode
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Writing '{0}' file.".format(file))
		writer = foundations.io.File(file)
		writer.content = [self.toPlainText().toUtf8()]
		if writer.write():
			self.setFile(file)

			self.fileSaved.emit()
			return True

	def closeFile(self):
		"""
		Closes the editor file.

		:return: Method success.
		:rtype: bool
		"""

		if not self.isModified():
			LOGGER.debug("> Closing '{0}' file.".format(self.__file))

			self.fileClosed.emit()
			return True

		choice = messageBox.messageBox("Warning", "Warning",
		"'{0}' document has been modified!\nWould you like to save your changes?".format(self.getFileShortName()),
		buttons=QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
		if choice == QMessageBox.Save:
			if self.saveFile():
				LOGGER.debug("> Closing '{0}' file.".format(self.__file))
				return True
		elif choice == QMessageBox.Discard:
			LOGGER.debug("> Discarding '{0}' file.".format(self.__file))

			self.fileClosed.emit()
			return True
		else:
			return False
