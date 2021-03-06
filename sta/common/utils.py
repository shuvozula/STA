__author__ = 'Spondon Saha'

import os
import logging
from sta.common.conf import DEFAULT_LOGGING_LEVEL, DEFAULT_LOG_FILE, \
                            DEFAULT_LOG_DIR


class Error(Exception):
    """Native exception class."""
    pass


def SetupLogging(logging_level=DEFAULT_LOGGING_LEVEL,
                 log_filepath=os.path.join(DEFAULT_LOG_DIR, DEFAULT_LOG_FILE)):
    """Sets up the logging parameters.

    Uses the logging library to create a log file, set the log-level,
    log file-mode, logging format, etc.

    Arguments:
        logging_level(optional): A valid logging level, usually DEBUG, INFO,
        WARNING, etc.
        log_filepath(optional): Log directory file-path

    Raises:
        None
    """
    logging.basicConfig(filename=log_filepath,
                        filemode='w',
                        level=logging_level,
                        format='%(asctime)s %(levelname)s:: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

def HasMember(c1, c2):
    """Checks if 2 coalitions has overlapping robots.

    For maintaining the Partition property, we need to make sure that
    all coalitions on a certain path in the STA tree have non-overlapping
    coalitions.

    Arguments:
        c1: coalition 1
        c2: coalition 2

    Returns:
        A boolean to signify if 2 coalitions have overlapping members or
        not.
    """
    for elem in c2:
        if elem in c1:
            return True
    return False
    