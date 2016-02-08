CHANGELOG
---------

0.0.4 (2016-02-08)
------------------

 - Show warning message instead of error if migrations directory is undefined
 - Add CHANGELOG

0.0.3 (2016-02-08)
------------------

 - Return error if migrations directory is undefined

0.0.2 (2016-02-03)
------------------

 - Fix invalid rst in README
 - Update setup.py description and long_description
 - Update setup.py to include README as the description and fix url
 - Update README and cli after removing default value for config file
 - Remove default config path (development.ini)
 - Add dbmigrator list command
 - Fix dbmigrator rollback to stop if there are no migrations to rollback
 - Print message after initializing schema migrations
 - Add note to run ``python setup.py install`` if using entry points
 - Add migrations directory setting from setup.py entry point in README
 - Update command names for init and generate in README
 - Get settings from setup.py entry points
 - Remove __init__.py generation in migrations directory
 - Add option version to dbmigrator init for setting the initial version
 - Rename "generate_migration" command to "generate"
 - Rename "init_schema_migrations" command to "init"
 - Change the way migrations are imported so it works in python2
 - Add "applied" timestamp to schema migrations table
 - Add ``# -*- coding: utf-8 -*-`` to the top of generated migration files
 - Add README
 - Add command "rollback" to rollback migrations
 - Add command "migrate" to run pending migrations
 - Add migrations to table when running init_schema_migrations
 - Add command for creating the schema migrations table
 - Create dbmigrator cli and "generate_migration" command
 - Create dbmigrator python package

