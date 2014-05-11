#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the Application nodes classes.

**Others:**

"""

from __future__ import unicode_literals

from PyQt4.QtCore import Qt

import foundations.exceptions
import foundations.verbose
import umbra.ui.models
from foundations.nodes import AbstractCompositeNode
from foundations.nodes import Attribute

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
           "Mixin_GraphModelObject",
           "GraphModelAttribute",
           "GraphModelNode",
           "DefaultNode",
           "FormatNode"]

LOGGER = foundations.verbose.install_logger()


class Mixin_GraphModelObject(object):
    """
    Defines a mixin used to bring common capabilities in Application Nodes classes.
    """

    def __init__(self):
        """
        Initializes the class.

        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        # --- Setting class attributes. ---
        self.__roles = None
        self.__flags = None

        self.__trigger_model = False

    @property
    def roles(self):
        """
        Property for **self.__roles** attribute.

        :return: self.__roles.
        :rtype: dict
        """

        return self.__roles

    @roles.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def roles(self, value):
        """
        Setter for **self.__roles** attribute.

        :param value: Attribute value.
        :type value: dict
        """

        if value is not None:
            assert type(value) is dict, "'{0}' attribute: '{1}' type is not 'dict'!".format("roles", value)
            for key in value:
                assert type(key) is Qt.ItemDataRole, "'{0}' attribute: '{1}' type is not 'Qt.ItemDataRole'!".format(
                    "roles", key)
        self.__roles = value

    @roles.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def roles(self):
        """
        Deleter for **self.__roles** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "roles"))

    @property
    def flags(self):
        """
        Property for **self.__flags** attribute.

        :return: self.__flags.
        :rtype: int
        """

        return self.__flags

    @flags.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def flags(self, value):
        """
        Setter for **self.__flags** attribute.

        :param value: Attribute value.
        :type value: int
        """

        if value is not None:
            assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("flags", value)
        self.__flags = value

    @flags.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def flags(self):
        """
        Deleter for **self.__flags** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "flags"))

    @property
    def trigger_model(self):
        """
        Property for **self.__trigger_model** attribute.

        :return: self.__trigger_model.
        :rtype: bool
        """

        return self.__trigger_model

    @trigger_model.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def trigger_model(self, value):
        """
        Setter for **self.__trigger_model** attribute.

        :param value: Attribute value.
        :type value: bool
        """

        if value is not None:
            assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("trigger_model", value)
        self.__trigger_model = value

    @trigger_model.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def trigger_model(self):
        """
        Deleter for **self.__trigger_model** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "trigger_model"))


class GraphModelAttribute(Attribute, Mixin_GraphModelObject):
    """
    Defines a storage object for the :class:`GraphModelNode` class attributes.
    """

    def __init__(self, name=None, value=None, roles=None, flags=None, **kwargs):
        """
        Initializes the class.

        :param name: Attribute name.
        :type name: unicode
        :param value: Attribute value.
        :type value: object
        :param roles: Roles.
        :type roles: dict
        :param flags: Flags.
        :type flags: int
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        Attribute.__init__(self, name, value, **kwargs)
        Mixin_GraphModelObject.__init__(self)

        # --- Setting class attributes. ---
        self.roles = roles or {Qt.DisplayRole: value, Qt.EditRole: value}
        self.flags = flags or int(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)

    def __setattr__(self, attribute, value):
        """
        Reimplements the :meth:`foundations.nodes.Attribute.__setattr__` method.

        :param attribute: Attribute.
        :type attribute: object
        :param value: Value.
        :type value: object
        """

        current_value = getattr(self, attribute, None)

        Attribute.__setattr__(self, attribute, value)

        if not attribute in ("_Attribute__name",
                             "_Attribute__value",
                             "_Attribute__roles",
                             "_Attribute__flags"):
            return

        trigger_model = getattr(self, "_Mixin_GraphModelObject__trigger_model", False)
        if trigger_model and value is not current_value:
            self.attribute_changed()

    __setitem__ = __setattr__

    def attribute_changed(self):
        """
        Triggers the host model(s) :meth:`umbra.ui.models.GraphModel.attribute_changed` method.

        :return: Method success.
        :rtype: bool
        """

        for model in umbra.ui.models.GraphModel.find_model(self):
            headers = model.horizontal_headers.values()
            if not self.name in headers:
                continue

            model.attribute_changed(model.find_node(self), headers.index(self.name))
        return True


