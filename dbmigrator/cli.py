# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

import argparse
import os
import sys

from . import commands, utils


DEFAULTS = {
    'migrations_directory': 'migrations',
    }

DEFAULT_CONFIG_PATH = 'development.ini'


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='DB Migrator')

    parser.add_argument('--migrations-directory')

    parser.add_argument('--config', default=DEFAULT_CONFIG_PATH)

    parser.add_argument('--db-connection-string',
                        help='a psycopg2 db connection string')

    subparsers = parser.add_subparsers(help='commands')
    commands.load_cli(subparsers)

    args = parser.parse_args(argv)
    args = vars(args)

    if os.path.exists(args['config']):
        utils.get_settings_from_config(args['config'], [
            'migrations-directory',
            'db-connection-string',
            ], args)

    for name, value in DEFAULTS.items():
        if not args.get(name):
            args[name] = value

    if 'cmmd' not in args:
        parser.print_help()
        return parser.error('command missing')

    return args['cmmd'](**args)
