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
""" TeSLA CE VLE Course Activity results client module """


class VleCourseActivityResultsClient():
    """
        VLE Course Activity client class
    """
    def __init__(self, connector):
        """
            Default constructor

            :param connector: Connector object
            :type connector: Connector
        """
        # Connector object -> Connector
        self._connector = connector

    def list(self, course_id, activity_id, vle_id=None):
        """
            Get the list of results for an activity

            :param course_id: Identifier of the course.
            :type course_id: str
            :param activity_id: Identifier of the activity
            :type activity_id: int
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: List of results for the activity
            :rtype: list
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        return self._connector.get('api/v2/vle/{}/course/{}/activity/{}/report/'.format(vle_id,
                                                                                        course_id,
                                                                                        activity_id))

    def get(self, course_id, activity_id, report_id, vle_id=None):
        """
            Get the detail of a single result

            :param course_id: Identifier of the course.
            :type course_id: str
            :param activity_id: Identifier of the activity
            :type activity_id: int
            :param report_id: Identifier of the report
            :type report_id: int
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: Result detail
            :rtype: object
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        return self._connector.get('api/v2/vle/{}/course/{}/activity/{}/report/{}/'.format(vle_id,
                                                                                           course_id,
                                                                                           activity_id,
                                                                                           report_id))

    def list_requests(self, course_id, activity_id, learner_id, instrument=None, vle_id=None):
        """
            Get the list of learner requests for an activity

            :param course_id: Identifier of the course.
            :type course_id: str
            :param activity_id: Identifier of the activity
            :type activity_id: int
            :param activity_id: Identifier of the activity
            :type activity_id: int
            :param instrument: Filter requests for provided instrument
            :type instrument: int
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: List of results for the activity
            :rtype: list
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        if instrument is None:
            return self._connector.get('api/v2/vle/{}/course/{}/activity/{}/learner/{}/request/'.format(vle_id,
                                                                                                        course_id,
                                                                                                        activity_id,
                                                                                                        learner_id)
                                       )
        return self._connector.get('api/v2/vle/{}/course/{}/activity/{}/learner/{}/request/?instruments={}'.format(
            vle_id,
            course_id,
            activity_id,
            learner_id,
            instrument)
        )
