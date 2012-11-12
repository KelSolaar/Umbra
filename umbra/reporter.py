#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**reporter.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines ... 

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import functools
import inspect
import os
import re
import sys
if sys.version_info[:2] <= (2, 6):
	from ordereddict import OrderedDict
else:
	from collections import OrderedDict
import time
import traceback
from PyQt4.QtGui import QApplication
from xml.etree import ElementTree

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
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER",
		"UI_FILE",
		"Reporter",
		"critical",
		"installReporter",
		"uninstallReporter"]

LOGGER = foundations.verbose.installLogger()

UI_FILE = umbra.ui.common.getResourcePath(UiConstants.reporterUiFile)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Reporter(foundations.ui.common.QWidgetFactory(uiFile=UI_FILE)):
	"""
	This class provides an exceptions reporting Widget.
	"""

	__instance = None
	"""Class instance. ( Reporter )"""

	def __new__(cls, *args, **kwargs):
		"""
		This method is the constructor of the class.
		
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		:return: Class instance. ( Library )
		"""

		if not cls._Reporter__instance:
			cls._Reporter__instance = super(Reporter, cls).__new__(cls, *args, **kwargs)
		return cls._Reporter__instance

	def __init__(self, parent=None, report=True, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param report: Report to Crittercism. ( Boolean )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(Reporter, self).__init__(parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__report = None
		self.report = report

		self.__jqueryJavascriptPath = umbra.ui.common.getResourcePath(os.path.join("javascripts", "jquery.js"))
		self.__crittercismJavascriptPath = umbra.ui.common.getResourcePath(os.path.join("javascripts", "crittercism.js"))
		self.__reporterJavascriptPath = umbra.ui.common.getResourcePath(os.path.join("javascripts", "reporter.js"))
		self.__jqueryJavascript = foundations.io.File(self.__jqueryJavascriptPath).read()
		self.__crittercismJavascript = foundations.io.File(self.__crittercismJavascriptPath).read()
		self.__reporterJavascript = foundations.io.File(self.__reporterJavascriptPath).read().format(
		UiConstants.crittercismId, Constants.releaseVersion)

		self.__style = """* {
							margin: 0;
							padding: 0;
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
						}

						div.header {
							background-color: rgb(210, 64, 32);
							color: rgb(32, 32, 32);
							padding: 24px;
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
							font-size: 16px;;
						}

						div.locals {
							background-color: rgb(48, 48, 48);
							color: rgb(160, 160, 160);
							line-height: 150%;
							padding: 32px;
						}

						div.traceback {
							background-color: rgb(210, 64, 32);
							color: rgb(32, 32, 32);
							font-size: 16px;
							padding: 16px;
						}"""
		self.__html = None

		self.__onlineText = "An <b>unhandled</b> exception occured!<br/> \
The following report has been sent to <b>HDRLabs</b> development team!"
		self.__offlineText = "An <b>unhandled</b> exception occured!<br/> \
Mailing the following report to <b>{0}</b> would help improving <b>{1}</b>!".format(__email__, Constants.applicationName)

		self.__initializeUi()

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def report(self):
		"""
		This method is the property for **self.__report** attribute.

		:return: self.__report. ( Boolean )
		"""

		return self.__report

	@report.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def report(self, value):
		"""
		This method is the setter method for **self.__report** attribute.

		:param value: Attribute value. ( Boolean )
		"""

		if value is not None:
			assert type(value) is bool, "'{0}' attribute: '{1}' type is not 'bool'!".format("report", value)
		self.__report = value

	@report.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def report(self):
		"""
		This method is the deleter method for **self.__report** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "report"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __call__(self, *args):
		"""
		This method is the caller of the class.
		
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		:return: Class instance. ( Library )
		"""

		self.handleException(args)

	def show(self):
		"""
		This method reimplements the :meth:`QWidget.show` method.
		"""

		super(Reporter, self).show()
		self.raise_()

	def __initializeUi(self):
		"""
		This method initializes the Widget ui.
		"""

		LOGGER.debug("> Initializing '{0}' Widget ui.".format(self.__class__.__name__))

		self.__view = self.Reporter_webView

		self.setWindowTitle("{0} - Reporter".format(Constants.applicationName))

		self.__initializeContextUi()

		self.__setHtml()

		# Signals / Slots.
		self.Copy_Report_pushButton.clicked.connect(self.__Copy_Report_pushButton__clicked)

	def __initializeContextUi(self):
		"""
		This method sets the context Widget ui.
		"""

		if foundations.common.isInternetAvailable():
			text = self.__onlineText
		else:
			text = self.__offlineText
		self.Header_label.setText(text)

	def __Copy_Report_pushButton__clicked(self, checked):
		"""
		This method is triggered when **Copy_Report_pushButton** Widget is clicked.

		:param checked: Checked state. ( Boolean )
		"""

		clipboard = QApplication.clipboard()
		clipboard.setText(self.__view.page().mainFrame().toPlainText())

	def __getHtml(self, body=None):
		"""
		This method returns the html content with given body tag content.

		:param body: Body tag content. ( String )
		:return: Html. ( String )
		"""

		root = ElementTree.Element("html")
		head = ElementTree.SubElement(root, "head")
		for javascript in (self.__jqueryJavascript,
						self.__crittercismJavascript,
						self.__reporterJavascript):
			script = ElementTree.SubElement(head, "script", attrib={"type" : "text/javascript"})
			script.text = javascript
		style = ElementTree.SubElement(head, "style", attrib={"type" : "text/css"})
		style.text = self.__style
		node = ElementTree.SubElement(root, "body")
		html = ElementTree.tostring(root, method="html")
		return re.sub(r"\<body\>.*\</body\>", body, html) if body is not None else html

	def __setHtml(self, body=None):
		"""
		This method sets the html content in the View using given body.

		:param body: Body tag content. ( String )
		"""

		self.__html = self.__getHtml(body)
		self.__view.setHtml(self.__html)

	def __evaluateJavascript(self, javascript):
		"""
		This method evaluates given javascript content in the View.

		:param javascript: Javascript. ( String )
		"""

		self.__view.page().mainFrame().evaluateJavaScript(javascript)

	def handleException(self, exception):
		"""
		This method handles given exception.

		:param exception: Exception informations. ( Tuple )
		"""

		cls, instance, trcback = exception

		LOGGER.info("{0} | Handling '{1}' exception!".format(self.__class__.__name__, str(cls)))

		self.__initializeContextUi()

		self.__setHtml(self.formatHtmlException(exception))

		self.show()
		self.__report and self.reportExceptionToCrittercism(exception)
		self.exec_()

	@staticmethod
	def formatHtmlException(exception):
		"""
		This method formats given exception as an html text.

		:param exception: Exception informations. ( Tuple )
		:return: Exception html text. ( String )
		"""

		escape = lambda x: foundations.strings.replace(x,
		OrderedDict([("&", "&amp;"), ("<", "&lt;"), (">", "&gt;")]))
		format = lambda x: foundations.strings.replace(x.expandtabs(8),
		OrderedDict([("\n\n", "\n \n"), ("\n\n", "\n \n"), (" ", "&nbsp;"), ("\n", "<br>\n")]))

		verbose = 10
		cls, instance, trcback = exception
		stack = foundations.exceptions.extractStack(foundations.exceptions.getInnerMostFrame(trcback), verbose)

		python = "Python {0}: {1}".format(sys.version.split()[0], sys.executable)
		date = time.ctime(time.time())

		html = []
		html.append(
		"<div class=\"header\"><span class=\"floatRight textAlignRight\"><h4>{0}<br/>{1}</h4></span><h2>{2}</h2></div>".format(
		python, date, escape(str(cls))))
		html.append("<div class=\"content\">")
		html.append("<p>An unhandled exception occured in <b>{0} {1}</b>! \
				Sequence of calls leading up to the exception, in their occurring order:</p>".format(
				Constants.applicationName, Constants.releaseVersion))
		html.append("<br/>")
		html.append("<div class=\"stack\">")
		for frame, fileName, lineNumber, name, context, index in stack:
			location = "<b>{0}{1}</b>".format(escape(name) if name != "<module>" else str(),
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

		html.append("<div class=\"traceback\">")
		for line in foundations.exceptions.formatException(cls, instance, trcback):
			html.append("{0}<br/>".format(format(line)))
		html.append("</div>")

		return "<body>{0}</body>".format(str().join(html))

	@staticmethod
	def formatTextException(exception):
		"""
		This method formats given exception as a text.

		:param exception: Exception informations. ( Tuple )
		:return: Exception text. ( String )
		"""

		format = lambda x: re.sub(r"^(\s+)", lambda y: "{0} ".format("." * len(y.group(0))), x.rstrip().expandtabs(4))

		verbose = 10
		cls, instance, trcback = exception
		stack = foundations.exceptions.extractStack(foundations.exceptions.getInnerMostFrame(trcback), verbose)

		text = []
		text.append(str(cls))
		text.append(str())
		text.append("An unhandled exception occured in {0} {1}!".format(Constants.applicationName,
																		Constants.releaseVersion))
		text.append("Sequence of calls leading up to the exception, in their occurring order:")
		text.append(str())

		for frame, fileName, lineNumber, name, context, index in stack:
			location = "{0}{1}".format(name if name != "<module>" else str(),
											inspect.formatargvalues(*inspect.getargvalues(frame)))
			text.append("File \"{0}\", line {1}, in {2}".format(fileName, lineNumber, location))
			for i, line in enumerate(context):
				if i == index:
					text.append(format("\t{0} {1} <===".format(lineNumber - index + i, format(format(line)))))
				else:
					text.append(format("\t{0} {1}".format(lineNumber - index + i, format(format(line)))))
			text.append(str())
		for line in traceback.format_exception_only(cls, instance):
			text.append("{0}".format(format(line)))
		text.append(str())

		text.append("Frames locals by stack ordering, innermost last:")
		text.append(str())
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
			text.append(str())

		for line in foundations.exceptions.formatException(cls, instance, trcback):
			text.append(format("{0}".format(format(line))))

		return text

	def reportExceptionToCrittercism(self, exception):
		"""
		This method reports given exception to Crittercism.

		:param exception: Exception informations. ( Tuple )
		:return: Method success. ( Boolean )
		"""

		if foundations.common.isInternetAvailable():
			cls, instance, trcback = exception

			title = "\s".join(map(lambda x: x.strip(), traceback.format_exception_only(cls, instance)))
			file = trcback.tb_frame.f_code.co_filename
			lineNumber = trcback.tb_lineno
			stack = repr(self.formatTextException(exception))

			self.__evaluateJavascript("Crittercism.logExternalException(\"{0}\", \"{1}\", {2}, {3});".format(
			title, file, lineNumber, stack))
			LOGGER.info("{0} | Exception report sent to Crittercism!".format(self.__class__.__name__))
			return True
		else:
			LOGGER.warning("!> {0} | Failed sending exception report to Crittercism!".format(self.__class__.__name__))
			return False

def critical(object):
	"""
	This decorator is used to mark an object that would system exit in case of critical exception.

	:param object: Object to decorate. ( Object )
	:return: Object. ( Object )
	"""

	@functools.wraps(object)
	def criticalWrapper(*args, **kwargs):
		"""
		This decorator is used to mark an object that would system exit in case of critical exception.

		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		_exceptions__frame__ = True

		try:
			return object(*args, **kwargs)
		except Exception as error:
			RuntimeGlobals.splashscreen and RuntimeGlobals.splashscreen.hide()

			exception = sys.exc_info()

			reporter = Reporter()
			reporter._Reporter__initializeContextUi = lambda: \
			reporter.Header_label.setText("{0}<br/><b>{1}</b> cannot continue and will now close!".format(
			reporter.Header_label.text(), Constants.applicationName))
			reporter.handleException(exception)

			foundations.exceptions.defaultExceptionHandler(error, None)

			foundations.core.exit(1)

	return criticalWrapper

def installReporter(report=True):
	"""
	This definition installs the exceptions reporter.
	
	:param report: Report to Crittercism. ( Boolean )
	:return: Definition success. ( Boolean )
	"""

	sys.excepthook = Reporter(report=report)
	return True

def uninstallReporter():
	"""
	This definition uninstalls the exceptions reporter.
	
	:return: Definition success. ( Boolean )
	"""

	sys.excepthook = sys.__excepthook__
	return True

if __name__ == "__main__":
	application = umbra.ui.common.getApplicationInstance()

	installReporter()

	def testReporter(bar=1, nemo="captain", *args, **kwargs):
		1 / 0

	testReporter(luke="skywalker")
