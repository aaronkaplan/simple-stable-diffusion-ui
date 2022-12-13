"""Logging module for the API."""

import logging
import os
from sys import stdout


def get_module_logger(mod_name):
    """Get a logger for a module.

    To use this, do logger = get_module_logger(__name__)
    """
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler(stdout)  # set streamhandler to stdout
    formatter = logging.Formatter('%(asctime)s [%(name)-12s] (%(process)d)  %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if not os.environ.get('LOG_LEVEL'):
        os.environ['LOG_LEVEL'] = 'INFO'
    if os.environ.get('LOG_LEVEL').upper() == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    elif os.environ.get('LOG_LEVEL').upper() == 'INFO':
        logger.setLevel(logging.INFO)
    elif os.environ.get('LOG_LEVEL').upper() == 'WARNING':
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.ERROR)
    return logger
