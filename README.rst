Umbra
=====

Introduction
------------

Umbra is the main package of `sIBL_GUI <http://github.com/KelSolaar/sIBL_GUI>`_ and `sIBL_Reporter <http://github.com/KelSolaar/sIBL_Reporter>`_.

Installation
------------

Umbra depends on some other packages / repositories:
-  Foundations package available from Github: https://github.com/KelSolaar/Foundations. You will need to create a symbolic link from "Foundations/src/foundations" to "Umbra/src/foundations" and from "Foundations/src/tests/testsFoundations" to "Umbra/src/tests/testsFoundations" or ensure the packages are available in Python path.
-  Manager package available from Github: https://github.com/KelSolaar/Manager. You will need to create a symbolic link from "Manager/src/manager" to "Umbra/src/manager" and from "Manager/src/tests/testsManager" to "Umbra/src/tests/testsManager" or ensure the packages are available in Python path.

Quick Repositories Cloning Commands::

   mkdir HDRLabs
   cd HDRLabs/
   git clone git://github.com/KelSolaar/Umbra.git && git clone git://github.com/KelSolaar/Foundations.git &&  git clone git://github.com/KelSolaar/Manager.git
   cd Umbra/src
   python Umbra.py

Usage
-----

About
-----

| **Umbra** by Thomas Mansencal – 2010 - 2012
| Copyright© 2010 - 2012 – Thomas Mansencal – `thomas.mansencal@gmail.com <mailto:thomas.mansencal@gmail.com>`_
| This software is released under terms of GNU GPL V3 license: http://www.gnu.org/licenses/
| `http://www.thomasmansencal.com/ <http://www.thomasmansencal.com/>`_