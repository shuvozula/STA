__author__ = 'Spondon Saha'

import os
import logging

LOGGING_LEVEL = logging.DEBUG


class Error(Exception):
    """Native exception class."""
    pass


class Utils(object):
    """Utility class for commonly used methods."""

    def __init__(self, debug_mode=False):
        """Constructor.

        Arguments:
            debug_mode: a boolean flag for signifying debug mode.

        Raises:
            None
        """
        self.debug_mode = debug_mode
        self.SetupLogging()

    def SetupLogging(self):
        """Sets up the logging parameters.

        Uses the logging library to create a log file, set the log-level,
        log file-mode, logging format, etc.

        Arguments:
            None

        Raises:
            None
        """
        log_file = 'sta.out'
        log_dir = '/tmp/'
        logging.basicConfig(filename=os.path.join(log_dir, log_file),
                            filemode='w',
                            level=LOGGING_LEVEL,
                            format='%(asctime)s %(levelname)s:: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    