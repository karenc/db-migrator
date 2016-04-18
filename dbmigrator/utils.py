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
import datetime
import difflib
import functools
import glob
import os
import pkg_resources
import psycopg2
import re
import sys
import subprocess

from . import logger


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


def get_schema_versions(cursor, versions_only=True, raise_error=True):
    try:
        cursor.execute('SELECT * FROM schema_migrations ORDER BY version')
        for i in cursor.fetchall():
            if versions_only:
                yield i[0]
            else:
                yield i
    except psycopg2.ProgrammingError as e:
        if raise_error:
            raise
        logger.warning(str(e))
        logger.warning('You may need to run "dbmigrator init" to create the '
                       'schema_migrations table')


def get_pending_migrations(migration_directories, cursor, import_modules=False,
                           up_to_version=None):
    migrated_versions = list(get_schema_versions(cursor))
    if up_to_version and up_to_version in migrated_versions:
        raise StopIteration
    migrations = list(get_migrations(migration_directories, import_modules))
    versions = [m[0] for m in migrations]
    if up_to_version:
        try:
            migrations = migrations[:versions.index(up_to_version) + 1]
        except ValueError:
            raise Exception('Version "{}" not found'.format(up_to_version))
    for migration in migrations:
        version = migration[0]
        if version not in migrated_versions:
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
                             n=10))))


def run_migration(cursor, version, migration_name, migration):
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
    if completed:
        cursor.execute('INSERT INTO schema_migrations VALUES (%s)', (version,))
    else:
        cursor.execute('DELETE FROM schema_migrations WHERE version = %s',
                       (version,))
