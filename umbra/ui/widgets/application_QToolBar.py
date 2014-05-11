#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**application_QToolBar.py.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`Application_QToolBar` class.

**Others:**

"""

from __future__ import unicode_literals

import functools
from PyQt4.QtCore import QSize
from PyQt4.QtCore import QString
from PyQt4.QtCore import QUrl
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QToolBar

import foundations.exceptions
import foundations.verbose
import umbra.managers.layouts_manager
import umbra.ui.common
from umbra.globals.constants import Constants
from umbra.globals.ui_constants import UiConstants
from umbra.ui.widgets.active_QLabel import Active_QLabel
from umbra.ui.widgets.active_QLabelsCollection import Active_QLabelsCollection

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Application_QToolBar"]

LOGGER = foundations.verbose.install_logger()

class Application_QToolBar(QToolBar):
	"""
	Defines a `QToolBar <http://doc.qt.nokia.com/qtoolbar.html>`_ subclass providing
	the Application toolbar.
	"""

	def __init__(self, parent=None):
		"""
		Initializes the class.

		:param parent: Widget parent.
		:type parent: QObject
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QToolBar.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__container = parent
		self.__settings = self.__container.settings

		self.__layouts_active_labels_collection = None
		self.__custom_layouts_menu = None
		self.__miscellaneous_menu = None

		self.__user_layouts = (umbra.managers.layouts_manager.Layout(name="1", identity="one", shortcut=Qt.Key_1),
							umbra.managers.layouts_manager.Layout(name="2", identity="two", shortcut=Qt.Key_2),
							umbra.managers.layouts_manager.Layout(name="3", identity="three", shortcut=Qt.Key_3),
							umbra.managers.layouts_manager.Layout(name="4", identity="four", shortcut=Qt.Key_4),
							umbra.managers.layouts_manager.Layout(name="5", identity="five", shortcut=Qt.Key_5))

		Application_QToolBar.__initialize_ui(self)

	@property
	def container(self):
		"""
		Property for **self.__container** attribute.

		:return: self.__container.
		:rtype: QObject
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		Setter for **self.__container** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		Deleter for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def settings(self):
		"""
		Property for **self.__settings** attribute.

		:return: self.__settings.
		:rtype: Preferences
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		Setter for **self.__settings** attribute.

		:param value: Attribute value.
		:type value: Preferences
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
	def layouts_active_labels_collection(self):
		"""
		Property for **self.__layouts_active_labels_collection** attribute.

		:return: self.__layouts_active_labels_collection.
		:rtype: Active_QLabelsCollection
		"""

		return self.__layouts_active_labels_collection

	@layouts_active_labels_collection.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def layouts_active_labels_collection(self, value):
		"""
		Setter for **self.__layouts_active_labels_collection** attribute.

		:param value: Attribute value.
		:type value: Active_QLabelsCollection
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "layouts_active_labels_collection"))

	@layouts_active_labels_collection.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def layouts_active_labels_collection(self):
		"""
		Deleter for **self.__layouts_active_labels_collection** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "layouts_active_labels_collection"))

	@property
	def custom_layouts_menu(self):
		"""
		Property for **self.__custom_layouts_menu** attribute.

		:return: self.__custom_layouts_menu.
		:rtype: QMenu
		"""

		return self.__custom_layouts_menu

	@custom_layouts_menu.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def custom_layouts_menu(self, value):
		"""
		Setter for **self.__custom_layouts_menu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		if value is not None:
			assert type(value) is QMenu, "'{0}' attribute: '{1}' type is not 'QMenu'!".format("custom_layouts_menu", value)
		self.__custom_layouts_menu = value

	@custom_layouts_menu.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def custom_layouts_menu(self):
		"""
		Deleter for **self.__custom_layouts_menu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "custom_layouts_menu"))

	@property
	def miscellaneous_menu(self):
		"""
		Property for **self.__miscellaneous_menu** attribute.

		:return: self.__miscellaneous_menu.
		:rtype: QMenu
		"""

		return self.__miscellaneous_menu

	@miscellaneous_menu.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def miscellaneous_menu(self, value):
		"""
		Setter for **self.__miscellaneous_menu** attribute.

		:param value: Attribute value.
		:type value: QMenu
		"""

		if value is not None:
			assert type(value) is QMenu, "'{0}' attribute: '{1}' type is not 'QMenu'!".format("miscellaneous_menu", value)
		self.__miscellaneous_menu = value

	@miscellaneous_menu.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def miscellaneous_menu(self):
		"""
		Deleter for **self.__miscellaneous_menu** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "miscellaneous_menu"))

	def __initialize_ui(self):
		"""
		Initializes the Widget ui.
		"""

		LOGGER.debug("> Initializing Application toolBar!")

		self.setIconSize(QSize(UiConstants.default_toolbar_icon_size, UiConstants.default_toolbar_icon_size))
		self.setAllowedAreas(Qt.TopToolBarArea)
		self.setFloatable(False)
		self.setMovable(False)
		self.set_layout_default_geometry()

		self.setObjectName("toolBar")
		self.setWindowTitle("{0} - toolBar".format(Constants.application_name))

		self.set_toolbar_children_widgets()

		# Signals / Slots.
		self.__container.layouts_manager.layout_stored.connect(self.__layouts_manager__layout_stored)
		self.__container.layouts_manager.layout_restored.connect(self.__layouts_manager__layout_restored)

	def __layout_active_label__clicked(self, layout):
		"""
		Defines the slot triggered by a **Active_QLabel** Widget when clicked.

		:param layout: Layout name.
		:type layout: unicode
		"""

		self.__container.layouts_manager.restore_layout(layout)

	def __layouts_manager__layout_stored(self, layout):
		"""
		Defines the slot triggered by :class:`umbra.managers.layouts_manager.LayoutsManager` class
		when a layout is stored.

		:param layout: Layout name.
		:type layout: unicode
		"""

		layout_active_label = self.__layouts_active_labels_collection.get_toggled_active_label()
		layout_active_label and self.__settings.set_key("Layouts",
										"{0}_active_label".format(layout),
										layout_active_label.objectName())

	def __layouts_manager__layout_restored(self, layout):
		"""
		Defines the slot triggered by :class:`umbra.managers.layouts_manager.LayoutsManager` class
		when a layout is restored.

		:param layout: Layout name.
		:type layout: unicode
		"""

		layout_active_label = self.__settings.get_key("Layouts", "{0}_active_label".format(layout)).toString()
		for active_label in self.__layouts_active_labels_collection.active_labels:
			if not active_label.objectName() == layout_active_label:
				continue

			active_label.set_checked(True)

	def __help_display_misc_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|ToolBar|Miscellaneous|Help content ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Opening url: '{0}'.".format(UiConstants.help_file))
		QDesktopServices.openUrl(QUrl(QString(UiConstants.help_file)))
		return True

	def __api_display_misc_action__triggered(self, checked):
		"""
		Defines the slot triggered by **'Actions|Umbra|ToolBar|Miscellaneous|Api content ...'** action.

		:param checked: Checked state.
		:type checked: bool
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Opening url: '{0}'.".format(UiConstants.api_file))
		QDesktopServices.openUrl(QUrl(QString(UiConstants.api_file)))
		return True

	def set_layout_default_geometry(self):
		"""
		Sets the toolBar layout default geometry.

		:return: Method success.
		:rtype: bool
		"""

		self.layout().setSpacing(8)
		self.layout().setContentsMargins(0, 0, 0, 0)
		return True

	def set_toolbar_children_widgets(self):
		"""
		Sets the toolBar children widgets.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Adding 'Application_Logo_label' widget!")
		self.addWidget(self.get_application_logo_label())

		LOGGER.debug("> Adding 'Spacer_label' widget!")
		self.addWidget(self.get_spacer_label())

		LOGGER.debug("> Adding 'Development_active_label', 'Preferences_active_label' widgets!")
		for layout_active_label in self.get_layouts_active_labels():
			self.addWidget(layout_active_label)

		LOGGER.debug("> Adding 'Custom_Layouts_active_label' widget!")
		self.addWidget(self.get_custom_layouts_active_label())

		LOGGER.debug("> Adding 'Miscellaneous_active_label' widget!")
		self.addWidget(self.get_miscellaneous_active_label())

		LOGGER.debug("> Adding 'Closure_Spacer_label' widget!")
		self.addWidget(self.get_closure_spacer_label())

		return True

	def get_application_logo_label(self):
		"""
		Provides the default **Application_Logo_label** widget.

		:return: Application logo label.
		:rtype: QLabel
		"""

		logo_label = QLabel()
		logo_label.setObjectName("Application_Logo_label")
		logo_label.setPixmap(QPixmap(umbra.ui.common.get_resource_path(UiConstants.logo_image)))
		return logo_label

	def get_layout_active_label(self, resources, name, title, identity, shortcut):
		"""
		Returns a layout **Active_QLabel** widget.

		:param resources: Icons resources ( Default / Hover / Active ).
		:type resources: tuple
		:param name: Ui object name.
		:type name: unicode
		:param title: Layout registration title.
		:type title: unicode
		:param identity: Layout code name.
		:type identity: unicode
		:param shortcut: Layout associated shortcut. ( QtCore.Key )
		:return: Layout active label.
		:rtype: Active_QLabel
		"""

		default_icon, hover_icon, active_icon = resources
		layout_active_label = Active_QLabel(self,
										QPixmap(umbra.ui.common.get_resource_path(default_icon)),
										QPixmap(umbra.ui.common.get_resource_path(hover_icon)),
										QPixmap(umbra.ui.common.get_resource_path(active_icon)),
										True)
		self.__container.layouts_manager.register_layout(identity, umbra.managers.layouts_manager.Layout(name=title,
																								identity=identity,
																								shortcut=shortcut))
		self.__container.addAction(
		self.__container.actions_manager.register_action("Actions|Umbra|ToolBar|Layouts|Restore layout {0}".format(title),
														shortcut=shortcut,
														shortcut_context=Qt.ApplicationShortcut,
														slot=functools.partial(
														self.__container.layouts_manager.restore_layout, identity)))

		layout_active_label.setObjectName(name)

		# Signals / Slots.
		layout_active_label.clicked.connect(functools.partial(self.__layout_active_label__clicked, identity))

		return layout_active_label

	def get_layouts_active_labels(self):
		"""
		Returns the layouts **Active_QLabel** widgets.

		:return: Layouts active labels.
		:rtype: list
		"""

		self.__layouts_active_labels_collection = Active_QLabelsCollection(self)

		self.__layouts_active_labels_collection.add_active_label(self.get_layout_active_label((UiConstants.development_icon,
																					UiConstants.development_hover_icon,
																					UiConstants.development_active_icon),
																					"Development_active_label",
																					"Development",
																					"development_centric",
																					Qt.Key_9))

		self.__layouts_active_labels_collection.add_active_label(self.get_layout_active_label((UiConstants.preferences_icon,
																					UiConstants.preferences_hover_icon,
																					UiConstants.preferences_active_icon),
																					"Preferences_active_label",
																					"Preferences",
																					"preferences_centric",
																					Qt.Key_0))
		return self.__layouts_active_labels_collection.active_labels

	def get_custom_layouts_active_label(self):
		"""
		Provides the default **Custom_Layouts_active_label** widget.

		:return: Layout active label.
		:rtype: Active_QLabel
		"""

		layout_active_label = Active_QLabel(self, QPixmap(umbra.ui.common.get_resource_path(UiConstants.custom_layouts_icon)),
									QPixmap(umbra.ui.common.get_resource_path(UiConstants.custom_layouts_hover_icon)),
									QPixmap(umbra.ui.common.get_resource_path(UiConstants.custom_layouts_active_icon)))
		layout_active_label.setObjectName("Custom_Layouts_active_label")

		self.__custom_layouts_menu = QMenu("Layouts", layout_active_label)

		for layout in self.__user_layouts:
			self.__container.layouts_manager.register_layout(layout.identity, layout)
			self.__custom_layouts_menu.addAction(self.__container.actions_manager.register_action(
			"Actions|Umbra|ToolBar|Layouts|Restore layout {0}".format(layout.name),
			shortcut=layout.shortcut,
			slot=functools.partial(self.__container.layouts_manager.restore_layout, layout.identity)))

		self.__custom_layouts_menu.addSeparator()

		for layout in self.__user_layouts:
			self.__custom_layouts_menu.addAction(self.__container.actions_manager.register_action(
			"Actions|Umbra|ToolBar|Layouts|Store layout {0}".format(layout.name),
			shortcut=Qt.CTRL + layout.shortcut,
			slot=functools.partial(self.__container.layouts_manager.store_layout, layout.identity)))

		self.__custom_layouts_menu.addSeparator()

		self.__custom_layouts_menu.addAction(self.__container.actions_manager.register_action(
		"Actions|Umbra|ToolBar|Layouts|Toggle FullScreen",
		shortcut=Qt.ControlModifier + Qt.SHIFT + Qt.Key_F,
		slot=self.__container.toggle_full_screen))

		layout_active_label.set_menu(self.__custom_layouts_menu)
		return layout_active_label

	def get_miscellaneous_active_label(self):
		"""
		Provides the default **Miscellaneous_active_label** widget.

		:return: Miscellaneous active label.
		:rtype: Active_QLabel
		"""

		miscellaneous_active_label = Active_QLabel(self,
											QPixmap(umbra.ui.common.get_resource_path(UiConstants.miscellaneous_icon)),
											QPixmap(umbra.ui.common.get_resource_path(UiConstants.miscellaneous_hover_icon)),
											QPixmap(umbra.ui.common.get_resource_path(UiConstants.miscellaneous_active_icon)))
		miscellaneous_active_label.setObjectName("Miscellaneous_active_label")

		self.__miscellaneous_menu = QMenu("Miscellaneous", miscellaneous_active_label)

		self.__miscellaneous_menu.addAction(self.__container.actions_manager.register_action(
											"Actions|Umbra|ToolBar|Miscellaneous|Help content ...",
											shortcut="F1",
											slot=self.__help_display_misc_action__triggered))
		self.__miscellaneous_menu.addAction(self.__container.actions_manager.register_action(
											"Actions|Umbra|ToolBar|Miscellaneous|Api content ...",
											slot=self.__api_display_misc_action__triggered))
		self.__miscellaneous_menu.addSeparator()

		miscellaneous_active_label.set_menu(self.__miscellaneous_menu)
		return miscellaneous_active_label

	def get_spacer_label(self):
		"""
		Provides the default **Spacer_label** widget.

		:return: Logo spacer label.
		:rtype: QLabel
		"""

		spacer = QLabel()
		spacer.setObjectName("Spacer_label")
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		return spacer

	def get_closure_spacer_label(self):
		"""
		Provides the default **Closure_Spacer_label** widget.

		:return: Closure spacer label.
		:rtype: QLabel
		"""

		spacer = QLabel()
		spacer.setObjectName("Closure_Spacer_label")
		spacer.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
		return spacer

if __name__ == "__main__":
	import sys
	from PyQt4.QtGui import QMainWindow

	from manager.components_manager import Manager
	from umbra.managers.actions_manager import ActionsManager
	from umbra.managers.layouts_manager import LayoutsManager
	from umbra.preferences import Preferences

	application = umbra.ui.common.get_application_instance()

	main_window = QMainWindow()

	main_window.settings = Preferences()
	main_window.actions_manager = ActionsManager(main_window)
	main_window.layouts_manager = LayoutsManager(main_window)
	main_window.components_manager = Manager()
	main_window.toggle_full_screen = lambda: sys.stdout.write("toggle_full_screen()\n")

	main_window.setCentralWidget(QLabel())

	application_QToolBar = Application_QToolBar(main_window)
	main_window.addToolBar(application_QToolBar)

	main_window.show()
	main_window.raise_()

	sys.exit(application.exec_())
