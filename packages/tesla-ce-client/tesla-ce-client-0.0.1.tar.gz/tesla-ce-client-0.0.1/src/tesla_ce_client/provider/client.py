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
""" TeSLA CE VLE client module """
from .enrolment import Enrolment
from .verification import Verification
from .notification import Notification


class ProviderClient():
    """
        Provider client class
    """

    #: Enrolment client
    _enrolment = None

    #: Verification client
    _verification = None

    #: Notification client
    _notification = None

    def __init__(self, connector):
        """
            Default constructor

            :param connector: Connector object
            :type connector: Connector
        """
        # Connector object -> Connector
        self._connector = connector

    @property
    def enrolment(self):
        """
            Access to the Provider enrolment related methods
            :return: Enrolment controller object
            :rtype: Enrolment
        """
        if self._enrolment is None:
            self._enrolment = Enrolment(self._connector)
        return self._enrolment

    @property
    def verification(self):
        """
            Access to the Provider verification related methods
            :return: Verification controller object
            :rtype: Verification
        """
        if self._verification is None:
            self._verification = Verification(self._connector)
        return self._verification

    @property
    def notification(self):
        """
            Access to the Provider notification related methods
            :return: Notification controller object
            :rtype: Notification
        """
        if self._notification is None:
            self._notification = Notification(self._connector)
        return self._notification

    def get(self, provider_id=None):
        """
            Get a VLE

            :param provider_id: Identifier of the provider. If not provided take it from module configuration
            :type provider_id: int
            :return: Provider object
            :rtype: dict
        """
        if provider_id is None:
            provider_id = self._connector.get_provider_id()
        return self._connector.get('/api/v2/provider/{}/'.format(provider_id))
