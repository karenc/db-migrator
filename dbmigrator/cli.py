# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
from __future__ import print_function
import argparse
import os
import sys

from . import commands, utils


DEFAULTS = {
    }


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='DB Migrator')

    parser.add_argument('--migrations-directory',
                        default='')

    parser.add_argument('--config')

    parser.add_argument('--db-connection-string',
                        help='a psycopg2 db connection string')

    subparsers = parser.add_subparsers(help='commands')
    commands.load_cli(subparsers)

    args = parser.parse_args(argv)
    args = vars(args)

    if args.get('config') and os.path.exists(args['config']):
        utils.get_settings_from_config(args['config'], [
            'migrations-directory',
            'db-connection-string',
            ], args)
    utils.get_settings_from_entry_points(args)

    for name, value in DEFAULTS.items():
        if not args.get(name):
            args[name] = value

    if 'cmmd' not in args:
        parser.print_help()
        return parser.error('command missing')

    if args.get('migrations_directory'):
        args['migrations_directory'] = os.path.relpath(
            args['migrations_directory'])
    else:
        print('migrations directory undefined', file=sys.stderr)

    return args['cmmd'](**args)
