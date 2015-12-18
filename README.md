# Cottage Labs Finance

Cottage Labs Accounting web application with OpenBooks / FreeAgent importer.

## Application structure

This app uses the Flask microframework as its base. It imports Magnificent Octopus, a Cottage Labs library of useful modules to do with running web apps and the various business domains we are engaged in, such as open data and scholarship/science.

The app relies on a PostgreSQL database as its data store.

It uses Flask-SQLAlchemy, enabling SQLAlchemy as the Object-Relational Mapping layer (and sometimes directly accesses the engine) to generate SQL CRUD operations and queries. It also uses Flask-Migrate, enabling the use of the Alembic library for writing and running migrations, and keeping the models used by the app in sync with the database schema. Note that Alembic does not maintain one single schema file as it is possible to simply issue some commands to rebuild the entire database:

    # TODO these need to be customised for our environment and can't run as they are
    # the gist is present though. my_metadata is SQLAlchemy's analysis of our models.
    # engine is db.engine (from service.db import db).
    # TODO this should probably just be part of service/manage.py so you
    # can say python service/manage.py db head

    ### Alembic instructions for complete DB schema load without migrations
    # start an interactive Python shell at root of repo
    # inside of a "create the database" script, first create tables
    my_metadata.create_all(engine)

    # then, load the Alembic configuration and generate the
    # version table, "stamping" it with the most recent rev:
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config("migrations/alembic.ini")   # path modified to suit us
    command.stamp(alembic_cfg, "head")

## Dependencies

The app uses the psycopg2 Postgres adapter, which does have some system package dependencies. On Linux you will need to install these Debian packages (or their equivalents on other distros)

    sudo apt-get install libxml2-dev libxslt-dev python-dev lib32z1-dev libpq-dev

libpq-dev contains postgres library "header" files. The rest are Magnificent Octopus system dependencies which have to do with the LXML library.

Mac OS X system dependency information is TODO.

We don't have information about libpq-dev for Windows. For LXML, Windows users can grab a precompiled one from http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml (go for version 3.x) and avoid installing the dependencies that way. Just make sure the virtual environment can see your precompiled version.

## Installation

Create your virtualenv and activate it. You will need to activate the virtualenv every time before you run anything inside the application.

    virtualenv finance
    source finance/bin/activate

Clone the project:

    cd finance
    mkdir src
    cd src
    git clone https://github.com/CottageLabs/finance.git
    # now you've got this repo at finance/src/finance
    # NOTE ALL COMMANDS BELOW ASSUME YOU ARE IN THIS DIRECTORY UNLESS OTHERWISE SPECIFIED

Get all the submodules

    cd finance
    git submodule update --init --recursive
    
This will initialise and clone the esprit and magnificent octopus libraries, and their submodules in turn.

Install the dependencies and this app:

    pip install -r requirements.txt
    
Create your local config

    touch local.cfg

Then you can override any config values that you need to.

Then, start your app with

    python service/web.py

If you want to specify your own root config file, you can use

    APP_CONFIG=path/to/rootcfg.py python service/web.py
    
## Configuration

You will need to have PostgreSQL running. You'll need to set:

    SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://pg_username:pg_password@localhost/pg_database"
    SQLALCHEMY_TRACK_MODIFICATIONS=False