#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`umbra.components.factory.script_editor.script_editor.ScriptEditor`
	Component Interface class Models.

**Others:**

"""

from __future__ import unicode_literals

import os
import re
from PyQt4.QtCore import QAbstractListModel
from PyQt4.QtCore import QModelIndex
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal

import foundations.exceptions
import foundations.io
import foundations.verbose
import foundations.walkers
import umbra.ui.models
import umbra.ui.nodes
from umbra.components.factory.script_editor.nodes import ProjectNode
from umbra.components.factory.script_editor.nodes import DirectoryNode
from umbra.components.factory.script_editor.nodes import EditorNode
from umbra.components.factory.script_editor.nodes import FileNode
from umbra.components.factory.script_editor.nodes import PatternNode
from umbra.ui.languages import Language

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
			"ProjectsModel",
			"LanguagesModel",
			"PatternsModel",
			"SearchResultsModel"]

LOGGER = foundations.verbose.install_logger()

class ProjectsModel(umbra.ui.models.GraphModel):
	"""
	Defines the Model used by :class:`umbra.components.factory.script_editor.script_editor.ScriptEditor`
	Component Interface class.
	"""

	file_registered = pyqtSignal(FileNode)
	"""
	This signal is emited by the :class:`ProjectsModel` class when a file is registered.

	:return: Registered file FileNode.
	:rtype: FileNode
	"""

	file_unregistered = pyqtSignal(FileNode)
	"""
	This signal is emited by the :class:`ProjectsModel` class when a file is unregistered.

	:return: Unregistered file FileNode.
	:rtype: FileNode
	"""

	editor_registered = pyqtSignal(EditorNode)
	"""
	This signal is emited by the :class:`ProjectsModel` class when an editor is registered.

	:return: Registered editor EditorNode.
	:rtype: EditorNode
	"""

	editor_unregistered = pyqtSignal(EditorNode)
	"""
	This signal is emited by the :class:`ProjectsModel` class when an editor is unregistered.

	:return: Unregistered editor EditorNode.
	:rtype: EditorNode
	"""

	directory_registered = pyqtSignal(DirectoryNode)
	"""
	This signal is emited by the :class:`ProjectsModel` class when a directory is registered.

	:return: Registered directory DirectoryNode.
	:rtype: DirectoryNode
	"""

	directory_unregistered = pyqtSignal(DirectoryNode)
	"""
	This signal is emited by the :class:`ProjectsModel` class when a directory is unregistered.

	:return: Unregistered directory DirectoryNode.
	:rtype: DirectoryNode
	"""

	project_registered = pyqtSignal(ProjectNode)
	"""
	This signal is emited by the :class:`ProjectsModel` class when a project is registered.

	:return: Registered project ProjectNode.
	:rtype: ProjectNode
	"""

	project_unregistered = pyqtSignal(ProjectNode)
	"""
	This signal is emited by the :class:`ProjectsModel` class when a project is unregistered.

	:return: Unregistered project ProjectNode.
	:rtype: ProjectNode
	"""

	def __init__(self,
				parent=None,
				root_node=None,
				horizontal_headers=None,
				vertical_headers=None,
				default_node=None,
				default_project=None):
		"""
		Initializes the class.

		:param default_project: Default project name.
		:type default_project: unicode
		:param parent: Object parent.
		:type parent: QObject
		:param root_node: Root node.
		:type root_node: AbstractCompositeNode
		:param horizontal_headers: Headers.
		:type horizontal_headers: OrderedDict
		:param vertical_headers: Headers.
		:type vertical_headers: OrderedDict
		:param default_node: Default node.
		:type default_node: GraphModelNode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModel.__init__(self, parent, root_node, horizontal_headers, vertical_headers, default_node)

		# --- Setting class attributes. ---
		self.__default_project = None
		self.default_project = default_project or "default_project"

		self.__default_project_node = None

		ProjectsModel.__initialize_model(self)

	@property
	def default_project(self):
		"""
		Property for **self.__default_project** attribute.

		:return: self.__default_project.
		:rtype: unicode
		"""

		return self.__default_project

	@default_project.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def default_project(self, value):
		"""
		Setter for **self.__default_project** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		if value is not None:
			assert type(value) is unicode, \
			 "'{0}' attribute: '{1}' type is not 'unicode'!".format("default_project", value)
		self.__default_project = value

	@default_project.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_project(self):
		"""
		Deleter for **self.__default_project** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_project"))

	@property
	def default_project_node(self):
		"""
		Property for **self.__default_project_node** attribute.

		:return: self.__default_project_node.
		:rtype: unicode
		"""

		return self.__default_project_node

	@default_project_node.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_project_node(self, value):
		"""
		Setter for **self.__default_project_node** attribute.

		:param value: Attribute value.
		:type value: unicode
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "default_project_node"))

	@default_project_node.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def default_project_node(self):
		"""
		Deleter for **self.__default_project_node** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "default_project_node"))

	def __initialize_model(self):
		"""
		Initializes the Model.
		"""

		LOGGER.debug("> Initializing model.")

		self.beginResetModel()
		self.root_node = umbra.ui.nodes.DefaultNode(name="InvisibleRootNode")
		self.__default_project_node = ProjectNode(name=self.__default_project,
								parent=self.root_node,
								node_flags=int(Qt.ItemIsEnabled),
								attributes_flags=int(Qt.ItemIsEnabled))
		self.enable_model_triggers(True)
		self.endResetModel()

	def list_editor_nodes(self, node=None):
		"""
		Returns the Model :class:`umbra.components.factory.script_editor.nodes.EditorNode` class nodes.

		:param node: Node to start walking from.
		:type node: AbstractNode or AbstractCompositeNode or Object
		:return: EditorNode nodes.
		:rtype: list
		"""

		return self.find_family("Editor", node=node or self.__default_project_node)

	def list_file_nodes(self, node=None):
		"""
		Returns the Model :class:`umbra.components.factory.script_editor.nodes.FileNode` class nodes.

		:param node: Node to start walking from.
		:type node: AbstractNode or AbstractCompositeNode or Object
		:return: FileNode nodes.
		:rtype: list
		"""

		return self.find_family("File", node=node or self.__default_project_node)

	def list_directory_nodes(self):
		"""
		Returns the Model :class:`umbra.components.factory.script_editor.nodes.DirectoryNode` class nodes.

		:return: DirectoryNode nodes.
		:rtype: list
		"""

		return self.find_family("Directory")

	def list_project_nodes(self, ignore_default_project_node=True):
		"""
		Returns the Model :class:`umbra.components.factory.script_editor.nodes.ProjectNode` class nodes.

		:param ignore_default_project_node: Default ProjectNode will be ignored.
		:type ignore_default_project_node: bool
		:return: ProjectNode nodes.
		:rtype: list
		"""

		project_nodes = self.find_family("Project")
		return filter(lambda x: x != self.__default_project_node, project_nodes) \
		if ignore_default_project_node else project_nodes

	def list_editors(self, node=None):
		"""
		Returns the Model editors.

		:param node: Node to start walking from.
		:type node: AbstractNode or AbstractCompositeNode or Object
		:return: Editors.
		:rtype: list
		"""

		return [editor_node.editor for editor_node in self.list_editor_nodes(node) 	if editor_node.editor]

	def list_files(self, node=None):
		"""
		Returns the Model files.

		:param node: Node to start walking from.
		:type node: AbstractNode or AbstractCompositeNode or Object
		:return: FileNode nodes.
		:rtype: list
		"""

		return [file_node.path for file_node in self.list_file_nodes(node) if file_node.path]

	def list_directories(self):
		"""
		Returns the Model directories.

		:return: DirectoryNode nodes.
		:rtype: list
		"""

		return [directory_node.path for directory_node in self.list_directory_nodes() if directory_node.path]

	def list_projects(self, ignore_default_project_node=True):
		"""
		Returns the Model projects.

		:param ignore_default_project_node: Default ProjectNode will be ignored.
		:type ignore_default_project_node: bool
		:return: ProjectNode nodes.
		:rtype: list
		"""

		return [project_node.path for project_node in self.list_project_nodes(ignore_default_project_node) if project_node.path]

	def get_editor_nodes(self, editor, node=None):
		"""
		Returns the :class:`umbra.components.factory.script_editor.nodes.EditorNode` class Nodes with given editor.

		:param node: Node to start walking from.
		:type node: AbstractNode or AbstractCompositeNode or Object
		:param editor: Editor.
		:type editor: Editor
		:return: EditorNode nodes.
		:rtype: list
		"""

		return [editor_node for editor_node in self.list_editor_nodes(node) if editor_node.editor == editor]

	def get_file_nodes(self, path, node=None):
		"""
		Returns the :class:`umbra.components.factory.script_editor.nodes.FileNode` class Nodes with given path.

		:param node: Node to start walking from.
		:type node: AbstractNode or AbstractCompositeNode or Object
		:param path: File path.
		:type path: unicode
		:return: FileNode nodes.
		:rtype: list
		"""

		return [file_node for file_node in self.list_file_nodes(node) if file_node.path == path]

	def get_directory_nodes(self, path):
		"""
		Returns the :class:`umbra.components.factory.script_editor.nodes.DirectoryNode` class Nodes with given path.

		:param path: Directory path.
		:type path: unicode
		:return: DirectoryNode nodes.
		:rtype: list
		"""

		return [directory_node for directory_node in self.list_directory_nodes() if directory_node.path == path]

	def get_project_nodes(self, path):
		"""
		Returns the :class:`umbra.components.factory.script_editor.nodes.ProjectNode` class Nodes with given path.

		:param path: Project path.
		:type path: unicode
		:return: ProjectNode nodes.
		:rtype: list
		"""

		return [project_node for project_node in self.list_project_nodes() if project_node.path == path]

	def move_node(self, parent, from_index, to_index):
		"""
		Moves given parent child to given index.

		:param to_index: Index to.
		:type to_index: int
		:param from_index: Index from.
		:type from_index: int
		:return: Method success.
		:rtype: bool
		"""

		# TODO: Should be refactored once this ticket is fixed:
		# https://bugreports.qt-project.org/browse/PYSIDE-78
		if not from_index >= 0 or \
		not from_index < parent.children_count() or \
		not to_index >= 0 or \
		not to_index < parent.children_count():
			return False

		parent_index = self.get_node_index(parent)
		self.beginRemoveRows(parent_index, from_index, from_index)
		child = parent.remove_child(from_index)
		self.endRemoveRows()

		start_index = parent.children_count() - 1
		end_index = to_index - 1

		tail = []
		for i in range(start_index, end_index, -1):
			self.beginRemoveRows(parent_index, i, i)
			tail.append(parent.remove_child(i))
			self.endRemoveRows()
		tail = list(reversed(tail))
		tail.insert(0, child)

		for node in tail:
			row = parent.children_count()
			self.beginInsertRows(parent_index, row, row)
			parent.add_child(node)
			self.endInsertRows()

		return True

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def register_file(self, file, parent, ensure_uniqueness=False):
		"""
		Registers given file in the Model.

		:param file: File to register.
		:type file: unicode
		:param parent: FileNode parent.
		:type parent: GraphModelNode
		:param ensure_uniqueness: Ensure registrar uniqueness.
		:type ensure_uniqueness: bool
		:return: FileNode.
		:rtype: FileNode
		"""

		if ensure_uniqueness:
			if self.get_file_nodes(file):
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' file is already registered!".format(
				self.__class__.__name__, file))

		LOGGER.debug("> Registering '{0}' file.".format(file))

		row = parent.children_count()
		self.beginInsertRows(self.get_node_index(parent), row, row)
		file_node = FileNode(name=os.path.basename(file),
							path=file,
							parent=parent)
		self.endInsertRows()

		self.file_registered.emit(file_node)

		return file_node

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def unregister_file(self, file_node, raise_exception=False):
		"""
		Unregisters given :class:`umbra.components.factory.script_editor.nodes.FileNode` class Node from the Model.

		:param file_node: FileNode to unregister.
		:type file_node: FileNode
		:param raise_exception: Raise the exception.
		:type raise_exception: bool
		:return: FileNode.
		:rtype: FileNode
		"""

		if raise_exception:
			if not file_node in self.list_file_nodes():
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' file 'FileNode' isn't registered!".format(
				self.__class__.__name__, file_node))

		LOGGER.debug("> Unregistering '{0}' file 'FileNode'.".format(file_node))

		parent = file_node.parent
		row = file_node.row()
		self.beginRemoveRows(self.get_node_index(parent), row, row)
		parent.remove_child(row)
		self.endRemoveRows()

		self.file_unregistered.emit(file_node)

		return file_node

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def register_directory(self, directory, parent, ensure_uniqueness=False):
		"""
		Registers given directory in the Model.

		:param directory: Directory to register.
		:type directory: unicode
		:param parent: DirectoryNode parent.
		:type parent: GraphModelNode
		:param ensure_uniqueness: Ensure registrar uniqueness.
		:type ensure_uniqueness: bool
		:return: DirectoryNode.
		:rtype: DirectoryNode
		"""

		if ensure_uniqueness:
			if self.get_directory_nodes(directory):
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' directory is already registered!".format(
				self.__class__.__name__, directory))

		LOGGER.debug("> Registering '{0}' directory.".format(directory))

		row = parent.children_count()
		self.beginInsertRows(self.get_node_index(parent), row, row)
		directory_node = DirectoryNode(name=os.path.basename(directory),
									path=directory,
									parent=parent)
		self.endInsertRows()

		self.directory_registered.emit(directory_node)

		return directory_node

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def unregister_directory(self, directory_node, raise_exception=False):
		"""
		Unregisters given :class:`umbra.components.factory.script_editor.nodes.DirectoryNode` class Node from the Model.

		:param directory_node: DirectoryNode to unregister.
		:type directory_node: DirectoryNode
		:param raise_exception: Raise the exception.
		:type raise_exception: bool
		:return: DirectoryNode.
		:rtype: DirectoryNode
		"""

		if raise_exception:
			if not directory_node in self.list_directory_nodes():
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' directory 'DirectoryNode' isn't registered!".format(
				self.__class__.__name__, directory_node))

		LOGGER.debug("> Unregistering '{0}' directory 'DirectoryNode'.".format(directory_node))

		parent = directory_node.parent
		row = directory_node.row()
		self.beginRemoveRows(self.get_node_index(parent), row, row)
		parent.remove_child(row)
		self.endRemoveRows()

		self.directory_unregistered.emit(directory_node)

		return directory_node

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def register_editor(self, editor, parent, ensure_uniqueness=False):
		"""
		Registers given :class:`umbra.components.factory.script_editor.editor.Editor` class editor in the Model.

		:param editor: Editor to register.
		:type editor: Editor
		:param parent: EditorNode parent.
		:type parent: GraphModelNode
		:param ensure_uniqueness: Ensure registrar uniqueness.
		:type ensure_uniqueness: bool
		:return: EditorNode.
		:rtype: EditorNode
		"""

		if ensure_uniqueness:
			if self.get_editor_nodes(editor):
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' editor is already registered!".format(
				self.__class__.__name__, editor))

		LOGGER.debug("> Registering '{0}' editor.".format(editor))

		row = parent.children_count()
		self.beginInsertRows(self.get_node_index(parent), row, row)
		editor_node = EditorNode(editor=editor,
								parent=parent)
		self.endInsertRows()

		self.editor_registered.emit(editor_node)

		return editor_node

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def unregister_editor(self, editor_node, raise_exception=False):
		"""
		Unregisters given :class:`umbra.components.factory.script_editor.nodes.EditorNode` class Node from the Model.

		:param editor_node: EditorNode to unregister.
		:type editor_node: EditorNode
		:param raise_exception: Raise the exception.
		:type raise_exception: bool
		:return: EditorNode.
		:rtype: EditorNode
		"""

		if raise_exception:
			if not editor_node in self.list_editor_nodes():
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' editor 'EditorNode' isn't registered!".format(
				self.__class__.__name__, editor_node))

		LOGGER.debug("> Unregistering '{0}' editor 'EditorNode'.".format(editor_node))

		parent = editor_node.parent
		row = editor_node.row()
		self.beginRemoveRows(self.get_node_index(parent), row, row)
		parent.remove_child(row)
		self.endRemoveRows()

		self.editor_unregistered.emit(editor_node)

		return editor_node

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def register_project(self, path, ensure_uniqueness=False):
		"""
		Registers given path in the Model as a project.

		:param path: Project path to register.
		:type path: unicode
		:param ensure_uniqueness: Ensure registrar uniqueness.
		:type ensure_uniqueness: bool
		:return: ProjectNode.
		:rtype: ProjectNode
		"""

		if ensure_uniqueness:
			if self.get_project_nodes(path):
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' project is already registered!".format(
				self.__class__.__name__, path))

		LOGGER.debug("> Registering '{0}' project.".format(path))

		row = self.root_node.children_count()
		self.beginInsertRows(self.get_node_index(self.root_node,), row, row)
		project_node = ProjectNode(name=os.path.basename(path),
								path=path,
								parent=self.root_node)
		self.endInsertRows()

		self.project_registered.emit(project_node)

		return project_node

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def unregister_project(self, project_node, raise_exception=False):
		"""
		Unregisters given :class:`umbra.components.factory.scriptProject.nodes.ProjectNode` class Node from the Model.

		:param project_node: ProjectNode to unregister.
		:type project_node: ProjectNode
		:param raise_exception: Raise the exception.
		:type raise_exception: bool
		:return: ProjectNode.
		:rtype: ProjectNode
		"""

		if raise_exception:
			if not project_node in self.list_project_nodes():
				raise foundations.exceptions.ProgrammingError("{0} | '{1}' project 'ProjectNode' isn't registered!".format(
				self.__class__.__name__, project_node))

		LOGGER.debug("> Unregistering '{0}' project 'ProjectNode'.".format(project_node))

		parent = project_node.parent
		row = project_node.row()
		self.beginRemoveRows(self.get_node_index(parent), row, row)
		parent.remove_child(row)
		self.endRemoveRows()

		self.project_unregistered.emit(project_node)

		return project_node

	def is_authoring_node(self, node):
		"""
		Returns if given Node is an authoring node.

		:param node: Node.
		:type node: ProjectNode or DirectoryNode or FileNode
		:return: Is authoring node.
		:rtype: bool
		"""

		for parent_node in foundations.walkers.nodes_walker(node, ascendants=True):
			if parent_node is self.__default_project_node:
				return True
		return False

	def set_authoring_nodes(self, editor):
		"""
		Sets the Model authoring Nodes using given editor.

		:param editor: Editor to set.
		:type editor: Editor
		:return: Method success.
		:rtype: bool
		"""

		project_node = self.default_project_node
		file_node = self.register_file(editor.file, project_node)
		editor_node = self.register_editor(editor, file_node)
		return True

	def delete_authoring_nodes(self, editor):
		"""
		Deletes the Model authoring Nodes associated with given editor.

		:param editor: Editor.
		:type editor: Editor
		:return: Method success.
		:rtype: bool
		"""

		editor_node = foundations.common.get_first_item(self.get_editor_nodes(editor))
		file_node = editor_node.parent
		self.unregister_editor(editor_node)
		self.unregister_file(file_node, raise_exception=False)
		return True

	def update_authoring_nodes(self, editor):
		"""
		Updates given editor Model authoring nodes.

		:param editor: Editor.
		:type editor: Editor
		:return: Method success.
		:rtype: bool
		"""

		editor_node = foundations.common.get_first_item(self.get_editor_nodes(editor))
		file_node = editor_node.parent
		file = editor.file
		file_node.name = editor_node.name = os.path.basename(file)
		file_node.path = editor_node.path = file

		self.node_changed(file_node)
		return True

	def set_project_nodes(self, root_node, maximum_depth=1):
		"""
		Sets the project Model children Nodes using given root node.

		:param root_node: Root node.
		:type root_node: ProjectNode or DirectoryNode
		:param maximum_depth: Maximum nodes nesting depth.
		:type maximum_depth: int
		"""

		root_directory = root_node.path
		for parent_directory, directories, files in foundations.walkers.depth_walker(root_directory, maximum_depth):
			if parent_directory == root_directory:
				parent_node = root_node
			else:
				parent_node = foundations.common.get_first_item(
							[node for node in foundations.walkers.nodes_walker(root_node) \
							if node.family == "Directory" and node.path == parent_directory])

			if not parent_node:
				continue

			paths = [node.path for node in parent_node.children]
			for directory in sorted(directories):
				if directory.startswith("."):
					continue

				path = os.path.join(parent_directory, directory)
				if path in paths:
					continue

				directory_node = self.register_directory(path, parent_node)

			for file in sorted(files):
				if file.startswith("."):
					continue

				path = os.path.join(parent_directory, file)
				if path in paths:
					continue

				if foundations.io.is_readable(path):
					if foundations.io.is_binary_file(path):
						continue

				file_node = self.register_file(path, parent_node)

	def delete_project_nodes(self, node):
		"""
		Deletes the Model project Nodes associated with given node.

		:param node: Node.
		:type node: ProjectNode
		"""

		self.unregister_project_nodes(node)
		self.unregister_project(node)

	def unregister_project_nodes(self, node):
		"""
		Unregisters given Node children.

		:param node: Node.
		:type node: ProjectNode or DirectoryNode
		"""

		for node in reversed(list(foundations.walkers.nodes_walker(node))):
			if node.family == "Directory":
				self.unregister_directory(node)
			elif node.family == "File":
				self.unregister_file(node)

	def update_project_nodes(self, node):
		"""
		Updates given root Node children.

		:param node: Node.
		:type node: ProjectNode or DirectoryNode
		"""

		self.unregister_project_nodes(node)
		self.set_project_nodes(node)

