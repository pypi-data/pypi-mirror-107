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
""" TeSLA CE Verification Client module """
import io
import simplejson
import requests
from enum import Enum
from tesla_ce_client import exception


class RequestResultStatus(Enum):
    """ RequestResultStatus definition """
    PENDING = 0
    PROCESSED = 1
    ERROR = 2
    TIMEOUT = 3
    MISSING_PROVIDER = 4
    MISSING_ENROLMENT = 5
    PROCESSING = 6
    WAITING_EXTERNAL_SERVICE = 7


class Verification:
    """
        Verification Client class
    """
    def __init__(self, connector):
        """
            Default constructor

            :param connector: Connector object
            :type connector: Connector
        """
        # Connector object -> Connector
        self._connector = connector

    def get_provider_request_result(self, provider_id, request_id):
        """
            Get verification request result for a provider

            :param provider_id: Provider ID
            :type provider_id: int
            :param request_id: Request result id
            :type request_id: int
            :return: Verification request result
            :rtype: dict
        """
        return self._connector.get('/api/v2/provider/{}/request/{}/'.format(provider_id, request_id))

    def set_provider_request_result(self, provider_id, request_id, result):
        """
            Store validation result for a verification request for a provider

            :param provider_id: Provider ID
            :type provider_id: int
            :param request_id: Request result id
            :type request_id: int
            :param result: Verification result
            :type result: dict
        """
        if 'audit' in result:
            result['audit_data'] = result['audit']
            del result['audit']
        return self._connector.put('/api/v2/provider/{}/request/{}/'.format(provider_id, request_id), body=result)

    def set_provider_request_status(self, provider_id, request_id, status):
        """
            Change provider request status

            :param provider_id: Provider ID
            :type provider_id: int
            :param request_id: Request result id
            :type request_id: int
            :param status: Request's status. Valid status: 1 ok, 2 error, 3 timeout, 6 processing, 7 waiting external
            service
            :type status: RequestResultStatus

            :return:
        """
        return self._connector.post('/api/v2/provider/{}/request/{}/status/'.format(provider_id, request_id),
                                    body={"status": status.value})
