#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**uiConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines **Umbra** package ui constants through the :class:`UiConstants` class.

**Others:**

"""

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["UiConstants"]

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class UiConstants():
	"""
	This class provides **Umbra** package ui constants.
	"""

	uiFile = "Umbra.ui"
	"""Application ui file: '**Umbra.ui**' ( String )"""

	processingUiFile = "Processing.ui"
	"""Processing ui file: '**Processing.ui**' ( String )"""

	windowsStylesheetFile = "styles/Windows_styleSheet.qss"
	"""Application Windows Os stylesheet file: '**styles/Windows_styleSheet.qss**' ( String )"""
	darwinStylesheetFile = "styles/Darwin_styleSheet.qss"
	"""Application Mac Os X Os stylesheet file: '**styles/Darwin_styleSheet.qss**' ( String )"""
	linuxStylesheetFile = "styles/Linux_styleSheet.qss"
	"""Application Linux Os stylesheet file: '**styles/Linux_styleSheet.qss**' ( String )"""
	windowsFullScreenStylesheetFile = "styles/Windows_FullScreen_styleSheet.qss"
	"""Application Windows Os fullscreen stylesheet file: '**styles/Windows_FullScreen_styleSheet.qss**' ( String )"""
	darwinFullScreenStylesheetFile = "styles/Darwin_FullScreen_styleSheet.qss"
	"""Application Mac Os X Os fullscreen stylesheet file: '**styles/Darwin_FullScreen_styleSheet.qss**' ( String )"""
	linuxFullScreenStylesheetFile = "styles/Linux_FullScreen_styleSheet.qss"
	"""Application Linux Os fullscreen stylesheet file: '**styles/Linux_FullScreen_styleSheet.qss**' ( String )"""
	windowsStyle = "plastique"
	"""Application Windows Os style: '**plastique**' ( String )"""
	darwinStyle = "plastique"
	"""Application Mac Os X Os style: '**plastique**' ( String )"""
	linuxStyle = "plastique"
	"""Application Linux Os style: '**plastique**' ( String )"""

	settingsFile = "preferences/Default_Settings.rc"
	"""Application defaults settings file: '**preferences/Default_Settings.rc**' ( String )"""

	layoutsFile = "layouts/Default_Layouts.rc"
	"""Application defaults layouts file: '**layouts/Default_Layouts.rc**' ( String )"""

	applicationWindowsIcon = "images/Icon_Dark.png"
	"""Application Windows Os icon file: '**images/Icon_Dark.png**' ( String )"""
	applicationDarwinIcon = "images/Icon_Dark.png"
	"""Application Mac Os X icon file: '**images/Icon_Dark.png**' ( String )"""

	splashScreenImage = "images/Umbra_SpashScreen.png"
	"""Application splashscreen image: '**images/Umbra_SpashScreen.png**' ( String )"""
	logoImage = "images/Umbra_Logo.png"
	"""Application logo image: '**images/Umbra_Logo.png**' ( String )"""

	defaultToolbarIconSize = 32
	"""Application toolbar icons size: '**32**' ( Integer )"""

	customLayoutsIcon = "images/Custom_Layouts.png"
	"""Application **Custom Layouts** icon: '**images/Custom_Layouts.png**' ( String )"""
	customLayoutsHoverIcon = "images/Custom_Layouts_Hover.png"
	"""Application **Custom Layouts** hover icon: '**images/Custom_Layouts_Hover.png**' ( String )"""
	customLayoutsActiveIcon = "images/Custom_Layouts_Active.png"
	"""Application **Custom Layouts** active icon: '**images/Custom_Layouts_Active.png**' ( String )"""

	miscellaneousIcon = "images/Miscellaneous.png"
	"""Application **Miscellaneous** icon: '**images/Miscellaneous.png**' ( String )"""
	miscellaneousHoverIcon = "images/Miscellaneous_Hover.png"
	"""Application **Miscellaneous** hover icon: '**images/Miscellaneous_Hover.png**' ( String )"""
	miscellaneousActiveIcon = "images/Miscellaneous_Active.png"
	"""Application **Miscellaneous** active icon: '**images/Miscellaneous_Active.png**' ( String )"""

	developmentIcon = "images/Development.png"
	"""Application **Development** icon: '**images/Development.png**' ( String )"""
	developmentHoverIcon = "images/Development_Hover.png"
	"""Application **Development** hover icon: '**images/Development_Hover.png**' ( String )"""
	developmentActiveIcon = "images/Development_Active.png"
	"""Application **Development** active icon: '**images/Development_Active.png**' ( String )"""

	preferencesIcon = "images/Preferences.png"
	"""Application **Preferences** icon: '**images/Preferences.png**' ( String )"""
	preferencesHoverIcon = "images/Preferences_Hover.png"
	"""Application **Preferences** hover icon: '**images/Preferences_Hover.png**' ( String )"""
	preferencesActiveIcon = "images/Preferences_Active.png"
	"""Application **Preferences** active icon: '**images/Preferences_Active.png**' ( String )"""

	startupLayout = "startupCentric"
	"""Application startup layout: '**startupCentric**' ( String )"""

	helpFile = "https://github.com/KelSolaar/Umbra"
	"""Application online help file: '**"https://github.com/KelSolaar/Umbra"**' ( String )"""
	apiFile = "https://github.com/KelSolaar/Umbra"
	"""Application online Api file: '**"https://github.com/KelSolaar/Umbra"**' ( String )"""

	developmentLayout = "developmentCentric"
	"""Application development layout: '**"developmentCentric"**' ( String )"""

	pythonGrammarFile = "grammars/Python/Python.grc"
	"""Python language grammar file: '**grammars/Python/Python.grc**' ( String )"""
	loggingGrammarFile = "grammars/Logging/Logging.grc"
	"""Logging language grammar file: '**grammars/Logging/Logging.grc**' ( String )"""
	textGrammarFile = "grammars/Text/Text.grc"
	"""Text language grammar file: '**grammars/Text/Text.grc**' ( String )"""