class LanguagesModel(QAbstractListModel):
	"""
	Defines a `QAbstractListModel <http://doc.qt.nokia.com/qabstractListmodel.html>`_ subclass used
	to store the :class:`umbra.components.factory.script_editor.script_editor.ScriptEditor`
	Component Interface class languages.
	"""

	def __init__(self, parent=None, languages=None):
		"""
		Initializes the class.

		:param parent: Parent object.
		:type parent: QObject
		:param languages: Languages.
		:type languages: list
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QAbstractListModel.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__languages = []
		self.languages = languages

	@property
	def languages(self):
		"""
		Property for **self.__languages** attribute.

		:return: self.__languages.
		:rtype: list
		"""

		return self.__languages

	@languages.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def languages(self, value):
		"""
		Setter for **self.__languages** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		if value is not None:
			assert type(value) is list, "'{0}' attribute: '{1}' type is not 'list'!".format("languages", value)
			for element in value:
				assert type(element) is Language, "'{0}' attribute: '{1}' type is not 'Language'!".format("languages", element)
		self.beginResetModel()
		self.__languages = value
		self.endResetModel()

	@languages.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def languages(self):
		"""
		Deleter for **self.__languages** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "languages"))

	def rowCount(self, parent=QModelIndex()):
		"""
		Reimplements the :meth:`QAbstractListModel.rowCount` method.

		:param parent: Parent.
		:type parent: QModelIndex
		:return: Row count.
		:rtype: int
		"""

		return len(self.__languages)

	def data(self, index, role=Qt.DisplayRole):
		"""
		Reimplements the :meth:`QAbstractListModel.data` method.

		:param index: Index.
		:type index: QModelIndex
		:param role: Role.
		:type role: int
		:return: Data.
		:rtype: QVariant
		"""

		if not index.isValid():
			return QVariant()

		if role == Qt.DisplayRole:
			return QVariant(self.__languages[index.row()].name)
		return QVariant()

	def sort_languages(self, order=Qt.AscendingOrder):
		"""
		Sorts the Model languages.

		:param order: Order. ( Qt.SortOrder )
		"""

		self.beginResetModel()
		self.__languages = sorted(self.__languages, key=lambda x: (x.name), reverse=order)
		self.endResetModel()

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def register_language(self, language):
		"""
		Registers given language in the :obj:`LanguagesModel.languages` class property.

		:param language: Language to register.
		:type language: Language
		:return: Method success.
		:rtype: bool
		"""

		if self.get_language(language):
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' language is already registered!".format(
			self.__class__.__name__, language.name))

		LOGGER.debug("> Registering '{0}' language.".format(language.name))

		self.__languages.append(language)
		self.sort_languages()
		return True

	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def unregister_language(self, name):
		"""
		Unregisters language with given name from the :obj:`LanguagesModel.languages` class property.

		:param name: Language to unregister.
		:type name: unicode
		:return: Method success.
		:rtype: bool
		"""

		if not self.get_language(name):
			raise foundations.exceptions.ProgrammingError("{0} | '{1}' language isn't registered!".format(
			self.__class__.__name__, name))

		LOGGER.debug("> Unregistering '{0}' language.".format(name))

		for i, language in enumerate(self.__languages):
			if not language.name == name:
				continue

			del(self.__languages[i])
			self.sort_languages()
			return True

	def get_language(self, name):
		"""
		Returns the language with given name.

		:param name: Language name.
		:type name: unicode
		:return: File language.
		:rtype: Language
		"""

		for language in self.__languages:
			if language.name == name:
				LOGGER.debug("> Language '{0}': '{1}'.".format(name, language))
				return language

	def get_file_language(self, file):
		"""
		Returns the language of given file.

		:param file: File to get language of.
		:type file: unicode
		:return: File language.
		:rtype: Language
		"""

		for language in self.__languages:
			if re.search(language.extensions, file):
				LOGGER.debug("> '{0}' file detected language: '{1}'.".format(file, language.name))
				return language

class PatternsModel(umbra.ui.models.GraphModel):
	"""
	Defines the Model used the by
	:class:`umbra.patterns.factory.script_editor.search_and_replace.SearchAndReplace` class to store the search and \
	replace patterns.
	"""

	# Custom signals definitions.
	pattern_inserted = pyqtSignal(PatternNode)
	"""
	This signal is emited by the :class:`PatternsModel` class when a pattern has been inserted.

	:return: Inserted pattern node.
	:rtype: PatternNode
	"""

	# Custom signals definitions.
	pattern_removed = pyqtSignal(PatternNode)
	"""
	This signal is emited by the :class:`PatternsModel` class when a pattern has been removed.

	:return: Removed pattern node.
	:rtype: PatternNode
	"""

	def __init__(self, parent=None, root_node=None, horizontal_headers=None, vertical_headers=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param root_node: Root node.
		:type root_node: AbstractCompositeNode
		:param horizontal_headers: Headers.
		:type horizontal_headers: OrderedDict
		:param vertical_headers: Headers.
		:type vertical_headers: OrderedDict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModel.__init__(self, parent, root_node, horizontal_headers, vertical_headers, PatternNode)

	def initialize_model(self, root_node):
		"""
		Initializes the Model using given root node.

		:param root_node: Graph root node.
		:type root_node: DefaultNode
		:return: Method success
		:rtype: bool
		"""

		LOGGER.debug("> Initializing model with '{0}' root node.".format(root_node))

		self.beginResetModel()
		self.root_node = root_node
		self.enable_model_triggers(True)
		self.endResetModel()
		return True

	def insert_pattern(self, pattern, index):
		"""
		Inserts given pattern into the Model.

		:param pattern: Pattern.
		:type pattern: unicode
		:param index: Insertion index.
		:type index: int
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Inserting '{0}' at '{1}' index.".format(pattern, index))

		self.remove_pattern(pattern)

		self.beginInsertRows(self.get_node_index(self.root_node), index, index)
		pattern_node = PatternNode(name=pattern)
		self.root_node.insert_child(pattern_node, index)
		self.endInsertRows()
		self.pattern_inserted.emit(pattern_node)
		return True

	def remove_pattern(self, pattern):
		"""
		Removes given pattern from the Model.

		:param pattern: Pattern.
		:type pattern: unicode
		:return: Method success.
		:rtype: bool
		"""

		for index, node in enumerate(self.root_node.children):
			if node.name != pattern:
				continue

			LOGGER.debug("> Removing '{0}' at '{1}' index.".format(pattern, index))

			self.beginRemoveRows(self.get_node_index(self.root_node), index, index)
			pattern_node = self.root_node.child(index)
			self.root_node.remove_child(index)
			self.endRemoveRows()
			self.pattern_removed.emit(pattern_node)
			return True

