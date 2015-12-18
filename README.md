# Cottage Labs Finance

Cottage Labs Accounting web application with OpenBooks / FreeAgent importer.

## Application structure

This app uses the Flask microframework as its base. It imports Magnificent Octopus, a Cottage Labs library of useful modules to do with running web apps and the various business domains we are engaged in, such as open data and scholarship/science.

The app relies on a PostgreSQL database as its data store.

It uses Flask-SQLAlchemy, enabling SQLAlchemy as the Object-Relational Mapping layer (and sometimes directly accesses the engine) to generate SQL CRUD operations and queries. It also uses Flask-Migrate, enabling the use of the Alembic library for writing and running migrations, and keeping the models used by the app in sync with the database schema. Note that Alembic does not maintain one single schema file as it is possible to rebuild the entire database from the model files (via SQLAlchemy analysing them). TODO how do things like indices and triggers get saved then, are they added directly into models?

Whenever you are wondering how to query, insert, update or delete something, you will find [the Flask-SQLAlchemy documentation](http://flask-sqlalchemy.pocoo.org/2.1/) useful. Often this will not be enough, as it's mostly just glue to enable using SQLAlchemy with less boilerplate code, so for advanced use you will need the [SQLAlchemy documentation itself](http://docs.sqlalchemy.org/en/rel_1_0/orm/index.html). All links in this Readme are to the documentation for the version of the library currently used by the app, so if you update any dependencies, do update this Readme.

Whenever you need to know how to do something related to database schema management and migrations, you will find [the Flask-Migrate documentation useful](http://flask-migrate.readthedocs.org/en/latest/). Note they only provide "latest" docs so type ```pip freeze | grep Flask-Migrate``` after activating the virtualenv to find out our current version in case they start providing old docs. It's only a thin wrapper around Alembic and [the Alembic documentation can be found here](http://alembic.readthedocs.org/en/rel_0_7/). This Readme makes an effort to give you the basics in the sections below as well. If you run into particular trouble, [the troubleshooting section of this blog post](http://www.chesnok.com/daily/2013/07/02/a-practical-guide-to-using-alembic/) has a good links related to common problems.

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

## Application development

### Changing submodules

If you need to change something in Magnificent Octopus or another submodule, go into the submodule's directory and checkout the relevant branch (octopus uses "develop", smaller libraries use "master" - check on github first). Make your changes and push (or make Pull Requests and wait for acceptance). Inform others if they're breaking changes so that if somebody else updates their app to a newer version of the library, they're aware of having to fix the breakage first.

### Applying other people's changes to submodules

If another developer updates one of the submodules and git status tells you so after a git pull, then run this

    git submodule update --recursive

If a new submodule gets added to the app or to one of the app's submodules (so 2 levels or more deep), then rerun the command from the Installation section to get the new submodule:

    git submodule update --init --recursive

### Changing the database - migrations

Add, change and remove model files as you wish under service/models.

Each model class (e.g. User) is in its own file/module (e.g. users.py). Therefore, make sure to make the model *classes* visible directly from the service.models package, so one can say ```from service.models import User``` rather than ```from service.models.users import User```. Edit ```service/models/__init__.py``` and follow the current examples to achieve this. Conversely, when you delete a model you will need to remove this import.

After making your changes, activate the virtualenv and (as usual from the root of the repository) run

    python service/manage.py db migrate

This will automatically generate a new migration for you. You are encouraged to check and edit the migration files to add things such as indices. Ideally try to stick to declaring everything possible in the models so it can be detected.

After modifying the migration if needed, you can now run it with

    python service/manage.py db upgrade

And downgrade with

    python service/manage.py db downgrade

Finally, the help output is very useful if you want to do something slightly different

    python service/manage.py db --help

[The Alembic tutorial](http://alembic.readthedocs.org/en/rel_0_7/tutorial.html#create-a-migration-script) is highly recommended. The sections above "Create a Migration Script" have already been done in this repo, but that section and all below it make a valuable read if you need to do more complex upgrading or downgrading.

Please note that Alembic cannot detect all changes you make to models, though it does pretty well when you are introducing a new model. See [the Alembic documentation on auto-generating migrations](http://alembic.readthedocs.org/en/rel_0_7/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect) on what Alembic can and cannot detect. Specifically changes to column types, column names and table names are not detected, those should be hand-edited into migrations.

### Loading the current schema without rerunning all migrations

    python service/manage.py db head  # eventually ... this little piece won't work yet and is under development at the moment