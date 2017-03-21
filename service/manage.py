from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from octopus.core import app, initialise
from service.database import db, FA_API_TABLES
from service.lib import Sync, CompareAPI2Models, util

initialise()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# # TODO these need to be customised for our environment and can't run as they are
# # the gist is present though. my_metadata is SQLAlchemy's analysis of our models.
# # engine is db.engine (from service.db import db).
# # TODO this should probably just be part of service/manage.py so you
# # can say python service/manage.py db head
#
# ### Alembic instructions for complete DB schema load without migrations
# # start an interactive Python shell at root of repo
# # inside of a "create the database" script, first create tables
# my_metadata.create_all(engine)
#
# # then, load the Alembic configuration and generate the
# # version table, "stamping" it with the most recent rev:
# from alembic.config import Config
# from alembic import command
# alembic_cfg = Config("migrations/alembic.ini")   # path modified to suit us
# command.stamp(alembic_cfg, "head")


@manager.command
def refresh_oauth():
    """
    Force refresh OAuth credentials.
    """
    Sync.refresh_oauth_creds()


@manager.option(
    '-t', '--table',
    help='Table name to sync with OpenBooks. Syncs all tables if not specified.')
@manager.option(
    '-c', '--use-cache',
    dest='use_cache', default=False, action="store_true",
    help='Use the data currently available in the cache, '
         'do not connect to OpenBooks to perform sync.')
@manager.option(
    '-r', '--refresh-cache',
    dest='refresh_cache', default=True, action="store_true",
    help='Write the fresh data from OpenBooks (if -c was not used) '
         'to the cache while performing the sync.')
def sync(table='', use_cache=False, refresh_cache=True):
    """
    Synchronises all DB tables with OpenBooks, or alternatively just 1
    table. Will drop/recreate table(s)!
    """

    if table:
        tables = [table]
    else:
        tables = FA_API_TABLES.keys()

    if not use_cache:
        data = Sync.sync_fetch(table)  # will take care of "1 vs all" table
        # update the cache with the fresh data
        for tname, tdata in data.iteritems():
            util.write_cache(tname, tdata)
    else:
        data = {}
        for tname in tables:
            data[tname] = util.read_cache(tname)

    # remove extra info from API responses - the models only accept
    # what they've got declared as fields, which is sensible.
    for tname in tables:
        data[tname] = CompareAPI2Models.trim_api_response_to_model(tname, data[tname])
        tobj = util.get_tableobj_by_name(tname)
        tobj.drop(bind=db.engine)
        tobj.create(bind=db.engine)
        Sync.sync_write_table(tname, data[tname])


@manager.option(
    '-t', '--table',
    help='Table name verify. Verifies all imported tables if not specified.')
def verify_sync_against_cache(table=''):
    """
    Verify that data in tables sourced from OpenBooks has been imported
    correctly and successfully. Only verifies data in the database
    against the local cache, so it is most useful (and mainly intended
    to be used) immediately after using the sync command.

    For now this just does a count of all records in a table vs. the
    same records in the cache.
    """
    if table:
        tables = [table]
    else:
        tables = FA_API_TABLES.keys()

    data = {}
    for tname in tables:
        data[tname] = util.read_cache(tname)
        assert len(data[tname]) == util.get_model_class_by_tablename(tname).query.count()
        app.logger.info('Data in table {0} matches cache.'.format(tname))


@manager.option(
    '-t', '--table',
    help='Fetch data from OpenBooks into the cache directory. '
         'Fetches data for all tables if not specified.')
def refresh_cache(table=''):
    """
    Fetch data from OpenBooks about a specific table or all tables.
    Written (with overwrite!) into <table name>.json in the root of
    the local repo for use during development, or with the
    check_models_in_sync_with_fa_api task.
    """
    data = Sync.sync_fetch(table)
    for tname, tdata in data.iteritems():
        util.write_cache(tname, tdata)


@manager.option(
    '-t', '--table',
    help='Fetch data sample and check for one specific model corresponding '
         'to the passed table name. Does it for all models/tables if not specified.')
@manager.option(
    '-c', '--use-cache',
    dest='use_cache', default=False, action="store_true",
    help='Use the data currently available in the cache, '
         'do not connect to OpenBooks to refresh them.')
def check_models_in_sync_with_fa_api(table='', use_cache=False):
    """
    Fetch data from OpenBooks about a specific table or all tables.
    Note any current <table name>.json data is overwritten.
    Then this checks whether all the colums we've declared in our models
    still exist in the OpenBooks API responses.
    """
    if not use_cache:
        refresh_cache(table)

    if table:
        checks = [table]
    else:
        checks = FA_API_TABLES.keys()

    for tablename in checks:
        api_sample = util.read_cache(tablename)

        CompareAPI2Models.cmp_api2model(tablename, api_sample)


if __name__ == '__main__':
    manager.run()
