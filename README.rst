DB Migrator
===========

.. image:: https://travis-ci.org/karenc/db-migrator.svg?branch=master
   :target: https://travis-ci.org/karenc/db-migrator

.. image:: https://coveralls.io/repos/github/karenc/db-migrator/badge.svg?branch=master
   :target: https://coveralls.io/github/karenc/db-migrator?branch=master

generate
--------

Example usage::

    dbmigrator generate add_id_to_users

generates a file called ``migrations/20151217170514_add_id_to_users.py``
with content::

    def up(cursor):
        # TODO migration code
        pass

    def down(cursor):
        # TODO rollback code
        pass


To set the migrations directory using an entry point, in mymodule ``setup.py``::

    setup(
        ...
        entry_points={
            'dbmigrator': [
                'migrations_directory = mymodule.main:migrations_directory',
                ],
            },
        )

**Important note**: For the settings from ``setup.py`` to be picked up, before
running ``dbmigrator``, first run ``python setup.py develop`` or
``python setup.py install``.

Then in ``mymodule/main.py``::

    import os

    migrations_directory = '{}/sql/migrations'.format(
        os.path.abspath(os.path.dirname(__file__)))

or::

    import os

    def migrations_directory():
        return '{}/sql/migrations'.format(
            os.path.abspath(os.path.dirname(__file__)))


init
----

Example usage::

    dbmigrator --db-connection-string='postgres://dbuser@localhost/dbname' init

or with a config file, ``development.ini``, that looks like this::

    [app:main]
    db-connection-string = postgres://dbuser@localhost/dbname

Run the command::

    dbmigrator --config=development.ini init


list
----

Example usage::

    $ dbmigrator list
    name                      | is applied | date applied
    ----------------------------------------------------------------------
    20151217170514_add_id_to_   True         2016-01-31 00:15:01.692570+01:00
    20151218145832_add_karen_   False               
    20160107200351_blah         False               


migrate
-------

Example usage:

With two migrations in the migrations directory,

``migrations/20151217170514_add_id_to_users.py``::

    def up(cursor):
        # TODO migration code
        pass

    def down(cursor):
        # TODO rollback code
        pass

and

``migrations/20151218145832_add_karen_to_users.py``::

    def up(cursor):
        cursor.execute('ALTER TABLE users ADD COLUMN karen TEXT')

    def down(cursor):
        cursor.execute('ALTER TABLE users DROP COLUMN karen')

To run the migrations::

    $ dbmigrator migrate
    Running migration 20151217170514 add_id_to_users

    Running migration 20151218145832 add_karen_to_users
    ---
    +++
    @@ -4005,21 +4005,22 @@
         first_name text,
         firstname text,
         last_name text,
         surname text,
         full_name text,
         fullname text,
         suffix text,
         title text,
         email text,
         website text,
    -    is_moderated boolean
    +    is_moderated boolean,
    +    karen text
     );

     ALTER TABLE public.users OWNER TO rhaptos;

     --
     -- Name: abstractid; Type: DEFAULT; Schema: public; Owner: rhaptos
     --

     ALTER TABLE ONLY abstracts ALTER COLUMN abstractid SET DEFAULT nextval('abstracts_abstractid_seq'::regclass);

or to run migrations up to a specific version::

    $ dbmigrator migrate version=20151217170514
    Running migration 20151217170514 add_id_to_users

if all migrations have already been run::

    $ dbmigrator migrate
    No pending migrations.  Database is up to date.

rollback
--------

Example usage:

With two migrations in the migrations directory,

``migrations/20151217170514_add_id_to_users.py``::

    def up(cursor):
        # TODO migration code
        pass

    def down(cursor):
        # TODO rollback code
        pass

and

``migrations/20151218145832_add_karen_to_users.py``::

    def up(cursor):
        cursor.execute('ALTER TABLE users ADD COLUMN karen TEXT')

    def down(cursor):
        cursor.execute('ALTER TABLE users DROP COLUMN karen')

Make sure the database is up to date::

    $ dbmigrator migrate
    No pending migrations.  Database is up to date.

Now rollback the last migration::

    $ dbmigrator rollback
    Rolling back migration 20151218145832 add_karen_to_users
    ---
    +++
    @@ -4005,22 +4005,21 @@
         first_name text,
         firstname text,
         last_name text,
         surname text,
         full_name text,
         fullname text,
         suffix text,
         title text,
         email text,
         website text,
    -    is_moderated boolean,
    -    karen text
    +    is_moderated boolean
     );

     ALTER TABLE public.users OWNER TO rhaptos;

     --
     -- Name: abstractid; Type: DEFAULT; Schema: public; Owner: rhaptos
     --

     ALTER TABLE ONLY abstracts ALTER COLUMN abstractid SET DEFAULT nextval('abstracts_abstractid_seq'::regclass);

To rollback the last 2 migrations::

    $ dbmigrator rollback --steps=2
    Rolling back migration 20151218145832 add_karen_to_users
    ---
    +++
    @@ -4005,22 +4005,21 @@
         first_name text,
         firstname text,
         last_name text,
         surname text,
         full_name text,
         fullname text,
         suffix text,
         title text,
         email text,
         website text,
    -    is_moderated boolean,
    -    karen text
    +    is_moderated boolean
     );

     ALTER TABLE public.users OWNER TO rhaptos;

     --
     -- Name: abstractid; Type: DEFAULT; Schema: public; Owner: rhaptos
     --

     ALTER TABLE ONLY abstracts ALTER COLUMN abstractid SET DEFAULT nextval('abstracts_abstractid_seq'::regclass);

    Rolling back migration 20151217170514 add_id_to_users

mark
----

Example usage::

    $ dbmigrator --config=development.ini --migrations-directory=migrations/ list
    name                      | is applied | date applied
    ----------------------------------------------------------------------
    20151217170514_add_id_to_   True         2016-01-31 00:15:01.692570+01:00
    20151218145832_add_karen_   False               
    20160107200351_blah         False               

    $ dbmigrator --config=development.ini --migrations-directory=migrations/ mark -f 20151217170514
    Migration 20151217170514 marked as not been run

    $ dbmigrator --config=development.ini --migrations-directory=migrations/ list
    name                      | is applied | date applied
    ----------------------------------------------------------------------
    20151217170514_add_id_to_   False               
    20151218145832_add_karen_   False               
    20160107200351_blah         False               
