#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the Application nodes classes.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import umbra.ui.models
from foundations.nodes import AbstractCompositeNode
from foundations.nodes import Attribute

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
		"Mixin_GraphModelObject",
		"GraphModelAttribute",
		"GraphModelNode",
		"DefaultNode" ,
		"FormatNode"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Mixin_GraphModelObject(object):
	"""
	This class is a mixin used to bring common capabilities in Application Nodes classes.
	"""

	def __init__(self):
		"""
		This method initializes the class.

		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		# --- Setting class attributes. ---
		self.__roles = None
		self.__flags = None

		self.__triggerModel = False

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def roles(self):
		"""
		This method is the property for **self.__roles** attribute.
	
		:return: self.__roles. ( Dictionary )
		"""

		return self.__roles

	@roles.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def roles(self, value):
		"""
		This method is the setter method for **self.__roles** attribute.
	
		:param value: Attribute value. ( Dictionary )
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("roles", value)
			for key in value:
				assert type(key) is Qt.ItemDataRole, "'{0}' attribute: '{1}' type is not 'Qt.ItemDataRole'!".format("roles", key)
		self.__roles = value

	@roles.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def roles(self):
		"""
		This method is the deleter method for **self.__roles** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "roles"))

	@property
	def flags(self):
		"""
		This method is the property for **self.__flags** attribute.
	
		:return: self.__flags. ( Integer )
		"""

		return self.__flags

	@flags.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def flags(self, value):
		"""
		This method is the setter method for **self.__flags** attribute.
	
		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("flags", value)
		self.__flags = value

	@flags.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def flags(self):
		"""
		This method is the deleter method for **self.__flags** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "flags"))

	@property
	def triggerModel(self):
		"""
		This method is the property for **self.__triggerModel** attribute.
	
		:return: self.__triggerModel. ( Boolean )
		"""

		return self.__triggerModel

	@triggerModel.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def triggerModel(self, value):
		"""
		This method is the setter method for **self.__triggerModel** attribute.
	
		:param value: Attribute value. ( Boolean )
		"""

		if value is not None:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("triggerModel", value)
		self.__triggerModel = value

	@triggerModel.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def triggerModel(self):
		"""
		This method is the deleter method for **self.__triggerModel** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "triggerModel"))

class GraphModelAttribute(Attribute, Mixin_GraphModelObject):
	"""
	This class represents a storage object for the :class:`GraphModelNode` class attributes.
	"""

	def __init__(self, name=None, value=None, roles=None, flags=None, **kwargs):
		"""
		This method initializes the class.

		:param name: Attribute name. ( String )
		:param value: Attribute value. ( Object )
		:param roles: Roles. ( Dictionary )
		:param flags: Flags. ( Integer )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		Attribute.__init__(self, name, value, **kwargs)
		Mixin_GraphModelObject.__init__(self)

		# --- Setting class attributes. ---
		self.roles = roles or {Qt.DisplayRole : value, Qt.EditRole : value}
		self.flags = flags or int(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __setattr__(self, attribute, value):
		"""
		This method reimplements the :meth:`foundations.nodes.Attribute.__setattr__` method.

		:param attribute: Attribute. ( Object )
		:param value: Value. ( Object )
		"""

		currentValue = getattr(self, attribute, None)

		Attribute.__setattr__(self, attribute, value)

		if not attribute in ("_Attribute__name",
							"_Attribute__value",
							"_Attribute__roles",
							"_Attribute__flags"):
			return

		triggerModel = getattr(self, "_Mixin_GraphModelObject__triggerModel", False)
		if triggerModel and value is not currentValue:
			self.attributeChanged()

	__setitem__ = __setattr__

	def attributeChanged(self):
		"""
		This method triggers the host model(s) :meth:`umbra.ui.models.GraphModel.attributeChanged` method.
		
		:return: Method success. ( Boolean )
		"""

		for model in umbra.ui.models.GraphModel.findModel(self):
			headers = model.horizontalHeaders.values()
			if not self.name in headers:
				continue

			model.attributeChanged(model.findNode(self), headers.index(self.name))
		return True

class GraphModelNode(AbstractCompositeNode, Mixin_GraphModelObject):
	"""
	This class defines :class:`GraphModel` class base Node object.
	"""

	__family = "GraphModel"
	"""Node family. ( String )"""

	def __init__(self, name=None, parent=None, children=None, roles=None, flags=None, **kwargs):
		"""
		This method initializes the class.

		:param name: Node name.  ( String )
		:param parent: Node parent. ( AbstractNode / AbstractCompositeNode )
		:param children: Children. ( List )
		:param roles: Roles. ( Dictionary )
		:param flags: Flags. ( Qt.ItemFlag )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractCompositeNode.__init__(self, name, parent, children, **kwargs)
		Mixin_GraphModelObject.__init__(self)

		# --- Setting class attributes. ---
		self.roles = roles or {Qt.DisplayRole : self.name, Qt.EditRole : self.name}
		self.flags = flags or int(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __setattr__(self, attribute, value):
		"""
		This method reimplements the :meth:`foundations.nodes.AbstractCompositeNode.__setattr__` method.

		:param attribute.: Attribute. ( Object )
		:param value.: Value. ( Object )
		"""

		currentValue = getattr(self, attribute, None)

		AbstractCompositeNode.__setattr__(self, attribute, value)

		if not attribute in ("_GraphModelNode__name",
							"_GraphModelNode__roles",
							"_GraphModelNode__flags"):
			return

		triggerModel = getattr(self, "_Mixin_GraphModelObject__triggerModel", False)
		if triggerModel and value is not currentValue:
			self.nodeChanged()

	__setitem__ = __setattr__

	def nodeChanged(self):
		"""
		This method triggers the host model(s) :meth:`umbra.ui.models.GraphModel.nodeChanged` method.
		
		:return: Method success. ( Boolean )
		"""

		for model in umbra.ui.models.GraphModel.findModel(self):
			model.nodeChanged(self)
		return True

class DefaultNode(AbstractCompositeNode):
	"""
	| This class defines the default Node used in :class:`GraphModel` class model.
	| This simple Node is used as an invisible root Node for :class:`GraphModel` class models.
	"""

	__family = "Default"
	"""Node family. ( String )"""

	def __init__(self, name=None, parent=None, children=None, **kwargs):
		"""
		This method initializes the class.

		:param name: Node name.  ( String )
		:param parent: Node parent. ( AbstractCompositeNode )
		:param children: Children. ( List )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractCompositeNode.__init__(self, name, parent, children, **kwargs)

class FormatNode(AbstractCompositeNode):
	"""
	This class defines the format base Node object.
	"""

	__family = "Format"
	"""Node family. ( String )"""

	def __init__(self, name=None, parent=None, children=None, format=None, **kwargs):
		"""
		This method initializes the class.

		:param name: Node name.  ( String )
		:param parent: Node parent. ( AbstractNode / AbstractCompositeNode )
		:param children: Children. ( List )
		:param format: Format. ( Object )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		AbstractCompositeNode.__init__(self, name, parent, children, **kwargs)

		# --- Setting class attributes. ---
		self.__format = None
		self.format = format

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def format(self):
		"""
		This method is the property for **self.__format** attribute.

		:return: self.__format. ( Object )
		"""

		return self.__format

	@format.setter
	def format(self, value):
		"""
		This method is the setter method for **self.__format** attribute.

		:param value: Attribute value. ( Object )
		"""

		self.__format = value

	@format.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def format(self):
		"""
		This method is the deleter method for **self.__format** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "format"))

