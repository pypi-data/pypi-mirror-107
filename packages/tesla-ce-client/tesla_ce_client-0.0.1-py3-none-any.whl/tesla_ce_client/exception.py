#  Copyright (c) 2020 Xavier Baró
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as
#      published by the Free Software Foundation, either version 3 of the
#      License, or (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
""" Exception definition module"""
# Initialize Sentry Error tracker
import os
import sentry_sdk
from sentry_sdk import capture_exception

# Initialize the Sentry Error Tracker
if os.getenv('SENTRY_ENABLED') in ['1', 1, 'True', 'yes', 'true'] and os.getenv('SENTRY_DSN') is not None:
    sentry_sdk.init(
        os.getenv('SENTRY_DSN'),
        max_breadcrumbs=50,
        debug=os.getenv('DEBUG', '1') in ['1', 1, 'True', 'yes', 'true'],
        release=open(os.path.join(os.path.dirname(__file__), 'data', 'VERSION'), 'r').read(),
        environment=os.getenv('SENTRY_ENVIRONMENT', 'production')
    )


def tesla_report_exception(exception=None):
    """
        Send given exception to the Sentry Error Tracking system
        :param exception: Exception (optional)
        :return: Issue id or None if tracking is not enabled
    """
    if os.getenv('SENTRY_ENABLED') in ['1', 1, 'True', 'yes', 'true'] and os.getenv('SENTRY_DSN') is not None:
        return capture_exception(exception)
    return None


class TeslaException(Exception):
    """ Base class to raise exceptions """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        tesla_report_exception(self)


class TeslaConfigException(TeslaException):
    """ Class to raise configuration exceptions """
    pass


class TeslaVaultException(TeslaException):
    """ Class to raise vault related exceptions """
    pass


class TeslaAuthException(TeslaException):
    """ Class to raise authentication related exceptions """
    pass


class TeslaNotFoundException(TeslaException):
    """ Class raises when object is not found """
    pass


# Exceptions used by LTI.
class InternalException(TeslaException):
    """ Class raises when an unexpected error is found accessing the API """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BadRequestException(InternalException):
    """ Class raises when a bad request error is found accessing the API """
    pass


class ObjectNotFoundException(TeslaException):
    """ Class raises when a requested object does not exist """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NotImplementedException(TeslaException):
    """ Class raises when a not implemented method is called """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class LockedResourceException(TeslaException):
    """ Class raises when trying to access a locked resource """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
