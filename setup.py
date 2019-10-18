"""Installation script for setuptools."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from setuptools import find_packages
from setuptools import setup

setup(
    name='ml-utilities',
    version='1.0.1',
    description=('ML-Utilities is a python-based library of utilities useful '
                 'for machine learning projects. It is untested, poorly '
                 'documented, and not intended for public use.'),
    author='Nicholas Watters',
    url='https://github.com/nwatters01/ml-utilities/',
    keywords=[],
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'absl-py',
        'six',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)