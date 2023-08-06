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
import base64
import requests
import json
import datetime
from .exception import (
    TeslaConfigException,
    ObjectNotFoundException,
    InternalException,
    NotImplementedException,
    TeslaAuthException,
    BadRequestException,
)


class Connector():
    """
        Connector class to manage connections with the APIs
    """
    _config = None

    def __init__(self, api_url, role_id, secret_id, verify_ssl=True):
        """
            Default constructor.

            :param api_url: TeSLA API URL
            :type api_url: str
            :param role_id: RoleId to authenticate with Vault
            :type role_id: str
            :param secret_id: SecretId to authenticate with Vault
            :type secret_id: str
            :param verify_ssl: Whether to verify certificate of the server
            :type verify_ssl: bool

        """

        if api_url is None:
            raise TeslaConfigException('Missing API URL')

        if role_id is None or secret_id is None:
            raise TeslaConfigException('Missing credentials')

        # Store initial configuration
        self._api_url = api_url
        self._role_id = role_id
        self._secret_id = secret_id
        self._verify_ssl = verify_ssl

        # Check API_URL
        if self._api_url.endswith('/'):
            self._api_url = self._api_url[:-1]

        # Authenticate with the API
        self._authenticate()

    def _authenticate(self):
        # Authenticate with the API
        auth_resp = requests.post('{}/api/v2/auth/approle'.format(self._api_url),
                                  verify=self._verify_ssl,
                                  json={
                                      'role_id': self._role_id,
                                      'secret_id': self._secret_id
                                  })
        if auth_resp.status_code != 200:
            raise TeslaAuthException('Invalid credentials')

        # Store authentication data
        self._module = auth_resp.json()

        # Initialize the token
        self._token = self._module['token']
        self._token_exp = self._get_token_expiration(self._token['access_token'])

    def get_vle_id(self):
        """
            Obtain the vle ID for current VLE

            :return: VLE ID if current module is a VLE, or None if provided credentials are not for a VLE
            :rtype: int
        """
        if 'vle_id' in self._module:
            return self._module['vle_id']
        return None

    def get_provider_id(self):
        """
            Obtain the provider ID for current Provider

            :return: Provider ID if current module is a Provider, or None if provided credentials are not for a Provider
            :rtype: int
        """
        if 'provider_id' in self._module:
            return self._module['provider_id']
        return None

    @staticmethod
    def _get_token_expiration(token):
        payload = token.split('.')[1]
        payload = json.loads(base64.b64decode(payload))

        return datetime.datetime.utcfromtimestamp(payload['exp'])

    @staticmethod
    def _check_response_status(status_code, content=''):
        """
            Check the status code returned by an executed request
            :param status_code: Status code returned by the request
            :type status_code: int
        """
        if status_code == 400:
            raise BadRequestException("HTTP 400, Bad Request: {}".format(content))
        if status_code == 404:
            raise ObjectNotFoundException("HTTP 404, Not Found")
        if status_code == 501:
            raise NotImplementedException("HTTP 501, Not implemented")
        if status_code >= 300:
            raise InternalException("Something Wrong: HTTP " + str(status_code))

    def _get_token(self):
        """
            Get the JWT token to authenticate with the API
            :return: JWT token
            :rtype: str
        """
        # Check the validity of the token
        if self._token_exp < datetime.datetime.utcnow() + datetime.timedelta(minutes=5):
            headers = {'Authorization': 'JWT {}'.format(self._token['refresh_token'])}
            # Refresh the token
            refresh_resp = requests.post('{}/api/v2/auth/token/refresh'.format(self._api_url),
                                         headers=headers,
                                         verify=self._verify_ssl,
                                         json={'token': self._token['access_token']})
            if refresh_resp.status_code == 200:
                self._token = refresh_resp.json()['token']
                self._token_exp = self._get_token_expiration(self._token['access_token'])
            else:
                try:
                    self._authenticate()
                except TeslaAuthException:
                    raise TeslaAuthException('Authentication failed during token refresh')

        return self._token['access_token']

    def executor(self, method, url, body=None):
        """
            Execute an HTTP request

            :param method: Method to be used (get, post, put, delete, patch)
            :type method: str
            :param url: Url to send the request
            :type url: str
            :param body: Data to include in the request
            :type body: dict
            :return: The response to the request
            :rtype: dict
        """
        # Build the request url
        if url.startswith(self._api_url):
            # Absolute url
            request_url = url
        else:
            # Relative url
            if url.startswith('/'):
                request_url = '{}{}'.format(self._api_url, url)
            else:
                request_url = '{}/{}'.format(self._api_url, url)
            request_url = request_url.replace('//', '/')
            request_url = request_url.replace(':/', '://')

        # Call the method
        headers = {'Authorization': 'JWT {}'.format(self._get_token())}
        resp = requests.request(method=method, url=request_url, json=body, headers=headers, verify=self._verify_ssl)

        # Take actions with the response
        self._check_response_status(resp.status_code, resp.content)

        # Consider the no content response
        if resp.status_code == 204:
            return None

        return resp.json()

    def get(self, url):
        """
            Execute a GET HTTP request
            :param url: Url to send the request
            :type url: str
            :return: The response to the request
            :rtype: dict
        """
        return self.executor('get', url=url)

    def delete(self, url):
        """
            Execute a DELETE HTTP request
            :param url: Url to send the request
            :type url: str
            :return: The response to the request
            :rtype: dict
        """
        return self.executor('delete', url=url)

    def post(self, url, body=None):
        """
            Execute a POST HTTP request
            :param url: Url to send the request
            :type url: str
            :param body: Data to include in the request
            :type body: dict
            :return: The response to the request
            :rtype: dict
        """
        return self.executor('post', url=url, body=body)

    def patch(self, url, body=None):
        """
            Execute a PATCH HTTP request
            :param url: Url to send the request
            :type url: str
            :param body: Data to include in the request
            :type body: dict
            :return: The response to the request
            :rtype: dict
        """
        return self.executor('patch', url=url, body=body)

    def put(self, url, body=None):
        """
            Execute a PUT HTTP request
            :param url: Url to send the request
            :type url: str
            :param body: Data to include in the request
            :type body: dict
            :return: The response to the request
            :rtype: dict
        """
        return self.executor('put', url=url, body=body)

    @property
    def config(self):
        """
            Access to module configuration
            :return: Module configuration
            :rtype: dict
        """
        return self._module['config']

    @property
    def module(self):
        """
            Access to module data
            :return: Module configuration
            :rtype: dict
        """
        return self._module
