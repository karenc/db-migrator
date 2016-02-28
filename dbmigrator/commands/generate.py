# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

import os

from ..utils import timestamp


__all__ = ('cli_loader',)


def cli_command(migration_name='', **kwargs):
    filename = '{}_{}.py'.format(timestamp(), migration_name)
    directory = kwargs['migrations_directory']
    if not directory:
        raise Exception('migrations directory undefined')
    if len(directory) > 1:
        raise Exception('more than one migrations directory specified')
    directory = directory[0]
    path = os.path.join(directory, filename)
    if not os.path.isdir(directory):
        os.makedirs(directory)
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
