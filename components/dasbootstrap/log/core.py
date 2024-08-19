"""Logging system component."""

import logging

# get an instance of the logger object this module will use
logger = logging.getLogger(__name__)

# add the journald handler to the current logger
logger.addHandler(journald_handler)
logger.setLevel(logging.INFO)
