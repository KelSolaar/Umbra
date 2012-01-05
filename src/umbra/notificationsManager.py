#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**notificationsManager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	This module defines the :class:`NotificationsManager` and :class:`Notification` classes.

**Others:**

"""

#**********************************************************************************************************************
#***	External imports.
#**********************************************************************************************************************
import logging
import time
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.core as core
import foundations.dataStructures
import foundations.exceptions
from umbra.globals.constants import Constants
from umbra.ui.widgets.notification_QLabel import Notification_QLabel

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2012 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Notification", "NotificationsManager"]

LOGGER = logging.getLogger(Constants.logger)

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Notification(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for :class:`NotificationsManager` class notification.
	"""

	@core.executionTrace
	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: message, origin. ( Key / Value pairs )
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class NotificationsManager(QObject):
	"""
	This class defines the Application notifications manager. 
	"""

	# Custom signals definitions.
	notificationRegistered = pyqtSignal(Notification)
	"""
	This signal is emited by the :class:`NotificationsManager` class when a notification is registered. ( pyqtSignal )

	:return: Current registered notification. ( Notification )	
	"""

	@core.executionTrace
	def __init__(self, parent):
		"""
		This method initializes the class.
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QObject.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__notifications = []
		self.__notifier = Notification_QLabel(parent)

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def notifications(self):
		"""
		This method is the property for **self.__notifications** attribute.

		:return: self.__notifications. ( List )
		"""

		return self.__notifications

	@notifications.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def notifications(self, value):
		"""
		This method is the setter method for **self.__notifications** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "notifications"))

	@notifications.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def notifications(self):
		"""
		This method is the deleter method for **self.__notifications** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "notifications"))

	@property
	def notifier(self):
		"""
		This method is the property for **self.__notifier** attribute.

		:return: self.__notifier. ( Notification_QLabel )
		"""

		return self.__notifier

	@notifier.setter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def notifier(self, value):
		"""
		This method is the setter method for **self.__notifier** attribute.

		:param value: Attribute value. ( Notification_QLabel )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "notifier"))

	@notifier.deleter
	@foundations.exceptions.exceptionsHandler(None, False, foundations.exceptions.ProgrammingError)
	def notifier(self):
		"""
		This method is the deleter method for **self.__notifier** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "notifier"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def registerNotification(self, notification):
		"""
		This method registers given notification.

		:param notification: Notification to register. ( Notification )
		:return: Method success. ( Boolean )
		"""

		LOGGER.debug("> Registering notification: '{0}'.".format(notification))

		self.__notifications.append(notification)
		self.notificationRegistered.emit(notification)
		return True

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def listNotifications(self):
		"""
		This method list the notifications.

		:return: Notifications list. ( List )
		"""

		return [self.formatNotification(notification) for notification in self.__notifications]

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def formatNotification(self, notification):
		"""
		This method formats given notification.

		:param notification: Notification to format. ( Notification )
		:return: Method success. ( Boolean )
		"""

		return "{0} | '{1}' | '{2}'".format(time.ctime(notification.time), notification.origin, notification.message)

	@core.executionTrace
	@foundations.exceptions.exceptionsHandler(None, False, Exception)
	def notify(self, message, origin=None, duration=2500):
		"""
		This method displays an Application notification.

		:param message: Notification message. ( String )
		:param origin: Notification origin. ( Object )
		:param duration: Notification display duration. ( Integer )
		:return: Method success. ( Boolean )
		"""

		notification = Notification(message=message, origin=origin, time=time.time())

		self.registerNotification(notification)

		message = origin and "{0} | {1}".format(origin, message) or message
		self.__notifier.showMessage(message, duration)

		LOGGER.info("{0} | '{1}'.".format(self.__class__.__name__, self.formatNotification(notification)))

		return True
