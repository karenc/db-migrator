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
def cli_command(cursor, **kwargs):
    cursor.execute("""\
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version TEXT NOT NULL
        )""")


def cli_loader(parser):
    return cli_command
