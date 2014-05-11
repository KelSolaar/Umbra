#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**ui_constants.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines **Umbra** package ui constants through the :class:`UiConstants` class.

**Others:**

"""

from __future__ import unicode_literals

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["UiConstants"]

class UiConstants():
    """
    Defines **Umbra** package ui constants.
    """

    ui_file = "Umbra.ui"
    """
    :param ui_file: Application ui file.
    :type ui_file: unicode
    """

    processing_ui_file = "Processing.ui"
    """
    :param processing_ui_file: Processing ui file.
    :type processing_ui_file: unicode
    """
    reporter_ui_file = "Reporter.ui"
    """
    :param reporter_ui_file: Reporter ui file.
    :type reporter_ui_file: unicode
    """

    windows_stylesheet_file = "styles/Windows_styleSheet.qss"
    """
    :param windows_stylesheet_file: Application Windows Os stylesheet file.
    :type windows_stylesheet_file: unicode
    """
    darwin_stylesheet_file = "styles/Darwin_styleSheet.qss"
    """
    :param darwin_stylesheet_file: Application Mac Os X Os stylesheet file.
    :type darwin_stylesheet_file: unicode
    """
    linux_stylesheet_file = "styles/Linux_styleSheet.qss"
    """
    :param linux_stylesheet_file: Application Linux Os stylesheet file.
    :type linux_stylesheet_file: unicode
    """
    windows_full_screen_stylesheet_file = "styles/Windows_FullScreen_styleSheet.qss"
    """
    :param windows_full_screen_stylesheet_file: Application Windows Os fullscreen stylesheet file.
    :type windows_full_screen_stylesheet_file: unicode
    """
    darwin_full_screen_stylesheet_file = "styles/Darwin_FullScreen_styleSheet.qss"
    """
    :param darwin_full_screen_stylesheet_file: Application Mac Os X Os fullscreen stylesheet file.
    :type darwin_full_screen_stylesheet_file: unicode
    """
    linux_full_screen_stylesheet_file = "styles/Linux_FullScreen_styleSheet.qss"
    """
    :param linux_full_screen_stylesheet_file: Application Linux Os fullscreen stylesheet file.
    :type linux_full_screen_stylesheet_file: unicode
    """
    windows_style = "plastique"
    """
    :param windows_style: Application Windows Os style.
    :type windows_style: unicode
    """
    darwin_style = "plastique"
    """
    :param darwin_style: Application Mac Os X Os style.
    :type darwin_style: unicode
    """
    linux_style = "plastique"
    """
    :param linux_style: Application Linux Os style.
    :type linux_style: unicode
    """

    settings_file = "preferences/Default_Settings.rc"
    """
    :param settings_file: Application defaults settings file.
    :type settings_file: unicode
    """

    layouts_file = "layouts/Default_Layouts.rc"
    """
    :param layouts_file: Application defaults layouts file.
    :type layouts_file: unicode
    """

    application_windows_icon = "images/Icon_Dark.png"
    """
    :param application_windows_icon: Application icon file.
    :type application_windows_icon: unicode
    """

    splash_screen_image = "images/Umbra_SpashScreen.png"
    """
    :param splash_screen_image: Application splashscreen image.
    :type splash_screen_image: unicode
    """
    logo_image = "images/Umbra_Logo.png"
    """
    :param logo_image: Application logo image.
    :type logo_image: unicode
    """

    default_toolbar_icon_size = 32
    """
    :param default_toolbar_icon_size: Application toolbar icons size.
    :type default_toolbar_icon_size: int
    """

    custom_layouts_icon = "images/Custom_Layouts.png"
    """
    :param custom_layouts_icon: Application **Custom Layouts** icon.
    :type custom_layouts_icon: unicode
    """
    custom_layouts_hover_icon = "images/Custom_Layouts_Hover.png"
    """
    :param custom_layouts_hover_icon: Application **Custom Layouts** hover icon.
    :type custom_layouts_hover_icon: unicode
    """
    custom_layouts_active_icon = "images/Custom_Layouts_Active.png"
    """
    :param custom_layouts_active_icon: Application **Custom Layouts** active icon.
    :type custom_layouts_active_icon: unicode
    """

    miscellaneous_icon = "images/Miscellaneous.png"
    """
    :param miscellaneous_icon: Application **Miscellaneous** icon.
    :type miscellaneous_icon: unicode
    """
    miscellaneous_hover_icon = "images/Miscellaneous_Hover.png"
    """
    :param miscellaneous_hover_icon: Application **Miscellaneous** hover icon.
    :type miscellaneous_hover_icon: unicode
    """
    miscellaneous_active_icon = "images/Miscellaneous_Active.png"
    """
    :param miscellaneous_active_icon: Application **Miscellaneous** active icon.
    :type miscellaneous_active_icon: unicode
    """

    development_icon = "images/Development.png"
    """
    :param development_icon: Application **Development** icon.
    :type development_icon: unicode
    """
    development_hover_icon = "images/Development_Hover.png"
    """
    :param development_hover_icon: Application **Development** hover icon.
    :type development_hover_icon: unicode
    """
    development_active_icon = "images/Development_Active.png"
    """
    :param development_active_icon: Application **Development** active icon.
    :type development_active_icon: unicode
    """

    preferences_icon = "images/Preferences.png"
    """
    :param preferences_icon: Application **Preferences** icon.
    :type preferences_icon: unicode
    """
    preferences_hover_icon = "images/Preferences_Hover.png"
    """
    :param preferences_hover_icon: Application **Preferences** hover icon.
    :type preferences_hover_icon: unicode
    """
    preferences_active_icon = "images/Preferences_Active.png"
    """
    :param preferences_active_icon: Application **Preferences** active icon.
    :type preferences_active_icon: unicode
    """

    startup_layout = "startup_centric"
    """
    :param startup_layout: Application startup layout.
    :type startup_layout: unicode
    """

    help_file = "http://thomasmansencal.com/Sharing/Umbra/Support/Documentation/Help/Umbra_Manual.html"
    """
    :param help_file: Application online help file.
    :type help_file: unicode
    """
    api_file = "http://thomasmansencal.com/Sharing/Umbra/Support/Documentation/Api/index.html"
    """
    :param api_file: Application online Api file.
    :type api_file: unicode
    """

    development_layout = "development_centric"
    """
    :param development_layout: Application development layout.
    :type development_layout: unicode
    """

    python_grammar_file = "grammars/Python/Python.grc"
    """
    :param python_grammar_file: Python language grammar file.
    :type python_grammar_file: unicode
    """
    logging_grammar_file = "grammars/Logging/Logging.grc"
    """
    :param logging_grammar_file: Logging language grammar file.
    :type logging_grammar_file: unicode
    """
    text_grammar_file = "grammars/Text/Text.grc"
    """
    :param text_grammar_file: Text language grammar file.
    :type text_grammar_file: unicode
    """

    invalid_link_html_file = "htmls/Invalid_Link.html"
    """
    :param invalid_link_html_file: Invalid link html file.
    :type invalid_link_html_file: unicode
    """

    crittercism_id = "5075c158d5f9b9796b000002"
    """
    :param crittercism_id: Crittercism Id.
    :type crittercism_id: unicode
    """
