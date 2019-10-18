"""Create a directory for logging."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import logging
from imp import reload

# pylint: disable=no-member


def make_log_dir(log_parent_dir='logs'):
    """Make logging directory and copy logs to a log.log file in it.

    Args:
        log_parent_dir: directory relative to the code path in which to write
            the logs.

    Returns:
        log_dir: Path to the log file itself.
    """
    reload(logging)
    logging.getLogger().setLevel(logging.DEBUG)

    if not os.path.exists(log_parent_dir):
        os.makedirs(log_parent_dir)

    # Find most recent log
    existing_log_dirs = os.listdir(log_parent_dir)
    if not existing_log_dirs:
        most_recent_log_dir = 0
    else:
        most_recent_log_dir = max([int(filename)
                                   for filename in existing_log_dirs])

    # Write to new log file
    log_dir = os.path.join(log_parent_dir, str(most_recent_log_dir + 1))
    os.makedirs(log_dir)
    log_filename = os.path.join(log_dir, 'log.log')
    logging.info('Log filename: {}'.format(log_filename))
    handler = logging.FileHandler(log_filename)
    logging.getLogger().addHandler(handler)

    logging.info('Log filename: {}'.format(log_filename))

    return log_dir
