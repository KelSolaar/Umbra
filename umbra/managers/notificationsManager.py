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
import time
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QObject
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QColor

#**********************************************************************************************************************
#***	Internal imports.
#**********************************************************************************************************************
import foundations.dataStructures
import foundations.exceptions
import foundations.verbose
from umbra.ui.widgets.notification_QLabel import Notification_QLabel

#**********************************************************************************************************************
#***	Module attributes.
#**********************************************************************************************************************
__author__ = "Thomas Mansencal"
__copyright__ = "Copyright (C) 2008 - 2013 - Thomas Mansencal"
__license__ = "GPL V3.0 - http://www.gnu.org/licenses/"
__maintainer__ = "Thomas Mansencal"
__email__ = "thomas.mansencal@gmail.com"
__status__ = "Production"

__all__ = ["LOGGER", "Notification", "NotificationsManager"]

LOGGER = foundations.verbose.installLogger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Notification(foundations.dataStructures.Structure):
	"""
	This class represents a storage object for :class:`NotificationsManager` class notification.
	"""

	def __init__(self, **kwargs):
		"""
		This method initializes the class.

		:param \*\*kwargs: message, time. ( Key / Value pairs )
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

	def __init__(self, parent=None):
		"""
		This method initializes the class.
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QObject.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__container = parent

		self.__notifications = []
		self.__notifiers = []

		self.__notifiersStackPadding = 10

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def container(self):
		"""
		This method is the property for **self.__container** attribute.

		:return: self.__container. ( QObject )
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		This method is the setter method for **self.__container** attribute.

		:param value: Attribute value. ( QObject )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		This method is the deleter method for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def notifications(self):
		"""
		This method is the property for **self.__notifications** attribute.

		:return: self.__notifications. ( List )
		"""

		return self.__notifications

	@notifications.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def notifications(self, value):
		"""
		This method is the setter method for **self.__notifications** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "notifications"))

	@notifications.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def notifications(self):
		"""
		This method is the deleter method for **self.__notifications** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "notifications"))

	@property
	def notifiers(self):
		"""
		This method is the property for **self.__notifiers** attribute.

		:return: self.__notifiers. ( List )
		"""

		return self.__notifiers

	@notifiers.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def notifiers(self, value):
		"""
		This method is the setter method for **self.__notifiers** attribute.

		:param value: Attribute value. ( List )
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "notifiers"))

	@notifiers.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def notifiers(self):
		"""
		This method is the deleter method for **self.__notifiers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "notifiers"))

	@property
	def notifiersStackPadding(self):
		"""
		This method is the property for **self.__notifiersStackPadding** attribute.

		:return: self.__notifiersStackPadding. ( Integer )
		"""

		return self.__notifiersStackPadding

	@notifiersStackPadding.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def notifiersStackPadding(self, value):
		"""
		This method is the setter method for **self.__notifiersStackPadding** attribute.

		:param value: Attribute value. ( Integer )
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("notifiersStackPadding", value)
			assert value >= 0, "'{0}' attribute: '{1}' need to be positive!".format("notifiersStackPadding", value)
		self.__notifiersStackPadding = value

	@notifiersStackPadding.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def notifiersStackPadding(self):
		"""
		This method is the deleter method for **self.__notifiersStackPadding** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
		"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "notifiersStackPadding"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __iter__(self):
		"""
		This method reimplements the :meth:`object.__iter__` method.

		:return: Notifications iterator. ( Object )
		"""

		return iter(self.__notifications)

	def __len__(self):
		"""
		This method reimplements the :meth:`object.__len__` method.

		:return: Notifications count. ( Integer )
		"""

		return len(self.__notifications)

	def __notifier__fadedOut(self):
		"""
		This method is triggered when a **Notification_QLabel** Widget has faded out.
		"""

		self.__notifiers.pop(self.__notifiers.index(self.sender()))

	def __offsetNotifiers(self, offset):
		"""
		This method offsets existing notifiers.

		:param offset: Offset. ( Integer )
		"""

		for notifier in self.__notifiers:
			notifier.verticalOffset += offset
			notifier.refreshPosition()

	def listNotifications(self):
		"""
		This method returns the registered notifications.

		:return: Notifications list. ( List )
		"""

		return [self.formatNotification(notification) for notification in self]

	def isNotificationRegistered(self, notification):
		"""
		This method returns if the given notification is registered.

		:param notification: Notification. ( String )
		:return: Is notification registered. ( Boolean )
		"""

		return notification in self

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

	def formatNotification(self, notification):
		"""
		This method formats given notification.

		:param notification: Notification to format. ( Notification )
		:return: Method success. ( Boolean )
		"""

		return "{0} | '{1}'".format(time.ctime(notification.time), notification.message)

	def notify(self, message, duration=3000, notificationClickedSlot=None, messageLevel="Information", **kwargs):
		"""
		This method displays an Application notification.

		:param message: Notification message. ( String )
		:param duration: Notification display duration. ( Integer )
		:param notificationClickedSlot: Notification clicked slot. ( Object )
		:param messageLevel: Message level ( "Information", "Warning", "Exception" ). ( String )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		:return: Method success. ( Boolean )
		"""

		notification = Notification(message=message, time=time.time())

		self.registerNotification(notification)

		notifier = Notification_QLabel(self.__container, **kwargs)

		# Signals / Slots.
		notifier.fadedOut.connect(self.__notifier__fadedOut)
		self.__container.sizeChanged.connect(notifier.resizeEvent)
		if notificationClickedSlot:
			notifier.notificationClicked.connect(notificationClickedSlot)
		else:
			notifier.setAttribute(Qt.WA_TransparentForMouseEvents)

		notifier.showMessage(message, duration)

		self.__offsetNotifiers(-notifier.height() - self.__notifiersStackPadding)
		self.__notifiers.append(notifier)

		if messageLevel == "Information":
			LOGGER.info("{0} | '{1}'.".format(self.__class__.__name__, self.formatNotification(notification)))
		elif messageLevel == "Warning":
			LOGGER.warning("!> {0} | '{1}'.".format(self.__class__.__name__, self.formatNotification(notification)))
		elif messageLevel == "Exception":
			LOGGER.error("!> {0} | '{1}'.".format(self.__class__.__name__, self.formatNotification(notification)))
		return True

	def warnify(self, message, duration=3000, notificationClickedSlot=None, **kwargs):
		"""
		This method displays an Application notification warning.

		:param message: Notification message. ( String )
		:param duration: Notification display duration. ( Integer )
		:param notificationClickedSlot: Notification clicked slot. ( Object )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		:return: Method success. ( Boolean )
		"""

		return self.notify(message,
					duration,
					notificationClickedSlot,
					messageLevel="Warning",
					color=QColor(220, 128, 64),
					backgroundColor=QColor(32, 32, 32),
					borderColor=QColor(220, 128, 64),
					**kwargs)

	def exceptify(self, message, duration=3000, notificationClickedSlot=None, **kwargs):
		"""
		This method displays an Application notification exception.

		:param message: Notification message. ( String )
		:param duration: Notification display duration. ( Integer )
		:param notificationClickedSlot: Notification clicked slot. ( Object )
		:param \*\*kwargs: Keywords arguments. ( \*\* )
		:return: Method success. ( Boolean )
		"""

		return self.notify(message,
					duration,
					notificationClickedSlot,
					messageLevel="Exception",
					color=QColor(220, 64, 64),
					backgroundColor=QColor(32, 32, 32),
					borderColor=QColor(220, 64, 64),
					**kwargs)
