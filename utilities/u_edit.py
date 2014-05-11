#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**u_edit.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	**Umbra** editing helper module.

**Others:**

"""

from __future__ import unicode_literals

import os
import socket
import sys

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["u_edit"]

COMMAND_TEMPLATE = ["[application.components_manager[\"factory.script_editor\"].load_path(path) for path in {0}]",
					"application.layouts_manager.restore_layout(\"development_centric\")",
					"application.raise_()"]

def u_edit(*args):
	"""
	Edits given paths into Umbra.

	:param \*args: Arguments.
	:type \*args: \*
	:return: Definition success.
	:rtype: bool
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
	u_edit(*sys.argv[1:])
