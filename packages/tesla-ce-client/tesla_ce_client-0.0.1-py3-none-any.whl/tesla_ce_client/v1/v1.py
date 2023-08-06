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
""" TeSLA CE API v1 Client module """
from .tip import TipClient
from .tep import TepClient
from .api import ApiClient
from .rt import RtClient


class V1():
    """
        V1 Client class
    """
    def __init__(self, connector):
        """
            Default constructor

            :param connector: Connector object
            :type connector: Connector
        """
        self.tip = TipClient(connector)
        self.tep = TepClient(connector)
        self.rt = RtClient(connector)
        self.api = ApiClient(connector)
