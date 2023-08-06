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
""" TeSLA CE VLE Course Learner client module """


class VleCourseLearnerClient():
    """
        VLE Course Learner client class
    """
    def __init__(self, connector):
        """
            Default constructor

            :param connector: Connector object
            :type connector: Connector
        """
        # Connector object -> Connector
        self._connector = connector

    def list(self, course_id, vle_id=None):
        """
            Get the list of learners

            :param course_id: Identifier of the course.
            :type course_id: str
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: List of learners
            :rtype: list
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        return self._connector.get('api/v2/vle/{}/course/{}/learner/'.format(vle_id, course_id))

    def get(self, course_id, learner_id, vle_id=None):
        """
            Get a learner

            :param course_id: Identifier of the course
            :type course_id: int
            :param learner_id: Identifier of the learner
            :type learner_id: int
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: List of activities
            :rtype: list
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        return self._connector.get('api/v2/vle/{}/course/{}/activity/{}/'.format(vle_id, course_id, learner_id))

    def find_by_uid(self, course_id, uid, vle_id=None):
        """
            Get a learner

            :param course_id: Identifier of the course
            :type course_id: int
            :param uid: UID of the learner
            :type uid: str
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: Learner data
            :rtype: dict
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        result = self._connector.get('api/v2/vle/{}/course/{}/learner/?uid={}'.format(
            vle_id, course_id, uid)
        )

        if result['count'] == 1:
            return result['results'][0]

        return None

    def find_by_mail(self, course_id, mail, vle_id=None):
        """
            Get a learner

            :param course_id: Identifier of the course
            :type course_id: int
            :param mail: Mail of the learner
            :type mail: str
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: Learner data
            :rtype: dict
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        result = self._connector.get('api/v2/vle/{}/course/{}/learner/?mail={}'.format(
            vle_id, course_id, mail)
        )

        if result['count'] == 1:
            return result['results'][0]

        return None

    def find_by_lerner_id(self, course_id, learner_id, vle_id=None):
        """
            Get a learner

            :param course_id: Identifier of the course
            :type course_id: int
            :param learner_id: Learner learner_id UUID
            :type learner_id: str
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: Learner data
            :rtype: dict
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        result = self._connector.get('api/v2/vle/{}/course/{}/learner/?lerner_id={}'.format(
            vle_id, course_id, learner_id)
        )

        if result['count'] == 1:
            return result['results'][0]

        return None

