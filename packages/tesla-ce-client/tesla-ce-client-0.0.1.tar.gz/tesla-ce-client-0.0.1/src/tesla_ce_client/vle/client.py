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
from .course import VleCourseClient


class VleClient():
    """
        VLE client class
    """

    #: Course client
    _course = None

    def __init__(self, connector):
        """
            Default constructor

            :param connector: Connector object
            :type connector: Connector
        """
        # Connector object -> Connector
        self._connector = connector

    @property
    def course(self):
        """
            Access to the VLE course related methods
            :return: Course controller object
            :rtype: VleCourseClient
        """
        if self._course is None:
            self._course = VleCourseClient(self._connector)
        return self._course

    def get(self, vle_id=None):
        """
            Get a VLE

            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: VLE object
            :rtype: dict
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        return self._connector.get('api/v2/vle/{}/'.format(vle_id))

    def list_instruments(self, vle_id=None):
        """
            Get the list of instruments

            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: List of instruments
            :rtype: dict
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        return self._connector.get('api/v2/vle/{}/instrument/'.format(vle_id))

    def get_launcher(self, vle_user_uid, vle_id=None, target="DASHBOARD", ttl=120, target_url=None, session_id=None):
        """
            Create a launcher for a user

            :param vle_user_uid: Identifier of the user in the vle.
            :type vle_user_uid: str
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :param target: The target for the launcher. Accepted values are "dashboard" (default) and "lapi".
            :type target: str
            :param target_url: The url where launcher is expected to be redirected.
            :type target_url: str
            :param ttl: The amount of time this launcher will be valid
            :type ttl: int
            :param session_id: The assessment session linked to this launcher
            :type session_id: int
            :return: Launcher id and token
            :rtype: dict
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()

        data = {
            "vle_user_uid": vle_user_uid,
            "target": target,
            "ttl": ttl,
            "session_id": session_id,
            "target_url": target_url
        }

        return self._connector.post('api/v2/vle/{}/launcher/'.format(vle_id), data)
