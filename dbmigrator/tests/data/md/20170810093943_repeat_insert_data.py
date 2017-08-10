# -*- coding: utf-8 -*-

import os


def should_run(cursor):
    return os.path.exists('insert_data.txt')


def up(cursor):
    with open('insert_data.txt') as f:
        data = f.read()
    cursor.execute('INSERT INTO a_table VALUES (%s)', (data,))


def down(cursor):
    with open('insert_data.txt') as f:
        data = f.read()
    cursor.execute('DELETE FROM a_table WHERE name = %s', (data,))
