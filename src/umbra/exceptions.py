#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**exceptions.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Umbra** package exceptions. 

**Others:**

"""

#***********************************************************************************************
#***	Internal imports.
#***********************************************************************************************
import foundations.exceptions

#***********************************************************************************************
#***	Module attributes.
#***********************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = []

#***********************************************************************************************
#***	Module classes and definitions.
#***********************************************************************************************
class AbstractEngineError(foundations.exceptions.AbstractError):
	"""
	This class is the abstract base class for engine related exceptions.
	"""

	pass

class EngineConfigurationError(foundations.exceptions.AbstractError):
	"""
	This class is used for engine configuration exceptions.
	"""

	pass

class EngineInitializationError(foundations.exceptions.AbstractError):
	"""
	This class is used for engine initialization exceptions.
	"""

	pass

class ResourceExistsError(foundations.exceptions.AbstractOsError):
	"""
	This class is used for non existing resource exceptions.
	"""

	pass

class AbstractActionsManagerError(foundations.exceptions.AbstractError):
	"""
	This class is the abstract base class for :class:`ActionsManager` related exceptions.
	"""

	pass

class CategoryExistsError(AbstractActionsManagerError):
	"""
	This class is used for non existing category exceptions.
	"""

	pass

class ActionExistsError(AbstractActionsManagerError):
	"""
	This class is used for non existing action exceptions.
	"""

	pass
