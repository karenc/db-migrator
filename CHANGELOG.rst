CHANGELOG
---------

0.1.4 (2016-05-12)
------------------
 - Change ``dbmigrator list`` to list version and migration name separately

0.1.3 (2016-04-19)
------------------

 - Separate cli tests into different test cases
 - Change test config to use the travis database
 - Change logger.warn to logger.warning
 - Add test case for cli verbose option
 - Add tests for ``dbmigrator list``
 - Add CLI init test case for multiple contexts
 - Add travis and coveralls badges to README
 - Move cli.main import to base test case
 - Refactor code for marking a migration as completed or not
 - Add ``mark`` command for marking a migration as completed or not
 - Add tests for the ``mark`` command
 - Update README with example usage for the ``mark`` command

0.1.2 (2016-03-18)
------------------

 - :bug: Fix ``list`` to not explode when no migrations directories are given
 - Log warning message for ``list`` if schema_migrations table doesn't exist
 - Change ``--verbose`` to set the logger level to debug
 - Add test for utils.timestamp
 - Add test for utils.rollback_migration
 - Add test for utils.run_migration
 - Add test for utils.get_pending_migrations
 - Add test for utils.get_migrations
 - Add test for utils.import_migration
 - Make ``dbmigrator generate`` generate pep8 compliant code
 - Fix ``dbmigrator generate`` migrations directory lookup
 - Add test for utils.with_cursor
 - Add test for utils.get_settings_from_config
 - Add integration tests with test packages
 - Add pep8 to travis
 - Add a logger for dbmigrator that writes to stdout
 - Change version information option to ``-V``
 - Sort migrations by their filename, not the full path

0.1.1 (2016-02-24)
------------------

 - Stop changing schema_migrations data if the table already exists
 - Rewrite ``--version`` to use argparse version action
 - Add unit test for ``--version``
 - Add travis CI configuration file
 - Fix default context (working directory) being a string instead of a list

0.1.0 (2016-02-12)
------------------

 - Allow multiple migrations directories / context to be specified
 - Add --verbose which prints the configuration used by dbmigrator
 - Use datetime ``utcnow`` instead of ``now`` for timestamps
 - Add ``--version`` to show the version of db-migrator installed

0.0.7 (2016-02-10)
------------------

 - Add option ``--context`` to dbmigrator in order to load entry points
 - Raise error if config file is specified but not found

0.0.6 (2016-02-08)
------------------

 - Fix missing migrations directory the "init" command

0.0.5 (2016-02-08)
------------------

 - Include CHANGELOG in distribution's manifest

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

