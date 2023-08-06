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
""" TeSLA CE VLE Course Activity client module """
from .results import VleCourseActivityResultsClient


class VleCourseActivityClient():
    """
        VLE Course Activity client class
    """

    #: Results client
    _results = None

    def __init__(self, connector):
        """
            Default constructor

            :param connector: Connector object
            :type connector: Connector
        """
        # Connector object -> Connector
        self._connector = connector

    @property
    def result(self):
        """
            Access to the VLE course activity results related methods
            :return: Activity results controller object
            :rtype: VleCourseActivityResultsClient
        """
        if self._results is None:
            self._results = VleCourseActivityResultsClient(self._connector)
        return self._results

    def list(self, course_id, vle_id=None):
        """
            Get the list of activities

            :param course_id: Identifier of the course.
            :type course_id: str
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: List of activities
            :rtype: list
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        return self._connector.get('api/v2/vle/{}/course/{}/activity/'.format(vle_id, course_id))

    def get(self, course_id, activity_id, vle_id=None):
        """
            Get an activity

            :param course_id: Identifier of the course
            :type course_id: int
            :param activity_id: Identifier of the activity
            :type activity_id: int
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: Activity data
            :rtype: dict
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        return self._connector.get('api/v2/vle/{}/course/{}/activity/{}/'.format(vle_id, course_id, activity_id))

    def find_by_vle_id(self, course_id, vle_activity_type, vle_activity_id, vle_id=None):
        """
            Find an activity using the VLE identifiers

            :param course_id: Identifier of the course
            :type course_id: int
            :param vle_activity_type: Type of the activity in the VLE
            :type vle_activity_type: str
            :param vle_activity_id: Activity ID in the VLE
            :type vle_activity_id: str
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: Activity data
            :rtype: dict
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        result = self._connector.get('api/v2/vle/{}/course/{}/activity/?vle_activity_type={}&vle_activity_id={}'.format(
            vle_id, course_id, vle_activity_type, vle_activity_id)
        )

        if result['count'] == 1:
            return result['results'][0]

        return None

    def create(self, course_id, vle_activity_type, vle_activity_id, name, description, enabled=True, start=None,
               end=None, conf=None, vle_id=None):
        """
            Create a new activity

            :param course_id: Id of the course
            :type course_id: int
            :param vle_activity_type: Type of the activity in the VLE
            :type vle_activity_type: str
            :param vle_activity_id: ID of the activity in the VLE
            :type vle_activity_id: str
            :param name: Name of the activity
            :type name: str
            :param description: Description of the course
            :type description: str
            :param enabled: Whether this activity is enabled for TeSLA
            :type enabled: bool
            :param start: Start date of the course
            :type start: datetime
            :param end: End date of the course
            :type end: datetime
            :param conf: Additional configuration for the activity
            :type conf: dict
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int

            :return: New created course
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()

        return self._connector.post('api/v2/vle/{}/course/{}/activity/'.format(vle_id, course_id), body={
            "vle_activity_type": vle_activity_type,
            "vle_activity_id": vle_activity_id,
            "name": name,
            "description": description,
            "enabled": enabled,
            "start": start,
            "end": end,
            "conf": conf
        })

    def update(self, course_id, activity_id, vle_activity_type, vle_activity_id, name, description, enabled=True,
               start=None, end=None, conf=None, vle_id=None):
        """
            Update an activity

            :param course_id: Id of the course
            :type course_id: int
            :param activity_id: Id of the activity
            :type activity_id: int
            :param vle_activity_type: Type of the activity in the VLE
            :type vle_activity_type: str
            :param vle_activity_id: ID of the activity in the VLE
            :type vle_activity_id: str
            :param name: Name of the activity
            :type name: str
            :param description: Description of the course
            :type description: str
            :param enabled: Whether this activity is enabled for TeSLA
            :type enabled: bool
            :param start: Start date of the course
            :type start: datetime
            :param end: End date of the course
            :type end: datetime
            :param conf: Additional configuration for the activity
            :type conf: dict
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int

            :return: New updated activity
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()

        return self._connector.put('api/v2/vle/{}/course/{}/activity/{}/'.format(vle_id, course_id, activity_id),
                                   body={
                                       "vle_activity_type": vle_activity_type,
                                       "vle_activity_id": vle_activity_id,
                                       "name": name,
                                       "description": description,
                                       "enabled": enabled,
                                       "start": start,
                                       "end": end,
                                       "conf": conf
                                   })

    def get_instruments(self, course_id, activity_id, vle_id=None):
        """
            Get the instrument configuration for a given activity

            :param course_id: Identifier of the course
            :type course_id: int
            :param activity_id: Activity ID
            :type activity_id: int
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: Activity data
            :rtype: dict
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        return self._connector.get('api/v2/vle/{}/course/{}/activity/{}/instrument/'.format(
            vle_id, course_id, activity_id)
        )

    def add_instrument(self, course_id, activity_id, instrument_id, active, required, options=None,
                       alternative_to=None, vle_id=None):
        """
            Add a new instrument to the activity

            :param course_id: Identifier of the course
            :type course_id: int
            :param activity_id: Activity ID
            :type activity_id: int
            :param instrument_id: Id of the instrument
            :type instrument_id: int
            :param active: Whether this instrument is active
            :type active: bool
            :param required: Whether this instrument is required
            :type required: bool
            :param options: Options for this instrument
            :type options: dict
            :param alternative_to: Instrument assignment this instrument is an alternative to
            :type alternative_to: int
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: Instrument assignment data
            :rtype: dict
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        return self._connector.post('api/v2/vle/{}/course/{}/activity/{}/instrument/'.format(
            vle_id, course_id, activity_id),
            body={
                "instrument": instrument_id,
                "active": active,
                "required": required,
                "options": options,
                "alternative_to": alternative_to
            }
        )

    def update_instrument(self, course_id, activity_id, assignment_id, instrument_id, active, required, options=None,
                          alternative_to=None, vle_id=None):
        """
            Update an instrument configuration for a given activity

            :param course_id: Identifier of the course
            :type course_id: int
            :param activity_id: Activity ID
            :type activity_id: int
            :param assignment_id: Instrument assignment ID
            :type assignment_id: int
            :param instrument_id: Id of the instrument
            :type instrument_id: int
            :param active: Whether this instrument is active
            :type active: bool
            :param required: Whether this instrument is required
            :type required: bool
            :param options: Options for this instrument
            :type options: dict
            :param alternative_to: Instrument assignment this instrument is an alternative to
            :type alternative_to: int
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: Instrument assignment data
            :rtype: dict
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        return self._connector.put('api/v2/vle/{}/course/{}/activity/{}/instrument/{}/'.format(
            vle_id, course_id, activity_id, assignment_id),
            body={
                "instrument": instrument_id,
                "active": active,
                "required": required,
                "options": options,
                "alternative_to": alternative_to
            }
        )

    def find_instrument(self, course_id, activity_id, instrument_id, vle_id=None):
        """
            Find an assigned instrument

            :param course_id: Identifier of the course
            :type course_id: int
            :param activity_id: Activity ID
            :type activity_id: int
            :param instrument_id: Id of the instrument
            :type instrument_id: int
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: List of instrument assignments
            :rtype: dict
        """
        if vle_id is None:
            vle_id = self._connector.get_vle_id()
        result = self._connector.get('api/v2/vle/{}/course/{}/activity/{}/instrument/?instrument_id={}'.format(
            vle_id, course_id, activity_id, instrument_id),
        )

        if result['count'] == 1:
            return result['results'][0]

        return None

    def add_or_update_instrument(self, course_id, activity_id, instrument_id, active, required, options=None,
                                 alternative_to=None, vle_id=None):
        """
            Add a new instrument to the activity or update the information if this instrument already is assigned

            :param course_id: Identifier of the course
            :type course_id: int
            :param activity_id: Activity ID
            :type activity_id: int
            :param instrument_id: Id of the instrument
            :type instrument_id: int
            :param active: Whether this instrument is active
            :type active: bool
            :param required: Whether this instrument is required
            :type required: bool
            :param options: Options for this instrument
            :type options: dict
            :param alternative_to: Instrument assignment this instrument is an alternative to
            :type alternative_to: int
            :param vle_id: Identifier of the vle. If not provided take it from module configuration
            :type vle_id: int
            :return: Instrument assignment data
            :rtype: dict
        """
        assignment = self.find_instrument(course_id, activity_id, instrument_id)

        if assignment is None:
            resp = self.add_instrument(course_id, activity_id, instrument_id,active, required, options, alternative_to,
                                       vle_id)
        else:
            resp = self.update_instrument(course_id, activity_id, assignment['id'], instrument_id, active, required,
                                          options, alternative_to, vle_id)
        return resp
