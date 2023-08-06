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
""" TeSLA CE VLE Activity client module """
from .activity import VleCourseActivityClient
from .learner import VleCourseLearnerClient


class VleCourseClient():
    """
        VLE Course client class
    """

    #: Activity client
    _activity = None

    #: Learner client
    _learner = None

    def __init__(self, connector):
        """
            Default constructor

            :param connector: Connector object
            :type connector: Connector
        """
        # Connector object -> Connector
        self._connector = connector

    @property
    def activity(self):
        """
            Access to the VLE course activity related methods
            :return: Activity controller object
            :rtype: VleCourseActivityClient
        """
        if self._activity is None:
            self._activity = VleCourseActivityClient(self._connector)
        return self._activity

    @property
    def learner(self):
        """
            Access to the VLE course learner related methods
            :return: Learner controller object
            :rtype: VleCourseLearnerClient
        """
        if self._learner is None:
            self._learner = VleCourseLearnerClient(self._connector)
        return self._learner

    def find_by_vle_id(self, vle_course_id, vle_id=None):
        """
            Get the learner from learner institution code

            :param vle_course_id: Identifier of the course in the vle
            :type vle_course_id: str | int
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: Course object
            :rtype: dict
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        result = self._connector.get('api/v2/vle/{}/course/?vle_course_id={}'.format(vle_id, vle_course_id))
        if result['count'] == 1:
            return result['results'][0]
        return None

    def list(self, vle_id=None):
        """
            Get the list of courses

            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: List of courses
            :rtype: list
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        return self._connector.get('api/v2/vle/{}/course/'.format(vle_id))

    def create(self, vle_course_id, code, description, start=None, end=None, vle_id=None):
        """
            Create a new course

            :param vle_course_id: Id of the course in the VLE
            :type vle_course_id: str
            :param code: Code of the course
            :type code: str
            :param description: Description of the course
            :type description: str
            :param start: Start date of the course
            :type start: datetime
            :param end: End date of the course
            :type end: datetime
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int

            :return: New created course
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()

        return self._connector.post('api/v2/vle/{}/course/'.format(vle_id), body={
            "vle_course_id": vle_course_id,
            "code": code,
            "description": description,
            "start": start,
            "end": end
        })
