"""Tests for src/configs/build_from_config.py."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Allow imports from ../../configs
import sys
sys.path.append("../..")

from absl.testing import absltest
from ml_utilities.configs import build_from_config


class DummyClass(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class BuildFromConfigTest(absltest.TestCase):

    def testBasicCorrectness(self):
        config = {
            'constructor': DummyClass,
            'args': (1, 2, 3),
            'kwargs': {
                'a': 4,
                'b': 5,
            }
        }

        model = build_from_config.build_from_config(config)
        self.assertIsInstance(model, DummyClass)
        self.assertEqual(model.args, (1, 2, 3))
        self.assertEqual(model.kwargs, {'a': 4, 'b': 5})

    def testNestedConfig(self):
        config = {
            'constructor': DummyClass,
            'args': [1, 2, 3, {
                'constructor': DummyClass,
                'args': [4, 5, 6],
                'kwargs': {'a': 1},
            },],
            'kwargs': {
                'b': 7,
                'c': [8, 7, 6],
                'd': {
                    'constructor': DummyClass,
                    'args': [9, 10, 11],
                    'kwargs': {'e': 'blargh'},
                }
            }
        }

        model = build_from_config.build_from_config(config)
        self.assertIsInstance(model, DummyClass)
        self.assertEqual(model.args[:3], (1, 2, 3))
        self.assertIsInstance(model.args[3], DummyClass)
        self.assertEqual(model.args[3].args, (4, 5, 6))
        self.assertEqual(model.args[3].kwargs, {'a': 1})
        self.assertEqual(model.kwargs['b'], 7)
        self.assertEqual(model.kwargs['c'], [8, 7, 6])
        self.assertIsInstance(model.kwargs['d'], DummyClass)
        self.assertEqual(model.kwargs['d'].args, (9, 10, 11))
        self.assertEqual(model.kwargs['d'].kwargs, {'e': 'blargh'})

    def testAlternativeTypes(self):
        config = {
            'a': set([1, 2, 3]),
            'b': DummyClass(1, 2, a=3, b=4),
        }

        model = build_from_config.build_from_config(config)
        self.assertIsInstance(model, dict)
        self.assertIsInstance(model['a'], set)
        self.assertIsInstance(model['b'], DummyClass)
        
    def testExpandsList(self):
        config = [
            {
                'a': 1,
                'b': 2,
            },
            {
                'constructor': DummyClass,
                'args': (4, 5, 6),
            },
        ]

        model = build_from_config.build_from_config(config)
        self.assertIsInstance(model[1], DummyClass)
        self.assertEqual(model[1].args, (4, 5, 6))

    def testExpandsTuple(self):
        config = (
            {
                'a': 1,
                'b': 2,
            },
            {
                'constructor': DummyClass,
                'args': (4, 5, 6),
            },
        )

        model = build_from_config.build_from_config(config)
        self.assertIsInstance(model[1], DummyClass)
        self.assertEqual(model[1].args, (4, 5, 6))

    def testExpandsDict(self):
        config = {
            '0': {
                'a': 1,
                'b': 2,
            },
            '1': {
                'constructor': DummyClass,
                'args': (4, 5, 6),
            },
            '2': {
                'c': {
                    'constructor': DummyClass,
                    'args': (4, 5, 6),
                }
            },
        }

        model = build_from_config.build_from_config(config)
        self.assertIsInstance(model['1'], DummyClass)
        self.assertEqual(model['1'].args, (4, 5, 6))
        self.assertIsInstance(model['2']['c'], DummyClass)
        self.assertEqual(model['2']['c'].args, (4, 5, 6))


if __name__ == '__main__':
  absltest.main()
