#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**notifications_manager.py**

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
import foundations.data_structures
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

LOGGER = foundations.verbose.install_logger()

#**********************************************************************************************************************
#***	Module classes and definitions.
#**********************************************************************************************************************
class Notification(foundations.data_structures.Structure):
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

		foundations.data_structures.Structure.__init__(self, **kwargs)

class NotificationsManager(QObject):
	"""
	Defines the Application notifications manager.
	"""

	# Custom signals definitions.
	notification_registered = pyqtSignal(Notification)
	"""
	This signal is emited by the :class:`NotificationsManager` class when a notification is registered.

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

		self.__notifiers_stack_padding = 10
		self.__maximum_notifiers = 5

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

	@property
	def notifications(self):
		"""
		Property for **self.__notifications** attribute.

		:return: self.__notifications.
		:rtype: list
		"""

		return self.__notifications

	@notifications.setter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def notifications(self, value):
		"""
		Setter for **self.__notifications** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "notifications"))

	@notifications.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
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
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def notifiers(self, value):
		"""
		Setter for **self.__notifiers** attribute.

		:param value: Attribute value.
		:type value: list
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is read only!".format(self.__class__.__name__, "notifiers"))

	@notifiers.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def notifiers(self):
		"""
		Deleter for **self.__notifiers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "notifiers"))

	@property
	def notifiers_stack_padding(self):
		"""
		Property for **self.__notifiers_stack_padding** attribute.

		:return: self.__notifiers_stack_padding.
		:rtype: int
		"""

		return self.__notifiers_stack_padding

	@notifiers_stack_padding.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def notifiers_stack_padding(self, value):
		"""
		Setter for **self.__notifiers_stack_padding** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("notifiers_stack_padding",
																						  value)
			assert value >= 0, "'{0}' attribute: '{1}' need to be positive!".format("notifiers_stack_padding", value)
		self.__notifiers_stack_padding = value

	@notifiers_stack_padding.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def notifiers_stack_padding(self):
		"""
		Deleter for **self.__notifiers_stack_padding** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "notifiers_stack_padding"))

	@property
	def maximum_notifiers(self):
		"""
		Property for **self.__maximum_notifiers** attribute.

		:return: self.__maximum_notifiers.
		:rtype: int
		"""

		return self.__maximum_notifiers

	@maximum_notifiers.setter
	@foundations.exceptions.handle_exceptions(AssertionError)
	def maximum_notifiers(self, value):
		"""
		Setter for **self.__maximum_notifiers** attribute.

		:param value: Attribute value.
		:type value: int
		"""

		if value is not None:
			assert type(value) is int, "'{0}' attribute: '{1}' type is not 'int'!".format("maximum_notifiers",
																						  value)
			assert value > 0, "'{0}' attribute: '{1}' need to be exactly positive!".format("maximum_notifiers", value)
		self.__maximum_notifiers = value

	@maximum_notifiers.deleter
	@foundations.exceptions.handle_exceptions(foundations.exceptions.ProgrammingError)
	def maximum_notifiers(self):
		"""
		Deleter for **self.__maximum_notifiers** attribute.
		"""

		raise foundations.exceptions.ProgrammingError(
			"{0} | '{1}' attribute is not deletable!".format(self.__class__.__name__, "maximum_notifiers"))

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

	def __notifier__faded_out(self):
		"""
		Defines the slot triggered by **Notification_QLabel** Widget when faded out.
		"""

		if self.sender() in self.__notifiers:
			self.__notifiers.pop(self.__notifiers.index(self.sender()))

	def __offset_notifiers(self, offset):
		"""
		Offsets existing notifiers.

		:param offset: Offset.
		:type offset: int
		"""

		overall_offset = offset
		for notifier in self.__notifiers:
			notifier.vertical_offset = overall_offset
			notifier.refresh_position()
			overall_offset += offset

	def list_notifications(self):
		"""
		Returns the registered notifications.

		:return: Notifications list.
		:rtype: list
		"""

		return [self.format_notification(notification) for notification in self]

	def is_notification_registered(self, notification):
		"""
		Returns if the given notification is registered.

		:param notification: Notification.
		:type notification: unicode
		:return: Is notification registered.
		:rtype: bool
		"""

		return notification in self

	def register_notification(self, notification):
		"""
		Registers given notification.

		:param notification: Notification to register.
		:type notification: Notification
		:return: Method success.
		:rtype: bool
		"""

		LOGGER.debug("> Registering notification: '{0}'.".format(notification))

		self.__notifications.append(notification)
		self.notification_registered.emit(notification)
		return True

	def format_notification(self, notification):
		"""
		Formats given notification.

		:param notification: Notification to format.
		:type notification: Notification
		:return: Method success.
		:rtype: bool
		"""

		return "{0} | '{1}'".format(time.ctime(notification.time), notification.message)

	def notify(self, message, duration=3000, notification_clicked_slot=None, message_level="Information", **kwargs):
		"""
		Displays an Application notification.

		:param message: Notification message.
		:type message: unicode
		:param duration: Notification display duration.
		:type duration: int
		:param notification_clicked_slot: Notification clicked slot.
		:type notification_clicked_slot: object
		:param message_level: Message level ( "Information", "Warning", "Exception" ).
		:type message_level: unicode
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Method success.
		:rtype: bool
		"""

		for notifier in self.__notifiers[self.__maximum_notifiers - 1:]:
			notifier.duration=150
			notifier.hide_message()

		notification = Notification(message=message, time=time.time())

		self.register_notification(notification)

		notifier = Notification_QLabel(self.__container, **kwargs)

		# Signals / Slots.
		notifier.faded_out.connect(self.__notifier__faded_out)
		self.__container.size_changed.connect(notifier.resizeEvent)
		if notification_clicked_slot:
			notifier.notification_clicked.connect(notification_clicked_slot)
		else:
			notifier.setAttribute(Qt.WA_TransparentForMouseEvents)

		notifier.show_message(message, duration)

		self.__offset_notifiers(-notifier.height() - self.__notifiers_stack_padding)
		self.__notifiers.insert(0, notifier)

		if message_level == "Information":
			LOGGER.info("{0} | '{1}'.".format(self.__class__.__name__, self.format_notification(notification)))
		elif message_level == "Warning":
			LOGGER.warning("!> {0} | '{1}'.".format(self.__class__.__name__, self.format_notification(notification)))
		elif message_level == "Exception":
			LOGGER.error("!> {0} | '{1}'.".format(self.__class__.__name__, self.format_notification(notification)))

		return True

	def warnify(self, message, duration=3000, notification_clicked_slot=None, **kwargs):
		"""
		Displays an Application notification warning.

		:param message: Notification message.
		:type message: unicode
		:param duration: Notification display duration.
		:type duration: int
		:param notification_clicked_slot: Notification clicked slot.
		:type notification_clicked_slot: object
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Method success.
		:rtype: bool
		"""

		return self.notify(message,
						   duration,
						   notification_clicked_slot,
						   message_level="Warning",
						   color=QColor(220, 128, 64),
						   background_color=QColor(32, 32, 32),
						   border_color=QColor(220, 128, 64),
						   **kwargs)

	def exceptify(self, message, duration=3000, notification_clicked_slot=None, **kwargs):
		"""
		Displays an Application notification exception.

		:param message: Notification message.
		:type message: unicode
		:param duration: Notification display duration.
		:type duration: int
		:param notification_clicked_slot: Notification clicked slot.
		:type notification_clicked_slot: object
		:param \*\*kwargs: Keywords arguments.
		:type \*\*kwargs: \*\*
		:return: Method success.
		:rtype: bool
		"""

		return self.notify(message,
						   duration,
						   notification_clicked_slot,
						   message_level="Exception",
						   color=QColor(220, 64, 64),
						   background_color=QColor(32, 32, 32),
						   border_color=QColor(220, 64, 64),
						   **kwargs)
