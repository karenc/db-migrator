# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2016, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

import os.path


def hello():
    print('hello world!')


def migrations_directory():
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(here, 'migrations')
