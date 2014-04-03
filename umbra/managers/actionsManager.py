#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**actionsManager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	| Defines the :class:`ActionsManager` class.
	| The :class:`ActionsManager` class provides a centralized hub to manage Applications actions.
	| It defines methods to register, unregister and list actions.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import re
import itertools
from PyQt4.QtCore import QObject
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QKeySequence

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.dataStructures
import foundations.exceptions
import foundations.namespace
import foundations.verbose
import foundations.walkers
import umbra.exceptions

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "ActionsManager"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ActionsManager(QObject):
	"""
	Defines a `QObject <http://doc.qt.nokia.com/qobject.html>`_ subclass providing an actions manager.
	"""

	def __init__(self, parent=None, namespaceSplitter="|", rootNamespace="Actions", defaultNamespace="Others"):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param namespaceSplitter: Namespace splitters character.
		:type namespaceSplitter: unicode
		:param rootNamespace: Root foundations.namespace.
		:type rootNamespace: unicode
		:param defaultNamespace: Default namespace ( For actions with relative path ).
		:type defaultNamespace: unicode
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
		Property for **self.__namespaceSplitter** attribute.

		:return: self.__namespaceSplitter.
		:rtype: unicode
		"""

		return self.__namespaceSplitter

	@namespaceSplitter.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def namespaceSplitter(self, value):
		"""
		Setter for **self.__namespaceSplitter** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"namespaceSplitter", value)
			assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("namespaceSplitter",
																							  value)
			assert not re.search(r"\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
				"namespaceSplitter", value)
		self.__namespaceSplitter = value

	@namespaceSplitter.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def namespaceSplitter(self):
		"""
		Deleter for **self.__namespaceSplitter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "namespaceSplitter"))

	@property
	def rootNamespace(self):
		"""
		Property for **self.__rootNamespace** attribute.

		:return: self.__rootNamespace.
		:rtype: unicode
		"""

		return self.__rootNamespace

	@rootNamespace.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def rootNamespace(self, value):
		"""
		Setter for **self.__rootNamespace** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"rootNamespace", value)
		self.__rootNamespace = value

	@rootNamespace.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def rootNamespace(self):
		"""
		Deleter for **self.__rootNamespace** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "rootNamespace"))

	@property
	def defaultNamespace(self):
		"""
		Property for **self.__defaultNamespace** attribute.

		:return: self.__defaultNamespace.
		:rtype: unicode
		"""

		return self.__defaultNamespace

	@defaultNamespace.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def defaultNamespace(self, value):
		"""
		Setter for **self.__defaultNamespace** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"defaultNamespace", value)
		self.__defaultNamespace = value

	@defaultNamespace.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultNamespace(self):
		"""
		Deleter for **self.__defaultNamespace** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultNamespace"))

	@property
	def categories(self):
		"""
		Property for **self.__categories** attribute.

		:return: self.__categories.
		:rtype: dict
		"""

		return self.__categories

	@categories.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def categories(self, value):
		"""
		Setter for **self.__categories** attribute.

		:param value: Attribute value.
		:type value: dict
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("categories", value)
			for key, element in value.iteritems():
				assert type(key) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("categories", key)
				assert type(element) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("categories", element)
		self.__categories = value

	@categories.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def categories(self):
		"""
		Deleter for **self.__categories** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "categories"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __getitem__(self, action):
		"""
		Reimplements the :meth:`object.__getitem__` method.

		:param action: Action name.
		:type action: unicode
		:return: Action.
		:rtype: QAction
		"""

		action = self.__normalizeName(action)
		for path, name, object in foundations.walkers.dictionariesWalker(self.__categories):
			if action == foundations.namespace.setNamespace(self.__namespaceSplitter.join(path), name):
				LOGGER.debug("> Retrieved object for '{0}' action name!".format(action))
				return object
		raise umbra.exceptions.ActionExistsError(
			"{0} | '{1}' action isn't registered!".format(self.__class__.__name__, action))

	def __setitem__(self, action, kwargs):
		"""
		Reimplements the :meth:`object.__setitem__` method.

		:param action: Action.
		:type action: unicode
		:param kwargs: kwargs.
		:type kwargs: dict
		"""

		self.registerAction(action, **kwargs)

	def __iter__(self):
		"""
		Reimplements the :meth:`object.__iter__` method.

		:return: Actions iterator.
		:rtype: object
		"""

		return foundations.walkers.dictionariesWalker(self.__categories)

	def __contains__(self, action):
		"""
		Reimplements the :meth:`object.__contains__` method.

		:param action: Action name.
		:type action: unicode
		:return: Action existence.
		:rtype: bool
		"""

		for path, name, object in self:
			if foundations.namespace.setNamespace(self.__namespaceSplitter.join(path), name) == action:
				return True
		return False

	def __len__(self):
		"""
		Reimplements the :meth:`object.__len__` method.

		:return: Actions count.
		:rtype: int
		"""

		return len([action for action in self])

	def __normalizeName(self, name):
		"""
		Normalizes given action name.

		:param name: Action name.
		:type name: unicode
		:return: Normalized name.
		:rtype: bool
		"""

		if not name.startswith(self.__rootNamespace):
			name = foundations.namespace.setNamespace(self.__rootNamespace,
													  foundations.namespace.setNamespace(self.__defaultNamespace, name))
			LOGGER.debug("> Normalized name: '{0}'.".format(name))
			return name
		else:
			LOGGER.debug("> Name '{0}' is already normalized!".format(name))
			return name

	def __getCategory(self, category, name, vivify=False):
		"""
		Gets recusively requested category, alternately if **vivify** argument is set,
		the category will be created.

		:param category: Base category.
		:type category: dict
		:param name: Category to retrieve or vivify.
		:type name: unicode
		:param vivify: Vivify missing parents in the chain to the requested category.
		:type vivify: bool
		:return: Requested category.
		:rtype: dict
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

	def get(self, action, default=None):
		"""
		Returns given action value.

		:param action: Action name.
		:type action: unicode
		:param default: Default value if action is not found.
		:type default: object
		:return: Action.
		:rtype: QAction
		"""

		try:
			return self.__getitem__(action)
		except KeyError as error:
			return default

	def listActions(self):
		"""
		Returns the registered actions.

		:return: Actions list.
		:rtype: list
		"""

		actions = []
		for path, actionName, action in self:
			actions.append(self.__namespaceSplitter.join(itertools.chain(path, (actionName,))))
		return sorted(actions)

	@foundations.exceptions.handleExceptions(umbra.exceptions.CategoryExistsError)
	def getCategory(self, name, vivify=False):
		"""
		Returns requested category.

		:param name: Category to retrieve.
		:type name: unicode
		:param vivify: Vivify missing parents in the chain to the requested category.
		:type vivify: bool
		:return: Category.
		:rtype: dict
		"""

		category = self.__getCategory(self.__categories, name, vivify)
		if isinstance(category, dict):
			LOGGER.debug("> Category '{0}': '{1}'.".format(name, category))
			return category
		else:
			raise umbra.exceptions.CategoryExistsError("{0} | '{1}' category doesn't exists!".format
													   (self.__class__.__name__, name))

	def addToCategory(self, category, name, action):
		"""
		Adds given action to given category.

		:param category: Category to store the action.
		:type category: unicode
		:param name: Action name.
		:type name: unicode
		:param action: Action object.
		:type action: QAction
		:return: Method success.
		:rtype: bool
		"""

		category = self.getCategory(category, vivify=True)
		if not isinstance(category, dict):
			return False

		category[name] = action
		LOGGER.debug("> Added '{0}' action to '{1}' category!".format(category, name))
		return True

	def removeFromCategory(self, category, name):
		"""
		Removes given action from given category.

		:param category: Category to remove the action from.
		:type category: unicode
		:param name: Action name.
		:type name: unicode
		:return: Method success.
		:rtype: bool
		"""

		category = self.getCategory(category)
		if not isinstance(category, dict):
			return False

		del (category[name])
		LOGGER.debug("> Removed '{0}' action from '{1}' category!".format(category, name))
		return True

	@foundations.exceptions.handleExceptions(umbra.exceptions.ActionExistsError)
	def getAction(self, action):
		"""
		Returns requested action.

		:param action: Action name.
		:type action: unicode
		:return: Action.
		:rtype: QAction
		"""

		return self[action]

	def isActionRegistered(self, name):
		"""
		Returns if the given action name is registered.

		:param name: Action name.
		:type name: unicode
		:return: Is action registered.
		:rtype: bool
		"""

		return name in self

	def registerAction(self, name, **kwargs):
		"""
		Registers given action name, optional arguments like a parent, icon, slot etc ... can be given.

		:param name: Action to register.
		:type name: unicode
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Action.
		:rtype: QAction
		"""

		settings = foundations.dataStructures.Structure(**{"parent": None,
														   "text": None,
														   "icon": None,
														   "iconText": None,
														   "checkable": None,
														   "checked": None,
														   "statusTip": None,
														   "whatsThis": None,
														   "toolTip": None,
														   "shortcut": None,
														   "shortcutContext": None,
														   "slot": None})
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

	def unregisterAction(self, name):
		"""
		Unregisters given action name.

		:param name: Action to register.
		:type name: unicode
		:return: Method success.
		:rtype: bool
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

	def isShortcutInUse(self, shortcut):
		"""
		Returns if given action shortcut is in use.

		:param name: Action shortcut.
		:type name: unicode
		:return: Is shortcut in use.
		:rtype: bool
		"""

		for path, actionName, action in foundations.walkers.dictionariesWalker(self.__categories):
			if action.shortcut() == QKeySequence(shortcut):
				return True
		return False

	def getShortcut(self, name):
		"""
		Returns given action shortcut.

		:param name: Action to retrieve the shortcut.
		:type name: unicode
		:return: Action shortcut.
		:rtype: unicode
		"""

		name = self.__normalizeName(name)
		action = self.getAction(name)
		if not action:
			return ""

		return action.shortcut().toString()

	def setShortcut(self, name, shortcut):
		"""
		Sets given action shortcut.

		:param name: Action to set the shortcut.
		:type name: unicode
		:param shortcut: Shortcut to set.
		:type shortcut: unicode
		:return: Method success.
		:rtype: bool
		"""

		name = self.__normalizeName(name)
		action = self.getAction(name)
		if not action:
			return

		action.setShortcut(QKeySequence(shortcut))
		return True
