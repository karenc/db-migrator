# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2016, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

from setuptools import setup, find_packages

setup(
    name='package-b',
    version='10.20.30',
    packages=find_packages(),
    entry_points={
        'dbmigrator': [
            'migrations_directory = package_b:find_migrations_directory',
            ],
        },
    )
