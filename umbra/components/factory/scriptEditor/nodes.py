#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**nodes.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor`
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
import os
from PyQt4.QtCore import Qt

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import umbra.ui.nodes
from umbra.components.factory.scriptEditor.editor import Editor

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
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

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class EditorNode(umbra.ui.nodes.GraphModelNode):
	"""
	This class factory defines :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class **Editor** node.
	"""

	__family = "Editor"

	def __init__(self,
				editor=None,
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

		# --- Setting class attributes. ---
		self.__editor = None
		self.editor = editor

		EditorNode.__initializeNode(self, attributesFlags)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def editor(self):
		"""
		This method is the property for **self.__editor** attribute.

		:return: self.__editor. ( Editor )
		"""

		return self.__editor

	@editor.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def editor(self, value):
		"""
		This method is the setter method for **self.__editor** attribute.

		:param value: Attribute value. ( Editor )
		"""

		if value is not None:
			assert type(value) is Editor, "'{0}' attribute: '{1}' type is not 'Editor'!".format("editor", value)
		self.__editor = value

	@editor.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def editor(self):
		"""
		This method is the deleter method for **self.__editor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "editor"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self, attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		This method initializes the node.
		
		:param attributesFlags: Attributes flags. ( Integer )
		"""

		pass

class FileNode(umbra.ui.nodes.GraphModelNode):
	"""
	This class factory defines :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class **File** node.
	"""

	__family = "File"

	def __init__(self,
				path=None,
				name=None,
				parent=None,
				roles=None,
				nodeFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				**kwargs):
		"""
		This method initializes the class.

		:param path: File path.  ( String )
		:param name: Node name.  ( String )
		:param parent: Node parent. ( GraphModelNode )
		:param roles: Roles. ( Dictionary )
		:param nodeFlags: Node flags. ( Integer )
		:param attributesFlags: Attributes flags. ( Integer )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.nodes.GraphModelNode.__init__(self, name, parent, None, roles, nodeFlags, **kwargs)

		# --- Setting class attributes. ---
		self.__path = None
		self.path = path

		FileNode.__initializeNode(self, attributesFlags)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def path(self):
		"""
		This method is the property for **self.__path** attribute.

		:return: self.__path. ( String )
		"""

		return self.__path

	@path.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def path(self, value):
		"""
		This method is the setter method for **self.__path** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format("path", value)
		self.__path = value

	@path.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def path(self):
		"""
		This method is the deleter method for **self.__path** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "path"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self, attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		This method initializes the node.
		
		:param attributesFlags: Attributes flags. ( Integer )
		"""

		pass

class DirectoryNode(umbra.ui.nodes.GraphModelNode):
	"""
	This class factory defines :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class **Directory** node.
	"""

	__family = "Directory"

	def __init__(self,
				path=None,
				name=None,
				parent=None,
				children=None,
				roles=None,
				nodeFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				**kwargs):
		"""
		This method initializes the class.

		:param path: Directory path.  ( String )
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
		self.__path = None
		self.path = path

		DirectoryNode.__initializeNode(self, attributesFlags)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def path(self):
		"""
		This method is the property for **self.__path** attribute.

		:return: self.__path. ( String )
		"""

		return self.__path

	@path.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def path(self, value):
		"""
		This method is the setter method for **self.__path** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format("path", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' path doesn't exists!".format("source", value)
		self.__path = value

	@path.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def path(self):
		"""
		This method is the deleter method for **self.__path** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "path"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self, attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		This method initializes the node.
		
		:param attributesFlags: Attributes flags. ( Integer )
		"""

		pass

class ProjectNode(umbra.ui.nodes.GraphModelNode):
	"""
	This class factory defines :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class **Project** node.
	"""

	__family = "Project"

	def __init__(self,
				path=None,
				name=None,
				parent=None,
				children=None,
				roles=None,
				nodeFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled),
				**kwargs):
		"""
		This method initializes the class.

		:param path: Project path.  ( String )
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
		self.__path = None
		self.path = path

		ProjectNode.__initializeNode(self, attributesFlags)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def path(self):
		"""
		This method is the property for **self.__path** attribute.

		:return: self.__path. ( String )
		"""

		return self.__path

	@path.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def path(self, value):
		"""
		This method is the setter method for **self.__path** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) is unicode, "'{0}' attribute: '{1}' type is not 'unicode'!".format("path", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' path doesn't exists!".format("source", value)
		self.__path = value

	@path.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def path(self):
		"""
		This method is the deleter method for **self.__path** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "path"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self, attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		This method initializes the node.
		
		:param attributesFlags: Attributes flags. ( Integer )
		"""

		pass

class PatternNode(umbra.ui.nodes.GraphModelNode):
	"""
	This class factory defines :class:`umbra.patterns.factory.scriptEditor.searchAndReplace.SearchAndReplace` class
	search and replace pattern node.
	"""

	__family = "Pattern"
	"""Node family. ( String )"""

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

		PatternNode.__initializeNode(self, attributesFlags)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self, attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		This method initializes the node.
		
		:param attributesFlags: Attributes flags. ( Integer )
		"""

		pass

class SearchFileNode(umbra.ui.nodes.GraphModelNode):
	"""
	This class factory defines :class:`umbra.patterns.factory.scriptEditor.searchInFiles.SearchInFiles` class
	search file node.
	"""

	__family = "SearchFile"
	"""Node family. ( String )"""

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

		SearchFileNode.__initializeNode(self, attributesFlags)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self, attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		This method initializes the node.
		
		:param attributesFlags: Attributes flags. ( Integer )
		"""

		pass

class SearchOccurenceNode(umbra.ui.nodes.GraphModelNode):
	"""
	This class factory defines :class:`umbra.patterns.factory.scriptEditor.searchInFiles.SearchInFiles` class
	search occurence node.
	"""

	__family = "SearchOccurence"
	"""Node family. ( String )"""

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

		SearchOccurenceNode.__initializeNode(self, attributesFlags)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self, attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		This method initializes the node.
		
		:param attributesFlags: Attributes flags. ( Integer )
		"""

		pass

class ReplaceResultNode(umbra.ui.nodes.GraphModelNode):
	"""
	This class factory defines :class:`umbra.patterns.factory.scriptEditor.searchInFiles.SearchInFiles` class
	replace result node.
	"""

	__family = "ReplaceResult"
	"""Node family. ( String )"""

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

		ReplaceResultNode.__initializeNode(self, attributesFlags)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeNode(self, attributesFlags=int(Qt.ItemIsSelectable | Qt.ItemIsEnabled)):
		"""
		This method initializes the node.
		
		:param attributesFlags: Attributes flags. ( Integer )
		"""

		pass
