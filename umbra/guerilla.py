#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**guerilla.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines various guerilla / monkey patching objects.

**Others:**
	Portions of the code by Guido Van Rossum: http://mail.python.org/pipermail/python-dev/2008-January/076194.html
"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.common

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "attributeWarfare", "baseWarfare"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def attributeWarfare(object):
	"""
	Alterates object attributes using guerilla / monkey patching.
	
	:param object: Object to alterate. ( Object )
	:return: Object. ( Object )
	"""

	def attributeWarfareWrapper(attribute):
		"""
		Alterates object attributes using guerilla / monkey patching.
		
		:param attribute: Attribute to alterate. ( Object )
		:return: Object. ( Object )
		"""

		setattr(object, attribute.__name__, attribute)
		return attribute

	return attributeWarfareWrapper

def baseWarfare(name, bases, attributes):
	"""
	Adds any number of attributes to an existing class.
	
	:param name: Name. ( String )
	:param bases: Bases. ( List )
	:param attributes: Attributes. ( Dictionary )
	:return: Base. ( Object )
	"""

	assert len(bases) == 1, "{0} | '{1}' object has multiple bases!".format(__name__, name)

	base = foundations.common.getFirstItem(bases)
	for name, value in attributes.iteritems():
		if name != "__metaclass__":
			setattr(base, name, value)
	return base
