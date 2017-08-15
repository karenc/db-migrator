# -*- coding: utf-8 -*-


from dbmigrator import super_user


def up(cursor):
    with super_user() as super_cursor:
        super_cursor.execute('SELECT current_user')
        assert super_cursor.fetchone()[0] == 'postgres'


def down(cursor):
    # TODO rollback code
    pass
