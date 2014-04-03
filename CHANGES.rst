**Umbra** - 1.0.9 - Stable
==========================

.. .changes

Changes
=======

1.0.9 - Stable
--------------

| **Umbra** 1.0.9 - Stable - Milestone: https://github.com/KelSolaar/Umbra/issues?milestone=10&state=closed
| **Manager** 2.0.5 - Stable - Milestone: https://github.com/KelSolaar/Manager/issues?milestone=4&state=closed
| **Foundations** 2.1.0 - Stable - Milestone: https://github.com/KelSolaar/Foundations/issues?milestone=8&page=1&state=closed

-  Handled potential **IOError** exceptions related to **foundations.common.foundations.common.isBinaryFile** definition usage when accessing a locked file.
-  Prevented exception reports stacking.
-  Prevented **AttributeError** exception in **umbra.components.scriptEditor.scriptEditor.ScriptEditor.__editor__modificationChanged** method.
-  Prevented files reloading on exit in **scriptEditor** component.
-  Fixed **notificationsManager** notifiers insertion order.
-  Fixed caching issue in **foundations.parsers.SectionsFileParser.write** method.
-  Handled **BadZipfile** exception in **foundations.pkzip.Pkzip.extractZipFile** method.
-  Ensured **notificationsManager** has a maximum number of displayed notifiers at same time.
-  Ensured **foundations.parsers.SectionsFileParser.parse** method reads current file content if no content has been previously set.
-  Ensured that loggers and their formatters receive unicode data. 
-  Removed dependency on **ordereddict** for Python versions that already include it.
-  Moved **foundations.common.isBinaryFile** definition into **foundations.io** module.
-  Added **foundations.shell.** module.
-  Extracted documentation utilities to their own repository.
-  Pass various globals variables through arguments in **umbra.engine.Umbra** class.
-  Refactored magic methods implementation in various managers.
-  Implemented **get** method in various managers.
-  Implemented **__setitem__** method in various managers.
-  Implemented magic methods tests for **foundations.parsers.SectionsFileParser** class.
-  Implemented **foundations.parsers.SectionsFileParser.setValue** method.
-  Implemented support for **ANSI** escape codes.
-  Implemented new documentation theme.
-  Reformatted package docstrings.
-  Verbosed **PyQt** version on startup.

1.0.8 - Stable
--------------

| **Umbra** 1.0.8 - Stable - Milestone: https://github.com/KelSolaar/Umbra/issues?milestone=9&state=closed
| **Manager** 2.0.4 - Stable - Milestone: https://github.com/KelSolaar/Manager/issues?milestone=3&state=open
| **Foundations** 2.0.8 - Stable - Milestone: https://github.com/KelSolaar/Foundations/issues?milestone=6&state=closed

-  Implemented better unicode support.

1.0.7 - Stable
--------------

| **Umbra** 1.0.7 - Stable - Milestone: https://github.com/KelSolaar/Umbra/issues?milestone=8&state=closed
| **Foundations** 2.0.7 - Stable - Milestone: https://github.com/KelSolaar/Foundations/issues?milestone=5&state=closed

-  Improved symbols expanding behavior in **Script Editor** Component.
-  Improved various dialog button sizes.
-  Handled **gaierror** exception in **Tcp Client** Component.
-  Fixed **Script Editor** Component **Save File As** action unexpected behavior.
-  Fixed **Script Editor** Component **searchAndReplace** replace method.
-  Fixed slowdown when switching editor in **Script Editor** Component.
-  Fixed symbols matching in **Script Editor** Component.
-  Fixed **socket** module related exceptions in **foundations.common.isInternetAvailable** definition.
-  Handled non existing files and directories in **foundations.pkzip.Pkzip.extract** method.

1.0.6 - Stable
--------------

| **Umbra** 1.0.6 - Stable - Milestone: https://github.com/KelSolaar/Umbra/issues?milestone=7&state=closed
| **Foundations** 2.0.6 - Stable - Milestone: https://github.com/KelSolaar/Foundations/issues?milestone=4&page=1&state=closed

-  Ensured **Reporter** is not initialising the "Crittercism" Client API 2 times.
-  Fixed **Search And Replace** dialog patterns related exception.

1.0.5 - Stable
--------------

