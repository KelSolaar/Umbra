#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class Models.

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
import re
from PyQt4.QtCore import QAbstractListModel
from PyQt4.QtCore import QModelIndex
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import foundations.walkers
import umbra.ui.models
import umbra.ui.nodes
from umbra.components.factory.scriptEditor.nodes import ProjectNode
from umbra.components.factory.scriptEditor.nodes import DirectoryNode
from umbra.components.factory.scriptEditor.nodes import EditorNode
from umbra.components.factory.scriptEditor.nodes import FileNode
from umbra.components.factory.scriptEditor.nodes import PatternNode
from umbra.ui.languages import Language

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "ProjectsModel",
			"LanguagesModel",
			"PatternsModel",
			"SearchResultsModel"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ProjectsModel(umbra.ui.models.GraphModel):
	"""
	This class defines the Model used by :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class. 
	"""

	fileRegistered = pyqtSignal(FileNode)
	"""
	This signal is emited by the :class:`ProjectsModel` class when a file is registered. ( pyqtSignal )

	:return: Registered file FileNode. ( FileNode )	
	"""

	fileUnregistered = pyqtSignal(FileNode)
	"""
	This signal is emited by the :class:`ProjectsModel` class when a file is unregistered. ( pyqtSignal )

	:return: Unregistered file FileNode. ( FileNode )	
	"""

	editorRegistered = pyqtSignal(EditorNode)
	"""
	This signal is emited by the :class:`ProjectsModel` class when an editor is registered. ( pyqtSignal )

	:return: Registered editor EditorNode. ( EditorNode )	
	"""

	editorUnregistered = pyqtSignal(EditorNode)
	"""
	This signal is emited by the :class:`ProjectsModel` class when an editor is unregistered. ( pyqtSignal )

	:return: Unregistered editor EditorNode. ( EditorNode )	
	"""

	directoryRegistered = pyqtSignal(DirectoryNode)
	"""
	This signal is emited by the :class:`ProjectsModel` class when a directory is registered. ( pyqtSignal )

	:return: Registered directory DirectoryNode. ( DirectoryNode )	
	"""

	directoryUnregistered = pyqtSignal(DirectoryNode)
	"""
	This signal is emited by the :class:`ProjectsModel` class when a directory is unregistered. ( pyqtSignal )

	:return: Unregistered directory DirectoryNode. ( DirectoryNode )	
	"""

	projectRegistered = pyqtSignal(ProjectNode)
	"""
	This signal is emited by the :class:`ProjectsModel` class when a project is registered. ( pyqtSignal )

	:return: Registered project ProjectNode. ( ProjectNode )	
	"""

	projectUnregistered = pyqtSignal(ProjectNode)
	"""
	This signal is emited by the :class:`ProjectsModel` class when a project is unregistered. ( pyqtSignal )

	:return: Unregistered project ProjectNode. ( ProjectNode )	
	"""

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
		:param defaultNode: Default node. ( GraphModelNode )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModel.__init__(self, parent, rootNode, horizontalHeaders, verticalHeaders, defaultNode)

		# --- Setting class attributes. ---
		self.__defaultProject = None
		self.defaultProject = defaultProject or "defaultProject"

		self.__defaultProjectNode = None

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
	@foundations.exceptions.handleExceptions(AssertionError)
	def defaultProject(self, value):
		"""
		This method is the setter method for **self.__defaultProject** attribute.

		:param value: Attribute value. ( String )
		"""

		if value is not None:
			assert type(value) is unicode, \
			 "'{0}' attribute: '{1}' type is not 'unicode'!".format("defaultProject", value)
		self.__defaultProject = value

	@defaultProject.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultProject(self):
		"""
		This method is the deleter method for **self.__defaultProject** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultProject"))

	@property
	def defaultProjectNode(self):
		"""
		This method is the property for **self.__defaultProjectNode** attribute.

		:return: self.__defaultProjectNode. ( String )
		"""

		return self.__defaultProjectNode

	@defaultProjectNode.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultProjectNode(self, value):
		"""
		This method is the setter method for **self.__defaultProjectNode** attribute.

		:param value: Attribute value. ( String )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "defaultProjectNode"))

	@defaultProjectNode.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def defaultProjectNode(self):
		"""
		This method is the deleter method for **self.__defaultProjectNode** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "defaultProjectNode"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __initializeModel(self):
		"""
		This method initializes the Model.
		"""

		LOGGER.debug("> Initializing model.")

		self.beginResetModel()
		self.rootNode = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")
		self.__defaultProjectNode = ProjectNode(name=self.__defaultProject,
								parent=self.rootNode,
								nodeFlags=int(Qt.ItemIsEnabled),
								attributesFlags=int(Qt.ItemIsEnabled))
		self.enableModelTriggers(True)
		self.endResetModel()

	def listEditorNodes(self, node=None):
		"""
		This method returns the Model :class:`umbra.components.factory.scriptEditor.nodes.EditorNode` class nodes.
		
		:param node: Node to start walking from. ( AbstractNode / AbstractCompositeNode / Object )
		:return: EditorNode nodes. ( List )
		"""

		return self.findFamily("Editor", node=node or self.__defaultProjectNode)

	def listFileNodes(self, node=None):
		"""
		This method returns the Model :class:`umbra.components.factory.scriptEditor.nodes.FileNode` class nodes.
		
		:param node: Node to start walking from. ( AbstractNode / AbstractCompositeNode / Object )
		:return: FileNode nodes. ( List )
		"""

		return self.findFamily("File", node=node or self.__defaultProjectNode)

	def listDirectoryNodes(self):
		"""
		This method returns the Model :class:`umbra.components.factory.scriptEditor.nodes.DirectoryNode` class nodes.
		
		:return: DirectoryNode nodes. ( List )
		"""

		return self.findFamily("Directory")

	def listProjectNodes(self, ignoreDefaultProjectNode=True):
		"""
		This method returns the Model :class:`umbra.components.factory.scriptEditor.nodes.ProjectNode` class nodes.
		
		:param ignoreDefaultProjectNode: Default ProjectNode will be ignored. (  Boolean )
		:return: ProjectNode nodes. ( List )
		"""

		projectNodes = self.findFamily("Project")
		return filter(lambda x: x != self.__defaultProjectNode, projectNodes) \
		if ignoreDefaultProjectNode else projectNodes

	def listEditors(self, node=None):
		"""
		This method returns the Model editors.
		
		:param node: Node to start walking from. ( AbstractNode / AbstractCompositeNode / Object )
		:return: Editors. ( List )
		"""

		return [editorNode.editor for editorNode in self.listEditorNodes(node) 	if editorNode.editor]

	def listFiles(self, node=None):
		"""
		This method returns the Model files.
		
		:param node: Node to start walking from. ( AbstractNode / AbstractCompositeNode / Object )
		:return: FileNode nodes. ( List )
		"""

		return [fileNode.path for fileNode in self.listFileNodes(node) if fileNode.path]

	def listDirectories(self):
		"""
		This method returns the Model directories.
		
		:return: DirectoryNode nodes. ( List )
		"""

		return [directoryNode.path for directoryNode in self.listDirectoryNodes() if directoryNode.path]

	def listProjects(self, ignoreDefaultProjectNode=True):
		"""
		This method returns the Model projects.
		
		:param ignoreDefaultProjectNode: Default ProjectNode will be ignored. (  Boolean )
		:return: ProjectNode nodes. ( List )
		"""

		return [projectNode.path for projectNode in self.listProjectNodes(ignoreDefaultProjectNode) if projectNode.path]

	def getEditorNodes(self, editor, node=None):
		"""
		This method returns the :class:`umbra.components.factory.scriptEditor.nodes.EditorNode` class Nodes with given editor.
		
		:param node: Node to start walking from. ( AbstractNode / AbstractCompositeNode / Object )
		:param editor: Editor. ( Editor )
		:return: EditorNode nodes. ( List )
		"""

		return [editorNode for editorNode in self.listEditorNodes(node) if editorNode.editor == editor]

	def getFileNodes(self, path, node=None):
		"""
		This method returns the :class:`umbra.components.factory.scriptEditor.nodes.FileNode` class Nodes with given path.
		
		:param node: Node to start walking from. ( AbstractNode / AbstractCompositeNode / Object )
		:param path: File path. ( String )
		:return: FileNode nodes. ( List )
		"""

		return [fileNode for fileNode in self.listFileNodes(node) if fileNode.path == path]

	def getDirectoryNodes(self, path):
		"""
		This method returns the :class:`umbra.components.factory.scriptEditor.nodes.DirectoryNode` class Nodes with given path.
		
		:param path: Directory path. ( String )
		:return: DirectoryNode nodes. ( List )
		"""

		return [directoryNode for directoryNode in self.listDirectoryNodes() if directoryNode.path == path]

	def getProjectNodes(self, path):
		"""
		This method returns the :class:`umbra.components.factory.scriptEditor.nodes.ProjectNode` class Nodes with given path.
		
		:param path: Project path. ( String )
		:return: ProjectNode nodes. ( List )
		"""

		return [projectNode for projectNode in self.listProjectNodes() if projectNode.path == path]

	def moveNode(self, parent, fromIndex, toIndex):
		"""
		This method moves given parent child to given index.

		:param toIndex: Index to. ( Integer )
		:param fromIndex: Index from. ( Integer )
		:return: Method success. ( Boolean )
		"""

		# TODO: This method should be refactored once this ticket is fixed:
		# https://bugreports.qt-project.org/browse/PYSIDE-78
		if not fromIndex >= 0 or \
		not fromIndex < parent.childrenCount() or \
		not toIndex >= 0 or \
		not toIndex < parent.childrenCount():
			return False

		parentIndex = self.getNodeIndex(parent)
		self.beginRemoveRows(parentIndex, fromIndex, fromIndex)
		child = parent.removeChild(fromIndex)
		self.endRemoveRows()

		startIndex = parent.childrenCount() - 1
		endIndex = toIndex - 1

		tail = []
		for i in range(startIndex, endIndex, -1):
			self.beginRemoveRows(parentIndex, i, i)
			tail.append(parent.removeChild(i))
			self.endRemoveRows()
		tail = list(reversed(tail))
		tail.insert(0, child)

		for node in tail:
			row = parent.childrenCount()
			self.beginInsertRows(parentIndex, row, row)
			parent.addChild(node)
			self.endInsertRows()

		return True

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def registerFile(self, file, parent, ensureUniqueness=False):
		"""
		This method registers given file in the Model.
		
		:param file: File to register. ( String )
		:param parent: FileNode parent. ( GraphModelNode )
		:param ensureUniqueness: Ensure registrar uniqueness. ( Boolean )
		:return: FileNode. ( FileNode )
		"""

		if ensureUniqueness:
			if self.getFileNodes(file):
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' file is already registered!".format(
				self.__class__.__name__, file))

		LOGGER.debug("> Registering '{0}' file.".format(file))

		row = parent.childrenCount()
		self.beginInsertRows(self.getNodeIndex(parent), row, row)
		fileNode = FileNode(name=os.path.basename(file),
							path=file,
							parent=parent)
		self.endInsertRows()

		self.fileRegistered.emit(fileNode)

		return fileNode

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def unregisterFile(self, fileNode, raiseException=False):
		"""
		This method unregisters given :class:`umbra.components.factory.scriptEditor.nodes.FileNode` class Node from the Model.
		
		:param fileNode: FileNode to unregister. ( FileNode )
		:param raiseException: Raise the exception. ( Boolean )
		:return: FileNode. ( FileNode )
		"""

		if raiseException:
			if not fileNode in self.listFileNodes():
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' file 'FileNode' isn't registered!".format(
				self.__class__.__name__, fileNode))

		LOGGER.debug("> Unregistering '{0}' file 'FileNode'.".format(fileNode))

		parent = fileNode.parent
		row = fileNode.row()
		self.beginRemoveRows(self.getNodeIndex(parent), row, row)
		parent.removeChild(row)
		self.endRemoveRows()

		self.fileUnregistered.emit(fileNode)

		return fileNode

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def registerDirectory(self, directory, parent, ensureUniqueness=False):
		"""
		This method registers given directory in the Model.
		
		:param directory: Directory to register. ( String )
		:param parent: DirectoryNode parent. ( GraphModelNode )
		:param ensureUniqueness: Ensure registrar uniqueness. ( Boolean )
		:return: DirectoryNode. ( DirectoryNode )
		"""

		if ensureUniqueness:
			if self.getDirectoryNodes(directory):
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' directory is already registered!".format(
				self.__class__.__name__, directory))

		LOGGER.debug("> Registering '{0}' directory.".format(directory))

		row = parent.childrenCount()
		self.beginInsertRows(self.getNodeIndex(parent), row, row)
		directoryNode = DirectoryNode(name=os.path.basename(directory),
									path=directory,
									parent=parent)
		self.endInsertRows()

		self.directoryRegistered.emit(directoryNode)

		return directoryNode

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def unregisterDirectory(self, directoryNode, raiseException=False):
		"""
		This method unregisters given :class:`umbra.components.factory.scriptEditor.nodes.DirectoryNode` class Node from the Model.
		
		:param directoryNode: DirectoryNode to unregister. ( DirectoryNode )
		:param raiseException: Raise the exception. ( Boolean )
		:return: DirectoryNode. ( DirectoryNode )
		"""

		if raiseException:
			if not directoryNode in self.listDirectoryNodes():
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' directory 'DirectoryNode' isn't registered!".format(
				self.__class__.__name__, directoryNode))

		LOGGER.debug("> Unregistering '{0}' directory 'DirectoryNode'.".format(directoryNode))

		parent = directoryNode.parent
		row = directoryNode.row()
		self.beginRemoveRows(self.getNodeIndex(parent), row, row)
		parent.removeChild(row)
		self.endRemoveRows()

		self.directoryUnregistered.emit(directoryNode)

		return directoryNode

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def registerEditor(self, editor, parent, ensureUniqueness=False):
		"""
		This method registers given :class:`umbra.components.factory.scriptEditor.editor.Editor` class editor in the Model.
		
		:param editor: Editor to register. ( Editor )
		:param parent: EditorNode parent. ( GraphModelNode )
		:param ensureUniqueness: Ensure registrar uniqueness. ( Boolean )
		:return: EditorNode. ( EditorNode )
		"""

		if ensureUniqueness:
			if self.getEditorNodes(editor):
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' editor is already registered!".format(
				self.__class__.__name__, editor))

		LOGGER.debug("> Registering '{0}' editor.".format(editor))

		row = parent.childrenCount()
		self.beginInsertRows(self.getNodeIndex(parent), row, row)
		editorNode = EditorNode(editor=editor,
								parent=parent)
		self.endInsertRows()

		self.editorRegistered.emit(editorNode)

		return editorNode

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def unregisterEditor(self, editorNode, raiseException=False):
		"""
		This method unregisters given :class:`umbra.components.factory.scriptEditor.nodes.EditorNode` class Node from the Model.
		
		:param editorNode: EditorNode to unregister. ( EditorNode )
		:param raiseException: Raise the exception. ( Boolean )
		:return: EditorNode. ( EditorNode )
		"""

		if raiseException:
			if not editorNode in self.listEditorNodes():
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' editor 'EditorNode' isn't registered!".format(
				self.__class__.__name__, editorNode))

		LOGGER.debug("> Unregistering '{0}' editor 'EditorNode'.".format(editorNode))

		parent = editorNode.parent
		row = editorNode.row()
		self.beginRemoveRows(self.getNodeIndex(parent), row, row)
		parent.removeChild(row)
		self.endRemoveRows()

		self.editorUnregistered.emit(editorNode)

		return editorNode

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def registerProject(self, path, ensureUniqueness=False):
		"""
		This method registers given path in the Model as a project.

		:param path: Project path to register. ( String )
		:param ensureUniqueness: Ensure registrar uniqueness. ( Boolean )
		:return: ProjectNode. ( ProjectNode )		
		"""

		if ensureUniqueness:
			if self.getProjectNodes(path):
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' project is already registered!".format(
				self.__class__.__name__, path))

		LOGGER.debug("> Registering '{0}' project.".format(path))

		row = self.rootNode.childrenCount()
		self.beginInsertRows(self.getNodeIndex(self.rootNode,), row, row)
		projectNode = ProjectNode(name=os.path.basename(path),
								path=path,
								parent=self.rootNode)
		self.endInsertRows()

		self.projectRegistered.emit(projectNode)

		return projectNode

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def unregisterProject(self, projectNode, raiseException=False):
		"""
		This method unregisters given :class:`umbra.components.factory.scriptProject.nodes.ProjectNode` class Node from the Model.
		
		:param projectNode: ProjectNode to unregister. ( ProjectNode )
		:param raiseException: Raise the exception. ( Boolean )
		:return: ProjectNode. ( ProjectNode )
		"""

		if raiseException:
			if not projectNode in self.listProjectNodes():
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' project 'ProjectNode' isn't registered!".format(
				self.__class__.__name__, projectNode))

		LOGGER.debug("> Unregistering '{0}' project 'ProjectNode'.".format(projectNode))

		parent = projectNode.parent
		row = projectNode.row()
		self.beginRemoveRows(self.getNodeIndex(parent), row, row)
		parent.removeChild(row)
		self.endRemoveRows()

		self.projectUnregistered.emit(projectNode)

		return projectNode

	def isAuthoringNode(self, node):
		"""
		This method returns if given Node is an authoring node.

		:param node: Node. ( ProjectNode / DirectoryNode / FileNode )
		:return: Is authoring node. ( Boolean )
		"""

		for parentNode in foundations.walkers.nodesWalker(node, ascendants=True):
			if parentNode is self.__defaultProjectNode:
				return True
		return False

	def setAuthoringNodes(self, editor):
		"""
		This method sets the Model authoring Nodes using given editor.

		:param editor: Editor to set. ( Editor )
		:return: Method success. ( Boolean )
		"""

		projectNode = self.defaultProjectNode
		fileNode = self.registerFile(editor.file, projectNode)
		editorNode = self.registerEditor(editor, fileNode)
		return True

	def deleteAuthoringNodes(self, editor):
		"""
		This method deletes the Model authoring Nodes associated with given editor.

		:param editor: Editor. ( Editor )
		:return: Method success. ( Boolean )
		"""

		editorNode = foundations.common.getFirstItem(self.getEditorNodes(editor))
		fileNode = editorNode.parent
		self.unregisterEditor(editorNode)
		self.unregisterFile(fileNode, raiseException=False)
		return True

	def updateAuthoringNodes(self, editor):
		"""
		This method updates given editor Model authoring nodes.
		
		:param editor: Editor. ( Editor )
		:return: Method success. ( Boolean )
		"""

		editorNode = foundations.common.getFirstItem(self.getEditorNodes(editor))
		fileNode = editorNode.parent
		file = editor.file
		fileNode.name = editorNode.name = os.path.basename(file)
		fileNode.path = editorNode.path = file

		self.nodeChanged(fileNode)
		return True

	def setProjectNodes(self, rootNode, maximumDepth=1):
		"""
		This method sets the project Model children Nodes using given root node.

		:param rootNode: Root node. ( ProjectNode / DirectoryNode )
		:param maximumDepth: Maximum nodes nesting depth. ( Integer )
		"""

		rootDirectory = rootNode.path
		for parentDirectory, directories, files in foundations.walkers.depthWalker(rootDirectory, maximumDepth):
			if parentDirectory == rootDirectory:
				parentNode = rootNode
			else:
				parentNode = foundations.common.getFirstItem(
							[node for node in foundations.walkers.nodesWalker(rootNode) \
							if node.family == "Directory" and node.path == parentDirectory])

			if not parentNode:
				continue

			paths = [node.path for node in parentNode.children]
			for directory in sorted(directories):
				if directory.startswith("."):
					continue

				path = os.path.join(parentDirectory, directory)
				if path in paths:
					continue

				directoryNode = self.registerDirectory(path, parentNode)

			for file in sorted(files):
				if file.startswith("."):
					continue

				path = os.path.join(parentDirectory, file)
				if path in paths:
					continue

				if foundations.common.isBinaryFile(path):
					continue

				fileNode = self.registerFile(path, parentNode)

	def deleteProjectNodes(self, node):
		"""
		This method deletes the Model project Nodes associated with given node.

		:param node: Node. ( ProjectNode )
		"""

		self.unregisterProjectNodes(node)
		self.unregisterProject(node)

	def unregisterProjectNodes(self, node):
		"""
		This method unregisters given Node children.
		
		:param node: Node. ( ProjectNode / DirectoryNode )
		"""

		for node in reversed(list(foundations.walkers.nodesWalker(node))):
			if node.family == "Directory":
				self.unregisterDirectory(node)
			elif node.family == "File":
				self.unregisterFile(node)

	def updateProjectNodes(self, node):
		"""
		This method updates given root Node children.
		
		:param node: Node. ( ProjectNode / DirectoryNode )
		"""

		self.unregisterProjectNodes(node)
		self.setProjectNodes(node)

class LanguagesModel(QAbstractListModel):
	"""
	This class is a `QAbstractListModel <http://doc.qt.nokia.com/qabstractListmodel.html>`_ subclass used
	to store the :class:`umbra.components.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class languages.
	"""

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
	@foundations.exceptions.handleExceptions(AssertionError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def languages(self):
		"""
		This method is the deleter method for **self.__languages** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "languages"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def rowCount(self, parent=QModelIndex()):
		"""
		This method reimplements the :meth:`QAbstractListModel.rowCount` method.

		:param parent: Parent. ( QModelIndex )
		:return: Row count. ( Integer )
		"""

		return len(self.__languages)

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

	def sortLanguages(self, order=Qt.AscendingOrder):
		"""
		This method sorts the Model languages.
		
		:param order: Order. ( Qt.SortOrder )
		"""

		self.beginResetModel()
		self.__languages = sorted(self.__languages, key=lambda x: (x.name), reverse=order)
		self.endResetModel()

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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

	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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

class PatternsModel(umbra.ui.models.GraphModel):
	"""
	This class defines the Model used the by
	:class:`umbra.patterns.factory.scriptEditor.searchAndReplace.SearchAndReplace` class to store the search and \
	replace patterns.
	"""

	# Custom signals definitions.
	patternInserted = pyqtSignal(PatternNode)
	"""
	This signal is emited by the :class:`PatternsModel` class when a pattern has been inserted. ( pyqtSignal )

	:return: Inserted pattern node. ( PatternNode )
	"""

	# Custom signals definitions.
	patternRemoved = pyqtSignal(PatternNode)
	"""
	This signal is emited by the :class:`PatternsModel` class when a pattern has been removed. ( pyqtSignal )

	:return: Removed pattern node. ( PatternNode )
	"""

	def __init__(self, parent=None, rootNode=None, horizontalHeaders=None, verticalHeaders=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param rootNode: Root node. ( AbstractCompositeNode )
		:param horizontalHeaders: Headers. ( OrderedDict )
		:param verticalHeaders: Headers. ( OrderedDict )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModel.__init__(self, parent, rootNode, horizontalHeaders, verticalHeaders, PatternNode)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def initializeModel(self, rootNode):
		"""
		This method initializes the Model using given root node.
		
		:param rootNode: Graph root node. ( DefaultNode )
		:return: Method success ( Boolean )
		"""

		LOGGER.debug("> Initializing model with '{0}' root node.".format(rootNode))

		self.beginResetModel()
		self.rootNode = rootNode
		self.enableModelTriggers(True)
		self.endResetModel()
		return True

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
		patternNode = PatternNode(name=pattern)
		self.rootNode.insertChild(patternNode, index)
		self.endInsertRows()
		self.patternInserted.emit(patternNode)
		return True

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
			patternNode = self.rootNode.child(index)
			self.rootNode.removeChild(index)
			self.endRemoveRows()
			self.patternRemoved.emit(patternNode)
			return True

class SearchResultsModel(umbra.ui.models.GraphModel):
	"""
	This class defines the Model used the by
	:class:`umbra.patterns.factory.scriptEditor.searchInFiles.SearchInFiles` class to store the search results.
	"""

	def __init__(self, parent=None, rootNode=None, horizontalHeaders=None, verticalHeaders=None, defaultNode=None):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param rootNode: Root node. ( AbstractCompositeNode )
		:param horizontalHeaders: Headers. ( OrderedDict )
		:param verticalHeaders: Headers. ( OrderedDict )
		:param defaultNode: Default node. ( GraphModelNode )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModel.__init__(self, parent, rootNode, horizontalHeaders, verticalHeaders, defaultNode)

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def initializeModel(self, rootNode):
		"""
		This method initializes the Model using given root node.
		
		:param rootNode: Graph root node. ( DefaultNode )
		:return: Method success ( Boolean )
		"""

		LOGGER.debug("> Initializing model with '{0}' root node.".format(rootNode))

		self.beginResetModel()
		self.rootNode = rootNode
		self.enableModelTriggers(True)
		self.endResetModel()
		return True

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
