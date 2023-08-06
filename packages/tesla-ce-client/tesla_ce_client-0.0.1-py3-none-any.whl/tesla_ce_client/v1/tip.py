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
""" TeSLA Identity Provider API client """


class TipClient():

    def __init__(self, connector):

        self._connector = connector

    # noinspection PyPep8Naming
    def getTeslaId(self, mail):
        """
            Get the learner ID from learner mail

            :param mail: A learner mail
            :type mail: str

        """
        return self._connector.post('api/v1/tip/users/id', {"mail": mail})

    # noinspection PyPep8Naming
    def getTeslaIds(self, mails):
        """
            Get the learner ID of a list of learner mails

            :param mails: List of learner mails
            :type mails: list

        """
        return self._connector.post('api/v1/tip/users/multiple/id', {"mails": mails})
