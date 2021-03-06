#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**processing.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`Processing` class.

**Others:**

"""

from __future__ import unicode_literals

import foundations.exceptions
import foundations.ui.common
import foundations.verbose
import umbra.ui.common
from umbra.globals.ui_constants import UiConstants

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "UI_FILE", "Processing"]

LOGGER = foundations.verbose.install_logger()

UI_FILE = umbra.ui.common.get_resource_path(UiConstants.processing_ui_file)


class Processing(foundations.ui.common.QWidget_factory(ui_file=UI_FILE)):
    """
    Defines the Application processing status bar widget.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initializes the class.

        :param parent: Object parent.
        :type parent: QObject
        :param \*args: Arguments.
        :type \*args: \*
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        super(Processing, self).__init__(parent, *args, **kwargs)

        # --- Setting class attributes. ---
        self.__container = parent

        Processing.__initialize_ui(self)

    @property
    def container(self):
        """
        Property for **self.__container** attribute.

        :return: self.__container.
        :rtype: QObject
        """

        return self.__container

    @container.setter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def container(self, value):
        """
        Setter for **self.__container** attribute.

        :param value: Attribute value.
        :type value: QObject
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

    @container.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def container(self):
        """
        Deleter for **self.__container** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

    def __initialize_ui(self):
        """
        Initializes the Widget ui.
        """

        pass
