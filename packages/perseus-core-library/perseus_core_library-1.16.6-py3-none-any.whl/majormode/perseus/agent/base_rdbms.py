# Copyright (C) 2020 Majormode.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from majormode.perseus.agent.base import BaseAgent
from majormode.perseus.utils import rdbms


class BaseRdbmsAgent(BaseAgent):
    def __init__(
            self,
            rdbms_properties,
            logging_formatter=None,
            logging_level=None,
            logger_name=None,
            name=None):
        """
        Build an object `BaseAgent`.


        :param rdbms_properties: A dictionary of connection properties::

               {
                 None: {
                   'rdbms_hostname': "...",
                   'rdbms_port': ...,
                   'rdbms_database_name': "...",
                   'rdbms_account_username': '...'
                   'rdbms_account_password': '...'
                 },
                 'tag': {
                   'rdbms_hostname': "...",
                   'rdbms_port': ...,
                   'rdbms_database_name': "...",
                   'rdbms_account_username': '...'
                   'rdbms_account_password': '...'
                 },
                 ...
               }

               The key `None` is the default tag.

        :param logging_formatter: An object `Formatter` to set for this handler.

        :param logger_name: Name of the logger to add the logging handler to.
            If `logger_name` is `None`, the function attaches the logging
            handler to the root logger of the hierarchy.

        :param logging_level: The threshold for the logger to `level`.  Logging
            messages which are less severe than `level` will be ignored;
            logging messages which have severity level or higher will be
            emitted by whichever handler or handlers service this logger,
            unless a handler's level has been set to a higher severity level
            than `level`.

        :param name: Name of the agent.
        """
        super().__init__(
            # logging_formatter=logging_formatter,
            # logger_name=logger_name,
            # logging_level=logging_level,
            name=name)

        self.__rdbms_properties = {None: rdbms_properties}

    def _acquire_connection(self, auto_commit=False, connection=None):
        """
        Return a connection to a Relational DataBase Management System (RDBMS)
        the most appropriate for the service requesting this connection.


        :param auto_commit: Indicate whether the transaction needs to be
            committed at the end of the session.

        :param connection: An object `RdbmsConnection` supporting the Python
            clause `with ...`.


        :return: An object `RdbmsConnection` to be used supporting the
            Python clause `with ...:`.
        """
        return rdbms.RdbmsConnection.acquire_connection(
            self.__rdbms_properties,
            auto_commit=auto_commit,
            connection=connection)

    def start(self):
        raise NotImplementedError()

