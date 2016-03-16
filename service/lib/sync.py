# class to get get data from OpenBooks

import httplib2
import json
from oauth2client import file, client, tools
from octopus.core import app

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
                break

            if method not in raw:
                app.logger.warn(
                    'Assumption made about FreeAgent API that it has an '
                    'envelope wrapping around all results with '
                    '{<method_name>: [<results>]} is not holding. Please '
                    'double-check documentation for getting {0} data and '
                    'fix code. Skipping {0}. Was on page {1}.'
                    .format(method, page))
                break

            batch = raw[method]

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
