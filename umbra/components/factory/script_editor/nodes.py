#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`umbra.components.factory.script_editor.script_editor.ScriptEditor`
    Component Interface class nodes.

**Others:**

"""

from __future__ import unicode_literals

import os
from PyQt4.QtCore import Qt

import foundations.exceptions
import foundations.verbose
import umbra.ui.nodes
from umbra.components.factory.script_editor.editor import Editor

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
           "EditorNode",
           "FileNode",
           "DirectoryNode",
           "ProjectNode",
           "PatternNode",
           "SearchFileNode",
           "SearchOccurenceNode",
           "ReplaceResultNode"]

LOGGER = foundations.verbose.install_logger()


class EditorNode(umbra.ui.nodes.GraphModelNode):
    """
    Defines :class:`umbra.components.factory.script_editor.script_editor.ScriptEditor`
    Component Interface class **Editor** node.
    """

    __family = "Editor"

    def __init__(self,
                 editor=None,
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

        # --- Setting class attributes. ---
        self.__editor = None
        self.editor = editor

        EditorNode.__initialize_node(self, attributes_flags)

    @property
    def editor(self):
        """
        Property for **self.__editor** attribute.

        :return: self.__editor.
        :rtype: Editor
        """

        return self.__editor

    @editor.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def editor(self, value):
        """
        Setter for **self.__editor** attribute.

        :param value: Attribute value.
        :type value: Editor
        """

        if value is not None:
            assert type(value) is Editor, "'{0}' attribute: '{1}' type is not 'Editor'!".format("editor", value)
        self.__editor = value

    @editor.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def editor(self):
        """
        Deleter for **self.__editor** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "editor"))

    def __initialize_node(self, attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
        """
        Initializes the node.

        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        """

        pass


class FileNode(umbra.ui.nodes.GraphModelNode):
    """
    Defines :class:`umbra.components.factory.script_editor.script_editor.ScriptEditor`
    Component Interface class **File** node.
    """

    __family = "File"

    def __init__(self,
                 path=None,
                 name=None,
                 parent=None,
                 roles=None,
                 node_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
                 attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
                 **kwargs):
        """
        Initializes the class.

        :param path: File path.
        :type path: unicode
        :param name: Node name.
        :type name: unicode
        :param parent: Node parent.
        :type parent: GraphModelNode
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

        umbra.ui.nodes.GraphModelNode.__init__(self, name, parent, None, roles, node_flags, **kwargs)

        # --- Setting class attributes. ---
        self.__path = None
        self.path = path

        FileNode.__initialize_node(self, attributes_flags)

    @property
    def path(self):
        """
        Property for **self.__path** attribute.

        :return: self.__path.
        :rtype: unicode
        """

        return self.__path

    @path.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def path(self, value):
        """
        Setter for **self.__path** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format("path", value)
        self.__path = value

    @path.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def path(self):
        """
        Deleter for **self.__path** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "path"))

    def __initialize_node(self, attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
        """
        Initializes the node.

        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        """

        pass


class DirectoryNode(umbra.ui.nodes.GraphModelNode):
    """
    Defines :class:`umbra.components.factory.script_editor.script_editor.ScriptEditor`
    Component Interface class **Directory** node.
    """

    __family = "Directory"

    def __init__(self,
                 path=None,
                 name=None,
                 parent=None,
                 children=None,
                 roles=None,
                 node_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
                 attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
                 **kwargs):
        """
        Initializes the class.

        :param path: Directory path.
        :type path: unicode
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
        self.__path = None
        self.path = path

        DirectoryNode.__initialize_node(self, attributes_flags)

    @property
    def path(self):
        """
        Property for **self.__path** attribute.

        :return: self.__path.
        :rtype: unicode
        """

        return self.__path

    @path.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def path(self, value):
        """
        Setter for **self.__path** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format("path", value)
            assert os.path.exists(value), "'{0}' attribute: '{1}' path doesn't exists!".format("source", value)
        self.__path = value

    @path.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def path(self):
        """
        Deleter for **self.__path** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "path"))

    def __initialize_node(self, attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
        """
        Initializes the node.

        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        """

        pass


class ProjectNode(umbra.ui.nodes.GraphModelNode):
    """
    Defines :class:`umbra.components.factory.script_editor.script_editor.ScriptEditor`
    Component Interface class **Project** node.
    """

    __family = "Project"

    def __init__(self,
                 path=None,
                 name=None,
                 parent=None,
                 children=None,
                 roles=None,
                 node_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
                 attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
                 **kwargs):
        """
        Initializes the class.

        :param path: Project path.
        :type path: unicode
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
        self.__path = None
        self.path = path

        ProjectNode.__initialize_node(self, attributes_flags)

    @property
    def path(self):
        """
        Property for **self.__path** attribute.

        :return: self.__path.
        :rtype: unicode
        """

        return self.__path

    @path.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def path(self, value):
        """
        Setter for **self.__path** attribute.

        :param value: Attribute value.
        :type value: unicode
        """

        if value is not None:
            assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format("path", value)
            assert os.path.exists(value), "'{0}' attribute: '{1}' path doesn't exists!".format("source", value)
        self.__path = value

    @path.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def path(self):
        """
        Deleter for **self.__path** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "path"))

    def __initialize_node(self, attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
        """
        Initializes the node.

        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        """

        pass


class PatternNode(umbra.ui.nodes.GraphModelNode):
    """
    Defines :class:`umbra.patterns.factory.script_editor.search_and_replace.SearchAndReplace` class
    search and replace pattern node.
    """

    __family = "Pattern"
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

        PatternNode.__initialize_node(self, attributes_flags)

    def __initialize_node(self, attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
        """
        Initializes the node.

        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        """

        pass


class SearchFileNode(umbra.ui.nodes.GraphModelNode):
    """
    Defines :class:`umbra.patterns.factory.script_editor.search_in_files.SearchInFiles` class
    search file node.
    """

    __family = "SearchFile"
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

        SearchFileNode.__initialize_node(self, attributes_flags)

    def __initialize_node(self, attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
        """
        Initializes the node.

        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        """

        pass


class SearchOccurenceNode(umbra.ui.nodes.GraphModelNode):
    """
    Defines :class:`umbra.patterns.factory.script_editor.search_in_files.SearchInFiles` class
    search occurence node.
    """

    __family = "SearchOccurence"
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

        SearchOccurenceNode.__initialize_node(self, attributes_flags)

    def __initialize_node(self, attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
        """
        Initializes the node.

        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        """

        pass


class ReplaceResultNode(umbra.ui.nodes.GraphModelNode):
    """
    Defines :class:`umbra.patterns.factory.script_editor.search_in_files.SearchInFiles` class
    replace result node.
    """

    __family = "ReplaceResult"
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

        ReplaceResultNode.__initialize_node(self, attributes_flags)

    def __initialize_node(self, attributes_flags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
        """
        Initializes the node.

        :param attributes_flags: Attributes flags.
        :type attributes_flags: int
        """

        pass
