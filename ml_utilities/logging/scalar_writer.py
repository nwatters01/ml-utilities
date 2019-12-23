"""Scalar write to log dictionaries of scalars to a .csv file.
"""
# pylint: disable=import-error

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import csv
from absl import logging


class ScalarWriter(object):
    """Writer that logs dictionaries of scalars to a csv file."""

    def __init__(self, filename, keys, flush_every=10):
        """Constructor.

        First row written to filename will be the keys. Subsequent rows will be
        scalars aligned to those keys (so each column will correspond to one
        key).

        Args:
            filename: String. Name of file to write scalars to. Must be a .csv
                file.
            keys: Iterable of strings. Keys of the scalars to write.
            flush_every: Int. Period at which the writer is flushed.
        """

        logging.info(
            'Writing scalars with keys {} to file {}'.format(keys, filename))

        if filename[-4:] != '.csv':
            raise ValueError(
                'filename {} must end in ".csv".'.format(filename))
        self._filename = filename
        self._keys = sorted(keys)
        self._flush_every = flush_every

        self._flush_index = 0
        self._open_file = open(self._filename, "w+")
        self._writer = csv.writer(self._open_file)
        self._writer.writerow(self._keys)

    def write(self, scalars):
        """Write dictionary of scalars to file.
        
        Args:
            scalars: Dictionary. Keys must be self._keys(). Values should be
                scalars.
        """
        if sorted(scalars.keys()) != self._keys:
            raise ValueError(
                'scalars.keys are {}, but ScalarLogger expected keys are '
                '{}.'.format(sorted(scalars.keys()), self._keys))

        scalars_vec = [scalars[k] for k in self._keys]
        self._writer.writerow(scalars_vec)
        self._flush_index += 1

        if self._flush_index == self._flush_every:
            self._open_file.flush()
            self._flush_index = 0
