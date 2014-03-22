#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**notificationsManager.py**

**Platform:**
	Windows, Linux, Mac Os X.

**Description:**
	Defines the :class:`NotificationsManager` and :class:`Notification` classes.

**Others:**

"""

#**********************************************************************************************************************
#***	Future imports.
#**********************************************************************************************************************
from __future__ import unicode_literals

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
__copyright__ = "Copyright (C) 2008 - 2014 - Thomas Mansencal"
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
	Defines a storage object for :class:`NotificationsManager` class notification.
	"""

	def __init__(self, **kwargs):
		"""
		Initializes the class.

		:param \*\*kwargs: message, time.
		:type \*\*kwargs: dict
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		foundations.dataStructures.Structure.__init__(self, **kwargs)

class NotificationsManager(QObject):
	"""
	Defines the Application notifications manager.
	"""

	# Custom signals definitions.
	notificationRegistered = pyqtSignal(Notification)
	"""
	This signal is emited by the :class:`NotificationsManager` class when a notification is registered. ( pyqtSignal )

	:return: Current registered notification.
	:rtype: Notification
	"""

	def __init__(self, parent=None):
		"""
		Initializes the class.
		"""

		LOGGER.debug("> Initializing '{0}()' class.".format(self.__class__.__name__))

		QObject.__init__(self, parent)

		# --- Setting class attributes. ---
		self.__container = parent

		self.__notifications = []
		self.__notifiers = []

		self.__notifiersStackPadding = 10
		self.__maximumNotifiers = 5

	#******************************************************************************************************************
	#***	Attributes properties.
	#******************************************************************************************************************
	@property
	def container(self):
		"""
		Property for **self.__container** attribute.

		:return: self.__container.
		:rtype: QObject
		"""

		return self.__container

	@container.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self, value):
		"""
		Setter for **self.__container** attribute.

		:param value: Attribute value.
		:type value: QObject
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "container"))

	@container.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def container(self):
		"""
		Deleter for **self.__container** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "container"))

	@property
	def notifications(self):
		"""
		Property for **self.__notifications** attribute.

		:return: self.__notifications.
		:rtype: list
		"""

		return self.__notifications

	@notifications.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def notifications(self, value):
		"""
		Setter for **self.__notifications** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "notifications"))

	@notifications.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def notifications(self):
		"""
		Deleter for **self.__notifications** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "notifications"))

	@property
	def notifiers(self):
		"""
		Property for **self.__notifiers** attribute.

		:return: self.__notifiers.
		:rtype: list
		"""

		return self.__notifiers

	@notifiers.setter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def notifiers(self, value):
		"""
		Setter for **self.__notifiers** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "notifiers"))

	@notifiers.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def notifiers(self):
		"""
		Deleter for **self.__notifiers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "notifiers"))

	@property
	def notifiersStackPadding(self):
		"""
		Property for **self.__notifiersStackPadding** attribute.

		:return: self.__notifiersStackPadding.
		:rtype: int
		"""

		return self.__notifiersStackPadding

	@notifiersStackPadding.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def notifiersStackPadding(self, value):
		"""
		Setter for **self.__notifiersStackPadding** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("notifiersStackPadding",
																						  value)
			assert value >= 0, "'{0}' attribute: '{1}' need to be positive!".format("notifiersStackPadding", value)
		self.__notifiersStackPadding = value

	@notifiersStackPadding.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def notifiersStackPadding(self):
		"""
		Deleter for **self.__notifiersStackPadding** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "notifiersStackPadding"))

	@property
	def maximumNotifiers(self):
		"""
		Property for **self.__maximumNotifiers** attribute.

		:return: self.__maximumNotifiers.
		:rtype: int
		"""

		return self.__maximumNotifiers

	@maximumNotifiers.setter
	@foundations.exceptions.handleExceptions(AssertionError)
	def maximumNotifiers(self, value):
		"""
		Setter for **self.__maximumNotifiers** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("maximumNotifiers",
																						  value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("maximumNotifiers", value)
		self.__maximumNotifiers = value

	@maximumNotifiers.deleter
	@foundations.exceptions.handleExceptions(foundations.exceptions.ProgrammingError)
	def maximumNotifiers(self):
		"""
		Deleter for **self.__maximumNotifiers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "maximumNotifiers"))

	#******************************************************************************************************************
	#***	Class methods.
	#******************************************************************************************************************
	def __iter__(self):
		"""
		Reimplements the :meth:`object.__iter__` method.

		:return: Notifications iterator.
		:rtype: object
		"""

		return iter(self.__notifications)

	def __len__(self):
		"""
		Reimplements the :meth:`object.__len__` method.

		:return: Notifications count.
		:rtype: int
		"""

		return len(self.__notifications)

	def __notifier__fadedOut(self):
		"""
		Defines the slot triggered by **Notification_QLabel** Widget when faded out.
		"""

		if self.sender() in self.__notifiers:
			self.__notifiers.pop(self.__notifiers.index(self.sender()))

	def __offsetNotifiers(self, offset):
		"""
		Offsets existing notifiers.

		:param offset: Offset.
		:type offset: int
		"""

		overallOffset = offset
		for notifier in self.__notifiers:
			notifier.verticalOffset = overallOffset
			notifier.refreshPosition()
			overallOffset += offset

	def listNotifications(self):
		"""
		Returns the registered notifications.

		:return: Notifications list.
		:rtype: list
		"""

		return [self.formatNotification(notification) for notification in self]

	def isNotificationRegistered(self, notification):
		"""
		Returns if the given notification is registered.

		:param notification: Notification.
		:type notification: unicode
		:return: Is notification registered.
		:rtype: bool
		"""

		return notification in self

	def registerNotification(self, notification):
		"""
		Registers given notification.

		:param notification: Notification to register.
		:type notification: Notification
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Registering notification: '{0}'.".format(notification))

		self.__notifications.append(notification)
		self.notificationRegistered.emit(notification)
		return True

	def formatNotification(self, notification):
		"""
		Formats given notification.

		:param notification: Notification to format.
		:type notification: Notification
		:return: Method success.
		:rtype: bool
		"""

		return "{0} | '{1}'".format(time.ctime(notification.time), notification.message)

	def notify(self, message, duration=3000, notificationClickedSlot=None, messageLevel="Information", **kwargs):
		"""
		Displays an Application notification.

		:param message: Notification message.
		:type message: unicode
		:param duration: Notification display duration.
		:type duration: int
		:param notificationClickedSlot: Notification clicked slot.
		:type notificationClickedSlot: object
		:param messageLevel: Message level ( "Information", "Warning", "Exception" ).
		:type messageLevel: unicode
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Method success.
		:rtype: bool
		"""

		for notifier in self.__notifiers[self.__maximumNotifiers - 1:]:
			notifier.duration=150
			notifier.hideMessage()

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
		self.__notifiers.insert(0, notifier)

		if messageLevel == "Information":
			LOGGER.info("{0} | '{1}'.".format(self.__class__.__name__, self.formatNotification(notification)))
		elif messageLevel == "Warning":
			LOGGER.warning("!> {0} | '{1}'.".format(self.__class__.__name__, self.formatNotification(notification)))
		elif messageLevel == "Exception":
			LOGGER.error("!> {0} | '{1}'.".format(self.__class__.__name__, self.formatNotification(notification)))

		return True

	def warnify(self, message, duration=3000, notificationClickedSlot=None, **kwargs):
		"""
		Displays an Application notification warning.

		:param message: Notification message.
		:type message: unicode
		:param duration: Notification display duration.
		:type duration: int
		:param notificationClickedSlot: Notification clicked slot.
		:type notificationClickedSlot: object
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Method success.
		:rtype: bool
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
		Displays an Application notification exception.

		:param message: Notification message.
		:type message: unicode
		:param duration: Notification display duration.
		:type duration: int
		:param notificationClickedSlot: Notification clicked slot.
		:type notificationClickedSlot: object
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Method success.
		:rtype: bool
		"""

		return self.notify(message,
						   duration,
						   notificationClickedSlot,
						   messageLevel="Exception",
						   color=QColor(220, 64, 64),
						   backgroundColor=QColor(32, 32, 32),
						   borderColor=QColor(220, 64, 64),
						   **kwargs)
