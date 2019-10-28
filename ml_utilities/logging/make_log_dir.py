"""Create a directory for logging."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from imp import reload
import logging
import os

# pylint: disable=no-member


def make_log_dir(log_dir='logs', make_subdir=False):
    """Make logging directory and copy logs to a log.log file in it.

    Args:
        log_dir: directory relative to the code path in which to write
            the logs.
        make_subdir: Bool. Whether to write the logs in a sub-directory of
            log_dir. This is useful if you want to use the same log_dir for
            multiple runs. If True, the sub-directories will be numerals,
            starting from 1.

    Returns:
        log_dir: Path to the log file itself.
    """
    reload(logging)
    logging.getLogger().setLevel(logging.DEBUG)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if make_subdir:
        # Find most recent log subdir, and log to the next numeral
        most_recent_log_dir = max([int(filename)
                                   for filename in os.listdir(log_dir)])
        log_dir = os.path.join(log_dir, str(most_recent_log_dir + 1))
        os.makedirs(log_dir)
    else:
        if os.listdir(log_dir):
            raise ValueError(
                'logdir {} is not empty. Please specify a new directory for '
                'logging or use make_subdirs=True.'.format(log_dir))
        
    # Write to log file
    log_filename = os.path.join(log_dir, 'log.log')
    logging.info('Log filename: {}'.format(log_filename))
    handler = logging.FileHandler(log_filename)
    logging.getLogger().addHandler(handler)

    logging.info('Log filename: {}'.format(log_filename))

    return log_dir
