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

from __future__ import unicode_literals

import os
import platform
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QPlainTextDocumentLayout
from PyQt4.QtGui import QTextOption

import foundations.exceptions
import foundations.io
import foundations.strings
import foundations.verbose
import umbra.ui.common
import umbra.ui.widgets.message_box as message_box
from umbra.ui.languages import PYTHON_LANGUAGE
from umbra.ui.widgets.codeEditor_QPlainTextEdit import CodeEditor_QPlainTextEdit

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Editor"]

LOGGER = foundations.verbose.install_logger()


class Editor(CodeEditor_QPlainTextEdit):
    """
    Defines the default editor used by
    the :class:`umbra.components.factory.script_editor.script_editor.ScriptEditor` Component Interface class.
    """

    __untitled_name_id = 1
    """
    :param __untitled_name_id: Editor untitled name id.
    :type __untitled_name_id: int
    """

    # Custom signals definitions.
    title_changed = pyqtSignal()
    """
    This signal is emited by the :class:`Editor` class when the current title is changed.
    """

    file_loaded = pyqtSignal()
    """
    This signal is emited by the :class:`Editor` class when the current file is loaded.
    """

    file_saved = pyqtSignal()
    """
    This signal is emited by the :class:`Editor` class when the current file is saved.
    """

    file_reloaded = pyqtSignal()
    """
    This signal is emited by the :class:`Editor` class when the current file is reloaded.
    """

    file_closed = pyqtSignal()
    """
    This signal is emited by the :class:`Editor` class when the current file is closed.
    """

    contents_changed = pyqtSignal()
    """
    This signal is emited by the :class:`Editor` class
    when the current editor document content has changed.
    """

    modification_changed = pyqtSignal(bool)
    """
    This signal is emited by the :class:`Editor` class
    when the current editor document content has been modified.
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

        self.__default_fonts_settings = {"Windows": ("Consolas", 10),
                                         "Darwin": ("Monaco", 12),
                                         "Linux": ("Monospace", 10)}
        self.__tab_width = None

        self.__title = None
        self.__is_untitled = True
        self.__default_file_name = "Untitled"
        self.__default_file_extension = "py"

        Editor.__initialize_ui(self)

        file and self.load_file(file)

    @property
    def file(self):
        """
        Property for **self.__file** attribute.

        :return: self.__file.
        :rtype: unicode
        """

        return self.__file

    @file.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
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
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def file(self):
        """
        Deleter for **self.__file** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "file"))

    @property
    def default_fonts_settings(self):
        """
        Property for **self.__default_fonts_settings** attribute.

        :return: self.__default_fonts_settings.
        :rtype: dict
        """

        return self.__default_fonts_settings

    @default_fonts_settings.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_fonts_settings(self, value):
        """
        Setter for **self.__default_fonts_settings** attribute.

        :param value: Attribute value.
        :type value: dict
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "default_fonts_settings"))

    @default_fonts_settings.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_fonts_settings(self):
        """
        Deleter for **self.__default_fonts_settings** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_fonts_settings"))

    @property
    def tab_width(self):
        """
        Property for **self.__tab_width** attribute.

        :return: self.__tab_width.
        :rtype: int
        """

        return self.__tab_width

    @tab_width.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def tab_width(self, value):
        """
        Setter for **self.__tab_width** attribute.

        :param value: Attribute value.
        :type value: int
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "tab_width"))

    @tab_width.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def tab_width(self):
        """
        Deleter for **self.__tab_width** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tab_width"))

    @property
    def title(self):
        """
        Property for **self.__title** attribute.

        :return: self.__title.
        :rtype: unicode
        """

        return self.__title

    @title.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def title(self, value):
        """
        Setter for **self.__title** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "title"))

    @title.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def title(self):
        """
        Deleter for **self.__title** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "title"))

    @property
    def is_untitled(self):
        """
        Property for **self.__is_untitled** attribute.

        :return: self.__is_untitled.
        :rtype: bool
        """

        return self.__is_untitled

    @is_untitled.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def is_untitled(self, value):
        """
        Setter for **self.__is_untitled** attribute.

        :param value: Attribute value.
        :type value: bool
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "is_untitled"))

    @is_untitled.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def is_untitled(self):
        """
        Deleter for **self.__is_untitled** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "is_untitled"))

    @property
    def default_file_name(self):
        """
        Property for **self.__default_file_name** attribute.

        :return: self.__default_file_name.
        :rtype: unicode
        """

        return self.__default_file_name

    @default_file_name.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_file_name(self, value):
        """
        Setter for **self.__default_file_name** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "default_file_name"))

    @default_file_name.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_file_name(self):
        """
        Deleter for **self.__default_file_name** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_file_name"))

    @property
    def default_file_extension(self):
        """
        Property for **self.__default_file_extension** attribute.

        :return: self.__default_file_extension.
        :rtype: unicode
        """

        return self.__default_file_extension

    @default_file_extension.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_file_extension(self, value):
        """
        Setter for **self.__default_file_extension** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "default_file_extension"))

    @default_file_extension.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def default_file_extension(self):
        """
        Deleter for **self.__default_file_extension** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_file_extension"))

    def __initialize_ui(self):
        """
        Initializes the Widget ui.
        """

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWordWrapMode(QTextOption.NoWrap)

        self.setAcceptDrops(True)

        if platform.system() == "Windows" or platform.system() == "Microsoft":
            fontFamily, fontSize = self.__default_fonts_settings["Windows"]
        elif platform.system() == "Darwin":
            fontFamily, fontSize = self.__default_fonts_settings["Darwin"]
        elif platform.system() == "Linux":
            fontFamily, fontSize = self.__default_fonts_settings["Linux"]
        font = QFont(fontFamily)
        font.setPointSize(fontSize)
        self.setFont(font)

    def __document__contents_changed(self):
        """
        Defines the slot triggered by the editor when document content changes.
        """

        self.set_title()

    def __document__modification_changed(self, changed):
        """
        Defines the slot triggered by the editor when document is modified.

        :param changed: File modification state.
        :type changed: bool
        """

        self.set_title()

    def __set_document_signals(self):
        """
        Connects the editor document signals.
        """

        # Signals / Slots.
        self.document().contentsChanged.connect(self.contents_changed.emit)
        self.document().contentsChanged.connect(self.__document__contents_changed)
        self.document().modificationChanged.connect(self.modification_changed.emit)
        self.document().modificationChanged.connect(self.__document__modification_changed)

    def set_title(self, title=None):
        """
        Sets the editor title.

        :param title: Editor title.
        :type title: unicode
        :return: Method success.
        :rtype: bool
        """

        if not title:
            # TODO: https://bugreports.qt-project.org/browse/QTBUG-27084
            # titleTemplate = self.is_modified() and "{0} *" or "{0}"
            # title = titleTemplate.format(self.get_file_short_name())
            title = self.get_file_short_name()

        LOGGER.debug("> Setting editor title to '{0}'.".format(title))
        self.__title = title
        self.setWindowTitle(title)

        self.title_changed.emit()
        return True

    def set_file(self, file=None, is_modified=False, is_untitled=False):
        """
        Sets the editor file.

        :param File: File to set.
        :type File: unicode
        :param is_modified: File modified state.
        :type is_modified: bool
        :param is_untitled: File untitled state.
        :type is_untitled: bool
        :return: Method success.
        :rtype: bool
        """

        LOGGER.debug("> Setting '{0}' editor file.".format(file))
        self.__file = file
        self.__is_untitled = is_untitled
        self.set_modified(is_modified)
        self.set_title()
        return True

    def get_file_short_name(self):
        """
        Returns the current editor file short name.

        :return: File short name.
        :rtype: unicode
        """

        if not self.__file:
            return ""

        return os.path.basename(self.__file)

    def get_untitled_file_name(self):
        """
        Returns an untitled editor file name.

        :return: Untitled file name.
        :rtype: unicode
        """

        name = "{0} {1}.{2}".format(
            self.__default_file_name, Editor._Editor__untitled_name_id, self.default_file_extension)
        Editor._Editor__untitled_name_id += 1
        LOGGER.debug("> Next untitled file name: '{0}'.".format(name))
        return name

    def load_document(self, document, file=None, language=None):
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
        self.set_file(file)
        self.set_language(language)
        self.__set_document_signals()

        self.file_loaded.emit()
        return True

    def new_file(self):
        """
        Creates a new editor file.

        :return: File name.
        :rtype: unicode
        """

        file = self.get_untitled_file_name()
        LOGGER.debug("> Creating '{0}' file.".format(file))
        self.set_file(file, is_modified=False, is_untitled=True)
        self.__set_document_signals()
        return file

    @foundations.exceptions.handle_exceptions(foundations.exceptions.FileExistsError)
    def load_file(self, file):
        """
        Reads and loads given file into the editor.

        :param File: File to load.
        :type File: unicode
        :return: Method success.
        :rtype: bool
        """

        if not foundations.common.path_exists(file):
            raise foundations.exceptions.FileExistsError(
                "{0} | '{1}' file doesn't exists!".format(self.__class__.__name__,
                                                          file))

        LOGGER.debug("> Loading '{0}' file.".format(file))
        reader = foundations.io.File(file)
        self.setPlainText(reader.read())
        self.set_file(file)
        self.__set_document_signals()
        self.file_loaded.emit()
        return True

    @foundations.exceptions.handle_exceptions(foundations.exceptions.FileExistsError)
    def reload_file(self, is_modified=True):
        """
        Reloads the current editor file.

        :param is_modified: File modified state.
        :type is_modified: bool
        :return: Method success.
        :rtype: bool
        """

        if not foundations.common.path_exists(self.__file):
            raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
                self.__class__.__name__, self.__file))

        LOGGER.debug("> Reloading '{0}' file.".format(self.__file))
        reader = foundations.io.File(self.__file)
        if reader.cache():
            self.set_content(reader.content)
            self.set_file(self.__file, is_modified=is_modified)

            self.file_reloaded.emit()
            return True

    def save_file(self):
        """
        Saves the editor file content.

        :return: Method success.
        :rtype: bool
        """

        if not self.__is_untitled and foundations.common.path_exists(self.__file):
            return self.write_file(self.__file)
        else:
            return self.save_fileAs()

    def save_fileAs(self, file=None):
        """
        Saves the editor file content either using given file or user chosen file.

        :return: Method success.
        :rtype: bool

        :note: May require user interaction.
        """

        file = file or umbra.ui.common.store_last_browsed_path(
            QFileDialog.getSaveFileName(self, "Save As:", self.__file))
        if not file:
            return False

        return self.write_file(foundations.strings.to_string(file))

    def write_file(self, file):
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
            self.set_file(file)

            self.file_saved.emit()
            return True

    def close_file(self):
        """
        Closes the editor file.

        :return: Method success.
        :rtype: bool
        """

        if not self.is_modified():
            LOGGER.debug("> Closing '{0}' file.".format(self.__file))

            self.file_closed.emit()
            return True

        choice = message_box.message_box("Warning", "Warning",
                                         "'{0}' document has been modified!\nWould you like to save your changes?".format(
                                             self.get_file_short_name()),
                                         buttons=QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        if choice == QMessageBox.Save:
            if self.save_file():
                LOGGER.debug("> Closing '{0}' file.".format(self.__file))
                return True
        elif choice == QMessageBox.Discard:
            LOGGER.debug("> Discarding '{0}' file.".format(self.__file))

            self.file_closed.emit()
            return True
        else:
            return False
