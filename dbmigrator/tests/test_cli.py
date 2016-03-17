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
    def tearDown(self):
        with psycopg2.connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute('DROP TABLE IF EXISTS schema_migrations')


class VersionTestCase(BaseTestCase):
    def test(self):
        from ..cli import main

        version = pkg_resources.get_distribution('db-migrator').version
        with testing.captured_output() as (out, err):
            self.assertRaises(SystemExit, main, ['-V'])

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
        from ..cli import main
        from .. import logger

        with testing.captured_output() as (out, err):
            main(['-v', '--config', testing.test_config_path, 'init'])

        stdout = out.getvalue()
        stderr = err.getvalue()

        self.assertEqual(1, debug.call_count)
        self.assertTrue(debug.call_args[0][0].startswith('args: {'))

        self.assertEqual('Schema migrations initialized.\n', stdout)
        self.assertEqual('', stderr)


class ListTestCase(BaseTestCase):
    def test_no_migrations_directory(self):
        from ..cli import main

        cmd = ['--db-connection-string', testing.db_connection_string]
        main(cmd + ['init'])
        with testing.captured_output() as (out, err):
            main(cmd + ['list'])

        stdout = out.getvalue()
        stderr = err.getvalue()

        self.assertEqual(stdout, """\
name                      | is applied | date applied
----------------------------------------------------------------------\n""")
        self.assertEqual(stderr, """\
context undefined, using current directory name "['db-migrator']"
migrations directory undefined\n""")

    @mock.patch('dbmigrator.logger.warning')
    def test_no_table(self, warning):
        from ..cli import main

        cmd = ['--config', testing.test_config_path]
        with testing.captured_output() as (out, err):
            main(cmd + ['list'])

        stdout = out.getvalue()
        stderr = err.getvalue()

        self.assertEqual("""\
name                      | is applied | date applied
----------------------------------------------------------------------\n""",
                         stdout)

        warning.assert_called_with('You may need to run "dbmigrator init" '
                                   'to create the schema_migrations table')
        self.assertEqual('', stderr)

    def test(self):
        from ..cli import main

        testing.install_test_packages()

        cmd = ['--db-connection-string', testing.db_connection_string]
        main(cmd + ['init'])
        with testing.captured_output() as (out, err):
            main(cmd + ['-v', '--context', 'package-a', 'list'])

        stdout = out.getvalue()
        stderr = err.getvalue()

        self.assertEqual("""\
name                      | is applied | date applied
----------------------------------------------------------------------
20160228202637_add_table    False        \

20160228212456_cool_stuff   False        \
\n""", stdout)
        self.assertEqual('', stderr)
