from flask.ext.sqlalchemy import SQLAlchemy
from octopus.core import app
from copy import deepcopy

db = SQLAlchemy(app)
from service import models  # initialise SQLAlchemy mappings with our models
__api_tables = db.metadata.tables.__reduce__()[1][0]

# remove all non-api tables from our temporary list
NON_FA_API_TABLE_NAMES = ['server_costs']
for tname in NON_FA_API_TABLE_NAMES:
    __api_tables.pop(tname, None)

FA_API_TABLES = __api_tables
