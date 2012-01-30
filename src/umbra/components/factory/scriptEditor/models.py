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
			"LanguagesModel",
			"PatternNode",
			"PatternsModel",
			"SearchFileNode",
			"SearchOccurenceNode",
			"SearchResultsModel"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
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
	def getOccurencesCount(self):
		"""
		This method returns the Model occurences count.
		
		:return: Occurences count. ( Integer )
		"""

		return len([node for node in foundations.walkers.nodesWalker(self.rootNode) if node.family == "SearchOccurence"])
