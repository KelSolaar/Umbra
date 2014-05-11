#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`umbra.components.factory.components_manager_ui.components_manager_ui.ComponentsManagerUi`
    Component Interface class nodes.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtCore import Qt

import foundations.exceptions
import foundations.verbose
import umbra.ui.nodes

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "PathNode", "ComponentNode"]

LOGGER = foundations.verbose.install_logger()


class PathNode(umbra.ui.nodes.GraphModelNode):
    """
    Defines :class:`umbra.components.factory.components_manager_ui.components_manager_ui.ComponentsManagerUi`
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
                 node_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
                 attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
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
        :param node_flags: Node flags.
        :type node_flags: int
        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        umbra.ui.nodes.GraphModelNode.__init__(self, name, parent, children, roles, node_flags, **kwargs)

        PathNode.__initialize_node(self, attributes_flags)

    def __initialize_node(self, attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
        """
        Initializes the node.

        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        """

        self["activated"] = umbra.ui.nodes.GraphModelAttribute(name="activated",
                                                               flags=attributes_flags)
        self["category"] = umbra.ui.nodes.GraphModelAttribute(name="category",
                                                              flags=attributes_flags)
        self["require"] = umbra.ui.nodes.GraphModelAttribute(name="require",
                                                             flags=attributes_flags)
        self["version"] = umbra.ui.nodes.GraphModelAttribute(name="version",
                                                             flags=attributes_flags)


class ComponentNode(umbra.ui.nodes.GraphModelNode):
    """
    Defines
    :class:`umbra.components.factory.components_manager_ui.components_manager_ui.ComponentsManagerUi`
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
                 node_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
                 attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
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
        :param node_flags: Node flags.
        :type node_flags: int
        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        umbra.ui.nodes.GraphModelNode.__init__(self, name, parent, children, roles, node_flags, **kwargs)

        # --- Setting class attributes. ---
        self.__component = component
        self.__tool_tip_text = """
                <p><b>{0}</b></p>
                <p><b>Author: </b>{1}<br>
                <b>Category: </b>{2}<br>
                <b>Dependencies: </b>{3}<br>
                <b>Version: </b>{4}<br>
                <b>Description: </b>{5}<br></p>
                """

        ComponentNode.__initialize_node(self, attributes_flags)

    @property
    def component(self):
        """
        Property for **self.__component** attribute.

        :return: self.__component.
        :rtype: Component or QWidgetComponent or QObjectComponent
        """

        return self.__component

    @component.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def component(self, value):
        """
        Setter for **self.__component** attribute.

        :param value: Attribute value.
        :type value: Component or QWidgetComponent or QObjectComponent
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "component"))

    @component.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def component(self):
        """
        Deleter for **self.__component** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "component"))

    @property
    def tool_tip_text(self):
        """
        Property for **self.__tool_tip_text** attribute.

        :return: self.__tool_tip_text.
        :rtype: unicode
        """

        return self.__tool_tip_text

    @tool_tip_text.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def tool_tip_text(self, value):
        """
        Setter for **self.__tool_tip_text** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format(
                "tool_tip_text", value)
        self.__tool_tip_text = value

    @tool_tip_text.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def tool_tip_text(self):
        """
        Deleter for **self.__tool_tip_text** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "tool_tip_text"))

    def __initialize_node(self, attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
        """
        Initializes the node.

        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        """

        attributes = dir(self.__component)
        for attribute in attributes:
            if attribute == "name":
                continue

            if not "_Profile__{0}".format(attribute) in attributes:
                continue

            value = getattr(self.__component, attribute)
            value = ", ".join(value) if type(value) in (tuple, list) else value
            roles = {Qt.DisplayRole: value,
                     Qt.EditRole: value}
            self[attribute] = umbra.ui.nodes.GraphModelAttribute(attribute, value, roles, attributes_flags)

        self.update_tool_tip()

    def update_tool_tip(self):
        """
        Updates the node tooltip.

        :return: Method success.
        :rtype: bool
        """

        self.roles[Qt.ToolTipRole] = self.__tool_tip_text.format(self.component.name,
                                                                 self.component.author,
                                                                 self.component.category,
                                                                 ", ".join(self.component.require),
                                                                 self.component.version,
                                                                 self.component.description)
        return True
