"""Functions for creating hyperparameter sweeps.

A hyperparameter spec is a list of dictionaries, each of which has:
* "node": A list of strings, specifying the path to a leaf in the config.
* "value": The new value for that leaf.

A hyperparameter sweep is a list of hyperparameter specs. This file contains
functions for composing hyperparameter sweeps.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import copy


def discrete(node, values):
    """Discrete sweep for a single node."""
    if not isinstance(values, (list, tuple)):
        values = [values]
    return [[{'node': node, 'value': v}] for v in values]


def product(*sweeps):
    """Product of multiple sweeps.
    
    This returns a sweep of length N_0 * N_1 * ... * N_k where
    N_i = len(sweeps[i]).
    """
    if len(sweeps) == 1:
        return sweeps[0]
    else:
        sweep_0 = sweeps[0]
        sweep_1 = product(*sweeps[1:])
        sweep = []
        for x in sweep_0:
            for y in sweep_1:
                sweep.append(copy.deepcopy(x) + copy.deepcopy(y))
        return sweep


def zipper(*sweeps):
    """Zip of sweeps, all of which should have the same length."""
    return zip(*sweeps)