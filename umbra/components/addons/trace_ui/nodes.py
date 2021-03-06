#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`umbra.components.factory.trace_ui.trace_ui.TraceUi`
    Component Interface class nodes.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtCore import Qt

import foundations.exceptions
import foundations.verbose
import foundations.trace
import umbra.ui.nodes

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "ModuleNode"]

LOGGER = foundations.verbose.install_logger()


class ModuleNode(umbra.ui.nodes.GraphModelNode):
    """
    Defines :class:`umbra.components.factory.trace_ui.trace_ui.TraceUi`
    Component Interface class **Module** node.
    """

    __family = "Module"

    def __init__(self,
                 module=None,
                 name=None,
                 parent=None,
                 children=None,
                 roles=None,
                 node_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
                 attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
                 **kwargs):
        """
        Initializes the class.

        :param module: Module.
        :type module: ModuleType
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
        self.__module = module

        ModuleNode.__initialize_node(self, attributes_flags)

    @property
    def module(self):
        """
        Property for **self.__module** attribute.

        :return: self.__module.
        :rtype: object
        """

        return self.__module

    @module.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def module(self, value):
        """
        Setter for **self.__module** attribute.

        :param value: Attribute value.
        :type value: object
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "module"))

    @module.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def module(self):
        """
        Deleter for **self.__module** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "module"))

    def __initialize_node(self, attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
        """
        Initializes the node.

        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        """

        self["traced"] = umbra.ui.nodes.GraphModelAttribute(name="traced",
                                                            value=foundations.trace.is_traced(self.__module),
                                                            flags=attributes_flags)
        self.update_node_attributes()

    def update_node_attributes(self, attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
        """
        Updates the Node attributes.

        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        :return: Method success.
        :rtype: bool
        """

        self.traced.value = foundations.trace.is_traced(self.__module)
        self.traced.roles[Qt.DisplayRole] = foundations.strings.to_string(self.traced.value).title()
