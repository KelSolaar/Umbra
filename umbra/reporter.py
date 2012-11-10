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
import urllib2
from xml.etree import ElementTree

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.exceptions
import foundations.verbose
import foundations.strings
import foundations.ui.common
import umbra.ui.common
from umbra.globals.constants import Constants
from umbra.globals.uiConstants import UiConstants

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
		"JQUERY_URL",
		"CRITTERCISM_URL",
		"CRITTERCISM_SUBSTITUTIONS",
		"CRITTERCISM_INITIALISATION"]

LOGGER = foundations.verbose.installLogger()

UI_FILE = umbra.ui.common.getResourcePath(UiConstants.reporterUiFile)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Reporter(foundations.ui.common.QWidgetFactory(uiFile=UI_FILE)):
	"""
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

	def __init__(self, parent=None, *args, **kwargs):
		"""
		This method initializes the class.

		:param parent: Object parent. ( QObject )
		:param \*args: Arguments. ( \* )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		super(Reporter, self).__init__(parent, *args, **kwargs)

		# --- Setting class attributes. ---
		self.__jqueryJavascriptPath = umbra.ui.common.getResourcePath(os.path.join("javascripts", "jquery.js"))
		self.__crittercismJavascriptPath = umbra.ui.common.getResourcePath(os.path.join("javascripts", "crittercism.js"))
		self.__reporterJavascriptPath = umbra.ui.common.getResourcePath(os.path.join("javascripts", "reporter.js"))
		self.__css = """body {
							background-color: rgb(32, 32, 32);
							color: rgb(192, 192, 192);
							font-size: 12pt;
							margin: 16px;
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

						div.header {
							background-color: rgb(210, 64, 32);
							color: rgb(32, 32, 32);
							padding: 8px;
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
		self.__htmlSubstitutions = {"#f0f0f8" : "rgb(48, 48, 48)",
								"#ffffff" : "rgb(32, 32, 32)",
								"#6622aa" : "rgb(210, 125, 80)",
								"#d8bbff" : "rgb(64, 64, 64)",
								"#ffccee" : "rgb(64, 64, 64)"}
		self.__jqueryJavascript = self.getJavascript(self.__jqueryJavascriptPath)
		self.__crittercismJavascript = self.getJavascript(self.__crittercismJavascriptPath)
		self.__reporterJavascript = self.getJavascript(self.__reporterJavascriptPath).format(UiConstants.crittercismId,
																							Constants.releaseVersion)
		self.__html = None

		self.__initializeUi()

	def __call__(self, type, message, trcback):
		"""
		"""

		self.handleException((type, message, trcback))

	def show(self):
		super(Reporter, self).show()
		self.raise_()

	def __initializeUi(self):
		self.__setHtml()

	def __getHtml(self, content=None):
		root = ElementTree.Element("html")
		head = ElementTree.SubElement(root, "head")
		for javascript in (self.__jqueryJavascript,
						self.__crittercismJavascript,
						self.__reporterJavascript):
			script = ElementTree.SubElement(head, "script", attrib={"type" : "text/javascript"})
			script.text = javascript
		style = ElementTree.SubElement(head, "style", attrib={"type" : "text/css"})
		style.text = self.__css
		body = ElementTree.SubElement(root, "body")
		html = ElementTree.tostring(root, method="html")
		return re.sub(r"\<body\>.*\</body\>", content, html) if content is not None else html

	def __formatHtmlException(self, exception):

		escape = lambda x: foundations.strings.replace(x, OrderedDict([("&", "&amp;"), ("<", "&lt;"), (">", "&gt;")]))
		format = lambda x: foundations.strings.replace(x.expandtabs(8), OrderedDict([("\n\n", "\n \n"), ("\n\n", "\n \n"), (" ", "&nbsp;"), ("\n", "<br>\n")]))

		verbose = 10
		type, message, trcback = exception
		stack = foundations.exceptions.extractStack(foundations.exceptions.getInnerMostFrame(trcback), verbose)

		python = "Python {0}: {1}".format(sys.version.split()[0], sys.executable)
		date = time.ctime(time.time())

		html = []
		html.append("<div class=\"header\"><span class=\"floatRight textAlignRight\"><h3>{0}</br>{1}</h3></span><h2>{2}</h2></div>".format(python, date, escape(str(type))))
		html.append("<div class=\"content\">")
		html.append("<p>An unhandled exception occured in <b>{0} {1}</b>! \
				Sequence of calls leading up to the exception, in their occurring order:</p>".format(
				Constants.applicationName, Constants.releaseVersion))
		html.append("<div class=\"stack\">")
		for frame, fileName, lineNumber, name, context, index in stack:
			location = "<b>{0}{1}</b>".format(escape(name) if name != "<module>" else str(),
											inspect.formatargvalues(*inspect.getargvalues(frame)))
			html.append("<div class=\"location\">File <a href=file://{0}>\"{0}\"</a>, line <b>{1}</b>, in {2}</div><br>".format(fileName, lineNumber, location))
			html.append("<div class=\"context\">")
			for i, line in enumerate(context):
				if i == index:
					html.append("<span class=\"highlight\">{0}&nbsp;{1}</span>".format(lineNumber - index + i, format(line)))
				else:
					html.append("{0}&nbsp;{1}".format(lineNumber - index + i, format(line)))
			html.append("</div>")
			html.append("</br>")
		html.append("</div>")
		html.append("</div>")
		html.append("<div class=\"exception\">")
		for line in traceback.format_exception_only(type, message):
			html.append("<b>{0}</b>".format(format(line)))
		html.append("</div>")

		html.append("<div class=\"debug\">")
		html.append("<p>Frames locals by stack ordering, innermost last:</p>")
		for frame, locals in foundations.exceptions.extractLocals(trcback):
			name, fileName, lineNumber = frame
			html.append("<div class=\"frame\">Frame \"{0}\" in <a href=file://{1}>\"{1}\"</a> file, line <b>{2}</b>:</div>".format(escape(name), fileName, lineNumber))
			html.append("</br>")
			html.append("<div class=\"locals\">")
			arguments, namelessArgs, keywordArgs, locals = locals
			hasArguments, hasLocals = any((arguments, namelessArgs, keywordArgs)), any(locals)
			hasArguments and html.append("<div class=\"type\"><b>{0}</b></div><ul>".format("Arguments:"))
			for key, value in arguments:
				html.append("<li><b>{0}</b> = {1}</li>".format(key, escape(value)))
			for value in namelessArgs:
				html.append("<li><b>{0}</b></li>".format(escape(value)))
			for key, value in keywordArgs:
				html.append("<li><b>{0}</b> = {1}</li>".format(key, escape(value)))
			hasArguments and html.append("</ul>")
			hasLocals and html.append("<div class=\"type\"><b>{0}</b></div><ul>".format("Locals:"))
			for key, value in sorted(locals.iteritems()):
				html.append("<li><b>{0}</b> = {1}</li>".format(key, escape(value)))
			hasLocals and html.append("</ul>")
			html.append("</div>")
			html.append("</br>")
		html.append("</div>")

		html.append("<div class=\"traceback\">")
		for line in foundations.exceptions.formatException(type, message, trcback):
			html.append("{0}</br>".format(format(line)))
		html.append("</div>")

		return "<body>{0}</body>".format(str().join(html))

	def __formatTextException(self, exception):

		format = lambda x: re.sub(r"^(\s+)", lambda y: "{0} ".format("." * len(y.group(0))), x.rstrip().expandtabs(4))

		verbose = 10
		type, message, trcback = exception
		stack = foundations.exceptions.extractStack(foundations.exceptions.getInnerMostFrame(trcback), verbose)

		text = []
		text.append(str(type))
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
		for line in traceback.format_exception_only(type, message):
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
			for key, value in arguments:
				text.append(format("\t\t{0} = {1}".format(key, value)))
			for value in namelessArgs:
				text.append(format("\t\t{0}".format(value)))
			for key, value in keywordArgs:
				text.append(format("\\tt{0} = {1}".format(key, value)))
			hasLocals and text.append(format("\tLocals:"))
			for key, value in sorted(locals.iteritems()):
				text.append(format("\t\t{0} = {1}".format(key, value)))
			text.append(str())

		for line in foundations.exceptions.formatException(type, message, trcback):
			text.append(format("{0}".format(format(line))))

		return text

	def __setHtml(self, content=None):
		self.__html = self.__getHtml(content)
		self.Reporter_webView.setHtml(self.__html)

	def __evaluateJavascript(self, javascript):
		self.Reporter_webView.page().mainFrame().evaluateJavaScript(javascript)

	def __sendExceptionToCrittercism(self, exception):
		type, message, trcback = exception
		import pprint
		pprint.pprint(self.__formatTextException(exception))
		self.__evaluateJavascript("Crittercism.logExternalException(\"{0}\", \"{1}\", {2}, {3});".format("\s".join(map(lambda x: x.strip(), traceback.format_exception_only(type, message))),
																								trcback.tb_frame.f_code.co_filename,
																								trcback.tb_lineno,
																								repr(self.__formatTextException(exception))))

	@staticmethod
	def getJavascript(path):
		if foundations.common.pathExists(path):
			return open(path).read()
		else:
			return urllib2.urlopen(path).read()

	def handleException(self, exception):
		content = self.__formatHtmlException(exception)
		self.__setHtml(content)

		self.show()
		self.__sendExceptionToCrittercism(exception)
		self.exec_()

application = umbra.ui.common.getApplicationInstance()
sys.excepthook = Reporter()

def foo(a=1, b="2", *args, **kwargs):
	test = 8
	1 / 0

foo(9)

sys.exit(application.exec_())
