#!/usr/bin/python

# Extract Cottage Labs finance data
# Now you can query OpenBooks like a boss!
# Written for Cottage Labs LLP accounting
# Martyn Whitwell 2015-02-11


import json
import urllib2
import os
import re
import psycopg2
import sys
import csv


FREE_AGENT_TOKEN = os.environ['FREE_AGENT_TOKEN'] # store your freeagent token  in an environment variable
BASE_URL = "https://api.freeagent.com/v2/"

def get_filename(method,subquery="",extension=".json"):
    if not os.path.exists("data"):
        os.makedirs("data")
    if subquery:
        return "data/{0}_{1}{2}".format(method, re.split('\/',subquery)[-1],extension)
    else:
        return "data/{0}{1}".format(method,extension)

    
def save_data(filename,data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def load_data(filename):
    data = None
    with open(filename) as infile:
        data = json.load(infile)
    return data
    
def get_data(method,querystring=""):
    request = urllib2.Request("{0}{1}{2}".format(BASE_URL,method,querystring), headers={"Accept" : "application/json", "Authorization" : "Bearer " + FREE_AGENT_TOKEN })
    return json.load(urllib2.urlopen(request))

def get_data_batch(method, subquery, page, per_page):
    querystring="?"
    if subquery:
        querystring += subquery + "&"
    querystring += "page={0}&per_page={1}".format(page, per_page)
    return get_data(method,querystring)


def get_paged_data(filename, method, subquery=""):
    page=1
    per_page=100
    data = []

    if (os.path.exists(filename)):
        print "skipping " + method
    else:
        print "loading " + method + " data from the API"
        while True:
            batch = get_data_batch(method, subquery, page, per_page)[method]
            if len(batch) > 0:
                data.extend(batch)
                page += 1
            else:
                break
        save_data(filename, data)
    return len(data)

def get_paged_data_and_load(cursor, method, subquery=""):
    filename = get_filename(method, subquery)
    get_paged_data(filename, method, subquery)
    load_table(filename, cursor, method)

def get_category_data_and_load(cursor, method, subquery=""):
    filename = get_filename(method, subquery)
    if (os.path.exists(filename)):
        print "skipping download for " + method
    else:
        print "loading " + method + " data from the API"
        data = get_data(method)
        save_data(filename, data)
    data_all_categories = load_data(filename)
    for key in data_all_categories.keys():        
        for row in data_all_categories[key]:
            sql = "INSERT INTO " + method + "(" + ",".join(row.keys()) + ") VALUES(" + ','.join(['%s']*len(row.keys())) + ")"
            cursor.execute(sql, row.values())

def get_csv_and_load(cursor, method, keys):
    filename = get_filename(method,"",".csv")
    with open(filename,'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            sql = "INSERT INTO " + method + "(" + ",".join(keys) + ") VALUES(" + ','.join(['%s']*len(keys)) + ")"
            cursor.execute(sql, row)
            
    
def load_table(filename, cursor, method):
    print "loading table: " + method
    data = load_data(filename)
    for row in data:
        if "attachment" in row:
            del row["attachment"] # we are ignoring attachments
        if "user" in row:
            del row["user"] # we are ignoring users
        if "ni_number" in row:
            del row["ni_number"] # we are ignoring NI numbers
        sql = "INSERT INTO " + method + "(" + ",".join(row.keys()) + ") VALUES(" + ','.join(['%s']*len(row.keys())) + ")"
        cursor.execute(sql, row.values())
    
        
def create_table(cursor, tablename, sql):
    print "recreating table: " + tablename
    cursor.execute("DROP TABLE IF EXISTS " + tablename)
    cursor.execute(sql)
    
def recreate_tables(cursor):
    create_table(cursor, "categories",
    """CREATE TABLE categories
        (
          url character varying(255) NOT NULL,
          allowable_for_tax boolean,
          auto_sales_tax_rate character varying(255),
          description character varying(255),
          nominal_code character varying(255),
          tax_reporting_name character varying(255),
          CONSTRAINT pk_categories PRIMARY KEY (url)
        )""")

    create_table(cursor, "bank_accounts",
    """CREATE TABLE bank_accounts
        (
          url character varying(255) NOT NULL,
          account_number character varying(255),
          bank_name character varying(255),
          bic character varying(255),
          created_at date,
          currency character varying(255),
          current_balance numeric(10,2),
          iban character varying(255),
          is_personal boolean,
          is_primary boolean,
          name character varying(255),
          opening_balance numeric(10,2),
          sort_code character varying(255),
          type character varying(255),
          updated_at date,
          CONSTRAINT pk_bank_accounts PRIMARY KEY (url)
        )""")
    
    create_table(cursor, "bank_transactions",
    """CREATE TABLE bank_transactions
        (
          url character varying(255) NOT NULL,
          bank_account character varying(255) NOT NULL,
          amount numeric(10,2),
          dated_on date,
          description character varying(255),
          is_manual boolean,
          unexplained_amount numeric(10,2),
          uploaded_at date,
          CONSTRAINT pk_bank_transactions PRIMARY KEY (url)
        )""")
    
    create_table(cursor, "bank_transaction_explanations",
    """CREATE TABLE bank_transaction_explanations
        (
          url character varying(255) NOT NULL,
          bank_transaction character varying(255) NOT NULL,
          bank_account character varying(255) NOT NULL,
          category character varying(255),
          dated_on date,
          description character varying(255),
          gross_value numeric(10,2),
          paid_bill character varying(255),
          paid_invoice character varying(255),
          paid_user character varying(255),
          receipt_reference character varying(255),
          sales_tax_rate numeric(10,2),
          CONSTRAINT pk_bank_transaction_explanations PRIMARY KEY (url)
        )""")

    create_table(cursor, "bills",
    """CREATE TABLE bills
        (
          url character varying(255) NOT NULL,
          category character varying(255) NOT NULL,
          project character varying(255),
          comments character varying(255),
          contact character varying(255),
          created_at date,
          dated_on date,
          due_on date,
          due_value numeric(10,2),
          paid_value numeric(10,2),
          reference character varying(255),
          sales_tax_rate numeric(10,2),
          sales_tax_value numeric(10,2),
          status character varying(255),
          total_value numeric(10,2),
          updated_at date,
          CONSTRAINT pk_bills PRIMARY KEY (url)
        )""")
    
    create_table(cursor, "contacts",
    """CREATE TABLE contacts
        (
          url character varying(255) NOT NULL,
          account_balance numeric(10,2),
          address1 character varying(255),
          address2 character varying(255),
          address3 character varying(255),
          billing_email character varying(255),
          charge_sales_tax character varying(255),
          contact_name_on_invoices boolean,
          country character varying(255),
          created_at date,
          email character varying(255),
          first_name character varying(255),
          is_deletable boolean,
          last_name character varying(255),
          locale character varying(255),
          mobile character varying(255),
          phone_number character varying(255),
          organisation_name character varying(255),
          postcode character varying(255),
          region character varying(255),
          status character varying(255),
          sales_tax_registration_number character varying(255),
          town character varying(255),
          updated_at date,
          uses_contact_invoice_sequence boolean,
          CONSTRAINT pk_contacts PRIMARY KEY (url)
        )""")

    create_table(cursor, "expenses",
    """CREATE TABLE expenses
        (
          url character varying(255) NOT NULL,
          category character varying(255),
          created_at date,
          currency character varying(255),
          dated_on date,
          description character varying(255),
          gross_value numeric(10,2),
          manual_sales_tax_amount numeric(10,2),
          native_gross_value numeric(10,2),
          native_sales_tax_value numeric(10,2),
          project character varying(255),
          receipt_reference character varying(255),
          sales_tax_rate numeric(10,2),
          sales_tax_value numeric(10,2),
          updated_at date,
          "user" character varying(255),
          CONSTRAINT pk_expenses PRIMARY KEY (url)
        )""")
    
    create_table(cursor, "invoices",
    """CREATE TABLE invoices
        (
          url character varying(255) NOT NULL,
          always_show_bic_and_iban boolean,
          comments character varying(1000),
          contact character varying(255),
          created_at date,
          currency character varying(255),
          dated_on date,
          discount_percent numeric(10,2),
          due_on date,
          due_value numeric(10,2),
          exchange_rate numeric(10,2),
          involves_sales_tax boolean,
          is_interim_uk_vat boolean,
          net_value numeric(10,2),
          omit_header boolean,
          paid_on date,
          paid_value numeric(10,2),
          payment_terms_in_days integer,
          po_reference character varying(255),
          project character varying(255),
          reference character varying(255),
          sales_tax_value numeric(10,2),
          show_project_name boolean,
          status character varying(255),
          total_value numeric(10,2),
          written_off_date date,
          updated_at date,
          CONSTRAINT pk_invoices PRIMARY KEY (url)
        )""")
    
    create_table(cursor, "projects",
    """CREATE TABLE projects
        (
          url character varying(255) NOT NULL,
          billing_period character varying(255),
          budget numeric(10,2),
          budget_units character varying(255),
          contact character varying(255),
          contract_po_reference character varying(255),
          created_at date,
          currency character varying(255),
          ends_on date,
          hours_per_day numeric(10,2),
          is_ir35 boolean,
          name character varying(255),
          normal_billing_rate numeric(10,2),
          starts_on date,
          status character varying(255),
          updated_at date,
          uses_project_invoice_sequence boolean,
          CONSTRAINT pk_projects PRIMARY KEY (url)
        )""")
        
    create_table(cursor, "users",
    """CREATE TABLE users
        (
          url character varying(255) NOT NULL,
          first_name character varying(255),
          last_name character varying(255),
          email character varying(255),
          role character varying(255),
          permission_level integer,
          opening_mileage numeric(10,2),
          created_at date,
          updated_at date,
          CONSTRAINT pk_users PRIMARY KEY (url)
        )""")
    
    create_table(cursor, "server_costs",
    """CREATE TABLE server_costs
        (
          project_name character varying(255) NOT NULL,
          value numeric(10,2),
          CONSTRAINT pk_server_costs PRIMARY KEY (project_name)
        )""")


def run():
    print "Extracting Cottage Labs finance data"
    print "Query OpenBooks like a boss!"
    
    connection = None    
    try:
        
        connection = psycopg2.connect(database='cottage_labs_finance', user='cottagelabs') 
        cursor = connection.cursor()
        
        recreate_tables(cursor)
        
        get_category_data_and_load(cursor, 'categories')
        
        get_paged_data_and_load(cursor, 'bank_accounts')
        bank_accounts = load_data(get_filename('bank_accounts'))
        for bank_account in bank_accounts:
            get_paged_data_and_load(cursor,'bank_transactions','bank_account=' + bank_account["url"])
            get_paged_data_and_load(cursor, 'bank_transaction_explanations','bank_account=' + bank_account["url"])
        
        get_paged_data_and_load(cursor, 'bills')
        get_paged_data_and_load(cursor, 'contacts')
        get_paged_data_and_load(cursor, 'expenses')
        get_paged_data_and_load(cursor, 'invoices')
        get_paged_data_and_load(cursor, 'projects')
        get_paged_data_and_load(cursor, 'users')
        
        get_csv_and_load(cursor, "server_costs", ["project_name","value"])
    
        connection.commit()
        
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e    
        sys.exit(1)
    
    
    finally:
    
        if connection:
            connection.close()
    print "All done."

run()


