#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**actions_manager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	| Defines the :class:`ActionsManager` class.
	| The :class:`ActionsManager` class provides a centralized hub to manage Applications actions.
	| It defines methods to register, unregister and list actions.

**Others:**

"""

from __future__ import unicode_literals

import re
import itertools
from PyQt4.QtCore import QObject
from PyQt4.QtGui import QAction
from PyQt4.QtGui import QKeySequence

import foundations.data_structures
import foundations.exceptions
import foundations.namespace
import foundations.verbose
import foundations.walkers
import umbra.exceptions

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "ActionsManager"]

LOGGER = foundations.verbose.install_logger()

class ActionsManager(QObject):
	"""
	Defines a `QObject <http://doc.qt.nokia.com/qobject.html>`_ subclass providing an actions manager.
	"""

	def __init__(self, parent=None, namespace_splitter="|", root_namespace="Actions", default_namespace="Others"):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param namespace_splitter: Namespace splitters character.
		:type namespace_splitter: unicode
		:param root_namespace: Root foundations.namespace.
		:type root_namespace: unicode
		:param default_namespace: Default namespace ( For actions with relative path ).
		:type default_namespace: unicode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QObject.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__namespace_splitter = None
		self.namespace_splitter = namespace_splitter
		self.__root_namespace = None
		self.root_namespace = root_namespace
		self.__default_namespace = None
		self.default_namespace = default_namespace

		self.__categories = {}

		self.__actions_signals_slots = {}

	@property
	def namespace_splitter(self):
		"""
		Property for **self.__namespace_splitter** attribute.

		:return: self.__namespace_splitter.
		:rtype: unicode
		"""

		return self.__namespace_splitter

	@namespace_splitter.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def namespace_splitter(self, value):
		"""
		Setter for **self.__namespace_splitter** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"namespace_splitter", value)
			assert len(value) == 1, "'{0}' attribute: '{1}' has multiples characters!".format("namespace_splitter",
																							  value)
			assert not re.search(r"\w", value), "'{0}' attribute: '{1}' is an alphanumeric character!".format(
				"namespace_splitter", value)
		self.__namespace_splitter = value

	@namespace_splitter.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def namespace_splitter(self):
		"""
		Deleter for **self.__namespace_splitter** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "namespace_splitter"))

	@property
	def root_namespace(self):
		"""
		Property for **self.__root_namespace** attribute.

		:return: self.__root_namespace.
		:rtype: unicode
		"""

		return self.__root_namespace

	@root_namespace.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def root_namespace(self, value):
		"""
		Setter for **self.__root_namespace** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"root_namespace", value)
		self.__root_namespace = value

	@root_namespace.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def root_namespace(self):
		"""
		Deleter for **self.__root_namespace** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "root_namespace"))

	@property
	def default_namespace(self):
		"""
		Property for **self.__default_namespace** attribute.

		:return: self.__default_namespace.
		:rtype: unicode
		"""

		return self.__default_namespace

	@default_namespace.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def default_namespace(self, value):
		"""
		Setter for **self.__default_namespace** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
				"default_namespace", value)
		self.__default_namespace = value

	@default_namespace.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_namespace(self):
		"""
		Deleter for **self.__default_namespace** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_namespace"))

	@property
	def categories(self):
		"""
		Property for **self.__categories** attribute.

		:return: self.__categories.
		:rtype: dict
		"""

		return self.__categories

	@categories.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def categories(self):
		"""
		Deleter for **self.__categories** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "categories"))

	def __getitem__(self, action):
		"""
		Reimplements the :meth:`object.__getitem__` method.

		:param action: Action name.
		:type action: unicode
		:return: Action.
		:rtype: QAction
		"""

		action = self.__normalize_name(action)
		for path, name, object in foundations.walkers.dictionaries_walker(self.__categories):
			if action == foundations.namespace.set_namespace(self.__namespace_splitter.join(path), name):
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

		self.register_action(action, **kwargs)

	def __iter__(self):
		"""
		Reimplements the :meth:`object.__iter__` method.

		:return: Actions iterator.
		:rtype: object
		"""

		return foundations.walkers.dictionaries_walker(self.__categories)

	def __contains__(self, action):
		"""
		Reimplements the :meth:`object.__contains__` method.

		:param action: Action name.
		:type action: unicode
		:return: Action existence.
		:rtype: bool
		"""

		for path, name, object in self:
			if foundations.namespace.set_namespace(self.__namespace_splitter.join(path), name) == action:
				return True
		return False

	def __len__(self):
		"""
		Reimplements the :meth:`object.__len__` method.

		:return: Actions count.
		:rtype: int
		"""

		return len([action for action in self])

	def __normalize_name(self, name):
		"""
		Normalizes given action name.

		:param name: Action name.
		:type name: unicode
		:return: Normalized name.
		:rtype: bool
		"""

		if not name.startswith(self.__root_namespace):
			name = foundations.namespace.set_namespace(self.__root_namespace,
													  foundations.namespace.set_namespace(self.__default_namespace, name))
			LOGGER.debug("> Normalized name: '{0}'.".format(name))
			return name
		else:
			LOGGER.debug("> Name '{0}' is already normalized!".format(name))
			return name

	def __get_category(self, category, name, vivify=False):
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

		namespace = foundations.namespace.get_namespace(name, root_only=True)
		name = foundations.namespace.remove_namespace(name, root_only=True)
		if namespace:
			if vivify and namespace not in category:
				category[namespace] = {}
			return self.__get_category(category[namespace], name, vivify)
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

	def list_actions(self):
		"""
		Returns the registered actions.

		:return: Actions list.
		:rtype: list
		"""

		actions = []
		for path, actionName, action in self:
			actions.append(self.__namespace_splitter.join(itertools.chain(path, (actionName,))))
		return sorted(actions)

	@foundations.exceptions.handle_exceptions(umbra.exceptions.CategoryExistsError)
	def get_category(self, name, vivify=False):
		"""
		Returns requested category.

		:param name: Category to retrieve.
		:type name: unicode
		:param vivify: Vivify missing parents in the chain to the requested category.
		:type vivify: bool
		:return: Category.
		:rtype: dict
		"""

		category = self.__get_category(self.__categories, name, vivify)
		if isinstance(category, dict):
			LOGGER.debug("> Category '{0}': '{1}'.".format(name, category))
			return category
		else:
			raise umbra.exceptions.CategoryExistsError("{0} | '{1}' category doesn't exists!".format
													   (self.__class__.__name__, name))

	def add_to_category(self, category, name, action):
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

		category = self.get_category(category, vivify=True)
		if not isinstance(category, dict):
			return False

		category[name] = action
		LOGGER.debug("> Added '{0}' action to '{1}' category!".format(category, name))
		return True

	def remove_from_category(self, category, name):
		"""
		Removes given action from given category.

		:param category: Category to remove the action from.
		:type category: unicode
		:param name: Action name.
		:type name: unicode
		:return: Method success.
		:rtype: bool
		"""

		category = self.get_category(category)
		if not isinstance(category, dict):
			return False

		del (category[name])
		LOGGER.debug("> Removed '{0}' action from '{1}' category!".format(category, name))
		return True

	@foundations.exceptions.handle_exceptions(umbra.exceptions.ActionExistsError)
	def get_action(self, action):
		"""
		Returns requested action.

		:param action: Action name.
		:type action: unicode
		:return: Action.
		:rtype: QAction
		"""

		return self[action]

	def is_action_registered(self, name):
		"""
		Returns if the given action name is registered.

		:param name: Action name.
		:type name: unicode
		:return: Is action registered.
		:rtype: bool
		"""

		return name in self

	def register_action(self, name, **kwargs):
		"""
		Registers given action name, optional arguments like a parent, icon, slot etc ... can be given.

		:param name: Action to register.
		:type name: unicode
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Action.
		:rtype: QAction
		"""

		settings = foundations.data_structures.Structure(**{"parent": None,
														   "text": None,
														   "icon": None,
														   "icon_text": None,
														   "checkable": None,
														   "checked": None,
														   "status_tip": None,
														   "whats_this": None,
														   "tool_tip": None,
														   "shortcut": None,
														   "shortcut_context": None,
														   "slot": None})
		settings.update(kwargs)

		name = self.__normalize_name(name)
		category = foundations.namespace.get_namespace(name)
		name = foundations.namespace.remove_namespace(name)

		action = QAction(name, settings.parent or self)
		self.add_to_category(category, name, action)

		settings.text and action.setText(settings.text)
		settings.icon and action.setIcon(settings.icon)
		settings.icon_text and action.setIconText(settings.icon_text)
		settings.checkable and action.setCheckable(settings.checkable)
		settings.checked and action.set_checked(settings.checked)
		settings.status_tip and action.setStatusTip(settings.status_tip)
		settings.whats_this and action.setWhatsThis(settings.whats_this)
		settings.tool_tip and action.setToolTip(settings.tool_tip)
		settings.shortcut and action.setShortcut(QKeySequence(settings.shortcut))
		settings.shortcut_context and action.setShortcutContext(settings.shortcut_context)
		if settings.slot:
			self.__actions_signals_slots[action] = settings.slot
			action.triggered.connect(settings.slot)
		return action

	def unregister_action(self, name):
		"""
		Unregisters given action name.

		:param name: Action to register.
		:type name: unicode
		:return: Method success.
		:rtype: bool
		"""

		name = self.__normalize_name(name)
		action = self.get_action(name)
		if not action:
			return False

		action.triggered.disconnect(self.__actions_signals_slots.pop(action))

		category = foundations.namespace.get_namespace(name)
		name = foundations.namespace.remove_namespace(name)
		self.remove_from_category(category, name)
		return True

	def is_shortcut_in_use(self, shortcut):
		"""
		Returns if given action shortcut is in use.

		:param name: Action shortcut.
		:type name: unicode
		:return: Is shortcut in use.
		:rtype: bool
		"""

		for path, actionName, action in foundations.walkers.dictionaries_walker(self.__categories):
			if action.shortcut() == QKeySequence(shortcut):
				return True
		return False

	def get_shortcut(self, name):
		"""
		Returns given action shortcut.

		:param name: Action to retrieve the shortcut.
		:type name: unicode
		:return: Action shortcut.
		:rtype: unicode
		"""

		name = self.__normalize_name(name)
		action = self.get_action(name)
		if not action:
			return ""

		return action.shortcut().toString()

	def set_shortcut(self, name, shortcut):
		"""
		Sets given action shortcut.

		:param name: Action to set the shortcut.
		:type name: unicode
		:param shortcut: Shortcut to set.
		:type shortcut: unicode
		:return: Method success.
		:rtype: bool
		"""

		name = self.__normalize_name(name)
		action = self.get_action(name)
		if not action:
			return

		action.setShortcut(QKeySequence(shortcut))
		return True
