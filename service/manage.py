from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from octopus.core import app, initialise
from service.db import db
from service import models
from service.lib.sync import Sync

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


@manager.option('-t', '--table', help='Table name to sync with OpenBooks. Syncs all tables if not specified')
def sync(table=''):
    """
    Synchronises all DB tables with OpenBooks, or alternatively just 1
    table.

    :param table: optionally specify the name of the table to sync.
    """
    if table:
        app.logger.info("Synchronising table: %s" % table)
    else:
        app.logger.info("Synchronising all tables.")

    s = Sync()
    if len(db.metadata.tables.keys()) == 0:
        app.logger.warn('No tables detected by SQLAlchemy! Can\'t sync. Stopping.')
        return

    data = {}

    if table:
        data[table] = s.get_one_table(table)
    else:
        for table_name in db.metadata.tables.keys():
            data[table_name] = s.get_one_table(table_name)

    import json
    print json.dumps(data, indent=2)



if __name__ == '__main__':
    manager.run()