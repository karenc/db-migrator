# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

import sys
from setuptools import setup, find_packages

install_requires = (
    'psycopg2>=2.5',
    )

tests_require = [
    ]

if sys.version_info.major < 3:
    tests_require.append('mock')

LONG_DESC = '\n\n~~~~\n\n'.join([open('README.rst').read(),
                                 open('CHANGELOG.rst').read()])

setup(
    name='db-migrator',
    version='0.1.4',
    author='Connexions',
    author_email='info@cnx.org',
    url='https://github.com/karenc/db-migrator',
    license='AGPL, see also LICENSE.txt',
    description='Python package to migrate postgresql database',
    long_description=LONG_DESC,
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='dbmigrator.tests',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'dbmigrator = dbmigrator.cli:main',
            ],
        },
    )
