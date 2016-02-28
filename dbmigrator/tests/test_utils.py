# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2016, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

import os.path
import unittest

from . import testing


class UtilsTestCase(unittest.TestCase):
    def test_get_settings_from_entry_points(self):
        from ..utils import get_settings_from_entry_points

        testing.install_test_packages()

        contexts = testing.test_packages
        settings = {
            'db_connection_string': testing.db_connection_string,
            }

        get_settings_from_entry_points(settings, contexts)

        self.assertEqual(
            settings,
            {'migrations_directory': testing.test_migrations_directories,
             'db_connection_string': testing.db_connection_string,
             })

    def test_get_settings_from_config(self):
        from ..utils import get_settings_from_config

        settings = {
            'migrations_directory': '/tmp/',
            }

        get_settings_from_config(
            testing.test_config_path,
            ['db-connection-string', 'migrations-directory', 'does-not-exist'],
            settings)

        self.assertEqual(
            settings,
            {'db_connection_string':
                'dbname=people user=test host=db.example.org',
             'migrations_directory': '/tmp/'})
