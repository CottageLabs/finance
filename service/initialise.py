from octopus.core import app

def initialise():
    # if we are not to initialise the db, stop here
    if not app.config.get("INITIALISE_DATABASE", False):
        return

    # The database and a suitable user must have been created by this point
    # and a DB connection string including the db, user and pass must be
    # set in the app config somewhere (preferably a .gitignored local.cfg).
    # Something like:
    # SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://user:pass@localhost/database_name"

    from service.db import db
    from sqlalchemy_utils import database_exists, create_database

    if not database_exists(db.engine.url):
        app.logger.info('Database specified in config does not exist, attempting to create it now.')
        try:
            create_database(db.engine.url)
        except Exception as e:
            app.logger.error('Exception {0} while trying to create database specified in config. Make sure the DB user has sufficient rights to create databases, this ability is not usually granted by default. Or create the database manually and rerun the app.'.format(e.message))
    else:
        app.logger.info('Database specified in config already exists, not creating or modifying it during init.')

    from service import models  # initialise SQLAlchemy mappings with our models
