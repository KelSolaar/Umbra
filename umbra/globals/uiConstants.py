#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**uiConstants.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines **Umbra** package ui constants through the :class:`UiConstants` class.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Defines **Umbra** package ui constants.
	"""

	uiFile = "Umbra.ui"
	"""
	:param uiFile: Application ui file.
	:type uiFile: unicode
	"""

	processingUiFile = "Processing.ui"
	"""
	:param processingUiFile: Processing ui file.
	:type processingUiFile: unicode
	"""
	reporterUiFile = "Reporter.ui"
	"""
	:param reporterUiFile: Reporter ui file.
	:type reporterUiFile: unicode
	"""

	windowsStylesheetFile = "styles/Windows_styleSheet.qss"
	"""
	:param windowsStylesheetFile: Application Windows Os stylesheet file.
	:type windowsStylesheetFile: unicode
	"""
	darwinStylesheetFile = "styles/Darwin_styleSheet.qss"
	"""
	:param darwinStylesheetFile: Application Mac Os X Os stylesheet file.
	:type darwinStylesheetFile: unicode
	"""
	linuxStylesheetFile = "styles/Linux_styleSheet.qss"
	"""
	:param linuxStylesheetFile: Application Linux Os stylesheet file.
	:type linuxStylesheetFile: unicode
	"""
	windowsFullScreenStylesheetFile = "styles/Windows_FullScreen_styleSheet.qss"
	"""
	:param windowsFullScreenStylesheetFile: Application Windows Os fullscreen stylesheet file.
	:type windowsFullScreenStylesheetFile: unicode
	"""
	darwinFullScreenStylesheetFile = "styles/Darwin_FullScreen_styleSheet.qss"
	"""
	:param darwinFullScreenStylesheetFile: Application Mac Os X Os fullscreen stylesheet file.
	:type darwinFullScreenStylesheetFile: unicode
	"""
	linuxFullScreenStylesheetFile = "styles/Linux_FullScreen_styleSheet.qss"
	"""
	:param linuxFullScreenStylesheetFile: Application Linux Os fullscreen stylesheet file.
	:type linuxFullScreenStylesheetFile: unicode
	"""
	windowsStyle = "plastique"
	"""
	:param windowsStyle: Application Windows Os style.
	:type windowsStyle: unicode
	"""
	darwinStyle = "plastique"
	"""
	:param darwinStyle: Application Mac Os X Os style.
	:type darwinStyle: unicode
	"""
	linuxStyle = "plastique"
	"""
	:param linuxStyle: Application Linux Os style.
	:type linuxStyle: unicode
	"""

	settingsFile = "preferences/Default_Settings.rc"
	"""
	:param settingsFile: Application defaults settings file.
	:type settingsFile: unicode
	"""

	layoutsFile = "layouts/Default_Layouts.rc"
	"""
	:param layoutsFile: Application defaults layouts file.
	:type layoutsFile: unicode
	"""

	applicationWindowsIcon = "images/Icon_Dark.png"
	"""
	:param applicationWindowsIcon: Application icon file.
	:type applicationWindowsIcon: unicode
	"""

	splashScreenImage = "images/Umbra_SpashScreen.png"
	"""
	:param splashScreenImage: Application splashscreen image.
	:type splashScreenImage: unicode
	"""
	logoImage = "images/Umbra_Logo.png"
	"""
	:param logoImage: Application logo image.
	:type logoImage: unicode
	"""

	defaultToolbarIconSize = 32
	"""
	:param defaultToolbarIconSize: Application toolbar icons size.
	:type defaultToolbarIconSize: int
	"""

	customLayoutsIcon = "images/Custom_Layouts.png"
	"""
	:param customLayoutsIcon: Application **Custom Layouts** icon.
	:type customLayoutsIcon: unicode
	"""
	customLayoutsHoverIcon = "images/Custom_Layouts_Hover.png"
	"""
	:param customLayoutsHoverIcon: Application **Custom Layouts** hover icon.
	:type customLayoutsHoverIcon: unicode
	"""
	customLayoutsActiveIcon = "images/Custom_Layouts_Active.png"
	"""
	:param customLayoutsActiveIcon: Application **Custom Layouts** active icon.
	:type customLayoutsActiveIcon: unicode
	"""

	miscellaneousIcon = "images/Miscellaneous.png"
	"""
	:param miscellaneousIcon: Application **Miscellaneous** icon.
	:type miscellaneousIcon: unicode
	"""
	miscellaneousHoverIcon = "images/Miscellaneous_Hover.png"
	"""
	:param miscellaneousHoverIcon: Application **Miscellaneous** hover icon.
	:type miscellaneousHoverIcon: unicode
	"""
	miscellaneousActiveIcon = "images/Miscellaneous_Active.png"
	"""
	:param miscellaneousActiveIcon: Application **Miscellaneous** active icon.
	:type miscellaneousActiveIcon: unicode
	"""

	developmentIcon = "images/Development.png"
	"""
	:param developmentIcon: Application **Development** icon.
	:type developmentIcon: unicode
	"""
	developmentHoverIcon = "images/Development_Hover.png"
	"""
	:param developmentHoverIcon: Application **Development** hover icon.
	:type developmentHoverIcon: unicode
	"""
	developmentActiveIcon = "images/Development_Active.png"
	"""
	:param developmentActiveIcon: Application **Development** active icon.
	:type developmentActiveIcon: unicode
	"""

	preferencesIcon = "images/Preferences.png"
	"""
	:param preferencesIcon: Application **Preferences** icon.
	:type preferencesIcon: unicode
	"""
	preferencesHoverIcon = "images/Preferences_Hover.png"
	"""
	:param preferencesHoverIcon: Application **Preferences** hover icon.
	:type preferencesHoverIcon: unicode
	"""
	preferencesActiveIcon = "images/Preferences_Active.png"
	"""
	:param preferencesActiveIcon: Application **Preferences** active icon.
	:type preferencesActiveIcon: unicode
	"""

	startupLayout = "startupCentric"
	"""
	:param startupLayout: Application startup layout.
	:type startupLayout: unicode
	"""

	helpFile = "http://thomasmansencal.com/Sharing/Umbra/Support/Documentation/Help/Umbra_Manual.html"
	"""
	:param helpFile: Application online help file.
	:type helpFile: unicode
	"""
	apiFile = "http://thomasmansencal.com/Sharing/Umbra/Support/Documentation/Api/index.html"
	"""
	:param apiFile: Application online Api file.
	:type apiFile: unicode
	"""

	developmentLayout = "developmentCentric"
	"""
	:param developmentLayout: Application development layout.
	:type developmentLayout: unicode
	"""

	pythonGrammarFile = "grammars/Python/Python.grc"
	"""
	:param pythonGrammarFile: Python language grammar file.
	:type pythonGrammarFile: unicode
	"""
	loggingGrammarFile = "grammars/Logging/Logging.grc"
	"""
	:param loggingGrammarFile: Logging language grammar file.
	:type loggingGrammarFile: unicode
	"""
	textGrammarFile = "grammars/Text/Text.grc"
	"""
	:param textGrammarFile: Text language grammar file.
	:type textGrammarFile: unicode
	"""

	invalidLinkHtmlFile = "htmls/Invalid_Link.html"
	"""
	:param invalidLinkHtmlFile: Invalid link html file.
	:type invalidLinkHtmlFile: unicode
	"""

	crittercismId = "51290b63421c983d17000490"
	"""
	:param crittercismId: Crittercism Id.
	:type crittercismId: unicode
	"""
