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
""" TeSLA CE CLient Module """
import os
import deprecation
from .connector import Connector
from .vle import VleClient
from .provider import ProviderClient
from .v1 import V1

__version__ = open(os.path.join(os.path.dirname(__file__), 'data', 'VERSION'), 'r').read()


class Client():
    """
        TeSLA CE Client class
    """
    #: Connector object -> Connector
    _connector = None

    #: API version 1 client -> V1
    _v1 = None

    #: VLE client -> VLEClient
    _vle = None

    #: Provider client -> ProviderClient
    _provider = None

    #: Verification client -> Verification
    _verification = None

    #: Notification client -> Notification
    _notification = None

    def __init__(self, api_url=None, role_id=None, secret_id=None, verify_ssl=None):

        # Find configuration if not provided
        if api_url is None or role_id is None or secret_id is None:
            conf = self._find_config()
            if api_url is None:
                api_url = conf['api_url']
            if role_id is None:
                role_id = conf['role_id']
            if secret_id is None:
                secret_id = conf['secret_id']
            if verify_ssl is None:
                verify_ssl = conf['verify_ssl']

        # Create the connector to communicate with TeSLA CE
        self._connector = Connector(api_url, role_id, secret_id, verify_ssl)

    @classmethod
    def _find_config_value(cls, base_key):
        """
            Check if a given key is available as environment variable or secret

            :param base_key: Base name of the key
            :type base_key: str
            :return: Value of the key if found or None
        """
        key = base_key.upper()
        if os.getenv(key) is not None:
            return os.getenv(key)
        if os.getenv('{}_FILE'.format(key)) is not None:
            with open(os.getenv('{}_FILE'.format(key)), 'r') as key_fh:
                return key_fh.read()
        if os.path.exists('/run/secrets/{}'.format(key)):
            with open('/run/secrets/{}'.format(key), 'r') as secret_fh:
                return secret_fh.read()
        return None

    @classmethod
    def _find_config(cls):
        """
            Find configuration in environment and secrets

            :return: Object with configuration values
            :rtype: dict
        """
        verify_ssl = True
        if cls._find_config_value('VERIFY_SSL') is not None:
            if cls._find_config_value('VERIFY_SSL') in ['0', 0, 'false', 'False']:
                verify_ssl = False
            else:
                verify_ssl = cls._find_config_value('VERIFY_SSL')

        return {
            'api_url': cls._find_config_value('API_URL'),
            'role_id': cls._find_config_value('ROLE_ID'),
            'secret_id': cls._find_config_value('SECRET_ID'),
            'verify_ssl': verify_ssl
        }

    @property
    @deprecation.deprecated(deprecated_in="1.0.0", removed_in="2.0.0",
                            current_version=__version__,
                            details="You are using v1 methods. Move to new methods.")
    def v1(self):
        """
            Access to the old API v1 methods
            :return: Old API v1 controller object
            :rtype: ClientV1
        """
        if self._v1 is None:
            self._v1 = V1(self._connector)
        return self._v1

    @property
    def vle(self):
        """
            Access to the VLE related methods
            :return: VLE controller object
            :rtype: VleClient
        """
        if self._vle is None:
            self._vle = VleClient(self._connector)
        return self._vle

    @property
    def provider(self):
        """
            Access to the Provider related methods
            :return: Provider controller object
            :rtype: ProviderClient
        """
        if self._provider is None:
            self._provider = ProviderClient(self._connector)
        return self._provider

    @property
    def config(self):
        """
            Get current module configuration
            :return: Module configuration
            :rtype: dict
        """
        return self._connector.config

    @property
    def module(self):
        """
            Get current module information
            :return: Module information
            :rtype: dict
        """
        return self._connector.module

    def get_next(self, list):
        """
            Get the next group of results from a list
            :param list: List of results
            :type list: dict
            :return: Next group of results
            :rtype: dict
        """
        if 'next' in list and list['next'] is not None:
            return self._connector.get(list['next'])
        return None

    def get_previous(self, list):
        """
            Get the previous group of results from a list
            :param list: List of results
            :type list: dict
            :return: Previous group of results
            :rtype: dict
        """
        if 'previous' in list and list['previous'] is not None:
            return self._connector.get(list['previous'])
        return None
