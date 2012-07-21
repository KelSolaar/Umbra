#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`umbra.languages.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class Models.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import os
import re
from PyQt4.QtCore import QAbstractListModel
from PyQt4.QtCore import QModelIndex
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import foundations.walkers
import umbra.ui.models
from umbra.components.factory.scriptEditor.editor import Editor
from umbra.components.factory.scriptEditor.editor import Language
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

__all__ = ["LOGGER",
			"ProjectNode",
			"EditorNode",
			"FileNode",
			"DirectoryNode",
			"ProjectsModel",
			"LanguagesModel",
			"PatternNode",
			"PatternsModel",
			"SearchFileNode",
			"SearchOccurenceNode",
			"ReplaceResultNode",
			"SearchResultsModel"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class EditorNode(umbra.ui.models.GraphModelNode):
	"""
	This class factory defines :class:`umbra.languages.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class **Editor* node.
	"""

	__family = "EditorNode"

	@core.executionTrace
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

		umbra.ui.models.GraphModelNode.__init__(self, name, parent, children, roles, nodeFlags, **kwargs)

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
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def editor(self, value):
		"""
		This method is the setter method for **self.__editor** attribute.

		:param value: Attribute value. ( Editor )
		"""

		if value is not None:
			assert type(value) is Editor, "'{0}' attribute: '{1}' type is not 'Editor'!".format("editor", value)
		self.__editor = value

	@editor.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def editor(self):
		"""
		This method is the deleter method for **self.__editor** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "editor"))

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

class FileNode(umbra.ui.models.GraphModelNode):
	"""
	This class factory defines :class:`umbra.languages.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class **File* node.
	"""

	__family = "FileNode"

	@core.executionTrace
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
		:param editor: File editor.  ( Editor )
		:param name: Node name.  ( String )
		:param parent: Node parent. ( GraphModelNode )
		:param roles: Roles. ( Dictionary )
		:param nodeFlags: Node flags. ( Integer )
		:param attributesFlags: Attributes flags. ( Integer )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModelNode.__init__(self, name, parent, None, roles, nodeFlags, **kwargs)

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
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def path(self, value):
		"""
		This method is the setter method for **self.__path** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("path", value)
		self.__path = value

	@path.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def path(self):
		"""
		This method is the deleter method for **self.__path** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "path"))

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

class DirectoryNode(umbra.ui.models.GraphModelNode):
	"""
	This class factory defines :class:`umbra.languages.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class **Directory* node.
	"""

	__family = "DirectoryNode"

	@core.executionTrace
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

		umbra.ui.models.GraphModelNode.__init__(self, name, parent, children, roles, nodeFlags, **kwargs)

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
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def path(self, value):
		"""
		This method is the setter method for **self.__path** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("path", value)
			assert os.path.exists(value), "'{0}' attribute: '{1}' path doesn't exists!".format("source", value)
		self.__path = value

	@path.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def path(self):
		"""
		This method is the deleter method for **self.__path** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "path"))

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

class ProjectNode(umbra.ui.models.GraphModelNode):
	"""
	This class factory defines :class:`umbra.languages.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class **Project* node.
	"""

	__family = "ProjectNode"

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

		umbra.ui.models.GraphModelNode.__init__(self, name, parent, children, roles, nodeFlags, **kwargs)

		ProjectNode.__initializeNode(self, attributesFlags)

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

class ProjectsModel(umbra.ui.models.GraphModel):
	"""
	This class defines the Model used by :class:`umbra.languages.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class. 
	"""

	fileRegistered = pyqtSignal(str)
	"""
	This signal is emited by the :class:`ProjectsModel` class when a file is registered. ( pyqtSignal )

	:return: Registered file. ( String )	
	"""

	fileUnregistered = pyqtSignal(str)
	"""
	This signal is emited by the :class:`ProjectsModel` class when a file is runegistered. ( pyqtSignal )

	:return: Unregistered file. ( String )	
	"""

	editorRegistered = pyqtSignal(Editor)
	"""
	This signal is emited by the :class:`ProjectsModel` class when an editor is registered. ( pyqtSignal )

	:return: Registered editor. ( Editor )	
	"""

	editorUnregistered = pyqtSignal(Editor)
	"""
	This signal is emited by the :class:`ProjectsModel` class when an editor is runegistered. ( pyqtSignal )

	:return: Unregistered editor. ( Editor )	
	"""

	@core.executionTrace
	def __init__(self,
				parent=None,
				rootNode=None,
				horizontalHeaders=None,
				verticalHeaders=None,
				defaultNode=None,
				defaultProject=None):
		"""
		This method initializes the class.

		:param defaultProject: Default project name. ( String )
		:param parent: Object parent. ( QObject )
		:param rootNode: Root node. ( AbstractCompositeNode )
		:param horizontalHeaders: Headers. ( OrderedDict )
		:param verticalHeaders: Headers. ( OrderedDict )
		:param defaultNode: Default node. ( AbstractCompositeNode )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModel.__init__(self, parent, rootNode, horizontalHeaders, verticalHeaders, defaultNode)

		# --- Setting class attributes. ---
		self.__defaultProject = None
		self.defaultProject = defaultProject or "defaultProject"

		ProjectsModel.__initializeModel(self)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def defaultProject(self):
		"""
		This method is the property for **self.__defaultProject** attribute.

		:return: self.__defaultProject. ( String )
		"""

		return self.__defaultProject

	@defaultProject.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def defaultProject(self, value):
		"""
		This method is the setter method for **self.__defaultProject** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) in (str, unicode), \
			 "'{0}' attribute: '{1}' type is not 'str' or 'unicode'!".format("defaultProject", value)
		self.__defaultProject = value

	@defaultProject.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def defaultProject(self):
		"""
		This method is the deleter method for **self.__defaultProject** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultProject"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def __initializeModel(self):
		"""
		This method initializes the Model.
		"""

		LOGGER.debug("> Initializing model.")

		self.beginResetModel()
		self.rootNode = umbra.ui.models.DefaultNode(name="InvisibleRootNode")
		defaultProjectNode = ProjectNode(name=self.__defaultProject,
								parent=self.rootNode,
								nodeFlags=int(Qt.ItemIsEnabled),
								attributesFlags=int(Qt.ItemIsEnabled))
		self.endResetModel()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listEditorNodes(self):
		"""
		This method returns the Model :class:`EditorNode` nodes.
		
		:return: EditorNode nodes. ( List )
		"""

		return self.listFamily("EditorNode")

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listFileNodes(self):
		"""
		This method returns the Model :class:`FileNode` nodes.
		
		:return: FileNode nodes. ( List )
		"""

		return self.listFamily("FileNode")

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listDirectoryNodes(self):
		"""
		This method returns the Model :class:`DirectoryNode` nodes.
		
		:return: DirectoryNode nodes. ( List )
		"""

		return self.listFamily("DirectoryNode")

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listProjectNodes(self):
		"""
		This method returns the Model :class:`ProjectNode` nodes.
		
		:return: ProjectNode nodes. ( List )
		"""

		return self.listFamily("ProjectNode")

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listEditors(self):
		"""
		This method returns the Model editors.
		
		:return: Editors. ( List )
		"""

		return [editorNode.editor for editorNode in self.listFamily("EditorNode") if editorNode.editor]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listFiles(self):
		"""
		This method returns the Model files.
		
		:return: FileNode nodes. ( List )
		"""

		return [fileNode.path for fileNode in self.listFamily("FileNode") if fileNode.path]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listDirectories(self):
		"""
		This method returns the Model directories.
		
		:return: DirectoryNode nodes. ( List )
		"""

		return [directoryNode.path for directoryNode in self.listFamily("DirectoryNode") if directoryNode.path]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listProjects(self):
		"""
		This method returns the Model projects.
		
		:return: ProjectNode nodes. ( List )
		"""

		return [projectNode.name for projectNode in self.listFamily("ProjectNode") if projectNode.name]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getEditorNode(self, editor):
		"""
		This method returns the :class:`EditorNode` node with given editor.
		
		:param editor: Editor. ( Editor )
		:return: EditorNode node. ( EditorNode )
		"""

		for editorNode in self.listEditorNodes():
			if editorNode.editor == editor:
				return editorNode

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getFileNode(self, path):
		"""
		This method returns the :class:`FileNode` node with given path.
		
		:param path: File path. ( String )
		:return: FileNode node. ( FileNode )
		"""

		for fileNode in self.listFileNodes():
			if fileNode.path == path:
				return fileNode

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getDirectoryNode(self, path):
		"""
		This method returns the :class:`DirectoryNode` node with given path.
		
		:param path: Directory path. ( String )
		:return: DirectoryNode node. ( DirectoryNode )
		"""

		for directoryNode in self.listDirectoryNodes():
			if directoryNode.path == path:
				return directoryNode

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getProjectNode(self, name):
		"""
		This method returns the :class:`ProjectNode` node with given name.
		
		:param name: Project path. ( String )
		:return: ProjectNode node. ( ProjectNode )
		"""

		for projectNode in self.listProjectNodes():
			if projectNode.name == name:
				return projectNode

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getEditor(self, file):
		"""
		This method returns the Model editor associated with given file.

		:param file: File to search editors for. ( String )
		:return: Editor. ( Editor )
		"""

		for editor in self.listEditors():
			if editor.file == file:
				return editor

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def registerFile(self, file, parent):
		"""
		This method registers given file in the Model.
		
		:param file: File to register. ( String )
		:param parent: FileNode parent. ( GraphModelNode )
		:return: FileNode. ( FileNode )
		"""

		if self.getFileNode(file):
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' file is already registered!".format(
			self.__class__.__name__, file))

		LOGGER.debug("> Registering '{0}' file.".format(file))

		row = parent.childrenCount()
		self.beginInsertRows(self.getNodeIndex(parent), row, row + 1)
		fileNode = FileNode(file, parent=parent)
		self.endInsertRows()

		self.fileRegistered.emit(file)

		return fileNode

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def unregisterFile(self, file, raiseException=True):
		"""
		This method unregisters given file from the Model.
		
		:param file: File to unregister. ( String )
		:param raiseException: Raise the exception. ( Boolean )
		:return: FileNode. ( FileNode )
		"""

		fileNode = self.getFileNode(file)
		if not fileNode:
			if not raiseException:
				return

			raise foundations.exceptions.ProgrammingError("{0} | '{1}' file isn't registered!".format(
			self.__class__.__name__, file))

		LOGGER.debug("> Unregistering '{0}' file.".format(file))

		parent = fileNode.parent
		row = fileNode.row()
		self.beginRemoveRows(self.getNodeIndex(parent), row, row + 1)
		parent.removeChild(row)
		self.endRemoveRows()

		self.fileUnregistered.emit(file)

		return fileNode

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def registerEditor(self, editor, parent):
		"""
		This method registers given :class:`umbra.components.factory.scriptEditor.editor.Editor` class in the Model.
		
		:param editor: Editor to register. ( Editor )
		:param parent: EditorNode parent. ( GraphModelNode )
		:return: EditorNode. ( EditorNode )
		"""

		if self.getEditorNode(editor):
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' editor is already registered!".format(
			self.__class__.__name__, editor))

		LOGGER.debug("> Registering '{0}' editor.".format(editor))

		row = parent.childrenCount()
		self.beginInsertRows(self.getNodeIndex(parent), row, row + 1)
		editorNode = EditorNode(editor, parent=parent)
		self.endInsertRows()

		self.editorRegistered.emit(editor)

		return editorNode

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def unregisterEditor(self, editor, raiseException=True):
		"""
		This method unregisters given :class:`umbra.components.factory.scriptEditor.editor.Editor` class from the Model.
		
		:param editor: Editor to unregister. ( String )
		:param raiseException: Raise the exception. ( Boolean )
		:return: EditorNode. ( EditorNode )
		"""

		editorNode = self.getEditorNode(editor)
		if not editorNode:
			if not raiseException:
				return

			raise foundations.exceptions.ProgrammingError("{0} | '{1}' editor isn't registered!".format(
			self.__class__.__name__, editor))

		LOGGER.debug("> Unregistering '{0}' editor.".format(editor))

		parent = editorNode.parent
		row = editorNode.row()
		self.beginRemoveRows(self.getNodeIndex(parent), row, row + 1)
		parent.removeChild(row)
		self.endRemoveRows()

		self.editorUnregistered.emit(editor)

		return editorNode

