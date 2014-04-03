#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`umbra.components.factory.componentsManagerUi.componentsManagerUi.ComponentsManagerUi`
	Component Interface class nodes.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import umbra.ui.nodes

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "PathNode", "ComponentNode"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class PathNode(umbra.ui.nodes.GraphModelNode):
	"""
	Defines :class:`umbra.components.factory.componentsManagerUi.componentsManagerUi.ComponentsManagerUi`
		Component Interface class Model path node.
	"""

	__family = "Path"
	"""
	:param __family: Node family.
	:type __family: unicode
	"""

	def __init__(self,
				name=None,
				parent=None,
				children=None,
				roles=None,
				nodeFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				**kwargs):
		"""
		Initializes the class.

		:param name: Node name.
		:type name: unicode
		:param parent: Node parent.
		:type parent: GraphModelNode
		:param children: Children.
		:type children: list
		:param roles: Roles.
		:type roles: dict
		:param nodeFlags: Node flags.
		:type nodeFlags: int
		:param attributesFlags: Attributes flags.
		:type attributesFlags: int
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.nodes.GraphModelNode.__init__(self, name, parent, children, roles, nodeFlags, **kwargs)

		PathNode.__initializeNode(self, attributesFlags)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self, attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		Initializes the node.
		
		:param attributesFlags: Attributes flags.
		:type attributesFlags: int
		"""

		self["activated"] = umbra.ui.nodes.GraphModelAttribute(name="activated",
																flags=attributesFlags)
		self["category"] = umbra.ui.nodes.GraphModelAttribute(name="category",
																flags=attributesFlags)
		self["require"] = umbra.ui.nodes.GraphModelAttribute(name="require",
																flags=attributesFlags)
		self["version"] = umbra.ui.nodes.GraphModelAttribute(name="version",
																flags=attributesFlags)

class ComponentNode(umbra.ui.nodes.GraphModelNode):
	"""
	Defines
	:class:`umbra.components.factory.componentsManagerUi.componentsManagerUi.ComponentsManagerUi`
	Component Interface class Model component node.
	"""

	__family = "Component"
	"""
	:param __family: Node family.
	:type __family: unicode
	"""

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
		Initializes the class.

		:param component: Component.
		:type component: Component or QWidgetComponent or QObjectComponent
		:param name: Node name.
		:type name: unicode
		:param parent: Node parent.
		:type parent: GraphModelNode
		:param children: Children.
		:type children: list
		:param roles: Roles.
		:type roles: dict
		:param nodeFlags: Node flags.
		:type nodeFlags: int
		:param attributesFlags: Attributes flags.
		:type attributesFlags: int
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.nodes.GraphModelNode.__init__(self, name, parent, children, roles, nodeFlags, **kwargs)

		# --- Setting class attributes. ---
		self.__component = component
		self.__toolTipText = """
				<p><b>{0}</b></p>
				<p><b>Author: </b>{1}<br>
				<b>Category: </b>{2}<br>
				<b>Dependencies: </b>{3}<br>
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
		Property for **self.__component** attribute.

		:return: self.__component.
		:rtype: Component or QWidgetComponent or QObjectComponent
		"""

		return self.__component

	@component.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def component(self, value):
		"""
		Setter for **self.__component** attribute.

		:param value: Attribute value.
		:type value: Component or QWidgetComponent or QObjectComponent
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "component"))

	@component.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def component(self):
		"""
		Deleter for **self.__component** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "component"))

	@property
	def toolTipText(self):
		"""
		Property for **self.__toolTipText** attribute.

		:return: self.__toolTipText.
		:rtype: unicode
		"""

		return self.__toolTipText

	@toolTipText.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def toolTipText(self, value):
		"""
		Setter for **self.__toolTipText** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
			"toolTipText", value)
		self.__toolTipText = value

	@toolTipText.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def toolTipText(self):
		"""
		Deleter for **self.__toolTipText** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "toolTipText"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self, attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		Initializes the node.
		
		:param attributesFlags: Attributes flags.
		:type attributesFlags: int
		"""

		attributes = dir(self.__component)
		for attribute in attributes:
			if attribute == "name":
				continue

			if not "_Profile__{0}".format(attribute) in attributes:
				continue

			value = getattr(self.__component, attribute)
			value = ", ".join(value) if type(value) in (tuple, list) else value
			roles = {Qt.DisplayRole : value,
					Qt.EditRole : value}
			self[attribute] = umbra.ui.nodes.GraphModelAttribute(attribute, value, roles, attributesFlags)

		self.updateToolTip()

	def updateToolTip(self):
		"""
		Updates the node tooltip.

		:return: Method success.
		:rtype: bool
		"""

		self.roles[Qt.ToolTipRole] = self.__toolTipText.format(self.component.name,
																self.component.author,
																self.component.category,
																", ".join(self.component.require),
																self.component.version,
																self.component.description)
		return True
