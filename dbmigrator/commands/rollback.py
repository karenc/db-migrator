# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
"""Rollback a migration."""

from .. import logger, utils


__all__ = ('cli_loader',)


@utils.with_cursor
def cli_command(cursor, migrations_directory='', steps=1,
                db_connection_string='', **kwargs):
    migrated_versions = list(utils.get_schema_versions(
        cursor, include_deferred=False, order_by='applied'))
    logger.debug('migrated_versions: {}'.format(migrated_versions))
    if not migrated_versions:
        logger.info('No migrations to roll back.')
        return
    migrations = {version: (name, migration)
                  for version, name, migration in utils.get_migrations(
                      migrations_directory, import_modules=True,
                      reverse=True)}

    rolled_back = 0
    for version in reversed(migrated_versions):
        if version not in migrations:
            logger.info('Migration {} not found.'.format(version))
            break
        migration_name, migration = migrations[version]
        utils.compare_schema(db_connection_string,
                             utils.rollback_migration,
                             cursor,
                             version,
                             migration_name,
                             migration)
        rolled_back += 1
        if rolled_back >= steps:
            break

    if not rolled_back:
        logger.info('No migrations to roll back.')


def cli_loader(parser):
    parser.add_argument('--steps', metavar='N', default=1, type=int,
                        help='Roll back the last N migrations, default 1')
    return cli_command
