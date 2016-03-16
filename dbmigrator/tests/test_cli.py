# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2016, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

import sys
import unittest

import pkg_resources
import psycopg2

from . import testing


class MainTestCase(unittest.TestCase):
    def tearDown(self):
        with psycopg2.connect(testing.db_connection_string) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute('DROP TABLE IF EXISTS schema_migrations')

    def test_version(self):
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

    def test_list_no_migrations_directory(self):
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
