import json
import sqlalchemy_utils
from service.database import db, FA_API_TABLES

CACHE_FILENAME_TEMPL = 'cache/{0}.json'


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


def read_cache(tablename):
    cache_name = CACHE_FILENAME_TEMPL.format(tablename)
    try:
        return json.loads(load(cache_name))
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


def write_cache(tablename, data):
    cache_name = CACHE_FILENAME_TEMPL.format(tablename)
    try:
        return save_overwrite(cache_name.format(tablename), json.dumps(data, indent=2))
    except IOError as e:
        raise IOError(
            'Filesystem or permissions error writing to cache file {0}.'
            .format(cache_name)
        )
    except ValueError as e:
        raise ValueError(
            'Data passed in to write to {0} cannot be converted to JSON.'
            .format(cache_name)
        )
