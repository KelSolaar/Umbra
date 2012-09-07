#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**exceptions.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`umbra.languages.factory.scriptEditor.scriptEditor.ScriptEditor`
	Component Interface class exceptions. 

**Others:**

"""

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["AbstractLanguageError", "LanguageGrammarError"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class AbstractLanguageError(foundations.exceptions.AbstractError):
	"""
	This class is the abstract base class for language related exceptions.
	"""

	pass

class LanguageGrammarError(AbstractLanguageError):
	"""
	This class is used for language grammar exceptions.
	"""

	pass
