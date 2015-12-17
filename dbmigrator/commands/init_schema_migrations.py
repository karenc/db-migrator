# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

from .. import utils


__all__ = ('cli_loader',)


@utils.with_cursor
def cli_command(cursor, migrations_directory='', **kwargs):
    cursor.execute("""\
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT NOT NULL
        )""")
    cursor.execute("""\
        DELETE FROM schema_migrations""")
    versions = []
    for version, name in utils.get_migrations(migrations_directory):
        versions.append((version,))
    cursor.executemany("""\
        INSERT INTO schema_migrations VALUES (%s)
        """, versions)


def cli_loader(parser):
    return cli_command
