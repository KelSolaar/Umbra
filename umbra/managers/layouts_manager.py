#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**layouts_manager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`LayoutsManager` and :class:`Layout` classes.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal

import foundations.data_structures
import foundations.exceptions
import foundations.verbose
import umbra.exceptions
from umbra.globals.ui_constants import UiConstants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Layout", "LayoutsManager"]

LOGGER = foundations.verbose.install_logger()

class Layout(foundations.data_structures.Structure):
	"""
	Defines a storage object for :class:`LayoutsManager` class layout.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param \*\*kwargs: name, identity, shortcut.
		:type \*\*kwargs: dict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.data_structures.Structure.__init__(self, **kwargs)

class LayoutsManager(QObject):
	"""
	Defines the Application layouts manager.
	"""

	layout_restored = pyqtSignal(unicode)
	"""
	This signal is emited by the :class:`LayoutsManager` class when the current layout has been restored.

	:return: Current layout.
	:rtype: unicode
	"""

	layout_stored = pyqtSignal(unicode)
	"""
	This signal is emited by the :class:`LayoutsManager` class when the current layout has been stored.

	:return: Current layout.
	:rtype: unicode
	"""

	def __init__(self, parent=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QObject.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__container = parent
		self.__settings = self.__container.settings

		self.__layouts = {}

		self.__current_layout = None
		self.__restore_geometry_on_layout_change = False

		self.register_layout(UiConstants.startup_layout, Layout(name="Startup",
															identity=UiConstants.startup_layout,
															shortcut=None))

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
	def layouts(self):
		"""
		Property for **self.__layouts** attribute.

		:return: self.__layouts.
		:rtype: dict
		"""

		return self.__layouts

	@layouts.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def layouts(self, value):
		"""
		Setter for **self.__layouts** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "layouts"))

	@layouts.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def layouts(self):
		"""
		Deleter for **self.__layouts** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "layouts"))

	@property
	def current_layout(self):
		"""
		Property for **self.__current_layout** attribute.

		:return: self.__current_layout.
		:rtype: tuple or list
		"""

		return self.__current_layout

	@current_layout.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def current_layout(self, value):
		"""
		Setter for **self.__current_layout** attribute.

		:param value: Attribute value.
		:type value: tuple or list
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "current_layout"))

	@current_layout.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def current_layout(self):
		"""
		Deleter for **self.__current_layout** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "current_layout"))

	@property
	def restore_geometry_on_layout_change(self):
		"""
		Property for **self.__restore_geometry_on_layout_change** attribute.

		:return: self.__restore_geometry_on_layout_change.
		:rtype: bool
		"""

		return self.__restore_geometry_on_layout_change

	@restore_geometry_on_layout_change.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def restore_geometry_on_layout_change(self, value):
		"""
		Setter for **self.__restore_geometry_on_layout_change** attribute.

		:param value: Attribute value.
		:type value: bool
		"""

		if value is not None:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format(
			"restore_geometry_on_layout_change", value)
		self.__restore_geometry_on_layout_change = value

	@restore_geometry_on_layout_change.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def restore_geometry_on_layout_change(self):
		"""
		Deleter for **self.__restore_geometry_on_layout_change** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "restore_geometry_on_layout_change"))

	def __getitem__(self, layout):
		"""
		Reimplements the :meth:`object.__getitem__` method.

		:param layout: Layout name.
		:type layout: unicode
		:return: Layout.
		:rtype: Layout
		"""

		return self.__layouts.__getitem__(layout)

	def __setitem__(self, name, layout):
		"""
		Reimplements the :meth:`object.__setitem__` method.

		:param name: Layout name.
		:type name: unicode
		:param layout: Layout.
		:type layout: Layout
		"""

		self.register_layout(name, layout)

	def __iter__(self):
		"""
		Reimplements the :meth:`object.__iter__` method.

		:return: Layouts iterator.
		:rtype: object
		"""

		return self.__layouts.iteritems()

	def __contains__(self, layout):
		"""
		Reimplements the :meth:`object.__contains__` method.

		:param layout: Layout name.
		:type layout: unicode
		:return: Layout existence.
		:rtype: bool
		"""

		return layout in self.__layouts

	def __len__(self):
		"""
		Reimplements the :meth:`object.__len__` method.

		:return: Layouts count.
		:rtype: int
		"""

		return len(self.__layouts)

	def get(self, layout, default=None):
		"""
		Returns given layout value.

		:param layout: Layout name.
		:type layout: unicode
		:param default: Default value if layout is not found.
		:type default: object
		:return: Action.
		:rtype: QAction
		"""

		try:
			return self.__getitem__(layout)
		except KeyError as error:
			return default

	def list_layouts(self):
		"""
		Returns the registered layouts.

		:return: Registered layouts.
		:rtype: list
		"""

		return sorted(self.__layouts.keys())

	def is_layout_registered(self, name):
		"""
		Returns if the given layout name is registered.

		:param name: Layout name.
		:type name: unicode
		:return: Is layout registered.
		:rtype: bool
		"""

		return name in self

	@foundations.exceptions.handle_exceptions(umbra.exceptions.LayoutRegistrationError)
	def register_layout(self, name, layout):
		"""
		Registers given layout.

		:param name: Layout name.
		:type name: unicode
		:param layout: Layout object.
		:type layout: Layout
		:return: Method success.
		:rtype: bool
		"""

		if name in self:
			raise umbra.exceptions.LayoutRegistrationError("{0} | '{1}' layout is already registered!".format(
			self.__class__.__name__, name))

		self.__layouts[name] = layout
		return True

	@foundations.exceptions.handle_exceptions(umbra.exceptions.LayoutRegistrationError)
	def unregister_layout(self, name):
		"""
		Unregisters given layout.

		:param name: Layout name.
		:type name: unicode
		:param layout: Layout object.
		:type layout: Layout
		:return: Method success.
		:rtype: bool
		"""

		if not name in self:
			raise umbra.exceptions.LayoutRegistrationError("{0} | '{1}' layout is not registered!".format(
			self.__class__.__name__, name))

		del(self.__layouts[name])
		return True

	@foundations.exceptions.handle_exceptions(umbra.exceptions.LayoutExistError)
	def restore_layout(self, name, *args):
		"""
		Restores given layout.

		:param name: Layout name.
		:type name: unicode
		:param \*args: Arguments.
		:type \*args: \*
		:return: Method success.
		:rtype: bool
		"""

		layout = self.__layouts.get(name)
		if not layout:
			raise umbra.exceptions.LayoutExistError("{0} | '{1}' layout isn't registered!".format(
			self.__class__.__name__, name))

		LOGGER.debug("> Restoring layout '{0}'.".format(name))

		for component, profile in self.__container.components_manager:
			if profile.category == "QWidget" and component not in self.__container.visible_components:
				interface = self.__container.components_manager.get_interface(component)
				interface and interface.hide()

		self.__current_layout = name
		self.__container.centralWidget().setVisible(
		self.__settings.get_key("Layouts", "{0}_central_widget".format(name)).toBool())
		self.__container.restoreState(
		self.__settings.get_key("Layouts", "{0}_window_state".format(name)).toByteArray())
		self.__restore_geometry_on_layout_change and \
		self.__container.restoreGeometry(
		self.__settings.get_key("Layouts", "{0}_geometry".format(name)).toByteArray())
		self.layout_restored.emit(self.__current_layout)
		return True

	@foundations.exceptions.handle_exceptions(umbra.exceptions.LayoutExistError)
	def store_layout(self, name, *args):
		"""
		Stores given layout.

		:param name: Layout name.
		:type name: unicode
		:param \*args: Arguments.
		:type \*args: \*
		:return: Method success.
		:rtype: bool
		"""

		layout = self.__layouts.get(name)
		if not layout:
			raise umbra.exceptions.LayoutExistError("{0} | '{1}' layout isn't registered!".format(
			self.__class__.__name__, name))

		LOGGER.debug("> Storing layout '{0}'.".format(name))

		self.__current_layout = name
		self.__settings.set_key("Layouts", "{0}_geometry".format(name), self.__container.saveGeometry())
		self.__settings.set_key("Layouts", "{0}_window_state".format(name), self.__container.saveState())
		self.__settings.set_key("Layouts", "{0}_central_widget".format(name), self.__container.centralWidget().isVisible())
		self.layout_stored.emit(self.__current_layout)
		return True

	def restore_startup_layout(self):
		"""
		Restores the startup layout.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Restoring startup layout.")

		if self.restore_layout(UiConstants.startup_layout):
			not self.__restore_geometry_on_layout_change and self.__container.restoreGeometry(
			self.__settings.get_key("Layouts", "{0}_geometry".format(UiConstants.startup_layout)).toByteArray())
			return True

	def store_startup_layout(self):
		"""
		Stores the startup layout.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Storing startup layout.")

		return self.store_layout(UiConstants.startup_layout)
