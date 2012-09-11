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
import logging
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
from foundations.nodes import AbstractCompositeNode
from foundations.nodes import Attribute
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

__all__ = ["LOGGER", "GraphModelAttribute", "GraphModelNode", "DefaultNode" , "FormatNode"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class GraphModelAttribute(Attribute):
	"""
	This class represents a storage object for the :class:`GraphModelNode` class attributes.
	"""

	@core.executionTrace
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

		# --- Setting class attributes. ---
		self.__roles = None
		self.roles = roles or {Qt.DisplayRole : value, Qt.EditRole : value}
		self.__flags = None
		self.flags = flags or int(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)

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
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
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
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def flags(self, value):
		"""
		This method is the setter method for **self.__flags** attribute.
	
		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("flags", value)
		self.__flags = value

	@flags.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def flags(self):
		"""
		This method is the deleter method for **self.__flags** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "flags"))

class GraphModelNode(AbstractCompositeNode):
	"""
	This class defines :class:`GraphModel` class base node object.
	"""

	__family = "GraphModel"
	"""Node family. ( String )"""

	@core.executionTrace
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

		# --- Setting class attributes. ---
		self.__roles = None
		self.roles = roles or {Qt.DisplayRole : name, Qt.EditRole : name}
		self.__flags = None
		self.flags = flags or int(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)

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
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def roles(self, value):
		"""
		This method is the setter method for **self.__roles** attribute.

		:param value: Attribute value. ( Dictionary )
		"""

		if value is not None:
			assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("roles", value)
			for key in value:
				assert type(key) is Qt.ItemDataRole, "'{0}' attribute: '{1}' type is not 'Qt.ItemDataRole'!".format(
				"roles", key)
		self.__roles = value

	@roles.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def flags(self, value):
		"""
		This method is the setter method for **self.__flags** attribute.
	
		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("flags", value)
		self.__flags = value

	@flags.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def flags(self):
		"""
		This method is the deleter method for **self.__flags** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "flags"))

class DefaultNode(AbstractCompositeNode):
	"""
	| This class defines the default node used in :class:`GraphModel` class model.
	| This simple node is used as an invisible root node for :class:`GraphModel` class models.
	"""

	__family = "Default"
	"""Node family. ( String )"""

	@core.executionTrace
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
	This class defines the format base node object.
	"""

	__family = "Format"
	"""Node family. ( String )"""

	@core.executionTrace
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
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def format(self, value):
		"""
		This method is the setter method for **self.__format** attribute.

		:param value: Attribute value. ( Object )
		"""

		self.__format = value

	@format.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def format(self):
		"""
		This method is the deleter method for **self.__format** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "format"))

