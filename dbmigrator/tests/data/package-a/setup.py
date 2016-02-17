# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2016, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

from setuptools import setup, find_packages

setup(
    name='package-a',
    version='1.2.3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'package_a_hello = package_a.hello',
            ],
        'dbmigrator': [
            'migrations_directory = package_a:migrations_directory',
            ],
        },
    )
