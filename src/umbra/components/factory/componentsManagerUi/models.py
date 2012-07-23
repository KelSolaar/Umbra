#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**models.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`umbra.components.factory.componentsManagerUi.componentsManagerUi.ComponentsManagerUi`
	Component Interface class Models.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.exceptions
import umbra.ui.models
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

__all__ = ["LOGGER", "ComponentsModel"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class ComponentsModel(umbra.ui.models.GraphModel):
	"""
	This class defines the Model used the by
	:class:`umbra.components.factory.componentsManagerUi.componentsManagerUi.ComponentsManagerUi`
	Component Interface class. 
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
