"""Methods for creating logging directories and redirecting logs."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from imp import reload
import logging
import os

# pylint: disable=no-member


def create_log_dir(log_dir='logs', make_subdir=False):
    """Make logging directory and copy logs to a log.log file in it.

    Args:
        log_dir: directory relative to the code path in which to create the
            directory.
        make_subdir: Bool. Whether to write the logs in a sub-directory of
            log_dir. This is useful if you want to use the same log_dir for
            multiple runs. If True, the sub-directories will be numerals,
            starting from 0.

    Returns:
        log_dir: Path to the log directory.
    """
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if make_subdir:
        # Find most recent log subdir, and log to the next numeral
        list_log_dir = os.listdir(log_dir)
        existing_log_subdirs = [
            int(filename) for filename in list_log_dir if filename.isdigit()]
        if existing_log_subdirs:
            new_log_subdir = str(max(existing_log_subdirs) + 1)
        else:
            new_log_subdir = '0'
        log_dir = os.path.join(log_dir, new_log_subdir)
        os.makedirs(log_dir)

    logging.info('Log directory: {}'.format(log_dir))
    
    return log_dir


def redirect_logs(log_dir, log_filename='log.log'):
    """Redirect logging to custom file.

    Args:
        log_dir: String. Directory relative to the code path in which to write
            the logs.
        log_filename: String. Filename in which to write the logs.
    """
    reload(logging)
    logging.getLogger().setLevel(logging.DEBUG)
    log_path = os.path.join(log_dir, 'log.log')
    logging.info('Log path: {}'.format(log_path))
    handler = logging.FileHandler(log_path)
    logging.getLogger().addHandler(handler)

    return