| **Umbra** 1.0.5 - Stable - Milestone: https://github.com/KelSolaar/Umbra/issues?milestone=5&state=closed
| **Foundations** 2.0.5 - Stable - Milestone: https://github.com/KelSolaar/Foundations/issues?milestone=3&state=closed

-  Fixed the encoding related issues preventing **sIBL_GUI** to work properly.

1.0.4 - Stable
--------------

| **Umbra** 1.0.4 - Stable - Milestone: https://github.com/KelSolaar/Umbra/issues?milestone=4&state=closed
| **Manager** 2.0.3 - Stable - https://github.com/KelSolaar/Manager/issues?milestone=2&state=closed
| **Foundations** 2.0.4 - Stable - Milestone: https://github.com/KelSolaar/Foundations/issues?milestone=2&state=closed

-  Implemented an unhandled exceptions **Reporter** connected to https://www.crittercism.com/
-  Implemented **Trace Ui** Component.
-  Reloading a Component will reload its dependencies in **Components Manager Ui** Component.
-  Implemented command line support for modules execution tracing through **-t, --traceModules** parameter.
-  Implemented support for per instance logging file.
-  Views display user friendly default message.
-  Fixed various widgets classes, implemented small ui test cases.
-  Fixed inconsistent Ui startup verbose level.
-  Components are properly displayed in **Components Manager Ui** Component.

1.0.3 - Stable
--------------

| **Umbra** 1.0.3 - Stable - Milestone: https://github.com/KelSolaar/Umbra/issues?milestone=3&state=closed
| **Manager** 2.0.2 - Stable - https://github.com/KelSolaar/Manager/issues?milestone=1&state=closed
| **Foundations** 2.0.3 - Stable - https://github.com/KelSolaar/Foundations/issues?milestone=1&state=closed

-  Added support for **Python 2.6**.

1.0.2 - Stable
--------------

**Umbra** 1.0.2 - Stable - Milestone: https://github.com/KelSolaar/Umbra/issues?milestone=2&state=closed

-  Updated package directory structure to be compliant with **Python Package Index**.
-  Added documentation / Api files.
-  Implemented **TCP Server Ui** Component.
-  Implemented **Script Editor** Component file revert.
-  Implemented **script Editor** Component session store / restore.
-  Implemented **script Editor** Component project management through **Projects Explorer** Component.
-  Implemented a generic **fileSystemWatcher** class. 
-  Loading a file in the **Script Editor** Component open the file browser at the current editor location.
-  **Search In Files** / **Search And Replace** dialogs search QComboBox have their text selected on dialog open.
-  Multiples files can be loaded at same time in **Script Editor** Component.
-  Ensure **messageBox** dialogs are centered on screen by default.
-  Fix issue where closing a tab in **Script Editor** Component may trigger closing of the next tab.
-  Fix various other **Script Editor** issues: https://github.com/KelSolaar/Umbra/issues?labels=Defect&milestone=2&page=1&state=closed

1.0.1 - Beta
------------

**Umbra** 1.0.1 - Beta - Milestone: https://github.com/KelSolaar/Umbra/issues?milestone=1&state=closed

-  Implemented notifications manager code.
-  Implemented **Search In Files** in **Script Editor** Component.
-  Implemented matching symbols pairs highlighting in **Script Editor** Component.
-  Implemented occurences highlighting in **Script Editor** Component.
-  Implemented **Duplicate Line(s)** methods in **Script Editor** Component.
-  Implemented **Delete Line(s)** methods in **Script Editor** Component.
-  Implemented **Move Up / Down** methods in **Script Editor** Component.
-  Implemented **Font Size Increase / Decrease** methods in **Script Editor** Component.
-  Refactored the layouts management code.
-  Added support for command line files arguments.

1.0.0 - Alpha
-------------

-  Initial release of **Umbra**.

.. .about

About
-----

| **Umbra** by Thomas Mansencal – 2010 - 2014
| Copyright © 2010 - 2014 – Thomas Mansencal – `thomas.mansencal@gmail.com <mailto:thomas.mansencal@gmail.com>`_
| This software is released under terms of GNU GPL V3 license: http://www.gnu.org/licenses/
| `http://www.thomasmansencal.com/ <http://www.thomasmansencal.com/>`_
