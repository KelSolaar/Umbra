#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**layoutsManager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`LayoutsManager` and :class:`Patches` classes.

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
from umbra.globals.constants import Constants
from umbra.globals.uiConstants import UiConstants
from umbra.ui.widgets.active_QLabel import Active_QLabel
import PyQt4

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Layout", "LayoutActiveLabel", "LayoutsManager"]

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

		:param \*\*kwargs: name. ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class LayoutsManager(QObject):
	"""
	This class defines the Application layouts manager. 
	"""

	layoutChanged = pyqtSignal(str)
	"""
	This signal is emited by the :class:`Umbra` class when the current layout has changed. ( pyqtSignal )

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

		self.__currentLayout = None

		self.__layouts = {}

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

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
#	@foundations.exceptions.exceptionsHandler(None, False, umbra.exceptions.PatchInterfaceError)
#	def registerPatch(self, name, path):
#		"""
#		This method registers given patch.
#
#		:param path: Patch name. ( String )
#		:param path: Patch path. ( String )
#		:return: Method success. ( Boolean )
#		"""
#
#		patch = foundations.strings.getSplitextBasename(path)
#		LOGGER.debug("> Current patch: '{0}'.".format(patch))
#
#		directory = os.path.dirname(path)
#		not directory in sys.path and sys.path.append(directory)
#
#		import_ = __import__(patch)
#		if hasattr(import_, "apply") and hasattr(import_, "UID"):
#			self.__layouts[name] = Patch(name=name,
#										path=path,
#										import_=import_,
#										apply=getattr(import_, "apply"),
#										uid=getattr(import_, "UID"))
#		else:
#			raise umbra.exceptions.PatchInterfaceError(
#			"{0} | '{1}' is not a valid patch and has been rejected!".format(self.__class__.__name__, patch))
#		return True
#
#	@core.executionTrace
#	@foundations.exceptions.exceptionsHandler(None, False, umbra.exceptions.PatchRegistrationError)
#	def registerPatches(self):
#		"""
#		This method registers the layouts.
#
#		:return: Method success. ( Boolean )
#		"""
#
#		if not self.__paths:
#			return
#
#		osWalker = OsWalker()
#		unregisteredPatches = []
#		for path in self.paths:
#			osWalker.root = path
#			osWalker.walk(("\.{0}$".format(self.__extension),), ("\._",))
#			for name, file in osWalker.files.iteritems():
#				if not self.registerPatch(name, file):
#					unregisteredPatches.append(name)
#
#		if not unregisteredPatches:
#			return True
#		else:
#			raise umbra.exceptions.PatchRegistrationError(
#			"{0} | '{1}' layouts failed to register!".format(self.__class__.__name__,
#																", ".join(unregisteredPatches)))
#
#	@core.executionTrace
#	@foundations.exceptions.exceptionsHandler(None, False, Exception)
#	def listPatches(self):
#		"""
#		This method list the layouts.
#
#		:return: Patches list. ( List )
#		"""
#
#		return [name for name, patch in sorted(self.__layouts.iteritems())]
#
#	@core.executionTrace
#	@foundations.exceptions.exceptionsHandler(None, False, Exception)
#	def getPatchFromUid(self, uid):
#		"""
#		This method returns the patch with given uid.
#
#		:param uid: Patch uid. ( String )
#		:return: Patch. ( Patch )
#		"""
#
#		for patch in self.__layouts.itervalues():
#			if patch.uid == uid:
#				return patch

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listLayouts(self, userLayouts=True):
		"""
		This method lists Application layouts.

		:param userLayouts: List user layouts. ( Boolean )
		:return: Application layouts. ( List )
		"""

		layouts = []
		for layoutActiveLabel in self.__layoutsActiveLabels:
			layouts.append(layoutActiveLabel.layout)

		if userLayouts:
			for index, shortcut, name in self.__userLayouts:
				layouts.append(name)

		return layouts

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def storeLayout(self, name, *args):
		"""
		This method is triggered when storing a layout.

		:param name: Layout name. ( String )
		:param \*args: Arguments. ( \* )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Storing layout '{0}'.".format(name))

		self.__container.settings.setKey("Layouts", "{0}_geometry".format(name), self.__container.saveGeometry())
		self.__container.settings.setKey("Layouts", "{0}_windowState".format(name), self.__container.saveState())
		self.__container.settings.setKey("Layouts", "{0}_centralWidget".format(name), self.__container.centralwidget.isVisible())
#		self.__container.settings.setKey("Layouts", "{0}_activeLabel".format(name), self.__container.__getCurrentLayoutActiveLabel())
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def restoreLayout(self, name, *args):
		"""
		This method is triggered when restoring a layout.

		:param name: Layout name. ( String )
		:param \*args: Arguments. ( \* )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Restoring layout '{0}'.".format(name))

		for component, profile in self.__container.componentsManager.components.iteritems():
			if profile.category == "QWidget" and component not in self.__container.visibleComponents:
				interface = self.__container.componentsManager.getInterface(component)
				interface and self.__container.componentsManager.getInterface(component).hide()

		self.__container.centralwidget.setVisible(self.__container.settings.getKey("Layouts", "{0}_centralWidget".format(name)).toBool())
		self.__container.restoreState(self.__container.settings.getKey("Layouts", "{0}_windowState".format(name)).toByteArray())
		self.__container.settings.data.restoreGeometryOnLayoutChange and \
		self.__container.restoreGeometry(self.__container.settings.getKey("Layouts", "{0}_geometry".format(name)).toByteArray())
#		self.__setLayoutsActiveLabels(self.__container.settings.getKey("Layouts", "{0}_activeLabel".format(name)).toInt()[0])
#		self.__currentLayout = self.__layoutsActiveLabels[self.__getCurrentLayoutActiveLabel()].layout
		self.__currentLayout = name

		self.layoutChanged.emit(self.__currentLayout)

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
			not self.__container.settings.data.restoreGeometryOnLayoutChange and \
			self.__container.restoreGeometry(self.__container.settings.getKey("Layouts",
														"{0}_geometry".format(UiConstants.startupLayout)).toByteArray())
			return True
		else:
			raise Exception("{0} | Exception raised while restoring startup layout!".format(self.__class__.__name__))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def storeStartupLayout(self):
		"""
		This method stores the startup layout.

		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Storing startup layout.")

		return self.storeLayout(UiConstants.startupLayout)
