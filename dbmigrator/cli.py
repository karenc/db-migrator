# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

import argparse
import sys

from . import commands


DEFAULT_MIGRATIONS_DIRECTORY = 'migrations'


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='DB Migrator')

    parser.add_argument('--migrations-directory',
                        default=DEFAULT_MIGRATIONS_DIRECTORY)

    subparsers = parser.add_subparsers(help='commands')
    commands.load_cli(subparsers)

    args = parser.parse_args(argv)
    args = vars(args)

    if 'cmmd' not in args:
        parser.print_help()
        return parser.error('command missing')

    return args['cmmd'](**args)
