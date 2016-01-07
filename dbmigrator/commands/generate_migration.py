# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

import datetime
import os


__all__ = ('cli_loader',)


def cli_command(migration_name='', **kwargs):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = '{}_{}.py'.format(timestamp, migration_name)
    directory = kwargs['migrations_directory']
    path = os.path.join(directory, filename)
    if not os.path.isdir(directory):
        os.makedirs(directory)
    if not os.path.exists(os.path.join(directory, '__init__.py')):
        with open(os.path.join(directory, '__init__.py'), 'w'):
            pass
    with open(path, 'w') as f:
        f.write("""\
# -*- coding: utf-8 -*-

def up(cursor):
    # TODO migration code
    pass


def down(cursor):
    # TODO rollback code
    pass
""")
    print('Generated migration script "{}"'.format(path))


def cli_loader(parser):
    parser.add_argument('migration_name')
    return cli_command