class GraphModelNode(AbstractCompositeNode, Mixin_GraphModelObject):
    """
    Defines :class:`GraphModel` class base Node object.
    """

    __family = "GraphModel"
    """
    :param __family: Node family.
    :type __family: unicode
    """

    def __init__(self, name=None, parent=None, children=None, roles=None, flags=None, **kwargs):
        """
        Initializes the class.

        :param name: Node name.
        :type name: unicode
        :param parent: Node parent.
        :type parent: AbstractNode or AbstractCompositeNode
        :param children: Children.
        :type children: list
        :param roles: Roles.
        :type roles: dict
        :param flags: Flags. ( Qt.ItemFlag )
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        AbstractCompositeNode.__init__(self, name, parent, children, **kwargs)
        Mixin_GraphModelObject.__init__(self)

        # --- Setting class attributes. ---
        self.roles = roles or {Qt.DisplayRole: self.name, Qt.EditRole: self.name}
        self.flags = flags or int(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)

    def __setattr__(self, attribute, value):
        """
        Reimplements the :meth:`foundations.nodes.AbstractCompositeNode.__setattr__` method.

        :param attribute.: Attribute.
        :type attribute.: object
        :param value.: Value.
        :type value.: object
        """

        current_value = getattr(self, attribute, None)

        AbstractCompositeNode.__setattr__(self, attribute, value)

        if not attribute in ("_GraphModelNode__name",
                             "_GraphModelNode__roles",
                             "_GraphModelNode__flags"):
            return

        trigger_model = getattr(self, "_Mixin_GraphModelObject__trigger_model", False)
        if trigger_model and value is not current_value:
            self.node_changed()

    __setitem__ = __setattr__

    def node_changed(self):
        """
        Triggers the host model(s) :meth:`umbra.ui.models.GraphModel.node_changed` method.

        :return: Method success.
        :rtype: bool
        """

        for model in umbra.ui.models.GraphModel.find_model(self):
            model.node_changed(self)
        return True


class DefaultNode(AbstractCompositeNode):
    """
    | Defines the default Node used in :class:`GraphModel` class model.
    | This simple Node is used as an invisible root Node for :class:`GraphModel` class models.
    """

    __family = "Default"
    """
    :param __family: Node family.
    :type __family: unicode
    """

    def __init__(self, name=None, parent=None, children=None, **kwargs):
        """
        Initializes the class.

        :param name: Node name.
        :type name: unicode
        :param parent: Node parent.
        :type parent: AbstractCompositeNode
        :param children: Children.
        :type children: list
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        AbstractCompositeNode.__init__(self, name, parent, children, **kwargs)


class FormatNode(AbstractCompositeNode):
    """
    Defines the format base Node object.
    """

    __family = "Format"
    """
    :param __family: Node family.
    :type __family: unicode
    """

    def __init__(self, name=None, parent=None, children=None, format=None, **kwargs):
        """
        Initializes the class.

        :param name: Node name.
        :type name: unicode
        :param parent: Node parent.
        :type parent: AbstractNode or AbstractCompositeNode
        :param children: Children.
        :type children: list
        :param format: Format.
        :type format: object
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        AbstractCompositeNode.__init__(self, name, parent, children, **kwargs)

        # --- Setting class attributes. ---
        self.__format = None
        self.format = format

    @property
    def format(self):
        """
        Property for **self.__format** attribute.

        :return: self.__format.
        :rtype: object
        """

        return self.__format

    @format.setter
    def format(self, value):
        """
        Setter for **self.__format** attribute.

        :param value: Attribute value.
        :type value: object
        """

        self.__format = value

    @format.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def format(self):
        """
        Deleter for **self.__format** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "format"))
