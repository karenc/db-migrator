# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2016, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

import os.path
import unittest

import psycopg2

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

    def test_with_cursor(self):
        from ..utils import with_cursor

        self.called = False

        @with_cursor
        def func(cursor, arg_1, kwarg_1='kwarg_1', kwarg_2='kwarg_2',
                 db_connection_string=None):
            self.assertTrue(isinstance(cursor, psycopg2.extensions.cursor))
            self.assertEqual(arg_1, 'arg_1')
            self.assertEqual(kwarg_1, 'called')
            self.assertEqual(kwarg_2, 'kwarg_2')
            self.assertEqual(
                db_connection_string, testing.db_connection_string)
            self.called = True

        func('arg_1', kwarg_1='called',
             db_connection_string=testing.db_connection_string)
        self.assertTrue(self.called)

        with self.assertRaises(Exception) as cm:
            func('')

        self.assertEqual(str(cm.exception), 'db-connection-string missing')
