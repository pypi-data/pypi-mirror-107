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
""" TeSLA eAssessment Portal API client """

class TepClient():

    def __init__(self, connector):

        self._connector = connector

    # noinspection PyPep8Naming
    def getLearnerEvaluationStart(self, vle_id, tesla_id, activity_id, activity_type):
        return self._connector.get('api/v1/tep/learner/evaluation/start/{}/{}/{}/{}'.format(
            vle_id, tesla_id, activity_id, activity_type
        ))
