#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for redtape."""

from setuptools import setup, find_packages
import sys, os

import redtape
version = '.'.join(map(str, redtape.VERSION))

# some trove classifiers:

# License :: OSI Approved :: MIT License
# Intended Audience :: Developers
# Operating System :: POSIX

setup(
    name='redtape',
    version=version,
    description="simple tiny document generator",
    long_description=open('README.rst').read(),
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
        'Operating System :: POSIX',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='github markdown documentation quick small simple',
    author='Jason Moiron',
    author_email='jmoiron@jmoiron.net',
    url='http://github.com/jmoiron/redtape',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite="tests",
    scripts=['bin/rt'],
    package_data={'redtape': ['assets/*']},
    install_requires=[
        "markdown",
        "pygments",
        "jinja2",
      # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
