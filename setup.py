# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

import os
import re
import sys
from setuptools import setup, find_packages

install_requires = (
    'psycopg2>=2.7',
    )

tests_require = [
    ]

if sys.version_info.major < 3:
    tests_require.append('mock')

here = os.path.dirname(__file__)


def read(path):
    with open(os.path.join(here, path)) as f:
        return f.read()


def find_version(path):
    m = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                  read(path), re.MULTILINE)
    if m:
        return m.group(1)
    raise RuntimeError('Unable to find version string')

LONG_DESC = '\n\n~~~~\n\n'.join([read('README.rst'),
                                 read('CHANGELOG.rst')])

setup(
    name='db-migrator',
    version=find_version('dbmigrator/__init__.py'),
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
