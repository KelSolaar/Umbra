#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**script_editor.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`ScriptEditor` Component Interface class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import code
import os
import platform
import re
import sys
import shutil
from PyQt4.QtCore import QChar
from PyQt4.QtCore import QString
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QColor
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QFont
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QKeySequence
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QMenuBar
from PyQt4.QtGui import QTextCursor
from PyQt4.QtGui import QTextOption

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common
import foundations.exceptions
import foundations.strings
import foundations.trace
import foundations.verbose
import foundations.walkers
import umbra.engine
import umbra.exceptions
import umbra.ui.common
import umbra.ui.highlighters
from manager.QWidget_component import QWidgetComponentFactory
from umbra.components.factory.script_editor.editor import Editor
from umbra.components.factory.script_editor.editor_status import EditorStatus
from umbra.components.factory.script_editor.models import LanguagesModel
from umbra.components.factory.script_editor.models import ProjectsModel
from umbra.components.factory.script_editor.search_and_replace import SearchAndReplace
from umbra.components.factory.script_editor.search_in_files import SearchInFiles
from umbra.components.factory.script_editor.views import ScriptEditor_QTabWidget
from umbra.globals.constants import Constants
from umbra.globals.runtime_globals import RuntimeGlobals
from umbra.globals.ui_constants import UiConstants
from umbra.ui.languages import get_language_description
from umbra.ui.languages import LOGGING_LANGUAGE
from umbra.ui.languages import PYTHON_LANGUAGE
from umbra.ui.languages import TEXT_LANGUAGE
from umbra.ui.widgets.basic_QPlainTextEdit import Basic_QPlainTextEdit

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "COMPONENT_UI_FILE", "ScriptEditor"]

LOGGER = foundations.verbose.install_logger()

