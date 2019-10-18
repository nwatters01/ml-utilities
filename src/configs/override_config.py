"""Tools for overriding nodes of a configuration dictionary.

This is useful for hyperparameter sweeping and easily testing hyperparams.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json


def override_config_node(config, node, value):
    """Override a node of a config.

    Args:
        config: Base configuration dictionary to be modified.
        node: Iterable of keys of config corresponding to a path to a leaf node.
        value: New value for the leaf node.

    Returns:
        Dictionary, config with a new leaf value.
    """
    if not isinstance(node, (list, tuple)):
        raise ValueError('node must be an iterable, but is {}'.format(node))
    
    if node[0] not in config:
        raise ValueError('node {} is not in config.'.format(node))

    if len(node) == 1:
        config[node[0]] = value
    else:
        override_config_node(config[node[0]], node[1:], value)


def override_config(config, overrides):
    """Override nodes of the config based on override_dict.

    Args:
        config: Base configuration dictionary (possibly nested).
        overrides: Iterable of dictionaries, each with a "node" and a "value"
            element specifying how to modify config. For each such dictionary,
            "node" is a tuple of keys in config that corresponding to a path to
            a leaf in the config and "value" is the new value for that leaf.

    Returns:
        Dictionary, config overridden according to override_dict.
    """
    for x in overrides:
        override_config_node(config, **x)
    return config


def override_config_from_json(config, json_overrides):
    """Override nodes of the config based on json_overrides.

    This is the same as override_config(), except it takes a json serialization
    of the overrides.
    """
    print(json.loads(json_overrides))
    return override_config(config, json.loads(json_overrides))
