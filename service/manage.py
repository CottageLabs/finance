from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from octopus.core import app
from service.db import db
from service import models

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()