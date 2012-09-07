#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`umbra.components.factory.componentsManagerUi.componentsManagerUi.ComponentsManagerUi`
	Component Interface class nodes.

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
import umbra.ui.nodes
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

__all__ = ["LOGGER", "PathNode", "ComponentNode"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class PathNode(umbra.ui.nodes.GraphModelNode):
	"""
	This class factory defines :class:`umbra.components.factory.componentsManagerUi.componentsManagerUi.ComponentsManagerUi`
		Component Interface class Model path node.
	"""

	__family = "Category"
	"""Node family. ( String )"""

	@core.executionTrace
	def __init__(self,
				name=None,
				parent=None,
				children=None,
				roles=None,
				nodeFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				**kwargs):
		"""
		This method initializes the class.

		:param name: Node name.  ( String )
		:param parent: Node parent. ( GraphModelNode )
		:param children: Children. ( List )
		:param roles: Roles. ( Dictionary )
		:param nodeFlags: Node flags. ( Integer )
		:param attributesFlags: Attributes flags. ( Integer )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.nodes.GraphModelNode.__init__(self, name, parent, children, roles, nodeFlags, **kwargs)

		PathNode.__initializeNode(self, attributesFlags)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __initializeNode(self, attributesFlags):
		"""
		This method initializes the node.
		
		:param attributesFlags: Attributes flags. ( Integer )
		"""

		pass

class ComponentNode(umbra.ui.nodes.GraphModelNode):
	"""
	This class factory defines
	:class:`umbra.components.factory.componentsManagerUi.componentsManagerUi.ComponentsManagerUi`
	Component Interface class Model component node.
	"""

	__family = "Component"
	"""Node family. ( String )"""

	@core.executionTrace
	def __init__(self,
				component,
				name=None,
				parent=None,
				children=None,
				roles=None,
				nodeFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				**kwargs):
		"""
		This method initializes the class.

		:param component: Component.  ( Component / QWidgetComponent / QObjectComponent )
		:param name: Node name.  ( String )
		:param parent: Node parent. ( GraphModelNode )
		:param children: Children. ( List )
		:param roles: Roles. ( Dictionary )
		:param nodeFlags: Node flags. ( Integer )
		:param attributesFlags: Attributes flags. ( Integer )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.nodes.GraphModelNode.__init__(self, name, parent, children, roles, nodeFlags, **kwargs)

		# --- Setting class attributes. ---
		self.__component = component
		self.__toolTipText = """
				<p><b>{0}</b></p>
				<p><b>Author: </b>{1}<br>
				<b>Category: </b>{2}<br>
				<b>Rank: </b>{3}<br>
				<b>Version: </b>{4}<br>
				<b>Description: </b>{5}<br></p>
				"""

		ComponentNode.__initializeNode(self, attributesFlags)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def component(self):
		"""
		This method is the property for **self.__component** attribute.

		:return: self.__component. ( Component / QWidgetComponent / QObjectComponent )
		"""

		return self.__component

	@component.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def component(self, value):
		"""
		This method is the setter method for **self.__component** attribute.

		:param value: Attribute value. ( Component / QWidgetComponent / QObjectComponent )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "component"))

	@component.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def component(self):
		"""
		This method is the deleter method for **self.__component** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "component"))

	@property
	def toolTipText(self):
		"""
		This method is the property for **self.__toolTipText** attribute.

		:return: self.__toolTipText. ( String )
		"""

		return self.__toolTipText

	@toolTipText.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def toolTipText(self, value):
		"""
		This method is the setter method for **self.__toolTipText** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format(
			"toolTipText", value)
		self.__toolTipText = value

	@toolTipText.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def toolTipText(self):
		"""
		This method is the deleter method for **self.__toolTipText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "toolTipText"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	def __initializeNode(self, attributesFlags):
		"""
		This method initializes the node.
		
		:param attributesFlags: Attributes flags. ( Integer )
		"""

		attributes = dir(self.__component)
		for attribute in attributes:
			if attribute == "name":
				continue

			if not "_Profile__{0}".format(attribute) in attributes:
				continue

			value = getattr(self.__component, attribute)
			roles = {Qt.DisplayRole : value,
					Qt.EditRole : value}
			self[attribute] = umbra.ui.nodes.GraphModelAttribute(attribute, value, roles, attributesFlags)

		self.synchronizeToolTip()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def synchronizeToolTip(self):
		"""
		This method synchronizes the node tooltip.

		:return: Method success. ( Boolean )
		"""

		self.roles[Qt.ToolTipRole] = self.__toolTipText.format(self.component.name,
																self.component.author,
																self.component.category,
																self.component.rank,
																self.component.version,
																self.component.description)
		return True
