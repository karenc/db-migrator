# -*- coding: utf-8 -*-


# Uncomment should_run if this is a repeat migration
# def should_run(cursor):
#     # TODO return True if migration should run


def up(cursor):
    cursor.execute('CREATE TABLE a_table (name TEXT)')


def down(cursor):
    cursor.execute('DROP TABLE a_table')
