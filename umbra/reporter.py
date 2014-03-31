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

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
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

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core
import foundations.exceptions
import foundations.io
import foundations.verbose
import foundations.strings
import foundations.ui.common
import umbra.ui.common
from umbra.globals.constants import Constants
from umbra.globals.uiConstants import UiConstants
from umbra.globals.runtimeGlobals import RuntimeGlobals

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
		"UI_FILE",
		"Reporter",
		"baseExceptionHandler",
		"systemExitExceptionHandler"
		"criticalExceptionHandler",
		"installExceptionReporter",
		"uninstallExceptionReporter",
		"enableExceptionReporter",
		"disableExceptionReporter"]

LOGGER = foundations.verbose.installLogger()

UI_FILE = umbra.ui.common.getResourcePath(UiConstants.reporterUiFile)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Reporter(foundations.ui.common.QWidgetFactory(uiFile=UI_FILE)):
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

		self.__jqueryJavascriptPath = umbra.ui.common.getResourcePath(os.path.join("javascripts", "jquery.js"))
		self.__crittercismJavascriptPath = umbra.ui.common.getResourcePath(os.path.join("javascripts", "crittercism.js"))
		self.__reporterJavascriptPath = umbra.ui.common.getResourcePath(os.path.join("javascripts", "reporter.js"))
		self.__jqueryJavascript = foundations.io.File(self.__jqueryJavascriptPath).read()
		self.__crittercismJavascript = foundations.io.File(self.__crittercismJavascriptPath).read()
		self.__reporterJavascript = foundations.io.File(self.__reporterJavascriptPath).read().format(
		UiConstants.crittercismId, Constants.version)

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
mailing this report to <b>{0}</b> would help improving <b>{1}</b>!".format(__email__, Constants.applicationName)
		self.__footerText = \
		"The severity of this exception is not critical and <b>{0}</b> will resume!".format(Constants.applicationName)

		self.__initializeUi()

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def report(self):
		"""
		Property for **self.__report** attribute.

		:return: self.__report.
		:rtype: bool
		"""

		return self.__report

	@report.setter
	@foundations.exceptions.handleExceptions(AssertionError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handleExceptions(AssertionError)
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
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def enabled(self):
		"""
		Deleter for **self.__enabled** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "enabled"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
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

		self.handleException(*args)

	def show(self):
		"""
		Reimplements the :meth:`QWidget.show` method.
		"""

		RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.hide()

		super(Reporter, self).show()

		self.raise_()

	def __initializeUi(self):
		"""
		Initializes the Widget ui.
		"""

		LOGGER.debug("> Initializing '{0}' Widget ui.".format(self.__class__.__name__))

		self.__view = self.Reporter_webView

		self.setWindowTitle("{0} - Reporter".format(Constants.applicationName))
		self.Footer_label.setText(self.__footerText)
		self.__initializeContextUi()

		self.__setHtml()

		# Signals / Slots.
		self.Copy_Report_pushButton.clicked.connect(self.__Copy_Report_pushButton__clicked)
		self.Disable_Reporter_pushButton.clicked.connect(self.__Disable_Reporter_pushButton__clicked)

	def __initializeContextUi(self):
		"""
		Sets the context Widget ui.
		"""

		if foundations.common.isInternetAvailable():
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

		uninstallExceptionReporter()
		self.__enabled = False

	def __getHtml(self, body=None):
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
		for javascript in (self.__jqueryJavascript,
						self.__crittercismJavascript,
						self.__reporterJavascript):
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

	def __setHtml(self, html=None):
		"""
		Sets the html content in the View using given body.

		:param html: Html content.
		:type html: unicode
		"""

		self.__html = self.__getHtml(html)
		self.__view.setHtml(self.__html)

	def __updateHtml(self, html):
		"""
		Updates the View with given html content.

		:param html: Html content.
		:type html: unicode
		"""

		if platform.system() in ("Windows", "Microsoft"):
			html = re.sub(r"((?:[a-zA-Z]\:|\\\\[\w\.]+\\[\w.$]+)\\(?:[\w]+\\)*\w([\w.])+)",
			              lambda x: foundations.strings.toForwardSlashes(x.group(1)),
			              html)

		html = foundations.strings.replace(html, OrderedDict([('"', '\\"'), ("\n", "")]))
		self.__evaluateJavascript("$(\"#report\").html(\"{0}\");".format(html))

	def __evaluateJavascript(self, javascript):
		"""
		Evaluates given javascript content in the View.

		:param javascript: Javascript.
		:type javascript: unicode
		"""

		self.__view.page().mainFrame().evaluateJavaScript(javascript)

	def handleException(self, *args):
		"""
		Handles given exception.

		:param \*args: Arguments.
		:type \*args: \*
		"""

		if not self.__enabled:
			return

		cls, instance, trcback = foundations.exceptions.extractException(*args)

		LOGGER.info("{0} | Handling '{1}' exception!".format(self.__class__.__name__, foundations.strings.toString(cls)))

		self.__initializeContextUi()

		self.__updateHtml(self.formatHtmlException(cls, instance, trcback))

		self.show()
		self.__report and self.reportExceptionToCrittercism(cls, instance, trcback)
		foundations.exceptions.baseExceptionHandler(cls, instance, trcback)
		self.exec_()

	@staticmethod
	def formatHtmlException(*args):
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
		OrderedDict([("\n\n", "\n \n"), ("\n\n", "\n \n"), (" ", "&nbsp;"), ("\n", "<br/>\n")]))

		verbose = 10
		cls, instance, trcback = args
		stack = foundations.exceptions.extractStack(foundations.exceptions.getInnerMostFrame(trcback), verbose)

		python = "Python {0}: {1}".format(sys.version.split()[0], sys.executable)
		date = time.ctime(time.time())

		html = []
		html.append(
		"<div class=\"header\"><span class=\"floatRight textAlignRight\"><h4>{0}<br/>{1}</h4></span><h2>{2}</h2></div>".format(
		python, date, escape(foundations.strings.toString(cls))))

		html.append("<div class=\"traceback\">")
		for line in foundations.exceptions.formatException(cls, instance, trcback):
			html.append("{0}<br/>".format(format(escape(line))))
		html.append("</div>")

		html.append("<div class=\"content\">")
		html.append("<p>An unhandled exception occured in <b>{0} {1}</b>! \
				Sequence of calls leading up to the exception, in their occurring order:</p>".format(
				Constants.applicationName, Constants.version))
		html.append("<br/>")
		html.append("<div class=\"stack\">")
		for frame, fileName, lineNumber, name, context, index in stack:
			location = "<b>{0}{1}</b>".format(escape(name) if name != "<module>" else "",
											inspect.formatargvalues(*inspect.getargvalues(frame)))
			html.append(
			"<div class=\"location\">File <a href=file://{0}>\"{0}\"</a>, line <b>{1}</b>, in {2}</div><br>".format(
			fileName, lineNumber, location))
			html.append("<div class=\"context\">")
			for i, line in enumerate(context):
				if i == index:
					html.append("<span class=\"highlight\">{0}&nbsp;{1}</span>".format(
					lineNumber - index + i, format(line)))
				else:
					html.append("{0}&nbsp;{1}".format(lineNumber - index + i, format(line)))
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
		for frame, locals in foundations.exceptions.extractLocals(trcback):
			name, fileName, lineNumber = frame
			html.append(
			"<div class=\"frame\">Frame \"{0}\" in <a href=file://{1}>\"{1}\"</a> file, line <b>{2}</b>:</div>".format(
			escape(name), fileName, lineNumber))
			html.append("<br/>")
			html.append("<div class=\"locals\">")
			arguments, namelessArgs, keywordArgs, locals = locals
			hasArguments, hasLocals = any((arguments, namelessArgs, keywordArgs)), any(locals)
			hasArguments and html.append("<div class=\"cls\"><b>{0}</b></div><ul>".format("Arguments:"))
			for key, value in arguments.iteritems():
				html.append("<li><b>{0}</b> = {1}</li>".format(key, escape(value)))
			for value in namelessArgs:
				html.append("<li><b>{0}</b></li>".format(escape(value)))
			for key, value in sorted(keywordArgs.iteritems()):
				html.append("<li><b>{0}</b> = {1}</li>".format(key, escape(value)))
			hasArguments and html.append("</ul>")
			hasLocals and html.append("<div class=\"cls\"><b>{0}</b></div><ul>".format("Locals:"))
			for key, value in sorted(locals.iteritems()):
				html.append("<li><b>{0}</b> = {1}</li>".format(key, escape(value)))
			hasLocals and html.append("</ul>")
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
		stack = foundations.exceptions.extractStack(foundations.exceptions.getInnerMostFrame(trcback), verbose)

		text = []
		text.append(foundations.strings.toString(cls))
		text.append("")

		for line in foundations.exceptions.formatException(cls, instance, trcback):
			text.append(format("{0}".format(format(line))))
		text.append("")

		text.append("An unhandled exception occured in {0} {1}!".format(Constants.applicationName,
																		Constants.version))
		text.append("Sequence of calls leading up to the exception, in their occurring order:")
		text.append("")

		for frame, fileName, lineNumber, name, context, index in stack:
			location = "{0}{1}".format(name if name != "<module>" else "",
											inspect.formatargvalues(*inspect.getargvalues(frame)))
			text.append("File \"{0}\", line {1}, in {2}".format(fileName, lineNumber, location))
			for i, line in enumerate(context):
				if i == index:
					text.append(format("\t{0} {1} <===".format(lineNumber - index + i, format(format(line)))))
				else:
					text.append(format("\t{0} {1}".format(lineNumber - index + i, format(format(line)))))
			text.append("")
		for line in traceback.format_exception_only(cls, instance):
			text.append("{0}".format(format(line)))
		text.append("")

		text.append("Frames locals by stack ordering, innermost last:")
		text.append("")
		for frame, locals in foundations.exceptions.extractLocals(trcback):
			name, fileName, lineNumber = frame
			text.append("Frame \"{0}\" in \"{1}\" file, line {2}:".format(name, fileName, lineNumber))
			arguments, namelessArgs, keywordArgs, locals = locals
			hasArguments, hasLocals = any((arguments, namelessArgs, keywordArgs)), any(locals)
			hasArguments and text.append(format("\tArguments:"))
			for key, value in arguments.iteritems():
				text.append(format("\t\t{0} = {1}".format(key, value)))
			for value in namelessArgs:
				text.append(format("\t\t{0}".format(value)))
			for key, value in sorted(keywordArgs.iteritems()):
				text.append(format("\\tt{0} = {1}".format(key, value)))
			hasLocals and text.append(format("\tLocals:"))
			for key, value in sorted(locals.iteritems()):
				text.append(format("\t\t{0} = {1}".format(key, value)))
			text.append("")

		return text

	def reportExceptionToCrittercism(self, *args):
		"""
		Reports given exception to Crittercism.

		:param \*args: Arguments.
		:type \*args: \*
		:return: Method success.
		:rtype: bool
		"""

		if foundations.common.isInternetAvailable():
			cls, instance, trcback = args

			title = re.escape("".join(map(lambda x: x.strip(), traceback.format_exception_only(cls, instance))))
			file = trcback.tb_frame.f_code.co_filename
			lineNumber = trcback.tb_lineno
			stack = repr(map(str, self.formatTextException(cls, instance, trcback)))

			javascript = "Crittercism.logExternalException(\"{0}\", \"{1}\", {2}, {3});".format(
			title, file, lineNumber, stack)
			self.__evaluateJavascript(javascript)
			LOGGER.info("{0} | Exception report sent to Crittercism!".format(self.__class__.__name__))
			return True
		else:
			LOGGER.warning("!> {0} | Failed sending exception report to Crittercism!".format(self.__class__.__name__))
			return False

def baseExceptionHandler(*args):
	"""
	Provides a base exception handler.

	:param \*args: Arguments.
	:type \*args: \*
	:return: Definition success.
	:rtype: bool
	"""

	Reporter().handleException(*args)

	return True

def systemExitExceptionHandler(*args):
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
	Constants.applicationName))

	baseExceptionHandler(*args)

	foundations.core.exit(1)

	return True

def criticalExceptionHandler(object):
	"""
	Marks an object that would system exit in case of critical exception.

	:param object: Object to decorate.
	:type object: object
	:return: Object.
	:rtype: object
	"""

	@functools.wraps(object)
	def criticalExceptionHandlerWrapper(*args, **kwargs):
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
			systemExitExceptionHandler(error)

	return criticalExceptionHandlerWrapper

def installExceptionReporter(report=True):
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

def uninstallExceptionReporter():
	"""
	Uninstalls the exceptions reporter.

	:return: Definition success.
	:rtype: bool
	"""

	return foundations.exceptions.installExceptionHandler()

def enableExceptionReporter():
	"""
	Enables the exceptions reporter.

	:return: Definition success.
	:rtype: bool
	"""

	reporter = Reporter().enabled = True
	return True

def disableExceptionReporter():
	"""
	Disables the exceptions reporter.

	:return: Definition success.
	:rtype: bool
	"""

	reporter = Reporter().enabled = False
	return True

if __name__ == "__main__":
	foundations.verbose.getLoggingConsoleHandler()
	foundations.verbose.setVerbosityLevel(3)

	application = umbra.ui.common.getApplicationInstance()

	installExceptionReporter()

	def _testReporter(bar=1, nemo="captain", *args, **kwargs):
		1 / 0

	_testReporter(luke="skywalker")
