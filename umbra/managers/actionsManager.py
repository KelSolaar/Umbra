#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**actionsManager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	| This module defines the :class:`ActionsManager` class.
	| The :class:`ActionsManager` class provides a centralized hub to manage Applications actions.
	| It defines methods to register, unregister and list actions.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import re
import itertools
from PyQt4.QtCore import QObject
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QKeySequence

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
import foundations.namespace
import foundations.walkers
import umbra.exceptions
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

__all__ = ["LOGGER", "ActionsManager"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ActionsManager(QObject):
	"""
	This class is a `QObject <http://doc.qt.nokia.com/qobject.html>`_ subclass providing an actions manager.
	"""

	@core.executionTrace
	def __init__(self, parent=None, namespaceSplitter="|", rootNamespace="Actions", defaultNamespace="Others"):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param namespaceSplitter: Namespace splitters character. ( String )
		:param rootNamespace: Root namespace. ( String )
		:param defaultNamespace: Default namespace ( For actions with relative path ). ( String )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QObject.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__namespaceSplitter = None
		self.namespaceSplitter = namespaceSplitter
		self.__rootNamespace = None
		self.rootNamespace = rootNamespace
		self.__defaultNamespace = None
		self.defaultNamespace = defaultNamespace

		self.__categories = {}

		self.__actionsSignalsSlots = {}

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def namespaceSplitter(self):
		"""
		This method is the property for **self.__namespaceSplitter** attribute.

		:return: self.__namespaceSplitter. ( String )
		"""

		return self.__namespaceSplitter

	@namespaceSplitter.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def namespaceSplitter(self, value):
		"""
		This method is the setter method for **self.__namespaceSplitter** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"namespaceSplitter", value)
			assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("namespaceSplitter", value)
			assert not re.search(r"\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
			"namespaceSplitter", value)
		self.__namespaceSplitter = value

	@namespaceSplitter.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def namespaceSplitter(self):
		"""
		This method is the deleter method for **self.__namespaceSplitter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "namespaceSplitter"))

	@property
	def rootNamespace(self):
		"""
		This method is the property for **self.__rootNamespace** attribute.

		:return: self.__rootNamespace. ( String )
		"""

		return self.__rootNamespace

	@rootNamespace.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def rootNamespace(self, value):
		"""
		This method is the setter method for **self.__rootNamespace** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"rootNamespace", value)
		self.__rootNamespace = value

	@rootNamespace.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def rootNamespace(self):
		"""
		This method is the deleter method for **self.__rootNamespace** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "rootNamespace"))

	@property
	def defaultNamespace(self):
		"""
		This method is the property for **self.__defaultNamespace** attribute.

		:return: self.__defaultNamespace. ( String )
		"""

		return self.__defaultNamespace

	@defaultNamespace.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultNamespace(self, value):
		"""
		This method is the setter method for **self.__defaultNamespace** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"defaultNamespace", value)
		self.__defaultNamespace = value

	@defaultNamespace.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultNamespace(self):
		"""
		This method is the deleter method for **self.__defaultNamespace** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultNamespace"))

	@property
	def categories(self):
		"""
		This method is the property for **self.__categories** attribute.

		:return: self.__categories. ( Dictionary )
		"""

		return self.__categories

	@categories.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def categories(self, value):
		"""
		This method is the setter method for **self.__categories** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("categories", value)
			for key, element in value.iteritems():
				assert type(key) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("categories", key)
				assert type(element) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("categories", element)
		self.__categories = value

	@categories.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def categories(self):
		"""
		This method is the deleter method for **self.__categories** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "categories"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __getitem__(self, action):
		"""
		This method reimplements the :meth:`object.__getitem__` method.

		:param action: Action name. ( String )
		:return: Action. ( QAction )
		"""

		action = self.__normalizeName(action)
		for path, name, object in foundations.walkers.dictionariesWalker(self.__categories):
			if action == foundations.namespace.setNamespace(self.__namespaceSplitter.join(path), name):
				LOGGER.debug("> Retrieved object for '{0}' action name!".format(action))
				return object
		raise umbra.exceptions.ActionExistsError("{0} | '{1}' action isn't registered!".format(self.__class__.__name__,
																								action))
	@core.executionTrace
	def __iter__(self):
		"""
		This method reimplements the :meth:`object.__iter__` method.

		:return: Actions iterator. ( Object )
		"""

		return foundations.walkers.dictionariesWalker(self.__categories)

	@core.executionTrace
	def __contains__(self, action):
		"""
		This method reimplements the :meth:`object.__contains__` method.

		:param action: Action name. ( String )
		:return: Action existence. ( Boolean )
		"""

		for path, name, object in self:
			if foundations.namespace.setNamespace(self.__namespaceSplitter.join(path), name) == action:
				return True
		return False

	@core.executionTrace
	def __len__(self):
		"""
		This method reimplements the :meth:`object.__len__` method.

		:return: Actions count. ( Integer )
		"""

		return len([action for action in self])

	@core.executionTrace
	def __normalizeName(self, name):
		"""
		This method normalizes given action name.

		:param name: Action name. ( String )
		:return: Normalized name. ( Boolean )
		"""

		if not name.startswith(self.__rootNamespace):
			name = foundations.namespace.setNamespace(self.__rootNamespace,
													foundations.namespace.setNamespace(self.__defaultNamespace, name))
			LOGGER.debug("> Normalized name: '{0}'.".format(name))
			return name
		else:
			LOGGER.debug("> Name '{0}' is already normalized!".format(name))
			return name

	@core.executionTrace
	def __getCategory(self, category, name, vivify=False):
		"""
		This method gets recusively requested category, alternately if **vivify** argument is set,
		the category will be created.

		:param category: Base category. ( Dictionary )
		:param name: Category to retrieve or vivify. ( String )
		:param vivify: Vivify missing parents in the chain to the requested category. ( Boolean )
		:return: Requested category. ( Dictionary )
		"""

		namespace = foundations.namespace.getNamespace(name, rootOnly=True)
		name = foundations.namespace.removeNamespace(name, rootOnly=True)
		if namespace:
			if vivify and namespace not in category:
				category[namespace] = {}
			return self.__getCategory(category[namespace], name, vivify)
		else:
			if vivify and name not in category:
				category[name] = {}
			return category[name]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listActions(self):
		"""
		This method returns the registered actions.

		:return: Actions list. ( List )
		"""

		actions = []
		for path, actionName, action in self:
			actions.append(self.__namespaceSplitter.join(itertools.chain(path, (actionName,))))
		return sorted(actions)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, umbra.exceptions.CategoryExistsError)
	def getCategory(self, name, vivify=False):
		"""
		This method returns requested category.

		:param name: Category to retrieve. ( String )
		:param vivify: Vivify missing parents in the chain to the requested category. ( Boolean )
		:return: Category. ( Dictionary )
		"""

		category = self.__getCategory(self.__categories, name, vivify)
		if isinstance(category, dict):
			LOGGER.debug("> Category '{0}': '{1}'.".format(name, category))
			return category
		else:
			raise umbra.exceptions.CategoryExistsError("{0} | '{1}' category doesn't exists!".format
			(self.__class__.__name__, name))

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def addToCategory(self, category, name, action):
		"""
		This method adds given action to given category.

		:param category: Category to store the action. ( String )
		:param name: Action name. ( String )
		:param action: Action object. ( QAction )
		:return: Method success. ( Boolean )
		"""

		category = self.getCategory(category, vivify=True)
		if not isinstance(category, dict):
			return False

		category[name] = action
		LOGGER.debug("> Added '{0}' action to '{1}' category!".format(category, name))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removeFromCategory(self, category, name):
		"""
		This method removes given action from given category.

		:param category: Category to remove the action from. ( String )
		:param name: Action name. ( String )
		:return: Method success. ( Boolean )
		"""

		category = self.getCategory(category)
		if not isinstance(category, dict):
			return False

		del(category[name])
		LOGGER.debug("> Removed '{0}' action from '{1}' category!".format(category, name))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, umbra.exceptions.ActionExistsError)
	def getAction(self, action):
		"""
		This method returns requested action.

		:param action: Action name. ( String )
		:return: Action. ( QAction )
		"""

		return self[action]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def isActionRegistered(self, name):
		"""
		This method returns if the given action name is registered.

		:param name: Action name. ( String )
		:return: Is action registered. ( Boolean )
		"""

		return name in self

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def registerAction(self, name, **kwargs):
		"""
		This method registers given action name, optional arguments like a parent, icon, slot etc ... can be given.

		:param name: Action to register. ( String )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		:return: Action. ( QAction )
		"""

		settings = foundations.dataStructures.Structure(**{"parent" : None,
									"text" : None,
									"icon" : None,
									"iconText" : None,
									"checkable" : None,
									"checked" : None,
									"statusTip" : None,
									"whatsThis" : None,
									"toolTip" : None,
									"shortcut" : None,
									"shortcutContext" : None,
									"slot" : None})
		settings.update(kwargs)

		name = self.__normalizeName(name)
		category = foundations.namespace.getNamespace(name)
		name = foundations.namespace.removeNamespace(name)

		action = QAction(name, settings.parent or self)
		self.addToCategory(category, name, action)

		settings.text and action.setText(settings.text)
		settings.icon and action.setIcon(settings.icon)
		settings.iconText and action.setIconText(settings.iconText)
		settings.checkable and action.setCheckable(settings.checkable)
		settings.checked and action.setChecked(settings.checked)
		settings.statusTip and action.setStatusTip(settings.statusTip)
		settings.whatsThis and action.setWhatsThis(settings.whatsThis)
		settings.toolTip and action.setToolTip(settings.toolTip)
		settings.shortcut and action.setShortcut(QKeySequence(settings.shortcut))
		settings.shortcutContext and action.setShortcutContext(settings.shortcutContext)
		if settings.slot:
			self.__actionsSignalsSlots[action] = settings.slot
			action.triggered.connect(settings.slot)
		return action

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def unregisterAction(self, name):
		"""
		This method unregisters given action name.

		:param name: Action to register. ( String )
		:return: Method success. ( Boolean )
		"""

		name = self.__normalizeName(name)
		action = self.getAction(name)
		if not action:
			return False

		action.triggered.disconnect(self.__actionsSignalsSlots.pop(action))

		category = foundations.namespace.getNamespace(name)
		name = foundations.namespace.removeNamespace(name)
		self.removeFromCategory(category, name)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def isShortcutInUse(self, shortcut):
		"""
		This method returns if given action shortcut is in use.

		:param name: Action shortcut. ( String )
		:return: Is shortcut in use. ( Boolean )
		"""

		for path, actionName, action in foundations.walkers.dictionariesWalker(self.__categories):
			if action.shortcut() == QKeySequence(shortcut):
				return True
		return False

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getShortcut(self, name):
		"""
		This method returns given action shortcut.

		:param name: Action to retrieve the shortcut. ( String )
		:return: Action shortcut. ( String )
		"""

		name = self.__normalizeName(name)
		action = self.getAction(name)
		if not action:
			return str()

		return action.shortcut().toString()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def setShortcut(self, name, shortcut):
		"""
		This method sets given action shortcut.

		:param name: Action to set the shortcut. ( String )
		:param shortcut: Shortcut to set. ( String )
		:return: Method success. ( Boolean )
		"""

		name = self.__normalizeName(name)
		action = self.getAction(name)
		if not action:
			return

		action.setShortcut(QKeySequence(shortcut))
		return True
