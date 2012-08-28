#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**uEdit.py

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	**Umbra** editing helper module.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import os
import socket
import sys

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["uEdit"]

COMMAND_TEMPLATE = ["[application.componentsManager[\"factory.scriptEditor\"].loadPath(path) for path in {0}]",
					"application.layoutsManager.restoreLayout(\"developmentCentric\")",
					"application.raise_()"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
def uEdit(*args):
	"""
	This definition edits given paths into Umbra.

	:param \*args: Arguments. ( \* )
	:return: Definition success. ( Boolean )
	"""

	paths = []
	for path in args:
		if not os.path.exists(path):
			continue

		paths.append(os.path.abspath(path))

	if not paths:
		return

	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connection.connect((socket.gethostbyname(socket.gethostname()), 16384))
	connection.send("{0}<!RE>".format("\n".join(COMMAND_TEMPLATE).format(paths)))
	connection.close()
	return True

if __name__ == "__main__":
	uEdit(*sys.argv[1:])