COMPONENT_UI_FILE = os.path.join(os.path.dirname(__file__), "ui", "Script_Editor.ui")

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ScriptEditor(QWidgetComponentFactory(ui_file=COMPONENT_UI_FILE)):
	"""
	Defines the :mod:`sibl_gui.components.addons.script_editor.script_editor` Component Interface class.
	"""

	# Custom signals definitions.
	ui_refresh = pyqtSignal()
	"""
	This signal is emited by the :class:`ScriptEditor` class when the Ui needs to be refreshed.
	"""

	recent_files_changed = pyqtSignal()
	"""
	This signal is emited by the :class:`ScriptEditor` class when the recent files list has changed.
	"""

	file_loaded = pyqtSignal(unicode)
	"""
	This signal is emited by the :class:`ScriptEditor` class when a file is loaded.

	:return: Loaded file.
	:rtype: unicode
	"""

	file_closed = pyqtSignal(unicode)
	"""
	This signal is emited by the :class:`ScriptEditor` class when a file is closed.

	:return: Closed file.
	:rtype: unicode
	"""

	def __init__(self, parent=None, name=None, *args, **kwargs):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param name: Component name.
		:type name: unicode
		:param \*args: Arguments.
		:type \*args: \*
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(ScriptEditor, self).__init__(parent, name, *args, **kwargs)

		# --- Setting class attributes. ---
		self.deactivatable = False

		self.__dock_area = 1

		self.__engine = None
		self.__settings = None
		self.__settings_section = None

		self.__development_layout = UiConstants.development_layout

		self.__grammars_directory = "grammars"
		self.__extension = "grc"

		self.__model = None
		self.__languages_model = None

		self.__default_project = "default_project"
		self.__default_language = "Text"
		self.__default_script_language = "Python"
		self.__default_file_name = "Untitled"
		self.__default_file_extension = "py"

		self.__default_window_title = "Script Editor"

		self.__default_script_editor_directory = "script_editor"
		self.__default_session_directory = "session"
		self.__default_script_editor_file = "default_script.py"
		self.__factory_default_script_editor_file = "others/default_script.py"
		self.__script_editor_file = None

		self.__maximum_recent_files = 10
		self.__recent_files_actions = None

		self.__search_and_replace = None
		self.__search_in_files = None

		self.__indent_width = 20
		self.__default_fonts_settings = {"Windows" : ("Consolas", 10),
										"Darwin" : ("Monaco", 12),
										"Linux" : ("Monospace", 10)}

		self.__console = None
		self.__memory_handler_stack_depth = None

		self.__menu_bar = None
		self.__file_menu = None
		self.__edit_menu = None
		self.__source_menu = None
		self.__navigate_menu = None
		self.__search_menu = None
		self.__command_menu = None
		self.__view_menu = None

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def dock_area(self):
		"""
		Property for **self.__dock_area** attribute.

		:return: self.__dock_area.
		:rtype: int
		"""

		return self.__dock_area

	@dock_area.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def dock_area(self, value):
		"""
		Setter for **self.__dock_area** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "dock_area"))

	@dock_area.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def dock_area(self):
		"""
		Deleter for **self.__dock_area** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "dock_area"))

	@property
	def engine(self):
		"""
		Property for **self.__engine** attribute.

		:return: self.__engine.
		:rtype: QObject
		"""

		return self.__engine

	@engine.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def engine(self, value):
		"""
		Setter for **self.__engine** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "engine"))

	@engine.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def engine(self):
		"""
		Deleter for **self.__engine** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "engine"))

	@property
	def settings(self):
		"""
		Property for **self.__settings** attribute.

		:return: self.__settings.
		:rtype: QSettings
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		Setter for **self.__settings** attribute.

		:param value: Attribute value.
		:type value: QSettings
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		Deleter for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def settings_section(self):
		"""
		Property for **self.__settings_section** attribute.

		:return: self.__settings_section.
		:rtype: unicode
		"""

		return self.__settings_section

	@settings_section.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings_section(self, value):
		"""
		Setter for **self.__settings_section** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings_section"))

	@settings_section.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings_section(self):
		"""
		Deleter for **self.__settings_section** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings_section"))

	@property
	def development_layout(self):
		"""
		Property for **self.__development_layout** attribute.

		:return: self.__development_layout.
		:rtype: unicode
		"""

		return self.__development_layout

	@development_layout.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def development_layout(self, value):
		"""
		Setter for **self.__development_layout** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "development_layout"))

	@development_layout.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def development_layout(self):
		"""
		Deleter for **self.__development_layout** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "development_layout"))

	@property
	def grammars_directory(self):
		"""
		Property for **self.__grammars_directory** attribute.

		:return: self.__grammars_directory.
		:rtype: unicode
		"""

		return self.__grammars_directory

	@grammars_directory.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def grammars_directory(self, value):
		"""
		Setter for **self.__grammars_directory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "grammars_directory"))

	@grammars_directory.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def grammars_directory(self):
		"""
		Deleter for **self.__grammars_directory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "grammars_directory"))

	@property
	def extension(self):
		"""
		Property for **self.__extension** attribute.

		:return: self.__extension.
		:rtype: unicode
		"""

		return self.__extension

	@extension.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def extension(self, value):
		"""
		Setter for **self.__extension** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "extension"))

	@extension.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def extension(self):
		"""
		Deleter for **self.__extension** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "extension"))

	@property
	def model(self):
		"""
		Property for **self.__model** attribute.

		:return: self.__model.
		:rtype: ProjectsModel
		"""

		return self.__model

	@model.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def model(self, value):
		"""
		Setter for **self.__model** attribute.

		:param value: Attribute value.
		:type value: ProjectsModel
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "model"))

	@model.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def model(self):
		"""
		Deleter for **self.__model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "model"))

	@property
	def languages_model(self):
		"""
		Property for **self.__languages_model** attribute.

		:return: self.__languages_model.
		:rtype: LanguagesModel
		"""

		return self.__languages_model

	@languages_model.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def languages_model(self, value):
		"""
		Setter for **self.__languages_model** attribute.

		:param value: Attribute value.
		:type value: LanguagesModel
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "languages_model"))

	@languages_model.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def languages_model(self):
		"""
		Deleter for **self.__languages_model** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "languages_model"))

	@property
	def default_project(self):
		"""
		Property for **self.__default_project** attribute.

		:return: self.__default_project.
		:rtype: unicode
		"""

		return self.__default_project

	@default_project.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_project(self, value):
		"""
		Setter for **self.__default_project** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "default_project"))

	@default_project.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_project(self):
		"""
		Deleter for **self.__default_project** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_project"))

	@property
	def default_language(self):
		"""
		Property for **self.__default_language** attribute.

		:return: self.__default_language.
		:rtype: unicode
		"""

		return self.__default_language

	@default_language.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_language(self, value):
		"""
		Setter for **self.__default_language** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "default_language"))

	@default_language.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_language(self):
		"""
		Deleter for **self.__default_language** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_language"))

	@property
	def default_script_language(self):
		"""
		Property for **self.__default_script_language** attribute.

		:return: self.__default_script_language.
		:rtype: unicode
		"""

		return self.__default_script_language

	@default_script_language.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_script_language(self, value):
		"""
		Setter for **self.__default_script_language** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "default_script_language"))

	@default_script_language.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_script_language(self):
		"""
		Deleter for **self.__default_script_language** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_script_language"))

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

	@property
	def default_window_title(self):
		"""
		Property for **self.__default_window_title** attribute.

		:return: self.__default_window_title.
		:rtype: unicode
		"""

		return self.__default_window_title

	@default_window_title.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_window_title(self, value):
		"""
		Setter for **self.__default_window_title** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "default_window_title"))

	@default_window_title.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_window_title(self):
		"""
		Deleter for **self.__default_window_title** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_window_title"))

	@property
	def default_script_editor_directory(self):
		"""
		Property for **self.__default_script_editor_directory** attribute.

		:return: self.__default_script_editor_directory.
		:rtype: unicode
		"""

		return self.__default_script_editor_directory

	@default_script_editor_directory.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_script_editor_directory(self, value):
		"""
		Setter for **self.__default_script_editor_directory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "default_script_editor_directory"))

	@default_script_editor_directory.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_script_editor_directory(self):
		"""
		Deleter for **self.__default_script_editor_directory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_script_editor_directory"))

	@property
	def default_session_directory(self):
		"""
		Property for **self.__default_session_directory** attribute.

		:return: self.__default_session_directory.
		:rtype: unicode
		"""

		return self.__default_session_directory

	@default_session_directory.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_session_directory(self, value):
		"""
		Setter for **self.__default_session_directory** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "default_session_directory"))

	@default_session_directory.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_session_directory(self):
		"""
		Deleter for **self.__default_session_directory** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_session_directory"))

	@property
	def default_script_editor_file(self):
		"""
		Property for **self.__default_script_editor_file** attribute.

		:return: self.__default_script_editor_file.
		:rtype: unicode
		"""

		return self.__default_script_editor_file

	@default_script_editor_file.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_script_editor_file(self, value):
		"""
		Setter for **self.__default_script_editor_file** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "default_script_editor_file"))

	@default_script_editor_file.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_script_editor_file(self):
		"""
		Deleter for **self.__default_script_editor_file** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_script_editor_file"))

	@property
	def factory_default_script_editor_file(self):
		"""
		Property for **self.__factory_default_script_editor_file** attribute.

		:return: self.__factory_default_script_editor_file.
		:rtype: unicode
		"""

		return self.__factory_default_script_editor_file

	@factory_default_script_editor_file.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def factory_default_script_editor_file(self, value):
		"""
		Setter for **self.__factory_default_script_editor_file** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "factory_default_script_editor_file"))

	@factory_default_script_editor_file.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def factory_default_script_editor_file(self):
		"""
		Deleter for **self.__factory_default_script_editor_file** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "factory_default_script_editor_file"))

	@property
	def script_editor_file(self):
		"""
		Property for **self.__script_editor_file** attribute.

		:return: self.__script_editor_file.
		:rtype: unicode
		"""

		return self.__script_editor_file

	@script_editor_file.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def script_editor_file(self, value):
		"""
		Setter for **self.__script_editor_file** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"script_editor_file", value)
		self.__script_editor_file = value

	@script_editor_file.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def script_editor_file(self):
		"""
		Deleter for **self.__script_editor_file** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "script_editor_file"))

	@property
	def maximum_recent_files(self):
		"""
		Property for **self.__maximum_recent_files** attribute.

		:return: self.__maximum_recent_files.
		:rtype: int
		"""

		return self.__maximum_recent_files

	@maximum_recent_files.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def maximum_recent_files(self, value):
		"""
		Setter for **self.__maximum_recent_files** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "maximum_recent_files"))

	@maximum_recent_files.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def maximum_recent_files(self):
		"""
		Deleter for **self.__maximum_recent_files** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "maximum_recent_files"))

	@property
	def recent_files_actions(self):
		"""
		Property for **self.__recent_files_actions** attribute.

		:return: self.__recent_files_actions.
		:rtype: list
		"""

		return self.__recent_files_actions

	@recent_files_actions.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def recent_files_actions(self, value):
		"""
		Setter for **self.__recent_files_actions** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "recent_files_actions"))

	@recent_files_actions.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def recent_files_actions(self):
		"""
		Deleter for **self.__recent_files_actions** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "recent_files_actions"))

	@property
	def search_and_replace(self):
		"""
		Property for **self.__search_and_replace** attribute.

		:return: self.__search_and_replace.
		:rtype: SearchAndReplace
		"""

		return self.__search_and_replace

	@search_and_replace.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def search_and_replace(self, value):
		"""
		Setter for **self.__search_and_replace** attribute.

		:param value: Attribute value.
		:type value: SearchAndReplace
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "search_and_replace"))

	@search_and_replace.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def search_and_replace(self):
		"""
		Deleter for **self.__search_and_replace** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "search_and_replace"))

	@property
	def search_in_files(self):
		"""
		Property for **self.__search_in_files** attribute.

		:return: self.__search_in_files.
		:rtype: SearchInFiles
		"""

		return self.__search_in_files

	@search_in_files.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def search_in_files(self, value):
		"""
		Setter for **self.__search_in_files** attribute.

		:param value: Attribute value.
		:type value: SearchInFiles
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "search_in_files"))

	@search_in_files.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def search_in_files(self):
		"""
		Deleter for **self.__search_in_files** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "search_in_files"))

	@property
	def indent_width(self):
		"""
		Property for **self.__indent_width** attribute.

		:return: self.__indent_width.
		:rtype: int
		"""

		return self.__indent_width

	@indent_width.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def indent_width(self, value):
		"""
		Setter for **self.__indent_width** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "indent_width"))

	@indent_width.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def indent_width(self):
		"""
		Deleter for **self.__indent_width** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "indent_width"))

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
	def console(self):
		"""
		Property for **self.__console** attribute.

		:return: self.__console.
		:rtype: dict
		"""

		return self.__console

	@console.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def console(self, value):
		"""
		Setter for **self.__console** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "console"))

	@console.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def console(self):
		"""
		Deleter for **self.__console** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "console"))

	@property
	def memory_handler_stack_depth(self):
		"""
		Property for **self.__memory_handler_stack_depth** attribute.

		:return: self.__memory_handler_stack_depth.
		:rtype: int
		"""

		return self.__memory_handler_stack_depth

	@memory_handler_stack_depth.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def memory_handler_stack_depth(self, value):
		"""
		Setter for **self.__memory_handler_stack_depth** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "memory_handler_stack_depth"))

	@memory_handler_stack_depth.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def memory_handler_stack_depth(self):
		"""
		Deleter for **self.__memory_handler_stack_depth** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "memory_handler_stack_depth"))

	@property
	def menu_bar(self):
		"""
		Property for **self.__menu_bar** attribute.

		:return: self.__menu_bar.
		:rtype: QToolbar
		"""

		return self.__menu_bar

	@menu_bar.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def menu_bar(self, value):
		"""
		Setter for **self.__menu_bar** attribute.

		:param value: Attribute value.
		:type value: QToolbar
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "menu_bar"))

	@menu_bar.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def menu_bar(self):
		"""
		Deleter for **self.__menu_bar** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "menu_bar"))

	@property
	def file_menu(self):
		"""
		Property for **self.__file_menu** attribute.

		:return: self.__file_menu.
		:rtype: QMenu
		"""

		return self.__file_menu

	@file_menu.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def file_menu(self, value):
		"""
		Setter for **self.__file_menu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "file_menu"))

	@file_menu.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def file_menu(self):
		"""
		Deleter for **self.__file_menu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "file_menu"))

	@property
	def edit_menu(self):
		"""
		Property for **self.__edit_menu** attribute.

		:return: self.__edit_menu.
		:rtype: QMenu
		"""

		return self.__edit_menu

	@edit_menu.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def edit_menu(self, value):
		"""
		Setter for **self.__edit_menu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "edit_menu"))

	@edit_menu.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def edit_menu(self):
		"""
		Deleter for **self.__edit_menu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "edit_menu"))

	@property
	def source_menu(self):
		"""
		Property for **self.__source_menu** attribute.

		:return: self.__source_menu.
		:rtype: QMenu
		"""

		return self.__source_menu

	@source_menu.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def source_menu(self, value):
		"""
		Setter for **self.__source_menu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "source_menu"))

	@source_menu.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def source_menu(self):
		"""
		Deleter for **self.__source_menu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "source_menu"))

	@property
	def navigate_menu(self):
		"""
		Property for **self.__navigate_menu** attribute.

		:return: self.__navigate_menu.
		:rtype: QMenu
		"""

		return self.__navigate_menu

	@navigate_menu.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def navigate_menu(self, value):
		"""
		Setter for **self.__navigate_menu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "navigate_menu"))

	@navigate_menu.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def navigate_menu(self):
		"""
		Deleter for **self.__navigate_menu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "navigate_menu"))

	@property
	def search_menu(self):
		"""
		Property for **self.__search_menu** attribute.

		:return: self.__search_menu.
		:rtype: QMenu
		"""

		return self.__search_menu

	@search_menu.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def search_menu(self, value):
		"""
		Setter for **self.__search_menu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "search_menu"))

	@search_menu.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def search_menu(self):
		"""
		Deleter for **self.__search_menu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "search_menu"))

	@property
	def command_menu(self):
		"""
		Property for **self.__command_menu** attribute.

		:return: self.__command_menu.
		:rtype: QMenu
		"""

		return self.__command_menu

	@command_menu.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def command_menu(self, value):
		"""
		Setter for **self.__command_menu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "command_menu"))

	@command_menu.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def command_menu(self):
		"""
		Deleter for **self.__command_menu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "command_menu"))

	@property
	def view_menu(self):
		"""
		Property for **self.__view_menu** attribute.

		:return: self.__view_menu.
		:rtype: QMenu
		"""

		return self.__view_menu

	@view_menu.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def view_menu(self, value):
		"""
		Setter for **self.__view_menu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "view_menu"))

	@view_menu.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def view_menu(self):
		"""
		Deleter for **self.__view_menu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "view_menu"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def activate(self, engine):
		"""
		Activates the Component.

		:param engine: Container to attach the Component to.
		:type engine: QObject
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Activating '{0}' Component.".format(self.__class__.__name__))

		self.__engine = engine
		self.__settings = self.__engine.settings
		self.__settings_section = self.name

		self.__default_script_editor_directory = os.path.join(self.__engine.user_application_data_directory,
															Constants.io_directory,
															self.__default_script_editor_directory)
		not foundations.common.path_exists(self.__default_script_editor_directory) and \
		os.makedirs(self.__default_script_editor_directory)
		self.__default_session_directory = os.path.join(self.__default_script_editor_directory, self.__default_session_directory)
		not foundations.common.path_exists(self.__default_session_directory) and os.makedirs(self.__default_session_directory)
		self.__default_script_editor_file = os.path.join(self.__default_script_editor_directory,
													self.__default_script_editor_file)

		self.__console = code.InteractiveConsole(self.__engine.locals)

		self.activated = True
		return True

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def deactivate(self):
		"""
		Deactivates the Component.

		:return: Method success.
		:rtype: bool
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component cannot be deactivated!".format(self.__class__.__name__, self.__name))

	def initialize_ui(self):
		"""
		Initializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Initializing '{0}' Component ui.".format(self.__class__.__name__))

		self.__model = ProjectsModel(self, default_project=self.__default_project)

		self.Script_Editor_tabWidget = ScriptEditor_QTabWidget(self.__engine)
		self.Script_Editor_tabWidget_frame_gridLayout.addWidget(self.Script_Editor_tabWidget, 0, 0)
		self.__Script_Editor_tabWidget_set_ui()

		self.__recent_files_actions = []
		for i in range(self.__maximum_recent_files):
			self.__recent_files_actions.append(QAction(self.__menu_bar,
													visible=False,
													triggered=self.__load_recent_file__triggered))

		self.__menu_bar = QMenuBar()
		self.__menu_bar.setNativeMenuBar(False)
		self.Menu_Bar_frame_gridLayout.addWidget(self.__menu_bar)
		# Qt 4.8.4: Needs to show the menu_bar, otherwise it doesn't appear.
		self.__menu_bar.show()
		self.__initialize_menu_bar()

		self.Script_Editor_Output_plainTextEdit.setParent(None)
		self.Script_Editor_Output_plainTextEdit = Basic_QPlainTextEdit(self)
		self.Script_Editor_Output_plainTextEdit_frame_gridLayout.addWidget(self.Script_Editor_Output_plainTextEdit, 0, 0)
		self.Script_Editor_Output_plainTextEdit.setObjectName("Script_Editor_Output_plainTextEdit")
		self.__Script_Editor_Output_plainTextEdit_set_ui()

		self.__search_and_replace = SearchAndReplace(self, Qt.Window)
		self.__search_in_files = SearchInFiles(self, Qt.Window)

		self.__initialize_languages_model()

		self.Editor_Status_editorStatus = EditorStatus(self)
		self.__engine.statusBar.insertPermanentWidget(0, self.Editor_Status_editorStatus)

		Editor.get_untitled_file_name = self.__get_untitled_file_name

		# Signals / Slots.
		self.__engine.timer.timeout.connect(self.__Script_Editor_Output_plainTextEdit_refresh_ui)
		self.__engine.content_dropped.connect(self.__engine__content_dropped)
		self.__engine.layouts_manager.layout_restored.connect(self.__engine_layouts_manager__layout_restored)
		self.__engine.file_system_events_manager.file_changed.connect(self.__engine_file_system_events_manager__file_changed)
		self.__engine.file_system_events_manager.file_invalidated.connect(
		self.__engine_file_system_events_manager__file_invalidated)
		self.__engine.file_system_events_manager.directory_changed.connect(
		self.__engine_file_system_events_manager__directory_changed)
		self.__engine.file_system_events_manager.directory_invalidated.connect(
		self.__engine_file_system_events_manager__directory_invalidated)
		self.Script_Editor_tabWidget.tabCloseRequested.connect(self.__Script_Editor_tabWidget__tabCloseRequested)
		self.Script_Editor_tabWidget.currentChanged.connect(self.__Script_Editor_tabWidget__currentChanged)
		self.Script_Editor_tabWidget.content_dropped.connect(self.__Script_Editor_tabWidget__content_dropped)
		self.Script_Editor_tabWidget.tabBar().tabMoved.connect(self.__Script_Editor_tabWidget_tabBar__tabMoved)
		self.visibilityChanged.connect(self.__script_editor__visibilityChanged)
		self.ui_refresh.connect(self.__Script_Editor_Output_plainTextEdit_refresh_ui)
		self.recent_files_changed.connect(self.__set_recent_files_actions)
		self.__model.file_registered.connect(self.__model__file_registered)
		self.__model.file_unregistered.connect(self.__model__file_unregistered)
		self.__model.directory_registered.connect(self.__model__directory_registered)
		self.__model.directory_unregistered.connect(self.__model__directory_unregistered)
		self.__model.project_registered.connect(self.__model__project_registered)
		self.__model.project_unregistered.connect(self.__model__project_unregistered)
		self.__model.editor_registered.connect(self.__model__editor_registered)
		self.__model.editor_unregistered.connect(self.__model__editor_unregistered)

		self.initialized_ui = True
		return True

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def uninitialize_ui(self):
		"""
		Uninitializes the Component ui.

		:return: Method success.
		:rtype: bool
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' Component ui cannot be uninitialized!".format(self.__class__.__name__, self.name))

	def add_widget(self):
		"""
		Adds the Component Widget to the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.addDockWidget(Qt.DockWidgetArea(self.__dock_area), self)

		return True

	def remove_widget(self):
		"""
		Removes the Component Widget from the engine.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing '{0}' Component Widget.".format(self.__class__.__name__))

		self.__engine.removeDockWidget(self)
		self.setParent(None)

		return True

	def on_startup(self):
		"""
		Defines the slot triggered on Framework startup.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'on_startup' method.".format(self.__class__.__name__))

		factory_default_script_editor_file = umbra.ui.common.get_resource_path(self.__factory_default_script_editor_file)
		if foundations.common.path_exists(factory_default_script_editor_file) and \
		not foundations.common.path_exists(self.__default_script_editor_file):
			shutil.copyfile(factory_default_script_editor_file, self.__default_script_editor_file)

		if foundations.common.path_exists(self.__default_script_editor_file):
			self.load_file(self.__default_script_editor_file)
		else:
			self.new_file()

		startup_script = self.__engine.parameters.startup_script
		if foundations.common.path_exists(startup_script):
			self.load_file(startup_script) and self.evaluate_script()

		self.restore_session()

		for argument in self.__engine.arguments[1:]:
			file = os.path.abspath(argument)
			if foundations.common.path_exists(file):
				os.path.isfile(file) and self.load_file(file)

		return True

	def on_close(self):
		"""
		Defines the slot triggered on Framework close.
		"""

		LOGGER.debug("> Calling '{0}' Component Framework 'on_close' method.".format(self.__class__.__name__))

		map(self.unregister_file, self.list_files())

		if self.store_session() and self.close_all_files(leave_first_editor=False):
			return True

	def __initialize_menu_bar(self):
		"""
		Initializes Component menu_bar.
		"""

		self.__file_menu = QMenu("&File", parent=self.__menu_bar)
		self.__file_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&File|&New",
		shortcut=QKeySequence.New,
		slot=self.__new_file_action__triggered))
		self.__file_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&File|&Load ...",
		shortcut=QKeySequence.Open,
		slot=self.__load_file_action__triggered))
		self.__file_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&File|Source ...",
		slot=self.__source_file_action__triggered))
		self.__file_menu.addSeparator()
		self.__file_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&File|Add Project ...",
		slot=self.__add_project_action__triggered))
		self.__file_menu.addSeparator()
		self.__file_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&File|&Save",
		shortcut=QKeySequence.Save,
		slot=self.__save_file_action__triggered))
		self.__file_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&File|Save As ...",
		shortcut=QKeySequence.SaveAs,
		slot=self.__save_file_as_action__triggered))
		self.__file_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&File|Save All",
		slot=self.__save_all_files_action__triggered))
		self.__file_menu.addSeparator()
		self.__file_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&File|Revert",
		slot=self.__revert_file_action__triggered))
		self.__file_menu.addSeparator()
		self.__file_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&File|Close ...",
		shortcut=QKeySequence.Close,
		slot=self.__close_file_action__triggered))
		self.__file_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&File|Close All ...",
		shortcut=Qt.SHIFT + Qt.ControlModifier + Qt.Key_W,
		slot=self.__close_all_files_action__triggered))
		self.__file_menu.addSeparator()
		for action in self.__recent_files_actions:
			self.__file_menu.addAction(action)
		self.__set_recent_files_actions()
		self.__menu_bar.addMenu(self.__file_menu)

		self.__edit_menu = QMenu("&Edit", parent=self.__menu_bar)
		self.__edit_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Edit|&Undo",
		shortcut=QKeySequence.Undo,
		slot=self.__undo_action__triggered))
		self.__edit_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Edit|&Redo",
		shortcut=QKeySequence.Redo,
		slot=self.__redo_action__triggered))
		self.__edit_menu.addSeparator()
		self.__edit_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Edit|Cu&t",
		shortcut=QKeySequence.Cut,
		slot=self.__cut_action__triggered))
		self.__edit_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Edit|&Copy",
		shortcut=QKeySequence.Copy,
		slot=self.__copy_action__triggered))
		self.__edit_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Edit|&Paste",
		shortcut=QKeySequence.Paste,
		slot=self.__paste_action__triggered))
		self.__edit_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Edit|Delete",
		slot=self.__delete_action__triggered))
		self.__edit_menu.addSeparator()
		self.__edit_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Edit|Select All",
		shortcut=QKeySequence.SelectAll,
		slot=self.__select_all_action__triggered))
		self.__menu_bar.addMenu(self.__edit_menu)

		self.__source_menu = QMenu("&Source", parent=self.__menu_bar)
		self.__source_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Source|Delete Line(s)",
		shortcut=Qt.ControlModifier + Qt.Key_D,
		slot=self.__delete_lines_action__triggered))
		self.__source_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Source|Duplicate Line(s)",
		shortcut=Qt.SHIFT + Qt.ControlModifier + Qt.Key_D,
		slot=self.__duplicate_lines_action__triggered))
		self.__source_menu.addSeparator()
		self.__source_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Source|Move Up",
		shortcut=Qt.SHIFT + Qt.ControlModifier + Qt.ALT + Qt.Key_Up,
		slot=self.__move_up_action__triggered))
		self.__source_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Source|Move Down",
		shortcut=Qt.SHIFT + Qt.ControlModifier + Qt.ALT + Qt.Key_Down,
		slot=self.__move_down_action__triggered))
		self.__source_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Source|Indent Selection",
		shortcut=Qt.Key_Tab,
		slot=self.__indent_selection_action__triggered))
		self.__source_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Source|Unindent Selection",
		shortcut=Qt.Key_Backtab,
		slot=self.__unindent_selection_action__triggered))
		self.__source_menu.addSeparator()
		self.__source_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Source|Convert Indentation To Tabs",
		slot=self.__convert_indentation_to_tabs_action__triggered))
		self.__source_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Source|Convert Indentation To Spaces",
		slot=self.__convert_indentation_to_spaces_action__triggered))
		self.__source_menu.addSeparator()
		self.__source_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Source|Remove Trailing WhiteSpaces",
		slot=self.__remove_trailing_white_spaces_action__triggered))
		self.__source_menu.addSeparator()
		self.__source_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Source|Toggle Comments",
		shortcut=Qt.ControlModifier + Qt.Key_Slash,
		slot=self.__toggle_comments_action__triggered))
		self.__menu_bar.addMenu(self.__source_menu)

		self.__navigate_menu = QMenu("&Navigate", parent=self.__menu_bar)
		self.__navigate_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Navigate|Goto Line ...",
		shortcut=Qt.ControlModifier + Qt.Key_L,
		slot=self.__go_to_line_action__triggered))
		self.__navigate_menu.addSeparator()
		self.__menu_bar.addMenu(self.__navigate_menu)

		self.__search_menu = QMenu("&Search", parent=self.__menu_bar)
		self.__search_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Search|Search And Replace ...",
		shortcut=Qt.ControlModifier + Qt.Key_F,
		slot=self.__search_and_replace_action__triggered))
		self.__search_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Search|Search In Files ...",
		shortcut=Qt.ALT + Qt.ControlModifier + Qt.Key_F,
		slot=self.__search_in_files_action__triggered))
		self.__search_menu.addSeparator()
		self.__search_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Search|Search Next",
		shortcut=Qt.ControlModifier + Qt.Key_K,
		slot=self.__search_next_action__triggered))
		self.__search_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Search|Search Previous",
		shortcut=Qt.SHIFT + Qt.ControlModifier + Qt.Key_K,
		slot=self.__search_previous_action__triggered))
		self.__menu_bar.addMenu(self.__search_menu)

		self.__command_menu = QMenu("&Command", parent=self.__menu_bar)
		self.__command_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Command|&Evaluate Selection",
		shortcut=Qt.ControlModifier + Qt.Key_Return,
		slot=self.__evaluate_selection_action__triggered))
		self.__command_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&Command|Evaluate &Script",
		shortcut=Qt.SHIFT + Qt.CTRL + Qt.Key_Return,
		slot=self.__evaluate_script_action__triggered))
		self.__menu_bar.addMenu(self.__command_menu)

		self.__view_menu = QMenu("&View", parent=self.__menu_bar)
		self.__view_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&View|Increase Font Size",
		shortcut=Qt.ControlModifier + Qt.Key_Plus,
		slot=self.__increase_font_size_action__triggered))
		self.__view_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&View|Decrease Font Size",
		shortcut=Qt.ControlModifier + Qt.Key_Minus,
		slot=self.__decrease_font_size_action__triggered))
		self.__view_menu.addSeparator()
		self.__view_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&View|Toggle Word Wrap",
		slot=self.__toggle_word_wrap_action__triggered))
		self.__view_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&View|Toggle White Spaces",
		slot=self.__toggle_white_spaces_action__triggered))
		self.__view_menu.addSeparator()
		self.__view_menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|&View|Loop Through Editors",
		shortcut=Qt.AltModifier + Qt.SHIFT + Qt.Key_Tab,
		slot=self.__loop_through_editors_action__triggered))
		self.__menu_bar.addMenu(self.__view_menu)

	@foundations.trace.untracable
	def __Script_Editor_Output_plainTextEdit_set_ui(self):
		"""
		Sets the **Script_Editor_Output_plainTextEdit** Widget.
		"""

		self.Script_Editor_Output_plainTextEdit.setReadOnly(True)
		self.Script_Editor_Output_plainTextEdit.highlighter = umbra.ui.highlighters.DefaultHighlighter(
																 self.Script_Editor_Output_plainTextEdit.document(),
																 LOGGING_LANGUAGE.rules,
																 LOGGING_LANGUAGE.theme)

		self.Script_Editor_Output_plainTextEdit.setTabStopWidth(self.__indent_width)
		self.Script_Editor_Output_plainTextEdit.setWordWrapMode(QTextOption.NoWrap)
		if platform.system() == "Windows" or platform.system() == "Microsoft":
			fontFamily, fontSize = self.__default_fonts_settings["Windows"]
		elif platform.system() == "Darwin":
			fontFamily, fontSize = self.__default_fonts_settings["Darwin"]
		elif platform.system() == "Linux":
			fontFamily, fontSize = self.__default_fonts_settings["Linux"]
		font = QFont(fontFamily)
		font.setPointSize(fontSize)
		self.Script_Editor_Output_plainTextEdit.setFont(font)
		self.Script_Editor_Output_plainTextEdit.contextMenuEvent = \
		self.__Script_Editor_Output_plainTextEdit_contextMenuEvent
		self.__Script_Editor_Output_plainTextEdit_set_default_view_state()

	@foundations.trace.untracable
	def __Script_Editor_Output_plainTextEdit_set_default_view_state(self):
		"""
		Sets the **Script_Editor_Output_plainTextEdit** Widget default View state.
		"""

		self.Script_Editor_Output_plainTextEdit.moveCursor(QTextCursor.End)
		self.Script_Editor_Output_plainTextEdit.ensureCursorVisible()

	@foundations.trace.untracable
	def __Script_Editor_Output_plainTextEdit_refresh_ui(self):
		"""
		Updates the **Script_Editor_Output_plainTextEdit** Widget.
		"""

		memory_handler_stack_depth = len(self.__engine.logging_session_handler_stream.stream)
		if memory_handler_stack_depth != self.__memory_handler_stack_depth:
			for line in self.__engine.logging_session_handler_stream.stream[
			self.__memory_handler_stack_depth:memory_handler_stack_depth]:
				self.Script_Editor_Output_plainTextEdit.moveCursor(QTextCursor.End)
				self.Script_Editor_Output_plainTextEdit.insertPlainText(line)
			self.__Script_Editor_Output_plainTextEdit_set_default_view_state()
			self.__memory_handler_stack_depth = memory_handler_stack_depth

	def __Script_Editor_Output_plainTextEdit_contextMenuEvent(self, event):
		"""
		Reimplements the :meth:`QPlainTextEdit.contextMenuEvent` method.

		:param event: QEvent.
		:type event: QEvent
		"""

		menu = self.Script_Editor_Output_plainTextEdit.createStandardContextMenu()
		menu.addSeparator()
		menu.addAction(self.__engine.actions_manager.register_action(
		"Actions|Umbra|Components|factory.script_editor|Edit Selected Path",
		slot=self.__edit_selected_path_action__triggered))
		menu.exec_(event.globalPos())

	def __Script_Editor_tabWidget_set_ui(self):
		"""
		Sets the **Script_Editor_tabWidget** Widget.
		"""

		self.Script_Editor_tabWidget.setTabsClosable(True)
		self.Script_Editor_tabWidget.setMovable(True)

	def __Script_Editor_tabWidget__tabCloseRequested(self, index):
		"""
		Defines the slot triggered by **Script_Editor_tabWidget** Widget when a tab is requested to be closed.

		:param index: Tab index.
		:type index: int
		"""

		LOGGER.debug("> Closing tab with index '{0}'.".format(index))

		self.Script_Editor_tabWidget.setCurrentIndex(index)
		return self.close_file()

	def __Script_Editor_tabWidget__currentChanged(self, index):
		"""
		Defines the slot triggered by **Script_Editor_tabWidget** Widget when the current tab is changed.

		:param index: Tab index.
		:type index: int
		"""

		LOGGER.debug("> Current tab changed to '{0}' index.".format(index))

		self.Editor_Status_editorStatus._EditorStatus__Languages_comboBox_set_default_view_state()
		self.__set_window_title()

	def __Script_Editor_tabWidget__content_dropped(self, event):
		"""
		Defines the slot triggered by content when dropped in the **Script_Editor_tabWidget** Widget.

		:param event: Event.
		:type event: QEvent
		"""

		self.__handle_dropped_content(event)

	def __Script_Editor_tabWidget_tabBar__tabMoved(self, to_index, from_index):
		"""
		Defines the slot triggered by a **Script_Editor_tabWidget** Widget tab when moved.

		:param to_index: Index to.
		:type to_index: int
		:param from_index: Index from.
		:type from_index: int
		"""

		editor = self.get_current_editor()
		if not editor:
			return

		editor_node = foundations.common.get_first_item(self.__model.get_editor_nodes(editor))
		file_node = editor_node.parent
		project_node = file_node.parent

		self.__model.move_node(project_node, from_index, to_index)

	def __engine__content_dropped(self, event):
		"""
		Defines the slot triggered by content when dropped into the engine.

		:param event: Event.
		:type event: QEvent
		"""

		self.__handle_dropped_content(event)

	def __engine_layouts_manager__layout_restored(self, current_layout):
		"""
		Defines the slot triggered by the engine layout when changed.

		:param current_layout: Current layout.
		:type current_layout: unicode
		"""

		self.Editor_Status_editorStatus.setVisible(not self.isHidden())

	def __engine_file_system_events_manager__file_changed(self, file):
		"""
		Defines the slot triggered by the **file_system_events_manager** when a file is changed.

		:param file: File changed.
		:type file: unicode
		"""

		file = foundations.strings.to_string(file)
		self.search_in_files._SearchInFiles__uncache(file)
		self.reload_file(file)

	def __engine_file_system_events_manager__file_invalidated(self, file):
		"""
		Defines the slot triggered by the **file_system_events_manager** when a file is invalidated.

		:param file: File changed.
		:type file: unicode
		"""

		file = foundations.strings.to_string(file)
		self.search_in_files._SearchInFiles__uncache(file)
		editor = self.get_editor(file)
		editor and	editor.set_modified(True)

	def __engine_file_system_events_manager__directory_changed(self, directory):
		"""
		Defines the slot triggered by the **file_system_events_manager** when a directory is changed.

		:param directory: Directory changed.
		:type directory: unicode
		"""

		for project_node in self.__model.list_project_nodes():
			if project_node.path == directory:
				self.__model.update_project_nodes(project_node)
			else:
				for node in foundations.walkers.nodes_walker(project_node):
					if node.path == directory:
						self.__model.update_project_nodes(node)
						break

	def __engine_file_system_events_manager__directory_invalidated(self, directory):
		"""
		Defines the slot triggered by the **file_system_events_manager** when a directory is invalidated.

		:param directory: Directory invalidated.
		:type directory: unicode
		"""

		for project_node in self.__model.list_project_nodes():
			if project_node.path == directory:
				self.__model.unregister_project(project_node)
				break

	def __script_editor__visibilityChanged(self, visibility):
		"""
		Defines the slot triggered by the **script_editor** Component when visibility changed.

		:param visibility: Widget visibility.
		:type visibility: bool
		"""

		self.Editor_Status_editorStatus.setVisible(visibility)

	def __new_file_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&File|&New'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.new_file()

	def __model__file_registered(self, file_node):
		"""
		Defines the slot triggered by Model when a file is registered.

		:param file_node: Registered file FileNode.
		:type file_node: FileNode
		"""

		self.register_node_path(file_node)

	def __model__file_unregistered(self, file_node):
		"""
		Defines the slot triggered by Model when a file is unregistered.

		:param file_node: Unregistered file FileNode.
		:type file_node: FileNode
		"""

		self.unregister_node_path(file_node)

	def __model__directory_registered(self, directory_node):
		"""
		Defines the slot triggered by Model when a directory is registered.

		:param directory_node: Registered directory DirectoryNode.
		:type directory_node: DirectoryNode
		"""

		self.register_node_path(directory_node)

	def __model__directory_unregistered(self, directory_node):
		"""
		Defines the slot triggered by Model when a directory is unregistered.

		:param directory_node: Unregistered directory DirectoryNode.
		:type directory_node: DirectoryNode
		"""

		self.unregister_node_path(directory_node)

	def __model__project_registered(self, project_node):
		"""
		Defines the slot triggered by Model when a project is registered.

		:param project_node: Registered project ProjectNode.
		:type project_node: ProjectNode
		"""

		self.register_node_path(project_node)

	def __model__project_unregistered(self, project_node):
		"""
		Defines the slot triggered by Model when a project is unregistered.

		:param project_node: Unregistered project ProjectNode.
		:type project_node: ProjectNode
		"""

		self.unregister_node_path(project_node)

	def __model__editor_registered(self, editor_node):
		"""
		Defines the slot triggered by Model when an editor is registered.

		:param editor_node: Registered editor EditorNode.
		:type editor_node: EditorNode
		"""

		self.add_editor_tab(editor_node.editor)

	def __model__editor_unregistered(self, editor_node):
		"""
		Defines the slot triggered by Model when an editor is unregistered.

		:param editor_node: Unregistered editor EditorNode.
		:type editor_node: EditorNode
		"""

		self.remove_editor_tab(editor_node.editor)

	def __load_file_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&File|&Load ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.load_file_ui()

	def __source_file_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&File|Source ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if self.load_file_ui():
			return self.evaluate_script()

	def __add_project_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&File|Add Project ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.add_project_ui()

	def __save_file_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&File|&Save'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.save_file()

	def __save_file_as_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&File|Save As ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.save_fileAs()

	def __save_all_files_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&File|Save All'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.save_all_files()

	def __revert_file_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&File|Revert'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.revert_file()

	def __close_file_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&File|Close ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.close_file()

	def __close_all_files_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&File|Close All ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.close_all_files()

	def __load_recent_file__triggered(self, checked):
		"""
		Defines the slot triggered by any recent file related action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		file = self.sender().data
		if foundations.common.path_exists(file):
			return self.load_file(file)

	def __undo_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Edit|&Undo'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.has_editor_tab():
			return False

		self.get_current_editor().undo()
		return True

	def __redo_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Edit|&Redo'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.has_editor_tab():
			return False

		self.get_current_editor().redo()
		return True

	def __cut_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Edit|Cu&t'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		current_widget = self.get_focus_widget()
		if not current_widget:
			return False

		if current_widget.objectName() == "Script_Editor_Output_plainTextEdit":
			current_widget.copy()
		else:
			current_widget.cut()
		return True

	def __copy_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Edit|&Copy'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		current_widget = self.get_focus_widget()
		if not current_widget:
			return False

		current_widget.copy()
		return True

	def __paste_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Edit|&Paste'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.has_editor_tab():
			return False

		self.get_current_editor().paste()
		return True

	def __delete_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Edit|Delete'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.has_editor_tab():
			return False

		self.get_current_editor().delete()
		return True

	def __select_all_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Edit|Select All'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		current_widget = self.get_focus_widget()
		if not current_widget:
			return False

		current_widget.selectAll()
		return True

	def __delete_lines_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Source|Delete Line(s)'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.has_editor_tab():
			return False

		return self.get_current_editor().delete_lines()

	def __duplicate_lines_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Source|Duplicate Line(s)'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.has_editor_tab():
			return False

		return self.get_current_editor().duplicate_lines()

	def __move_up_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Source|Move Up'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.has_editor_tab():
			return False

		return self.get_current_editor().move_lines_up()

	def __move_down_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Source|Move Down'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.has_editor_tab():
			return False

		return self.get_current_editor().move_lines_down()

	def __indent_selection_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Source|Indent Selection'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.has_editor_tab():
			return False

		return self.get_current_editor().indent()

	def __unindent_selection_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Source|Unindent Selection'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.has_editor_tab():
			return False

		return self.get_current_editor().unindent()

	def __convert_indentation_to_tabs_action__triggered(self, checked):
		"""
		Defines the slot triggered by
		**'Actions|Umbra|Components|factory.script_editor|&Source|Convert Identation To Tabs'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.has_editor_tab():
			return False

		return self.get_current_editor().convert_indentation_to_tabs()

	def __convert_indentation_to_spaces_action__triggered(self, checked):
		"""
		Defines the slot triggered by
		**'Actions|Umbra|Components|factory.script_editor|&Source|Convert Identation To Spaces'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.has_editor_tab():
			return False

		return self.get_current_editor().convert_indentation_to_spaces()

	def __remove_trailing_white_spaces_action__triggered(self, checked):
		"""
		Defines the slot triggered by
		**'Actions|Umbra|Components|factory.script_editor|&Source|Remove Trailing WhiteSpaces'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.has_editor_tab():
			return False

		return self.get_current_editor().remove_trailing_white_spaces()

	def __toggle_comments_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Source|Toggle Comments'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.has_editor_tab():
			return False

		return self.get_current_editor().toggle_comments()

	def __go_to_line_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Navigate|Goto Line ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.go_to_line()

	def __search_and_replace_action__triggered(self, checked):
		"""
		Defines the slot triggered by
		**'Actions|Umbra|Components|factory.script_editor|&Search|Search And Replace ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.search_and_replace_ui()

	def __search_in_files_action__triggered(self, checked):
		"""
		Defines the slot triggered by
		**'Actions|Umbra|Components|factory.script_editor|&Search|Search In Files ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.search_in_files_ui()

	def __search_next_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Search|Search Next'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.has_editor_tab():
			return False

		return self.get_current_editor().search_next()

	def __search_previous_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Search|Search Previous'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		if not self.has_editor_tab():
			return False

		return self.get_current_editor().search_previous()

	def __evaluate_selection_action__triggered(self, checked):
		"""
		Defines the slot triggered by
		**'Actions|Umbra|Components|factory.script_editor|&Command|&Evaluate Selection'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.evaluate_selection()

	def __evaluate_script_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&Command|Evaluate &Script'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.evaluate_script()

	def __increase_font_size_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&View|Increase Font Size'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		current_widget = self.get_focus_widget()
		if not current_widget:
			return False

		return current_widget.zoom_in()

	def __decrease_font_size_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&View|Decrease Font Size'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		current_widget = self.get_focus_widget()
		if not current_widget:
			return False

		return current_widget.zoom_out()

	def __toggle_word_wrap_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&View|Toggle Word Wrap'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		current_widget = self.get_focus_widget()
		if not current_widget:
			return False

		return current_widget.toggle_word_wrap()

	def __toggle_white_spaces_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&View|Toggle White Spaces'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		current_widget = self.get_focus_widget()
		if not current_widget:
			return False

		return current_widget.toggle_white_spaces()

	def __loop_through_editors_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|&View|Loop Through Editors'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.loop_through_editors()

	def __edit_selected_path_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|Components|factory.script_editor|Edit Selected Path'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		return self.load_path(foundations.strings.to_string(self.Script_Editor_Output_plainTextEdit.get_selected_text()))

	def __editor__patterns_replaced(self, patterns):
		"""
		Defines the slot triggered by an editor when patterns have been replaced.
		"""

		replacedPatternsCount = len(patterns)
		replacedPatternsCount and self.__engine.notifications_manager.notify(
		"{0} | '{1}' pattern(s) replaced!".format(self.__class__.__name__, replacedPatternsCount))

	def __editor__title_changed(self):
		"""
		Defines the slot triggered by an editor when title is changed.
		"""

		self.__set_tab_title(self.get_editorTab(self.sender()))
		self.__set_window_title()

	def __editor__file_loaded(self):
		"""
		Defines the slot triggered by an editor when file is loaded.
		"""

		self.register_node_path(self.sender())

	def __editor__file_saved(self):
		"""
		Defines the slot triggered by an editor when file is saved.
		"""

		self.register_node_path(self.sender())

	def __editor__language_changed(self):
		"""
		Defines the slot triggered by an editor when language is changed.
		"""

		self.Editor_Status_editorStatus._EditorStatus__Languages_comboBox_set_default_view_state()

	def __editor__modification_changed(self, changed):
		"""
		Defines the slot triggered by an editor when document is modified.

		:param changed: File modification state.
		:type changed: bool
		"""

		if self.sender() is not None:
			self.search_in_files._SearchInFiles__uncache(self.sender().file)

	def __initialize_languages_model(self):
		"""
		Initializes the languages Model.
		"""

		languages = [PYTHON_LANGUAGE, LOGGING_LANGUAGE, TEXT_LANGUAGE]
		existingGrammarFiles = [os.path.normpath(language.file) for language in languages]

		for directory in RuntimeGlobals.resources_directories:
			for file in foundations.walkers.files_walker(directory, ("\.{0}$".format(self.__extension),), ("\._",)):
				if os.path.normpath(file) in existingGrammarFiles:
					continue

				languageDescription = get_language_description(file)
				if not languageDescription:
					continue

				LOGGER.debug("> Adding '{0}' language to model.".format(languageDescription))
				languages.append(languageDescription)

		self.__languages_model = LanguagesModel(self, sorted(languages, key=lambda x: (x.name)))
		self.__get_supported_file_types_string()

	@umbra.engine.encapsulate_processing
	def __handle_dropped_content(self, event):
		"""
		Handles dopped content event.

		:param event: Content dropped event.
		:type event: QEvent
		"""

		if not event.mimeData().hasUrls():
			return

		urls = event.mimeData().urls()

		self.__engine.start_processing("Loading Files ...", len(urls))
		for url in event.mimeData().urls():
			path = foundations.strings.to_string(url.path())
			LOGGER.debug("> Handling dropped '{0}' file.".format(path))
			path = (platform.system() == "Windows" or platform.system() == "Microsoft") and \
			re.search(r"^\/[A-Z]:", path) and path[1:] or path
			self.load_path(path) and self.restore_development_layout()
			self.__engine.step_processing()
		self.__engine.stop_processing()

	def __get_supported_file_types_string(self):
		"""
		Returns the supported file types dialog string.
		"""

		languages = ["All Files (*)"]
		for language in self.__languages_model.languages:
			languages.append("{0} Files ({1})".format(language.name,
													" ".join(language.extensions.split("|")).replace("\\", "*")))
		return ";;".join(languages)

	def __set_recent_files_actions(self):
		"""
		Sets the recent files actions.
		"""

		recentFiles = [foundations.strings.to_string(file)
					for file in self.__settings.get_key(self.__settings_section, "recentFiles").toStringList()
					if foundations.common.path_exists(file)]
		if not recentFiles:
			return

		numberRecentFiles = min(len(recentFiles), self.__maximum_recent_files)

		for i in range(self.__maximum_recent_files):
			if i >= numberRecentFiles:
				self.__recent_files_actions[i].setVisible(False)
				continue

			LOGGER.debug("> Adding '{0}' file to recent files actions.".format(recentFiles[i]))

			self.__recent_files_actions[i].setText("{0} {1}".format(i + 1, os.path.basename(
			foundations.strings.to_string(recentFiles[i]))))
			self.__recent_files_actions[i].data = foundations.strings.to_string(recentFiles[i])
			self.__recent_files_actions[i].setVisible(True)

	def __store_recent_file(self, file):
		"""
		Stores given recent file into the settings.

		:param file: File to store.
		:type file: unicode
		"""

		LOGGER.debug("> Storing '{0}' file in recent files.".format(file))

		recentFiles = [foundations.strings.to_string(recentFile)
					for recentFile in self.__settings.get_key(self.__settings_section, "recentFiles").toStringList()
					if foundations.common.path_exists(recentFile)]
		if not recentFiles:
			recentFiles = []

		if file in recentFiles:
			recentFiles.pop(recentFiles.index(file))
		recentFiles.insert(0, file)
		del recentFiles[self.__maximum_recent_files:]
		recentFiles = self.__settings.set_key(self.__settings_section, "recentFiles", recentFiles)
		self.recent_files_changed.emit()

	def __set_window_title(self):
		"""
		Sets the Component window title.
		"""

		if self.has_editor_tab():
			windowTitle = "{0} - {1}".format(self.__default_window_title, self.get_current_editor().file)
		else:
			windowTitle = "{0}".format(self.__default_window_title)

		LOGGER.debug("> Setting 'Script Editor' window title to '{0}'.".format(windowTitle))
		self.setWindowTitle(windowTitle)

	def __set_tab_title(self, index):
		"""
		Sets the name and toolTip of the **Script_Editor_tabWidget** Widget tab with given index.

		:param index: Index of the tab containing the Model editor.
		:type index: int
		"""

		editor = self.get_widget(index)
		if not editor:
			return

		title, tool_tip = foundations.strings.to_string(editor.title), foundations.strings.to_string(editor.file)
		LOGGER.debug("> Setting '{0}' window title and '{1}' toolTip to tab with '{2}' index.".format(title, tool_tip, index))
		# TODO: https://bugreports.qt-project.org/browse/QTBUG-27084
		color = QColor(224, 224, 224) if editor.is_modified() else QColor(160, 160, 160)
		self.Script_Editor_tabWidget.tabBar().setTabTextColor(index, color)
		tabText = self.Script_Editor_tabWidget.tabText(index)
		tabText != title and self.Script_Editor_tabWidget.setTabText(index, title)
		self.Script_Editor_tabWidget.setTabToolTip(index, tool_tip)

	def __has_editor_lock(self, editor):
		"""
		Returns if given editor has a lock.

		:param editor: Editor.
		:type editor: Editor
		:return: Has editor lock.
		:rtype: bool
		"""

		return hasattr(editor, "__lock")

	def __lock_editor(self, editor):
		"""
		Locks given editor.

		:param editor: Editor.
		:type editor: Editor
		"""

		setattr(editor, "__lock", True)

	def __unlock_editor(self, editor):
		"""
		Locks given editor.

		:param editor: Editor.
		:type editor: Editor
		"""

		delattr(editor, "__lock")

	def __get_untitled_file_name(self):
		"""
		Returns an untitled file name.

		:return: Untitled file name.
		:rtype: unicode
		"""

		untitledNameId = Editor._Editor__untitled_name_id
		for file in self.list_files():
			if not os.path.dirname(file) == self.__default_session_directory:
				continue

			search = re.search(r"\d+", os.path.basename(file))
			if not search:
				continue

			untitledNameId = max(int(search.group(0)), untitledNameId) + 1

		name = "{0} {1}.{2}".format(self.__default_file_name, untitledNameId, self.__default_file_extension)
		Editor._Editor__untitled_name_id += 1
		LOGGER.debug("> Next untitled file name: '{0}'.".format(name))
		return name

	def register_file(self, file):
		"""
		Registers given file in the **file_system_events_manager**.

		:param file: File.
		:type file: unicode
		:return: Method success.
		:rtype: bool
		"""

		not self.__engine.file_system_events_manager.is_path_registered(file) and \
		self.__engine.file_system_events_manager.register_path(file)
		return True

	def unregister_file(self, file):
		"""
		Unregisters given file in the **file_system_events_manager**.

		:param file: File.
		:type file: unicode
		:return: Method success.
		:rtype: bool
		"""

		self.__engine.file_system_events_manager.is_path_registered(file) and \
		self.__engine.file_system_events_manager.unregister_path(file)
		return True

	def register_node_path(self, node):
		"""
		Registers given Node path in the **file_system_events_manager**.

		:param node: Node.
		:type node: FileNode or DirectoryNode or ProjectNode
		:return: Method success.
		:rtype: bool
		"""

		path = node.file if hasattr(node, "file") else node.path
		path = foundations.strings.to_string(path)
		if not foundations.common.path_exists(path):
			return False

		return self.register_file(path)

	def unregister_node_path(self, node):
		"""
		Unregisters given Node path from the **file_system_events_manager**.

		:param node: Node.
		:type node: FileNode or DirectoryNode or ProjectNode
		:return: Method success.
		:rtype: bool
		"""

		path = node.file if hasattr(node, "file") else node.path
		path = foundations.strings.to_string(path)

		return self.unregister_file(path)

	def load_file_ui(self):
		"""
		Loads user chosen file(s) into **Script_Editor_tabWidget** Widget tab Model editor(s).

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		editor = self.get_current_editor()
		file = editor and editor.file or None

		browsedPath = os.path.dirname(file) if foundations.common.path_exists(file) else RuntimeGlobals.last_browsed_path
		files = umbra.ui.common.store_last_browsed_path(QFileDialog.getOpenFileNames(self,
																				"Load File(s):",
																				browsedPath,
																				self.__get_supported_file_types_string()))
		if not files:
			return False

		success = True
		for file in files:
			success *= self.load_file(file)
		return success

	def add_project_ui(self):
		"""
		Adds user chosen project **Script_Editor_tabWidget** Widget tab Model.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		directory = umbra.ui.common.store_last_browsed_path(QFileDialog.getExistingDirectory(self,
																				"Add Project:",
																				RuntimeGlobals.last_browsed_path))
		if not directory:
			return False

		return self.add_project(directory)

	def search_and_replace_ui(self):
		"""
		Performs a search and replace in the current **Script_Editor_tabWidget** Widget tab Model editor.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		self.__search_and_replace.show()
		return True

	def search_in_files_ui(self):
		"""
		Performs a search in the current user chosen files.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		self.__search_in_files.show()
		return True

	def get_widget(self, index):
		"""
		Returns the **Script_Editor_tabWidget** Widget associated with given index.

		:param index: Tab index.
		:type index: int
		:return: Widget.
		:rtype: QWidget
		"""

		if index is not None:
			return self.Script_Editor_tabWidget.widget(index)

	def get_focus_widget(self):
		"""
		Returns the Widget with focus.

		:return: Widget with focus.
		:rtype: QWidget
		"""

		current_widget = QApplication.focusWidget()
		if current_widget is None:
			return False

		if current_widget.objectName() == "Script_Editor_Output_plainTextEdit" or \
			isinstance(current_widget, Editor):
			return current_widget

	def get_editorTab(self, editor):
		"""
		Returns the **Script_Editor_tabWidget** Widget tab associated with the given editor.

		:param editor: Editor to search tab for.
		:type editor: Editor
		:return: Tab index.
		:rtype: Editor
		"""

		for i in range(self.Script_Editor_tabWidget.count()):
			if not self.get_widget(i) == editor:
				continue

			LOGGER.debug("> Editor '{0}': Tab index '{1}'.".format(editor, i))
			return i

	def add_editor_tab(self, editor):
		"""
		Adds a new tab to the **Script_Editor_tabWidget** Widget and sets the given editor as child widget.

		:param editor: Editor.
		:type editor: Editor
		:return: New tab index.
		:rtype: int
		"""

		index = self.Script_Editor_tabWidget.addTab(editor, editor.get_file_short_name())
		LOGGER.debug("> Assigning '{0}' editor to '{1}' tab index.".format(editor, index))
		self.Script_Editor_tabWidget.setCurrentIndex(index)
		self.__set_tab_title(index)

		# Signals / Slots.
		editor.patterns_replaced.connect(self.__editor__patterns_replaced)
		editor.title_changed.connect(self.__editor__title_changed)
		editor.file_loaded.connect(self.__editor__file_loaded)
		editor.file_saved.connect(self.__editor__file_saved)
		editor.language_changed.connect(self.__editor__language_changed)
		editor.modification_changed.connect(self.__editor__modification_changed)
		editor.cursorPositionChanged.connect(self.Editor_Status_editorStatus._EditorStatus__editor__cursorPositionChanged)
		return index

	def remove_editor_tab(self, editor):
		"""
		Removes the **Script_Editor_tabWidget** Widget tab with given editor.

		:param editor: Editor.
		:type editor: Editor
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Removing tab with Editor '{0}'.".format(editor))
		self.Script_Editor_tabWidget.removeTab(self.get_editorTab(editor))
		return True

	def find_editor_tab(self, file):
		"""
		Finds the **Script_Editor_tabWidget** Widget tab associated to the given file.

		:param file: File to search tab for.
		:type file: unicode
		:return: Tab index.
		:rtype: Editor
		"""

		for i in range(self.Script_Editor_tabWidget.count()):
			if not self.get_widget(i).file == file:
				continue

			LOGGER.debug("> File '{0}': Tab index '{1}'.".format(file, i))
			return i

	def has_editor_tab(self):
		"""
		Returns if the **Script_Editor_tabWidget** Widget has at least one tab.

		:return: Has tab.
		:rtype: bool
		"""

		return self.Script_Editor_tabWidget.count() and True or False

	def get_current_editor(self):
		"""
		Returns the current **Script_Editor_tabWidget** Widget tab Model editor.

		:return: Current editor.
		:rtype: Editor
		"""

		if not self.has_editor_tab():
			return

		return self.Script_Editor_tabWidget.currentWidget()

	def set_current_editor(self, file):
		"""
		Focus the **Script_Editor_tabWidget** Widget tab Model editor with given file.

		:param file: File.
		:type file: unicode
		:return: Method success.
		:rtype: bool
		"""

		index = self.find_editor_tab(file)
		if index is not None:
			self.Script_Editor_tabWidget.setCurrentIndex(index)
			return True

	def load_path(self, path):
		"""
		Loads given path.

		:param path: Path to load.
		:type path: unicode
		:return: Method success.
		:rtype: bool
		"""

		if not foundations.common.path_exists(path):
			return False

		if os.path.isfile(path):
			if path in self.list_files():
				self.set_current_editor(path)
			else:
				self.load_file(path)
		else:
			if not path in self.list_projects():
				self.add_project(path)
		return True

	def load_document(self, document, file):
		"""
		Loads given document into a new **Script_Editor_tabWidget** Widget tab Model editor.

		:param document: Document to load.
		:type document: QTextDocument
		:param file: Document file.
		:type file: unicode
		:return: Method success.
		:rtype: bool
		"""

		if not foundations.common.path_exists(file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
			self.__class__.__name__, file))

		if self.get_editor(file):
			LOGGER.info("{0} | '{1}' is already loaded!".format(self.__class__.__name__, file))
			return True

		self.close_first_file()
		language = self.__languages_model.get_language(self.__default_language)
		editor = Editor(parent=self, language=language)
		if not editor.new_file():
			return False

		LOGGER.info("{0} | Loading '{1}' file document!".format(self.__class__.__name__, file))
		language = self.__languages_model.get_file_language(file) or self.__languages_model.get_language(self.__default_language)
		if not editor.load_document(document, file, language):
			return False

		if self.__model.set_authoring_nodes(editor):
			self.__store_recent_file(file)
			self.file_loaded.emit(file)
			return True

	def add_project(self, path):
		"""
		Adds a project.

		:param path: Project path.
		:type path: unicode
		:return: Method success.
		:rtype: bool
		"""

		if not foundations.common.path_exists(path):
			return False

		path = os.path.normpath(path)
		if self.__model.get_project_nodes(path):
			self.__engine.notifications_manager.warnify(
			"{0} | '{1}' project is already opened!".format(self.__class__.__name__, path))
			return False

		LOGGER.info("{0} | Adding '{1}' project!".format(self.__class__.__name__, path))
		project_node = self.__model.register_project(path)
		if not project_node:
			return False

		self.__model.set_project_nodes(project_node)
		return True

	def remove_project(self, path):
		"""
		Removes a project.

		:param path: Project path.
		:type path: unicode
		:return: Method success.
		:rtype: bool
		"""

		project_node = foundations.common.get_first_item(self.__model.get_project_nodes(path))
		if not project_node:
			self.__engine.notifications_manager.warnify(
			"{0} | '{1}' project is not opened!".format(self.__class__.__name__, path))
			return False

		LOGGER.info("{0} | Removing '{1}' project!".format(self.__class__.__name__, path))
		self.__model.delete_project_nodes(project_node)
		return True

	def new_file(self):
		"""
		Creates a new file into a new **Script_Editor_tabWidget** Widget tab.

		:return: Method success.
		:rtype: bool
		"""

		language = self.__languages_model.get_language(self.__default_script_language)
		editor = Editor(parent=self, language=language)

		file = editor.new_file()
		if not file:
			return False

		LOGGER.info("{0} | Creating '{1}' file!".format(self.__class__.__name__, file))

		if self.__model.set_authoring_nodes(editor):
			self.__store_recent_file(file)
			self.file_loaded.emit(file)
			return True

	@foundations.exceptions.handle_exceptions(foundations.exceptions.FileExistsError)
	def load_file(self, file):
		"""
		Loads user chosen file in a new **Script_Editor_tabWidget** Widget tab Model editor.

		:param file: File to load.
		:type file: unicode
		:return: Method success.
		:rtype: bool
		"""

		if not foundations.common.path_exists(file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
			self.__class__.__name__, file))

		if self.get_editor(file):
			LOGGER.info("{0} | '{1}' is already loaded!".format(self.__class__.__name__, file))
			return True

		self.close_first_file()

		LOGGER.info("{0} | Loading '{1}' file!".format(self.__class__.__name__, file))
		language = self.__languages_model.get_file_language(file) or self.__languages_model.get_language(self.__default_language)
		editor = Editor(parent=self, language=language)

		if not editor.load_file(file):
			return False

		if self.__model.set_authoring_nodes(editor):
			self.__store_recent_file(file)
			self.file_loaded.emit(file)
			return True

	@foundations.exceptions.handle_exceptions(foundations.exceptions.FileExistsError)
	def reload_file(self, file, is_modified=True):
		"""
		Reloads given file **Script_Editor_tabWidget** Widget tab Model editor content.

		:param file: File to reload.
		:type file: unicode
		:param is_modified: File modified state.
		:type is_modified: bool
		:return: Method success.
		:rtype: bool
		"""

		if not foundations.common.path_exists(file):
			raise foundations.exceptions.FileExistsError("{0} | '{1}' file doesn't exists!".format(
			self.__class__.__name__, file))

		editor = self.get_editor(file)
		if not editor:
			return False

		if self.__has_editor_lock(editor):
			self.__unlock_editor(editor)
			return True

		LOGGER.info("{0} | Reloading '{1}' file!".format(self.__class__.__name__, file))
		return editor.reload_file(is_modified)

	def save_file(self, file=None):
		"""
		Saves either given file or current **Script_Editor_tabWidget** Widget tab Model editor file.

		:param file: File to save.
		:type file: unicode
		:return: Method success.
		:rtype: bool
		"""

		editor = file and self.get_editor(file) or self.get_current_editor()
		if not editor:
			return False

		LOGGER.info("{0} | Saving '{1}' file!".format(self.__class__.__name__, editor.file))
		self.__lock_editor(editor)
		if not editor.is_untitled and foundations.common.path_exists(editor.file):
			return editor.save_file()
		else:
			return self.save_fileAs()

	@foundations.exceptions.handle_exceptions(umbra.exceptions.notify_exception_handler,
											foundations.exceptions.UserError)
	def save_fileAs(self):
		"""
		Saves current **Script_Editor_tabWidget** Widget tab Model editor file as user chosen file.

		:return: Method success.
		:rtype: bool
		"""

		editor = self.get_current_editor()
		if not editor:
			return False

		file = umbra.ui.common.store_last_browsed_path(QFileDialog.getSaveFileName(self, "Save As:", editor.file))
		if not file:
			return False

		candidate_editor = self.get_editor(file)
		if candidate_editor:
			if not candidate_editor is editor:
				raise foundations.exceptions.UserError("{0} | '{1}' file is already opened!".format(
				self.__class__.__name__, file))
			else:
				return self.save_file(file)

		LOGGER.info("{0} | Saving '{1}' file!".format(self.__class__.__name__, file))
		self.__lock_editor(editor)
		self.unregister_node_path(editor)
		if editor.save_fileAs(file):
			self.__model.update_authoring_nodes(editor)
			language = self.__languages_model.get_file_language(file) or self.__languages_model.get_language(self.__default_language)
			if editor.language.name != language.name:
				self.set_language(editor, language)
			return True

	@umbra.engine.encapsulate_processing
	def save_all_files(self):
		"""
		Saves all **Script_Editor_tabWidget** Widget tab Model editor files.

		:return: Method success.
		:rtype: bool
		"""

		self.__engine.start_processing("Saving All Files ...", len(self.list_editors()))
		success = True
		for file in self.list_files():
			success *= self.save_file(file)
			self.__engine.step_processing()
		self.__engine.stop_processing()
		return success

	@umbra.engine.encapsulate_processing
	def revert_file(self, file=None):
		"""
		Reverts either given file or current **Script_Editor_tabWidget** Widget tab Model editor file.

		:param file: File to revert.
		:type file: unicode
		:return: Method success.
		:rtype: bool
		"""

		editor = file and self.get_editor(file) or self.get_current_editor()
		if not editor:
			return False

		file = editor.file
		LOGGER.info("{0} | Reverting '{1}' file!".format(self.__class__.__name__, file))
		if self.reload_file(file, is_modified=False):
			return True

	def close_file(self, file=None, leave_first_editor=True):
		"""
		Closes either given file or current **Script_Editor_tabWidget** Widget tab Model editor file.

		:param file: File to save.
		:type file: unicode
		:param leave_first_editor: Leave first editor.
		:type leave_first_editor: bool
		:return: Method success.
		:rtype: bool
		"""

		editor = file and self.get_editor(file) or self.get_current_editor()
		if not editor:
			return False

		file = editor.file
		LOGGER.info("{0} | Closing '{1}' file!".format(self.__class__.__name__, file))
		if not editor.close_file():
			return False

		if self.__model.delete_authoring_nodes(editor):
			if not self.has_editor_tab() and leave_first_editor:
				self.new_file()
			self.file_closed.emit(file)
			return True

	# @umbra.engine.encapsulate_processing
	def close_all_files(self, leave_first_editor=True):
		"""
		Closes every opened files and removes their associated **Script_Editor_tabWidget** Widget tabs.

		:return: Method success.
		:rtype: bool
		"""

		# self.__engine.start_processing("Closing All Files ...", len(self.list_editors()))
		success = True
		for file in self.list_files():
			success *= True if self.close_file(file, leave_first_editor) else False
			if not success:
				break

			# self.__engine.step_processing()
		# self.__engine.stop_processing()
		return success

	def close_first_file(self):
		"""
		Attemtps to close the first **Script_Editor_tabWidget** Widget tab Model editor file.

		:return: Method success.
		:rtype: bool
		"""

		editor = self.get_current_editor()
		if len(self.__model.list_editors()) == 1 and editor.is_untitled and not editor.is_modified():
			self.close_file(leave_first_editor=False)
			return True

	def list_editors(self):
		"""
		Returns the Model editors.

		:return: Editors.
		:rtype: list
		"""

		return self.__model.list_editors()

	def list_files(self):
		"""
		Returns the Model files.

		:return: FileNode nodes.
		:rtype: list
		"""

		return self.__model.list_files()

	def list_directories(self):
		"""
		Returns the Model directories.

		:return: DirectoryNode nodes.
		:rtype: list
		"""

		return self.__model.list_directories()

	def list_projects(self, ignore_default_project=True):
		"""
		Returns the Model projects.

		:return: ProjectNode nodes.
		:rtype: list
		"""

		return self.__model.list_projects()

	def get_editor(self, file):
		"""
		Returns the Model editor associated with given file.

		:param file: File to search editors for.
		:type file: unicode
		:return: Editor.
		:rtype: Editor
		"""

		for editor in self.__model.list_editors():
			if editor.file == file:
				return editor

	def set_language(self, editor, language):
		"""
		Sets given language to given Model editor.

		:param editor: Editor to set language to.
		:type editor: Editor
		:param language: Language to set.
		:type language: Language
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Setting '{0}' language to '{1}' editor.".format(language.name, editor))

		return editor.set_language(language)

	def go_to_line(self):
		"""
		Moves current **Script_Editor_tabWidget** Widget tab Model editor cursor to user defined line.

		:return: Method success.
		:rtype: bool

		:note: May require user interaction.
		"""

		editor = self.get_current_editor()
		if not editor:
			return False

		line, state = QInputDialog.getInt(self, "Goto Line Number", "Line number:", min=1)
		if not state:
			return False

		LOGGER.debug("> Chosen line number: '{0}'.".format(line))
		return editor.go_to_line(line)

	def evaluate_selection(self):
		"""
		Evaluates current **Script_Editor_tabWidget** Widget tab Model editor
		selected content in the interactive console.

		:return: Method success.
		:rtype: bool
		"""

		editor = self.get_current_editor()
		if not editor:
			return False

		LOGGER.debug("> Evaluating 'Script Editor' selected content.")
		if self.evaluate_code(foundations.strings.to_string(editor.get_selected_text().replace(QChar(QChar.ParagraphSeparator),
																			QString("\n")))):
			self.ui_refresh.emit()
			return True

	def evaluate_script(self):
		"""
		Evaluates current **Script_Editor_tabWidget** Widget tab Model editor content
		into the interactive console.

		:return: Method success.
		:rtype: bool
		"""

		editor = self.get_current_editor()
		if not editor:
			return False

		LOGGER.debug("> Evaluating 'Script Editor' content.")
		if self.evaluate_code(foundations.strings.to_string(editor.toPlainText().toUtf8())):
			self.ui_refresh.emit()
			return True

	def evaluate_code(self, code):
		"""
		Evaluates given code into the interactive console.

		:param code: Code to evaluate.
		:type code: unicode
		:return: Method success.
		:rtype: bool
		"""

		if not code:
			return False

		LOGGER.debug("> Evaluating given code.")

		code = code.endswith("\n") and code or "{0}\n".format(code)

		code = code.split("\n", 3)
		for i, line in enumerate(code[:-2]):
			if "coding" in line:
				code[i] = line.replace("=", "\=").replace(":", "\:")
				break
		code = "\n".join(code)

		sys.stdout.write(code)
		self.__console.runcode(code)
		return True

	def store_session(self):
		"""
		Stores the current session.

		:return: Method success.
		:rtype: bool
		"""

		session = []
		for editor in self.list_editors():
			file = editor.file
			ignore_file = True
			if editor.is_untitled and not editor.is_empty():
				file = os.path.join(self.__default_session_directory, file)
				editor.write_file(file)
			elif os.path.dirname(file) == self.__default_session_directory:
				editor.save_file()
			session.append(file)

		for directory in self.list_projects():
			if not os.path.exists(directory):
				continue

			session.append(directory)

		LOGGER.debug("> Storing session :'{0}'.".format(session))
		self.__settings.set_key(self.__settings_section, "session", session)
		return True

	def restore_session(self):
		"""
		Restores the stored session.

		:return: Method success.
		:rtype: bool
		"""

		session = [foundations.strings.to_string(path)
					for path in self.__settings.get_key(self.__settings_section, "session").toStringList()
					if foundations.common.path_exists(path)]

		LOGGER.debug("> Restoring session :'{0}'.".format(session))
		success = True
		for path in session:
			if os.path.isfile(path):
				success *= self.load_file(path)
			else:
				success *= self.add_project(path)
		return success


	def loop_through_editors(self, backward=False):
		"""
		Loops through the editor tabs.

		:param backward: Looping backward.
		:type backward: bool
		:return: Method success.
		:rtype: bool
		"""

		step = not backward and 1 or -1
		idx = self.Script_Editor_tabWidget.currentIndex() + step
		if idx < 0:
			idx = self.Script_Editor_tabWidget.count() - 1
		elif idx > self.Script_Editor_tabWidget.count() - 1:
			idx = 0
		self.Script_Editor_tabWidget.setCurrentIndex(idx)
		return True

	def restore_development_layout(self):
		"""
		Restores the development layout.

		:return: Definition success.
		:rtype: bool
		"""

		if self.__engine.layouts_manager.current_layout != self.__development_layout and not self.isVisible():
			self.__engine.layouts_manager.restore_layout(self.__development_layout)
		return True
