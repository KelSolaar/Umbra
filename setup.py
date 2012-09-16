import re
from setuptools import setup
from setuptools import find_packages

import umbra.globals.constants

def getLongDescription():
	"""
	This definition returns the Package long description.

	:return: Package long description. ( String )
	"""

	description = []
	with open("README.rst") as file:
		for line in file:
			if ".. code:: python" in line and len(description) >= 2:
				blockLine = description[-2]
				if re.search(r":$", blockLine) and not re.search(r"::$", blockLine):
					description[-2] = "::".join(blockLine.rsplit(":", 1))
				continue

			description.append(line)
	return str().join(description)

setup(name=umbra.globals.constants.Constants.applicationName,
	version=umbra.globals.constants.Constants.releaseVersion,
	author=umbra.globals.constants.__author__,
	author_email=umbra.globals.constants.__email__,
	include_package_data=True,
	packages=find_packages(),
	scripts=["bin/Umbra"],
	url="https://github.com/KelSolaar/Umbra",
	license="GPLv3",
	description="Umbra is the main package of sIBL_GUI and sIBL_Reporter.",
	long_description=getLongDescription(),
	install_requires=["sphinx>=1.1.3", "Foundations>=2.0.2", "Manager>=2.0.1"],
	classifiers=["Development Status :: 5 - Production/Stable",
				"Environment :: Console",
				"Environment :: MacOS X",
				"Intended Audience :: Developers",
				"Environment :: Win32 (MS Windows)",
				"Environment :: X11 Applications :: Qt",
				"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
				"Natural Language :: English",
				"Operating System :: OS Independent",
				"Programming Language :: Python :: 2.7",
				"Topic :: Utilities"])
