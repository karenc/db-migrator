# -*- coding: utf-8 -*-


def up(cursor):
    cursor.execute('CREATE TABLE a_table (name TEXT)')


def down(cursor):
    cursor.execute('DROP TABLE a_table')
