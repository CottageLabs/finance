# class to get get data from OpenBooks

import httplib2
import json
from oauth2client import file, client, tools


class Sync():

    SCOPES = 'CottageLabsFinance'
    CLIENT_SECRET_FILE = 'config/openbooks_secret.json'
    STORAGE_SECRET_FILE = 'config/openbooks_secret_storage.json'
    BASE_URL = "https://api.freeagent.com/v2/"
    JSON_HEADERS = { 'Accept': 'application/json', 'Content-Type': 'application/json; charset=UTF-8' }


    def __init__(self):
        print "test1"

        #try:
        #    print "test2"
        #    import argparse
        #    print "test3"
        #    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        #    print "test4"
        #except ImportError:
        #    flags = None
        #    print "test5"
        #print "test6"




        store = file.Storage(self.STORAGE_SECRET_FILE)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:
                credentials = tools.run(flow, store)



        # apply credentials to http instance
        self.http = httplib2.Http()
        self.http = credentials.authorize(self.http)

    def get_data(self, method, querystring=""):
        return json.loads(self.http.request("{0}{1}{2}".format(self.BASE_URL, method, querystring), headers=self.JSON_HEADERS)[1])


    def get_data_batch(self, method, subquery, page, per_page):
        querystring="?"
        if subquery:
            querystring += subquery + "&"
        querystring += "page={0}&per_page={1}".format(page, per_page)
        return self.get_data(method, querystring)


    def get_data_paged(self, method, subquery=""):
        page=1
        per_page=100
        data = []

        while True:
            batch = self.get_data_batch(method, subquery, page, per_page)[method]
            if len(batch) > 0:
                data.extend(batch)
                page += 1
            else:
                break
        return data