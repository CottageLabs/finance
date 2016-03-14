import sys
from setuptools import setup, find_packages

setup(
    name = 'Cottage Labs Finance',
    version = '1.0.0',
    packages = find_packages(),
    install_requires = [
        "octopus==1.0.0",
        "esprit",
        "Flask",
        "psycopg2==2.6.1",
        "Flask-SQLAlchemy==2.1",
        "Flask-Migrate==1.6.0",
        "sqlalchemy-utils==0.31.4",
        "Flask-OAuthlib==0.9.2",
        "Flask-Script==2.0.5",
        "oauth2client==2.0.1",
        # for deployment
        "gunicorn",
        "newrelic",
    ] + (["setproctitle"] if "linux" in sys.platform else []),
    url = 'http://cottagelabs.com/',
    author = 'Cottage Labs',
    author_email = 'us@cottagelabs.com',
    description = 'Cottage Labs Accounting web application with OpenBooks / FreeAgent importer.',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Apache v2',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
)
