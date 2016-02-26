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

from .testing import captured_output


class MainTestCase(unittest.TestCase):
    def test_version(self):
        from ..cli import main

        version = pkg_resources.get_distribution('db-migrator').version
        with captured_output() as (out, err):
            self.assertRaises(SystemExit, main, ['-V'])

        stdout = out.getvalue()
        stderr = err.getvalue()
        if sys.version_info[0] == 3:
            self.assertEqual(stdout.strip(), version)
            self.assertEqual(stderr, '')
        else:
            self.assertEqual(stdout, '')
            self.assertEqual(stderr.strip(), version)
