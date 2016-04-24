# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2016, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

import sys
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

import pkg_resources
import psycopg2

from . import testing


class BaseTestCase(unittest.TestCase):
    @property
    def target(self):
        from ..cli import main
        return main

    def tearDown(self):
        with psycopg2.connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute('DROP TABLE IF EXISTS schema_migrations')


class VersionTestCase(BaseTestCase):
    def test(self):
        version = pkg_resources.get_distribution('db-migrator').version
        with testing.captured_output() as (out, err):
            self.assertRaises(SystemExit, self.target, ['-V'])

        stdout = out.getvalue()
        stderr = err.getvalue()
        if sys.version_info[0] == 3:
            self.assertEqual(stdout.strip(), version)
            self.assertEqual(stderr, '')
        else:
            self.assertEqual(stdout, '')
            self.assertEqual(stderr.strip(), version)


class VerboseTestCase(BaseTestCase):
    @mock.patch('dbmigrator.logger.debug')
    def test(self, debug):
        from .. import logger

        with testing.captured_output() as (out, err):
            self.target(['-v', '--config', testing.test_config_path, 'init'])

        stdout = out.getvalue()
        stderr = err.getvalue()

        self.assertEqual(1, debug.call_count)
        self.assertTrue(debug.call_args[0][0].startswith('args: {'))

        self.assertEqual('Schema migrations initialized.\n', stdout)
        self.assertEqual('', stderr)


class ListTestCase(BaseTestCase):
    def test_no_migrations_directory(self):
        cmd = ['--db-connection-string', testing.db_connection_string]
        self.target(cmd + ['init'])
        with testing.captured_output() as (out, err):
            self.target(cmd + ['list'])

        stdout = out.getvalue()
        stderr = err.getvalue()

        self.assertEqual(stdout, """\
version        | name            | is applied | date applied
----------------------------------------------------------------------\n""")
        self.assertEqual(stderr, """\
context undefined, using current directory name "['db-migrator']"
migrations directory undefined\n""")

    @mock.patch('dbmigrator.logger.warning')
    def test_no_table(self, warning):
        cmd = ['--config', testing.test_config_path]
        with testing.captured_output() as (out, err):
            self.target(cmd + ['list'])

        stdout = out.getvalue()
        stderr = err.getvalue()

        self.assertEqual("""\
version        | name            | is applied | date applied
----------------------------------------------------------------------\n""",
                         stdout)

        warning.assert_called_with('You may need to run "dbmigrator init" '
                                   'to create the schema_migrations table')
        self.assertEqual('', stderr)

    def test(self):
        testing.install_test_packages()

        cmd = ['--db-connection-string', testing.db_connection_string]
        self.target(cmd + ['init'])
        with testing.captured_output() as (out, err):
            self.target(cmd + ['-v', '--context', 'package-a', 'list'])

        stdout = out.getvalue()
        stderr = err.getvalue()

        self.assertEqual("""\
version        | name            | is applied | date applied
----------------------------------------------------------------------
20160228202637   add_table         False        \

20160228212456   cool_stuff        False        \
\n""", stdout)
        self.assertEqual('', stderr)


class InitTestCase(BaseTestCase):
    def test_multiple_contexts(self):
        testing.install_test_packages()

        cmd = ['--db-connection-string', testing.db_connection_string]
        self.target(cmd + ['--context', 'package-a', '--context', 'package-b',
                           'init'])

        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a', '--context',
                               'package-b', 'list'])

        stdout = out.getvalue()
        self.assertIn('20160228202637   add_table         True', stdout)
        self.assertIn('20160228210326   initial_data      True', stdout)
        self.assertIn('20160228212456   cool_stuff        True', stdout)


class MarkTestCase(BaseTestCase):
    def test_missing_t_f_option(self):
        cmd = ['--db-connection-string', testing.db_connection_string]

        self.target(cmd + ['--context', 'package-a', 'init'])

        with self.assertRaises(Exception) as cm:
            self.target(cmd + ['--context', 'package-a', 'mark',
                               '20160228212456'])

        print(str(cm.exception))

    def test_mark_as_true(self):
        testing.install_test_packages()
        cmd = ['--db-connection-string', testing.db_connection_string]

        self.target(cmd + ['--context', 'package-a', 'init', '--version', '0'])

        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a',
                               'mark', '-t', '20160228212456'])

        stdout = out.getvalue()
        self.assertEqual('Migration 20160228212456 marked as completed\n',
                         stdout)

        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a', 'list'])

        stdout = out.getvalue()
        self.assertIn('20160228202637   add_table         False', stdout)
        self.assertIn('20160228212456   cool_stuff        True', stdout)

    def test_mark_as_true_already_true(self):
        testing.install_test_packages()
        cmd = ['--db-connection-string', testing.db_connection_string]

        self.target(cmd + ['--context', 'package-a', 'init'])

        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a',
                               'mark', '-t', '20160228212456'])

        stdout = out.getvalue()
        self.assertEqual('Migration 20160228212456 marked as completed\n',
                         stdout)

        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a', 'list'])

        stdout = out.getvalue()
        self.assertIn('20160228202637   add_table         True', stdout)
        self.assertIn('20160228212456   cool_stuff        True', stdout)

    @mock.patch('dbmigrator.logger.warning')
    def test_migration_not_found(self, warning):
        testing.install_test_packages()
        cmd = ['--db-connection-string', testing.db_connection_string]

        self.target(cmd + ['--context', 'package-a', 'init', '--version', '0'])

        self.target(cmd + ['mark', '-t', '012345'])
        warning.assert_called_with('Migration 012345 not found')

        self.target(cmd + ['mark', '-f', '012345'])
        warning.assert_called_with('Migration 012345 not found')

    def test_mark_as_false(self):
        testing.install_test_packages()
        cmd = ['--db-connection-string', testing.db_connection_string]

        self.target(cmd + ['--context', 'package-a', 'init'])

        with testing.captured_output() as (out, err):
            self.target(cmd + ['mark', '-f', '20160228202637'])

        stdout = out.getvalue()
        self.assertEqual('Migration 20160228202637 marked as not been run\n',
                         stdout)

        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a', 'list'])

        stdout = out.getvalue()
        self.assertIn('20160228202637   add_table         False', stdout)
        self.assertIn('20160228212456   cool_stuff        True', stdout)

    def test_mark_as_false_already_false(self):
        testing.install_test_packages()
        cmd = ['--db-connection-string', testing.db_connection_string]

        self.target(cmd + ['--context', 'package-a', 'init', '--version', '0'])

        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a', 'mark', '-f',
                               '20160228202637'])

        stdout = out.getvalue()
        self.assertEqual('Migration 20160228202637 marked as not been run\n',
                         stdout)

        with testing.captured_output() as (out, err):
            self.target(cmd + ['--context', 'package-a', 'list'])

        stdout = out.getvalue()
        self.assertIn('20160228202637   add_table         False', stdout)
        self.assertIn('20160228212456   cool_stuff        False', stdout)