class SearchResultsModel(umbra.ui.models.GraphModel):
	"""
	Defines the Model used the by
	:class:`umbra.patterns.factory.script_editor.search_in_files.SearchInFiles` class to store the search results.
	"""

	def __init__(self, parent=None, root_node=None, horizontal_headers=None, vertical_headers=None, default_node=None):
		"""
		Initializes the class.

		:param parent: Object parent.
		:type parent: QObject
		:param root_node: Root node.
		:type root_node: AbstractCompositeNode
		:param horizontal_headers: Headers.
		:type horizontal_headers: OrderedDict
		:param vertical_headers: Headers.
		:type vertical_headers: OrderedDict
		:param default_node: Default node.
		:type default_node: GraphModelNode
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		umbra.ui.models.GraphModel.__init__(self, parent, root_node, horizontal_headers, vertical_headers, default_node)

	def initialize_model(self, root_node):
		"""
		Initializes the Model using given root node.

		:param root_node: Graph root node.
		:type root_node: DefaultNode
		:return: Method success
		:rtype: bool
		"""

		LOGGER.debug("> Initializing model with '{0}' root node.".format(root_node))

		self.beginResetModel()
		self.root_node = root_node
		self.enable_model_triggers(True)
		self.endResetModel()
		return True

	def get_metrics(self):
		"""
		Returns the Model metrics.

		:return: Nodes metrics.
		:rtype: dict
		"""

		search_file_nodes_count = search_occurence_nodesCount = 0

		for node in foundations.walkers.nodes_walker(self.root_node):
			if node.family == "SearchFile":
				search_file_nodes_count += 1
			elif node.family == "SearchOccurence":
				search_occurence_nodesCount += 1

		return {"SearchFile" : search_file_nodes_count, "SearchOccurence" : search_occurence_nodesCount}
