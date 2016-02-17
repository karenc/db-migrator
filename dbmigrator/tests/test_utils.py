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
