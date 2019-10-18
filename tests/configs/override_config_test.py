"""Tests for src/configs/override_config.py."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Allow imports from ../../configs
import sys
sys.path.append("../..")

from absl.testing import absltest
from absl.testing import parameterized
from src.configs import override_config
import json


def _get_config():
    config = {
        '1a': {
            '2a': 0,
            '2b': 1,
            '2c': [2, 3, 4, 5],
        },
        42: '2d',
    }
    return config
    
    
def _get_node(config, node):
    if node[0] not in config:
        raise ValueError('node {} is not in config.'.format(node))

    if len(node) == 1:
        return config[node[0]]
    else:
        return _get_node(config[node[0]], node[1:])


class OverrideConfigNodeTest(parameterized.TestCase):

    @parameterized.parameters(
        (('1a', '2a'), 17),
        (['1a', '2a'], 18),
        (['1a', '2c'], 'blargh'),
        ((42,), 4),
    )
    def testCorrectness(self, node, new_value):
        config = _get_config()
        old_value = _get_node(config, node)
        
        # Change node to new value
        override_config.override_config_node(config, node, new_value)
        self.assertEqual(new_value, _get_node(config, node))
        
        # Change node back to old value
        override_config.override_config_node(config, node, old_value)
        self.assertEqual(config, _get_config())

    @parameterized.parameters(
        ('1a', 0),
        (['3a', '2a'], 0),
    )
    def testRaisesError(self, node, new_value):
        config = _get_config()
        with self.assertRaises(ValueError):
            override_config.override_config_node(config, node, new_value)


class OverrideConfigTest(parameterized.TestCase):
    
    def testCorrectness(self):
        overrides = [
            {
                'node': ('1a', '2a'),
                'value' : 17,
            },
            {
                'node': ('1a', '2c'),
                'value' : 'blargh',
            },
            {
                'node': (42,),
                'value' : 4,
            },
        ]

        config = _get_config()
        override_config.override_config(config, overrides)
        for x in overrides:
            self.assertEqual(_get_node(config, x['node']), x['value'])
        

class OverrideConfigFromJSONTest(parameterized.TestCase):
    
    def testCorrectness(self):
        overrides = (
            {
                'node': ('1a', '2a'),
                'value' : 17,
            },
            {
                'node': ('1a', '2c'),
                'value' : 'blargh',
            },
            {
                'node': (42,),
                'value' : 4,
            },
        )
        json_overrides = json.dumps(overrides)

        config = _get_config()
        override_config.override_config_from_json(config, json_overrides)
        for x in overrides:
            self.assertEqual(_get_node(config, x['node']), x['value'])


if __name__ == '__main__':
  absltest.main()
