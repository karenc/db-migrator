# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
"""Run all pending migrations."""

from .. import logger, utils


__all__ = ('cli_loader',)


@utils.with_cursor
def cli_command(cursor, migrations_directory='', version='',
                db_connection_string='', run_deferred=False, **kwargs):
    pending_migrations = utils.get_pending_migrations(
        migrations_directory, cursor, import_modules=True,
        up_to_version=version, include_defers=True)

    migrated = False
    for version, migration_name, migration in pending_migrations:
        migrated = True
        utils.compare_schema(db_connection_string,
                             utils.run_migration,
                             cursor,
                             version,
                             migration_name,
                             migration,
                             run_deferred)

    if not migrated:
        logger.info('No pending migrations.  Database is up to date.')


def cli_loader(parser):
    parser.add_argument('--version',
                        help='Migrate database up to this version')
    parser.add_argument('--run-deferred',
                        action='store_true',
                        help='Also run the deferred migrations')
    return cli_command
