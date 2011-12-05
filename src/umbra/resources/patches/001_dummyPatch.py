#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**001_dummyPatch.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module is a dummy patch provided as an example file.

**Others:**

"""

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2011 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["UID", "apply"]

UID = "6476c4d6da7ea194cc25a6b4b5efb06f"

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def apply():
	"""
	This definition is called by the Application and triggers the patch execution.
	:return: Definition success. ( Boolean )
	"""

	return True
