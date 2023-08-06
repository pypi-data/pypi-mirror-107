# Copyright (C) 2019 Majormode.  All rights reserved.
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

import argparse
import getpass
import logging
import sys
import time
import traceback


class BaseAgent:
    # Logging levels supported by the base agent.
    LOGGING_LEVELS = (
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG
    )

    # Default format to use by the logger.
    DEFAULT_LOGGING_FORMATTER = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    # Default idle duration in seconds of the agent between two consecutive
    # iterations.
    DEFAULT_IDLE_TIME = 5 * 60

    def __init__(
            self,
            argument_parser_description=None,
            include_rdbms_arguments=False,
            include_smtp_arguments=False,
            name=None):
        """
        Build an object `BaseAgent`.


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
        self.__name = name or self.__class__.__name__

        # Setup the command line argument parser.
        self._argument_parser = self.__build_argument_parser(description=argument_parser_description)
        if include_rdbms_arguments:
            self.__include_rdbms_arguments(self._argument_parser)
        if include_smtp_arguments:
            self.__include_smtp_properties(self._argument_parser)

        self.__arguments = None

    @classmethod
    def __build_argument_parser(
            cls,
            description=None):
        parser = argparse.ArgumentParser(description=description)

        parser.add_argument(
            '--debug',
            dest='logging_level',
            metavar='LEVEL',
            required=False,
            default=0,
            type=int,
            help=f"specify the logging level (value between 0 and {len(cls.LOGGING_LEVELS) - 1}, "
                 "from critical to debug)")

        return parser

    @staticmethod
    def __get_console_handler(logging_formatter=DEFAULT_LOGGING_FORMATTER):
        """
        Return a logging handler that sends logging output to the system's
        standard output.


        :param logging_formatter: An object `Formatter` to set for this handler.


        :return: An instance of the `StreamHandler` class.
        """
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging_formatter)
        return console_handler

    @staticmethod
    def __include_rdbms_arguments(parser):
        """
        Add the command line arguments to define the properties to connect to
        a Relational DataBase Management System (RDBMS) server


        :param parser: An object `ArgumentParser`.


        :return: The object `ArgumentParser` that has been passed to this
            function.
        """
        parser.add_argument(
            '--db-hostname',
            required=False,
            help="specify the host name of the machine on which the server is running.")

        parser.add_argument(
            '--db-port',
            required=False,
            type=int,
            default=5432,
            help="specify the database TCP port or the local Unix-domain socket file "
                 "extension on which the server is listening for connections. Defaults "
                 "to the port specified at compile time, usually 5432.")

        parser.add_argument(
            '--db-name',
            required=True,
            help='Specify the name of the database to connect to.')

        parser.add_argument(
            '--db-username',
            required=False,
            default=getpass.getuser(),
            help="connect to the database as the user username instead of the default.")

    @staticmethod
    def __include_smtp_properties(parser):
        """
        Add the command line arguments to define the properties to connect to
        a Simple Mail Transfer Protocol (SMTP) server


        :param parser: An object `ArgumentParser`.


        :return: The object `ArgumentParser` that has been passed to this
            function.
        """
        parser.add_argument(
            '--smtp-hostname',
            required=True,
            help="specify the host name of the machine on which the SMTP server is running.")

        parser.add_argument(
            '--smtp-username',
            required=True,
            help='specify the username/email address to connect to the SMPT server.')

        parser.add_argument(
            '--smtp-port',
            required=False,
            type=int,
            default=587,
            help="specify the TCP port or the local Unix-domain socket file extension on "
                 "which the SMTP server is listening for connections.")

    @classmethod
    def __setup_logger(
            cls,
            logging_formatter=DEFAULT_LOGGING_FORMATTER,
            logging_level=logging.INFO,
            logger_name=None):
        """
        Setup a logging handler that sends logging output to the system's
        standard output.


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


        :return: An object `Logger`.
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging_level)
        logger.addHandler(cls.__get_console_handler(logging_formatter=logging_formatter))
        logger.propagate = False
        return logger

    @property
    def name(self):
        return self.__name

    def _run(self):
        raise NotImplementedError("This method MUST be implemented by the inheriting class")

    def start(
            self,
            logging_formatter=None,
            logger_name=None):
        # Convert argument strings to objects and assign them as attributes of
        # the namespace.  This is done here to give the chance to the inheriting
        # class to add its custom arguments in its constructor.
        self.__arguments = self._argument_parser.parse_args()

        # Setup the logging handler that sends logging output to the system's
        # standard output.  This is done here as we need the argument strings to
        # be converted into object to set up the logging handler (cf. logging
        # level).
        self.__setup_logger(
            logging_formatter=logging_formatter or self.DEFAULT_LOGGING_FORMATTER,
            logging_level=self.__arguments.logging_level or logging.INFO,
            logger_name=logger_name or self.__name)

        self._run()


class LooperBaseAgent(BaseAgent):
    def __init__(self,
                 idle_time=None,
                 logging_formatter=None,
                 logging_level=None,
                 logger_name=None,
                 name=None):
        super().__init__(
            logging_formatter=logging_formatter,
            logging_level=logging_level,
            logger_name=logger_name,
            name=name)

        self.__idle_time = idle_time or self.DEFAULT_IDLE_TIME

    def _run(self):
        raise NotImplementedError("This method MUST be implemented by the inheriting class")

    def start(self):
        try:
            while True:
                did_something = self._run()
                if not did_something:
                    logging.debug("Breathing a little bit...")
                    time.sleep(self.__idle_time)

        except KeyboardInterrupt:
            logging.info(f"Shutting down {self.name}...")

        except Exception:
            logging.error(traceback.format_exc())
