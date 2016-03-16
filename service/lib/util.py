import sqlalchemy_utils
from service.db import db


def get_model_class_by_tablename(table):
    return sqlalchemy_utils.get_class_by_table(db.Model, db.metadata.tables[table])
