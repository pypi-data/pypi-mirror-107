#!/usr/bin/env python

from os import path, getenv
from setuptools import setup
from codecs import open

VERSION = [0, 1, 0]
readme = open('README.rst').read()

setup(
    name='superset-clickhouse',
    version='.'.join('%d' % v for v in VERSION[0:3]),
    description='ClickHouse SQLAlchemy Dialect for Superset',
    long_description = readme,
    author = 'nPhase, Inc.',
    author_email = 'etorap@redcapcloud.com',
    license = 'Apache License, Version 2.0',
    keywords = "db database cloud analytics clickhouse",
    install_requires = [
        'sqlalchemy>=1.3,<1.4',
        'infi.clickhouse_orm==1.0.4'
    ],
    packages=[
        'superset-clickhouse',
    ],
    package_dir={
        'superset-clickhouse': '.',
    },
    package_data={
        'superset-clickhouse': ['LICENSE.txt'],
    },
    entry_points={
        'sqlalchemy.dialects': [
            'clickhouse=sqlalchemy_clickhouse.base',
        ]
    },
    classifiers = [
        'Development Status :: 5 - Production/Stable',

        'Environment :: Console',
        'Environment :: Other Environment',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',

        'License :: OSI Approved :: Apache Software License',

        'Operating System :: OS Independent',

        'Programming Language :: SQL',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

        'Topic :: Database',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
