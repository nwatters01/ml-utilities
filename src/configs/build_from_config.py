"""Build module from config."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import logging


def build_from_config(x):
    """Build module from config.

    Converts a dictionary with keys "constructor" and optionally "args" and
    "kwargs" items into a module built by constructor(*args, **kwargs). "args"
    and "kwargs" themselves may contain modules (also defined by dicts with
    "constructor").
    
    Args:
        x: If dict containing "constructor", may contain only "constructor" and
            optionally "args" and "kwargs" items. Else is assumed to be a leaf
            node.

    Returns:
        Module constructed from x.
    """
    if not isinstance(x, dict):
        # Leaf node
        logging.info('Returning non-dictionary {}.'.format(x))
        return x
    elif 'constructor' not in x:
        # Leaf node
        logging.info('Returning leaf dictionary {}.'.format(x))
        return x
    else:
        # Not leaf node
        constructor = x['constructor']
        if 'args' in x:
            args = tuple([build_from_config(v) for v in x['args']])
        else:
            args = ()
        if 'kwargs' in x:
            kwargs = {k: build_from_config(v) for k, v in x['kwargs'].items()}
        else:
            kwargs = {}
        logging.info('Constructor: {}.'.format(constructor))
        return constructor(*args, **kwargs)
