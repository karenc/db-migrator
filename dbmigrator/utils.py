# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###

try:
    import configparser
except ImportError:
    # python 2
    import ConfigParser as configparser
from contextlib import contextmanager
import datetime
import difflib
import functools
import glob
import logging
import os
import pkg_resources
import re
from select import select
import sys
import subprocess

import psycopg2
from psycopg2.extensions import POLL_OK, POLL_READ, POLL_WRITE


logger = logging.getLogger('dbmigrator')
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(name)s (%(filename)s) - %(message)s'))
logger.addHandler(handler)


_settings = {}


def get_settings():
    return _settings


def set_settings(settings):
    global _settings
    _settings = settings


@contextmanager
def super_user():
    settings = get_settings()
    super_user = settings.get('super_user', 'postgres')
    with psycopg2.connect(settings['db_connection_string'],
                          user=super_user) as db_conn:
        with db_conn.cursor() as cursor:
            yield cursor


# psycopg2 / libpq doesn't respond to SIGINT (ctrl-c):
# https://github.com/psycopg/psycopg2/issues/333
# To get around this problem, using code from:
# http://initd.org/psycopg/articles/2014/07/20/cancelling-postgresql-statements-python/ # noqa
def wait_select_inter(conn):
    while 1:
        try:
            state = conn.poll()
            if state == POLL_OK:
                break
            elif state == POLL_READ:
                select([conn.fileno()], [], [])
            elif state == POLL_WRITE:
                select([], [conn.fileno()], [])
            else:
                raise conn.OperationalError(
                    'bad state from poll: {}'.format(state))
        except KeyboardInterrupt:
            conn.cancel()
            continue


def get_settings_from_entry_points(settings, contexts):
    context_settings = {}

    for context in contexts:
        entry_points = pkg_resources.get_entry_map(
            context, __package__).values()
        for entry_point in entry_points:
            setting_name = entry_point.name
            if settings.get(setting_name):
                # don't overwrite settings given from the CLI
                continue

            value = entry_point.load()
            if callable(value):
                value = value()

            old_value = context_settings.get(setting_name)
            if (old_value and old_value != value or
                    isinstance(old_value, list) and value not in old_value):
                if not isinstance(old_value, list):
                    context_settings[setting_name] = [old_value]
                context_settings[setting_name].append(value)
            else:
                context_settings[setting_name] = value

    for name, value in context_settings.items():
        settings[name] = value


def get_settings_from_config(filename, config_names, settings):
    config = configparser.ConfigParser()
    config.read(filename)
    for name in config_names:
        setting_name = name.replace('-', '_')
        if settings.get(setting_name):
            # don't overwrite settings given from the CLI
            continue

        for section_name in config.sections():
            try:
                value = config.get(section_name, name)
                settings[setting_name] = value
                break
            except configparser.NoOptionError:
                pass


def with_cursor(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not kwargs.get('db_connection_string'):
            raise Exception('db-connection-string missing')
        db_conn_str = kwargs.get('db_connection_string')
        with psycopg2.connect(db_conn_str) as db_conn:
            with db_conn.cursor() as cursor:
                return func(cursor, *args, **kwargs)
    return wrapper


def import_migration(path):
    dirname, basename = os.path.split(path)
    if dirname not in sys.path:
        sys.path.append(dirname)
    module_name = basename.rsplit('.', 1)[0]
    return __import__(module_name)


def get_migrations(migration_directories, import_modules=False, reverse=False):
    paths = [os.path.join(md, '*.py') for md in migration_directories]
    python_files = functools.reduce(
        lambda a, b: a + b,
        [glob.glob(path) for path in paths], [])
    for path in sorted(python_files,
                       key=lambda path: os.path.basename(path),
                       reverse=reverse):
        filename = os.path.basename(path)
        m = re.match('([0-9]+)_(.+).py$', filename)
        if m:
            version, migration_name = m.groups()
            if import_modules:
                yield version, migration_name, import_migration(path)
            else:
                yield version, migration_name


def get_schema_versions(cursor, versions_only=True, raise_error=True,
                        include_deferred=True, order_by='version'):
    try:
        cursor.execute('SELECT * FROM schema_migrations ORDER BY {}'
                       .format(order_by))
        for i in cursor.fetchall():
            if not include_deferred and i[1] is None:
                continue
            if versions_only:
                yield i[0]
            else:
                yield i
    except psycopg2.ProgrammingError as e:
        if raise_error:
            raise
        logger.warning(str(e))
        logger.warning('You may need to create the schema_migrations table: '
                       'dbmigrator init --help')


def get_pending_migrations(migration_directories, cursor, import_modules=False,
                           up_to_version=None):
    migrated_versions = {i[0]: i[1] or 'deferred'
                         for i in get_schema_versions(
                             cursor, versions_only=False)}

    migrations = list(get_migrations(migration_directories,
                                     import_modules=True))
    versions = [m[0] for m in migrations]
    if up_to_version:
        try:
            migrations = migrations[:versions.index(up_to_version) + 1]
        except ValueError:
            raise Exception('Version "{}" not found'.format(up_to_version))

    for migration in migrations:
        version, migration_name, mod = migration
        if not import_modules:
            migration = migration[:-1]
        if migrated_versions.get(version) != 'deferred':
            if hasattr(mod, 'should_run'):
                # repeat migrations are always included
                yield migration
            elif version not in migrated_versions:
                yield migration


def compare_schema(db_connection_string, callback, *args, **kwargs):
    old_schema = subprocess.check_output(
        ['pg_dump', '-s', db_connection_string]).decode('utf-8')
    callback(*args, **kwargs)
    new_schema = subprocess.check_output(
        ['pg_dump', '-s', db_connection_string]).decode('utf-8')
    print(''.join(list(
        difflib.unified_diff(old_schema.splitlines(True),
                             new_schema.splitlines(True),
                             n=10))).encode('utf-8'))


def run_migration(cursor, version, migration_name, migration):
    try:
        if not migration.should_run(cursor):
            print('Skipping migration {} {}: should_run is false'
                  .format(version, migration_name))
            return
    except AttributeError:
        # not a repeat migration
        pass
    print('Running migration {} {}'.format(version, migration_name))
    migration.up(cursor)
    mark_migration(cursor, version, True)
    cursor.connection.commit()


def rollback_migration(cursor, version, migration_name, migration):
    print('Rolling back migration {} {}'.format(version, migration_name))
    migration.down(cursor)
    mark_migration(cursor, version, False)
    cursor.connection.commit()


def timestamp():
    now = datetime.datetime.utcnow()
    return now.strftime('%Y%m%d%H%M%S')


def mark_migration(cursor, version, completed):
    if completed == 'deferred':
        cursor.execute('INSERT INTO schema_migrations (version, applied) '
                       'VALUES (%s, NULL)', (version,))
    elif completed:
        cursor.execute('INSERT INTO schema_migrations VALUES (%s)', (version,))
    else:
        cursor.execute('DELETE FROM schema_migrations WHERE version = %s',
                       (version,))
