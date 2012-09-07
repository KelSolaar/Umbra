#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**layoutsManager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`LayoutsManager` and :class:`Layout` classes.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
import umbra.exceptions
from umbra.globals.constants import Constants
from umbra.globals.uiConstants import UiConstants

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Layout", "LayoutsManager"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Layout(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for :class:`LayoutsManager` class layout.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: name, identity, shortcut. ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class LayoutsManager(QObject):
	"""
	This class defines the Application layouts manager. 
	"""

	layoutRestored = pyqtSignal(str)
	"""
	This signal is emited by the :class:`LayoutsManager` class when the current layout has been restored. ( pyqtSignal )

	:return: Current layout. ( String )	
	"""

	layoutStored = pyqtSignal(str)
	"""
	This signal is emited by the :class:`LayoutsManager` class when the current layout has been stored. ( pyqtSignal )

	:return: Current layout. ( String )	
	"""

	@core.executionTrace
	def __init__(self, parent):
		"""
		This method initializes the class.
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
	def settings(self):
		"""
		This method is the property for **self.__settings** attribute.

		:return: self.__settings. ( Preferences )
		"""

		return self.__settings

	@settings.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self, value):
		"""
		This method is the setter method for **self.__settings** attribute.

		:param value: Attribute value. ( Preferences )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "settings"))

	@settings.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def settings(self):
		"""
		This method is the deleter method for **self.__settings** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "settings"))

	@property
	def layouts(self):
		"""
		This method is the property for **self.__layouts** attribute.

		:return: self.__layouts. ( Dictionary )
		"""

		return self.__layouts

	@layouts.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def layouts(self, value):
		"""
		This method is the setter method for **self.__layouts** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "layouts"))

	@layouts.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def layouts(self):
		"""
		This method is the deleter method for **self.__layouts** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "layouts"))

	@property
	def currentLayout(self):
		"""
		This method is the property for **self.__currentLayout** attribute.

		:return: self.__currentLayout. ( Tuple / List )
		"""

		return self.__currentLayout

	@currentLayout.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentLayout(self, value):
		"""
		This method is the setter method for **self.__currentLayout** attribute.

		:param value: Attribute value. ( Tuple / List )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "currentLayout"))

	@currentLayout.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def currentLayout(self):
		"""
		This method is the deleter method for **self.__currentLayout** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "currentLayout"))

	@property
	def restoreGeometryOnLayoutChange(self):
		"""
		This method is the property for **self.__restoreGeometryOnLayoutChange** attribute.

		:return: self.__restoreGeometryOnLayoutChange. ( Boolean )
		"""

		return self.__restoreGeometryOnLayoutChange

	@restoreGeometryOnLayoutChange.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def restoreGeometryOnLayoutChange(self, value):
		"""
		This method is the setter method for **self.__restoreGeometryOnLayoutChange** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		if value is not None:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format(
			"restoreGeometryOnLayoutChange", value)
		self.__restoreGeometryOnLayoutChange = value

	@restoreGeometryOnLayoutChange.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def restoreGeometryOnLayoutChange(self):
		"""
		This method is the deleter method for **self.__restoreGeometryOnLayoutChange** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "restoreGeometryOnLayoutChange"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __getitem__(self, layout):
		"""
		This method reimplements the :meth:`object.__getitem__` method.

		:param layout: Layout name. ( String )
		:return: Layout. ( Layout )
		"""

		return self.__layouts.__getitem__(layout)

	@core.executionTrace
	def __iter__(self):
		"""
		This method reimplements the :meth:`object.__iter__` method.

		:return: Layouts iterator. ( Object )
		"""

		return self.__layouts.iteritems()

	@core.executionTrace
	def __contains__(self, layout):
		"""
		This method reimplements the :meth:`object.__contains__` method.

		:param layout: Layout name. ( String )
		:return: Layout existence. ( Boolean )
		"""

		return layout in self.__layouts.keys()

	@core.executionTrace
	def __len__(self):
		"""
		This method reimplements the :meth:`object.__len__` method.

		:return: Layouts count. ( Integer )
		"""

		return len(self.__layouts.keys())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listLayouts(self):
		"""
		This method returns the registered layouts.

		:return: Registered layouts. ( List )
		"""

		return sorted(self.__layouts.keys())

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def isLayoutRegistered(self, name):
		"""
		This method returns if the given layout name is registered.

		:param name: Layout name. ( String )
		:return: Is layout registered. ( Boolean )
		"""

		return name in self

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, umbra.exceptions.LayoutRegistrationError)
	def registerLayout(self, name, layout):
		"""
		This method registers given layout.

		:param name: Layout name. ( String )
		:param layout: Layout object. ( Layout )
		:return: Method success. ( Boolean )
		"""

		if name in self:
			raise umbra.exceptions.LayoutRegistrationError("{0} | '{1}' layout is already registered!".format(
			self.__class__.__name__, name))

		self.__layouts[name] = layout
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, umbra.exceptions.LayoutRegistrationError)
	def unregisterLayout(self, name):
		"""
		This method unregisters given layout.

		:param name: Layout name. ( String )
		:param layout: Layout object. ( Layout )
		:return: Method success. ( Boolean )
		"""

		if not name in self:
			raise umbra.exceptions.LayoutRegistrationError("{0} | '{1}' layout is not registered!".format(
			self.__class__.__name__, name))

		del(self.__layouts[name])
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, umbra.exceptions.LayoutExistError)
	def restoreLayout(self, name, *args):
		"""
		This method restores given layout.

		:param name: Layout name. ( String )
		:param \*args: Arguments. ( \* )
		:return: Method success. ( Boolean )
		"""

		layout = self.__layouts.get(name)
		if not layout:
			raise umbra.exceptions.LayoutExistError("{0} | '{1}' layout isn't registered!".format(
			self.__class__.__name__, name))

		LOGGER.debug("> Restoring layout '{0}'.".format(name))

		for component, profile in self.__container.componentsManager.components.iteritems():
			if profile.category == "QWidget" and component not in self.__container.visibleComponents:
				interface = self.__container.componentsManager.getInterface(component)
				interface and interface.hide()

		self.__currentLayout = name
		self.__container.centralwidget.setVisible(
		self.__settings.getKey("Layouts", "{0}_centralWidget".format(name)).toBool())
		self.__container.restoreState(
		self.__settings.getKey("Layouts", "{0}_windowState".format(name)).toByteArray())
		self.__restoreGeometryOnLayoutChange and \
		self.__container.restoreGeometry(
		self.__settings.getKey("Layouts", "{0}_geometry".format(name)).toByteArray())
		self.layoutRestored.emit(self.__currentLayout)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, umbra.exceptions.LayoutExistError)
	def storeLayout(self, name, *args):
		"""
		This method stores given layout.

		:param name: Layout name. ( String )
		:param \*args: Arguments. ( \* )
		:return: Method success. ( Boolean )
		"""

		layout = self.__layouts.get(name)
		if not layout:
			raise umbra.exceptions.LayoutExistError("{0} | '{1}' layout isn't registered!".format(
			self.__class__.__name__, name))

		LOGGER.debug("> Storing layout '{0}'.".format(name))

		self.__currentLayout = name
		self.__settings.setKey("Layouts", "{0}_geometry".format(name), self.__container.saveGeometry())
		self.__settings.setKey("Layouts", "{0}_windowState".format(name), self.__container.saveState())
		self.__settings.setKey("Layouts", "{0}_centralWidget".format(name), self.__container.centralwidget.isVisible())
		self.layoutStored.emit(self.__currentLayout)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def restoreStartupLayout(self):
		"""
		This method restores the startup layout.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Restoring startup layout.")

		if self.restoreLayout(UiConstants.startupLayout):
			not self.__restoreGeometryOnLayoutChange and self.__container.restoreGeometry(
			self.__settings.getKey("Layouts", "{0}_geometry".format(UiConstants.startupLayout)).toByteArray())
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def storeStartupLayout(self):
		"""
		This method stores the startup layout.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Storing startup layout.")

		return self.storeLayout(UiConstants.startupLayout)
