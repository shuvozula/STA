
__author__ = 'Spondon Saha'

import logging
import math

# logging parameters
DEFAULT_LOGGING_LEVEL = logging.DEBUG
DEFAULT_LOG_FILE = 'sta.out'
DEFAULT_LOG_DIR = '/tmp'

# Random Data Generator parameters
NUM_ROBOTS = 10
COALITION_SIZE_RANGE = (1, 3)
BID_LIMIT = 10
TASK_SIZE = 3
MAX_BID_VALUE = 10
MAX_BIDS_PER_TASK = int(math.ceil(float(BID_LIMIT)/float(TASK_SIZE))) * 2