superset-clickhouse
=====================

ClickHouse dialect for SQLAlchemy for Superset.

Installation
------------

The package is installable through PIP::

   pip install superset-clickhouse

Usage
-----

The DSN format is similar to that of regular Postgres::

    >>> import sqlalchemy as sa
    >>> sa.create_engine('clickhouse://username:password@hostname:port/database')
    Engine('clickhouse://username:password@hostname:port/database')
    
For SSL add ssl parameter to URL::

    >>> import sqlalchemy as sa
    >>> sa.create_engine('clickhouse://username:password@hostname:port/database?ssl=True')
    Engine('clickhouse://username:password@hostname:port/database')

It implements a dialect, so there's no user-facing API.
