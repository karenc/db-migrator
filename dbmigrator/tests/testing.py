# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2016, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

from contextlib import contextmanager
from io import StringIO
import os.path
import sys

import pip


here = os.path.abspath(os.path.dirname(__file__))
db_connection_string = 'dbname=travis user=travis host=localhost'
test_data_path = os.path.join(here, 'data')
test_packages = ['package-a', 'package-b']
test_config_path = os.path.join(test_data_path, 'config.ini')
test_migrations_directories = [
    os.path.join(test_data_path, 'package-a', 'package_a', 'migrations'),
    os.path.join(test_data_path, 'package-b', 'package_b', 'm'),
    ]


# noqa from http://stackoverflow.com/questions/4219717/how-to-assert-output-with-nosetest-unittest-in-python
@contextmanager
def captured_output():
    if sys.version_info[0] == 3:
        new_out, new_err = StringIO(), StringIO()
    else:
        from io import BytesIO
        new_out, new_err = BytesIO(), BytesIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def install_test_packages(packages=None):
    if packages is None:
        packages = test_packages
    for package in packages:
        pip.main(['install', '-e', os.path.join(test_data_path, package)])
