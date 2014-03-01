#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='bbots',
    version='0.1.0',
    description='bbot aggregator',
    long_description=readme + '\n\n' + history,
    author='Derrick Karimi',
    author_email='derrick.karimi@gmail.com',
    url='https://github.com/AlwaysTraining/bbots',
    packages=[
        'bbots',
    ],
    package_dir={'bbots': 'bbots'},
    include_package_data=True,
    install_requires=[
        'daemon','bbot'
    ],
    dependency_links=[
        'git+https://github.com/AlwaysTraining/bbot.git#egg=bbot'
        '.gzuuuuuu],
    license="BSD",
    zip_safe=False,
    keywords='bbots',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
