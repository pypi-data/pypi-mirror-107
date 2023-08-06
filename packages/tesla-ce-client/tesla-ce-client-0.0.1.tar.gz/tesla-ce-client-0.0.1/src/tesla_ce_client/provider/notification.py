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
""" TeSLA CE Notifications Client module """


class Notification():
    """
        Notifications Client class
    """
    def __init__(self, connector):
        """
            Default constructor

            :param connector: Connector object
            :type connector: Connector
        """
        self._connector = connector

    def get(self, provider_id, notification_id):
        """
            Get a notification for a provider

            :param provider_id: Identifier of the provider
            :type provider_id: int
            :param notification_id: Id of the notification
            :type notification_id: int
            :return: Notification object
            :rtype: dict
        """
        return self._connector.get('/api/v2/provider/{}/notification/{}/'.format(provider_id, notification_id))

    def update_or_create(self, provider_id, key, when, info=None):
        """
            Updates or create a notification for a given provider

            :param provider_id: Identifier of the provider
            :type provider_id: int
            :param key: Key of the notification
            :type key: str
            :return: Created or updated Notification
            :rtype: Notification
        """
        return self._connector.post('/api/v2/provider/{}/notification/'.format(provider_id),
                                    body={
                                        'key': key,
                                        'when': when.isoformat(),
                                        'info': info
                                    })

    def delete(self, provider_id, notification_id):
        """
            Get a notification for a provider

            :param provider_id: Identifier of the provider
            :type provider_id: int
            :param notification_id: Id of the notification
            :type notification_id: int
        """
        self._connector.delete('/api/v2/provider/{}/notification/{}/'.format(provider_id, notification_id))