class LanguagesModel(QAbstractListModel):
	"""
	This class is a `QAbstractListModel <http://doc.qt.nokia.com/qabstractListmodel.html>`_ subclass used
	to store the :class:`umbra.languages.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class languages.
	"""

	@core.executionTrace
	def __init__(self, parent=None, languages=None):
		"""
		This method initializes the class.

		:param parent: Parent object. ( QObject )
		:param languages: Languages. ( List )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QAbstractListModel.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__languages = []
		self.languages = languages

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def languages(self):
		"""
		This method is the property for **self.__languages** attribute.

		:return: self.__languages. ( List )
		"""

		return self.__languages

	@languages.setter
	@foundations.exceptions.exceptionsHandler(None, False, AssertionError)
	def languages(self, value):
		"""
		This method is the setter method for **self.__languages** attribute.

		:param value: Attribute value. ( List )
		"""

		if value is not None:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("languages", value)
			for element in value:
				assert type(element) is Language, "'{0}' attribute: '{1}' type is not 'Language'!".format("languages", element)
		self.beginResetModel()
		self.__languages = value
		self.endResetModel()

	@languages.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def languages(self):
		"""
		This method is the deleter method for **self.__languages** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "languages"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
	def rowCount(self, parent=QModelIndex()):
		"""
		This method reimplements the :meth:`QAbstractListModel.rowCount` method.

		:param parent: Parent. ( QModelIndex )
		:return: Row count. ( Integer )
		"""

		return len(self.__languages)

	# @core.executionTrace
	# @foundations.exceptions.exceptionsHandler(None, False, Exception)
	def data(self, index, role=Qt.DisplayRole):
		"""
		This method reimplements the :meth:`QAbstractListModel.data` method.

		:param index: Index. ( QModelIndex )
		:param role: Role. ( Integer )
		:return: Data. ( QVariant )
		"""

		if not index.isValid():
			return QVariant()

		if role == Qt.DisplayRole:
			return QVariant(self.__languages[index.row()].name)
		return QVariant()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def sortLanguages(self, order=Qt.AscendingOrder):
		"""
		This method sorts the Model languages.
		
		:param order: Order. ( Qt.SortOrder )
		"""

		self.beginResetModel()
		self.__languages = sorted(self.__languages, key=lambda x: (x.name), reverse=order)
		self.endResetModel()

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def registerLanguage(self, language):
		"""
		This method registers given language in the :obj:`LanguagesModel.languages` class property.
		
		:param language: Language to register. ( Language )
		:return: Method success. ( Boolean )
		"""

		if self.getLanguage(language):
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' language is already registered!".format(
			self.__class__.__name__, language.name))

		LOGGER.debug("> Registering '{0}' language.".format(language.name))

		self.__languages.append(language)
		self.sortLanguages()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def unregisterLanguage(self, name):
		"""
		This method unregisters language with given name from the :obj:`LanguagesModel.languages` class property.
		
		:param name: Language to unregister. ( String )
		:return: Method success. ( Boolean )
		"""

		if not self.getLanguage(name):
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' language isn't registered!".format(
			self.__class__.__name__, name))

		LOGGER.debug("> Unregistering '{0}' language.".format(name))

		for i, language in enumerate(self.__languages):
			if not language.name == name:
				continue

			del(self.__languages[i])
			self.sortLanguages()
			return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getLanguage(self, name):
		"""
		This method returns the language with given name.
		
		:param name: Language name. ( String )
		:return: File language. ( Language )
		"""

		for language in self.__languages:
			if language.name == name:
				LOGGER.debug("> Language '{0}': '{1}'.".format(name, language))
				return language

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getFileLanguage(self, file):
		"""
		This method returns the language of given file.
		
		:param file: File to get language of. ( String )
		:return: File language. ( Language )
		"""

		for language in self.__languages:
			if re.search(language.extensions, file):
				LOGGER.debug("> '{0}' file detected language: '{1}'.".format(file, language.name))
				return language

