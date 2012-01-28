__author__ = 'Spondon Saha'

import os
import logging

DEFAULT_LOGGING_LEVEL = logging.DEBUG
DEFAULT_LOG_FILE = 'sta.out'
DEFAULT_LOG_DIR = '/tmp'


class Error(Exception):
    """Native exception class."""
    pass


def SetupLogging(logging_level=DEFAULT_LOGGING_LEVEL,
                 log_dir=DEFAULT_LOG_DIR,
                 log_file=DEFAULT_LOG_FILE):
    """Sets up the logging parameters.

    Uses the logging library to create a log file, set the log-level,
    log file-mode, logging format, etc.

    Arguments:
        logging_level(optional): A valid logging level, usually DEBUG, INFO,
        WARNING, etc.
        log_dir(optional): Log directory path
        log_file(optional): Name of log file

    Raises:
        None
    """
    logging.basicConfig(filename=os.path.join(log_dir, log_file),
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
    