#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**layoutsManager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`LayoutsManager` and :class:`Layout` classes.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.dataStructures
import foundations.exceptions
import foundations.verbose
import umbra.exceptions
from umbra.globals.uiConstants import UiConstants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Layout", "LayoutsManager"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Layout(foundations.dataStructures.Structure):
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

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class LayoutsManager(QObject):
	"""
	Defines the Application layouts manager.
	"""

	layoutRestored = pyqtSignal(unicode)
	"""
	This signal is emited by the :class:`LayoutsManager` class when the current layout has been restored. ( pyqtSignal )

	:return: Current layout.
	:rtype: unicode
	"""

	layoutStored = pyqtSignal(unicode)
	"""
	This signal is emited by the :class:`LayoutsManager` class when the current layout has been stored. ( pyqtSignal )

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

		self.__currentLayout = None
		self.__restoreGeometryOnLayoutChange = False

		self.registerLayout(UiConstants.startupLayout, Layout(name="Startup",
															identity=UiConstants.startupLayout,
															shortcut=None))

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
	def settings(self):
		"""
		Property for **self.__settings** attribute.

		:return: self.__settings.
		:rtype: Preferences
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		Setter for **self.__settings** attribute.

		:param value: Attribute value.
		:type value: Preferences
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def layouts(self, value):
		"""
		Setter for **self.__layouts** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "layouts"))

	@layouts.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def layouts(self):
		"""
		Deleter for **self.__layouts** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "layouts"))

	@property
	def currentLayout(self):
		"""
		Property for **self.__currentLayout** attribute.

		:return: self.__currentLayout.
		:rtype: tuple or list
		"""

		return self.__currentLayout

	@currentLayout.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def currentLayout(self, value):
		"""
		Setter for **self.__currentLayout** attribute.

		:param value: Attribute value.
		:type value: tuple or list
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "currentLayout"))

	@currentLayout.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def currentLayout(self):
		"""
		Deleter for **self.__currentLayout** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "currentLayout"))

	@property
	def restoreGeometryOnLayoutChange(self):
		"""
		Property for **self.__restoreGeometryOnLayoutChange** attribute.

		:return: self.__restoreGeometryOnLayoutChange.
		:rtype: bool
		"""

		return self.__restoreGeometryOnLayoutChange

	@restoreGeometryOnLayoutChange.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def restoreGeometryOnLayoutChange(self, value):
		"""
		Setter for **self.__restoreGeometryOnLayoutChange** attribute.

		:param value: Attribute value.
		:type value: bool
		"""

		if value is not None:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format(
			"restoreGeometryOnLayoutChange", value)
		self.__restoreGeometryOnLayoutChange = value

	@restoreGeometryOnLayoutChange.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def restoreGeometryOnLayoutChange(self):
		"""
		Deleter for **self.__restoreGeometryOnLayoutChange** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "restoreGeometryOnLayoutChange"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
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

		self.registerLayout(name, layout)

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

	def listLayouts(self):
		"""
		Returns the registered layouts.

		:return: Registered layouts.
		:rtype: list
		"""

		return sorted(self.__layouts.keys())

	def isLayoutRegistered(self, name):
		"""
		Returns if the given layout name is registered.

		:param name: Layout name.
		:type name: unicode
		:return: Is layout registered.
		:rtype: bool
		"""

		return name in self

	@foundations.exceptions.handleExceptions(umbra.exceptions.LayoutRegistrationError)
	def registerLayout(self, name, layout):
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

	@foundations.exceptions.handleExceptions(umbra.exceptions.LayoutRegistrationError)
	def unregisterLayout(self, name):
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

	@foundations.exceptions.handleExceptions(umbra.exceptions.LayoutExistError)
	def restoreLayout(self, name, *args):
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

		for component, profile in self.__container.componentsManager:
			if profile.category == "QWidget" and component not in self.__container.visibleComponents:
				interface = self.__container.componentsManager.getInterface(component)
				interface and interface.hide()

		self.__currentLayout = name
		self.__container.centralWidget().setVisible(
		self.__settings.getKey("Layouts", "{0}_centralWidget".format(name)).toBool())
		self.__container.restoreState(
		self.__settings.getKey("Layouts", "{0}_windowState".format(name)).toByteArray())
		self.__restoreGeometryOnLayoutChange and \
		self.__container.restoreGeometry(
		self.__settings.getKey("Layouts", "{0}_geometry".format(name)).toByteArray())
		self.layoutRestored.emit(self.__currentLayout)
		return True

	@foundations.exceptions.handleExceptions(umbra.exceptions.LayoutExistError)
	def storeLayout(self, name, *args):
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

		self.__currentLayout = name
		self.__settings.setKey("Layouts", "{0}_geometry".format(name), self.__container.saveGeometry())
		self.__settings.setKey("Layouts", "{0}_windowState".format(name), self.__container.saveState())
		self.__settings.setKey("Layouts", "{0}_centralWidget".format(name), self.__container.centralWidget().isVisible())
		self.layoutStored.emit(self.__currentLayout)
		return True

	def restoreStartupLayout(self):
		"""
		Restores the startup layout.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Restoring startup layout.")

		if self.restoreLayout(UiConstants.startupLayout):
			not self.__restoreGeometryOnLayoutChange and self.__container.restoreGeometry(
			self.__settings.getKey("Layouts", "{0}_geometry".format(UiConstants.startupLayout)).toByteArray())
			return True

	def storeStartupLayout(self):
		"""
		Stores the startup layout.

		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Storing startup layout.")

		return self.storeLayout(UiConstants.startupLayout)