class PatternNode(umbra.ui.models.GraphModelNode):
	"""
	This class factory defines :class:`umbra.patterns.factory.scriptEditor.searchAndReplace.SearchAndReplace` class
	search and replace pattern node.
	"""

	__family = "Pattern"
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

		umbra.ui.models.GraphModelNode.__init__(self, name, parent, children, roles, nodeFlags, **kwargs)

		PatternNode.__initializeNode(self, attributesFlags)

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

class PatternsModel(umbra.ui.models.GraphModel):
	"""
	This class defines the Model used the by
	:class:`umbra.patterns.factory.scriptEditor.searchAndReplace.SearchAndReplace` class to store the search and \
	replace patterns.
	"""

	# Custom signals definitions.
	patternInserted = pyqtSignal(QModelIndex)
	"""
	This signal is emited by the :class:`PatternsModel` class when a pattern has been inserted. ( pyqtSignal )

	:return: Inserted pattern index. ( QModelIndex )
	"""

	# Custom signals definitions.
	patternRemoved = pyqtSignal(QModelIndex)
	"""
	This signal is emited by the :class:`PatternsModel` class when a pattern has been removed. ( pyqtSignal )

	:return: Removed pattern index. ( QModelIndex )
	"""

	@core.executionTrace
	def __init__(self, parent=None, rootNode=None, horizontalHeaders=None, verticalHeaders=None, defaultNode=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param rootNode: Root node. ( AbstractCompositeNode )
		:param horizontalHeaders: Headers. ( OrderedDict )
		:param verticalHeaders: Headers. ( OrderedDict )
		:param defaultNode: Default node. ( AbstractCompositeNode )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModel.__init__(self, parent, rootNode, horizontalHeaders, verticalHeaders, defaultNode)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def insertPattern(self, pattern, index):
		"""
		This method inserts given pattern into the Model.

		:param pattern: Pattern. ( String )
		:param index: Insertion index. ( Integer )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Inserting '{0}' at '{1}' index.".format(pattern, index))

		self.removePattern(pattern)

		self.beginInsertRows(self.getNodeIndex(self.rootNode), index, index)
		self.rootNode.insertChild(PatternNode(name=pattern), index)
		self.endInsertRows()
		self.patternInserted.emit(self.getNodeIndex(self.rootNode.children[index]))
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def removePattern(self, pattern):
		"""
		This method removes given pattern from the Model.

		:param pattern: Pattern. ( String )
		:return: Method success. ( Boolean )
		"""

		for index, node in enumerate(self.rootNode.children):
			if node.name != pattern:
				continue

			LOGGER.debug("> Removing '{0}' at '{1}' index.".format(pattern, index))

			self.beginRemoveRows(self.getNodeIndex(self.rootNode), index, index)
			self.rootNode.removeChild(index)
			self.endRemoveRows()
			self.patternRemoved.emit(self.getNodeIndex(self.rootNode.children[index]))
			return True

class SearchFileNode(umbra.ui.models.GraphModelNode):
	"""
	This class factory defines :class:`umbra.patterns.factory.scriptEditor.searchInFiles.SearchInFiles` class
	search file node.
	"""

	__family = "SearchFile"
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

		umbra.ui.models.GraphModelNode.__init__(self, name, parent, children, roles, nodeFlags, **kwargs)

		SearchFileNode.__initializeNode(self, attributesFlags)

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

class SearchOccurenceNode(umbra.ui.models.GraphModelNode):
	"""
	This class factory defines :class:`umbra.patterns.factory.scriptEditor.searchInFiles.SearchInFiles` class
	search occurence node.
	"""

	__family = "SearchOccurence"
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

		umbra.ui.models.GraphModelNode.__init__(self, name, parent, children, roles, nodeFlags, **kwargs)

		SearchOccurenceNode.__initializeNode(self, attributesFlags)

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

class ReplaceResultNode(umbra.ui.models.GraphModelNode):
	"""
	This class factory defines :class:`umbra.patterns.factory.scriptEditor.searchInFiles.SearchInFiles` class
	replace result node.
	"""

	__family = "ReplaceResult"
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

		umbra.ui.models.GraphModelNode.__init__(self, name, parent, children, roles, nodeFlags, **kwargs)

		ReplaceResultNode.__initializeNode(self, attributesFlags)

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

class SearchResultsModel(umbra.ui.models.GraphModel):
	"""
	This class defines the Model used the by
	:class:`umbra.patterns.factory.scriptEditor.searchInFiles.SearchInFiles` class to store the search results.
	"""

	@core.executionTrace
	def __init__(self, parent=None, rootNode=None, horizontalHeaders=None, verticalHeaders=None, defaultNode=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param rootNode: Root node. ( AbstractCompositeNode )
		:param horizontalHeaders: Headers. ( OrderedDict )
		:param verticalHeaders: Headers. ( OrderedDict )
		:param defaultNode: Default node. ( AbstractCompositeNode )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModel.__init__(self, parent, rootNode, horizontalHeaders, verticalHeaders, defaultNode)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def initializeModel(self, rootNode):
		"""
		This method initializes the Model using given root node.
		
		:param rootNode: Graph root node. ( DefaultNode )
		:return: Method success ( Boolean )
		"""

		LOGGER.debug("> Initializing model with '{0}' root node.".format(rootNode))

		self.beginResetModel()
		self.rootNode = rootNode
		self.endResetModel()
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def getMetrics(self):
		"""
		This method returns the Model metrics.
		
		:return: Nodes metrics. ( Dictionary )
		"""

		searchFileNodesCount = searchOccurenceNodesCount = 0

		for node in foundations.walkers.nodesWalker(self.rootNode):
			if node.family == "SearchFile":
				searchFileNodesCount += 1
			elif node.family == "SearchOccurence":
				searchOccurenceNodesCount += 1

		return {"SearchFile" : searchFileNodesCount, "SearchOccurence" : searchOccurenceNodesCount}
