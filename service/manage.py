from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from octopus.core import app
from service.db import db
from service import models
from service.lib.sync import Sync


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
#manager.add_command('openbooks', OpenbooksCommand)

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
def synchronise(table):
    """
    Synchronises the specified table with OpenBooks
    """
    print "Synchronising table:", table

    sync = Sync()
    data = sync.get_data_paged(table)
    print data





if __name__ == '__main__':
    manager.run()