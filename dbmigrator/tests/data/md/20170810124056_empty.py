# -*- coding: utf-8 -*-

from dbmigrator import deferred


# Uncomment should_run if this is a repeat migration
def should_run(cursor):
    # TODO return True if migration should run
    return True


@deferred
def up(cursor):
    # TODO migration code
    pass


def down(cursor):
    # TODO rollback code
    pass
