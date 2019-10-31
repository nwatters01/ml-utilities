"""Build module from config."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import logging
import importlib
import tensorflow as tf


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
    if isinstance(x, list):
        return [build_from_config(i) for i in x]
    elif isinstance(x, tuple):
        return tuple([build_from_config(i) for i in x])
    elif isinstance(x, dict):
        if 'constructor' in x:
            constructor = build_from_config(x['constructor'])

            if 'args' in x:
                args = tuple([build_from_config(v) for v in x['args']])
            else:
                args = ()
            if 'kwargs' in x:
                kwargs = {k: build_from_config(v)
                          for k, v in x['kwargs'].items()}
            else:
                kwargs = {}
            logging.info('Constructor: {}.'.format(constructor))
            return constructor(*args, **kwargs)
        elif 'module' in x:
            module = importlib.import_module(x['module'])
            method = getattr(module, x['method'])
            return method
        elif 'choice' in x:
            return build_from_config(x['options'][x['choice']])
        else:
            output = {}
            for k, v in x.items():
                with tf.name_scope(k):
                    output[k] = build_from_config(v)
            return output
    else:  # x has a type that we won't worry about
        return x