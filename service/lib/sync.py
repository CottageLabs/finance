# class to get get data from OpenBooks

import httplib2
import json
import sqlalchemy_utils
from oauth2client import file, client, tools
from octopus.core import app, initialise
from service.db import db
from service.lib import util

class Sync(object):

    SCOPES = 'CottageLabsFinance'
    CLIENT_SECRET_FILE = 'config/openbooks_secret.json'
    STORAGE_SECRET_FILE = 'config/openbooks_secret_storage.json'
    BASE_URL = "https://api.freeagent.com/v2/"
    JSON_HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json; charset=UTF-8'}
    DATA_REQUIRING_BANK_ACC = ['bank_transactions', 'bank_transaction_explanations']

    def __init__(self):
        store = file.Storage(self.STORAGE_SECRET_FILE)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            credentials = tools.run_flow(flow, store)

        # apply credentials to http instance
        self.http = httplib2.Http()
        self.http = credentials.authorize(self.http)

    @staticmethod
    def sync_prep():
        initialise()

    @classmethod
    def sync_fetch(cls, table=''):
        if table:
            app.logger.info("Fetching data from API for table: %s" % table)
        else:
            app.logger.info("Fetching data from API for all tables.")

        s = cls()
        data = {}

        if table:
            data[table] = s.get_one_table(table)
        else:
            cls.sync_prep()
            if len(db.metadata.tables.keys()) == 0:
                app.logger.critical('No tables detected by SQLAlchemy! '
                                    'Can\'t fetch. Stopping.')
                return {}

            for table_name in db.metadata.tables.keys():
                data[table_name] = s.get_one_table(table_name)

        return data

    @classmethod
    def sync_write_table(cls, table, data):
        if table:
            app.logger.info("Writing data to DB for table: %s" % table)
        else:
            app.logger.info("Writing data to DB for all tables.")

        for obj in data:
            # look up sqlalchemy Table obj by the table name we have,
            # then look up the model class corresponding to that table
            mclass = util.get_model_class_by_tablename(table)

            modeli = mclass(**obj)
            db.session.add(modeli)

        db.session.commit()

    def get_data(self, method, querystring=""):
        app.logger.debug("Requesting {0}{1}{2} with headers:\n{3}"
                         .format(self.BASE_URL, method, querystring, self.JSON_HEADERS))
        return json.loads(self.http.request("{0}{1}{2}".format(self.BASE_URL, method, querystring), headers=self.JSON_HEADERS)[1])

    def get_data_batch(self, method, subquery, page, per_page):
        querystring = "?"
        if subquery:
            querystring += subquery + "&"
        querystring += "page={0}&per_page={1}".format(page, per_page)
        return self.get_data(method, querystring)

    def get_data_paged(self, method, subquery=""):
        page = 1
        per_page = 100
        data = []

        while True:
            if method == 'bank_transactions' and not subquery:
                raise ValueError(
                    "You must specify a subquery when asking for bank "
                    "transactions. Something like bank_account=' + bank_account[\"url\"]"
                    " where bank_account is the bank account you want to query."
                )
            raw = self.get_data_batch(method, subquery, page, per_page)
            if u'errors' in raw:
                app.logger.error("FreeAgent API returned errors:\n" + json.dumps(raw[u'errors']))
                return []

            if method not in raw:
                app.logger.error(
                    'Assumption made about FreeAgent API that it has an '
                    'envelope wrapping around all results (except '
                    'categories) with '
                    '{{<method_name>: [<results>]}} is not holding. Please '
                    'double-check documentation for getting {0} data and '
                    "fix code. Skipping {0}. Was on page {1}. "
                    "Response dump:\n\n{2}\n\nAn error occurred! "
                    .format(method, page, json.dumps(raw, indent=2)))
                return []

            batch = raw[method]
            if method == 'users':
                for user in batch:
                    user.pop('ni_number', '')  # throw away this private info

            if len(batch) > 0:
                data.extend(batch)
                page += 1
            else:
                break
        return data

    def get_one_table(self, table_name):
        if table_name in self.DATA_REQUIRING_BANK_ACC:
            accounts = self.get_one_table("bank_accounts")
            primary_account = self.get_primary_bank_acc(accounts)
            return self.get_data_paged(table_name, subquery='bank_account=' + primary_account["url"])

        if table_name == 'categories':
            # Paging doesn't work on the categories endpoint.
            # Specifically, it keeps returning the same data for
            # pages 1,2,3 etc. So we don't add paging info to request.
            raw = self.get_data(table_name)
            categories = []
            for cat_type in raw.keys():
                # flatten out the categories to 1 list, not several
                categories.extend(raw[cat_type])
            return categories

        return self.get_data_paged(table_name)

    @staticmethod
    def get_primary_bank_acc(bank_accounts):
        account = None
        for acc in bank_accounts:
            if acc['is_primary']:
                account = acc
        if not account:
            raise ValueError('No bank account is marked as primary in '
                             'FreeAgent API. Please double-check and fix.')
        return account
