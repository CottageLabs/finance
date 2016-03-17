import sqlalchemy_utils
from service.db import db


def get_tableobj_by_name(tablename):
    return db.metadata.tables[tablename]


def get_model_class_by_tablename(table):
    return sqlalchemy_utils.get_class_by_table(db.Model, get_tableobj_by_name(table))


def load(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    return content


def save_overwrite(filename, content):
    with open(filename, 'wb') as o:
        o.write(content)
