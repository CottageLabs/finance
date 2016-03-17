import json
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import sqlalchemy

from octopus.core import app, initialise
from service.db import db
from service.lib import Sync, util

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

EXAMPLES_FN_TEMPL = '{0}_example.json'

@manager.option(
    '-t', '--table',
    help='Table name to sync with OpenBooks. Syncs all tables if not specified.')
@manager.option(
    '-c', '--use-cache',
    dest='use_cache', default=False, action="store_true",
    help='Use the data currently available in JSON files at the root of '
         'the repo, do not connect to OpenBooks to perform sync.')
def sync(table='', use_cache=False):
    """
    Synchronises all DB tables with OpenBooks, or alternatively just 1
    table. Will drop/recreate table(s)!
    """

    if table:
        tables = [table]
    else:
        tables = db.metadata.tables.keys()

    if not use_cache:
        data = Sync.sync_fetch(table)  # will take care of "1 vs all" table
    else:
        data = {}
        for tname in tables:
            data[tname] = json.loads(util.load(EXAMPLES_FN_TEMPL.format(tname)))

    for tname in tables:
        tobj = util.get_tableobj_by_name(tname)
        tobj.drop(bind=db.engine)
        tobj.create(bind=db.engine)
        Sync.sync_write_table(tname, data[tname])


@manager.option(
    '-t', '--table',
    help='Fetch data from OpenBooks into <table name>.json in the root '
         'of the local repo. Fetches samples for all tables if not specified.')
def refresh_local_examples(table=''):
    """
    Fetch data from OpenBooks about a specific table or all tables.
    Written (with overwrite!) into <table name>.json in the root of
    the local repo for use during development, or with the
    check_models_in_sync_with_fa_api task.
    """
    data = Sync.sync_fetch(table)
    for key, value in data.iteritems():
        # note we're also unpacking the data here, so we get lists
        # directly in the example files rather than e.g. {'users': [...]}
        util.save_overwrite(EXAMPLES_FN_TEMPL.format(key), json.dumps(value, indent=2))


@manager.option(
    '-t', '--table',
    help='Fetch data sample and check for one specific model corresponding '
         'to the passed table name. Does it for all models/tables if not specified.')
@manager.option(
    '-c', '--use-cache',
    dest='use_cache', default=False, action="store_true",
    help='Use the data currently available in JSON files at the root of '
         'the repo, do not connect to OpenBooks to refresh them.')
def check_models_in_sync_with_fa_api(table='', use_cache=False):
    """
    Fetch data from OpenBooks about a specific table or all tables.
    Note any current <table name>.json data is overwritten.
    Then this checks whether all the colums we've declared in our models
    still exist in the OpenBooks API responses.
    """
    if not use_cache:
        refresh_local_examples(table)

    if table:
        checks = [table]
    else:
        checks = db.metadata.tables.keys()

    for tablename in checks:
        cache_name = EXAMPLES_FN_TEMPL.format(tablename)
        try:
            api_sample = json.loads(util.load(cache_name))
        except IOError as e:
            raise IOError(
                'File {0} does not exist. Please run this command without '
                'the -c flag to connect to the API and generate {0}.'
                .format(cache_name)
            )
        except ValueError as e:
            raise ValueError(
                'Contents of {0} are invalid JSON. Please run this '
                'command without the -c flag to connect to the API and '
                'regenerate {0}'.format(cache_name)
            )

        detected_differences = False

        api_fields = set()
        for obj in api_sample:
            api_fields |= set(obj.keys())

        mclass = util.get_model_class_by_tablename(tablename)

        # get a list of database fields present in the model
        model_fields = []
        for attr in dir(mclass):
            is_db_field = isinstance(getattr(mclass, attr), sqlalchemy.orm.attributes.InstrumentedAttribute)
            if is_db_field:
                model_fields.append(attr)

        # check for fields the API has that we do not
        for field in api_fields:
            if not hasattr(mclass, field):
                app.logger.warn('{0} does not have field {1} present in API.'
                                .format(mclass.__name__, field))
                detected_differences = True

        # check for fields our models have, but the API does not
        for mfield in model_fields:
            if mfield not in api_fields:
                app.logger.warn('{0} has an attribute {1} NOT present in API.'
                                .format(mclass.__name__, mfield))
                detected_differences = True

        if not detected_differences:
            app.logger.info('No differences detected between {0} and API'.format(tablename))

if __name__ == '__main__':
    manager.run()
