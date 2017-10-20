# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2016, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
"""List migration versions, names, whether it has been applied and the date
applied."""

from .. import utils


__all__ = ('cli_loader',)


@utils.with_cursor
def cli_command(cursor, migrations_directory='', db_connection_string='',
                wide=False, sort='version', **kwargs):
    # version -> applied timestamp
    migrated_versions = dict(list(
        utils.get_schema_versions(cursor, versions_only=False,
                                  raise_error=False)))
    migrations = utils.get_migrations(migrations_directory,
                                      import_modules=True)

    if wide:
        migrations = list(migrations)
        name_width = max([len(name) for _, name, _ in migrations])
    else:
        name_width = 15

    name_format = '{:<%s}' % (name_width,)
    print('version        | {} | is applied | date applied'
          .format(name_format.format('name')))
    print('-' * 70)

    migrations = [(version, migration_name, migration,
                   migrated_versions.get(version, ''))
                  for version, migration_name, migration in migrations]
    if sort == 'applied':
        migrations.sort(key=lambda a: str(a[-1]) or 'None')

    name_format = '{: <%s}' % (name_width,)
    for version, migration_name, migration, applied_timestamp in migrations:
        deferred = utils.is_deferred(
            version, migration, migrated_versions)
        is_applied = deferred and 'deferred' or bool(applied_timestamp)
        if hasattr(migration, 'should_run'):
            is_applied = '{}*'.format(is_applied)
        print('{}   {}   {!s: <10}   {}'.format(
            version, name_format.format(migration_name[:name_width]),
            is_applied, applied_timestamp))


def cli_loader(parser):
    parser.add_argument('--wide', action='store_true',
                        dest='wide', default=False,
                        help='Display the full name of every migration')
    parser.add_argument(
        '--sort', default='version', choices=['version', 'applied'],
        help='Sort by migration "version" (default), or "applied" dates')
    return cli_command
