import sqlalchemy_utils
from service.database import db, FA_API_TABLES


def get_tableobj_by_name(tablename):
    return FA_API_TABLES[tablename]


def get_model_class_by_tablename(table):
    mclass = sqlalchemy_utils.get_class_by_table(db.Model, get_tableobj_by_name(table))
    if not mclass:
        raise ValueError("Can't find model class for table name %s" % table)
    return mclass


def load(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    return content


def save_overwrite(filename, content):
    with open(filename, 'wb') as o:
        o.write(content)
