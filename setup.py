#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from distutils.core import setup
from os import path
from glob import glob

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_modules():
    objdir = path.join(path.dirname(__file__), 'bbots/*.py')
    mods = []
    for f in glob(objdir):
        name = path.splitext(path.basename(f))[0]
        if name == '__init__':
            continue
        mods.append("bbots." + name)

    return mods


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
    packages=['bbots'],
    py_modules=get_modules(),
    scripts=['bin/bbotsd.py'],
    package_dir={'bbots': 'bbots'},
    include_package_data=True,
    install_requires=[
        'daemon','gdata','bbot'
    ],
    dependency_links=[
        'git+https://github.com/AlwaysTraining/bbot.git#egg=bbot-0.1'],
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
