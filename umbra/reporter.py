#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**reporter.py**

**Platform:**
    Windows, Linux, Mac Os X.

**Description:**
    Defines the :class:`Reporter` class and various others exceptions handling related objects.

**Others:**

"""

from __future__ import unicode_literals

import functools
import inspect
import os
import platform
import re
import sys

if sys.version_info[:2] <= (2, 6):
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict
import time
import traceback
from PyQt4.QtGui import QApplication

import foundations.core
import foundations.exceptions
import foundations.io
import foundations.verbose
import foundations.strings
import foundations.ui.common
import umbra.ui.common
from umbra.globals.constants import Constants
from umbra.globals.ui_constants import UiConstants
from umbra.globals.runtime_globals import RuntimeGlobals

__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
           "UI_FILE",
           "Reporter",
           "base_exception_handler",
           "system_exit_exception_handler"
           "critical_exception_handler",
           "install_exception_reporter",
           "uninstall_exception_reporter",
           "enable_exception_reporter",
           "disable_exception_reporter"]

LOGGER = foundations.verbose.install_logger()

UI_FILE = umbra.ui.common.get_resource_path(UiConstants.reporter_ui_file)


class Reporter(foundations.ui.common.QWidget_factory(ui_file=UI_FILE)):
    """
    Defines an exception reporting Widget.
    """

    __instance = None
    """
    :param __instance: Class instance.
    :type __instance: Reporter
    """

    def __new__(cls, *args, **kwargs):
        """
        Constructor of the class.

        :param \*args: Arguments.
        :type \*args: \*
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        :return: Class instance.
        :rtype: Library
        """

        if not cls._Reporter__instance:
            cls._Reporter__instance = super(Reporter, cls).__new__(cls, *args, **kwargs)
        return cls._Reporter__instance

    def __init__(self, parent=None, report=True, enabled=True, *args, **kwargs):
        """
        Initializes the class.

        :param parent: Object parent.
        :type parent: QObject
        :param report: Report to Crittercism.
        :type report: bool
        :param enabled: Is reporter enabled.
        :type enabled: bool
        :param \*args: Arguments.
        :type \*args: \*
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        if hasattr(self, "_Reporter__initialized"):
            return

        LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

        super(Reporter, self).__init__(parent, *args, **kwargs)

        # --- Setting class attributes. ---
        self.__initialized = True

        self.__report = None
        self.report = report
        self.__enabled = None
        self.enabled = enabled

        self.__jquery_javascript_path = umbra.ui.common.get_resource_path(os.path.join("javascripts", "jquery.js"))
        self.__crittercism_javascript_path = umbra.ui.common.get_resource_path(
            os.path.join("javascripts", "crittercism.js"))
        self.__reporter_javascript_path = umbra.ui.common.get_resource_path(os.path.join("javascripts", "reporter.js"))
        self.__jquery_javascript = foundations.io.File(self.__jquery_javascript_path).read()
        self.__crittercism_javascript = foundations.io.File(self.__crittercism_javascript_path).read()
        self.__reporter_javascript = foundations.io.File(self.__reporter_javascript_path).read().format(
            UiConstants.crittercism_id, Constants.version)

        self.__style = """* {
                            margin: 0;
                            padding: 0;
                        }

                        ::-webkit-scrollbar {
                            height: 12px;
                            width: 12px;
                        }

                        ::-webkit-scrollbar-track-piece  {
                            background-color: rgb(48, 48, 48);
                        }

                        ::-webkit-scrollbar-thumb:horizontal, ::-webkit-scrollbar-thumb:vertical {
                            background-color: rgb(96, 96, 96);
                        }

                        ::-webkit-scrollbar-thumb:horizontal:hover, ::-webkit-scrollbar-thumb:vertical:hover {
                            background-color: rgb(128, 128, 128);
                        }

                        ::-webkit-scrollbar-thumb:horizontal {
                            width: 50px;
                        }

                        ::-webkit-scrollbar-thumb:vertical {
                            height: 50px;
                        }

                        body {
                            background-color: rgb(32, 32, 32);
                            color: rgb(192, 192, 192);
                            font-size: 12pt;
                            margin: 16px;
                            overflow-y: scroll;
                        }

                        A:link {
                            color: rgb(160, 96, 64);
                            text-decoration: none;
                        }

                        A:visited {
                            text-decoration: none;
                            color: rgb(160, 96, 64);
                        }

                        A:active {
                            text-decoration: none;
                            color: rgb(160, 96, 64);
                        }

                        A:hover {
                            text-decoration: underline;
                            color: rgb(160, 96, 64);
                        }

                        .floatRight {
                            float: right;
                        }

                        .textAlignRight {
                            text-align: right;
                        }

                        div {
                            overflow:hidden;
                            margin: auto;
                            text-overflow: ellipsis;
                            word-wrap: break-word;
                        }

                        div.header {
                            background-color: rgb(210, 64, 32);
                            color: rgb(32, 32, 32);
                            padding: 24px;
                        }

                        div.traceback {
                            background-color: rgb(210, 64, 32);
                            color: rgb(32, 32, 32);
                            font-size: 16px;
                            padding: 16px;
                        }

                        div.content {
                            padding: 16px;
                        }

                        div.stack {
                        }

                        div.location {
                            background-color: rgb(48, 48, 48);
                            font-size: 16px;
                            padding: 8px;
                        }

                        div.context {
                            background-color: rgb(48, 48, 48);
                            color: rgb(160, 160, 160);
                            font-family: "Courier New";
                            font-size: 14px;
                            padding: 32px;

                        }

                        span.highlight {
                            background-color: rgb(160, 96, 64);
                            color: rgb(32, 32, 32);
                            display: block;
                            font-weight: bold;
                        }

                        div.exception {
                            background-color: rgb(210, 64, 32);
                            color: rgb(32, 32, 32);
                            font-size: 16px;
                            padding: 16px;
                        }

                        div.debug {
                            padding: 16px;
                        }

                        div.frame {
                            background-color: rgb(48, 48, 48);
                            padding: 8px;
                        }

                        div.type {
                            font-size: 16px;
                        }

                        div.locals {
                            background-color: rgb(48, 48, 48);
                            color: rgb(160, 160, 160);
                            line-height: 150%;
                            padding: 32px;
                        }"""
        self.__html = None

        self.__onlineText = "An <b>unhandled</b> exception occured, \
this report has been sent to <b>HDRLabs</b> development team!"
        self.__offlineText = "An <b>unhandled</b> exception occured, \
mailing this report to <b>{0}</b> would help improving <b>{1}</b>!".format(__email__, Constants.application_name)
        self.__footerText = \
            "The severity of this exception is not critical and <b>{0}</b> will resume!".format(
                Constants.application_name)

        self.__initialize_ui()

    @property
    def report(self):
        """
        Property for **self.__report** attribute.

        :return: self.__report.
        :rtype: bool
        """

        return self.__report

    @report.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def report(self, value):
        """
        Setter for **self.__report** attribute.

        :param value: Attribute value.
        :type value: bool
        """

        if value is not None:
            assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("report", value)
        self.__report = value

    @report.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def report(self):
        """
        Deleter for **self.__report** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "report"))

    @property
    def enabled(self):
        """
        Property for **self.__enabled** attribute.

        :return: self.__enabled.
        :rtype: bool
        """

        return self.__enabled

    @enabled.setter
    @foundations.exceptions.handle_exceptions(AssertionError)
    def enabled(self, value):
        """
        Setter for **self.__enabled** attribute.

        :param value: Attribute value.
        :type value: bool
        """

        if value is not None:
            assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("enabled", value)
        self.__enabled = value

    @enabled.deleter
    @foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
    def enabled(self):
        """
        Deleter for **self.__enabled** attribute.
        """

        raise foundations.exceptions.ProgrammingError(
            "{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "enabled"))

    def __call__(self, *args):
        """
        Caller of the class.

        :param \*args: Arguments.
        :type \*args: \*
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        :return: Class instance.
        :rtype: Library
        """

        self.handle_exception(*args)

    def show(self):
        """
        Reimplements the :meth:`QWidget.show` method.
        """

        RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.hide()

        super(Reporter, self).show()

        self.raise_()

    def __initialize_ui(self):
        """
        Initializes the Widget ui.
        """

        LOGGER.debug("> Initializing '{0}' Widget ui.".format(self.__class__.__name__))

        self.__view = self.Reporter_webView

        self.setWindowTitle("{0} - Reporter".format(Constants.application_name))
        self.Footer_label.setText(self.__footerText)
        self.__initialize_context_ui()

        self.__set_html()

        # Signals / Slots.
        self.Copy_Report_pushButton.clicked.connect(self.__Copy_Report_pushButton__clicked)
        self.Disable_Reporter_pushButton.clicked.connect(self.__Disable_Reporter_pushButton__clicked)

    def __initialize_context_ui(self):
        """
        Sets the context Widget ui.
        """

        if foundations.common.is_internet_available():
            text = self.__onlineText
        else:
            text = self.__offlineText
        self.Header_label.setText(text)

    def __Copy_Report_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Copy_Report_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        clipboard = QApplication.clipboard()
        clipboard.setText(self.__view.page().mainFrame().toPlainText())

    def __Disable_Reporter_pushButton__clicked(self, checked):
        """
        Defines the slot triggered by **Disable_Reporter_pushButton** Widget when clicked.

        :param checked: Checked state.
        :type checked: bool
        """

        uninstall_exception_reporter()
        self.__enabled = False

    def __get_html(self, body=None):
        """
        Returns the html content with given body tag content.

        :param body: Body tag content.
        :type body: unicode
        :return: Html.
        :rtype: unicode
        """

        output = []
        output.append("<html>")
        output.append("<head>")
        for javascript in (self.__jquery_javascript,
                           self.__crittercism_javascript,
                           self.__reporter_javascript):
            output.append("<script type=\"text/javascript\">")
            output.append(javascript)
            output.append("</script>")
        output.append("<style type=\"text/css\">")
        output.append(self.__style)
        output.append("</style>")
        output.append("</head>")
        if body is not None:
            output.append(body)
        else:
            output.append("<body>")
            output.append("<div id=\"report\">")
            output.append("</div>")
            output.append("</body>")
        output.append("</html>")
        return "\n".join(output)

    def __set_html(self, html=None):
        """
        Sets the html content in the View using given body.

        :param html: Html content.
        :type html: unicode
        """

        self.__html = self.__get_html(html)
        self.__view.setHtml(self.__html)

    def __update_html(self, html):
        """
        Updates the View with given html content.

        :param html: Html content.
        :type html: unicode
        """

        if platform.system() in ("Windows", "Microsoft"):
            html = re.sub(r"((?:[a-zA-Z]\:|\\\\[\w\.]+\\[\w.$]+)\\(?:[\w]+\\)*\w([\w.])+)",
                          lambda x: foundations.strings.to_forward_slashes(x.group(1)),
                          html)

        html = foundations.strings.replace(html, OrderedDict([('"', '\\"'), ("\n", "")]))
        self.__evaluate_javascript("$(\"#report\").html(\"{0}\");".format(html))

    def __evaluate_javascript(self, javascript):
        """
        Evaluates given javascript content in the View.

        :param javascript: Javascript.
        :type javascript: unicode
        """

        self.__view.page().mainFrame().evaluateJavaScript(javascript)

    def handle_exception(self, *args):
        """
        Handles given exception.

        :param \*args: Arguments.
        :type \*args: \*
        """

        if not self.__enabled:
            return

        cls, instance, trcback = foundations.exceptions.extract_exception(*args)

        LOGGER.info("{0} | Handling '{1}' exception!".format(
            self.__class__.__name__, foundations.strings.to_string(cls)))

        self.__initialize_context_ui()

        self.__update_html(self.format_html_exception(cls, instance, trcback))

        self.show()
        self.__report and self.report_exception_to_crittercism(cls, instance, trcback)
        foundations.exceptions.base_exception_handler(cls, instance, trcback)
        self.exec_()

    @staticmethod
    def format_html_exception(*args):
        """
        Formats given exception as an html text.

        :param \*args: Arguments.
        :type \*args: \*
        :return: Exception html text.
        :rtype: unicode
        """

        escape = lambda x: foundations.strings.replace(x,
                                                       OrderedDict([("&", "&amp;"), ("<", "&lt;"), (">", "&gt;")]))
        format = lambda x: foundations.strings.replace(x.expandtabs(8),
                                                       OrderedDict(
                                                           [("\n\n", "\n \n"), ("\n\n", "\n \n"), (" ", "&nbsp;"),
                                                            ("\n", "<br/>\n")]))

        verbose = 10
        cls, instance, trcback = args
        stack = foundations.exceptions.extract_stack(foundations.exceptions.get_inner_most_frame(trcback), verbose)

        python = "Python {0}: {1}".format(sys.version.split()[0], sys.executable)
        date = time.ctime(time.time())

        html = []
        html.append(
            "<div class=\"header\"><span class=\"floatRight textAlignRight\"><h4>{0}<br/>{1}</h4></span><h2>{2}</h2></div>".format(
                python, date, escape(foundations.strings.to_string(cls))))

        html.append("<div class=\"traceback\">")
        for line in foundations.exceptions.format_exception(cls, instance, trcback):
            html.append("{0}<br/>".format(format(escape(line))))
        html.append("</div>")

        html.append("<div class=\"content\">")
        html.append("<p>An unhandled exception occured in <b>{0} {1}</b>! \
                Sequence of calls leading up to the exception, in their occurring order:</p>".format(
            Constants.application_name, Constants.version))
        html.append("<br/>")
        html.append("<div class=\"stack\">")
        for frame, file_name, line_number, name, context, index in stack:
            location = "<b>{0}{1}</b>".format(escape(name) if name != "<module>" else "",
                                              inspect.formatargvalues(*inspect.getargvalues(frame)))
            html.append(
                "<div class=\"location\">File <a href=file://{0}>\"{0}\"</a>, line <b>{1}</b>, in {2}</div><br>".format(
                    file_name, line_number, location))
            html.append("<div class=\"context\">")
            for i, line in enumerate(context):
                if i == index:
                    html.append("<span class=\"highlight\">{0}&nbsp;{1}</span>".format(
                        line_number - index + i, format(line)))
                else:
                    html.append("{0}&nbsp;{1}".format(line_number - index + i, format(line)))
            html.append("</div>")
            html.append("<br/>")
        html.append("</div>")
        html.append("</div>")
        html.append("<div class=\"exception\">")
        for line in traceback.format_exception_only(cls, instance):
            html.append("<b>{0}</b>".format(format(line)))
        html.append("</div>")

        html.append("<div class=\"debug\">")
        html.append("<p>Frames locals by stack ordering, innermost last:</p>")
        for frame, locals in foundations.exceptions.extract_locals(trcback):
            name, file_name, line_number = frame
            html.append(
                "<div class=\"frame\">Frame \"{0}\" in <a href=file://{1}>\"{1}\"</a> file, line <b>{2}</b>:</div>".format(
                    escape(name), file_name, line_number))
            html.append("<br/>")
            html.append("<div class=\"locals\">")
            arguments, nameless_args, keyword_args, locals = locals
            has_arguments, has_locals = any((arguments, nameless_args, keyword_args)), any(locals)
            has_arguments and html.append("<div class=\"cls\"><b>{0}</b></div><ul>".format("Arguments:"))
            for key, value in arguments.iteritems():
                html.append("<li><b>{0}</b> = {1}</li>".format(key, escape(value)))
            for value in nameless_args:
                html.append("<li><b>{0}</b></li>".format(escape(value)))
            for key, value in sorted(keyword_args.iteritems()):
                html.append("<li><b>{0}</b> = {1}</li>".format(key, escape(value)))
            has_arguments and html.append("</ul>")
            has_locals and html.append("<div class=\"cls\"><b>{0}</b></div><ul>".format("Locals:"))
            for key, value in sorted(locals.iteritems()):
                html.append("<li><b>{0}</b> = {1}</li>".format(key, escape(value)))
            has_locals and html.append("</ul>")
            html.append("</div>")
            html.append("<br/>")
        html.append("</div>")

        return "".join(html)

    @staticmethod
    def formatTextException(*args):
        """
        Formats given exception as a text.

        :param \*args: Arguments.
        :type \*args: \*
        :return: Exception text.
        :rtype: unicode
        """

        format = lambda x: re.sub(r"^(\s+)", lambda y: "{0} ".format("." * len(y.group(0))), x.rstrip().expandtabs(4))

        verbose = 10
        cls, instance, trcback = args
        stack = foundations.exceptions.extract_stack(foundations.exceptions.get_inner_most_frame(trcback), verbose)

        text = []
        text.append(foundations.strings.to_string(cls))
        text.append("")

        for line in foundations.exceptions.format_exception(cls, instance, trcback):
            text.append(format("{0}".format(format(line))))
        text.append("")

        text.append("An unhandled exception occured in {0} {1}!".format(Constants.application_name,
                                                                        Constants.version))
        text.append("Sequence of calls leading up to the exception, in their occurring order:")
        text.append("")

        for frame, file_name, line_number, name, context, index in stack:
            location = "{0}{1}".format(name if name != "<module>" else "",
                                       inspect.formatargvalues(*inspect.getargvalues(frame)))
            text.append("File \"{0}\", line {1}, in {2}".format(file_name, line_number, location))
            for i, line in enumerate(context):
                if i == index:
                    text.append(format("\t{0} {1} <===".format(line_number - index + i, format(format(line)))))
                else:
                    text.append(format("\t{0} {1}".format(line_number - index + i, format(format(line)))))
            text.append("")
        for line in traceback.format_exception_only(cls, instance):
            text.append("{0}".format(format(line)))
        text.append("")

        text.append("Frames locals by stack ordering, innermost last:")
        text.append("")
        for frame, locals in foundations.exceptions.extract_locals(trcback):
            name, file_name, line_number = frame
            text.append("Frame \"{0}\" in \"{1}\" file, line {2}:".format(name, file_name, line_number))
            arguments, nameless_args, keyword_args, locals = locals
            has_arguments, has_locals = any((arguments, nameless_args, keyword_args)), any(locals)
            has_arguments and text.append(format("\tArguments:"))
            for key, value in arguments.iteritems():
                text.append(format("\t\t{0} = {1}".format(key, value)))
            for value in nameless_args:
                text.append(format("\t\t{0}".format(value)))
            for key, value in sorted(keyword_args.iteritems()):
                text.append(format("\\tt{0} = {1}".format(key, value)))
            has_locals and text.append(format("\tLocals:"))
            for key, value in sorted(locals.iteritems()):
                text.append(format("\t\t{0} = {1}".format(key, value)))
            text.append("")

        return text

    def report_exception_to_crittercism(self, *args):
        """
        Reports given exception to Crittercism.

        :param \*args: Arguments.
        :type \*args: \*
        :return: Method success.
        :rtype: bool
        """

        if foundations.common.is_internet_available():
            cls, instance, trcback = args

            title = re.escape("".join(map(lambda x: x.strip(), traceback.format_exception_only(cls, instance))))
            file = trcback.tb_frame.f_code.co_filename
            line_number = trcback.tb_lineno
            stack = repr(map(str, self.formatTextException(cls, instance, trcback)))

            javascript = "Crittercism.logExternalException(\"{0}\", \"{1}\", {2}, {3});".format(
                title, file, line_number, stack)
            self.__evaluate_javascript(javascript)
            LOGGER.info("{0} | Exception report sent to Crittercism!".format(self.__class__.__name__))
            return True
        else:
            LOGGER.warning("!> {0} | Failed sending exception report to Crittercism!".format(self.__class__.__name__))
            return False


def base_exception_handler(*args):
    """
    Provides a base exception handler.

    :param \*args: Arguments.
    :type \*args: \*
    :return: Definition success.
    :rtype: bool
    """

    Reporter().handle_exception(*args)

    return True


def system_exit_exception_handler(*args):
    """
    Provides a system exit exception handler.

    :param \*args: Arguments.
    :type \*args: \*
    :return: Definition success.
    :rtype: bool
    """

    reporter = Reporter()
    reporter.Footer_label.setText(
        "The severity of this exception is critical, <b>{0}</b> cannot continue and will now close!".format(
            Constants.application_name))

    base_exception_handler(*args)

    foundations.core.exit(1)

    return True


def critical_exception_handler(object):
    """
    Marks an object that would system exit in case of critical exception.

    :param object: Object to decorate.
    :type object: object
    :return: Object.
    :rtype: object
    """

    @functools.wraps(object)
    def critical_exception_handler_wrapper(*args, **kwargs):
        """
        Marks an object that would system exit in case of critical exception.

        :param \*args: Arguments.
        :type \*args: \*
        :param \*\*kwargs: Keywords arguments.
        :type \*\*kwargs: \*\*
        """

        _exceptions__frame__ = True

        try:
            return object(*args, **kwargs)
        except Exception as error:
            system_exit_exception_handler(error)

    return critical_exception_handler_wrapper


def install_exception_reporter(report=True):
    """
    Installs the exceptions reporter.

    :param report: Report to Crittercism.
    :type report: bool
    :return: Reporter instance.
    :rtype: Reporter
    """

    reporter = Reporter(report=report)
    sys.excepthook = reporter
    return reporter


def uninstall_exception_reporter():
    """
    Uninstalls the exceptions reporter.

    :return: Definition success.
    :rtype: bool
    """

    return foundations.exceptions.install_exception_handler()


def enable_exception_reporter():
    """
    Enables the exceptions reporter.

    :return: Definition success.
    :rtype: bool
    """

    reporter = Reporter().enabled = True
    return True


def disable_exception_reporter():
    """
    Disables the exceptions reporter.

    :return: Definition success.
    :rtype: bool
    """

    reporter = Reporter().enabled = False
    return True


if __name__ == "__main__":
    foundations.verbose.get_logging_console_handler()
    foundations.verbose.set_verbosity_level(3)

    application = umbra.ui.common.get_application_instance()

    install_exception_reporter()

    def _testReporter(bar=1, nemo="captain", *args, **kwargs):
        1 / 0

    _testReporter(luke="skywalker")
