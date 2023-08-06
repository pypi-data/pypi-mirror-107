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
""" Test module for TeSLA CE client creation """
import os
import pytest
import mock
from requests import exceptions
from tesla_ce_client import Client
from tesla_ce_client.exception import TeslaConfigException

@mock.patch.dict(os.environ, {}, clear=True)
def test_client_creation():
    # Check that client cannot be created without API URL argument
    try:
        client = Client()
        pytest.fail('Client creation without API URL should not be possible')
    except TeslaConfigException as exc:
        assert 'API URL' in str(exc)

    # Provide API URL as argument
    try:
        client = Client(api_url='https://localhost/invalid-path/to/api')
        pytest.fail('Client creation without API URL should not be possible')
    except TeslaConfigException as exc:
        assert 'API URL' not in str(exc)

    # Provide API URL as environment variable
    try:
        with mock.patch.dict(os.environ, {'API_URL': 'https://localhost/invalid-path/to/api'}):
            client = Client()
        pytest.fail('Client creation without API URL should not be possible')
    except TeslaConfigException as exc:
        assert 'API URL' not in str(exc)

    # Check that client cannot be created without credentials
    try:
        client = Client(api_url='https://localhost/invalid-path/to/api')
        pytest.fail('Client creation without credentials should not be possible')
    except TeslaConfigException as exc:
        assert 'Missing credentials' in str(exc)
    try:
        client = Client(api_url='https://localhost/invalid-path/to/api', role_id='test-role')
        pytest.fail('Client creation without secret should not be possible')
    except TeslaConfigException as exc:
        assert 'Missing credentials' in str(exc)
    try:
        client = Client(api_url='https://localhost/invalid-path/to/api', secret_id='test-secret')
        pytest.fail('Client creation without role should not be possible')
    except TeslaConfigException as exc:
        assert 'Missing credentials' in str(exc)

    # Check that credentials are taken via arguments
    try:
        client = Client(api_url='https://localhost/invalid-path/to/api', role_id='test-role', secret_id='test-secret')
        pytest.fail('Client creation without role should not be possible')
    except exceptions.ConnectionError as exc:
        # Once all arguments are provided we expect a connection error
        pass

    # Check that credentials are taken via environment
    try:
        with mock.patch.dict(os.environ, {
            'API_URL': 'https://localhost/invalid-path/to/api',
            'ROLE_ID': 'test-role',
            'SECRET_ID': 'test-secret'
        }):
            client = Client(api_url='https://localhost/invalid-path/to/api', role_id='test-role',
                            secret_id='test-secret')
        pytest.fail('Client creation without role should not be possible')
    except exceptions.ConnectionError as exc:
        # Once all arguments are provided we expect a connection error
        pass
